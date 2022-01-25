from subprocess import Popen, PIPE


p = Popen("python test.py t=6.0 f=C:\\Users\\young\\Documents\\Code\\CPC\\Runner\\CPCRunner\\runner.py", stdout=PIPE, stderr=PIPE, stdin=PIPE)

inp = "test\n".encode("ascii")

stdout, stderr = p.communicate(inp)

if stdout:
    print("o:",str(stdout))
if stderr:
    print("e:",str(stderr))