import streamlit as st
import datetime
from friendly_ui import STORIES,SCENARIOS
from knowledge import works,CONTENT
from settings_ui import saved

def home_ui():
 st.markdown("""<style>.rr-hero{position:relative;overflow:hidden;padding:32px;border-radius:26px;background:linear-gradient(120deg,#2f7148,#619b55 55%,#d7b64d);color:white;margin:16px 0 24px}.rr-hero:after{content:'🕊️  🌿  🪷';position:absolute;right:22px;top:18px;font-size:2rem;opacity:.85}.rr-hero h2{color:white;font-family:Georgia,serif;font-size:2rem;max-width:720px}.rr-hero p{font-size:1.1rem}.rr-hero small{color:#fffbdc}@media(prefers-reduced-motion:no-preference){.rr-hero{animation:reader-arrive .7s ease-out}@keyframes reader-arrive{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}}</style><div class="rr-hero"><small>A QUIET GARDEN OF STORIES AND WISDOM</small><h2>Reflect fully. Then choose your next step.</h2><p>A simple rendering of the invitation in Bhagavad Gita 18.63.</p><small>Read slowly · listen gently · carry one useful teaching into today</small></div>""",unsafe_allow_html=True)
 st.write('A place for children, elders and everyone in between to read, listen, remember and reflect.')
 reviews=saved('reviews',{}) if st.session_state.get('_profile') else st.session_state.get('_reviews',{})
 due=[r for r in reviews.values() if r.get('due','9999')<=datetime.date.today().isoformat()]
 if due:
  with st.container(border=True):
   st.subheader('Ready for review')
   st.write(f'{len(due)} learned verse'+('s are' if len(due)!=1 else ' is')+' ready for a short recall practice.')
   if st.button('Continue my verse practice',type='primary'):
    item=sorted(due,key=lambda x:x['due'])[0];st.session_state.page='Learn & chant';st.session_state.learning_course=item['work'];st.rerun()
 journeys=[('📚','Read & discover','Open stories and scripture chapters inside the app.','Reading room'),('🪷','Find a helpful next step','Explore a difficulty through teachings, stories and practical actions.','Situations'),('🎧','Learn & remember','Understand a verse, listen where recordings are available, and practise recall.','Learn & chant'),('🎲','Play & learn','Try scripture quizzes, character clues, family networks and event sequences.','Games'),('💬','Ask your mentor','Discuss a teaching or a real-life difficulty in simple language.','Converse')]
 for start in range(0,len(journeys),3):
  for col,(icon,title,body,page) in zip(st.columns(3),journeys[start:start+3]):
   with col.container(border=True):
    st.subheader(icon+' '+title);st.write(body)
    st.button('Open '+title.lower(),key='home_'+page,on_click=lambda p=page:st.session_state.update({'page':p}))
 st.caption(f"{len(works())} attributed source collections · {len(STORIES)} prepared readings · {len(SCENARIOS)+len(CONTENT['guidance']['guidance'])} practical situations")
 with st.expander('What kind of mentor is this?'):
  st.write('The Reading Room is a study companion. It helps you ask questions, understand a source and try a useful next step. Interpretations differ between traditions. It does not claim to replace a qualified human teacher or speak with divine authority.')
