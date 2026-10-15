"""Top navigation for the Tattvika learning experience.

Internal page names are kept stable so existing saved sessions and page routing do
not break. Only the user-facing labels are simplified.
"""
import streamlit as st

ITEMS=[
    ('Home','Home'),
    ('Reading room','Explore & Read'),
    ('Story garden','Stories'),
    ('Learn & chant','Chant & Learn'),
    ('Situations','Reflect'),
    ('Games','Quiz'),
    ('Converse','Ask Tattvika'),
    ('Study my text','My Library'),
    ('Coverage & sources','Sources'),
]

def _go(page):
    st.session_state.page=page

def top_navigation():
    if 'page' not in st.session_state:
        st.session_state.page='Home'
    cols=st.columns([.72,1.18,.78,1.06,.78,.66,1.08,.82,.78],gap='small')
    for col,(page,label) in zip(cols,ITEMS):
        col.button(label,key='nav_'+page,use_container_width=True,
                   type='primary' if st.session_state.page==page else 'secondary',
                   on_click=_go,args=(page,))
    return st.session_state.page

sidebar_navigation=top_navigation
