"""
AWS CDK app for content creator infrastructure.
"""
import aws_cdk as cdk
from stacks.content_creator_stack import ContentCreatorStack


app = cdk.App()
ContentCreatorStack(
    app,
    "ContentCreatorStack",
    env=cdk.Environment(
        account=app.node.try_get_context("account"),
        region=app.node.try_get_context("region") or "us-east-1"
    ),
    description="AWS Bedrock-powered content creation platform"
)

app.synth()

