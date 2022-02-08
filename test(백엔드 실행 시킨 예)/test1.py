import os
import time

print('test1입니다.')
pid1 = os.getpid()
pid1 = str(pid1)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID1: ',pid1)
print('\n')

f = open('/home/gdl1/gdl/pid.txt','w')
f.write(pid1)
f.close()

os.system('python3 /home/gdl1/gdl/test/module/test2.py')

time.sleep(50)