# Library
from pydantic import BaseModel

# Utils
from utils.model.Igithub_users import IGitHubUser


class IGitHubContributor(IGitHubUser, BaseModel):
    contributions: int
