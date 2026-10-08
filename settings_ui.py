import os
import streamlit as st
from study_store import StudyStore
from providers import CONFIG
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
 provider=st.session_state.get('_primary',saved('primary','OpenRouter'))
 config=saved('provider:'+provider,{})
 key=st.session_state.get('_keys',{}).get(provider) or configured_key(provider)
 model=st.session_state.get('_models',{}).get(provider) or config.get('model') or CONFIG[provider][1]
 out=[(provider,key,model)]
 fallback=st.session_state.get('_fallback',saved('fallback','None'))
 if fallback in CONFIG and fallback!=provider:
  conf=saved('provider:'+fallback,{})
  key=st.session_state.get('_keys',{}).get(fallback) or configured_key(fallback)
  if key:out.append((fallback,key,conf.get('model',CONFIG[fallback][1])))
 return out
def settings_ui():
 st.header('Conversation & teaching settings')
 st.write('Set up one provider for questions and new chapter explanations. Saved readings are reused, so opening them again does not make another AI call.')
 provider=st.selectbox('Provider',list(CONFIG),key='settings_provider')
 configured=bool(configured_key(provider))
 if configured:st.success('A saved or hosting key is available for '+provider+'. The key is not displayed.')
 key=st.text_input('New API key',type='password',key='new_key_'+provider)
 model=st.text_input('Model',value=saved('provider:'+provider,{}).get('model',CONFIG[provider][1]),key='model_config_'+provider)
 fallback=st.selectbox('Fallback provider',['None']+[p for p in CONFIG if p!=provider])
 if st.button('Use these settings for this visit'):
  st.session_state['_primary']=provider;st.session_state['_fallback']=fallback
  st.session_state.setdefault('_keys',{})[provider]=key or configured_key(provider)
  st.session_state.setdefault('_models',{})[provider]=model;st.success('Ready for this visit.')
 if st.button('Save settings securely',disabled=not st.session_state.get('_profile')):
  effective=key or configured_key(provider)
  if not effective:st.error('Enter a key before saving.')
  else:
   save('provider:'+provider,{'key':effective,'model':model});save('primary',provider);save('fallback',fallback)
   st.session_state.update({'_primary':provider,'_fallback':fallback});st.session_state.setdefault('_keys',{})[provider]=effective;st.session_state.setdefault('_models',{})[provider]=model;st.success('Saved. Open the same profile on a later visit to use this key again.')
 if st.button('Forget saved '+provider+' key',disabled=not st.session_state.get('_profile')):
  STORE.forget(st.session_state['_profile'],'provider:'+provider);st.session_state.get('_keys',{}).pop(provider,None);st.success('Saved key removed.')
 st.caption('Hosting keys stay private on the server. A profile passphrase is needed to unlock personal saved keys; forgetting the passphrase means the encrypted keys cannot be recovered.')
