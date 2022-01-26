
from fileinput import filename
from re import L
from subprocess import Popen, PIPE
import os
from time import time
import random
import shutil

random.seed()

progFolder = os.path.dirname(__file__)

TYPE_PYTHON = "TYPE_PYTHON"
TYPE_JAVA = "TYPE_JAVA"
TYPE_CPP = "TYPE_CPP"

OUTPUT_ERROR = "OUTPUT_ERROR"
OUTPUT_TIMEOUT = "OUTPUT_TIMEOUT"
OUTPUT_SUCCESS = "OUTPUT_SUCCESS"

def saveProgram(fileName:str, prog:list):
    f = open(os.path.join(progFolder, fileName), "x")
    f.writelines(prog)
    f.close()
    print("File Saved: ", fileName)


def runProgram(typ:str, tim:float, prog:str, inps:list):

    runFolder = "F" + str(time()).replace(".","_") + "_" + str(random.random())[2:] + "\\"
    
    runFolderPath = os.path.join(progFolder, runFolder)
    
    os.mkdir(runFolderPath)

    cmd = ""
    if typ == TYPE_PYTHON:
        fileName = "test.py"
        saveProgram(runFolder + fileName, prog)
        cmd = "python " + fileName
    elif typ == TYPE_JAVA:
        arrProg = prog.split()
        fileName = ""
        for i in range(len(arrProg) - 2):
            if arrProg[i] == "public" and arrProg[i+1] == "class":
                fileName = arrProg[i+2].split("{")[0]
                break
            elif arrProg[i+1] == "class" and len(fileName) == 0:
                fileName = arrProg[i+1].split("{")[0]
        saveProgram(runFolder + fileName + ".java", prog)
        p = Popen("javac " + runFolder + fileName + ".java", stdout=PIPE, stderr=PIPE, stdin=PIPE)
        p.wait()
        cmd = "java " + fileName
    elif typ == TYPE_CPP:
        fileName = "test.cpp"
        saveProgram(runFolder + fileName, prog)
        p = Popen("g++ -o ./" + runFolder + "test.exe " + runFolder + fileName, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        p.wait()
        cmd = ".\\test.exe"
        
        

    #Python Exmaple
    # cmd = "python runs/runner.py"
    # inp = "test\n1\n2\n3".encode("ascii")

    testRuns = []

    for i in inps:
        runCmd = "python myThreader.py t=" + str(tim) + " \"c=" + cmd + "\" f=" + runFolderPath + ""
        p = Popen(runCmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)

        # python test.py t=6.0 "f=python C:\Users\young\Documents\Code\CPC\Runner\CPCRunner\runner.py"
        stdout, stderr = p.communicate(i.encode("ascii"))

        if stdout:
            out = stdout.decode('ascii').split("\r\n")
            
            output = ""
            timer = 0.0
            error = ""
            for i in out:
                if len(i) > 0 and i[0] == "t":
                    timer = float(i[2:])
                elif len(i) > 0 and i[0] == "o":
                    output = eval(i[2:])
                elif len(i) > 0 and i[0] == "e":
                    error = i[2:]
            testRuns.append((i,timer,output, error))

        if stderr:
            print("e:",str(stderr))
            return (OUTPUT_ERROR, str(stderr))
    print(testRuns)       
        
    shutil.rmtree(runFolderPath)

runProgram(TYPE_PYTHON, 6.0, """
print('[\\n',input(),'\\n]')
""", ["a", "hi there", "your mom"])
# runProgram(TYPE_JAVA,6.0, """public class Hello{
# 	public static void main(String[] args){
# 		System.out.println("hi");
# 	}
# }""", [])
# runProgram(TYPE_CPP, 6.0, """
# #include <iostream>

# using namespace std;
# int main() {
#     cout << "Hello World!";
#     return 0;
# }             
# """, [])