import tempfile,unittest
from study_store import StudyStore
from game_bank import QUIZ_BANK
from streamlit.testing.v1 import AppTest
class StudyTests(unittest.TestCase):
 def test_encrypted_keys_survive_restart_and_are_private(self):
  with tempfile.TemporaryDirectory() as d:
   store=StudyStore(d);name,cipher=store.unlock('reader','a-long-private-passphrase',True)
   store.save(name,cipher,'provider:Groq',{'key':'private-test-key'})
   self.assertNotIn(b'private-test-key',store.path.read_bytes())
   fresh=StudyStore(d);name,cipher=fresh.unlock('reader','a-long-private-passphrase')
   self.assertEqual(fresh.get(name,cipher,'provider:Groq')['key'],'private-test-key')
   with self.assertRaises(ValueError):fresh.unlock('reader','the-wrong-passphrase')
   other,othercipher=fresh.unlock('another','another-private-passphrase',True)
   self.assertIsNone(fresh.get(other,othercipher,'provider:Groq'))
 def test_scripture_banks_and_refresh(self):
  for book in ['Gita','Narayaneeyam','Bhagavatam']:
   bank=[q for q in QUIZ_BANK if q['book']==book]
   self.assertGreaterEqual(len(bank),25)
   for q in bank:self.assertTrue(q['reference']);self.assertTrue(q['why']);self.assertIn(q['answer'],range(len(q['choices'])))
  app=AppTest.from_file('app.py').run();app.sidebar.radio[0].set_value('Games').run()
  self.assertEqual(len(app.select_slider[0].options),25)
  previous=app.session_state['_game']['items']
  next(b for b in app.button if b.label=='Refresh · different challenges').click().run()
  self.assertFalse(app.exception);self.assertTrue(all(q not in previous for q in app.session_state['_game']['items']))
 def test_reading_shiva_explanation(self):
  app=AppTest.from_file('app.py').run();app.selectbox[0].set_value('shiva').run()
  self.assertFalse(app.exception)
  self.assertTrue(any('Prayaga' in m.value for m in app.markdown))
if __name__=='__main__':unittest.main()
