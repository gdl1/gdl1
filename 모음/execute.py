import os
import cv2
import psutil

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS.py')               # 시각장애인을 위해 시작 전 ITS 한번 실행
os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ros_execute.py&')      # ros 실행하는 파일
                                                                     #(이 파일안에 실행하는 것 적어야 함/ip와 비밀번호 저장한 파일 하나 만들어서 import해도 좋을 듯)

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_rms_u_and_e.py&')

while True:
    key = cv2.waitKeyEx(30)
    if key == ___:                                                     ### esc키 값 넣기
        if os.path.isfile('/home/gdl1/gdl/caption_data/pid_its.txt'):
            f = open('/home/gdl1/gdl/caption_data/pid_its.txt','r')
            pid_its = f.readline()
            pid_its = int(pid_its)
            psutil.Process(pid_its).kill()
            print('프로세스 Kill\n')
            f.close()
            os.remove('/home/gdl1/gdl/caption_data/pid_its.txt')
        elif os.path.isfile('/home/gdl1/gdl/caption_data/pid_u.txt'):
            f = open('/home/gdl1/gdl/caption_data/pid_u.txt','r')
            pid_u = f.readline()
            pid_u = int(pid_u)
            psutil.Process(pid_u).kill()
            print('프로세스 Kill\n')
            f.close()
            os.remove('/home/gdl1/gdl/caption_data/pid_u.txt')
        elif os.path.isfile('/home/gdl1/gdl/caption_data/pid_u_e.txt'):
            f = open('/home/gdl1/gdl/caption_data/pid_u_e.txt','r')
            pid_u_e = f.readline()
            pid_u_e = int(pid_u_e)
            psutil.Process(pid_u_e).kill()
            print('프로세스 Kill\n')
            f.close()
            os.remove('/home/gdl1/gdl/caption_data/pid_u_e.txt')
        elif os.path.isfile('/home/gdl1/gdl/caption_data/pid_e_1_g.txt'):
            f = open('/home/gdl1/gdl/caption_data/pid_e_1_g.txt','r')
            pid_e_1_g = f.readline()
            pid_e_1_g = int(pid_e_1_g)
            psutil.Process(pid_e_1_g).kill()
            print('프로세스 Kill\n')
            f.close()
            os.remove('/home/gdl1/gdl/caption_data/pid_e_1_g.txt')
        elif os.path.isfile('/home/gdl1/gdl/caption_data/pid_ITS_u_a_e.txt'):
            f = open('/home/gdl1/gdl/caption_data/pid_ITS_u_a_e.txt','r')
            pid_ITS_u_a_e = f.readline()
            pid_ITS_u_a_e = int(pid_ITS_u_a_e)
            psutil.Process(pid_ITS_u_a_e).kill()
            print('프로세스 Kill\n')
            f.close()
            os.remove('/home/gdl1/gdl/caption_data/pid_ITS_u_a_e.txt')
        else:
            os.system('rosnode kill -a')
            os.system('killall ros')                                   ###39행이나 40행 중 맞는 거 하나만 하기
        break

# 응급상황이 여러번 발생할 수 있으므로 11-20 묶어서 반복실행되도록 해야함
# while 다시 실행한다면 프로세스가 누적되지 않게 while 전 프로세스 kill하고 다시하도록 해야함
# 키 입력을 받아서 끝낼 수 있도록 하는 것도 만들어야 함