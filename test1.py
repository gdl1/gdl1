import os
import sys
sys.path.append("/home/gdl1/gdl")
import time

print('test1입니다.')
pid = os.getpid()
pid = str(pid)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID1: ',pid)
print('\n')

f = open('/home/gdl1/gdl/pid.txt','w')
f.write(pid)

import test2
test2()

time.sleep(100)
f.close()