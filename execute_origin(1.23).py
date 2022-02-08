import os
import playsound

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS.py')               # 시각장애인을 위해 시작 전 ITS 한번 실행
os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ros_execute.py&')      # ros 실행하는 파일
                                                                     #(이 파일안에 실행하는 것 적어야 함/ip와 비밀번호 저장한 파일 하나 만들어서 import해도 좋을 듯)
os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_rmx_u.py&')        # ITS를 반복적으로 실행
# 5, 7 묶어주는 게 좋을 듯

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/key.py&')              ### esc키 누르면 종료되게 하는 코드 실행(작성해야 함)

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/e_s.py')               # 응급상황 발생되는 지 감지할 수 있는 코드
                                                                     # 감지가 되면 응급상황임을 알리고 종료됨
                                                                     # 응급상황 발생시 실행시키는 코드(ITS_rmx_u_e.py도 넣음)

os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ros_execute.py&')      # ros 실행하는 파일
                                                                     #(이 파일안에 실행하는 것 적어야 함/ip와 비밀번호 저장한 파일 하나 만들어서 import해도 좋을 듯)
os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_rmx_u.py&')

# 응급상황이 여러번 발생할 수 있으므로 11-20 묶어서 반복실행되도록 해야함
# while 다시 실행한다면 프로세스가 누적되지 않게 while 전 프로세스 kill하고 다시하도록 해야함
# 키 입력을 받아서 끝낼 수 있도록 하는 것도 만들어야 함