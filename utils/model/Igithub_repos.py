# Library
from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime

# Utils
from utils.model.Igithub_users import IGitHubUser


class IGitHubLicense(BaseModel):
    key: str
    name: str
    spdx_id: str
    url: Optional[str] = None
    node_id: str


class IGitHubRepository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: IGitHubUser
    html_url: str
    description: Optional[str] = None
    fork: bool = False
    url: str = ""
    forks_url: str = ""
    keys_url: str = ""
    collaborators_url: str = ""
    teams_url: str = ""
    hooks_url: str = ""
    issue_events_url: str = ""
    events_url: str = ""
    assignees_url: str = ""
    branches_url: str = ""
    tags_url: str = ""
    blobs_url: str = ""
    git_tags_url: str = ""
    git_refs_url: str = ""
    trees_url: str = ""
    statuses_url: str = ""
    languages_url: str = ""
    stargazers_url: str = ""
    contributors_url: str = ""
    subscribers_url: str = ""
    subscription_url: str = ""
    commits_url: str = ""
    git_commits_url: str = ""
    comments_url: str = ""
    issue_comment_url: str = ""
    contents_url: str = ""
    compare_url: str = ""
    merges_url: str = ""
    archive_url: str = ""
    downloads_url: str = ""
    issues_url: str = ""
    pulls_url: str = ""
    milestones_url: str = ""
    notifications_url: str = ""
    labels_url: str = ""
    releases_url: str = ""
    deployments_url: str = ""
    created_at: str = ""
    updated_at: str = ""
    pushed_at: str = ""
    git_url: str = ""
    ssh_url: str = ""
    clone_url: str = ""
    svn_url: str = ""
    homepage: Optional[str] = None
    size: int = 0
    stargazers_count: int = 0
    watchers_count: int = 0
    language: Optional[str] = None
    has_issues: bool = True
    has_projects: bool = True
    has_downloads: bool = True
    has_wiki: bool = False
    has_pages: bool = False
    has_discussions: bool = False
    forks_count: int = 0
    mirror_url: Optional[str] = None
    archived: bool = False
    disabled: bool = False
    open_issues_count: int = 0
    license: Optional[IGitHubLicense] = None
    allow_forking: bool = True
    is_template: bool = False
    web_commit_signoff_required: bool = False
    topics: List[str] = []
    visibility: str = "public"  # "public" | "private"
    forks: int = 0
    open_issues: int = 0
    watchers: int = 0
    default_branch: str = "main"
    score: Optional[float] = None

    # New fields from the second JSON sample
    temp_clone_token: Optional[str] = None
    custom_properties: Dict[str, Any] = {}
    organization: Optional[IGitHubUser] = None
    network_count: Optional[int] = None
    subscribers_count: Optional[int] = None

    # Helper properties for datetime conversion
    @property
    def created_datetime(self) -> datetime:
        return datetime.fromisoformat(self.created_at.replace("Z", "+00:00"))

    @property
    def updated_datetime(self) -> datetime:
        return datetime.fromisoformat(self.updated_at.replace("Z", "+00:00"))

    @property
    def pushed_datetime(self) -> datetime:
        return datetime.fromisoformat(self.pushed_at.replace("Z", "+00:00"))
