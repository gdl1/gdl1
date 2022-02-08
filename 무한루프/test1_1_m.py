import os
import sys
sys.path.append("/home/gdl1/gdl")
import psutil
import time

print('test1입니다.')
pid_1 = os.getpid()
pid_1 = str(pid_1)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID1: ',pid_1)
print('\n')

if os.path.isfile('/home/gdl1/gdl/pid_2.txt'):
    f = open('/home/gdl1/gdl/pid_2.txt','r')
    pid_2 = f.readline()
    pid_2 = int(pid_2)
    psutil.Process(pid_2).kill()
    print('프로세스 Kill\n')
    f.close()
    time.sleep(3)

f = open('/home/gdl1/gdl/pid_1.txt','w')
f.write(pid_1)
f.close()

time.sleep(3)

os.system('python3 /home/gdl1/gdl/test2_1.py')

time.sleep(3)
