from subprocess import Popen, PIPE
from time import sleep, time
import threading
import sys

def runCommandThread(cmd_list:list, folder:str):
	p = Popen(cmd_list, stdout=PIPE, stderr=PIPE, stdin=sys.stdin, shell=True, cwd=folder) #
	st = time()
	stdout = p.stdout.read()
	stderr = p.stderr.read()
	if stdout:
		print("t:" +  str(time() - st))
		print("o:" + str(stdout.decode('ascii').split("\r\n")))
	if stderr:
		print("e:" + str(stderr))
	global commandComplete
	commandComplete = True

def waitThread(t:float):
	sleep(t)
	global timerComplete
	timerComplete = True

def runCommandWithTimout(cmd_list:list, t:float, folder:str):
	print("l:starting")
	global commandComplete
	global timerComplete
	commandComplete = False
	timerComplete = False
	
	threadCommand = threading.Thread(target=runCommandThread, args=(cmd_list, folder))
	threadCommand.daemon = True
	threadTimer = threading.Thread(target=waitThread, args=(t,))
	threadTimer.daemon = True

	threadCommand.start()
	threadTimer.start()

	while(not timerComplete and not commandComplete): pass
	
	if(not commandComplete):
		print("e:Out of time")

	print("l:Done")


timers = 1.0

for i in sys.argv:
	arr = i.split("=")
	if arr[0] == "t" and len(arr) >= 2:
		timers = float(arr[1])
		break

folder = ""
for i in sys.argv:
	arr = i.split("=")
	if arr[0] == "f" and len(arr) >= 2:
		folder = str(arr[1])
		break

for i in sys.argv:
	arr = i.split("=")
	if arr[0] == "c" and len(arr) >= 2:
		f = str(arr[1])
		runCommandWithTimout(f, timers, folder)
		break

#runCommandWithTimout("python C:\\Users\\young\\Documents\\Code\\CPC\\Runner\\CPCRunner\\runner.py", 6.0)
