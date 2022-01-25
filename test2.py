
from subprocess import PIPE, Popen
p = Popen(["python runner.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE,) 


stdout, stderr = p.communicate("help\n".encode("ascii"))

if stdout:
    print(str(stdout))