import os
from aws_cdk import (
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_secretsmanager as secretsmanager,
    Stack,
    Duration,
    BundlingOptions,
    CfnOutput
)
from constructs import Construct

class MyCdkLambdaProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. IAMロールの定義
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ]
        )

        # 2. Secrets Managerのシークレットオブジェクトを取得
        gemini_api_key_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "GeminiApiKeySecret",
            secret_name="gemini-api-key"
        )

        # 3. Lambda関数の定義
        my_lambda = lambda_.Function(
            self, "ArinChatbotHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="A-rinApp.lambda_handler",
            code=lambda_.Code.from_asset("A-rin_lambda",
                bundling=BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ]
                )
            ),
            role=lambda_role,
            timeout=Duration.seconds(30),
            environment={
                # APIキーの代わりに、シークレット名を環境変数として渡す
                "SECRET_NAME": "gemini-api-key"
            }
        )

        # 4. Lambdaの実行ロールにシークレットの読み取り権限を付与
        gemini_api_key_secret.grant_read(my_lambda)

        # 5. API Gatewayの定義
        api = apigw.LambdaRestApi(
            self, "ArinChatbotApi",
            handler=my_lambda,
            proxy=True,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=["POST", "OPTIONS"],
                allow_headers=["Content-Type"]
            )
        )

        # 6. APIエンドポイントURLの出力
        CfnOutput(self, "ApiEndpointUrl",
            value=api.url,
            description="The endpoint URL of the API Gateway"
        )