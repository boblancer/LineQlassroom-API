from flask import Flask, Blueprint, jsonify, abort, request, current_app
import src.DB
import json
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
    ImageMessage, Content, CarouselTemplate, TemplateSendMessage, PostbackAction, CarouselColumn, MessageAction,
    URIAction)
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
    student_id = current_app.state.session[str(event.source.user_id)].student_id
    hw = current_app.state.session[str(event.source.user_id)].homework_id
    doc_ref = current_app.db.collection(u'Students').document(student_id).collection(u'HomeworksDetail').document(hw)
    doc_ref.update({"url": public_url})
    project_id = "line-qlassroom2019"


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(event.message.text)))
    '''
    project_id = "line-qlassroom2019"
    session_id = event.source.user_id
    if str(event.source.user_id) not in current_app.state.session:
        current_app.state.session[str(event.source.user_id)] = model.CreateHomework()
    else:
        current_app.state.session[str(event.source.user_id)].clear()
    message = dialogflow.detect_intent_texts(project_id, session_id, {event.message.text:""}, "th")
    carousel_template_message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item1.jpg',
                    title='this is menu1',
                    text='description1',
                    actions=[
                        PostbackAction(
                            label='postback1',
                            display_text='postback text1',
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='message1',
                            text='message text1'
                        ),
                        URIAction(
                            label='uri1',
                            uri='http://example.com/1'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://example.com/item2.jpg',
                    title='this is menu2',
                    text='description2',
                    actions=[
                        PostbackAction(
                            label='postback2',
                            display_text='postback text2',
                            data='action=buy&itemid=2'
                        ),
                        MessageAction(
                            label='message2',
                            text='message text2'
                        ),
                        URIAction(
                            label='uri2',
                            uri='http://example.com/2'
                        )
                    ]
                )
            ]
        )
    )

    rep = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_2_restaurant.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "spacer",
                    "size": "xxl"
                },
                {
                    "type": "button",
                    "style": "primary",
                    "color": "#905c44",
                    "action": {
                        "type": "uri",
                        "label": "Add to Cart",
                        "uri": "https://linecorp.com"
                    }
                },
                {
                    "type": "spacer",
                    "size": "xxl"
                }
            ]
        }
    }

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=str(message)))
    line_bot_api.reply_message(
        event.reply_token,
        json.dumps(rep))





