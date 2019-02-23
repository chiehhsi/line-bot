import requests
import re
import random
import configparser
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('06kc7waJVq9BYlHa+NNFSErsNYBKfbNti3zZByetNA0sUmzGks4+vOZ1ID0Sgg0vdOfCjKrAweEJWbO1LGf6uqbFqX7j+wEGy6/cOtfRdQz8GEzk9dKC2ixu8lY3UHBZVMYQjSM5r8ZJM82GxSWspQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('8ba7f286a5b9c3b94f95b751240543b5')

@app.route('/')
def index():
    return "<p>Hello World!</p>"

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "Hi":
        message ="Hello"
    else:
        message = TextSendMessage(text=event.message.text)

    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
