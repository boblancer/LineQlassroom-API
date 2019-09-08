from flask import Flask , Blueprint, jsonify, abort, request

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage)

app = Blueprint('MessagingApiRoute', __name__)

line_bot_api = LineBotApi('7ZhYcRofXp0gR++3VC0aXV+Xtt36XSsCtpqu8Hpwh/L2b70FE0wN5G2SkPW5QqjLMGobF9FXglqyxB3A+YotCPN5'
                          'JZk2nzBYtiu76OxYnv9BBSmaUbLHW5hA2IG3odqJkrEwd2vFu3JC8s7g7VDajgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ff13ecf3c4dc16c47bee15857376aab4')


@app.route('/image')
def show():
    print("bat")
    return jsonify({"Pokemon": "Go"})


@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    raise Exception(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    raise Exception(event)
    message_content = line_bot_api.get_message_content(event.message.id)
    result = ""
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="fuck"))
    with open("../buffer", 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
            result += str(chunk)
    print({"content": result})

