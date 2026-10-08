import json,unittest,urllib.error
from pathlib import Path
from streamlit.testing.v1 import AppTest
from knowledge import audit,connect,works,passages
from providers import request,ProviderError,CONFIG
class Response:
 def __init__(self,obj):self.raw=json.dumps(obj).encode() if not isinstance(obj,bytes) else obj
 def __enter__(self):return self
 def __exit__(self,*args):pass
 def read(self):return self.raw
class Tests(unittest.TestCase):
 def test_database(self):
  with connect() as c:
   self.assertEqual(c.execute('pragma integrity_check').fetchone()[0],'ok')
   self.assertEqual(c.execute('select count(*) from passages where length(original)=0 or length(source_url)=0').fetchone()[0],0)
   self.assertEqual(c.execute('select count(*) from passages where work_id not in(select id from works)').fetchone()[0],0)
  self.assertEqual(len(works()),30)
  for w in works():self.assertTrue(passages(w['id']))
  self.assertTrue(any('not the complete' in r['Review'] for r in audit()))
 def test_providers(self):
  for provider in CONFIG:
   obj={'candidates':[{'content':{'parts':[{'text':'A readable answer.'}]}}]} if provider=='Gemini' else {'choices':[{'message':{'content':'A readable answer.'}}]}
   self.assertEqual(request(provider,'test-key',CONFIG[provider][1],[{'role':'user','content':'Question'}],opener=lambda *a,**k:Response(obj)),'A readable answer.')
   with self.assertRaises(ProviderError):request(provider,'test-key',CONFIG[provider][1],[],opener=lambda *a,**k:Response(b'<html>sign in</html>'))
 def test_every_page(self):
  app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run(timeout=20)
  for page in ['Situations','Story garden','Reading room','Learn & chant','Games','Converse','Settings','Coverage & sources']:
   app.sidebar.radio[0].set_value(page).run(timeout=20);self.assertFalse(app.exception,page)
 def test_learning_advances(self):
  app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run();app.sidebar.radio[0].set_value('Learn & chant').run()
  before=app.number_input[0].value
  next(b for b in app.button if b.label=='Practised · learn next').click().run()
  self.assertFalse(app.exception);self.assertEqual(app.number_input[0].value,before+1)
 def test_quiz_feedback_next(self):
  app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run();app.sidebar.radio[0].set_value('Games').run()
  app.radio[0].set_value(app.radio[0].options[0]).run()
  next(b for b in app.button if b.label=='Check answer').click().run()
  self.assertFalse(app.exception)
  next(b for b in app.button if b.label=='Next challenge').click().run()
  self.assertFalse(app.exception);self.assertEqual(app.session_state['_game']['index'],1)
 def test_no_key_keeps_question(self):
  app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run();app.sidebar.radio[0].set_value('Converse').run()
  app.text_area[0].set_value('How can I decide?').run();next(b for b in app.button if b.label=='Send question').click().run()
  self.assertFalse(app.exception);self.assertTrue(app.error);self.assertEqual(app.text_area[0].value,'How can I decide?')
 def test_prepared_answer_needs_no_key(self):
  app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run();app.sidebar.radio[0].set_value('Converse').run()
  app.text_area[0].set_value('What is Narayaneeyam?').run();next(b for b in app.button if b.label=='Send question').click().run()
  self.assertFalse(app.exception);self.assertFalse(app.error);self.assertTrue(app.session_state['history'])
 def test_notes_survive_navigation(self):
  app=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run();app.sidebar.radio[0].set_value('Situations').run()
  next(b for b in app.button if b.key=='need_decisions').click().run()
  area=next(t for t in app.text_input if t.key=='nextstep_decisions');area.set_value('Compare two realistic options').run()
  app.sidebar.radio[0].set_value('Reading room').run();app.sidebar.radio[0].set_value('Situations').run()
  self.assertFalse(app.exception);self.assertEqual(next(t for t in app.text_input if t.key=='nextstep_decisions').value,'Compare two realistic options')
if __name__=='__main__':unittest.main()
