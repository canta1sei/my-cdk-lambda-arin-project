from aws_cdk import (
    aws_lambda as lambda_,
    aws_iam as iam,
    Stack,
    Duration # Durationをインポート
)
from constructs import Construct

class MyCdkLambdaProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. IAMロールの定義（前回の指示通り Bedrock InvokeModel などの権限を付与）
        # 例:
        lambda_role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                # Bedrockへのアクセス権限は不要になったので削除
            ]
        )


        # 2. Lambda関数の定義
        # コードのパスを 'A-rin_lambda' ディレクトリに設定
        # ファイル名は A-rinApp.py、ハンドラーは A-rinApp.lambda_handler と仮定
        my_lambda = lambda_.Function(
            self, "ArinChatbotHandler",
            runtime=lambda_.Runtime.PYTHON_3_9, # または適切なバージョン
            handler="A-rinApp.lambda_handler", # 'ファイル名.ハンドラー関数名'
            code=lambda_.Code.from_asset("A-rin_lambda"), # ★ここをA-rin_lambdaディレクトリに設定
            role=lambda_role,
            timeout=Duration.seconds(30), # タイムアウトを30秒に設定
            environment={
                "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY") # 環境変数を追加
            }
        )
