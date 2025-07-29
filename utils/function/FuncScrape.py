# Library
from bs4 import Tag


def bs_select_one(
    soup: Tag | None, selector: str | None, attr: str | None = None
) -> str | None:
    if not soup:
        return None
    element = soup.select_one(selector) if selector else soup
    if not element:
        return None
    if attr:
        return element.get(attr)
    return element.text.strip()
