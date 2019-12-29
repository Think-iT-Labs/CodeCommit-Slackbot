from .base import BaseEvent
from helpers import parse_arn


class CommentEvent(BaseEvent):
    def __init__(self, event_payload):
        event_details = event_payload['detail']
        self.author = parse_arn(event_details['callerUserArn'])['resource']
        self.comment_id = event_details['commentId']
        self.in_reply_to_comment_id = event_details.get('inReplyTo')
        super().__init__(event_payload)

    @property
    def in_reply_to_author(self):
        if self.in_reply_to_comment_id:
            return self.codecommit_agent.get_comment_author(self.in_reply_to_comment_id)
        else:
            return None

    @property
    def content(self):
        return self.codecommit_agent.get_comment_content(self.comment_id)
