import os
import time

a = False

if a == False:
    os.system('python3 /home/gdl1/gdl/test/module/test1.py&')

time.sleep(5)

a = True

if a == True:
    os.system('python3 /home/gdl1/gdl/test/module/test3.py')

time.sleep(50)