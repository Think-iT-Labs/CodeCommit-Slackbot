from aws_cdk import core, aws_lambda, aws_events, aws_events_targets, aws_iam


class CodecommitSlackBotStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, lambda_path: str,
                 slack_webhook_url: str, codecommit_repo_arn: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # The code that defines your stack goes here
        lambda_role_policy = aws_iam.PolicyDocument(
            statements=[
                aws_iam.PolicyStatement(
                    effect=aws_iam.Effect.ALLOW,
                    actions=['codecommit:*'],
                    resources=[codecommit_repo_arn]
                ),
                aws_iam.PolicyStatement(
                    effect=aws_iam.Effect.ALLOW,
                    actions=[
                        'logs:CreateLogGroup',
                        'logs:CreateLogStream',
                        'logs:PutLogEvents'
                    ],
                    resources=['*']
                )
            ]
        )

        lambda_role = aws_iam.Role(
            self,
            id='role',
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
            inline_policies={
                'policy': lambda_role_policy
            }
        )

        lambda_function = aws_lambda.Function(
            self,
            id='handler',
            code=aws_lambda.Code.from_asset(lambda_path),
            handler='lambda_function.lambda_handler',
            timeout=core.Duration.seconds(300),
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            role=lambda_role,
            environment={
                'SLACK_WEBHOOK_URL': slack_webhook_url
            }
        )

        pattern = aws_events.EventPattern(
            resources=[codecommit_repo_arn],
            source=['aws.codecommit']
        )

        aws_events.Rule(
            self,
            id='cloudwatch-rule',
            event_pattern=pattern,
            targets=[aws_events_targets.LambdaFunction(lambda_function)]
        )
