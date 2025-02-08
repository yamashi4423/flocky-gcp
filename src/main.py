import os
import openai
from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import logging
from utils import hello_world, response_text_from_llm


# 環境変数からキーを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ログの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        return {"status": "error", "message": "Invalid signature"}
    return {"status": "success"}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # DMの場合
    if event.source.type == "user":
        user_message = event.message.text
        reply_text = response_text_from_llm(user_message, client, MODEL_NAME)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))

    # グループ or 複数人トークの場合
    elif event.source.type in ["group", "room"]:
        mentionees = event.message.mention.mentionees if event.message.mention else []
        user_message = event.message.text

        for mention in mentionees:
            if mention.user_id == BOT_USER_ID:
                reply_text = response_text_from_llm(user_message, client, MODEL_NAME)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                return