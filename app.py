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
config = configparser.ConfigParser()
config.read("config.ini")

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
def profile():

    content = "Jessi"
    return content

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    text = event.message.text

#Profile photo
    if text == "How do Jessi Look":
        image_message = ImageSendMessage(original_content_url='https://drive.google.com/file/d/1TtCrL2qUuiKX1_Dpy6tkF_FLvcdXiXis/view?usp=sharing', preview_content_url= 'https://drive.google.com/file/d/1TtCrL2qUuiKX1_Dpy6tkF_FLvcdXiXis/view?usp=sharing')
        line_bot_api.reply_message(event.reply_token, image_message)

#Profile info
    if text == "Jessi是誰":
        content = "林倢希%0D%0A 國立政治大學 資訊科學系四年級%0D%0A Email:j4500123@gmail.com%0D%0A電話:0975241136"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

#Work Experience
    if text == "Jessi的經驗":
        content = "[富邦證券] %0D%0A 電子交易科 股票分析預測實習生%0D%0A 2018.02-2018.06 %0D%0A Github: https://github.com/chiehhsi/Tensorflow/blob/master/TSMC-co.ipynb %0D%0A [丹麥交換]%0D%0A AARHUS UNIVERSITY%0D%0A2018.08-2019.01"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= content))

#Skills        
    if text == "Jessi的技能":
        reply_text = "[中文] 精通\n [英文] 精通\n [韓文] 良好\n"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= reply_text))

    if text == "Thank you"||"Thanks" :
        reply_text = "Tell me if you want to know about Jessi"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    if text == "Bye":
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=1, sticker_id=408))

    else:
        buttons_template = TemplateSendMessage(
                alt_text = 'Self_intro template',
                template = ButtonsTemplate(
                    title ='Something about Jessi',
                    text = 'Check it out',
                    thumbnail_image_url='https://i.imgur.com/kzi5kKy.jpg',
                    actions = [
                        MessageTemplateAction(
                            label = 'How do Jessi Look',
                            text = 'How do Jessi Look?'
                            ),
                        MessageTemplateAction(
                            label = 'Jessi是誰',
                            text = 'Jessi是誰'
                            ),
                        MessageTemplateAction(
                            label = 'Jessi的經驗',
                            text = 'Jessi的經驗'
                            ),
                        MessageTemplateAction(
                            label = 'Jessi的技能',
                            text = 'Jessi的技能'
                            ),
                        ]
                    )
                )
        line_bot_api.reply_message(event.reply_token, buttons_template)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
     # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 119, 120, 121, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402, 403, 404, 405, 406, 407, 408, 410, 411, 412, 414, 415, 416, 417, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage( package_id='1', sticker_id=sticker_id)
    line_bot_api.reply_message(event.reply_token,sticker_message)


import os
if __name__ == "__main__":
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
