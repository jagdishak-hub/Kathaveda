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
 if not any(s[1] for s in settings):raise ProviderError('An online provider is needed to prepare this explanation once. Open Settings to set it up. Previously prepared readings can be opened without another call.')
 prompt='Explain this '+purpose+' in clear, simple English for children and elders. Use short sentences. Explain every Sanskrit term on first use. Do not invent facts, quotes or missing parts. Stay within the supplied text. Distinguish religious beliefs, original narrative and modern application. Use headings: What happens or is said; What it means; One everyday example; A small next step; What needs context. For a verse, also explain important words if you can do so reliably. This is an explanatory guide, not a literal translation. About 600 words maximum. Source reference: '+reference+'\n\nOriginal source text:\n'+original
 if len(original)>100000:raise ProviderError('This chapter needs to be explained in smaller parts. Open its individual reading units first; no incomplete explanation has been saved.')
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
  # The Gajendra retelling gives both references; keep the Bhagavatam part.
  ref=s['ref'].split('Bhagavatam ')[-1]
  m=re.search(r'(\d+)\.(\d+)(?:[–-](\d+))?',ref)
  if m and int(m[1])==section:
   first=int(m[2]);last=int(m[3]) if m[3] else first
   if first<=chapter<=last:out.append(s)
 return out

def reader_ui():
 st.header('Reading room · understand a scripture')
 W=works();lookup={w['id']:w for w in W};ids=[w['id'] for w in W]
 wid=st.selectbox('Choose a scripture',ids,index=ids.index('bhagavatam'),format_func=lambda i:lookup[i]['title'])
 work=lookup[wid];st.subheader(work['title']);st.write(BOOK_INTROS.get(wid,'Read this work a little at a time. Follow who is speaking, what happens and what the passage teaches.'))
 with st.expander('What is available in this edition?'):st.write(work['coverage']);st.write(work['note'])
 rows=passages(wid);sections=sorted({r['section'] for r in rows})
 section=st.selectbox('Canto / book / section',sections,format_func=lambda s:'Main text' if not s else str(s))
 chapters=sorted({r['chapter'] for r in rows if r['section']==section})
 def label(ch):
  if wid=='gita':return f'{ch}. {GITA[ch-1][0]}'
  stories=story_for(wid,section,ch)
  title=stories[0]['title'] if stories else SHIVA_READINGS.get((section,ch),('',''))[0] if wid=='shiva' else ''
  return f'Chapter {ch}'+(' · '+title if title else '')
 default=chapters.index(5) if wid=='bhagavatam' and section==1 and 5 in chapters else chapters.index(26) if wid=='narayaneeyam' and 26 in chapters else 0
 chapter=st.selectbox('Open a chapter',chapters,index=default,format_func=label)
 selected=[r for r in rows if r['section']==section and r['chapter']==chapter];original='\n\n'.join(r['original'] for r in selected)
 st.subheader(label(chapter));st.caption('Read here in KathaVeda. You do not need to open another website.')
 available=False
 if wid=='gita':
  title,body,action,ref,situation=GITA[chapter-1];st.markdown(body);st.info('Try this: '+action);st.caption('Plain-language chapter guide · focus passage: Bhagavad Gita '+ref);available=True
 elif wid=='shiva' and (section,chapter) in SHIVA_READINGS:
  title,body=SHIVA_READINGS[section,chapter];st.markdown(body);st.caption('Original explanatory retelling based on Shiva Purana '+str(section)+'.'+str(chapter)+' · awaiting specialist review');available=True
 stories=story_for(wid,section,chapter)
 for s in stories:
  st.markdown(s['text']);st.info('Think about this: '+s['reflection']);st.caption('Prepared retelling · '+s['book']+' '+s['ref']+' · awaiting specialist review');available=True
 cache_id='reading-v2:'+hashlib.sha256((wid+str(section)+str(chapter)+original).encode()).hexdigest()
 cached=STORE.cached(cache_id)
 if cached:
  with st.expander('Saved plain-language explanation',expanded=not available):st.markdown(cached['body']);st.caption('AI-assisted explanation · '+cached['provider']+' · not independently reviewed')
 elif not available:st.info('The original chapter is stored. Its English explanation has not been prepared yet. Prepare it once below; it will then be saved for later readers.')
 if st.button('Prepare and save a simple chapter explanation',disabled=bool(cached)):
  try:
   with st.spinner('Preparing this chapter from its source text…'):prepare_explanation(cache_id,work['title']+' '+str(section)+'.'+str(chapter),original)
   st.rerun()
  except ProviderError as e:st.error(str(e))
 with st.expander('Original text and source details'):
  for r in selected:
   st.caption(r['reference']);st.text(r['original'])
  st.write('Source: '+work['sourceName']);st.write('Edition: '+work['edition']);st.code(selected[0]['source_url'],language=None)
 if st.button('Discuss this chapter'):
  st.session_state['_reading_context']=selected;st.session_state['_conversation_question']='Help me apply the teaching in '+selected[0]['reference']+' to a situation I am facing.';st.success('Chapter selected. Open Converse to describe your situation.')
