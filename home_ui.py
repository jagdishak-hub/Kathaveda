import streamlit as st
import datetime
from friendly_ui import STORIES,SCENARIOS
from knowledge import works,CONTENT
from settings_ui import saved

def home_ui():
 st.markdown("""<style>.rr-hero{position:relative;overflow:hidden;padding:32px;border-radius:26px;background:linear-gradient(120deg,#2f7148,#619b55 55%,#d7b64d);color:white;margin:16px 0 24px}.rr-hero:after{content:'🕊️  🌿  🪷';position:absolute;right:22px;top:18px;font-size:2rem;opacity:.85}.rr-hero h2{color:white;font-family:Georgia,serif;font-size:2rem;max-width:720px}.rr-hero p{font-size:1.1rem}.rr-hero small{color:#fffbdc}@media(prefers-reduced-motion:no-preference){.rr-hero{animation:reader-arrive .7s ease-out}@keyframes reader-arrive{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}}</style><div class="rr-hero"><small>A QUIET GARDEN OF STORIES AND WISDOM</small><h2>Reflect fully. Then choose your next step.</h2><p>A simple rendering of the invitation in Bhagavad Gita 18.63.</p><small>Read slowly · listen gently · carry one useful teaching into today</small></div>""",unsafe_allow_html=True)
 st.write('A calm, carefully sourced place for children, elders and everyone in between to read, learn, remember and apply scripture.')
 reviews=saved('reviews',{}) if st.session_state.get('_profile') else st.session_state.get('_reviews',{})
 due=[r for r in reviews.values() if r.get('due','9999')<=datetime.date.today().isoformat()]
 if due:
  with st.container(border=True):
   st.subheader('Ready for review')
   st.write(f'{len(due)} learned verse'+('s are' if len(due)!=1 else ' is')+' ready for a short recall practice.')
   if st.button('Continue my verse practice',type='primary'):
    item=sorted(due,key=lambda x:x['due'])[0];st.session_state.page='Learn & chant';st.session_state.learning_course=item['work'];st.rerun()
 st.markdown('## Begin with a collection')
 books=[('🕉','Bhagavad Gita','18 chapters · verse learning and practical guidance','Complete structured text'),('🪷','Srimad Bhagavatam','12 cantos · stories, characters and devotion','Source text with growing story guides'),('🎶','Narayaneeyam','100 dasakams · Bhagavatam retold through devotion','Complete verse sequence'),('🔱','Shiva Purana','7 samhitas · 457 Sanskrit chapters','Complete named Sanskrit edition'),('📜','Saraswati Literature','Upanishad, hymns, stotras and attributed narratives','Verified collection in development')]
 for start in range(0,len(books),3):
  for col,(icon,title,body,status) in zip(st.columns(3),books[start:start+3]):
   with col.container(border=True):
    st.markdown('<span class="rr-kicker">'+status+'</span>',unsafe_allow_html=True);st.subheader(icon+' '+title);st.write(body)
    st.button('Open collection',key='home_book_'+title,on_click=lambda:st.session_state.update({'page':'Reading room'}),use_container_width=True)
 st.markdown('## What would you like to do?')
 journeys=[('Read a chapter','Reading room'),('Learn a verse','Learn & chant'),('Find guidance','Situations'),('Play a challenge','Games'),('Ask the mentor','Converse'),('Study my own text','Study my text')]
 for col,(label,page) in zip(st.columns(6),journeys):col.button(label,key='home_'+page,on_click=lambda p=page:st.session_state.update({'page':p}),use_container_width=True)
 st.caption(f"Five focused collections · {len(STORIES)} prepared readings · {len(SCENARIOS)+len(CONTENT['guidance']['guidance'])} practical situations · additional legacy sources remain under Sources")
 with st.expander('What kind of mentor is this?'):
  st.write('The Reading Room is a study companion. It helps you ask questions, understand a source and try a useful next step. Interpretations differ between traditions. It does not claim to replace a qualified human teacher or speak with divine authority.')
