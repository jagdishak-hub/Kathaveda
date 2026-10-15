import datetime,json
import streamlit as st
from friendly_ui import STORIES,SCENARIOS
from knowledge import works,passages,CONTENT
from settings_ui import saved


def _go(page,**state):
    st.session_state.page=page
    st.session_state.update(state)


def _daily(items,salt=0):
    if not items:return None
    day=datetime.date.today().toordinal()+salt
    return items[day%len(items)]


def _short(text,n=180):
    text=' '.join((text or '').split())
    return text if len(text)<=n else text[:n].rsplit(' ',1)[0]+'…'


def home_ui():
    st.markdown('''
    <style>
    .tv-hero{position:relative;overflow:hidden;padding:38px 40px;border-radius:30px;
      background:linear-gradient(125deg,#193f2b 0%,#3f7550 52%,#c49a43 100%);color:white;margin:10px 0 24px}
    .tv-hero h2{color:white!important;font-size:2.35rem!important;margin:.25rem 0 .5rem;max-width:780px}
    .tv-hero p{font-size:1.08rem;max-width:780px;opacity:.94}.tv-hero small{letter-spacing:.14em;font-weight:700;color:#fff3bd}
    .tv-hero:after{content:'🪷';position:absolute;right:34px;top:22px;font-size:5rem;opacity:.16}
    .tv-card{min-height:215px;padding:20px;border-radius:22px;background:#fffefa;border:1px solid #d9e4cf;box-shadow:0 8px 24px #28452f0c}
    .tv-card h3{margin:.25rem 0 .45rem}.tv-kicker{font-size:.72rem;letter-spacing:.13em;text-transform:uppercase;color:#7c7656;font-weight:800}
    .tv-muted{color:#657268;font-size:.9rem}.tv-strip{padding:18px 20px;border-radius:20px;background:linear-gradient(90deg,#eef7e8,#fff7df);border:1px solid #d7e3c8;margin:8px 0 18px}
    </style>
    <div class="tv-hero"><small>TATTVIKA · LIVING HINDU WISDOM</small><h2>Read the text. Understand the meaning. Carry it into life.</h2>
    <p>Explore scripture, stories and chants with meaning, context, reflection and source-grounded conversation in one place.</p></div>
    ''',unsafe_allow_html=True)

    W=works(); by_id={w['id']:w for w in W}
    reviews=saved('reviews',{}) if st.session_state.get('_profile') else st.session_state.get('_reviews',{})
    due=[r for r in reviews.values() if r.get('due','9999')<=datetime.date.today().isoformat()]
    if due:
        st.markdown(f'<div class="tv-strip"><b>{len(due)} review item'+('s are' if len(due)!=1 else ' is')+' ready.</b> A short recall session is waiting for you.</div>',unsafe_allow_html=True)
        if st.button('Continue review',type='primary'):
            item=sorted(due,key=lambda x:x['due'])[0]
            _go('Learn & chant',learning_course=item.get('work'))
            st.rerun()

    st.markdown('## Today in Tattvika')
    c1,c2,c3=st.columns(3)
    # Daily wisdom from the stored Gita corpus when available.
    gita=passages('gita') if 'gita' in by_id else []
    verse=_daily(gita)
    with c1:
        st.markdown('<div class="tv-card"><div class="tv-kicker">Daily wisdom</div>',unsafe_allow_html=True)
        if verse:
            st.markdown('### '+verse['reference'])
            st.write(_short(verse.get('transliteration') or verse.get('original'),150))
            try:meaning=json.loads(verse.get('metadata') or '{}').get('meaning')
            except Exception:meaning=None
            if meaning and not meaning.startswith('An editorially reviewed'):st.caption(_short(meaning,170))
            if st.button('Open this verse',key='daily_verse',use_container_width=True):
                _go('Learn & chant',learning_course='gita');st.rerun()
        else:st.write('Daily wisdom becomes available when the Gita corpus is loaded.')
        st.markdown('</div>',unsafe_allow_html=True)
    story=_daily(STORIES,17)
    with c2:
        st.markdown('<div class="tv-card"><div class="tv-kicker">Story of the day</div>',unsafe_allow_html=True)
        if story:
            st.markdown('### '+story['title']);st.write(_short(story.get('text'),190));st.caption(story.get('book','')+' · '+story.get('ref',''))
            if st.button('Read the story',key='daily_story',use_container_width=True):
                st.session_state['_open_story']=story['id'];_go('Story garden');st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    prompt=_daily(SCENARIOS,29)
    with c3:
        st.markdown('<div class="tv-card"><div class="tv-kicker">Reflect</div>',unsafe_allow_html=True)
        if prompt:
            st.markdown('### '+prompt[0]);st.write(_short(prompt[3],190))
            if st.button('Explore this situation',key='daily_reflect',use_container_width=True):
                _go('Situations');st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('## Explore the library')
    preferred=['gita','bhagavatam','vishnu','lalita','narayaneeyam','shiva-complete']
    selected=[by_id[i] for i in preferred if i in by_id]
    if len(selected)<9:
        selected += [w for w in W if w not in selected][:9-len(selected)]
    icons={'gita':'🕉️','bhagavatam':'🪷','vishnu':'🔵','lalita':'🌺','narayaneeyam':'🎶','shiva-complete':'🔱'}
    for start in range(0,min(len(selected),9),3):
        for col,w in zip(st.columns(3),selected[start:start+3]):
            with col:
                st.markdown('<div class="tv-card">',unsafe_allow_html=True)
                st.markdown('<div class="tv-kicker">'+str(w.get('language','Scripture'))+'</div>',unsafe_allow_html=True)
                st.markdown('### '+icons.get(w['id'],'📜')+' '+w['title'])
                st.write(_short(w.get('coverage') or w.get('note') or 'Open this collection to read and study.',170))
                if w['id'] in ('vishnu','lalita','narayaneeyam','gita'):
                    label='Chant & understand'
                    if st.button(label,key='home_chant_'+w['id'],use_container_width=True):
                        _go('Learn & chant',learning_course=w['id']);st.rerun()
                else:
                    if st.button('Explore & read',key='home_read_'+w['id'],use_container_width=True):
                        _go('Reading room',_library_work=w['id']);st.rerun()
                st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('## Choose your path')
    actions=[
      ('📖','Read deeply','Open a scripture with text, meaning and context.','Reading room'),
      ('🎶','Chant with meaning','Learn a verse or name without leaving Tattvika.','Learn & chant'),
      ('🌿','Read a story','Follow a source-grounded narrative and reflect on it.','Story garden'),
      ('🧭','Find perspective','Start from a real-life feeling or dilemma.','Situations'),
      ('💬','Ask Tattvika','Ask across the stored library and keep the sources visible.','Converse'),
      ('🧠','Test yourself','Use quizzes and challenges to strengthen recall.','Games'),
    ]
    for start in range(0,6,3):
        for col,(icon,title,body,page) in zip(st.columns(3),actions[start:start+3]):
            with col.container(border=True):
                st.markdown(f'### {icon} {title}');st.write(body)
                st.button('Open',key='path_'+page,on_click=_go,args=(page,),use_container_width=True)

    st.markdown('## Your own books')
    st.write('Use **My Library** for PDFs or texts you personally own or are allowed to use. They can be studied privately without copying a restricted edition into the public Tattvika corpus.')
    if st.button('Open My Library'):
        _go('Study my text');st.rerun()

    st.caption(f"{len(W)} attributed collections in the catalogue · {len(STORIES)} prepared stories · sources and coverage remain auditable under Sources")
