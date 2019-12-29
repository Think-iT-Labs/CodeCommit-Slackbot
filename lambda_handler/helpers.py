import boto3


def parse_arn(arn):
    # http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
    elements = arn.split(':')
    result = {
        'arn': elements[0],
        'partition': elements[1],
        'service': elements[2],
        'region': elements[3],
        'account': elements[4]
    }
    if len(elements) == 7:
        result['resourcetype'], result['resource'] = elements[5:]
    elif '/' not in elements[5]:
        result['resource'] = elements[5]
        result['resourcetype'] = None
    else:
        result['resourcetype'], result['resource'] = elements[5].split('/')
    return result


class CodeCommitAgent(object):
    def __init__(self, repository_arn):
        region = parse_arn(repository_arn)['region']
        self.codecommit = boto3.client('codecommit', region_name=region)
        super().__init__()

    def get_comment_author(self, comment_id):
        comment_reponse = self.codecommit.get_comment(
            commentId=comment_id
        )
        author_arn = comment_reponse['comment']['authorArn']
        author_username = parse_arn(author_arn)['resource']
        return author_username

    def get_pull_request_title(self, pull_request_id):
        pull_request_response = self.codecommit.get_pull_request(
            pullRequestId=pull_request_id
        )
        pull_request_title = pull_request_response['pullRequest']['title']
        return pull_request_title

    def get_comment_content(self, comment_id):
        comment_reponse = self.codecommit.get_comment(
            commentId=comment_id
        )
        comment_content = comment_reponse['comment']['content']
        return comment_content

    def get_commit_message(self, commit_id, repository):
        commit_response = self.codecommit.get_commit(
            repositoryName=repository,
            commitId=commit_id
        )
        return commit_response['commit']['message']

    def get_commit_author(self, commit_id, repository):
        commit_response = self.codecommit.get_commit(
            repositoryName=repository,
            commitId=commit_id
        )
        return commit_response['commit']['author']['name']
