# Scraper
from scraper.GitHub import Scrape as ScraperGithub
from spark.GitHub import Spark as SparkGitHub

# Run with `-B`` flag to prevent "__pycache__/""
# python -B main.py


def GitHubETL():
    while True:
        print("\nMenu:")
        print("[1] Scrap Data")
        print("[2] Export Data into Delta Table")
        print("[3] Exit")
        choice = input("Enter your choice (1-3): ").strip()

        print(f"\n\n")
        if choice == "1":
            ScraperGithub.scrape()
        elif choice == "2":
            SparkGitHub.run()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":

    GitHubETL()
