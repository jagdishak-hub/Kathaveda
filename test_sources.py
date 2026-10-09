import json,unittest
from knowledge import passages
from friendly_ui import STORIES
from streamlit.testing.v1 import AppTest
class SourceTests(unittest.TestCase):
 def test_paired_gita_edition_and_numbering(self):
  readings=passages('gita-besant')
  self.assertEqual(len(readings),701)
  self.assertEqual(len({r['chapter'] for r in readings}),18)
  self.assertEqual(len([r for r in readings if r['chapter']==13]),35)
  self.assertTrue(all(json.loads(r['metadata'])['meaning'] for r in readings))
 def test_historical_epic_books_and_purana(self):
  self.assertEqual({r['section'] for r in passages('mahabharata-english')},set(range(1,19)))
  self.assertEqual(len(passages('vishnu-english')),126)
  self.assertEqual({r['section'] for r in passages('ramayana-english')},set(range(1,7)))
 def test_complete_shiva_purana_structure(self):
  rows=passages('shiva-complete')
  self.assertEqual(len(rows),457)
  self.assertEqual({s:len([r for r in rows if r['section']==s]) for s in sorted({r['section'] for r in rows})},{100:25,201:20,202:43,203:55,204:20,205:59,300:42,400:43,500:51,600:23,701:35,702:41})
  self.assertTrue(all(len(r['original'])>80 for r in rows))
 def test_folklore_is_separate_and_substantial(self):
  tales=[s for s in STORIES if s.get('genre')=='Folklore']
  self.assertEqual(len(tales),29)
  self.assertTrue(all(len(s['text'])>400 for s in tales))
 def test_home_opens_english_reader(self):
  app=AppTest.from_file('app.py').run()
  self.assertTrue(any('The Reading Room' in m.value for m in app.markdown))
  next(b for b in app.button if b.key=='home_Reading room').click().run()
  self.assertFalse(app.exception)
  next(s for s in app.selectbox if s.label=='Choose an English book').set_value('vishnu-english').run()
  self.assertFalse(app.exception)
  self.assertTrue(any(len(m.value)>500 for m in app.markdown))
if __name__=='__main__':unittest.main()
