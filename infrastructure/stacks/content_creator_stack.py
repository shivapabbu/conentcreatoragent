"""
AWS CDK stack for Content Creator infrastructure.
"""
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    Duration,
    RemovalPolicy
)
from constructs import Construct


class ContentCreatorStack(Stack):
    """Main stack for content creation platform"""
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # S3 bucket for documents and assets
        self.documents_bucket = s3.Bucket(
            self,
            "DocumentsBucket",
            bucket_name=f"content-creator-documents-{self.account}",
            removal_policy=RemovalPolicy.DESTROY,  # For dev, use RETAIN in prod
            auto_delete_objects=True
        )
        
        # DynamoDB table for metadata and user settings
        self.metadata_table = dynamodb.Table(
            self,
            "MetadataTable",
            table_name="content-creator-metadata",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY  # For dev
        )
        
        # Lambda function for content generation
        self.lambda_function = _lambda.Function(
            self,
            "ContentGeneratorFunction",
            function_name="content-generator",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("../backend"),
            timeout=Duration.minutes(5),
            memory_size=512,
            environment={
                "AWS_REGION": self.region,
                "USE_LOCAL_MOCKS": "false",
                "VECTOR_DB_TYPE": "opensearch",
                "DOCUMENTS_BUCKET": self.documents_bucket.bucket_name,
                "METADATA_TABLE": self.metadata_table.table_name
            }
        )
        
        # Grant permissions to Lambda
        # Bedrock permissions
        self.lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream"
                ],
                resources=[
                    f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-5-sonnet-*",
                    f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-3-5-haiku-*",
                    f"arn:aws:bedrock:{self.region}::foundation-model/amazon.titan-embed-*"
                ]
            )
        )
        
        # S3 permissions
        self.documents_bucket.grant_read_write(self.lambda_function)
        
        # DynamoDB permissions
        self.metadata_table.grant_read_write_data(self.lambda_function)
        
        # OpenSearch permissions (if using OpenSearch Serverless)
        self.lambda_function.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "aoss:APIAccessAll"
                ],
                resources=["*"]  # Restrict to specific collection in production
            )
        )
        
        # API Gateway
        self.api = apigateway.RestApi(
            self,
            "ContentCreatorApi",
            rest_api_name="Content Creator API",
            description="API for content generation",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "X-Amz-Date", "Authorization", "X-Api-Key"]
            )
        )
        
        # Lambda integration
        lambda_integration = apigateway.LambdaIntegration(
            self.lambda_function,
            request_templates={"application/json": '{"statusCode": "200"}'}
        )
        
        # API routes
        self.api.root.add_resource("api").add_resource("generate").add_method(
            "POST",
            lambda_integration
        )
        
        # Health check endpoint
        self.api.root.add_resource("health").add_method(
            "GET",
            apigateway.LambdaIntegration(
                self.lambda_function,
                request_templates={"application/json": '{"statusCode": "200"}'}
            )
        )
        
        # Outputs
        cdk.CfnOutput(
            self,
            "ApiEndpoint",
            value=self.api.url,
            description="API Gateway endpoint URL"
        )
        
        cdk.CfnOutput(
            self,
            "DocumentsBucketName",
            value=self.documents_bucket.bucket_name,
            description="S3 bucket for documents"
        )

