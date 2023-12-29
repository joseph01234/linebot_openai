from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import os

app = Flask(__name__)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

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
    text = event.message.text
    if '組員名單'in text:  
        # 用户输入包含“組員”的情况
        output_text = '資工4C \n409410510 游家碩\n409411021 馬儒彬\n409411054 周庭蔚'
        message = TextSendMessage(text=output_text)
        line_bot_api.reply_message(event.reply_token, message)
    elif'科目內容'in text:
        output_text ='金融科技理論與實務-產業應用與趨勢'
        message = TextSendMessage(text=output_text)
        line_bot_api.reply_message(event.reply_token, message)
    elif'授課老師'in text:
        output_text ='林明杰'
        message = TextSendMessage(text=output_text)
        line_bot_api.reply_message(event.reply_token, message)
     elif'坐殺博徒'in text:
         message = VideoSendMessage(
            original_content_url='https://memeprod.ap-south-1.linodeobjects.com/user-maker-thumbnail/120dc96e75b25c107485a60f21d5efb1.gif',
            preview_image_url='https://memeprod.ap-south-1.linodeobjects.com/user-maker-thumbnail/120dc96e75b25c107485a60f21d5efb1.gif'
         )
          line_bot_api.reply_message(event.reply_token, message)
    else:
        # 用户输入不包含“組員”的情况，直接回复用户输入的文本
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text))




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
