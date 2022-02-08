import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

form_class1 = uic.loadUiType("/home/gdl1/SDR.ui")[0]
form_class2 = uic.loadUiType("/home/gdl1/좌표_입력.ui")[0]

class Window2(QMainWindow, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("좌표 입력")
        self.pushButton.clicked.connect(self.input_clicked)

    def input_clicked(self):
        print(self.lineEdit.text())
        print(self.lineEdit_2.text())
        self.close()


class MyWindow(QMainWindow, form_class1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start_clicked)
        self.pushButton_2.clicked.connect(self.driving_clicked)

    def start_clicked(self):
        os.system('python3 /home/gdl1/gdl/TTS/TTS/bin/ITS_a.py')        # 주행 전 안전을 위해 경고를 알리고 ITS 한번 실행

    def driving_clicked(self):
        self.w = Window2()
        self.w.show()



    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()