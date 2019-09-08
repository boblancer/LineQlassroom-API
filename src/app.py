from flask import Flask, request, jsonify, abort
import src.MessagingApiRoute
app = Flask(__name__)
#app.register_blueprint(src.MessagingApiRoute.app)
@app.route('/')
def home():
    return jsonify({'Qlassroom': 'hello student'})


if __name__ == "__main__":
    app.run()