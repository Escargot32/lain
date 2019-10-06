from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=TextMessage)
def test_handle(event):
    sent_text = event.message.text
    if(sent_text == "Hello"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hi!")
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello World!")
        )


if __name__ == "__main__":

    port = int(os.getenv("PORT", 5000))
    app.run("0.0.0.0", port=port)

