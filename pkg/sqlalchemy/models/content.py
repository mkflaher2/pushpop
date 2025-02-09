from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.content import Comment, Submission
from pkg.sqlalchemy.models.base import Base

# table record models
class CommentRecord(Base):
    __tablename__ = "comment"
    id: Mapped[str] = mapped_column(primary_key=True)
    subreddit: Mapped[str]
    link_id: Mapped[str] = mapped_column(ForeignKey("submission.id"))
    parent_id: Mapped[str]
    author: Mapped[str]
    body: Mapped[str]

    __table_args = (
        UniqueConstraint("id", "subreddit", "parent_id", name="unique_comment_id"),
    )


class SubmissionRecord(Base):
    __tablename__ = "submission"
    id: Mapped[str] = mapped_column(primary_key=True)
    subreddit: Mapped[str]
    permalink: Mapped[str]
    domain: Mapped[str]
    score: Mapped[int]
    num_comments: Mapped[int]
    selftext: Mapped[str] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint("id", "subreddit", name="unique_submission_id"),
    )

