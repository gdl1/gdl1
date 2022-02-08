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

me = singleton.SingleInstance() # 중복 실행 방지

pid_its = os.getpid()
pid_its = str(pid_its)      #f.write에 int가 아닌 string이 필요해서 첨가
print('PID_u_e : ',pid_its)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_its.txt','w')
f.write(pid_its)
f.close()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def main():

    # 원격 접속
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.0.7',22,'pi','skdnwjd1')

    ssh.exec_command("python3 Video_Capture.py")

    # 캡쳐한 이미지를 저장하는 데 시간이 걸려서 딜레이
    time.sleep(5)

    # 캡쳐한 이미지 다운로드
    sftp = ssh.open_sftp()
    sftp.get('/home/pi/VC.png','/home/gdl1/gdl/caption_data/VC.png')

    img = cv2.imread('/home/gdl1/gdl/caption_data/VC.png')
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

    # ssh로 파일 업로드
    sftp.put('/home/gdl1/gdl/caption_data/ITS.wav', '/home/pi/ITS.wav')

    ssh.exec_command("python3 sound.py")
    # 터미널 창에서 실행하듯이 적으면 됨

    print("실행완료")

if __name__ == "__main__":
    main()

os.remove('/home/gdl1/gdl/caption_data/pid_its.txt')        # def main이 끝나면 이 파일 실행이 끝난 것이므로 pid 기록된 것 삭제