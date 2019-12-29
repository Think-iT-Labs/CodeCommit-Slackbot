from .base import BaseEvent
from helpers import parse_arn


class PullRequestEvent(BaseEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)
        event_details = event_payload['detail']
        self.repository = event_details.get('repositoryNames')[0]
        self.pull_request_id = event_details['pullRequestId']
        self.author = parse_arn(event_details['callerUserArn'])['resource']

    @property
    def pull_request_title(self):
        return self.codecommit_agent.get_pull_request_title(self.pull_request_id)

    @property
    def pull_request_url(self):
        return f'https://{self.region}.console.aws.amazon.com/codesuite/codecommit/repositories/{self.repository}/pull-requests/{self.pull_request_id}'


class PullRequestCreatedEvent(PullRequestEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)

    def get_text(self):
        return ''

    def get_pretext(self):
        return f'{self.author} opened <{self.pull_request_url}|*{self.pull_request_id}* {self.pull_request_title}> in <{self.repository_url}|{self.repository}>'


class PullRequestStatusChangedEvent(PullRequestEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)

    def get_text(self):
        return ''

    def get_pretext(self):
        return f'{self.author} closed <{self.pull_request_url}|*{self.pull_request_id}* {self.pull_request_title}> in <{self.repository_url}|{self.repository}>'


class PullRequestMergeStatusUpdatedEvent(PullRequestEvent):
    def __init__(self, event_payload):
        super().__init__(event_payload)

    def get_text(self):
        return ''

    def get_pretext(self):
        return f'{self.author} merged <{self.pull_request_url}|*{self.pull_request_id}* {self.pull_request_title}> in <{self.repository_url}|{self.repository}>'
