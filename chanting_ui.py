import hashlib,json
import streamlit as st
from settings_ui import STORE,active_settings
from providers import request,ProviderError

# Trusted external references for meaning/commentary. These are deliberately
# separate from the stored source transcription so Tattvika never blurs the
# difference between scripture, a historical/reference meaning, and its own
# explanatory study aid.
REFERENCE_MEANINGS={
 'vishnu':{
  'label':'Vishnu Sahasranama meaning resources · Sanskrit Documents',
  'url':'https://sanskritdocuments.org/sanskrit/vishhnu/',
  'note':'The Sanskrit Documents index links several independent meaning/commentary resources for the Mahabharata Vishnu Sahasranama.'
 },
 'lalita':{
  'label':'Lalita Sahasranamavali · name-by-name meanings · Sanskrit Documents',
  'url':'https://sanskritdocuments.org/doc_devii/lalita1000.html',
  'note':'This attributed reference presents all 1000 names in name-by-name format with brief English meanings.'
 }
}

def _existing_meaning(r):
 try:meta=json.loads(r.get('metadata') or '{}')
 except (TypeError,ValueError):meta={}
 meaning=(meta.get('meaning') or '').strip()
 if not meaning or meaning.startswith('An editorially reviewed'):return None,None
 label='Historical translation' if r.get('work_id')=='gita-besant' else 'Stored explanatory meaning'
 return label,meaning

def _prompt(title,r):
 original=r.get('original','')
 translit=r.get('transliteration','')
 return f'''You are preparing a careful study aid for a Hindu chanting text.

Work: {title}
Reference: {r.get('reference','')}
Original text:
{original}

Transliteration, if available:
{translit}

Give a concise, useful explanation using EXACTLY these headings:

### Important words or names
For each important Sanskrit word/name that you can interpret reliably, give the word and a short English meaning. Do not invent an etymology. If a compound or divine name has more than one standard interpretation, say that briefly.

### Overall meaning
Give the sense of the complete verse/reading unit in clear English. Do not pretend this is a literal translation unless the wording supports that.

### Devotional significance
Explain the traditional devotional or theological idea conveyed by the verse. Clearly frame it as a traditional interpretation where appropriate.

### A simple way to remember it
Give one short memory cue that helps a learner connect the meaning to the chant.

### Caution / context
Mention uncertainty, context, or multiple interpretations if relevant. Do not invent a story, claim, quotation, benefit, ritual rule, or source that is not in the supplied text.

This is an AI-assisted study explanation, NOT scripture and NOT a traditional commentary. Keep it under 450 words.'''

def prepared_meaning(r,title):
 key='chant-meaning-v2:'+hashlib.sha256((r.get('id','')+r.get('reference','')+r.get('original','')).encode()).hexdigest()
 cached=STORE.cached(key)
 if cached:return cached
 settings=active_settings();errors=[]
 if not any(s[1] for s in settings):
  raise ProviderError('Connect an online provider in Settings once to prepare a structured meaning. After preparation it is saved and can be reopened without another AI call.')
 for provider,key_value,model in settings:
  if not key_value:continue
  try:
   answer=request(provider,key_value,model,[{'role':'user','content':_prompt(title,r)}])
   STORE.cache(key,answer,provider)
   return {'body':answer,'provider':provider}
  except ProviderError as e:errors.append(provider+': '+str(e))
 raise ProviderError('\n'.join(errors))

def cached_meaning(r):
 key='chant-meaning-v2:'+hashlib.sha256((r.get('id','')+r.get('reference','')+r.get('original','')).encode()).hexdigest()
 return STORE.cached(key)

def chanting_study(r,wid,title):
 '''Meaning-first study layer for chanting literature.'''
 stored_label,stored=_existing_meaning(r)
 cached=cached_meaning(r)
 ref=REFERENCE_MEANINGS.get(wid)

 st.markdown('#### Understand what you are chanting')
 if stored:
  st.success(stored_label)
  st.write(stored)
 elif cached:
  st.markdown(cached['body'])
  st.caption('AI-assisted Tattvika study explanation · '+cached['provider']+' · saved for reuse · not a traditional commentary')
 else:
  st.info('A verse-level English meaning has not yet been stored for this unit. You can prepare and save a structured study explanation below.')

 if ref:
  with st.container(border=True):
   st.markdown('**Reference meaning source**')
   st.write(ref['note'])
   st.link_button(ref['label'],ref['url'])

 if not cached:
  if st.button('Prepare and save detailed meaning',key='chant_meaning_'+r['id'],type='primary'):
   try:
    with st.spinner('Preparing the word meanings and verse sense…'):prepared_meaning(r,title)
    st.rerun()
   except ProviderError as e:st.error(str(e))
 else:
  with st.expander('Meaning provenance'):
   st.write('This explanation was generated from the exact stored chanting unit and cached for later use. It is clearly labelled as a study aid so it cannot be confused with the canonical text or with a traditional bhashya/commentary.')

 st.caption('Tattvika keeps four layers separate: source text · transliteration · attributed/reference meaning · Tattvika study explanation.')
