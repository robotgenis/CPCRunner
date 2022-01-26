from flask import Flask, request

app = Flask(__name__)

#{"type":"TYPE_PYTHON","code":"print(input());","timer":"6.0","inputs":["1","2","3"]}

@app.route("/", methods=['get','post'])
def hello():
    return "hello"


