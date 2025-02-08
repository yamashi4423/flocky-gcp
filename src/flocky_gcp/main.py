import os
import openai
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError


# 環境変数からキーを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LINE Bot API & Webhookパーサー
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

# Botのユーザー情報
bot_profile = line_bot_api.get_bot_info()
BOT_USER_ID = bot_profile.user_id

# OPENAI
MODEL_NAME = "gpt-4o"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Webアプリ立ち上げ
app = FastAPI()
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
        if event.source.type == "user": # DMの場合
            user_message = event.message.text  # ユーザーのメッセージ

            # ChatGPT に問い合わせ
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": user_message}]
            )
            reply_text = response.choices[0].message.content.strip()

            # ユーザーに返信
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    return {"status": "success"}

@handler.add(MessageEvent, message=TextMessage)
def handle_message_on_mention(event):
    # メッセージにメンションが含まれるか確認
    mentionees = event.message.mention
    user_message = event.message.text

    if mentionees:
        for mention in mentionees:
            if mention.user_id == BOT_USER_ID:
                # ChatGPT に問い合わせ
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": user_message}]
                )
                reply_text = response.choices[0].message.content.strip()

                # ユーザーに返信
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                return

