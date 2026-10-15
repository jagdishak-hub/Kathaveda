"""Content-first experiences for Tattvika.

This module keeps the literature database as the source of truth while presenting it
as a spiritual learning product rather than a database browser.
"""
import json
import streamlit as st
from knowledge import works, passages
from friendly_ui import STORIES, SCENARIOS
from reader_ui import reader_ui


def _go(page, **state):
    st.session_state.page = page
    st.session_state.update(state)


def _short(text, n=180):
    text = ' '.join((text or '').split())
    return text if len(text) <= n else text[:n].rsplit(' ', 1)[0] + '…'


def _group(work):
    title = work['title'].lower()
    if any(x in title for x in ('sahasranama', 'narayaneeyam', 'stotra', 'hymn')):
        return 'Chanting & devotion'
    if any(x in title for x in ('purana', 'bhagavatam', 'ramayana', 'mahabharata')):
        return 'Epics & Puranas'
    if any(x in title for x in ('upanishad', 'gita', 'vedanta', 'sutra')):
        return 'Philosophy & wisdom'
    if 'veda' in title:
        return 'Vedas'
    return 'Other texts'


def explore_library():
    st.markdown('''
    <div class="tv-section-hero">
      <div class="tv-kicker">EXPLORE</div>
      <h2>Choose a text, not a database row.</h2>
      <p>Browse the library visually, then open the text with meaning, context and Tattvika beside it.</p>
    </div>''', unsafe_allow_html=True)

    W = works()
    lookup = {w['id']: w for w in W}
    open_id = st.session_state.get('_open_work') or st.session_state.get('_library_work')
    if open_id in lookup:
        if st.button('← Back to Explore'):
            st.session_state.pop('_open_work', None)
            st.session_state.pop('_library_work', None)
            st.rerun()
        reader_ui(locked_id=open_id)
        return

    search = st.text_input('Search the library', placeholder='Try Gita, Shiva, devotion, Upanishad…')
    groups = ['All'] + sorted({_group(w) for w in W})
    group = st.segmented_control('Browse by', groups, default='All')
    filtered = [w for w in W if (group == 'All' or _group(w) == group) and
                (not search or search.lower() in (w['title'] + ' ' + w.get('coverage','') + ' ' + w.get('note','')).lower())]

    st.caption(f'{len(filtered)} collections shown · every card retains its own edition and coverage record')
    icons = {'gita':'🕉️','bhagavatam':'🪷','vishnu':'🔵','lalita':'🌺','narayaneeyam':'🎶','shiva-complete':'🔱'}
    for start in range(0, len(filtered), 3):
        for col, w in zip(st.columns(3), filtered[start:start+3]):
            with col:
                st.markdown('<div class="tv-library-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="tv-kicker">{_group(w)}</div>', unsafe_allow_html=True)
                st.markdown('### ' + icons.get(w['id'], '📜') + ' ' + w['title'])
                st.write(_short(w.get('coverage') or w.get('note') or 'Open this collection to read and study.', 200))
                badges=[]
                if w.get('language'): badges.append(w['language'])
                if w.get('edition'): badges.append(_short(w['edition'],70))
                if badges: st.caption(' · '.join(badges))
                if w['id'] in ('vishnu','lalita','narayaneeyam','gita','gita-besant'):
                    a,b=st.columns(2)
                    if a.button('Read', key='read_'+w['id'], use_container_width=True):
                        st.session_state['_open_work']=w['id']; st.rerun()
                    if b.button('Chant / Learn', key='chant_'+w['id'], type='primary', use_container_width=True):
                        _go('Learn & chant', learning_course=w['id']); st.rerun()
                else:
                    if st.button('Open text', key='open_'+w['id'], type='primary', use_container_width=True):
                        st.session_state['_open_work']=w['id']; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)


def _story_card(story, key):
    st.caption(story.get('book','') + ' · ' + story.get('ref',''))
    st.markdown('### ' + story['title'])
    st.write(_short(story.get('text'), 210))
    if story.get('themes'): st.caption(' · '.join(story['themes'][:4]))
    if st.button('Read story', key=key, use_container_width=True, type='primary'):
        st.session_state['_story_focus'] = story['id']
        st.rerun()


def stories_experience():
    st.markdown('''<div class="tv-section-hero"><div class="tv-kicker">STORIES</div>
    <h2>Enter scripture through the people, choices and turning points.</h2>
    <p>Prepared retellings stay separate from canonical Read text, with their source range kept visible.</p></div>''', unsafe_allow_html=True)

    sid = st.session_state.get('_story_focus') or st.session_state.pop('_open_story', None)
    story = next((s for s in STORIES if s['id']==sid), None)
    if story:
        if st.button('← Back to Stories'):
            st.session_state.pop('_story_focus',None); st.rerun()
        st.caption(story.get('book','') + ' · ' + story.get('ref','') + ' · prepared retelling')
        st.title(story['title'])
        st.markdown(story.get('text',''))
        if story.get('reflection'): st.info('Reflect: ' + story['reflection'])
        c1,c2=st.columns(2)
        if c1.button('Ask Tattvika about this story', type='primary', use_container_width=True):
            st.session_state['_conversation_question']='Help me understand the story '+story['title']+'. Explain its source context, main turning points and what it may teach without presenting the retelling as a literal translation.'
            _go('Converse'); st.rerun()
        if c2.button('Find related stories', use_container_width=True):
            st.session_state.pop('_story_focus',None); st.session_state['_story_theme']=story.get('themes',[None])[0]; st.rerun()
        with st.expander('Source notes'):
            st.write('This page is a prepared narrative layer. The canonical scripture remains in Explore & Read. Source references are retained so the two layers can be compared.')
        return

    themes=sorted({t for s in STORIES for t in s.get('themes',[])})
    qcol,tcol=st.columns([2,1])
    term=qcol.text_input('Find a story or character',placeholder='Krishna, Dhruva, courage, friendship…')
    default_theme=st.session_state.pop('_story_theme',None)
    options=['All themes']+themes
    theme=tcol.selectbox('Theme',options,index=options.index(default_theme) if default_theme in options else 0)
    filtered=[s for s in STORIES if (theme=='All themes' or theme in s.get('themes',[])) and
              (not term or term.lower() in (s['title']+' '+s.get('text','')+' '+' '.join(s.get('themes',[]))).lower())]
    st.caption(f'{len(filtered)} stories available')
    for start in range(0,min(len(filtered),60),3):
        for col,s in zip(st.columns(3),filtered[start:start+3]):
            with col.container(border=True): _story_card(s,'story_'+s['id'])


def reflect_experience():
    st.markdown('''<div class="tv-section-hero"><div class="tv-kicker">REFLECT</div>
    <h2>Start with what you are actually feeling.</h2>
    <p>Choose a situation first. Tattvika then connects it to relevant practices, stories and scripture instead of forcing you to know a verse number.</p></div>''', unsafe_allow_html=True)

    feelings={
      'Anxious / overwhelmed':['scared','too big','exhausted','wandering','disconnected'],
      'Jealous / comparing':['better than me','envy'],
      'Angry / hurt':['angry','defensive','listen to me'],
      'Stuck / procrastinating':['putting off','repeat','reward before'],
      'Unsure / changing direction':['option to choose','change my mind','begin again'],
      'Relationships':['message','corrected','listen','judge','say yes'],
    }
    label=st.selectbox('What is closest to your situation?',['Browse all']+list(feelings))
    rows=SCENARIOS
    if label!='Browse all':
        terms=feelings[label]
        rows=[r for r in SCENARIOS if any(t in r[0].lower() for t in terms)] or SCENARIOS
    for start in range(0,min(len(rows),24),3):
        for col,row in zip(st.columns(3),rows[start:start+3]):
            title,category,level,practice,example,topic=row
            with col.container(border=True):
                st.caption(category)
                st.markdown('### '+title)
                st.write(_short(practice,180))
                if st.button('Explore with Tattvika',key='reflect_'+str(start)+title,use_container_width=True,type='primary'):
                    st.session_state['_conversation_question']='I am dealing with this situation: '+title+'. Start with a practical response, then use relevant Hindu texts or stories as perspective. Clearly separate scripture from interpretation.'
                    _go('Converse');st.rerun()
