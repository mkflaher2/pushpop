import requests
from typing import List

from clients.pullpush.config import PullPushConfig
from models.content import Submission, Comment
""" Facade pattern client for pullpush API """

class PullPushClient:
    def __init__(self, config: PullPushConfig):
        self.url = config.url

    def get_submissions(self, params: dict) -> List[Submission]:
        try:
            response = requests.get(
                f"{self.url}/submission/",
                params=params
            )
            data = response.json().get('data')
            submissions = [Submission.model_validate(submission) for submission in data]
            return submissions
        except Exception as e:
            print(f"Failed to get submissions: {e}")
            return None

    def get_comments(self, params: dict) -> List[Comment]:
        try:
            response = requests.get(
                f"{self.url}/comment/",
                params=params
            )
            data = response.json().get('data')
            comments = [Comment.model_validate(comment) for comment in data]
            return comments
        except Exception as e:
            print(f"Failed to get comments: {e}")
            return None


