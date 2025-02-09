from pydantic import BaseModel

from models.content import Comment, Submission
from pkg.sqlalchemy.models.content import CommentRecord, SubmissionRecord

def map_record(model: BaseModel):
    map_dict = {
        Comment: CommentRecord,
        Submission: SubmissionRecord,
    }

    return map_dict[model]

