import os

pid_ITS_u_a_e = os.getpid()
pid_ITS_u_a_e = str(pid_ITS_u_a_e)      #f.write에 int가 아닌 string이 필요해서 첨가
print('PID_its_u_a_e : ',pid_ITS_u_a_e)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_ITS_u_a_e.txt','w')
f.write(pid_ITS_u_a_e)
f.close()

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_rmx_u.py&')
os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_rmx_u_e.py')
os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/e_s_1_ITS_g.py')