"""
Example presents usage of the successful compilers() API method
"""
from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException
from time import sleep
import requests

# define access parameters
accessToken = '7dffbeac5ce76c2ee696e93d6fed578a'
endpoint = '63bebb51.compilers.sphere-engine.com'

# initialization
client = CompilersClientV4(accessToken, endpoint)

# API usage
source = """
// Your First C++ Program

#include <iostream>

int main() {
    std::cout << "Hello World!";
    return 0;
}"""
compiler = 1 # C language
inpu = '2017'

try:
    response = client.submissions.create(source, compiler, inpu,time_limit=5, memory_limit=2048)
    # response['id'] stores the ID of the created submission
    print(response)
    print(response['id'])
    
    sleep(5)
    
    out = client.submissions.get(response['id'])
    programOutput = out['result']['streams']['output']
    
    print(programOutput)
    
    if(programOutput):
        x = requests.get(programOutput['uri'])
        
        print(x.content)
    
    sleep(5)

    
except SphereEngineException as e:
    print("ERROR", e.code)
    print("ERROR", e)
    if e.code == 401:
        print('Invalid access token')
    elif e.code == 402:
        print('Unable to create submission')
    elif e.code == 400:
        print('Error code: ' + str(e.error_code) + ', details available in the message: ' + str(e))