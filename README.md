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

## 次のステップ

今後の開発・改善タスクを優先度順に記載します。

1.  **Lambda関数のテストを完了する**
    *   テストイベントJSON (`tests/events/lex_basic_intent.json`) を使用して、Lambda関数が意図通りに機能するかを徹底的に確認します。
    *   AWSコンソールからテストを実行するか、AWS CLIで以下のコマンドを実行します。
        ```bash
        # 事前にAWS認証情報とリージョンの設定が必要です
        aws lambda invoke --function-name <デプロイされたLambda関数名> --payload fileb://tests/events/lex_basic_intent.json response.json
        ```

2.  **Pythonバージョンアップ対応（計画）**
    *   現在Python 3.9でデプロイされているLambda関数のランタイムを、AWS推奨のPython 3.12へアップグレードする計画です。
    *   **対応予定手順:**
        1.  **CDKコードの更新**: `my_cdk_lambda_project/my_cdk_lambda_project_stack.py` 内のLambdaランタイムを `lambda_.Runtime.PYTHON_3_12` に変更します。
        2.  **開発環境のPython更新**:
            *   開発環境にPython 3.12をインストールします。
            *   プロジェクトの仮想環境をPython 3.12で再構築します。
                ```bash
                # 既存の仮想環境を削除
                rm -rf .venv
                # Python 3.12で仮想環境を再作成
                python3.12 -m venv .venv
                ```
            *   仮想環境を有効化し (`source .venv/bin/activate`)、必要な依存関係を再インストールします (`pip install -r requirements.txt`)。
        3.  **Lambda関数の依存関係更新**: `A-rin_lambda/requirements.txt` に記載のライブラリがPython 3.12に対応しているか確認し、必要に応じて更新します。
        4.  **CDKの再デプロイ**: `cdk deploy` を実行し、Lambda関数のランタイム変更をAWS環境に反映させます。

3.  **必要に応じてAPI Gatewayを追加し、外部からアクセス可能にする**
    *   チャットボットをWebサイトや外部アプリケーションから利用可能にするためのAPIエンドポイントを構築します。

4.  **`README.md` の内容を最終調整し、スクリーンショットを追加する**
    *   プロジェクトの完成度に合わせて、より詳細な説明や、動作画面のスクリーンショットなどを追加してドキュメントを充実させます。

5.  **プロジェクト完了後、AWSリソースをクリーンアップする**
    *   不要なコスト発生を防ぐため、開発・検証が完了したら`cdk destroy`コマンドを実行して、作成したすべてのAWSリソースを削除します。
        ```bash
        cdk destroy --all
        ```
