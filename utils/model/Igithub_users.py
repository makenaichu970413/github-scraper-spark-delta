# Library
from pydantic import BaseModel
from typing import Optional



class IGitHubUser(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool
    user_view_type: Optional[str] = None


class IGitHubUsers(IGitHubUser, BaseModel):
    name: str
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    hireable: Optional[bool] = None
    bio: Optional[str] = None
    twitter_username: Optional[str] = None
    public_repos: Optional[int] = None
    public_gists: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: str
    updated_at: str
