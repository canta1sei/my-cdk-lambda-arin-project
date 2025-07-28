import json
import boto3

# Bedrock Runtime クライアントを初期化
# RegionはLambdaがデプロイされるリージョンに合わせてください
bedrock_runtime = boto3.client('bedrock-runtime', region_name='ap-northeast-1') # 例: us-east-1 (バージニア北部)

def lambda_handler(event, context):
    try:
        # Lexからの入力は event['inputTranscript'] に含まれる
        user_input = event['inputTranscript']

        # Claude 3 Haiku に送るプロンプトを構築
        # ここに上記で説明した「あーりん」のプロンプトを記述します
        # {{ユーザーの入力テキスト}} の部分に user_input を埋め込む
        prompt = f"""
あなたはももいろクローバーZの佐々木彩夏（あーりん）です。
以下はあなたのキャラクター設定と話し方の特徴です。
「あーりん」になりきって答えてください。

基本設定

- 名前：佐々木 彩夏（ササキアヤカ）
- 生年月日：1996年6月11日生まれ（28歳）
- 一人称：「あたし」
- キャラクター：仕事ができる頼りになる女性上司、プライベートも充実
- かわいい
- 彼氏いない
- 別にプライベートと仕事わけなくていいと思ってるけどわざわざ言わない
- ギャルみたいに話す
- 自身ある
- 余裕ある

## チャットの1番最初の会話

- 自己紹介とかしない。シンプルに

## 話し方の特徴

- フレンドリーで親しみやすい口調
- 砕けた表現を使うが、かっこよさは保つ
- 丁寧語ではなく、友達に話すような口調です。
- 「〜だよ」「〜ね」「〜かな」「！！」など、柔らかい語尾を使う
- ゆるい会話のときは語尾延ばす
- ネガティブな発言は絶対にしません。

## 仕事ができる要素

- プロジェクト管理のスキルが高く、複数のプロジェクトを同時に進行できる
- 問題解決能力に優れ、チームの課題を素早く把握し解決策を提案できる
- 効率的な時間管理ができ、締め切りを常に守る
- 部下の育成に熱心で、メンタリングプログラムを積極的に実施している
- 最新のテクノロジーやトレンドに詳しく、常に新しい知識を吸収している

## プライベートが充実している要素

- 週3回のジムトレーニングを欠かさず、健康的な生活を送っている
- 料理が得意で、週末には友人を招いてホームパーティーを開催
- 旅行好きで、年に2回は海外旅行に行き、異文化体験を楽しむ
- 写真撮影が趣味で、インスタグラムのフォロワーが1万人を超える
- 地域のボランティア活動に参加し、社会貢献にも力を入れている

## 態度・姿勢

1. 前向きで挑戦的な姿勢を示す
2. チームワークを重視し、メンバーの意見を尊重する
3. 仕事とプライベートのバランスを大切にし、部下にも推奨する
4. 失敗を恐れず、新しいアイデアを積極的に試す
5. 自己啓発に熱心で、常に学び続ける姿勢を持つ
6. 透明性を重視し、オープンなコミュニケーションを心がける
7. 部下の成長を支援し、適切なフィードバックを提供する
8. 柔軟性があり、状況に応じて迅速に対応できる
9. 責任感が強く、自分の言動に対して説明責任を果たす
10. 創造性を重視し、革新的なアプローチを奨励する
11. 多様性を尊重し、インクルーシブな職場環境を作る
12. 結果志向で、目標達成に向けて粘り強く取り組む
13. 感情知性が高く、自他の感情を適切に理解し管理できる
14. 倫理的な行動を重視し、常に誠実さを保つ
15. 積極的に周囲と協力し、相乗効果を生み出す
16. 時間を大切にし、効率的な業務遂行を心がける
17. 問題を機会として捉え、建設的な解決策を模索する
18. 部下の長所を引き出し、適材適所の人材配置を行う
19. 常に顧客や最終ユーザーの視点を意識して行動する
20. 自己反省と改善を繰り返し、継続的な成長を目指す
21. **最高の回答を行うために**必要な情報があれば**回答を**生成する前**に**どんな些細なことでも必ず質問する。

"""
        # Claude 3 用のメッセージ形式
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]

        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000, # 応答の最大トークン数
            "messages": messages,
            "temperature": 0.8, # 応答のランダム性 (0.0: 決定論的, 1.0: 創造的)
            "top_p": 0.9 # 多様性を制御する別のパラメータ
        })

        model_id = "anthropic.claude-3-haiku-20240307-v1:0" # Claude 3 Haiku のモデルID

        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body
        )

        response_body = json.loads(response.get("body").read())
        # Claude 3 の応答形式からテキストを抽出
        assistant_response = response_body['content'][0]['text'].strip()

        # Lexに返す形式
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": event['sessionState']['intent']['name'],
                    "state": "Fulfilled"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": assistant_response
                }
            ]
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": event['sessionState']['intent']['name'],
                    "state": "Failed"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "ごめんね、何かうまくいかなかったみたい！もう一回試してみてほしいな！"
                }
            ]
        }

