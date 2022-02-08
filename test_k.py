import os
import psutil

if os.path.isfile('/home/gdl1/gdl/pid_1.txt'):
    f = open('/home/gdl1/gdl/pid_1.txt','r')
    pid_1 = f.readline()
    pid_1 = int(pid_1)
    psutil.Process(pid_1).kill()
    print('프로세스 Kill\n')
    f.close()
    os.remove('/home/gdl1/gdl/pid_1.txt')

if os.path.isfile('/home/gdl1/gdl/pid_2.txt'):
    f = open('/home/gdl1/gdl/pid_2.txt','r')
    pid_2 = f.readline()
    pid_2 = int(pid_2)
    psutil.Process(pid_2).kill()
    print('프로세스 Kill\n')
    f.close()
    os.remove('/home/gdl1/gdl/pid_2.txt')