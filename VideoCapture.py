import cv2

def Video_capture():
    cap = cv2.VideoCapture('192.168.0.7:8091/?action=stream') #cv2.VideoCapture에 들어가는 숫자는 비디오 객체에 맞게 설정해줘야 함/ 0은 임의로 적은 것
    if (not cap.isOpened()):
        print('Error opening video')

    ret, frame = cap.read()
    # 제대로 프레임을 읽으면 ret값이 True, 실패하면 False가 나타남
    # fram에 읽은 프레임이 나옵니다
    if not ret:
        print("프레임을 읽지 못 하였습니다.")
        return 0
    else:
        return frame