# Library
import code
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from pydantic import BaseModel


# ? Scrapper
from scraper.GitHub import Scrape as ScraperGithub


# ? Utils
from utils.constant import (
    DB_NAME_REPO,
    STATUS_FAILED,
    STATUS_PROCESS,
    THREAD_MAX_WORKER,
)
from utils.function import FuncDBLogRepo as Log
from utils.model.Sgithub import TGitHubRepoLog


def scrape_error_repo() -> None:

    # Initialize DB When Start
    isDBInit = Log.init_table()
    if not isDBInit:
        return

    errors = Log.load([STATUS_FAILED, STATUS_PROCESS])
    total = len(errors)
    print(f'❌In "{DB_NAME_REPO}" found total errors "{total}"')
    for i, item in enumerate(errors, start=1):
        print(f"{i}. {item}")

    if not total:
        return

    print(
        f'\n🚀MULTI_THREAD "{THREAD_MAX_WORKER}" in "scrape_error_repo()" re-scraping "{total}"  ...'
    )
    with ThreadPoolExecutor(max_workers=THREAD_MAX_WORKER) as executor:
        # Create a future for each URL
        futures = {
            executor.submit(ScraperGithub.process, item.url, i, total): (
                item.url,
                i,
                total,
            )
            for i, item in enumerate(errors, start=1)
        }

        # ? Process results as they complete
        for future in as_completed(futures):
            url, i, total = futures[future]
            try:
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
