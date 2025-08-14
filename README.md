# 私のCDK Lambda A-rinプロジェクト

このプロジェクトは、AWS CDKとReactを使用して、Google Gemini APIを活用したフルスタックAIチャットボットを構築・デプロイするサンプルです。

## 主要技術

*   **フロントエンド**
    *   React (TypeScript)
    *   Vite
    *   axios
*   **バックエンド**
    *   AWS CDK (Python)
    *   AWS Lambda
    *   AWS API Gateway
    *   AWS Secrets Manager
*   **その他**
    *   Google Gemini API
    *   Python 3.9
    *   Docker

## プロジェクト構造

*   `frontend/`: Reactで構築されたフロントエンドアプリケーション。
    *   `src/App.tsx`: チャットUIのメインコンポーネント。
    *   `vite.config.ts`: APIリクエストをバックエンドに転送（プロキシ）するための設定。
*   `A-rin_lambda/`: Lambda関数のソースコードと依存関係。
    *   `A-rinApp.py`: チャットボットのコアとなるLambda関数コード。
*   `my_cdk_lambda_project/`: AWSインフラを定義するCDKコード。
    *   `my_cdk_lambda_project_stack.py`: Lambda, API Gateway等をデプロイするCDKスタック定義。
*   `app.py`: CDKアプリケーションのエントリーポイント。
*   `cdk.json`: CDKの設定ファイル。

## 動作に必要な環境 (Prerequisites)

*   AWS CLI （設定済みであること）
*   Python 3.9 以上
*   Node.js と npm
*   AWS CDK CLI (`npm install -g aws-cdk`)
*   Docker (Lambdaのライブラリをパッケージングするために**必須**です)

## セットアップと実行手順

このアプリケーションは、AWSにデプロイされる**バックエンド**と、ローカルで実行する**フロントエンド**で構成されます。

### 1. バックエンドのセットアップとデプロイ

まず、バックエンドのAWSリソースを準備・デプロイします。

1.  **リポジトリのクローンと移動:**
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
    お使いのシステムでDockerデーモンを起動してください。

5.  **APIキーをSecrets Managerに保存:**
    Google Gemini APIのキーをAWS Secrets Managerに `gemini-api-key` という名前で保存します。
    ```bash
    # 初回のみ実行
    aws secretsmanager create-secret --name gemini-api-key --secret-string YOUR_GEMINI_API_KEY
    ```
    ※ `YOUR_GEMINI_API_KEY` の部分を実際のAPIキーに置き換えてください。

6.  **CDKデプロイ:**
    以下のコマンドでAWSにスタックをデプロイします。
    ```bash
    cdk deploy --all
    ```
    デプロイが完了すると、`Outputs`としてAPI GatewayのエンドポイントURLが表示されます。このURLはフロントエンドの設定で使用します。

### 2. フロントエンドのセットアップと実行

バックエンドのデプロイが完了したら、フロントエンドのチャット画面を起動します。

1.  **Viteプロキシ設定の更新:**
    `frontend/vite.config.ts` ファイルを開き、`target` をご自身のAPI GatewayエンドポイントURLに設定してください。（この作業はすでに行われています）

2.  **フロントエンド用の依存関係をインストール:**
    ```bash
    cd frontend
    npm install
    ```

3.  **開発サーバーの起動:**
    ```bash
    npm run dev
    ```
    サーバーが起動したら、コンソールに表示されるURL（通常は `http://localhost:5173`）にブラウザでアクセスしてください。チャット画面が表示されます。

## 本日の更新内容 (Development Log)

*   **フロントエンドアプリケーションの構築:** ReactとViteを使用して、ユーザーがメッセージを入力し、AIからの応答を表示するUIを構築しました。
*   **バックエンドAPIとの連携:**
    *   当初、フロントエンドとバックエンドのAPI仕様（リクエスト/レスポンス形式）が異なっていましたが、フロントエンド側を修正してバックエンドの仕様に合わせました。
    *   開発サーバーからAWS上のAPIを呼び出す際に発生するCORSエラーと404エラーを解決しました。
        *   **CORS対応:** バックエンド(CDK)側にCORS許可設定を追加しました。
        *   **プロキシ設定:** フロントエンド(Vite)にプロキシを設定し、APIリクエストが正しくバックエンドに転送されるようにしました。
*   **READMEの更新:** フロントエンドの起動方法や、ここまでの開発経緯を反映させました。

## セキュリティに関する注意

このプロジェクトでは、APIキーのような機密情報を安全に管理するため、AWS Secrets Managerを利用しています。Lambda関数は実行時に動的にSecrets ManagerからAPIキーを取得するため、コードや環境変数に直接キー情報が含まれることはありません。

## 次のステップ

今後の開発・改善タスクを優先度順に記載します。

1.  **フロントエンドのAWSへのデプロイ (S3 + CloudFront)**
    *   現在ローカルで動作しているフロントエンドアプリケーションを、Amazon S3とCloudFrontを利用してAWS上にデプロイし、インターネットからアクセス可能にします。
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
3.  **設定管理の改善（将来的な課題）**
    *   現在、モデル名などの設定を簡単のために`config.json`ファイルに記述していますが、これは一時的な措置です。
    *   本番環境やチームでの開発を見据える場合、設定値は環境変数や、AWS Systems Manager Parameter Store、AWS Secrets Managerといった、よりセキュアで管理しやすい方法に移行することを推奨します。
4.  **プロジェクト完了後、AWSリソースをクリーンアップする**
    *   不要なコスト発生を防ぐため、開発・検証が完了したら`cdk destroy`コマンドを実行して、作成したすべてのAWSリソースを削除します。
        ```bash
        cdk destroy --all
        ```