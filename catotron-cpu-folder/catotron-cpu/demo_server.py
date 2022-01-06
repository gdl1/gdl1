import argparse
import falcon
import os
from synthesizer import Synthesizer

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_BODY = os.path.join(PROJECT_PATH, 'templates/demo.html')
COQUI_PAU = './models/upc_pau_coqui_speedy_speech.pth.tar'
COQUI_PAU_CONF = './models/config_pau_speedy_speech.json'
MELGAN_MODEL = './models/upc_pau_tacotron2.pt'
MELGAN_CONF = './models/config_coqui_vocoder.json'

class UIResource:
  def on_get(self, req, res):
    res.content_type = 'text/html'
    with open(HTML_BODY, 'r') as html_file:
        res.body = html_file.read()

class SynthesisResource:
  def on_get(self, req, res):
    max_chars = 500
    if not req.params.get('text'):
      raise falcon.HTTPBadRequest()
    if len(req.params.get('text')) > max_chars:
      raise falcon.HTTPBadRequest('String too long',
                                  'String length shorter'\
                                  ' than %i is accepted.'%max_chars)
    res.data = synthesizer.synthesize(req.params.get('text'))
    res.content_type = 'audio/wav'

synthesizer = Synthesizer()
api = falcon.API()
api.add_route('/synthesize', SynthesisResource())
api.add_route('/', UIResource())

if __name__ == '__main__':
  from wsgiref import simple_server
  parser = argparse.ArgumentParser()
  parser.add_argument('--t_checkpoint', help='Full path to tts checkpoint')
  parser.add_argument('--v_checkpoint', help='Full path to melgan checkpoint')
  parser.add_argument('--t_config', help='Full path to tts config')
  parser.add_argument('--v_config', help='Full path to vocoder config')
  parser.add_argument('--port', type=int, default=8000)
  parser.add_argument('--hparams', default='',
    help='Hyperparameter overrides as a comma-separated list of name=value pairs')
  args = parser.parse_args()
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
  if args.t_checkpoint and args.v_checkpoint and not args.t_config:
      print('No tts config given, assuming nvidia tacotron2')
      synthesizer.load(args.t_checkpoint, args.v_checkpoint)
  elif args.t_checkpoint and args.v_checkpoint and args.t_config and args.v_config:
      print('Loading custom coqui tts')
      synthesizer.load(args.t_checkpoint, args.v_checkpoint,
                       args.t_config, args.v_config)
  else:
      print('Loading default coqui tts models')
      t_model_path = os.path.join(PROJECT_PATH,
                                  'models/upc_pau_coqui_speedy_speech.pth.tar')
      t_config_path = os.path.join(PROJECT_PATH,
                                  'models/config_pau_speedy_speech.json')
      v_model_path = os.path.join(PROJECT_PATH,
                                  'models/melgan_onapau_catotron.pt')
      v_config_path = os.path.join(PROJECT_PATH,
                                   'models/config_coqui_vocoder.json')
      synthesizer.load(t_model_path, v_model_path,
                       t_config_path, v_config_path)
  print('Serving on port %d' % args.port)
  simple_server.make_server('0.0.0.0', args.port, api).serve_forever()
else:
  synthesizer.load(COQUI_PAU, MELGAN_MODEL, COQUI_PAU_CONF, MELGAN_CONF)
