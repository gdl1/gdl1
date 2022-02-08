import os
import sys
sys.path.append("/home/gdl1/gdl")
import psutil
import time

print('test2입니다.')
pid_2 = os.getpid()
pid_2 = str(pid_2)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID2: ',pid_2)
print('\n')

f = open('/home/gdl1/gdl/pid_2.txt','w')
f.write(pid_2)
f.close()

if os.path.isfile('/home/gdl1/gdl/pid_1.txt'):
    f = open('/home/gdl1/gdl/pid_1.txt','r')
    pid_1 = f.readline()
    pid_1 = int(pid_1)
    psutil.Process(pid_1).kill()
    print('프로세스 Kill\n')
    f.close()
    os.remove('/home/gdl1/gdl/pid_1.txt')
    #time.sleep(3)

time.sleep(3)

os.system('python3 /home/gdl1/gdl/test1_1.py')
