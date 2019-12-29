# AWS CodeCommit Slack Bot

## Requirements
- Slack  [incoming webhook url](https://api.slack.com/messaging/webhooks)

- AWS CodeCommit [repository](https://aws.amazon.com/codecommit/)

- Python 3 runtime with Virtualenv

- AWS CDK installed in you client machine
    ```bash
    npm install -g cdk
    ```
    > Note: if CDK has never been used in you aws account, you should execute the command `cdk bootstrap`

## Usage

1. Clone the repository and install all the needed dependencies
    ```bash
    git clone https://github.com/Think-iT-Labs/CodeCommit-Slackbot.git
    cd CodeCommit-Slackbot

    python3 -m venv env
    source .env/bin/activate 
    python3 -m pip install -r requirements.txt
    ```

2. Edit the `cdk.json` file with your CodeCommit repository arn and  you slack webhook url
    ```json
    {
        "app": "python3 app.py",
        "context": {
            "codecommit_repo_arn": "arn:aws:codecommit:<region>:<account>:<repository_name>",
            "slack_webhook_url": "<slack_webhook_url>"
        }
    }
    ```

3. Run
    ```bash
    cdk deploy
    ```
    