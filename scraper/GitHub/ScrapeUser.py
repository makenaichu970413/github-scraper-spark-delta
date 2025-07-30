# ? Library
import requests
from bs4 import BeautifulSoup
import logging
from pydantic import BaseModel

# ? Utils
from utils.model.Sgithub import TGitHubUser
from utils.constant import REQUEST_TIMEOUT
from utils.function.FuncScrape import bs_select_one
from utils.function.FuncRequest import check_request_rate, create_session


class DScrapeUser(BaseModel):
    data: TGitHubUser = TGitHubUser()
    error: str | None = None


def scrape_user(url: str) -> DScrapeUser:
    """Scrape user profile for academic affiliations"""

    result: DScrapeUser = DScrapeUser()
    data: TGitHubUser = TGitHubUser()

    try:
        data.profile_url = url

        # Check rate limit before request
        check_request_rate()

        # Put the Network operations inside "with" context manager block
        with create_session() as session:
            page = session.get(url, timeout=REQUEST_TIMEOUT)
            page.raise_for_status()

        # Ensure we have valid content before parsing
        if not page.text:
            raise ValueError(f'EMPTY_PAGE "{url}"')

        try:
            # "lxml" 3-5x faster than 'html.parser'
            soup = BeautifulSoup(page.text, "lxml")
        except Exception:
            # "html.parser" slower than "lxml"
            soup = BeautifulSoup(page.text, "html.parser")

        # print(f"soup:\n\n {soup}")

        username = bs_select_one(soup, 'span[itemprop="additionalName"]')
        data.username = username

        bio = bs_select_one(soup, "[data-bio-text]")
        data.bio = bio

        email = bs_select_one(soup, 'a[data-test-selector="profile-email"]')
        email = email.replace("mailto:", "") if email else None
        data.email = email

        # Remove '@' prefix
        orgs_els = soup.select(".avatar-group-item img")
        organizations = [img["alt"][1:] for img in orgs_els] if orgs_els else None
        data.organizations = organizations

    except Exception as err:
        result.error = err
        logging.error(err)

    # ? Set Final Data
    result.data = data

    return result
