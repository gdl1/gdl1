import os
from tkinter.tix import Tree
import paramiko

pid_r = os.getpid()
pid_r = str(pid_r)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID: ',pid_r)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_r.txt','w')
f.write(pid_r)
f.close()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.123.8',22,'pi','skdnwjd1')

ssh.exec_command("roscore&")
ssh.exec_command("roslaunch ydlidar lidar.launch&")
ssh.exec_command("rosrun ydlidar ydlidar_client&")
ssh.exec_command()
# 마지막에 내비 키고 골 보내는 거 적어야 함
# 묶어서 파이썬 파일에 저장자하고 os.getpid로 프로세스 저장하고 kill해도 괜찮을 듯 -> 실제로 만든 게 이거
## kill 할 때 killall ros 이렇게 하면 될 듯(참고: https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=dudwo567890&logNo=130156854673)
# ros 다 안 꺼지고 멈추게 할려면 속도 0 주고

os.remove('/home/gdl1/gdl/caption_data/pid_r.txt.txt')

##while True:
##    a = 1
### while문을 빼고 ros_execute.py를 종료시켰을 때 ros 실행하는 부분들이 종료된다면
### 이 while문을 통해 이 파일이 계속 실행되도록 설정할 것
## -> 안해도 됨