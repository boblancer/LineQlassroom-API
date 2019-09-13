from flask import current_app
from google.cloud import exceptions

def upload_blob(source, id):

    file_name = "LHQ" + str(get_metadata()["TotalHW"] + "_" + id).zfill(5)
    image_blob = current_app.bucket.blob(file_name)
    image_blob.upload_from_file(source)

def get_metadata():
    try:
        doc = current_app.doc_ref.get()
        return doc.to_dict()
    except exceptions.NotFound:
        print(u'No such document!')



def update_image_public_url():
    try:
        current_app.db.document('Students/61090026/homeworkdetail')
    except exceptions.GoogleCloudError:
        print("cloud error")