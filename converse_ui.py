import streamlit as st
from knowledge import CONTENT,search,passages
from settings_ui import active_settings
from providers import discuss,ProviderError


def converse_ui():
    st.markdown('''<div class="tv-section-hero"><div class="tv-kicker">ASK TATTVIKA</div>
    <h2>Ask the library, not a generic chatbot.</h2>
    <p>Questions are grounded in stored passages. Tattvika keeps the textual evidence visible and separates it from interpretation.</p></div>''',unsafe_allow_html=True)
    settings=active_settings();connected=[s[0] for s in settings if s[1]]
    if connected:st.success('Ready · fallback order: '+' → '.join(connected))
    else:st.info('Prepared local answers still work. Connect an AI provider in Settings for new open-ended questions.')

    mode=st.segmented_control('Mode',['Textual','Reflective','Compare'],default='Textual')
    starters={
      'Textual':['Help me understand Bhagavad Gita 2.47.','What is Narayaneeyam?','What does this Vishnu Sahasranama name mean?'],
      'Reflective':['I am jealous of someone more successful than me.','I feel overwhelmed by my responsibilities.','How should I think about failure?'],
      'Compare':['Compare action in the Gita and Upanishadic thought.','Compare devotion in the Bhagavatam and Narayaneeyam.','How do different texts speak about anger?']}
    cols=st.columns(3)
    for i,prompt in enumerate(starters[mode]):
        if cols[i].button(prompt,key='starter_'+mode+str(i),use_container_width=True):
            st.session_state.pending_question=prompt;st.rerun()

    if 'history' not in st.session_state:st.session_state['history']=[]
    if st.session_state.get('_conversation_question'):
        st.session_state['pending_question']=st.session_state.pop('_conversation_question')

    for m in st.session_state['history']:
        with st.chat_message(m['role']):st.markdown(m['content'])

    question=st.text_area('Your question',key='pending_question',placeholder='Ask about a verse, story, divine name, teaching, comparison or a real-life situation…')
    if st.button('Ask Tattvika',type='primary',use_container_width=True,disabled=not question.strip()):
        prepared=next((a for a in CONTENT['corpus']['corpusAnswers'] if a['question']==question.lower().strip().rstrip('?!.') and not a['id'].startswith('guidance-')),None)
        context=search(question,limit=10)
        if st.session_state.get('_reading_context'):
            context=st.session_state['_reading_context']+context
        gid=st.session_state.get('conversation_context')
        if gid:
            guidance=next((g for g in CONTENT['guidance']['guidance'] if g['id']==gid),None)
            if guidance:
                context=[r for r in passages('gita') if r['reference'].removeprefix('Bhagavad Gita ') in guidance['gita']]+context
        # de-duplicate while preserving passage objects
        seen=set();dedup=[]
        for r in context:
            if r['id'] not in seen:seen.add(r['id']);dedup.append(r)
        context=dedup[:10]
        try:
            if prepared:answer,used=prepared['answer'],'prepared local answer'
            else:
                prefix={'Textual':'Answer as a textual question.','Reflective':'First address the human situation practically, then use scripture as perspective.','Compare':'Actively compare similarities, differences and context across the retrieved texts.'}[mode]
                q=prefix+' '+question
                with st.spinner('Searching the library and reasoning from the retrieved passages…'):
                    answer,used=discuss(q,context,st.session_state['history'],settings)
            st.session_state['history'] += [{'role':'user','content':question},{'role':'assistant','content':answer}]
            st.rerun()
        except ProviderError as e:st.error(str(e))

    if st.session_state['history']:
        # Re-retrieve for the most recent user question so evidence stays visible after rerun.
        lastq=next((m['content'] for m in reversed(st.session_state['history']) if m['role']=='user'),None)
        if lastq:
            context=search(lastq,limit=8)
            if st.session_state.get('_reading_context'):context=st.session_state['_reading_context']+context
            if context:
                with st.expander('Evidence from the library',expanded=True):
                    seen=set()
                    for r in context:
                        if r['id'] in seen:continue
                        seen.add(r['id'])
                        st.markdown('**'+r['reference']+'**')
                        text=' '.join((r.get('original') or '').split())
                        st.write(text[:700]+('…' if len(text)>700 else ''))
                        if len(seen)>=8:break
                st.caption('Source links and edition details remain under Sources; Converse keeps the reading experience inside Tattvika.')
    c1,c2=st.columns(2)
    if c1.button('Clear conversation',use_container_width=True):
        st.session_state['history']=[];st.session_state.pop('pending_question',None);st.rerun()
    if c2.button('Clear passage context',use_container_width=True):
        st.session_state.pop('_reading_context',None);st.success('Passage context cleared.')
