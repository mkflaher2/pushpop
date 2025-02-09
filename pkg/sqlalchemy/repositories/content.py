from typing import List

from models.content import Comment, Submission
from pkg.sqlalchemy.mapper import map_record
from pkg.sqlalchemy.models.content import CommentRecord, SubmissionRecord
from pkg.sqlalchemy.repository import RepositoryBase, repository_factory

# model-specific repositories
class CommentRepository(RepositoryBase):
    def __new__(RepositoryBase, postgres_uri: str):
        return repository_factory(Comment)(postgres_uri)

    def get_by_link_id(self, link_id: str) -> List[Comment]:
        with self.session_maker as session:
            try:
                stmt = select(CommentRecord).where(CommentRecord.link_id == link_id)
                records = session.scalars(stmt).all()
                return [Comment.model_validate(record) for record in records]
            except NoResultFound:
                return []

class SubmissionRepository:
    def __new__(RepositoryBase, postgres_uri: str):
        return repository_factory(Submission)(postgres_uri)
