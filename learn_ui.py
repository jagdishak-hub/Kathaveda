import json
import streamlit as st
from knowledge import works,passages
from settings_ui import saved,save
from chanting_ui import chanting_study
from pronunciation_ui import pronunciation_ui


def _render_text(r):
    st.markdown('### '+r['reference'])
    st.text(r['original'])
    if r.get('transliteration') and r['transliteration']!=r['original']:
        with st.expander('Transliteration',expanded=True):st.text(r['transliteration'])
    try:meta=json.loads(r.get('metadata') or '{}')
    except Exception:meta={}
    meaning=(meta.get('meaning') or '').strip()
    if meaning and not meaning.startswith('An editorially reviewed'):
        st.info(meaning)


def learn_and_chant():
    st.markdown('''<div class="tv-section-hero"><div class="tv-kicker">CHANT & LEARN</div>
    <h2>See it. Understand it. Chant it. Recall it.</h2>
    <p>Text, transliteration, meaning, pronunciation guidance and review stay together. You never need to leave Tattvika to understand what you are chanting.</p></div>''',unsafe_allow_html=True)
    titles={w['id']:w['title'] for w in works()}
    courses=[i for i in ['gita','gita-besant','vishnu','lalita','narayaneeyam'] if i in titles]
    preferred=st.session_state.get('learning_course')
    wid=st.selectbox('Choose a course',courses,index=courses.index(preferred) if preferred in courses else 0,format_func=lambda i:titles[i],key='learning_course')
    units=passages(wid)
    if not units:
        st.warning('No learning units are stored for this collection yet.');return
    position_key='position_'+wid
    if position_key not in st.session_state:
        st.session_state[position_key]=min(saved('chant-progress',{}).get(position_key,0),len(units)-1)
    def move(delta):
        st.session_state[position_key]=max(0,min(len(units)-1,st.session_state[position_key]+delta))
    unit_key='unit_'+wid
    if unit_key not in st.session_state:st.session_state[unit_key]=st.session_state[position_key]+1
    top1,top2=st.columns([2,1])
    idx=top1.number_input('Current unit',1,len(units),key=unit_key)
    if idx-1!=st.session_state[position_key]:st.session_state[position_key]=idx-1
    r=units[st.session_state[position_key]]
    top2.metric('Progress',f'{idx}/{len(units)}')
    st.progress(idx/len(units))
    st.caption(r['reference'])

    text_tab,meaning_tab,practice_tab=st.tabs(['📜 Text','💡 Meaning','🎧 Practise'])
    with text_tab:_render_text(r)
    with meaning_tab:chanting_study(r,wid,titles[wid])
    with practice_tab:
        st.write('Read once slowly. Listen or pronounce carefully. Repeat one line at a time. Hide the text and recall it. Then join this unit to the previous one.')
        pronunciation_ui(r)
        hide=st.toggle('Hide text for recall',value=False,key='hide_'+r['id'])
        if hide:st.info('Recite from memory, then turn this off to compare.')
        else:_render_text(r)

    def advance():
        st.session_state['practised_'+r['id']]=True;move(1);st.session_state[unit_key]=st.session_state[position_key]+1
    a,b,c=st.columns([1,1,1.4])
    a.button('← Previous',on_click=lambda:(move(-1),st.session_state.update({unit_key:st.session_state[position_key]+1})),disabled=idx==1,use_container_width=True)
    b.button('Repeat',on_click=lambda:None,use_container_width=True)
    c.button('Understood & practised →',on_click=advance,disabled=idx==len(units),type='primary',use_container_width=True)
    if st.session_state.get('_profile') and st.button('Save progress to my profile'):
        save('chant-progress',{k:v for k,v in st.session_state.items() if k.startswith(('position_','practised_'))});st.success('Progress saved.')
    with st.expander('Learning notes'):
        st.write('Meanings and Tattvika explanations are displayed separately from the canonical chant text. AI-assisted explanations are study aids, not traditional commentary. Pronunciation guidance is supplementary; use a trained reciter for difficult passages.')
