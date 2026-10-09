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

def reader_ui(default_id=None,allowed_ids=None,locked_id=None):
 st.header('Reading room · understand a scripture')
 W=works();lookup={w['id']:w for w in W};ids=[w['id'] for w in W if not allowed_ids or w['id'] in allowed_ids]
 preferred=locked_id if locked_id in ids else default_id if default_id in ids else 'bhagavatam' if 'bhagavatam' in ids else ids[0]
 if locked_id in ids:
  wid=locked_id
 else:
  wid=st.selectbox('Choose a scripture',ids,index=ids.index(preferred),format_func=lambda i:lookup[i]['title'])
 work=lookup[wid];st.subheader(work['title']);st.write(BOOK_INTROS.get(wid,'Read this work a little at a time. Follow who is speaking, what happens and what the passage teaches.'))
 with st.expander('What is available in this edition?'):st.write(work['coverage']);st.write(work['note'])
 rows=passages(wid);sections=sorted({r['section'] for r in rows})
 def section_label(s):
  first=next(r for r in rows if r['section']==s)
  title=json.loads(first['metadata']).get('readingTitle')
  return title or ('Main text' if not s else str(s))
 section=st.selectbox('Canto / book / section',sections,format_func=section_label)
 chapters=sorted({r['chapter'] for r in rows if r['section']==section})
 def label(ch):
  if wid in ('gita','gita-besant'):return f'{ch}. {GITA[ch-1][0]}'
  first=next(r for r in rows if r['section']==section and r['chapter']==ch)
  heading=json.loads(first['metadata']).get('readingTitle')
  if heading:return f'{ch}. {heading}'
  stories=story_for(wid,section,ch)
  title=stories[0]['title'] if stories else SHIVA_READINGS.get((section,ch),('',''))[0] if wid=='shiva' else ''
  return f'Chapter {ch}'+(' · '+title if title else '')
 default=chapters.index(5) if wid=='bhagavatam' and section==1 and 5 in chapters else chapters.index(26) if wid=='narayaneeyam' and 26 in chapters else 0
 chapter=st.selectbox('Open a chapter',chapters,index=default,format_func=label)
 selected=[r for r in rows if r['section']==section and r['chapter']==chapter];original='\n\n'.join(r['original'] for r in selected)
 st.subheader(label(chapter));st.caption('Read here in The Reading Room. You do not need to open another website.')
 available=False
 if wid in ('gita','gita-besant'):
  title,body,action,ref,situation=GITA[chapter-1];st.markdown(body);st.info('Try this: '+action);st.caption('Plain-language chapter guide · focus passage: Bhagavad Gita '+ref);available=True
 elif wid in ('shiva','shiva-complete'):
  legacy=(section,chapter) if wid=='shiva' else (1,chapter) if section==100 else None
  if legacy in SHIVA_READINGS:
   title,body=SHIVA_READINGS[legacy];st.markdown(body);st.caption('Prepared explanation based on the opening Shiva Purana chapter · awaiting specialist review');available=True
 stories=story_for(wid,section,chapter)
 for s in stories:
  st.markdown(s['text']);st.info('Think about this: '+s['reflection']);st.caption('Prepared retelling · '+s['book']+' '+s['ref']+' · awaiting specialist review');available=True
 cache_id='reading-v2:'+hashlib.sha256((wid+str(section)+str(chapter)+original).encode()).hexdigest()
 if wid=='gita-besant':
  for r in selected:
   meta=json.loads(r['metadata']);st.markdown('**Verse '+str(r['verse'])+'**');st.write(meta.get('meaning',''));st.caption('Annie Besant · 1922 historical translation')
 english=work.get('language')=='English'
 if english:
  for r in selected:st.markdown(r['original'])
  st.caption('Attributed historical translation · '+work['edition']);available=True
 cached=STORE.cached(cache_id)
 if cached:
  with st.expander('Saved plain-language explanation',expanded=not available):st.markdown(cached['body']);st.caption('AI-assisted explanation · '+cached['provider']+' · not independently reviewed')
 elif not available:st.info('The original chapter is stored. Its English explanation has not been prepared yet. Prepare it once below; it will then be saved for later readers.')
 if st.button('Prepare and save a simple chapter explanation',disabled=bool(cached) or english):
  try:
   with st.spinner('Preparing this chapter from its source text…'):prepare_explanation(cache_id,work['title']+' '+str(section)+'.'+str(chapter),original)
   st.rerun()
  except ProviderError as e:st.error(str(e))
 with st.expander('Read the original scripture text',expanded=True):
  for r in selected:
   st.markdown('**'+r['reference']+'**');st.text(r['original'])
   meta=json.loads(r['metadata']);meaning=meta.get('meaning')
   if meaning and not meaning.startswith('An editorially reviewed'):
    st.info(meaning)
  st.write('Source: '+work['sourceName']);st.write('Edition: '+work['edition']);st.code(selected[0]['source_url'],language=None)
 if st.button('Discuss this chapter'):
  st.session_state['_reading_context']=selected;st.session_state['_conversation_question']='Help me apply the teaching in '+selected[0]['reference']+' to a situation I am facing.';st.success('Chapter selected. Open Converse to describe your situation.')
