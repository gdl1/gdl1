import os
import time
import psutil
import time

print('test3입니다.')
pid3 = os.getpid()
print('현재 PID3: ',pid3)
print('\n')

if os.path.isfile('/home/gdl1/gdl/pid.txt'):
    f = open('/home/gdl1/gdl/pid.txt','r')
    pid5 = f.readline()
    f.close()    
    print('kill하는 pid = ',pid5)
    pid5 = int(pid5)
    psutil.Process(pid5).kill()
    print('프로세스 Kill\n')

time.sleep(100)
