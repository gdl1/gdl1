import os
import time
import psutil
import time

print('test3입니다.')
pid = os.getpid()
print('현재 PID3: ',pid)
print('\n')

if os.path.isfile('/home/gdl1/gdl/pid.txt'):
    f = open('/home/gdl1/gdl/pid.txt','r')
    pid = f.readline()
    pid = int(pid)
    psutil.Process(pid).kill()
    print('프로세스 Kill\n')
    f.close()
    time.sleep(100)