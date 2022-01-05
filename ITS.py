import cv2
import numpy as np
from ImageCaptioning import caption
from TTS.bin import synthesize
import torch
import json
from TTS.bin import *
import string
from TTS.utils.synthesizer import Synthesizer
import os

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
    img = Video_capture()
    if img==0:
        pass
    model='path/to/BEST_checkpoint_coco_5_cap_per_img_5_min_word_freq.pth.tar'
    word_map='path/to/WORDMAP_coco_5_cap_per_img_5_min_word_freq.json'
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

    seq, alphas = caption.caption_image_beam_search(encoder, decoder, img, word_map, beam_size)

    # TTS 부분
    model_path = None
    config_path = None
    vocoder_path = None
    vocoder_config_path = None
    synthesizer = Synthesizer(model_path, config_path, vocoder_path, vocoder_config_path, use_cuda=False)
    out_path = "folder/to/save/output/"
    wav = synthesize.tts(seq)
    file_name =  seq.replace(" ", "_")[0:20]
    file_name = file_name.translate(
        str.maketrans('', '', string.punctuation.replace('_', ''))) + '.wav'
    out_path = os.path.join(out_path, file_name)
    print(" > Saving output to {}".format(out_path))
    synthesizer.save_wav(wav, out_path)

if __name__ == "__main__":
    main()