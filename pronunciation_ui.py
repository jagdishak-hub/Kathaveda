import datetime
import html,re
import streamlit as st
from settings_ui import saved,save
AUDIO_URL='https://upload.wikimedia.org/wikipedia/commons/e/e2/%E0%A4%AF%E0%A5%8B%E0%A4%97%E0%A4%B8%E0%A5%8D%E0%A4%A5%E0%A4%83_%E0%A4%95%E0%A5%81%E0%A4%B0%E0%A5%81_%E0%A4%95%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE%E0%A4%A3%E0%A4%BF.wav'
def pronunciation_ui(r):
 st.subheader('Listen, repeat, recall')
 translit=(r.get('transliteration') or '').strip()
 if translit:
  st.markdown('**Pronunciation line**')
  for number,line in enumerate(translit.splitlines(),1):
   words=line.replace('|',' । ').replace('||',' ॥ ').split()
   chips=''.join(f'<span style="display:inline-block;background:#f4eafb;border:1px solid #dfcbea;border-radius:10px;padding:6px 9px;margin:3px;font-size:1.06rem">{html.escape(w)}</span>' for w in words)
   st.markdown(chips,unsafe_allow_html=True)
  with st.expander('How to sound the marked letters'):
   st.markdown('**ā ī ū** — hold the vowel for two beats  ·  **ṛ** — a short vocalic *r*  ·  **ṃ / ṁ** — nasalise the preceding sound  ·  **ḥ** — a soft breath after the vowel')
   st.markdown('**ṭ ṭh ḍ ḍh ṇ** — curl the tongue back  ·  **ś** — as in *shiva*  ·  **ṣ** — a deeper *sh* with the tongue back  ·  **ñ** — as in *canyon*')
   st.caption('The marks make a written guide. A trained human recitation remains the reference for rhythm, pitch and joined sounds.')
 supported=r['work_id'] in ('gita','gita-besant') and r['chapter']==2 and r['verse']==48
 if supported:
  st.audio(AUDIO_URL,format='audio/wav',loop=True)
  st.caption('Human recitation: NehalDaveND · 21 October 2015 · CC BY-SA 4.0 · played without modification. Not independently checked by a pronunciation teacher.')
  with st.expander('Recording credit and licence'):
   st.link_button('Recording source','https://commons.wikimedia.org/wiki/File:योगस्थः_कुरु_कर्माणि.wav');st.link_button('CC BY-SA 4.0','https://creativecommons.org/licenses/by-sa/4.0/')
 else:st.caption('A matching attributed recitation is not available for this unit yet. Use a qualified reciter; pronunciation cannot be inferred from an English meaning.')
 st.write('1. Follow one word group. 2. Repeat one line slowly three times. 3. Hide the line and recall it. 4. Join it to the previous verse. 5. Review on the scheduled day.')
 if translit:
  lines=[x.strip() for x in translit.splitlines() if x.strip()]
  completed=0
  cols=st.columns(min(2,max(1,len(lines))))
  for i,line in enumerate(lines):
   if cols[i%len(cols)].checkbox('Line '+str(i+1)+' repeated 3 times',key='line_'+r['id']+'_'+str(i)):completed+=1
  st.progress(completed/max(1,len(lines)))
 with st.expander('Record a practice attempt'):
  recording=st.audio_input('Record yourself, then listen back')
  if recording:st.audio(recording);st.caption('Compare vowels, consonants and pauses with a trained reciter. This app does not automatically certify pronunciation. Your practice audio is not added to the shared scripture library.')
 rating=st.radio('How did recall feel?',['Still learning','Recalled with a hint','Recalled without looking'],horizontal=True,key='recall_'+r['id'])
 if st.button('Schedule my next review',key='review_'+r['id']):
  days={'Still learning':1,'Recalled with a hint':2,'Recalled without looking':7}[rating]
  due=(datetime.date.today()+datetime.timedelta(days=days)).isoformat()
  reviews=st.session_state.setdefault('_reviews',saved('reviews',{}));reviews[r['id']]={'reference':r['reference'],'due':due,'rating':rating,'work':r['work_id'],'id':r['id']}
  if st.session_state.get('_profile'):save('reviews',reviews)
  st.success('Next review: '+due+('. Saved to your profile.' if st.session_state.get('_profile') else '. Kept for this visit.'))
