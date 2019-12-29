from .comment import CommentEvent


class CommentOnPullRequestEvent(CommentEvent):
    def __init__(self, event_payload):
        event_details = event_payload['detail']
        self.pull_request_id = event_details['pullRequestId']
        super().__init__(event_payload)

    @property
    def pull_request_url(self):
        return f'https://{self.region}.console.aws.amazon.com/codesuite/codecommit/repositories/{self.repository}/pull-requests/{self.pull_request_id}'

    @property
    def pull_request_title(self):
        return self.codecommit_agent.get_pull_request_title(self.pull_request_id)


class CommentOnPullRequestCreatedEvent(CommentOnPullRequestEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)

    def get_pretext(self):
        if self.in_reply_to_author:
            return f"{self.author} replied to {self.in_reply_to_author}'s comment in <{self.pull_request_url}|*{self.pull_request_id}* {self.pull_request_title}> in < {self.repository_url} | {self.repository} >"
        else:
            return f"{self.author} commented in <{self.pull_request_url}|*{self.pull_request_id}* {self.pull_request_title}> in <{self.repository_url}|{self.repository}>"

    def get_text(self):
        return self.content


class CommentOnPullRequestUpdatedEvent(CommentOnPullRequestEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)

    def get_pretext(self):
        if self.in_reply_to_author:
            return f"{self.author} updated their reply to {self.in_reply_to_author}'s comment in <{self.pull_request_url}|*{self.pull_request_id}* {self.pull_request_title}> in <{self.repository_url}|{self.repository}>"
        else:
            return f"{self.author} updated their comment in <{self.pull_request_url}|*{self.pull_request_id}* {self.pull_request_title}> in <{self.repository_url}|{self.repository}>"

    def get_text(self):
        return self.content
