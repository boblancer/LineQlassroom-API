from flask import Flask, Blueprint, jsonify, abort, request, current_app
import src.DB
import requests
import ast
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
access_token = ('XF9eRcyOk/nZd5hmo+e1/l3UL/sFMbaO3r0OHuSm0volMzYLoux5NshVwOdRlAaQBcrzw0h6tHkysVE4GppMm+tSbxRQ'
                'EHbE7hZnQpZrwYvZfSgJgL5kG/RQhvDcrljdKSJqMMaV3OdufeCPqWJrAwdB04t89/1O/w1cDnyilFU=')
line_bot_api = LineBotApi(access_token)
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
    message = {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "nano",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "In Progress",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "70%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": "70%",
                                    "backgroundColor": "#0D8186",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#27ACB2",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Buy milk and lettuce before class",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": true
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": false
                    }
                }
            },
            {
                "type": "bubble",
                "size": "nano",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "Pending",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "30%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": "30%",
                                    "backgroundColor": "#DE5658",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#FAD2A76E",
                            "height": "6px",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#FF6B6E",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Wash my car",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": true
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": false
                    }
                }
            },
            {
                "type": "bubble",
                "size": "nano",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "In Progress",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "md",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "100%",
                            "color": "#ffffff",
                            "align": "start",
                            "size": "xs",
                            "gravity": "center",
                            "margin": "lg"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "filler"
                                        }
                                    ],
                                    "width": "100%",
                                    "backgroundColor": "#7D51E4",
                                    "height": "6px"
                                }
                            ],
                            "backgroundColor": "#9FD8E36E",
                            "height": "6px",
                            "margin": "sm"
                        }
                    ],
                    "backgroundColor": "#A17DF5",
                    "paddingTop": "19px",
                    "paddingAll": "12px",
                    "paddingBottom": "16px"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Buy milk and lettuce before class",
                                    "color": "#8C8C8C",
                                    "size": "sm",
                                    "wrap": true
                                }
                            ],
                            "flex": 1
                        }
                    ],
                    "spacing": "md",
                    "paddingAll": "12px"
                },
                "styles": {
                    "footer": {
                        "separator": false
                    }
                }
            }
        ]
    }

    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}
    # data = {
    #     "replyToken": event.reply_token,
    #     "messages":[
    #         ast.literal_eval(message)
    #     ]
    # }
    data = {
        "replyToken": event.reply_token,
        "messages":[
            message, message
        ]
    }
    r = requests.post('https://api.line.me/v2/bot/message/reply', data=json.dumps(data), headers=headers)





