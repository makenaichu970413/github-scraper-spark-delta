# Library
from typing import List
from pydantic import BaseModel

# Utils
from utils.model.Igithub_repos import IGitHubRepository


class IGitHubSearchRepositories(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[IGitHubRepository]
