import argparse
import falcon
import os
from synthesizer import Synthesizer

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
#HTML_BODY = os.path.join(PROJECT_PATH, 'templates/demo.html')
HTML_BODY = os.path.join(PROJECT_PATH, 'info/index.html')
HTML_ABOUT = os.path.join(PROJECT_PATH, 'info/qui-som/index.html')
HTML_CONTACT = os.path.join(PROJECT_PATH, 'info/contacte/index.html')
HTML_LEGAL = os.path.join(PROJECT_PATH, 'info/avis-legal/index.html')
HTML_PRIVACY = os.path.join(PROJECT_PATH, 'info/politica-de-privacitat/index.html')
SITE_PATH = os.path.join(PROJECT_PATH, 'info')

class UIResource:
  def __init__(self, filename):
    self.filename = filename
  def on_get(self, req, res):
    res.content_type = 'text/html'
    with open(self.filename, 'r', encoding='utf-8') as html_file:
        res.body = html_file.read()

class SynthesisResource:
  def on_get(self, req, res):
    if not req.params.get('text'):
      raise falcon.HTTPBadRequest()
    if len(req.params.get('text')) > 150:
      raise falcon.HTTPBadRequest('String too long',
                                  'String length shorter than 150 is accepted.')
    res.data = synthesizer.synthesize(req.params.get('text'))
    res.content_type = 'audio/wav'

synthesizer = Synthesizer()
# TODO load via config
t_model_path = os.path.join(PROJECT_PATH, 'models/upc_pau_tacotron2.pt')
v_model_path = os.path.join(PROJECT_PATH, 'models/melgan_onapau_catotron.pt')
synthesizer.load(t_model_path, v_model_path)

app = falcon.API()
app.add_route('/synthesize', SynthesisResource())
app.add_route('/', UIResource(HTML_BODY))
app.add_route('/info/', UIResource(HTML_BODY))
app.add_route('/info/contacte/', UIResource(HTML_CONTACT))
app.add_route('/info/qui-som/', UIResource(HTML_ABOUT))
app.add_route('/info/avis-legal/', UIResource(HTML_LEGAL))
app.add_route('/info/politica-de-privacitat/', UIResource(HTML_PRIVACY))

app.add_static_route('/info',SITE_PATH)

if __name__ == '__main__':
    from wsgiref import simple_server
    port = 9000
    print('Serving on port %d' % port)
    simple_server.make_server('0.0.0.0', port, app).serve_forever()
