"""Compact top navigation for the focused five-collection experience."""
import streamlit as st

ITEMS=[('Home','Home'),('Reading room','Library'),('Learn & chant','Learn'),
       ('Situations','Guidance'),('Games','Games'),('Converse','Ask'),
       ('Study my text','My text'),('Settings','Profile'),('Coverage & sources','Sources')]

def _go(page):st.session_state.page=page

def top_navigation():
 if 'page' not in st.session_state:st.session_state.page='Home'
 cols=st.columns([1,1.05,.9,1.05,.9,.9,1,.9,.9],gap='small')
 for col,(page,label) in zip(cols,ITEMS):
  col.button(label,key='nav_'+page,use_container_width=True,
             type='primary' if st.session_state.page==page else 'secondary',
             on_click=_go,args=(page,))
 return st.session_state.page

sidebar_navigation=top_navigation
