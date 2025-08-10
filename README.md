# 私のCDK Lambda A-rinプロジェクト

このプロジェクトは、AWS CDKとPythonを使用して、Google Gemini APIを活用したAIチャットボットを構築・デプロイするサンプルです。

## 主要技術

*   AWS CDK (Python)
*   AWS Lambda
*   Google Gemini API
*   Python 3.9
*   Docker

## プロジェクト構造

*   `A-rin_lambda/`: Lambda関数のソースコードと依存関係を格納するディレクトリ。
    *   `A-rinApp.py`: チャットボットのコアとなるLambda関数コード。
    *   `requirements.txt`: Lambda関数が使用するPythonライブラリ。
*   `my_cdk_lambda_project/`: AWSインフラを定義するCDKコード。
    *   `my_cdk_lambda_project_stack.py`: Lambda関数とIAMロールをデプロイするためのCDKスタック定義。
*   `app.py`: CDKアプリケーションのエントリーポイント。
*   `cdk.json`: CDKの設定ファイル。
*   `requirements.txt`: CDKアプリケーション自体の実行に必要なPythonライブラリ。

## 動作に必要な環境 (Prerequisites)

このプロジェクトをローカル環境でセットアップ・デプロイするには、以下が必要です。

*   AWS CLI （設定済みであること）
*   Python 3.9 以上
*   Python仮想環境を作成するツール (例: `venv`)
*   Node.js と AWS CDK CLI
*   Docker (Lambdaのライブラリをパッケージングするために**必須**です)

## セットアップとデプロイ手順

1.  **リポジトリのクローン:**
    ```bash
    git clone <repository-url>
    cd my-cdk-lambda-arin-project
    ```

2.  **Python仮想環境の作成と有効化:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **CDK用の依存関係をインストール:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Dockerの起動:**
    お使いのシステムでDockerデーモンを起動してください。CDKがLambdaの依存関係をパッケージングする際に使用します。
    (例: `sudo systemctl start docker`)

5.  **環境変数の設定:**
    Google Gemini APIのAPIキーを設定します。
    ```bash
    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```

6.  **CDKデプロイ:**
    全ての準備が整ったら、以下のコマンドでAWSにスタックをデプロイします。
    ```bash
    cdk deploy --all
    ```

## セキュリティに関する注意

APIキーのような機密情報は、環境変数として直接設定するよりも、AWS Secrets Managerなどのサービスを使用して管理することが推奨されます。本番環境で利用する場合は、より安全な方法を検討してください。