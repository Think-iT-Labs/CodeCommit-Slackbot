from helpers import CodeCommitAgent


class BaseEvent(object):
    def __init__(self, event_payload):
        self.region = event_payload['region']
        self.repository = event_payload['detail'].get('repositoryName')
        self.repository_arn = event_payload['resources'][0]
        self.codecommit_agent = CodeCommitAgent(self.repository_arn)

    @property
    def repository_url(self):
        if self.repository:
            return f'https://{self.region}.console.aws.amazon.com/codesuite/codecommit/repositories/{self.repository}/browse'

    def get_text(self):
        pass

    def get_pretext(self):
        pass

    def get_slack_payload(self):
        return {
            "attachments": [
                {
                    "mrkdwn_in": ["pretext", "text"],
                    "color": "#65923e",
                    "pretext": self.get_pretext(),
                    "text": self.get_text(),
                    "unfurl_links": True
                }
            ]
        }
