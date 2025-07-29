# Library
import requests
from bs4 import BeautifulSoup
import logging
from pydantic import BaseModel


# ? Scrapper
from scraper.GitHub.ScrapeContributors import scrape_contributors


# ? Utils
from utils.constant import REQUEST_TIMEOUT
from utils.models import TGitHubRepo
from utils.function.FuncRequest import check_request_rate, create_session
from utils.function.FuncScrape import bs_select_one


class DScrapeRepo(BaseModel):
    data: TGitHubRepo = TGitHubRepo()
    error: str | None = None


def scrape_repo(url: str) -> DScrapeRepo:
    """Scrape key repository data and contributor affiliations"""

    result: DScrapeRepo = DScrapeRepo()
    data: TGitHubRepo = TGitHubRepo()

    try:
        data.repo_url = url

        # 1. Fetch repository main page

        # Check rate limit before request
        check_request_rate()

        # Put the Network operations inside "with" context manager block
        with create_session() as session:
            page = session.get(url, timeout=REQUEST_TIMEOUT)
            page.raise_for_status()

        # Ensure we have valid content before parsing
        if not page.text:
            raise ValueError(f'EMPTY_PAGE "{url}"')

        """
        Automatically fallback to `html.parser` if:
        * `lxml` is not installed
        * `HTML` is malformed
        * Any parsing error occurs
        """
        try:
            # "lxml" 3-5x faster than 'html.parser'
            soup = BeautifulSoup(page.text, "lxml")
        except Exception:
            # "html.parser" slower than "lxml"
            soup = BeautifulSoup(page.text, "html.parser")

        # print(f"soup:\n\n {soup}")
        # https://github.com/rise-lab
        url_repo_name = url.rstrip("/").split("/")[-1]
        repo_name = bs_select_one(soup, 'strong[itemprop="name"]')
        data.repo_name = repo_name if repo_name else url_repo_name

        # 2. Extract About metadata
        soup_about = soup.select_one("div.BorderGrid-cell")
        if soup_about:
            description = bs_select_one(soup_about, "p.f4.my-3")
            data.description = description if description else None

            website = bs_select_one(soup_about, "a.text-bold[href]")  # ? ['href']
            data.website = website if website else None

            topics_els = soup_about.select("a.topic-tag.topic-tag-link")
            topics = (
                [bs_select_one(topic, None) for topic in topics_els]
                if topics_els
                else None
            )
            data.topics = topics if topics and len(topics) else None

            license = bs_select_one(soup_about, 'a[href*="LICENSE"]')
            data.license = license if license else None

            code_of_conduct = bs_select_one(soup_about, 'a[href*="code-of-conduct"]')
            data.code_of_conduct = code_of_conduct if code_of_conduct else None

            security_policy = bs_select_one(soup_about, 'a[href*="security"]')
            data.security_policy = security_policy if security_policy else None

            stars = bs_select_one(soup_about, 'a[href$="/stargazers"] strong')
            data.stars = stars if stars else None

            watchers = bs_select_one(soup_about, 'a[href$="/watchers"] strong')
            data.watchers = watchers if watchers else None

            forks = bs_select_one(soup_about, 'a[href$="/forks"] strong')
            data.forks = forks if forks else None

        # Process contributors
        contributor_els = soup.select('a[data-hovercard-type="user"]')
        contributor_urls: list[str] = (
            [item["href"] for item in contributor_els] if contributor_els else []
        )
        contributor_urls = contributor_urls[:5]
        contributors_result = scrape_contributors(
            soup=soup, URLs=contributor_urls, repo_name=repo_name, repo_url=url
        )
        data.contributors = contributors_result.data
        data.contributors_total = contributors_result.total

    except Exception as err:
        obj = {"url": url, "error": err}
        error = f"scrape_repo_error: {obj}"
        result.error = error
        logging.error(err)

    # ? Set Final Data
    result.data = data

    return result
