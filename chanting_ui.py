import hashlib,json
import streamlit as st
from settings_ui import STORE,active_settings
from providers import request,ProviderError

# The chanting experience must remain inside Tattvika. External source sites are
# provenance only and belong on the Sources page, never in the learning flow.
REFERENCE_NOTES={
 'vishnu':'Reference meanings/commentaries were consulted during curation. Tattvika keeps the learner inside the app and clearly labels generated explanations as study aids.',
 'lalita':'Name-by-name reference material was consulted during curation. Tattvika keeps the learner inside the app and clearly labels generated explanations as study aids.'
}

def _existing_meaning(r):
 try:meta=json.loads(r.get('metadata') or '{}')
 except (TypeError,ValueError):meta={}
 meaning=(meta.get('meaning') or '').strip()
 if not meaning or meaning.startswith('An editorially reviewed'):return None,None
 label='Historical translation' if r.get('work_id')=='gita-besant' else 'Stored meaning'
 return label,meaning

def _prompt(title,r):
 original=r.get('original','')
 translit=r.get('transliteration','')
 return f'''You are preparing a careful in-app study aid for a Hindu chanting text.

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

This is an AI-assisted Tattvika study explanation, NOT scripture and NOT a traditional commentary. Keep it under 450 words.'''

def _cache_key(r):
 return 'chant-meaning-v2:'+hashlib.sha256((r.get('id','')+r.get('reference','')+r.get('original','')).encode()).hexdigest()

def prepared_meaning(r,title):
 key=_cache_key(r)
 cached=STORE.cached(key)
 if cached:return cached
 settings=active_settings();errors=[]
 if not any(s[1] for s in settings):
  raise ProviderError('A provider is needed only once to prepare this meaning. After preparation, Tattvika stores it and opens it locally without sending you to another website.')
 for provider,key_value,model in settings:
  if not key_value:continue
  try:
   answer=request(provider,key_value,model,[{'role':'user','content':_prompt(title,r)}])
   STORE.cache(key,answer,provider)
   return {'body':answer,'provider':provider}
  except ProviderError as e:errors.append(provider+': '+str(e))
 raise ProviderError('\n'.join(errors))

def cached_meaning(r):
 return STORE.cached(_cache_key(r))

def chanting_study(r,wid,title):
 '''Meaning-first study layer for chanting literature. Nothing here redirects the learner away from Tattvika.'''
 stored_label,stored=_existing_meaning(r)
 cached=cached_meaning(r)

 st.markdown('#### Understand what you are chanting')
 if stored:
  st.success(stored_label)
  st.write(stored)
  if cached:
   with st.expander('Deeper Tattvika study explanation'):
    st.markdown(cached['body'])
    st.caption('AI-assisted study explanation · '+cached['provider']+' · saved inside Tattvika · not a traditional commentary')
 elif cached:
  st.markdown(cached['body'])
  st.caption('AI-assisted Tattvika study explanation · '+cached['provider']+' · saved inside Tattvika · not a traditional commentary')
 else:
  st.info('A complete English meaning is not stored for this unit yet. Prepare it once below; Tattvika will save it here for future study.')

 if not cached:
  if st.button('Prepare and save meaning in Tattvika',key='chant_meaning_'+r['id'],type='primary'):
   try:
    with st.spinner('Preparing the word meanings and verse sense inside Tattvika…'):prepared_meaning(r,title)
    st.rerun()
   except ProviderError as e:st.error(str(e))

 with st.expander('Meaning provenance'):
  if stored:
   st.write('This unit already contains a stored meaning in the Tattvika corpus metadata.')
  if cached:
   st.write('The deeper explanation was generated from this exact stored chanting unit and cached in Tattvika for reuse.')
  if wid in REFERENCE_NOTES:st.write(REFERENCE_NOTES[wid])
  st.write('External source links are intentionally kept out of the learning flow. They remain available only on the Sources page for provenance checking.')

 st.caption('Tattvika keeps these layers separate: source text · transliteration · stored meaning · Tattvika study explanation.')
