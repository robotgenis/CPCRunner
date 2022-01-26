from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['get','post'])
def hello():
    return "hello"


