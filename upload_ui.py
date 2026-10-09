"""Private, session-scoped reading workspace for user-supplied scripture files."""
import hashlib,io,re
import streamlit as st
from providers import request,ProviderError
from settings_ui import active_settings

def _extract(upload):
 data=upload.getvalue();name=upload.name.lower()
 if len(data)>15_000_000:raise ValueError('Please upload a file smaller than 15 MB.')
 if name.endswith('.txt'):return data.decode('utf-8','replace')
 if name.endswith('.pdf'):
  from pypdf import PdfReader
  return '\n\n'.join((p.extract_text() or '') for p in PdfReader(io.BytesIO(data)).pages)
 if name.endswith('.docx'):
  from docx import Document
  return '\n'.join(p.text for p in Document(io.BytesIO(data)).paragraphs)
 raise ValueError('Use a UTF-8 text, searchable PDF or DOCX file.')

def _sections(text,limit=9000):
 blocks=[b.strip() for b in re.split(r'\n\s*\n',text) if b.strip()]
 out=[];current=''
 for block in blocks:
  if current and len(current)+len(block)>limit:out.append(current);current=''
  current+=(('\n\n' if current else '')+block)
 if current:out.append(current)
 return out

def upload_ui():
 st.header('Study my text')
 st.write('Bring a scripture or commentary you are allowed to use. Read it privately, choose a passage, and ask for a simple explanation.')
 st.info('Your upload is used only in this browser session. It is not added to the shared scripture library or treated as an authenticated edition.')
 upload=st.file_uploader('Upload a searchable text',type=['txt','pdf','docx'],help='Scanned image-only PDFs need OCR before their text can be studied reliably.')
 if not upload:return
 token=hashlib.sha256(upload.getvalue()).hexdigest()
 if st.session_state.get('_upload_token')!=token:
  try:text=_extract(upload)
  except Exception as e:st.error('This file could not be read: '+str(e));return
  if len(text.strip())<80:st.error('Very little searchable text was found. This may be a scanned PDF that needs OCR.');return
  st.session_state.update({'_upload_token':token,'_upload_text':text,'_upload_sections':_sections(text),'_upload_answers':{}})
 sections=st.session_state['_upload_sections'];st.success(f'{len(st.session_state["_upload_text"]):,} characters found · {len(sections)} study sections')
 index=st.selectbox('Choose a section',range(len(sections)),format_func=lambda i:f'Section {i+1} · {sections[i][:75].replace(chr(10)," ")}…')
 passage=sections[index]
 search=st.text_input('Find within this section',placeholder='Character, Sanskrit word or idea…')
 shown=passage
 if search:
  lines=[x for x in passage.splitlines() if search.casefold() in x.casefold()]
  shown='\n'.join(lines) if lines else 'No matching lines in this section.'
 st.markdown('<div class="rr-long-reader">'+shown.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br>')+'</div>',unsafe_allow_html=True)
 st.subheader('Understand this section')
 purpose=st.selectbox('What help do you need?',['Simple explanation','Story and characters','Important Sanskrit words','Practical teaching','Questions for study'])
 st.caption('The explanation is model-assisted and may be wrong, especially where OCR, sandhi or a rare commentary is involved. Compare it with the original text and a qualified teacher.')
 key=f'{token}:{index}:{purpose}';cached=st.session_state['_upload_answers'].get(key)
 if st.button('Explain selected section',type='primary',disabled=not any(k for _,k,_ in active_settings())):
  prompt=f'''You are assisting with a user-supplied religious text. Explain only what the supplied passage supports. Do not invent verses, speakers, chapter names or translations. Use simple English suitable for children and elders. Separate literal content, traditional interpretation and modern application. If Sanskrit analysis is uncertain, show the uncertainty instead of guessing. Request: {purpose}.\n\nPASSAGE:\n{passage[:18000]}'''
  errors=[]
  for provider,secret,model in active_settings():
   if not secret:continue
   try:
    cached=request(provider,secret,model,[{'role':'user','content':prompt}]);st.session_state['_upload_answers'][key]=cached;break
   except ProviderError as e:errors.append(provider+': '+str(e))
  if not cached:st.error('\n'.join(errors) or 'Connect an AI provider in Profile first.')
 if cached:st.markdown(cached)
 if not any(k for _,k,_ in active_settings()):st.warning('Connect at least one provider in Profile to prepare a new explanation. Reading and searching the uploaded text works without AI.')
