import argparse
import os

from synthesizer import Synthesizer

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

def main(args):
  synthesizer = Synthesizer()
  if args.t_checkpoint and args.v_checkpoint\
     and args.t_config and args.v_config:
      synthesizer.load(args.t_checkpoint, args.v_checkpoint,
                       args.t_config, args.v_config)
  else:
      t_model_path = os.path.join(PROJECT_PATH,
                                  'models/upc_pau_coqui_speedy_speech.pth.tar')
      v_model_path = os.path.join(PROJECT_PATH,
                                  'models/melgan_onapau_catotron.pt')
      t_config_path = os.path.join(PROJECT_PATH,
                                   'models/config_pau_speedy_speech.json')
      v_config_path = os.path.join(PROJECT_PATH,
                                   'models/config_coqui_vocoder.json')
      synthesizer.load(t_model_path, v_model_path,
                       t_config_path, v_config_path)
  audio = synthesizer.synthesize(args.text)

  with open(args.out, 'wb') as out:
    out.write(audio)

if __name__ == '__main__':
  from wsgiref import simple_server
  parser = argparse.ArgumentParser()
  parser.add_argument('--t_checkpoint', help='Full path to tacotron2 checkpoint')
  parser.add_argument('--v_checkpoint', help='Full path to melgan checkpoint')
  parser.add_argument('--t_config', help='Full path to tts config')
  parser.add_argument('--v_config', help='Full path to vocoder config')
  parser.add_argument('--out', help='Full path to output wav file')
  parser.add_argument('--text', help='Text to be synthesized')
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  args = parser.parse_args()
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#  if not (args.out or args.text):
#    raise ValueError('output file and text needs to be given')

  main(args)
