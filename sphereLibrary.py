
from sphere_engine import CompilersClientV4
from sphere_engine.exceptions import SphereEngineException
from time import sleep
import requests
from sympy import true

# define access parameters
accessToken = '7dffbeac5ce76c2ee696e93d6fed578a'
endpoint = '63bebb51.compilers.sphere-engine.com'

# initialization
client = CompilersClientV4(accessToken, endpoint)

COMPILER_PYTHON = 116
COMPILER_CPP = 1


class TestCase:
    def __init__(self, inpu:str, outp:str):
        self.inpu = inpu
        self.outp = outp.strip()
    def checkOutput(self, checkStr:str):
        return checkStr == self.outp

class Problem:
    def __init__(self, testCaseList:list, timeLimit:float, memoryLimit:int):
        self.testCaseList = testCaseList
        self.timeLimit = timeLimit
        self.memoryLimit = memoryLimit
    def getInput(self, index:int) -> str:
        return self.testCaseList[index].inpu
    def checkOutput(self, index:int, outp:str):
        return self.testCaseList[index].checkOutput(outp)

class Submission:
    def __init__(self, source:str, compiler:int, problem:Problem, testCaseIndex:int):
        self.source = source
        self.compiler = compiler
        self.problem = problem
        self.testCaseIndex = testCaseIndex
        self.id = None
        self.output = None
    def createSubmission(self):
        if(self.id): return False
        try:
            response = client.submissions.create(
                self.source, self.compiler, self.problem.getInput(self.testCaseIndex),
                time_limit=self.problem.timeLimit, memory_limit=self.problem.memoryLimit)
            self.id = response['id']
            return True
        except SphereEngineException as e:
            print("ERROR", e.code, e)
            return False
    def updateStatus(self):
        if(self.output): return False
        try:
            self.response = client.submissions.get(self.id)
            self.status = self.response['result']['status']['code']
            if self.status > 10:
                programOutput = self.response['result']['streams']['output']
                if(programOutput):
                    self.output = requests.get(programOutput['uri']).content.decode('ascii').strip()
                return True
        except SphereEngineException as e:
            print("ERROR", e.code, e)
            return False
    def submissionOutput(self):
        if(not self.id): return (-2,)
        if(not self.status): return (-1,)
        if(not self.output): return (self.status,)
        return (self.status, self.problem)
 
        
        
            
if __name__ == "__main__":
    # API usage
    source = """
    print(input())
    """
    compiler = COMPILER_PYTHON
    inpu = '2017'

    t = TestCase("2017", "2017")

    p = Problem([t], 1, 1024)

    s = Submission(source, compiler, p, 0)
    s.id = 309333907

    s.updateStatus()

    print(s.output)
    print(t.checkOutput(s.output))