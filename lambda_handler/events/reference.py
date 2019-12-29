from .base import BaseEvent
from helpers import parse_arn


class ReferenceEvent(BaseEvent):
    def __init__(self, event_payload):
        event_details = event_payload['detail']
        self.branch = event_details['referenceName']
        self.reference_full_name = event_details['referenceFullName']
        if 'commitId' in event_details:
            self.commit_id = event_details['commitId']
        elif 'oldCommitId' in event_details:
            self.old_commit_id = event_details['oldCommitId']
        super().__init__(event_payload)

    @property
    def branch_url(self):
        return f'https://{self.region}.console.aws.amazon.com/codesuite/codecommit/repositories/{self.repository}/browse/{self.reference_full_name}'

    @property
    def commit_message(self):
        if hasattr(self, 'commit_id'):
            return self.codecommit_agent.get_commit_message(self.commit_id, self.repository)

    @property
    def author(self):
        if hasattr(self, 'commit_id'):
            return self.codecommit_agent.get_commit_author(self.commit_id, self.repository)


class ReferenceCreated(ReferenceEvent):
    @property
    def commit_url(self):
        return f'https://{self.region}.console.aws.amazon.com/codesuite/codecommit/repositories/{self.repository}/commit/{self.commit_id}'

    @property
    def commit_hash(self):
        return self.commit_id[:5]

    def get_pretext(self):
        return f'{self.author} pushed a new branch <{self.branch_url}|{self.branch}> in <{self.repository_url}|{self.repository}>'

    def get_text(self):
        return f'<{self.commit_url}|{self.commit_hash}> {self.commit_message}'


class ReferenceUpdated(ReferenceEvent):
    @property
    def commit_url(self):
        return f'https://{self.region}.console.aws.amazon.com/codesuite/codecommit/repositories/{self.repository}/commit/{self.commit_id}'

    @property
    def commit_hash(self):
        return self.commit_id[:5]

    def get_pretext(self):
        return f'{self.author} pushed to branch <{self.branch_url}|{self.branch}> of <{self.repository_url}|{self.repository}>'

    def get_text(self):
        return f'<{self.commit_url}|{self.commit_hash}> {self.commit_message}'


class ReferenceDeleted(ReferenceEvent):
    def __init__(self, event_payload):
        event_details = event_payload['detail']
        self._author = parse_arn(event_details['callerUserArn'])['resource']
        super().__init__(event_payload)

    @property
    def author(self):
        return self._author

    def get_pretext(self):
        return f'{self.author} deleted the branch <{self.branch_url}|{self.branch}> of <{self.repository_url}|{self.repository}>'

    def get_text(self):
        return ''
