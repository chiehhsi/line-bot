import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

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

# imgur key
client_id = '8f7088d3788e5cf'
client_secret = '864e69cc013de5f77e1acfa018c07bed04cc5e32'
album_id = 'YOUR_IMGUR_ALBUM_ID'
access_token = 'YOUR_IMGUR_ACCESS_TOKEN'
refresh_token = 'YOUR_IMGUR_ACCESS_TOKEN'

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

def movie():
    target_url = 'http://www.atmovies.com.tw/movie/next/0/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('ul.filmNextListAll a')):
        if index == 3:
            return content
        title = data.text.replace('\t', '').replace('\r', '')
        link = "http://www.atmovies.com.tw" + data['href']
        content += '{}\n{}\n'.format(title, link)
    return content

def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    text = event.message.text

#Profile photo
    if text == "What does Jessi Looks Like":
        image_message = ImageSendMessage(original_content_url='https://imgur.com/OZ7vuKO', preview_image_url= 'https://imgur.com/OZ7vuKO')
        line_bot_api.reply_message(event.reply_token, image_message)

#Profile info
    if text == "Jessi是誰":
        content = "林倢希\n 國立政治大學 資訊科學系四年級\n Email:j4500123@gmail.com\n 電話:0975241136"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

#Work Experience
    if text == "Jessi的經驗":
        content = "[富邦證券]\n 電子交易科 股票分析預測實習生\n 2018.02-2018.06\n Github: https://github.com/chiehhsi/Tensorflow/blob/master/TSMC-co.ipynb\n [丹麥交換]\n AARHUS UNIVERSITY\n 2018.08-2019.01"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= content))

#Skills        
    if text == "Jessi的技能":
        reply_text = "[中文] 精通\n [英文] 精通\n [韓文] 良好"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text= reply_text))

    if text == "你喜歡做什麼":
        reply_text = "玩..玩..還是玩"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    if text == "你好無聊":
        reply_text = "沒辦法, 做我的人只會這樣"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
    if text == "Bye":
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=1, sticker_id=408))

    if text == "我想看電影":
        content = movie()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    if text == "我想看廢文":
        content = ptt_hot()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
#Introduce Jessi
    if text == "介紹Jessi":
        buttons_template = TemplateSendMessage(
                alt_text = 'Self_intro template',
                template = ButtonsTemplate(
                    title ='Something about Jessi',
                    text = 'Check it out',
                    thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                    actions = [
                        MessageTemplateAction(
                            label = 'What does Jessi Look Like',
                            text = 'What does Jessi Look Like'
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
    else :
        carousel_template_message = TemplateSendMessage(
                alt_text = '目錄 template',
                template = CarouselTemplate(
                    columns = [
                        CarouselColumn(
                            title = 'Chatbot會做的事',
                            text = 'Check it out',
                            actions = [
                                MessageAction(
                                    label ='介紹Jessi',
                                    text='介紹Jessi'
                                    ),
                                MessageAction(
                                    label ='我想看廢文',
                                    text= '我想看廢文'
                                    ),
                                MessageAction(
                                    label = '我想看電影',
                                    text = '我想看電影'
                                    ),
                                ]
                            ),
                        CarouselColumn(
                            title = 'Chatbot 說說話',
                            text = '想對我說什麼',
                            actions = [
                                MessageAction(
                                    label = '你喜歡做什麼',
                                    text = '你喜歡做什麼'
                                    ),
                                MessageAction(
                                    label = '你好無聊',
                                    text = '你好無聊'
                                    ),
                                MessageAction(
                                    label = 'Bye',
                                    text = 'Bye'
                                    ),
                                ]
                            )
                        ]
                    )
                )

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
