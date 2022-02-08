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
from TTS.utils.synthesizer import Synthesizer
import os
import paramiko
from tendo import singleton
import time
import simpleaudio as sa

me = singleton.SingleInstance() # 중복 실행 방지

pid_its = os.getpid()
pid_its = str(pid_its)      #f.write에 int가 아닌 string이 필요해서 첨가
print('PID_u_e : ',pid_its)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_its.txt','w')
f.write(pid_its)
f.close()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def img_Contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))

    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return final

def main():
    
    while True:
        # 원격 접속
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect('192.168.0.10',22,'pi','skdnwjd1')
        
        # 캡쳐한 이미지 다운로드
        sftp = ssh.open_sftp()        
        
        cap = cv2.VideoCapture('http://192.168.0.10:8091/?action=stream') #cv2.VideoCapture에 홈페이지 주소 적기
        if (not cap.isOpened()):
            print('Error opening video')

        height, width = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))

        ret, frame = cap.read()
        # 제대로 프레임을 읽으면 ret값이 True, 실패하면 False가 나타남
        # fram에 읽은 프레임이 나옵니다
        if not ret:
            print("프레임을 읽지 못 하였습니다.")
        else:
            pass
        
        img = frame
        img = img_Contrast(img)
        ##cap = cv2.VideoCapture()        
        ##if (not cap.isOpened()):
        ##    print('Error opening video')
        ##height, width = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        ##                int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        ##ret, img = cap.read()
        ##if not ret:
        ##    print("프레임을 읽지 못 하였습니다.")
        ##else:
        ##    pass
        ##img = img_Contrast(img)

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

        seq, _ = caption.caption_image_beam_search(encoder, decoder, img, word_map, beam_size)
        words = [rev_word_map[ind] for ind in seq]
        words = words[1:len(words)-1]
        sentence = ""
        for i in words[0:len(words)-1]:
            sentence += i+" "
        sentence += words[len(words)-1]
        sentence = "Calling. " + sentence

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
        file_name =  'ITS'+ '.wav'
        out_path = os.path.join(out_path, file_name)
        print(" > Saving output to {}".format(out_path))
        synthesizer.save_wav(wav, out_path)
        ##wave_obj = sa.WaveObject.from_wave_file('/home/gdl1/gdl/caption_data/ITS.wav')
        ##play_obj = wave_obj.play()
        ##play_obj.wait_done()
        # ssh로 파일 업로드
        sftp.put('/home/gdl1/gdl/caption_data/ITS.wav', '/home/pi/ITS.wav')

        ssh.exec_command("python3 sound.py")
        # 터미널 창에서 실행하듯이 적으면 됨

        print("실행완료")

        ssh.close()

if __name__ == "__main__":
    main()

os.remove('/home/gdl1/gdl/caption_data/pid_its.txt')        # def main이 끝나면 이 파일 실행이 끝난 것이므로 pid 기록된 것 삭제