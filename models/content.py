from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional

class Comment(BaseModel):
    id: str
    subreddit: str
    link_id: str
    parent_id: str
    author: str
    body: str

    @field_validator("link_id", mode="before")
    @classmethod
    def truncate_link_id(cls, v: str):
        return v.split('_')[1]


class Submission(BaseModel):
    id: str
    subreddit: str
    permalink: str
    domain: str
    score: int
    num_comments: int
    selftext: Optional[str] = None

