from flask import Flask, request, jsonify
import src.MessagingApiRoute
app = Flask(__name__)
app.register_blueprint(src.MessagingApiRoute.image)
@app.route('/')
def home():
    return jsonify({'Qlassroom': 'hello student'})
