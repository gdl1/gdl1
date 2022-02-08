# 원격 접속 안 하는 코드
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

me = singleton.SingleInstance() # 중복 실행 방지

pid = os.getpid()
pid = str(pid)      #f.write에 int가 아닌 string이 필요해서 첨가
print('현재 PID: ',pid)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid.txt','w')
f.write(pid)
f.close()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("cuda use or not : ",torch.cuda.is_available())

def main():
    ##image_path = "/home/gdl1/gdl/caption_data/ski.jpg"
    #img = Video_capture()``
    ##if image_path==0:
    ##    pass
    # 원격 접속
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('222.100.65.196',5555,'pi','skdnwjd1')

    ssh.exec_command("python3 /home/pi/gdl/sound_pre.py")
    
    ### 묵음 처리를 위한 설정
    ##a = 0
    
    while True:
        ##img = cv2.imread('/home/gdl1/gdl/caption_data/ski.jpg')
        img = ssh.exec_command("python3 /home/pi/gdl/VideoCapture.py")
        print('img = ',img)
        
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

    ##seq, _ = caption_origin.caption_image_beam_search(encoder, decoder, image_path, word_map, beam_size)
        seq, _ = caption.caption_image_beam_search(encoder, decoder, img, word_map, beam_size)
        words = [rev_word_map[ind] for ind in seq]
        words = words[1:len(words)-1]
        sentence = ""
        for i in words[0:len(words)-1]:
            sentence += i+" "
        sentence += words[len(words)-1]
        # TTS 부분
        model_path = "/home/gdl1/tts/tts_models--en--ek1--tacotron2/model_file.pth.tar"
        config_path = "/home/gdl1/tts/tts_models--en--ek1--tacotron2/config.json"
        vocoder_path = "/home/gdl1/tts/vocoder_models--en--ek1--wavegrad/model_file.pth.tar"
        vocoder_config_path = "/home/gdl1/tts/vocoder_models--en--ek1--wavegrad/config.json"
        speakers_file_path =  None
        language_ids_file_path =  None
        encoder_path = None
        encoder_config_path = None
    #    use_cuda = False(넣어줘도 되고 안 넣어줘도 됨/ 왜냐하면 use_cuda를 arg로 안 줬기 때문에 default로 False 들어감)

        synthesizer = Synthesizer(
            model_path,
            config_path,
            speakers_file_path,
            language_ids_file_path,
            vocoder_path,
            vocoder_config_path,
            encoder_path,
            encoder_config_path,
            use_cuda = True
            )

        print(" > Text: {}".format(sentence))
    
        out_path = "/home/gdl1/gdl/caption_data"
        wav = synthesizer.tts(sentence)
        file_name = 'ITS.wav'
        out_path = os.path.join(out_path, file_name)
        print(" > Saving output to {}".format(out_path))
        synthesizer.save_wav(wav, out_path)
        sftp = ssh.open_sftp()
        sftp.put('/home/gdl1/gdl/caption_data/ITS.wav', '/home/pi/gdl/caption_data/ITS.wav')
        ssh.exec_command("python3 /home/pi/gdl/sound.py")
    ssh.close()

if __name__ == "__main__":
    main()
        
os.remove('/home/gdl1/gdl/caption_data/pid.txt')