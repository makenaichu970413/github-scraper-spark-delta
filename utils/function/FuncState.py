from utils.function.FuncLog import StateManager
from concurrent.futures import as_completed


class StateManager:
    """
    Manages the state of scraping for a repository.
    """

    def __init__(self, repo_name: str, state_dir: str = "state"):
        self.repo_name = repo_name
        self.state_dir = state_dir
        os.makedirs(self.state_dir, exist_ok=True)
        self.state_file = os.path.join(self.state_dir, f"{repo_name}.json")
        self.state = self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading state file {self.state_file}: {e}")
                return self._initial_state()
        return self._initial_state()

    def _initial_state(self):
        return {
            "repo_name": self.repo_name,
            "contributors": {},  # key: contributor_url, value: { "status": "pending/success/error", "data": ... }
        }

    def save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Error saving state to {self.state_file}: {e}")

    def get_contributor_state(self, url):
        return self.state["contributors"].get(url, {"status": "pending"})

    def update_contributor_state(self, url, status, data=None):
        if url not in self.state["contributors"]:
            self.state["contributors"][url] = {}
        self.state["contributors"][url]["status"] = status
        if data is not None:
            self.state["contributors"][url]["data"] = data
        self.save_state()
