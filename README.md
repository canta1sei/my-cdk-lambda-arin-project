# 私のCDK Lambda A-rinプロジェクト

このプロジェクトは、AWS CDK、Python Lambda、およびAmazon Bedrockを使用してAIチャットボットを構築およびデプロイする方法を示すものです。カスタムVPCのセットアップからLambda関数のデプロイまで、エンドツーエンドの構築をカバーしています。

## 使用技術

* AWS CDK (Python)
* AWS Lambda
* Amazon Bedrock (Claudeモデル)
* AWS VPC, サブネット, インターネットゲートウェイ, ルートテーブル
* Python 3.9+
* pipenv

## プロジェクト構造

* `A-rin_lambda/A-rinApp.py`: チャットボットのコアとなるLambda関数コード。
* `my_cdk_lambda_project/my_cdk_lambda_project_stack.py`: Lambda関数とIAMロールをデプロイするためのCDKスタック定義。
* `tests/events/`: Lambda関数のテストイベントJSONファイルを格納するディレクトリ。

## セットアップとデプロイ

1.  **VPCとEC2のセットアップ**: カスタムVPC、パブリックサブネット、インターネットゲートウェイ、および適切なIAMロールを持つEC2インスタンス（`t2.small`）を設定しました。
2.  **CDK開発環境のセットアップ**: EC2インスタンスにNode.js、npm、pipenv、AWS CDK CLIをインストールしました。
3.  **CDKブートストラップ**: `cdk bootstrap` を実行し、AWS環境の準備を行いました。
4.  **依存関係のインストール**: `pipenv install` を実行し、プロジェクトの依存関係をインストールします。
5.  **CDK設定の更新**: `cdk.json` の `app` 設定を `"pipenv run python app.py"` に変更し、`pipenv` 仮想環境を使用するようにします。
6.  **Lambdaデプロイ**: `cdk deploy` を使用してLambda関数と関連するIAMロールをデプロイします。

## 次のステップ

優先度順に記載しています。

1.  **Lambda関数の `KeyError: 'sessionState'` を解決する。**
    * **完了済み**。`A-rin_lambda/A-rinApp.py` に `event.get()` を使用する修正を適用し、デプロイ済み。
2.  **Lambda関数のタイムアウトを解決する。**
    * **完了済み**。`my_cdk_lambda_project/my_cdk_lambda_project_stack.py` に `timeout=Duration.seconds(30)` を追加し、デプロイ済み。
3.  **Lambda関数のテストを完了する。**
    * テストイベントJSON (`tests/events/lex_basic_intent.json` など) を作成し、AWS CLIの `aws lambda invoke` コマンド (`fileb://` プレフィックスを使用) またはAWSコンソールからテストを実行して、チャットボットが意図通りに機能するかを徹底的に確認します。
4.  **Pythonバージョンアップ対応（計画）**
    * 現在Python 3.9でデプロイされているLambda関数のランタイムを、AWS Lambdaで推奨されるPython 3.12へアップグレードする計画です。
    * **対応予定手順:**
        1.  **CDKコードの更新**: `my_cdk_lambda_project/my_cdk_lambda_project_stack.py` 内のLambdaランタイムを `lambda_.Runtime.PYTHON_3_12` に変更します。
        2.  **EC2インスタンスのPython環境更新**:
            * EC2インスタンスにPython 3.12をインストールします (`sudo dnf install python3.12 -y` など)。
            * `pipenv` を使用して、プロジェクトの仮想環境をPython 3.12で再構築します (`pipenv --rm` 後、`pipenv --python 3.12 install`)。
            * 仮想環境をアクティブ化し (`pipenv shell`)、必要な依存関係を再インストールします (`pip install -r requirements.txt`)。
        3.  **Lambda関数の依存関係更新**: Lambda関数 (`A-rin_lambda`) 独自の依存関係がある場合、それらもPython 3.12環境で更新します。
        4.  **CDKの再デプロイ**: `cdk deploy` を実行し、Lambda関数のランタイム変更をAWS環境に反映させます。
5.  **必要に応じてAPI Gatewayを追加し、外部からアクセス可能にする。**
    * チャットボットを外部から利用可能にするためのAPIエンドポイントの構築です。
6.  **`README.md` の内容を最終調整し、スクリーンショットを追加する。**
    * プロジェクトの完了度合いに合わせて、より詳細な説明や、動作画面のスクリーンショットなどを追加し、見栄えを良くします。Findyへのアピールにも繋がります。
7.  **プロジェクト完了後、AWSリソースをクリーンアップする。**
    * 不要なコスト発生を防ぐため、開発・検証が完了したらリソースを削除します。