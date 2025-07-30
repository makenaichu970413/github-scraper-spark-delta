# Utils
from utils.function.FuncRequest import create_session
from utils.constant import REQUEST_TIMEOUT, DOMAIN_GITHUB
from utils.model.Iapi import IHeaders
from utils.model.Igithub_contributors import IGitHubContributor
from utils.model.Igithub_issues import IGitHubIssue
from utils.model.Igithub_repos import IGitHubRepository
from utils.model.Igithub_search_repositories import IGitHubSearchRepositories
from utils.model.Igithub_users import IGitHubUsers


def scrape() -> None:

    token = "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"
    headers = IHeaders(Authorization=token)
    print(f"IHeaders: {headers}")

    # Search Repositories:
    # GET "/search/repositories?q={query}"
    # e.g., https://api.github.com/search/repositories?q=stars:>1000
    url_search_repositories = f"{DOMAIN_GITHUB}search/repositories?q=stars:>10000"
    with create_session(headers) as session:
        res = session.get(url_search_repositories, timeout=REQUEST_TIMEOUT)
        temp = res.json()
        data_search_repositories = IGitHubSearchRepositories.model_validate(temp)
        print(f"\n\ndata_search_repositories: {data_search_repositories}")

    data_repo = data_search_repositories.items[0] if data_search_repositories else None

    # {owner}/{repo} <=> "facebook/react"
    owner_repo = data_repo.full_name if data_repo else None

    print(f"\n\nowner_repo: {owner_repo}")

    if not owner_repo:
        print(f'NOT FOUND "owner_repo" !')
        return

    # Repository Data:
    # GET "/repos/{owner}/{repo}"
    url_repos = f"{DOMAIN_GITHUB}repos/{owner_repo}"
    with create_session(headers) as session:
        res = session.get(url_repos, timeout=REQUEST_TIMEOUT)
        temp = res.json()
        data_repo = IGitHubRepository.model_validate(temp)
        print(f"\n\ndata_repo: {data_repo}")

    # Contributors Data:
    # GET "/repos/{owner}/{repo}/contributors"
    url_contributors = data_repo.contributors_url
    with create_session(headers) as session:
        res = session.get(url_contributors, timeout=REQUEST_TIMEOUT)
        temp = res.json()
        data_contributors = [IGitHubContributor.model_validate(item) for item in temp]
        print(f"\n\ndata_contributors: {data_contributors}")

    # User Data:
    # GET "/users/{username}"
    url_users = data_repo.owner.url
    with create_session(headers) as session:
        res = session.get(url_users, timeout=REQUEST_TIMEOUT)
        temp = res.json()
        data_users = IGitHubUsers.model_validate(temp)
        print(f"\n\ndata_users: {data_users}")

    # Repository Issues Data:
    # GET "/repos/{owner}/{repo}/issues"
    url_issues = f"{DOMAIN_GITHUB}repos/{owner_repo}/issues"
    with create_session(headers) as session:
        res = session.get(url_issues, timeout=REQUEST_TIMEOUT)
        temp = res.json()
        data_issues = [IGitHubIssue.model_validate(item) for item in temp]
        data_issue = data_issues[0]
        print(f"\n\ndata_issue: {data_issue}")
