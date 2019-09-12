from flask import current_app
from google.cloud import exceptions

def upload_blob(source):

    file_name = "LHQ" + str(get_metadata()["TotalHW"]).zfill(5)
    image_blob = current_app.bucket.blob(file_name)
    image_blob.upload_from_file(source)
    increment_homework()

def get_metadata():
    try:
        doc = current_app.doc_ref.get()
        return doc.to_dict()
    except exceptions.NotFound:
        print(u'No such document!')


def increment_homework():
    try:
        data = get_metadata()
        print(data)
        data["TotalHW"] += 1
        current_app.doc_ref.set(data)
    except exceptions.GoogleCloudError:
        print("cloud error")

