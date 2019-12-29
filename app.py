#!/usr/bin/env python3

from aws_cdk import core
from os import path

from codecommit_slack_bot.codecommit_slack_bot_stack import CodecommitSlackBotStack


project_root_path = path.dirname(path.realpath(__file__))
lambda_source_code_path = path.join(project_root_path, 'lambda_handler')

app = core.App()

codecommit_repo_arn = app.node.try_get_context('codecommit_repo_arn')
slack_webhook_url = app.node.try_get_context('slack_webhook_url')

repository_details = core.Arn.parse(codecommit_repo_arn)
account = repository_details.account
region = repository_details.region
repository_name = repository_details.resource

env = core.Environment(account=account, region=region)

CodecommitSlackBotStack(
    app,
    f'codecommit-slack-bot-{repository_name}',
    lambda_path=lambda_source_code_path,
    slack_webhook_url=slack_webhook_url,
    codecommit_repo_arn=codecommit_repo_arn,
    env=env
)

app.synth()
