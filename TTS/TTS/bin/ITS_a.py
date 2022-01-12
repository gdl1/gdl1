import cv2
import numpy as np
import sys
sys.path.append("/home/gdl1/gdl")
sys.path.append("/home/gdl1/gdl/ImageCaptioning")
sys.path.append("/home/gdl1/gdl/TTS")
from ImageCaptioning import caption
import torch
import json
from TTS.bin import *
import string
from TTS.utils.synthesizer import Synthesizer
import os
import ftplib
import playsound
import paramiko

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def Video_capture():
    cap = cv2.VideoCapture(0) #cv2.VideoCapture에 들어가는 숫자는 비디오 객체에 맞게 설정해줘야 함/ 0은 임의로 적은 것
    if (not cap.isOpened()):
        print('Error opening video')

    height, width = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))

    ret, frame = cap.read()
    # 제대로 프레임을 읽으면 ret값이 True, 실패하면 False가 나타남
    # fram에 읽은 프레임이 나옵니다
    if not ret:
        print("프레임을 읽지 못 하였습니다.")
        return 0
    else:
        return frame

def main():
    image_path = "/home/gdl1/gdl/caption_data/street.jpg"
    #img = Video_capture()``
    if image_path==0:
        pass
    model='/home/gdl1/gdl/caption_data/BEST_checkpoint_coco_5_cap_per_img_5_min_word_freq.pth.tar'
    word_map='/home/gdl1/gdl/caption_data/WORDMAP_coco_5_cap_per_img_5_min_word_freq.json'
    beam_size=5

    checkpoint = torch.load(model, map_location=str(device))
    decoder = checkpoint['decoder']
    decoder = decoder.to(device)
    decoder.eval()
    encoder = checkpoint['encoder']
    encoder = encoder.to(device)
    encoder.eval()

    with open(word_map, 'r') as j:
        word_map = json.load(j)
    rev_word_map = {v: k for k, v in word_map.items()}

    seq, _ = caption.caption_image_beam_search(encoder, decoder, image_path, word_map, beam_size)
    words = [rev_word_map[ind] for ind in seq]
    words = words[1:len(words)-1]
    sentence = ""
    for i in words[0:len(words)-1]:
        sentence += i+" "
    sentence += words[len(words)-1]

    # TTS 부분
    model_path = "/home/gdl1/.local/share/tts/tts_models--en--ek1--tacotron2/model_file.pth.tar"
    config_path = "/home/gdl1/.local/share/tts/tts_models--en--ek1--tacotron2/config.json"
    vocoder_path = "/home/gdl1/.local/share/tts/vocoder_models--en--ek1--wavegrad/model_file.pth.tar"
    vocoder_config_path = "/home/gdl1/.local/share/tts/vocoder_models--en--ek1--wavegrad/config.json"
    speakers_file_path =  None
    language_ids_file_path =  None
    encoder_path = None
    encoder_config_path = None

    synthesizer = Synthesizer(
        model_path,
        config_path,
        speakers_file_path,
        language_ids_file_path,
        vocoder_path,
        vocoder_config_path,
        encoder_path,
        encoder_config_path
    )

    print(" > Text: {}".format(sentence))

    out_path = "/home/gdl1/gdl/caption_data"
    wav = synthesizer.tts(sentence)
    file_name =  sentence.replace(" ", "_")[0:20]
    file_name = file_name.translate(
        str.maketrans('', '', string.punctuation.replace('_', ''))) + '.wav'
    out_path = os.path.join(out_path, file_name)
    print(" > Saving output to {}".format(out_path))
    synthesizer.save_wav(wav, out_path)

    # ftp 서버 접속
#    session = ftplib.FTP()
#    session.connect('192.168.123.8')
#    session.login("pi","skdnwjd1")

#    uploadfile = open('/home/gdl1/gdl/caption_data/a_group_of_people_wa.wav','rb')

#    session.encoding='utf-8'
#    session.storbinary('STOR '+'a_group_of_people_wa.wav',uploadfile)

    # 원격 파일 실행
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.123.8',22,'pi','skdnwjd1')

    # ssh로 파일 업로드
    sftp = ssh.open_sftp()
    sftp.put('/home/gdl1/gdl/caption_data/a_group_of_people_wa.wav', '/home/pi/a_group_of_people_wa.wav')

    ssh.exec_command("python3 sound.py")
    # 터미널 창에서 실행하듯이 적으면 됨

#    playsound.playsound('/home/pi/a_group_of_people_wa.wav')

#    uploadfile.close()

#    session.quit()
    print("실행완료")

if __name__ == "__main__":
    main()