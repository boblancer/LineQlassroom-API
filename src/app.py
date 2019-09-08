from flask import Flask, request, jsonify
import src.MessagingApiRoute
app = Flask(__name__)
#app.register_blueprint(src.MessagingApiRoute.app)
@app.route('/')
def home():
    return jsonify({'Qlassroom': 'hello student'})

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage)

handler = WebhookHandler('ff13ecf3c4dc16c47bee15857376aab4')
line_bot_api = LineBotApi('7ZhYcRofXp0gR++3VC0aXV+Xtt36XSsCtpqu8Hpwh/L2b70FE0wN5G2SkPW5QqjLMGobF9FXglqyxB3A+YotCPN5'
                          'JZk2nzBYtiu76OxYnv9BBSmaUbLHW5hA2IG3odqJkrEwd2vFu3JC8s7g7VDajgdB04t89/1O/w1cDnyilFU=')

@app.route('/bot')
def bottest():
    line_bot_api.push_message("Ue952fb83bb2975a6ec362d1fe8cf8338", TextSendMessage(text='Hello World!'))
    return jsonify({'botbot': 'hello student'})

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    print("plspls")
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()