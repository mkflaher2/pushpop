from typing import Optional, TypeVar

from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from pydantic import BaseModel

from models.content import Comment, Submission
from pkg.sqlalchemy.models.content import CommentRecord, SubmissionRecord
from pkg.sqlalchemy.mapper import map_record

T = TypeVar("T", bound=BaseModel)

class RepositoryBase:
    def __init__(self, uri: str):
        self.engine = create_engine(uri)
        self.session_maker = sessionmaker(bind=self.engine)
        self.async_engine = create_async_engine(uri)
        self.async_session_maker = async_sessionmaker(bind=self.async_engine, expire_on_commit=False)

        async def get_async_session(self) -> AsyncSession:
            db = self.async_session_maker()
            try:
                yield db
            except Exception as e:
                print(f"{e}")
                await db.rollback()
            finally:
                await db.close()


def repository_factory(model: T):
    """
    Generic repsository factory (good for models where specific repository doesn't exist/isn't needed)
    """
    record_model = map_record(model)

    class Repository(RepositoryBase):
        def add(self, data: T) -> str:
            record = record_model(**data.model_dump())
            with self.session_maker() as session:
                session.add(record)
                session.commit()
                return getattr(record, "id", None)

        def get_by_id(self, record_id: str) -> Optional[T]:
            with self.session_maker() as session:
                try:
                    stmt = select(record_model).where(record_model.id == record_id)
                    record = session.scalars(stmt).one()
                    return model.model_validate(record)
                except NoResultFound:
                    return None

    Repository.model = model
    Repository.record_model = record_model
    return Repository


