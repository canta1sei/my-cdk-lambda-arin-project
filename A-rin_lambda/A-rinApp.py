import json
import os
import boto3
import google.generativeai as genai

# --- 初期化処理 (Lambdaのコールドスタート時に一度だけ実行) ---

# 設定ファイルを読み込む
with open('config.json', 'r') as f:
    config = json.load(f)
MODEL_NAME = config['model_name']

# 環境変数からシークレット名を取得
SECRET_NAME = os.environ.get("SECRET_NAME")

# APIキーをSecrets Managerから取得する関数
def get_api_key():
    if not SECRET_NAME:
        raise ValueError("Environment variable 'SECRET_NAME' is not set.")

    try:
        # boto3を使ってSecrets Managerクライアントを作成
        client = boto3.client('secretsmanager')
        
        # シークレットの値を取得
        get_secret_value_response = client.get_secret_value(
            SecretId=SECRET_NAME
        )
        
        # シークレットは文字列として取得されるので、必要に応じてパース
        # この例では、シークレットがプレーンテキストで保存されていると仮定
        return get_secret_value_response['SecretString']

    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise e

# Geminiクライアントを初期化
API_KEY = get_api_key()
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# --- Lambdaハンドラー関数 ---

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    user_message = ""
    try:
        # API Gatewayからのリクエストの場合、bodyは文字列なのでパースする
        if 'body' in event and isinstance(event['body'], str):
            body = json.loads(event['body'])
            user_message = body.get("inputTranscript", "")
        # Lexからのテストイベントや直接呼び出しの場合
        else:
            user_message = event.get("inputTranscript", "")

        if not user_message:
             raise ValueError("inputTranscript is empty or not found")

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Error parsing input: {e}")
        return {
            'statusCode': 400,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'message': 'Bad Request: Invalid input format.'})
        }

    # Gemini APIを呼び出し
    try:
        response_from_gemini = model.generate_content(user_message)
        gemini_text_response = response_from_gemini.text
    except Exception as e:
        gemini_text_response = f"ごめんね、エラーが発生しちゃった！: {str(e)}"
        print(f"Gemini API Error: {e}")

    # API Gatewayに返すレスポンスを構築
    # LexのフォーマットとAPI Gatewayのフォーマットを判定
    if 'sessionState' in event:
        # Lexフォーマットのレスポンス
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": event["sessionState"]["intent"]["name"],
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": gemini_text_response
                }
            ]
        }
    else:
        # API Gateway用のHTTPレスポンス
        response = {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({'response': gemini_text_response})
        }

    return response
