# Library
from bs4 import BeautifulSoup
import re
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import BaseModel

# ? Scrapper
from scraper.GitHub.ScrapeUser import scrape_user

# ? Utils
from utils.constant import (
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_PROCESS,
    THREAD_SUB_MAX_WORKER,
    REQUEST_RETRY_ATTEMPT,
)
from utils.function import FuncDBLogContributor as Log
from utils.function.FuncScrape import bs_select_one
from utils.function.FuncRequest import ethical_delay
from utils.models import TGitHubContributorLog, TGitHubUser


class DProcessContributor(BaseModel):
    data: TGitHubUser = TGitHubUser()
    error: str | None = None


class DScrapeContributors(BaseModel):
    data: list[TGitHubUser] = []
    total: int | None = None
    error: str | None = None


def process_contributor(
    url: str, i: int, total: int, repo_name: str
) -> DProcessContributor:

    result: DProcessContributor = DProcessContributor()

    label = f"{repo_name}_contributor"

    for attempt in range(REQUEST_RETRY_ATTEMPT):
        try:

            Log.upsert(props=TGitHubContributorLog(url=url, status=STATUS_PROCESS))

            result_user = scrape_user(url)
            data = result_user.data
            result.data = data

            if result_user.error:
                msg_error = f'❌[{i}/{total}] FAILED_SCRAPE in "process_contributor()" "{label}" "{url}" : {result_user.error}'
                result.error = msg_error
                raise Exception(msg_error)

            result.error = None
            print(f'✅[{i}/{total}] "{label}" : {data}')

            ethical_delay()  #! Critical delay for ethical web scraping

            break  #! Exit retry loop once success

        except Exception as err:
            logging.error(err)
            if attempt < REQUEST_RETRY_ATTEMPT:
                print(f"🔁[{attempt + 1}/{REQUEST_RETRY_ATTEMPT}] RETRYING : {err} ")
                ethical_delay()
                continue

    return result


def scrape_contributors(
    soup: BeautifulSoup, URLs: list[str], repo_name: str, repo_url: str
) -> DScrapeContributors:
    """Process contributor URLs and extract contributor data and total count."""
    result: DScrapeContributors = DScrapeContributors()

    total = len(URLs)
    data: list[TGitHubUser] = []

    records = [
        TGitHubContributorLog(url=url, repo_url=repo_url, repo_name=repo_name)
        for url in URLs
    ]
    print(f'Total "{len(records)}" contributor')
    for i, item in enumerate(records, start=1):
        print(f"{i}. {item}")

    # Insert all the contributors into DB
    Log.insert_batch(records, STATUS_PENDING)

    print(
        f'🚀MULTI_THREAD "{THREAD_SUB_MAX_WORKER}" in "scrape_contributors()" scraping "{total}"  ...'
    )
    with ThreadPoolExecutor(max_workers=THREAD_SUB_MAX_WORKER) as executor:
        # Create a future for each URL
        futures = {
            executor.submit(process_contributor, url, i, total, repo_name): (
                url,
                i,
                total,
            )
            for i, url in enumerate(URLs, start=1)
        }
        """
        futures = {
            <Future at 0x... state=running>: ("https://github.com/repo1", 0, 3)
            <Future at 0x... state=pending>: ("https://github.com/repo2", 1, 3)
            <Future at 0x... state=pending>: ("https://github.com/repo3", 2, 3)
        }
        """

        # ? Process results as they complete
        for future in as_completed(futures):
            url, i, total = futures[future]
            try:
                result_contributor = future.result()
                data.append(result_contributor.data)
                print("result_contributor: ", result_contributor)

                if result_contributor.error:
                    raise Exception(result_contributor.error)

                Log.upsert(TGitHubContributorLog(url=url, status=STATUS_COMPLETE))

            except Exception as err:
                logging.error(err)
                Log.upsert(
                    TGitHubContributorLog(url=url, error=str(err), status=STATUS_FAILED)
                )

    #! Set contributos to result after multi thread completed scrape
    result.data = data

    # Get total contributors
    contributors_total_el = bs_select_one(
        soup, 'a[href$="/graphs/contributors"] span.Counter'
    )
    if contributors_total_el:
        # Use regex to find the first number in the string
        match = re.search(r"\d+", contributors_total_el)
        if match:
            result.total = int(match.group())

    return result
