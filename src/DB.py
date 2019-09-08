import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage
from firebase import firebase

cred = credentials.Certificate("../ServiceAccountSecretKey.json")
default_app = firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

storage = storage.Client()
bucket = storage.get_bucket("gs://line-qlassroom-7bed0.appspot.com")