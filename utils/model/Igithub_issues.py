# Library
from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, HttpUrl

# Utils
from utils.model.Igithub_users import IGitHubUser


class IGitHubIssueLabel(BaseModel):
    id: int
    node_id: str
    url: HttpUrl
    name: str
    color: str
    default: bool
    description: Optional[str] = None


class IGitHubMilestone(BaseModel):
    url: HttpUrl
    html_url: HttpUrl
    labels_url: HttpUrl
    id: int
    node_id: str
    number: int
    title: str
    description: Optional[str] = None
    creator: IGitHubUser
    open_issues: int
    closed_issues: int
    state: str
    created_at: datetime
    updated_at: datetime
    due_on: Optional[datetime] = None
    closed_at: Optional[datetime] = None


class IGitHubReactions(BaseModel):
    url: HttpUrl
    total_count: int
    plus1: int = Field(alias="+1")
    minus1: int = Field(alias="-1")
    laugh: int
    hooray: int
    confused: int
    heart: int
    rocket: int
    eyes: int


class IGitHubSubIssuesSummary(BaseModel):
    total: int
    completed: int
    percent_completed: int


class IGitHubPullRequest(BaseModel):
    url: HttpUrl
    html_url: HttpUrl
    diff_url: HttpUrl
    patch_url: HttpUrl
    merged_at: Optional[datetime] = None


class IGitHubIssueType(BaseModel):
    id: int
    node_id: str
    name: str
    description: Optional[str] = None
    color: str
    created_at: datetime
    updated_at: datetime
    is_enabled: bool


class IGitHubIssue(BaseModel):
    url: HttpUrl
    repository_url: HttpUrl
    labels_url: str
    comments_url: HttpUrl
    events_url: HttpUrl
    html_url: HttpUrl
    id: int
    node_id: str
    number: int
    title: str
    user: IGitHubUser
    labels: List[IGitHubIssueLabel]
    state: str
    locked: bool
    assignee: Optional[IGitHubUser] = None
    assignees: List[IGitHubUser]
    milestone: Optional[IGitHubMilestone] = None
    comments: int
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None
    author_association: str
    type: Optional[IGitHubIssueType] = None
    active_lock_reason: Optional[str] = None
    sub_issues_summary: Optional[IGitHubSubIssuesSummary] = None
    body: Optional[str] = None
    closed_by: Optional[IGitHubUser] = None
    reactions: IGitHubReactions
    timeline_url: HttpUrl
    performed_via_github_app: Optional[str] = None
    state_reason: Optional[str] = None
    draft: Optional[bool] = None
    pull_request: Optional[IGitHubPullRequest] = None
