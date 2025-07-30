# Library
import code
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime


# ? Scrapper
from scraper.GitHub.ReadInput import read_input
from scraper.GitHub.ScrapeRepo import scrape_repo
from scraper.GitHub.ScrapeErrorRepo import scrape_error_repo
from scraper.GitHub.ScrapeErrorContributors import scrape_error_contributors


# ? Utils
# Add this roject root to Python path before other imports
# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent))
from utils.constant import (
    REPORT_COUNT,
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PROCESS,
    THREAD_MAX_WORKER,
    REQUEST_RETRY_ATTEMPT,
)


from utils.function import FuncDBLogRepo as Log
from utils.function.FuncReport import github_report, github_report_repo
from utils.function.FuncRequest import ethical_delay
from utils.function.FuncFile import export_json
from utils.model.Sgithub import TGitHubRepo, TGitHubRepoLog


class DProcessGitHub(BaseModel):
    data: TGitHubRepo = TGitHubRepo()
    output: Path | None = None
    error: str | None = None


def process(url: str, i: int, total: int) -> DProcessGitHub:

    result: DProcessGitHub = DProcessGitHub()

    for attempt in range(REQUEST_RETRY_ATTEMPT):
        try:
            print(f'\n\n🤖[{i}/{total}] Scrapping "{url}" ...')

            Log.upsert(props=TGitHubRepoLog(url=url, status=STATUS_PROCESS))

            result_repo = scrape_repo(url)

            if result_repo.error:
                msg_error = (
                    f'❌[{i}/{total}] FAILED_SCRAPE in "process()" "{url}": {err}'
                )
                result.error = msg_error
                raise Exception(result_repo.error)

            data = result_repo.data
            result.data = data

            repo_name = data.repo_name
            json_data = data.model_dump_json(indent=2)
            output = export_json(
                data=json_data,
                filename=f"github_{repo_name}.json",
            )
            result.output = output

            result.error = None
            print(f'✅[{i}/{total}] "{repo_name}": {result}')

            ethical_delay()  #! Critical delay for ethical web scraping

            break  #! Exit retry loop once success

        except Exception as err:
            logging.error(err)
            if attempt < REQUEST_RETRY_ATTEMPT:
                print(f"🔁[{attempt + 1}/{REQUEST_RETRY_ATTEMPT}] RETRYING : {err} ")
                ethical_delay()
                continue

    return result


def scrape() -> None:

    # Handle the error record  whenever need to restart the record
    scrape_error_repo()

    scrape_error_contributors()

    URLs = read_input()

    total = len(URLs)
    start_time = datetime.now()
    count = 1

    if not total:
        github_report(start_time, completed=True)
        return

    """Scrape GitHub for repositories and user profiles"""

    # We'll use a thread pool with 5 workers to avoid overwhelming GitHub
    start_time = datetime.now()

    print(f'🚀MULTI_THREAD "{THREAD_MAX_WORKER}" in "scrape()" scraping "{total}"  ...')

    with ThreadPoolExecutor(max_workers=THREAD_MAX_WORKER) as executor:
        # Create a future for each URL
        futures = {
            executor.submit(process, url, i, total): (url, i, total)
            for i, url in enumerate(URLs, start=1)
        }
        """
        futures = {
            <Future at 0x... state=running>: ("https://github.com/repo1", 0, 3)
            <Future at 0x... state=pending>: ("https://github.com/repo2", 1, 3)
            <Future at 0x... state=pending>: ("https://github.com/repo3", 2, 3)
        }
        """

        # ? The loop body runs immediately for each completed future
        # ? Process results as they complete
        for future in as_completed(futures):
            url, i, total = futures[future]
            try:

                # Increment processed counter
                count += 1

                # Generate Report whenever N item complete whatever Success or Failed
                if count % REPORT_COUNT == 0:
                    github_report(start_time)

                result = future.result()
                if result.error:
                    raise Exception(result.error)

                # Log success with the output path string
                output = str(result.output) if result.output else ""
                Log.upsert(
                    props=TGitHubRepoLog(url=url, output=output, status=STATUS_COMPLETE)
                )

            except Exception as err:
                logging.error(err)
                Log.upsert(
                    props=TGitHubRepoLog(url=url, error=str(err), status=STATUS_FAILED)
                )

    # ? Generate Report whenever All Completed
    github_report(start_time, completed=True)
