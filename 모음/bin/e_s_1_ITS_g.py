import playsound
import os
import psutil

pid_e_1_g = os.getpid()
pid_e_1_g = str(pid_e_1_g)      #f.write에 int가 아닌 string이 필요해서 첨가
print('PID_e_1_g : ',pid_e_1_g)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_e_1_g.txt','w')
f.write(pid_e_1_g)
f.close()

playsound.playsound('/home/gdl1/gdl/caption_data/emergency.wav')     # 'EMERGENCY!'와 같이 응급상황을 알리는 파일 재생

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS.py')               # 한번 ITS 실행
os.system('&')                                                       ##### goal 실행시키는 명령어든 차 움직이게 하는 명령어 넣기

f = open('/home/gdl1/gdl/caption_data/pid_ITS_u_a_e','r')
pid_ITS_u_a_e = f.readline()
pid_ITS_u_a_e = int(pid_ITS_u_a_e)
psutil.Process(pid_ITS_u_a_e).kill()
print('프로세스 Kill\n')
f.close()
os.remove('/home/gdl1/gdl/caption_data/pid_ITS_u_a_e.txt')          # ITS_rms_u_and_e.py 재실행 전 kill함

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_rms_u_and_e.py&')
os.remove('/home/gdl1/gdl/caption_data/pid_e_1_g.txt')

### 오류 발생하면 여기서 먼저 ITS_rms_u_and_e.py를 kill 해주고 다시 ITS_rms_u_and_e.py 실행