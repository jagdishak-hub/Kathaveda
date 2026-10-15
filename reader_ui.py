import hashlib,re,json
import streamlit as st
from knowledge import works,passages,CONTENT
from chapter_guides import GITA,BOOK_INTROS,SHIVA_READINGS
from settings_ui import STORE,active_settings
from providers import request,ProviderError


def prepare_explanation(id,reference,original,purpose='chapter'):
    cached=STORE.cached(id)
    if cached:return cached
    settings=active_settings();errors=[]
    if not any(s[1] for s in settings):raise ProviderError('Connect a provider in Settings once to prepare this explanation. Saved explanations reopen without another call.')
    prompt='Explain this '+purpose+' in clear, simple English. Stay strictly within the supplied text. Do not invent facts, quotations, Sanskrit meanings or missing events. Distinguish source narrative, traditional belief and modern reflection. Use headings: Overview; What happens or is said; Important words and ideas; Context; What to notice; Reflection. This is an explanatory study aid, not a literal translation or traditional commentary. Source: '+reference+'\n\nSOURCE TEXT:\n'+original
    if len(original)>100000:raise ProviderError('This reading is too long for a single explanation. Open a smaller reading unit.')
    for provider,key,model in settings:
        if not key:continue
        try:
            answer=request(provider,key,model,[{'role':'user','content':prompt}]);STORE.cache(id,answer,provider);return {'body':answer,'provider':provider}
        except ProviderError as e:errors.append(provider+': '+str(e))
    raise ProviderError('\n'.join(errors))


def story_for(wid,section,chapter):
    if wid not in ('bhagavatam','narayaneeyam'):return []
    out=[]
    for s in CONTENT['scriptures']['stories']:
        if wid=='narayaneeyam':
            if s['id']=='gajendra' and chapter==26:out.append(s)
            continue
        ref=s['ref'].split('Bhagavatam ')[-1]
        m=re.search(r'(\d+)\.(\d+)(?:[–-](\d+))?',ref)
        if m and int(m[1])==section:
            first=int(m[2]);last=int(m[3]) if m[3] else first
            if first<=chapter<=last:out.append(s)
    return out


def _meta(r):
    try:return json.loads(r.get('metadata') or '{}')
    except Exception:return {}


def _verse_card(r,wid):
    meta=_meta(r);meaning=(meta.get('meaning') or '').strip()
    with st.container(border=True):
        st.caption(r['reference'])
        st.markdown('#### '+r['original'].replace('\n','  \n'))
        if r.get('transliteration') and r['transliteration']!=r['original']:
            st.markdown('**Transliteration**')
            st.write(r['transliteration'])
        if meaning and not meaning.startswith('An editorially reviewed'):
            st.markdown('**Meaning / translation**')
            st.info(meaning)
        elif wid not in ('vishnu','lalita','narayaneeyam'):
            st.caption('A reviewed verse-level English meaning is not stored for this unit yet.')
        c1,c2=st.columns(2)
        if c1.button('Ask about this',key='ask_'+r['id'],use_container_width=True):
            st.session_state['_reading_context']=[r]
            st.session_state['_conversation_question']='Explain '+r['reference']+' carefully. Use this exact passage first, then add relevant context from the library. Separate the text from interpretation.'
            st.session_state.page='Converse';st.rerun()
        if wid in ('vishnu','lalita','narayaneeyam','gita','gita-besant'):
            if c2.button('Learn / chant',key='learn_'+r['id'],use_container_width=True):
                st.session_state.learning_course=wid;st.session_state.page='Learn & chant';st.rerun()


def reader_ui(default_id=None,allowed_ids=None,locked_id=None):
    W=works();lookup={w['id']:w for w in W};ids=[w['id'] for w in W if not allowed_ids or w['id'] in allowed_ids]
    if not ids:st.info('No reader-ready collections are available.');return
    preferred=locked_id if locked_id in ids else default_id if default_id in ids else 'bhagavatam' if 'bhagavatam' in ids else ids[0]
    wid=locked_id if locked_id in ids else st.selectbox('Choose a scripture',ids,index=ids.index(preferred),format_func=lambda i:lookup[i]['title'])
    work=lookup[wid]
    st.markdown(f'''<div class="tv-reader-hero"><div class="tv-kicker">{work.get('language','SCRIPTURE')}</div><h2>{work['title']}</h2><p>{BOOK_INTROS.get(wid,'Read slowly. Notice who is speaking, what happens and what the passage is trying to teach.')}</p></div>''',unsafe_allow_html=True)
    rows=passages(wid)
    if not rows:st.warning('This collection has no stored reading units.');return
    sections=sorted({r['section'] for r in rows})
    def section_label(s):
        first=next(r for r in rows if r['section']==s);title=_meta(first).get('readingTitle')
        return title or ('Main text' if not s else str(s))
    nav1,nav2=st.columns(2)
    section=nav1.selectbox('Canto / book / section',sections,format_func=section_label)
    chapters=sorted({r['chapter'] for r in rows if r['section']==section})
    def label(ch):
        if wid in ('gita','gita-besant') and 1<=ch<=len(GITA):return f'{ch}. {GITA[ch-1][0]}'
        first=next(r for r in rows if r['section']==section and r['chapter']==ch);heading=_meta(first).get('readingTitle')
        if heading:return f'{ch}. {heading}'
        stories=story_for(wid,section,ch);title=stories[0]['title'] if stories else ''
        return f'Chapter {ch}'+(' · '+title if title else '')
    chapter=nav2.selectbox('Chapter / reading',chapters,format_func=label)
    selected=[r for r in rows if r['section']==section and r['chapter']==chapter]
    original='\n\n'.join(r['original'] for r in selected)
    st.session_state['_last_reading']={'work':wid,'section':section,'chapter':chapter,'title':work['title'],'label':label(chapter)}

    read_tab,understand_tab,context_tab=st.tabs(['📖 Read','💡 Understand','💬 Ask & reflect'])
    with read_tab:
        if work.get('language')=='English':
            for r in selected:
                with st.container(border=True):st.markdown(r['original'])
            st.caption('Attributed historical translation · '+work.get('edition',''))
        else:
            for r in selected:_verse_card(r,wid)
        with st.expander('Edition & provenance'):
            st.write('**Source:** '+work.get('sourceName','Not recorded'))
            st.write('**Edition:** '+work.get('edition','Not recorded'))
            st.write('**Coverage:** '+work.get('coverage','Not recorded'))
            st.write(work.get('note',''))

    with understand_tab:
        available=False
        if wid in ('gita','gita-besant') and 1<=chapter<=18:
            title,body,action,ref,situation=GITA[chapter-1];st.markdown(body);st.info('Reflect on this: '+action);st.caption('Plain-language Tattvika chapter guide · focus passage: Bhagavad Gita '+ref);available=True
        elif wid in ('shiva','shiva-complete'):
            legacy=(section,chapter) if wid=='shiva' else (1,chapter) if section==100 else None
            if legacy in SHIVA_READINGS:
                title,body=SHIVA_READINGS[legacy];st.markdown(body);st.caption('Prepared explanation based on the stored source · awaiting specialist review');available=True
        stories=story_for(wid,section,chapter)
        for s in stories:
            st.markdown('#### Story lens · '+s['title']);st.markdown(s['text']);st.info('Reflect: '+s['reflection']);st.caption('Prepared retelling · '+s['book']+' '+s['ref']);available=True
        cache_id='reading-v4:'+hashlib.sha256((wid+str(section)+str(chapter)+original).encode()).hexdigest()
        cached=STORE.cached(cache_id)
        if cached:
            st.markdown(cached['body']);st.caption('AI-assisted Tattvika explanation · '+cached['provider']+' · study aid, not traditional commentary')
        elif not available:st.info('A plain-language explanation has not yet been prepared for this reading.')
        if not cached and work.get('language')!='English':
            if st.button('Prepare and save an in-app explanation',key='explain_'+cache_id,type='primary'):
                try:
                    with st.spinner('Preparing this explanation from the stored source…'):prepare_explanation(cache_id,work['title']+' '+str(section)+'.'+str(chapter),original)
                    st.rerun()
                except ProviderError as e:st.error(str(e))

    with context_tab:
        st.write('Keep this chapter open as evidence while you ask a question or reflect on a real-life situation.')
        a,b=st.columns(2)
        if a.button('Ask Tattvika about this reading',type='primary',use_container_width=True):
            st.session_state['_reading_context']=selected
            st.session_state['_conversation_question']='Help me understand '+selected[0]['reference']+'. Explain its meaning and context using this passage, and distinguish source text from interpretation.'
            st.session_state.page='Converse';st.rerun()
        if b.button('Reflect on its relevance to life',use_container_width=True):
            st.session_state['_reading_context']=selected
            st.session_state['_conversation_question']='I want to reflect on how the teaching in '+selected[0]['reference']+' may apply to a situation in my life. Explain the source first, then help me think through the situation.'
            st.session_state.page='Converse';st.rerun()
