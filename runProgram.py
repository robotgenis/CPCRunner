
from fileinput import filename
from subprocess import Popen, PIPE
import os
from time import time
import random

random.seed()

progFolder = os.path.dirname(__file__)

TYPE_PYTHON = "TYPE_PYTHON"
TYPE_JAVA = "TYPE_JAVA"

def saveProgram(fileName:str, prog:list):
    f = open(os.path.join(progFolder, fileName), "x")
    f.writelines(prog)
    f.close()
    print("File Saved: ", fileName)


def runProgram(typ:str, tim:float, prog:str, inps:list):

    runFolder = str(time()).replace(".","-") + "-" + str(random.random())[2:] + "/"
    
    runFolderPath = os.path.join(progFolder, runFolder)
    
    os.mkdir(runFolderPath)

    cmd = ""
    if typ == TYPE_PYTHON:
        fileName = runFolder + "test.py"
        saveProgram(fileName, prog)
        cmd = "python " + fileName
    elif typ == TYPE_JAVA:
        
        arrProg = " ".join(prog).split()
        
        fileName = ""
        
        for i in range(len(arrProg) - 2):
            if arrProg[i] == "public" and arrProg[i+1] == "class":
                fileName = runFolder + arrProg[i+2]
                break
            elif arrProg[i+1] == "class" and len(fileName) == 0:
                fileName = runFolder + arrProg[i+1]
        print(fileName)
        p = Popen("javac " + fileName + ".java", stdout=PIPE, stderr=PIPE, stdin=PIPE)
        p.wait()
        cmd = "java " + fileName

    #Python Exmaple
    # cmd = "python runs/runner.py"
    # inp = "test\n1\n2\n3".encode("ascii")



    runCmd = "python myThreader.py t=" + str(tim) + " \"f=" + cmd + "\""
    p = Popen(runCmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)

    # python test.py t=6.0 "f=python C:\Users\young\Documents\Code\CPC\Runner\CPCRunner\runner.py"
    stdout, stderr = p.communicate("\n".encode("ascii"))

    if stdout:
        print("o:",str(stdout).split("\\r\\n"))
    if stderr:
        print("e:",str(stderr))

runProgram(TYPE_PYTHON, 6.0, "print('hi')", [])