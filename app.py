import csv,io,json,random,os,base64
from pathlib import Path
import streamlit as st
from knowledge import CONTENT,works,passages,search,audit
from providers import CONFIG,discuss,ProviderError
from reader_ui import prepare_explanation
from friendly_ui import reading_room,situations_ui,STORIES
from games_ui import games_ui
from settings_ui import profile_ui,settings_ui,active_settings,saved,save
from chapter_guides import GITA
ROOT=Path(__file__).parent
st.set_page_config(page_title='The Reading Room · Learn and live',page_icon='🪷',layout='wide')
st.markdown('''<style>
.stApp{background:radial-gradient(circle at 85% 6%,#fff9c9 0 3%,transparent 3.2%),linear-gradient(145deg,#f8fff1 0%,#eaf7e7 52%,#f7f1df 100%);background-attachment:fixed}h1,h2,h3{color:#285c3a;font-family:Georgia,serif}p{line-height:1.65}div[data-testid="stVerticalBlockBorderWrapper"]{background:#ffffffe8;border-radius:20px;border:1px solid #c9dfc5;padding:5px;box-shadow:0 8px 26px #285c3a0d}.block-container{max-width:1280px;padding-top:2rem}h3{font-size:1.2rem!important}button{border-radius:999px!important}section[data-testid="stSidebar"],div[data-testid="stSidebar"]{background:linear-gradient(180deg,#eaf6e4 0%,#dcefdc 58%,#f5edda 100%)!important;border-right:1px solid #b7d0ae}div[data-testid="stSidebar"] img{display:block;margin:4px auto 0;filter:drop-shadow(0 7px 12px #294a2a25)}div[data-testid="stSidebar"] button{border:1px solid #bad1b4!important;text-align:left!important;justify-content:flex-start!important;padding:.55rem .75rem!important;min-height:2.55rem;background:#ffffffd9!important;color:#294b35!important;box-shadow:0 2px 7px #274d310d}div[data-testid="stSidebar"] button p{color:inherit!important}div[data-testid="stSidebar"] button:hover{background:#f7fff3!important;border-color:#6fa477!important;transform:translateX(2px)}div[data-testid="stSidebar"] button[kind="primary"]{background:linear-gradient(90deg,#34764b,#5c934f)!important;border-color:transparent!important;color:#fff!important;box-shadow:0 5px 14px #274b303d;font-weight:700}.rr-side-name{text-align:center;color:#264c32!important;font-family:Georgia,serif;font-weight:800;letter-spacing:.08em;font-size:1.05rem;margin-top:4px}.rr-side-line{text-align:center;color:#57745d!important;font-size:.78rem;margin:2px 0 12px}.rr-side-group{font-size:.67rem;letter-spacing:.16em;color:#3e6c48!important;margin:18px 4px 6px;font-weight:800}.rr-study-card{background:#f9fff5cc;border:1px solid #bdd4b7;color:#294b35!important;padding:12px;border-radius:14px;font-size:.82rem;line-height:1.45}.rr-study-card b{color:#274f34!important}.rr-study-card span{color:#57705d!important}.rr-study-card hr{border:0;border-top:1px solid #c7d9c2;margin:9px 0}.rr-long-reader{max-width:820px;margin:18px auto;padding:28px 34px;background:#fffef8;border:1px solid #d9ddc6;border-radius:18px;box-shadow:0 10px 30px #31573510;color:#2d332c;line-height:1.8;font-family:Georgia,serif}.rr-long-reader p{margin:0 0 1.15em}div[data-testid="stMetric"]{background:#fffceb;padding:16px;border-radius:16px}.rr-garden{padding:12px 18px;border-radius:18px;background:linear-gradient(90deg,#dff1d7,#fff6cd);border:1px solid #b9d0a9;color:#31543a;margin:8px 0 18px}.rr-game-map{padding:12px;border-radius:16px;background:#f4fae9;border:1px dashed #7ea36f;letter-spacing:.12em;text-align:center}.stProgress>div>div{background:linear-gradient(90deg,#4e8c55,#d3a741)!important}@media(prefers-reduced-motion:no-preference){h1{animation:arrive .6s ease-out}.rr-garden{animation:breathe 4s ease-in-out infinite alternate}@keyframes arrive{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}@keyframes breathe{to{box-shadow:0 7px 28px #6b9a6030}}}</style>''',unsafe_allow_html=True)
logo_data=base64.b64encode((ROOT/'assets/logo.svg').read_bytes()).decode()
st.sidebar.markdown(f'<div style="display:flex;justify-content:center;align-items:center;width:100%;padding:2px 0 0"><img alt="The Reading Room logo" src="data:image/svg+xml;base64,{logo_data}" style="display:block;width:112px;height:auto;margin:0 auto"></div>',unsafe_allow_html=True)
from ambience import ambience_ui
with st.sidebar:ambience_ui()
st.title('The Reading Room')
st.caption('Read a story. Learn a verse. Find a helpful next step.')
from navigation import sidebar_navigation
page=sidebar_navigation()
# Profiles are optional; keep account setup out of the reading flow.
if page=='Settings':profile_ui()
elif st.session_state.get('_profile'):st.sidebar.caption('Study profile: '+st.session_state['_profile'])
family=False
W=works();titles={w['id']:w['title'] for w in W}
G=CONTENT['guidance']['guidance'];S=STORIES
journal=st.session_state.setdefault('_journal',{})
for k,v in list(st.session_state.items()):
 if k.startswith(('reflection_','nextstep_')) or any(k.startswith(g['id']+'_') for g in G):journal[k]=v
for k,v in journal.items():
 if k not in st.session_state:st.session_state[k]=v
def source(r):
 st.caption(r['reference']);st.link_button('Read source',r.get('source_url',r.get('sourceUrl','https://sa.wikisource.org')))
def render_passage(r):
 st.markdown('### '+r['reference']);st.text(r['original'])
 if r.get('transliteration') and r['transliteration']!=r['original']:
  with st.expander('IAST transliteration'):st.text(r['transliteration'])
 meta=json.loads(r['metadata']);meaning=meta.get('meaning')
 if meaning and not meaning.startswith('An editorially reviewed'):st.info(('Historical translation: ' if r['work_id']=='gita-besant' else 'Explanatory paraphrase: ')+meaning)
 else:st.caption('A reviewed English meaning is not available for this passage.')
 st.caption(meta.get('reviewStatus','Source transcription; not independently collated'));source(r)

if page=='Home':
 from home_ui import home_ui
 home_ui()

elif page=='Coverage & sources':
 st.header('What is actually available?')
 st.warning('The full set of Puranas is not complete. These are attributed electronic transcriptions, not independently verified critical editions. A title in the catalogue does not mean every part is present.')
 report=audit();st.dataframe(report,hide_index=True,width='stretch')
 output=io.StringIO();writer=csv.DictWriter(output,fieldnames=report[0].keys());writer.writeheader();writer.writerows(report)
 st.download_button('Download coverage report',output.getvalue(),'kathaveda-coverage.csv','text/csv')
 st.caption('Internal numbering gaps only compare the smallest and largest stored numbers. Entire absent books and missing chapters after the last stored number must be checked against the edition inventory.')
 for w in W:
  with st.expander(w['title']+' · edition and rights'):
   for label,key in [('Edition','edition'),('Coverage','coverage'),('Source','sourceName'),('Rights','rights'),('Review','note')]:st.write('**'+label+'**: '+w.get(key,'Not recorded'))
   st.link_button('Source edition',w['sourceUrl'])

elif page=='Reading room':
 reading_room()

elif page=='Story garden':
 st.header('Take time with a story')
 themes=sorted({t for s in S for t in s['themes']});theme=st.selectbox('Theme',['All']+themes)
 choices=[s for s in S if theme=='All' or theme in s['themes']]
 sid=st.selectbox('Choose a story',[s['id'] for s in choices],format_func=lambda i:next(s['title'] for s in choices if s['id']==i))
 s=next(s for s in S if s['id']==sid);st.subheader(s['title']);st.caption(s['book']+' '+s['ref']+' · prepared retelling, awaiting scholarly review')
 st.markdown(s['child'] if family else s['text']);st.info(s['reflection']);st.link_button('Compare with source chapters',s['url'])
 st.text_area('A family conversation or personal reflection',key='reflection_'+sid)

elif page=='Situations':
 situations_ui()

elif page=='Learn & chant':
 st.header('Learn a little, return often')
 courses=[i for i in ['gita','gita-besant','vishnu','lalita','narayaneeyam'] if i in titles]
 wid=st.selectbox('Course',courses,format_func=lambda i:titles[i],key='learning_course');units=passages(wid)
 position_key='position_'+wid
 if position_key not in st.session_state:st.session_state[position_key]=min(saved('chant-progress',{}).get(position_key,0),len(units)-1)
 def move(delta):st.session_state[position_key]=max(0,min(len(units)-1,st.session_state[position_key]+delta))
 if 'unit_'+wid not in st.session_state:st.session_state['unit_'+wid]=st.session_state[position_key]+1
 idx=st.number_input('Current reading unit',1,len(units),key='unit_'+wid)
 if idx-1!=st.session_state[position_key]:st.session_state[position_key]=idx-1
 r=units[st.session_state[position_key]];st.progress((idx-1)/len(units));st.caption(f'{idx} of {len(units)} · {r["reference"]}')
 st.write('1. Recall the previous unit. 2. Read one line of this unit slowly. 3. Try it from memory. 4. Join the lines, then review both units together.')
 reveal=st.toggle('Show text while practising',value=True)
 if reveal:render_passage(r)
 else:st.info('Try from memory, then reveal the text to compare.')
 from pronunciation_ui import pronunciation_ui
 pronunciation_ui(r)
 def advance():
  st.session_state['practised_'+r['id']]=True;move(1);st.session_state['unit_'+wid]=st.session_state[position_key]+1
 a,b=st.columns(2)
 a.button('Previous unit',on_click=lambda:(move(-1),st.session_state.update({'unit_'+wid:st.session_state[position_key]+1})),disabled=idx==1)
 b.button('Practised · learn next',on_click=advance,disabled=idx==len(units))
 if st.session_state.get('_profile') and st.button('Save learning progress to my profile'):
  save('chant-progress',{k:v for k,v in st.session_state.items() if k.startswith(('position_','practised_'))});st.success('Progress saved.')
 st.caption('Use the same profile to save progress across visits. Narayaneeyam is grouped by dasakam. Recorded pronunciation is still being assembled; do not treat generated speech as a pronunciation teacher.')
 with st.expander('Pronunciation essentials'):
  st.write('ā, ī and ū are long vowels: hold them longer than a, i and u. In kh, gh, th and dh, h marks a breath after the consonant. ṭ and ḍ use the tongue curled back. Listen to a trained reciter before practising a difficult word.')
 with st.expander('Understand this verse or reading unit'):
  st.caption('A saved AI-assisted explanation is a study aid, awaiting review.')
  if st.button('Prepare / open the meaning'):
   try:
    meaning=prepare_explanation('learning:'+r['id'],r['reference'],r['original'],'verse');st.markdown(meaning['body'] if isinstance(meaning,dict) else meaning)
   except ProviderError as e:st.error(str(e))
 progress={k:v for k,v in st.session_state.items() if k.startswith(('position_','practised_'))}
 st.download_button('Download my progress',json.dumps(progress),'chant-progress.json','application/json')
 uploaded=st.file_uploader('Restore my progress',type=['json'])
 def restore():
  try:
   saved=json.load(uploaded)
   for k,v in saved.items():
    if k.startswith('position_') and isinstance(v,int) and v>=0:
     course=k.removeprefix('position_')
     if course in courses:st.session_state[k]=min(v,len(passages(course))-1);st.session_state['unit_'+course]=st.session_state[k]+1
    elif k.startswith('practised_') and isinstance(v,bool):st.session_state[k]=v
  except (ValueError,AttributeError):st.session_state['restore_error']='This progress file could not be read.'
 if uploaded:st.button('Restore',on_click=restore)
 if st.session_state.get('restore_error'):st.error(st.session_state['restore_error'])

elif page=='Games':
 games_ui()

elif page=='Settings':
 settings_ui()

elif page=='Converse':
 st.header('Continue the conversation')
 st.caption('Ask about a story, verse or difficulty. Answers use stored scripture passages and your configured provider fallback.')
 settings=active_settings()
 provider,key,model=settings[0]
 connected=[s[0] for s in settings if s[1]]
 if connected:st.success('Ready · fallback order: '+' → '.join(connected))
 else:
  st.info('No conversation key is connected. Prepared library answers still work; connect a provider for new questions.')
  if st.button('Open Settings to connect AI'):st.session_state.page='Settings';st.rerun()
 st.markdown('**Try a question**')
 starters=['What is Narayaneeyam?','How can I make a difficult decision?','Tell me the story of Dhruva simply.','Help me understand Bhagavad Gita 2.47.']
 cols=st.columns(2)
 for i,prompt in enumerate(starters):
  if cols[i%2].button(prompt,key='starter_'+str(i),use_container_width=True):st.session_state.pending_question=prompt;st.rerun()
 if 'history' not in st.session_state:st.session_state['history']=[]
 for m in st.session_state['history']:
  with st.chat_message(m['role']):st.markdown(m['content'])
 if st.session_state.get('_conversation_question'):
  st.session_state['pending_question']=st.session_state.pop('_conversation_question')
 question=st.text_area('Your question',key='pending_question')
 if st.button('Send question',disabled=not question.strip()):
  prepared=next((a for a in CONTENT['corpus']['corpusAnswers'] if a['question']==question.lower().strip().rstrip('?!.') and not a['id'].startswith('guidance-')),None)
  context=search(question)
  gid=st.session_state.get('conversation_context');g=next((g for g in G if g['id']==gid),None)
  if g:
   context=[r for r in passages('gita') if r['reference'].removeprefix('Bhagavad Gita ') in g['gita']]+context
  if st.session_state.get('_reading_context'):context=st.session_state['_reading_context']+context
  try:
   if prepared:answer,used=prepared['answer'],'prepared local answer (no AI call)'
   else:
    with st.spinner('Considering your question…'):answer,used=discuss(question,context,st.session_state['history'],settings)
   st.session_state['history'] += [{'role':'user','content':question},{'role':'assistant','content':answer}]
   with st.chat_message('assistant'):st.markdown(answer)
   st.caption('Answered by '+used+('' if prepared else ' · model interpretation, not an independently reviewed commentary'))
   for i,r in enumerate(context,1):st.markdown(f'[{i}] [{r["reference"]}]({r["source_url"]})')
  except ProviderError as e:st.error(str(e))
 if st.button('Clear conversation'):
  for k in list(st.session_state):
   if k in ('history','pending_question'):del st.session_state[k]
  st.rerun()
