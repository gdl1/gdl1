import os
import sys
sys.path.append("/home/gdl1/gdl")
import psutil
import time

if os.path.isfile('/home/gdl1/gdl/pid_2.txt'):
    f = open('/home/gdl1/gdl/pid_2.txt','r')
    pid_2 = f.readline()
    pid_2 = int(pid_2)
    psutil.Process(pid_2).kill()
    print('프로세스 Kill\n')
    f.close()
    time.sleep(3)

#os.remove('/home/gdl1/gdl/pid_2.txt')

print('test2입니다.')
pid_2 = os.getpid()
pid_2 = str(pid_2)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID2: ',pid_2)
print('\n')

f = open('/home/gdl1/gdl/pid_2.txt','w')
f.write(pid_2)
f.close()

time.sleep(3)

os.system('python3 /home/gdl1/gdl/test1_1_c.py')

time.sleep(3)
