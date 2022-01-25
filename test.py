from subprocess import Popen, PIPE
from time import sleep, time
import threading

def runCommandThread(cmd_list:list):
	p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
	stdout = p.stdout.read()
	stderr = p.stderr.read()
	if stdout:
		print(stdout)
	if stderr:
		print(stderr)


def waitThread(t:float):
    sleep(t)

def runCommandWithTimout(cmd_list:list, t:float):
	threadCommand = threading.Thread(target=runCommandThread, args=(cmd_list,))
	threadCommand.daemon = True
	threadTimer = threading.Thread(target=waitThread, args=(timers,))

	threadCommand.start()
	threadTimer.start()

	threadTimer.join()
	if(threadCommand.is_alive()):
		print("Out of time")

	print("Done")


cmd_list = ['python runner.py']
timers = 6.0

runCommandWithTimout(cmd_list, timers)