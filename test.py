from subprocess import Popen, PIPE
from time import sleep, time
import threading
import sys

def runCommandThread(cmd_list:list):
	st = time()
	p = Popen(cmd_list, stdout=PIPE, stderr=PIPE, shell=True)
	stdout = p.stdout.read()
	stderr = p.stderr.read()
	if stdout:
		print("o:",str(stdout))
	if stderr:
		print("e:",str(stderr))
	print("t:", time() - st)
	global commandComplete
	commandComplete = True

def waitThread(t:float):
	sleep(t)
	global timerComplete
	timerComplete = True

def runCommandWithTimout(cmd_list:list, t:float):
	print("l:starting")
	global commandComplete
	global timerComplete
	commandComplete = False
	timerComplete = False
	
	threadCommand = threading.Thread(target=runCommandThread, args=(cmd_list,))
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


for i in sys.argv:
	arr = i.split("=")
	if arr[0] == "f" and len(arr) >= 2:
		f = "python " + str(arr[1])
		print(f)
		runCommandWithTimout(f, timers)
		break

#runCommandWithTimout("python C:\\Users\\young\\Documents\\Code\\CPC\\Runner\\CPCRunner\\runner.py", 6.0)
