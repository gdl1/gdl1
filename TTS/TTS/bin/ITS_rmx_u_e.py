# 원격 접속 안 하는 코드
import numpy as np
import sys
sys.path.append("/home/gdl1/gdl")
sys.path.append("/home/gdl1/gdl/ImageCaptioning")
sys.path.append("/home/gdl1/gdl/TTS")
from ImageCaptioning import caption_origin
from TTS.bin import *
from TTS.utils.synthesizer import Synthesizer
import os
import psutil

pid_u_e = os.getpid()
pid_u_e = str(pid_u_e)      #f.write에 int가 아닌 string이 필요해서 첨가
print('PID_u_e : ',pid_u_e)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_u_e.txt','w')
f.write(pid_u_e)
f.close()

while True:
    if os.path.isfile('/home/gdl1/gdl/caption_data/em.txt'):
        f = open('/home/gdl1/gdl/caption_data/em.txt','r')
        val = str(f.readline())
        if val == True:
    #a = os.system()                                                  ##### 응급상황 발생시 받는 것 설정
    #if a == em:
            if os.path.isfile('/home/gdl1/gdl/caption_data/pid_u.txt'):
                f = open('/home/gdl1/gdl/caption_data/pid_u.txt','r')
                pid_u = f.readline()
                pid_u = int(pid_u)
                psutil.Process(pid_u).kill()
                print('프로세스 Kill\n')
                f.close()                                                      # 응급상황시 em / 아닐 시 n_em
                os.remove('/home/gdl1/gdl/caption_data/pid_u.txt')
        break

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/e_s_1_ITS_g.py')
os.remove('/home/gdl1/gdl/caption_data/pid_u_e.txt')        # 응급 상황시 발생되는 파일 실행이 끝났으므로 기록한 pid 삭제