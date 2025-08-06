import json
import os
import google.generativeai as genai

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")

    # APIキーを環境変数から読み込む
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

    # Geminiモデルを初期化
    model = genai.GenerativeModel('gemini-pro')

    # ユーザーの入力を取得
    user_message = event["inputTranscript"]

    # Gemini APIを呼び出し
    try:
        response_from_gemini = model.generate_content(user_message)
        gemini_text_response = response_from_gemini.text
    except Exception as e:
        gemini_text_response = f"ごめんね、エラーが発生しちゃった！: {str(e)}"
        print(f"Gemini API Error: {e}")

    # レスポンスを構築
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

    return response