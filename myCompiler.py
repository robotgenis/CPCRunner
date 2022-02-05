
import requests
import compilerConstants
import json

clientId = "8d4f846be4e1d90c42a9dd64fc544cd"
clientSecret = "d9e2b9a4474c5eb499106490a9c2b52641992066385dec916ea4c8d0c186b997"
url = "https://api.jdoodle.com/v1/execute"


class TestCase:
    def __init__(self, inpu: str, outp: str):
        self.input = inpu
        self.output = outp.strip()

    def checkOutput(self, checkStr: str):
        return checkStr.strip() == self.output


class Problem:
    def __init__(self, testCast: TestCase, timeLimit: float, memoryLimit: int):
        self.testCase = testCast
        self.timeLimit = timeLimit
        self.memoryLimit = memoryLimit


class Submission:
    def __init__(self, source: str, compiler: str, problem: Problem):
        self.source = source
        self.compiler = compiler
        self.problem = problem
        self.output = None
        self.results = None

    def createSubmission(self):
        if not(self.compiler in compilerConstants.COMPILERS):
            print("Compiler Doesn't Exist")
            return
        data = {
            "clientId":  clientId,
            "clientSecret": clientSecret,
            "script": self.source,
            "language": self.compiler,
            "versionIndex": str(compilerConstants.VERSIONS[self.compiler]),
            "stdin": self.problem.testCase.input,
        }
        headers = {'Content-type': 'application/json'}
        print("Running Submission", data)

        content = requests.post(url, data=json.dumps(data), headers=headers).content
        # content = b'{"output":"2\\n","statusCode":200,"memory":"8152","cpuTime":"0.00"}'

        self.output = json.loads(content.decode('ascii'))
        self.checkSubmission()
        print("Conent", content)
        print("Output", self.output)
        print("Results", self.results)

    def checkSubmission(self):
        if not self.output:
            self.results = {'statusCode': compilerConstants.STATUS_NOT_COMPLETE}
            return self.results
        self.results = {'statusCode': self.output['statusCode']}
        if self.output['statusCode'] != 200:
            return
        if float(self.output['cpuTime']) > self.problem.timeLimit:
            self.results['statusCode'] = compilerConstants.STATUS_TIME_LIMIT_EXCEDED
            return
        if int(self.output['memory']) > self.problem.memoryLimit:
            self.results['statusCode'] = compilerConstants.STATUS_MEMORY_LIMIT_EXCEDED
            return
        if self.problem.testCase.checkOutput(self.output['output']):
            self.results['statusCode'] = compilerConstants.STATUS_ACCEPTED
            return
        self.results['statusCode'] = compilerConstants.STATUS_WRONG_ANSWER
        return


def problemFromDatebase(problem):
    tc = TestCase(problem['testCase']['input'], problem['testCase']['output'])

    return Problem(tc, problem['timeLimit'], problem['memoryLimit'])


if __name__ == "__main__":
    # API usage

    tc = TestCase("1 1", "2")

    p = Problem(tc, 1, 1000000)

    src = """
print(sum(list(map(int,input().split()))))
"""

    s = Submission(src, compilerConstants.COMPILER_PYTHON3, p)

    s.createSubmission()
