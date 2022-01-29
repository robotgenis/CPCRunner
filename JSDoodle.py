import requests
import json


clientId = "8d4f846be4e1d90c42a9dd64fc544cd"
clientSecret = "d9e2b9a4474c5eb499106490a9c2b52641992066385dec916ea4c8d0c186b997"
script = """
print(input())
print(input())
"""
language = "python3"
versionIndex = 4
inp = "Hi there!\nHi there"

url = "https://api.jdoodle.com/v1/execute"

def testCall():
    
    
    data = {
        "clientId":  clientId,
        "clientSecret": clientSecret,
        "script":script,
        "language": language,
        "versionIndex": str(versionIndex),
        "stdin": inp,
    }
    headers = {'Content-type': 'application/json'}
    print(data)
    
    
    out =  requests.post(url, data=json.dumps(data), headers=headers)
    
    
    print(out)
    print(out.content)

testCall()