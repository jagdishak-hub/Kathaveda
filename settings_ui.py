import os
import streamlit as st
from study_store import StudyStore
from providers import CONFIG,request,ProviderError
STORE=StudyStore()
def profile_ui():
 with st.sidebar.expander('My study profile',expanded=not bool(st.session_state.get('_profile'))):
  if st.session_state.get('_profile'):
   st.success('Profile open: '+st.session_state['_profile'])
   if st.button('Lock my profile'):
    for k in list(st.session_state):
     if k.startswith(('_cipher','_profile','key_','fallback_key_','new_key_')) or k in ('_keys','_models','_primary','_fallback','history','pending_question','_reading_context'):del st.session_state[k]
    st.rerun()
  else:
   with st.form('profile_login'):
    name=st.text_input('Profile name');password=st.text_input('Private passphrase',type='password');create=st.checkbox('Create a new profile')
    submitted=st.form_submit_button('Open profile')
   if submitted:
    try:
     name,cipher=STORE.unlock(name,password,create);st.session_state.update({'_profile':name,'_cipher':cipher});st.rerun()
    except ValueError as e:st.error(str(e))
   st.caption('Use a passphrase of at least 10 characters. Your saved API keys are encrypted. You can browse and play without opening a profile.')
def saved(name,default=None):
 if st.session_state.get('_profile'):return STORE.get(st.session_state['_profile'],st.session_state['_cipher'],name,default)
 return default
def save(name,value):
 if not st.session_state.get('_profile'):raise ValueError('Open a private study profile first to save across visits.')
 STORE.save(st.session_state['_profile'],st.session_state['_cipher'],name,value)
def configured_key(provider):
 try:secret=str(st.secrets.get('KATHAVEDA_'+provider.upper()+'_API_KEY',''))
 except (FileNotFoundError,KeyError):secret=''
 return os.environ.get('KATHAVEDA_'+provider.upper()+'_API_KEY','') or secret or saved('provider:'+provider,{}).get('key','')
def active_settings():
 primary=st.session_state.get('_primary',saved('primary','OpenRouter'))
 order=[primary]+[p for p in CONFIG if p!=primary]
 out=[]
 for provider in order:
  conf=saved('provider:'+provider,{})
  key=st.session_state.get('_keys',{}).get(provider) or configured_key(provider)
  model=st.session_state.get('_models',{}).get(provider) or conf.get('model') or CONFIG[provider][1]
  if key:out.append((provider,key,model))
 return out or [(primary,'',CONFIG[primary][1])]
def settings_ui():
 st.header('Connect your AI providers')
 st.write('Enter all the keys you want to use. Your preferred provider answers first. If it fails, the others are tried one at a time. A successful answer stops further calls.')
 if not st.session_state.get('_profile'):st.info('Open a study profile in the sidebar to save keys across visits. You can also use keys just for this visit.')
 with st.form('all_provider_keys'):
  current=st.session_state.get('_primary',saved('primary','OpenRouter'))
  primary=st.selectbox('Preferred provider',list(CONFIG),index=list(CONFIG).index(current))
  typed={};models={}
  for provider in CONFIG:
   st.subheader(provider)
   if configured_key(provider):st.caption('A saved key is connected. Leave the field empty to keep it.')
   typed[provider]=st.text_input(provider+' API key',type='password',key='new_key_'+provider)
   models[provider]=st.text_input(provider+' model',value=saved('provider:'+provider,{}).get('model',CONFIG[provider][1]))
  visit=st.form_submit_button('Use all keys for this visit')
  persist=st.form_submit_button('Save all keys securely',disabled=not st.session_state.get('_profile'))
 if visit or persist:
  st.session_state['_primary']=primary
  for provider in CONFIG:
   key=typed[provider] or st.session_state.get('_keys',{}).get(provider) or configured_key(provider)
   if key:
    st.session_state.setdefault('_keys',{})[provider]=key
    st.session_state.setdefault('_models',{})[provider]=models[provider]
    if persist:save('provider:'+provider,{'key':key,'model':models[provider]})
  if persist:save('primary',primary)
  count=len([x for x in active_settings() if x[1]])
  st.success(f'{count} providers connected. '+('All keys saved. Reopen this profile next time.' if persist else 'Ready for this visit.'))
 st.caption('Fallback order: '+ ' → '.join(s[0] for s in active_settings() if s[1]))
 connected=[s for s in active_settings() if s[1]]
 if connected:
  with st.expander('Check my connected providers'):
   st.write('This sends one tiny test request to each connected provider. It may use a small amount of your provider quota.')
   if st.button('Run connection check'):
    st.session_state['_provider_checks']={}
    for provider,key,model in connected:
     try:
      with st.spinner('Checking '+provider+'…'):request(provider,key,model,[{'role':'user','content':'Reply with exactly: READY'}])
      st.session_state['_provider_checks'][provider]='Connected · '+model
     except ProviderError as e:st.session_state['_provider_checks'][provider]=str(e)
  for provider,result in st.session_state.get('_provider_checks',{}).items():
   (st.success if result.startswith('Connected') else st.error)(provider+' · '+result)
 with st.expander('Remove a saved provider key'):
  provider=st.selectbox('Provider to disconnect',list(CONFIG))
  if st.button('Remove this saved key',disabled=not st.session_state.get('_profile')):
   STORE.forget(st.session_state['_profile'],'provider:'+provider);st.session_state.get('_keys',{}).pop(provider,None);st.success('Saved key removed.')
 st.caption('Keys are encrypted using your profile passphrase. Hosting keys stay private on the server. Never put keys into a conversation message.')
