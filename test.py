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

ACCESS_TOKEN = os.environ["DGah4VpgHL2R53MwQmwuR3VfVhxxImseP/gHWjuNr+L7hDcy4NhWXiWIMqb1zFe0tR308g07R8m2g3rxUq5z4LprpK+OKLdWplH4D0OmfiKvZ7Dk8g0UawF556PdAj4ChJ94eicJcYDfQuCv2H49pQdB04t89/1O/w1cDnyilFU="]
CHANNEL_SECRET = os.environ["993fd2773e79e311f8a784c3ae2d9ef1"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['post'])
def callback():
    signature = request.headers['X-Line=Signature']

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


if __name__ == "__main__":

    port = int(os.getenv(("PORT", 5000)))
    app.run("0.0.0.0", port=port)

