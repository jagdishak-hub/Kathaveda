import datetime,json
import streamlit as st
from friendly_ui import STORIES,SCENARIOS
from knowledge import works,passages
from settings_ui import saved
from game_bank import QUIZ_BANK


def _go(page,**state):
    st.session_state.page=page;st.session_state.update(state)

def _daily(items,salt=0):
    if not items:return None
    return items[(datetime.date.today().toordinal()+salt)%len(items)]

def _short(text,n=180):
    text=' '.join((text or '').split())
    return text if len(text)<=n else text[:n].rsplit(' ',1)[0]+'…'


def home_ui():
    st.markdown('''<style>
    .tv-hero{position:relative;overflow:hidden;padding:42px;border-radius:30px;background:linear-gradient(125deg,#193f2b 0%,#3f7550 52%,#c49a43 100%);color:white;margin:10px 0 24px}.tv-hero h2{color:white!important;font-size:2.45rem!important;margin:.25rem 0 .5rem;max-width:790px}.tv-hero p{font-size:1.08rem;max-width:800px;opacity:.94}.tv-hero small{letter-spacing:.14em;font-weight:700;color:#fff3bd}.tv-hero:after{content:'🪷';position:absolute;right:34px;top:18px;font-size:6rem;opacity:.15}.tv-card{min-height:220px;padding:20px;border-radius:22px;background:#fffefa;border:1px solid #d9e4cf;box-shadow:0 8px 24px #28452f0c}.tv-card h3{margin:.25rem 0 .45rem}.tv-strip{padding:18px 20px;border-radius:20px;background:linear-gradient(90deg,#eef7e8,#fff7df);border:1px solid #d7e3c8;margin:8px 0 18px}
    </style><div class="tv-hero"><small>TATTVIKA · LIVING HINDU WISDOM</small><h2>Read deeply. Chant with meaning. Ask across the tradition.</h2><p>A living library for scripture, stories, reflection and learning - with the text and its meaning kept together.</p></div>''',unsafe_allow_html=True)
    W=works();by_id={w['id']:w for w in W}

    last=st.session_state.get('_last_reading')
    if last:
        st.markdown('<div class="tv-strip"><b>Continue where you left off</b><br>'+last['title']+' · '+last['label']+'</div>',unsafe_allow_html=True)
        if st.button('Continue reading',type='primary'):
            _go('Reading room',_open_work=last['work']);st.rerun()

    reviews=saved('reviews',{}) if st.session_state.get('_profile') else st.session_state.get('_reviews',{})
    due=[r for r in reviews.values() if r.get('due','9999')<=datetime.date.today().isoformat()]
    if due:
        st.info(f"{len(due)} review item{'s are' if len(due)!=1 else ' is'} ready in Chant & Learn.")

    st.markdown('## Today')
    gita=passages('gita') if 'gita' in by_id else []
    verse=_daily(gita);story=_daily(STORIES,17);quiz=_daily(QUIZ_BANK,41);prompt=_daily(SCENARIOS,29)
    cards=[('Daily wisdom',verse),('Story of the day',story),('Daily quiz',quiz),('Reflect',prompt)]
    cols=st.columns(4)
    with cols[0]:
        st.markdown('<div class="tv-card"><div class="tv-kicker">DAILY WISDOM</div>',unsafe_allow_html=True)
        if verse:
            st.markdown('### '+verse['reference']);st.write(_short(verse.get('transliteration') or verse.get('original'),140))
            try:meaning=json.loads(verse.get('metadata') or '{}').get('meaning')
            except Exception:meaning=None
            if meaning and not meaning.startswith('An editorially reviewed'):st.caption(_short(meaning,145))
            if st.button('Open verse',key='daily_verse',use_container_width=True):_go('Learn & chant',learning_course='gita');st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="tv-card"><div class="tv-kicker">STORY OF THE DAY</div>',unsafe_allow_html=True)
        if story:
            st.markdown('### '+story['title']);st.write(_short(story.get('text'),170));st.caption(story.get('book','')+' · '+story.get('ref',''))
            if st.button('Read story',key='daily_story',use_container_width=True):_go('Story garden',_story_focus=story['id']);st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div class="tv-card"><div class="tv-kicker">DAILY QUIZ</div>',unsafe_allow_html=True)
        if quiz:
            st.markdown('### One question');st.write(_short(quiz.get('prompt'),170));st.caption(quiz.get('book','Scripture'))
            if st.button('Take today’s quiz',key='daily_quiz',use_container_width=True):_go('Games');st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with cols[3]:
        st.markdown('<div class="tv-card"><div class="tv-kicker">REFLECT</div>',unsafe_allow_html=True)
        if prompt:
            st.markdown('### '+prompt[0]);st.write(_short(prompt[3],165))
            if st.button('Explore this',key='daily_reflect',use_container_width=True):_go('Situations');st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('## Featured paths')
    actions=[('📖','Explore scriptures','Browse the full attributed library visually.','Reading room'),('🎶','Chant with meaning','Learn Gita, Sahasranamas and Narayaneeyam without leaving Tattvika.','Learn & chant'),('🌿','Stories','Enter the tradition through people, choices and turning points.','Story garden'),('🧭','I’m feeling…','Start from a real-life emotion or dilemma.','Situations'),('💬','Ask Tattvika','Ask a verse, compare texts or reflect with evidence visible.','Converse'),('🧠','Games','Build recall through quizzes, characters, family trees and timelines.','Games')]
    for start in range(0,6,3):
        for col,(icon,title,body,page) in zip(st.columns(3),actions[start:start+3]):
            with col.container(border=True):
                st.markdown(f'### {icon} {title}');st.write(body);st.button('Open',key='path_'+page,on_click=_go,args=(page,),use_container_width=True)

    st.markdown('## Featured library')
    preferred=['gita','bhagavatam','vishnu','lalita','narayaneeyam','shiva-complete']
    selected=[by_id[i] for i in preferred if i in by_id]
    for start in range(0,len(selected),3):
        for col,w in zip(st.columns(3),selected[start:start+3]):
            with col.container(border=True):
                st.caption(w.get('language','Scripture'))
                st.markdown('### '+w['title']);st.write(_short(w.get('coverage') or w.get('note'),170))
                if w['id'] in ('vishnu','lalita','narayaneeyam','gita'):
                    a,b=st.columns(2)
                    if a.button('Read',key='hr_'+w['id'],use_container_width=True):_go('Reading room',_open_work=w['id']);st.rerun()
                    if b.button('Learn',key='hl_'+w['id'],type='primary',use_container_width=True):_go('Learn & chant',learning_course=w['id']);st.rerun()
                else:
                    if st.button('Explore',key='he_'+w['id'],type='primary',use_container_width=True):_go('Reading room',_open_work=w['id']);st.rerun()
    st.caption(f"{len(W)} attributed collections · {len(STORIES)} prepared stories · all edition and coverage details remain auditable under Sources")
