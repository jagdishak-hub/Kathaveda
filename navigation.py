import datetime
import streamlit as st
from settings_ui import saved

GROUPS=[
 ('DISCOVER',[('Home','⌂','Home'),('Reading room','▤','Reading room'),('Story garden','✦','Story garden'),('Situations','◈','Guidance')]),
 ('PRACTISE',[('Learn & chant','♫','Learn & chant'),('Games','◆','Games'),('Converse','◌','Ask the mentor')]),
 ('MY SPACE',[('Settings','⚙','Settings'),('Coverage & sources','ⓘ','Sources & coverage')])]

def _go(page):
 st.session_state.page=page

def sidebar_navigation():
 if 'page' not in st.session_state:st.session_state.page='Home'
 st.sidebar.markdown('<div class="rr-side-name">THE READING ROOM</div><div class="rr-side-line">Read · Reflect · Remember</div>',unsafe_allow_html=True)
 for group,items in GROUPS:
  st.sidebar.markdown(f'<div class="rr-side-group">{group}</div>',unsafe_allow_html=True)
  for page,icon,label in items:
   st.sidebar.button(f'{icon}  {label}',key='nav_'+page,use_container_width=True,type='primary' if st.session_state.page==page else 'secondary',on_click=_go,args=(page,))
 st.sidebar.markdown('<div class="rr-side-group">TODAY</div>',unsafe_allow_html=True)
 reviews=saved('reviews',{}) if st.session_state.get('_profile') else st.session_state.get('_reviews',{})
 today=datetime.date.today().isoformat();due=sum(1 for r in reviews.values() if r.get('due','9999')<=today)
 profile=st.session_state.get('_profile')
 st.sidebar.markdown(f'<div class="rr-study-card"><b>{"Study profile open" if profile else "Browsing privately"}</b><br><span>{profile if profile else "Open a profile in Settings to keep progress."}</span><hr><b>{due}</b> verse review{"s" if due!=1 else ""} due</div>',unsafe_allow_html=True)
 return st.session_state.page
