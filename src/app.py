from flask import Flask, request, jsonify, abort
import src.MessagingApiRoute
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ServiceAccountSecretKey.json"
cred = credentials.Certificate("../ServiceAccountSecretKey.json")
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'metadata').document(u'config')

storage = storage.Client()
bucket = storage.get_bucket("line-qlassroom2019.appspot.com")
state = {}
app = Flask(__name__)
app.register_blueprint(src.MessagingApiRoute.app)
@app.route('/')
def home():
    return jsonify({'Qlassroom': 'hello student'})


if __name__ == "__main__":
    app.run()