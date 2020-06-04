from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from change_items import change_items
from search_items import search_items

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('SP1vXi5BkkR6FcVegl+gSRSNkuuKNp7JcGvAFI2AIq8MRS1d5ghykGBTMvvfAuNoAI7fvxMx1DHvpe+6I+nLe495mdoq0OwCwJCjnSE8IY4QzrD54+vnP7aPvXeihYlmbqkyO9BF4cPiS1JQXSSTOAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('80b3674657a8bd701d965046f7d432e2')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    ordi_message = event.message.text
    message = ordi_message.split()
    reply_message = ""
    if(message[0].lower() == 'add'):
        result = change_items(message[1],message[2],user_id)
        if(result == "ERROR"):
            reply_message = '出現問題了!請回報工程師'
        elif(result == "Success"):
            reply_message = '修改數據成功!'
    elif(message[0].lower() == 'reduce'):
        result = change_items(message[1],str(-1*int(message[2])),user_id)
        if(result == "ERROR"):
            reply_message = '物品不存在'
        elif(result == "Success"):
            reply_message = '修改數據成功!'
    elif(message[0].lower() == 'check'):
        result = search_items(message[1],user_id)
        if(result == "ERROR"):
            reply_message = "物品不存在"
        else:
            reply_message = message[1] + '目前數量: ' + result
    elif(message[0].lower() == 'list'):
        result = search_items('ALL_ITEMS',user_id)
        if(result == "ERROR"):
            reply_message = '您尚未新增任何物品喔!'
        else:
            reply_message = result
    else:
        reply_message = ordi_message
    line_bot_api.reply_message(reply_token, TextSendMessage(text = reply_message))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)
