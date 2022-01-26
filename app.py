from flask import Flask, request
from runProgram import runProgram
import json

app = Flask(__name__)

#{"type":"TYPE_PYTHON","code":"print(input());","timer":"6.0","inputs":["1","2","3"]}

@app.route("/", methods=['get','post'])
def hello():
    j = request.get_json(force=True)
    typ = j["type"]
    code = j["code"]
    timer = j["timer"]
    inputs = j["inputs"]
    
    result = runProgram(typ, timer, code, inputs)
    print(result)
    
    return json.dumps(result)


