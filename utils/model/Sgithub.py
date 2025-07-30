from pydantic import BaseModel
from typing_extensions import TypedDict


class TGitHubContributor(TypedDict):
    username: str | None
    url: str | None


class TGitHubUser(BaseModel):
    profile_url: str | None = None
    username: str | None = None
    email: str | None = None
    bio: str | None = None
    organizations: list[str] | None = None


class TGitHubRepo(BaseModel):
    repo_name: str | None = None
    repo_url: str | None = None
    description: str | None = None
    website: str | None = None
    topics: list[str] | None = None
    license: str | None = None
    code_of_conduct: str | None = None
    security_policy: str | None = None
    stars: str | None = None
    watchers: str | None = None
    forks: str | None = None
    contributors: list[TGitHubUser] | None = None
    contributors_total: int | None = None


class TStatus(BaseModel):
    code: int
    type: str
    message: str
    description: str | None = None


class TStatusSucess:
    SUCCESS = TStatus(code=200, type="SUCCESS", message="The request has succeeded.")


class TStatusError:
    THREAD = TStatus(
        code=400,
        type="ERROR_THREAD",
        message="Internla thread pool error",
    )
    # Add more as needed


class TGitHubRepoLog(BaseModel):
    id: int | None = None
    url: str | None = None
    output: str | None = None
    error: str | None = None
    status: str | None = None
    timestamp: str | None = None


class TGitHubContributorLog(BaseModel):
    id: int | None = None
    url: str | None = None
    repo_url: str | None = None
    repo_name: str | None = None
    error: str | None = None
    status: str | None = None
    timestamp: str | None = None


class TGitHubContributorJoinLog(TGitHubContributorLog):
    output: str | None = None


class TGitHubContributorBatchLog(BaseModel):
    repo_url: str | None = None
    repo_name: str | None = None
    repo_output: str | None = None
