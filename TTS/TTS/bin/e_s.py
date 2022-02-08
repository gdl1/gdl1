import os
import playsound

pid_e_s = os.getpid()
pid_e_s = str(pid_e_s)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID: ',pid_e_s)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_e_s.txt','w')
f.write(pid_e_s)
f.close()

while True:
    a = os.system()                                                  # 응급상황 발생시 받는 것 설정
    if a == em:                                                      # 응급상황시 em/ 아닐 시 n_em
       break
playsound.playsound()                                                # 'EMERGENCY!'와 같이 응급상황을 알리는 파일 재생

os.remove('/home/gdl1/gdl/caption_data/pid_e_s.txt')                 # 응급상황이 종료되었으므로 기록된 pid 삭제  


os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_rmx_u_e.py&')