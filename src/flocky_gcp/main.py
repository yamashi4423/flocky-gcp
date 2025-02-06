import os
import openai
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError


# 環境変数からキーを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LINE Bot API & Webhookパーサー
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

# インスタンス作成
client = openai.OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello World!"}

@app.post("/webhook")
async def webhook(request: Request):
    """LINE Webhook エンドポイント"""
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        return {"status": "error", "message": "Invalid signature"}

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            user_message = event.message.text  # ユーザーのメッセージ

            # ChatGPT に問い合わせ
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            reply_text = response.choices[0].message.content.strip()

            # ユーザーに返信
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    return {"status": "success"}
