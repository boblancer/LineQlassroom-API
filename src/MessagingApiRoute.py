from flask import Flask, Blueprint, jsonify, abort, request, current_app
import src.DB
import src.DialogFlow as dialogflow
import src.CreateHomeworkModel as model
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage, Content)
app = Blueprint('MessagingApiRoute', __name__)

line_bot_api = LineBotApi('XF9eRcyOk/nZd5hmo+e1/l3UL/sFMbaO3r0OHuSm0volMzYLoux5NshVwOdRlAaQBcrzw0h6tHkysVE4GppMm+tSbxRQ'
                          'EHbE7hZnQpZrwYvZfSgJgL5kG/RQhvDcrljdKSJqMMaV3OdufeCPqWJrAwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a969bc64bdb41abc6f669c85893463a4')


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
    current_app.logger.info("Request body: " + body)

    # handle webhook body

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    public_url = None
    current_app.logger.info("Content id: " + str(event.source.user_id))
    message_content: Content = line_bot_api.get_message_content(event.message.id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(event.source.user_id)))
    with open("tmp/temp", 'wb') as f:
        for chunk in message_content.iter_content():
            f.write(chunk)
            current_app.logger.info(chunk)
    with open("tmp/temp", "rb") as f:
        public_url = src.DB.upload_blob(f)
    student_id = current_app.state[str(event.source.user_id)].student_id
    hw = current_app.state[str(event.source.user_id)].homework_id
    doc_ref = current_app.db.collection(u'Students').document(student_id).collection(u'HomeworksDetail').document(hw)
    doc_ref.update({"url": public_url})
    project_id = "linemessage-qlwfhy"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(event.message.text)))
    '''
    project_id = "linemessage-qlwfhy"
    session_id = event.source.user_id
    if str(event.source.userId) not in current_app.state:
        current_app.state[str(event.source.user_id)] = model.CreateHomework()
    message = dialogflow.detect_intent_texts(project_id, session_id, event.message.text, "th")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(message)))




