import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage
import json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/ServiceAccountSecretKey.json"
'''
with open('ServiceAccountSecretKey.json') as dataFile:
    data = dataFile.read()
    obj = data[data.find('{') : data.rfind('}')+1]
    jsonObj = json.loads(obj)

cred = credentials.Certificate("../ServiceAccountSecretKey.json")
default_app = firebase_admin.initialize_app(cred)
firestore_db = firestore.client()
'''

storage = storage.Client()
bucket = storage.get_bucket("gs://line-qlassroom-7bed0.appspot.com")

def upload_blob(source):
    imageBlob = bucket.blob("foobar")
    imageBlob.upload_from_file(source)


