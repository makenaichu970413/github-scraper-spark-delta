# Library
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import cast, Optional


# ? Scrapper
from scraper.GitHub.ScrapeContributors import process_contributor


# ? Utils
from utils.constant import (
    DB_NAME_CONTRIBUTOR,
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_PENDING,
    STATUS_PROCESS,
    THREAD_MAX_WORKER,
    THREAD_SUB_MAX_WORKER,
)
from utils.function import FuncDBLogContributor as LogContributor
from utils.function import FuncDBLogRepo as LogRepo
from utils.function.FuncFile import export_json, import_json
from utils.models import TGitHubContributorLog, TGitHubRepo, TGitHubRepoLog, TGitHubUser


def scrape_error_contributor(
    repo_url: str, batch_index: int, batch_total: int
) -> list[TGitHubUser]:
    errors = LogContributor.load(
        status=[STATUS_FAILED, STATUS_COMPLETE], repo_url=repo_url
    )
    total = len(errors)
    print(
        f'\n❌[{batch_index}/{batch_total}] BATCH In "{DB_NAME_CONTRIBUTOR}" found total errors "{total}" under "{repo_url}"'
    )
    for i, item in enumerate(errors, start=1):
        print(f"{i}. {item}")

    print(
        f'\n🚀MULTI_THREAD "{THREAD_MAX_WORKER}" in "scrape_error_contributor()" re-scraping "{total}" under "{repo_url}" ...'
    )

    data: list[TGitHubUser] = []

    with ThreadPoolExecutor(max_workers=THREAD_SUB_MAX_WORKER) as executor:
        # Create a future for each URL
        futures = {
            executor.submit(process_contributor, item.url, i, total, item.repo_name): (
                item.url,
                i,
                total,
                item.repo_name,
            )
            for i, item in enumerate(errors, start=1)
        }

        # ? Process results as they complete
        for future in as_completed(futures):
            url, i, total, repo_name = futures[future]
            try:
                result_contributor = future.result()
                print("result_contributor: ", result_contributor)
                data.append(result_contributor.data)

                if result_contributor.error:
                    raise Exception(result_contributor.error)

                LogContributor.upsert(
                    TGitHubContributorLog(url=url, status=STATUS_COMPLETE)
                )

            except Exception as err:
                logging.error(err)
                LogContributor.upsert(
                    TGitHubContributorLog(url=url, error=str(err), status=STATUS_FAILED)
                )

    #! Return "contributos" after multi thread completed
    return data


def scrape_error_contributors() -> None:

    # Initialize DB When Start
    isDBInit = LogContributor.init_table()
    if not isDBInit:
        return

    batches = LogContributor.load_batch(status=[STATUS_FAILED, STATUS_PROCESS])
    # ? Filtering out batches where "repo_output" is "None"
    # batches = [item for item in batches if item.repo_output]
    total = len(batches)
    print(f'In "{DB_NAME_CONTRIBUTOR}" found total error batches "{total}"')
    for i, item in enumerate(batches, start=1):
        print(f"{i}. {item}")

    if not total:
        return

    with ThreadPoolExecutor(max_workers=THREAD_MAX_WORKER) as executor:
        # Create a future for each URL
        futures = {
            executor.submit(scrape_error_contributor, item.repo_url, i, total): (
                item.repo_url,
                item.repo_output,
                i,
            )
            for i, item in enumerate(batches, start=1)
        }

        # ? Process results as they complete
        for future in as_completed(futures):
            url, repo_output, i = futures[future]
            try:
                new_contributors = future.result()
                data_dict = import_json(repo_output) if repo_output else None
                data = TGitHubRepo.model_validate(data_dict) if data_dict else None

                if data:
                    # Update back into the parent JSON if the data is found
                    new_contributor_urls = [
                        item.profile_url
                        for item in new_contributors
                        if item.profile_url
                    ]
                    data.contributors = [
                        item
                        for item in data.contributors
                        if item.profile_url not in new_contributor_urls
                    ]
                    data.contributors.extend(new_contributors)
                    export_json(data=data.model_dump_json(indent=2), path=repo_output)

            except Exception as err:
                logging.error(f"scrape_error_contributors ERROR: {err}")
