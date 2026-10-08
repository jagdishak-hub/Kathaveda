import streamlit as st
from friendly_ui import STORIES,SCENARIOS
from knowledge import works,CONTENT

def home_ui():
 st.markdown("""<style>.rr-hero{padding:26px;border-radius:24px;background:linear-gradient(120deg,#563974,#984d7b,#d58a5a);color:white;margin:16px 0 24px}.rr-hero h2{color:white;font-family:Georgia,serif;font-size:2rem}.rr-hero p{font-size:1.1rem}.rr-hero small{color:#ffeed9}@media(prefers-reduced-motion:no-preference){.rr-hero{animation:reader-arrive .7s ease-out}@keyframes reader-arrive{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}}</style><div class="rr-hero"><small>A LITTLE WISDOM FOR EVERY DAY</small><h2>Reflect fully. Then choose your next step.</h2><p>A simple rendering of the invitation in Bhagavad Gita 18.63.</p><small>Explore the teaching, understand its context, and decide how it can help you today.</small></div>""",unsafe_allow_html=True)
 st.write('A place for children, elders and everyone in between to read, listen, remember and reflect.')
 journeys=[('📚','Read & discover','Open stories and scripture chapters inside the app.','Reading room'),('🪷','Find a helpful next step','Explore a difficulty through teachings, stories and practical actions.','Situations'),('🎧','Learn & remember','Understand a verse, listen where recordings are available, and practise recall.','Learn & chant'),('🎲','Play & learn','Try scripture quizzes, character clues, family networks and event sequences.','Games'),('💬','Ask your mentor','Discuss a teaching or a real-life difficulty in simple language.','Converse')]
 for start in range(0,len(journeys),3):
  for col,(icon,title,body,page) in zip(st.columns(3),journeys[start:start+3]):
   with col.container(border=True):
    st.subheader(icon+' '+title);st.write(body)
    st.button('Open '+title.lower(),key='home_'+page,on_click=lambda p=page:st.session_state.update({'page':p}))
 st.caption(f"{len(works())} attributed source collections · {len(STORIES)} prepared readings · {len(SCENARIOS)+len(CONTENT['guidance']['guidance'])} practical situations")
 with st.expander('What kind of mentor is this?'):
  st.write('The Reading Room is a study companion. It helps you ask questions, understand a source and try a useful next step. Interpretations differ between traditions. It does not claim to replace a qualified human teacher or speak with divine authority.')
