import subprocess
import os

processes = []
for file in files_output:
    f = os.tmpfile()
    p = subprocess.Popen(['md5sum',file],stdout=f)
    processes.append((p, f))

for p, f in processes:
    p.wait()
    f.seek(0)
    logfile.write(f.read())
    f.close()