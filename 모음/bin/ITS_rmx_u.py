# 원격 접속 안 하는 코드
import cv2
import sys
sys.path.append("/home/gdl1/gdl")
sys.path.append("/home/gdl1/gdl/ImageCaptioning")
sys.path.append("/home/gdl1/gdl/TTS")
from ImageCaptioning import caption_origin
import torch
import json
from TTS.bin import *
from TTS.utils.synthesizer import Synthesizer
import os
import playsound
from tendo import singleton
import time

me = singleton.SingleInstance() # 중복 실행 방지

pid_u = os.getpid()
pid_u = str(pid_u)      #f.write에 int가 아닌 string이 필요해서 첨가
print('PID_u : ',pid_u)
print('\n')

f = open('/home/gdl1/gdl/caption_data/pid_u.txt','w')
f.write(pid_u)
f.close()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("cuda use or not : ",torch.cuda.is_available())

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
    while True:
        image_path = "/home/gdl1/gdl/caption_data/ski.jpg"
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

        seq, _ = caption_origin.caption_image_beam_search(encoder, decoder, image_path, word_map, beam_size)
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
#        use_cuda = False(넣어줘도 되고 안 넣어줘도 됨/ 왜냐하면 use_cuda를 arg로 안 줬기 때문에 default로 False 들어감)

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
        file_name = 'ITS.wav'
        out_path = os.path.join(out_path, file_name)
        print(" > Saving output to {}".format(out_path))
        synthesizer.save_wav(wav, out_path)
        playsound.playsound(out_path)
        time.sleep()                                    ##### 시간 틈을 얼마로 할 것인지 정해야 함

if __name__ == "__main__":
    main()

#os.remove('/home/gdl1/gdl/caption_data/pid_u.txt')        # def main이 끝나면 이 파일 실행이 끝난 것이므로 pid 기록된 것 삭제
                                                           # 반복적으로 계속 실행되는 것이라 u_e에서 kill하지 않는 한 끝나지 않으니까 없어도 될 듯