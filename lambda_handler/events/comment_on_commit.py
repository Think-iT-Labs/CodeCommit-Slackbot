from .comment import CommentEvent


class CommentOnCommitEvent(CommentEvent):
    def __init__(self, event_payload):
        event_details = event_payload['detail']
        self.commit_id = event_details['afterCommitId']
        super().__init__(event_payload)

    @property
    def commit_url(self):
        return f'https://{self.region}.console.aws.amazon.com/codesuite/codecommit/repositories/{self.repository}/commit/{self.commit_id}'

    @property
    def commit_hash(self):
        return self.commit_id[:5]


class CommentOnCommitCreatedEvent(CommentOnCommitEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)

    def get_pretext(self):
        if self.in_reply_to_author:
            return f"{self.author} replied to {self.in_reply_to_author}'s comment in <{self.commit_url}|*{self.commit_hash}*> in <{self.repository_url}|{self.repository}>"
        else:
            return f"{self.author} commented in <{self.commit_url}|*{self.commit_hash}*> in <{self.repository_url}|{self.repository}>"

    def get_text(self):
        return self.content


class CommentOnCommitUpdatedEvent(CommentOnCommitEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)

    def get_pretext(self):
        if self.in_reply_to_author:
            return f"{self.author} updated their reply to {self.in_reply_to_author}'s comment in <{self.commit_url}|*{self.commit_hash}*> in <{self.repository_url}|{self.repository}>"
        else:
            return f"{self.author} updated their comment in <{self.commit_url}|*{self.commit_hash}*> in <{self.repository_url}|{self.repository}>"

    def get_text(self):
        return self.content
