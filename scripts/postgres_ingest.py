from clients.pullpush.config import load_pullpush_config
from clients.pullpush.client import PullPushClient
from models.content import Submission
from pkg.sqlalchemy.config import postgres_settings
from pkg.sqlalchemy.repositories.content import CommentRepository, SubmissionRepository

postgres_uri = postgres_settings.SQLALCHEMY_DATABASE_URI
comment_repo = CommentRepository(postgres_uri)
submission_repo = SubmissionRepository(postgres_uri)
pullpush_client = PullPushClient(load_pullpush_config())

submissions = pullpush_client.get_submissions(
    {
        "subreddit": "AskReddit",
        "size": 10,
        "num_comments": ">100"
    }
)

for submission in submissions:
    try:
        submission_repo.add(submission)
    except Exception as e:
        print(f"Could not add submission: {e}")

    comments = pullpush_client.get_comments(
        {"link_id": submission.id, "size": submission.num_comments}
    )
    for comment in comments:
        try:
            comment_repo.add(comment)
        except Exception as e:
            print(f"Could not add comment: {e}")
