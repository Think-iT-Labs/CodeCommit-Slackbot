# AWS CodeCommit Slack Bot

## Requirements
- Slack  [incoming webhook url](https://api.slack.com/messaging/webhooks)

- AWS CodeCommit [repository](https://aws.amazon.com/codecommit/)

- AWS CDK installed in you client machine
    ```bash
    npm install -g cdk
    ```
    > Note: if CDK has never been used in you aws account, you should execute the command `cdk bootstrap`

## Usage
1. Edit the `cdk.json` file with your CodeCommit repository arn and  you slack webhook url

2. Run
    ```bash
    cdk deploy
    ```
    