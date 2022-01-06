import os
import io
import re
import torch
import scipy
import numpy as np
import pysbd

from hparams_synth import create_hparams
from text import text_to_sequence
from model import Tacotron2

from TTS.tts.utils.synthesis import synthesis, trim_silence
from TTS.config import load_config
from TTS.tts.models import setup_model as setup_tts_model
from TTS.utils.audio import AudioProcessor

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

SEG = pysbd.Segmenter(language="en", clean=True)

class Synthesizer:
  def load(self, t_checkpoint_path, v_checkpoint_path,
           t_config_path=None, v_config_path=None, model_name='tacotron'):
    if t_checkpoint_path.endswith('.pt'):
        self.model_name = 'nvidia'
        print('Constructing model: %s' % self.model_name)

        # set-up params
        hparams = create_hparams()

        # load model from checkpoint
        self.model = Tacotron2(hparams)
        self.model.load_state_dict(torch.load(t_checkpoint_path,
                                              map_location='cpu')['state_dict'])
        _ = self.model.eval()
    else: # elif t_checkpoint_path.endswith('.pth.tar'):
        self.model_name = 'coqui'
        print('Constructing model: %s' % self.model_name)

        # load tts config and audio processor
        self.tts_config = load_config(t_config_path)
        self.tts_model = setup_tts_model(config=self.tts_config)
        self.tts_model.load_checkpoint(self.tts_config,
                                       t_checkpoint_path, eval=True)
        self.ap = AudioProcessor(verbose=False, **self.tts_config.audio)

        # load vocoder config and audio processor
        vocoder_config = load_config(v_config_path)
        self.vocoder_ap = AudioProcessor(verbose=False, **vocoder_config.audio)

    # Load neurips MelGAN for mel2audio synthesis
    self.vocoder = torch.hub.load('descriptinc/melgan-neurips', 'load_melgan')
    melgan_ckpt = torch.load(v_checkpoint_path, map_location='cpu')
    self.vocoder.mel2wav.load_state_dict(melgan_ckpt)


  def synthesize(self, response_text):
    # pre cleaning
    text = self.pre_clean(response_text)

    if self.model_name == 'nvidia':
        # TODO choose language?
        cleaner = ['catalan_cleaners']

        # Prepare text input
        sequence = np.array(text_to_sequence(text, cleaner))[None, :]
        sequence = torch.from_numpy(sequence).to(device='cpu', dtype=torch.int64)

        # TODO run within the queue
        # decode text input
        mel_outputs, mel_outputs_postnet, _, alignments = self.model.inference(sequence)

        # TODO run within the queue
        # Synthesize using neurips Melgan
        with torch.no_grad():
            audio = self.vocoder.inverse(mel_outputs_postnet.float())
        audio_numpy = audio[0].data.cpu().numpy()

        # normalize and convert from float32 to int16 pcm
        audio_numpy /= np.max(np.abs(audio_numpy))
        audio_numpy *= 32768*0.99
        waveform = audio_numpy.astype(np.int16)
    elif self.model_name == 'coqui':
        wavs = []
        sens = self.split_into_sentences(text)
        for sen in sens:
            outputs = synthesis(model=self.tts_model,
                                text=text,
                                CONFIG=self.tts_config,
                                use_cuda=False,
                                ap=self.ap,
                                speaker_id=None,
                                style_wav=None,
                                enable_eos_bos_chars=self.tts_config.enable_eos_bos_chars,
                                use_griffin_lim=False,
                                d_vector=None)

            # extract and normalize the spectogram
            mel_postnet_spec = outputs["outputs"]["model_outputs"][0].detach().cpu().numpy()
            mel_postnet_spec = self.ap.denormalize(mel_postnet_spec.T).T
            vocoder_input = self.vocoder_ap.normalize(mel_postnet_spec.T)
            vocoder_input = torch.tensor(vocoder_input).unsqueeze(0)

            # Synthesize using neurips Melgan
            audio = self.vocoder.inverse(vocoder_input.to('cpu'))
            audio_numpy = audio[0].data.cpu().numpy()
            audio_numpy /= np.max(np.abs(audio_numpy))
            audio_numpy *= 32768*0.99
            waveform = list(audio_numpy.astype(np.int16).squeeze())
            wavs += waveform

        waveform = audio_numpy.astype(np.int16).squeeze()
    else:
        raise ValueError('% unknown model name for synthesis'%self.model_name)

    # out
    out = io.BytesIO()

    # save
    scipy.io.wavfile.write(out, 22050, waveform)

    return out.getvalue()

  def pre_clean(self, response_text):
    if not re.search("[.?!:,;][ ]*$", response_text):
      return '%s. .'%response_text
    else:
      return '%s.'%response_text

  @staticmethod
  def split_into_sentences(text):
    return SEG.segment(text)
