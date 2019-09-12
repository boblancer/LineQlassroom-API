import re
import json
from flask import make_response, current_app

def dialogfow_api(request):
    request_json = request.get_json(silent=True, force=True)
    response = process_req(request_json)
    response_json = json.dumps(response, indent=4)
    res = make_response(response_json)
    res.headers['Content-Type'] = 'application/json'
    return res

def process_req(request):
    message = 'Hello line qlassroom'

    intent = request['queryResult']['intent']['displayName']

    if intent == 'StudentSubmitHW/StudentID/HomeworkID':
        param = request['queryResult']['outputContexts'][0]['parameters']
        homework_id = param['HomeworkID.original'].upper()
        student_id = param['StudentID.original']

        if re.search('^LQH.*', homework_id):
            message = 'StudentID {} HomeworkID {}'.format(student_id, homework_id)
        else:
            message = 'เกิดข้อผิดพลาดกรุณาลองใหม่อีกครั้ง'

    elif intent == 'StudentReport/GetStudentID':
        param = request['queryResult']['outputContexts'][0]['parameters']
        student_id = param['StudentID.original']

        try:
            from datetime import date, timedelta
            dt = date.today()
            start = dt - timedelta(days=dt.weekday())
            end = start + timedelta(days=6)
            start = start.strftime('%d/%m/%Y')
            end = end.strftime('%d/%m/%Y')

            totalHW = 0


            homeworks = current_app.db.collection(u'Students').document(student_id).collection(u'HomeworksDetail') \
                .where(u'DueDate', u'>=', str(start)).where(u'DueDate', u'<=', str(end)).stream()

            message = '- รายงานของฉัน -' \
                     '\nตั้งแต่วันที่ {} - {}\n'.format(start, end)

            for h in homeworks:
                totalHW += 1
                homework = h.to_dict()
                message += '\nวิชา {}' \
                          '\nเรื่อง {}'.format(homework['Subject'], homework['Name'])
                if homework['Score']:
                    message += '\nสถานะ ส่งแล้ว' \
                              '\nคะแนน {}/{}' \
                              '\n---------------'.format(homework['Score'], homework['TotalScore'])
                else:
                    message += '\nสถานะ ยังไม่ส่ง' \
                              '\nกำหนดส่ง {}' \
                              '\n---------------'.format(homework['DueDate'])

            message += '\n\n\nจำนวนการบ้านทั้งหมด {}'.format(totalHW)


        except Exception:
            message = 'can connect to db'

    res = make_webhook_res(message)
    return res

def make_webhook_res(message):
    res = {
        'fulfillmentText': message
    }
    return res
