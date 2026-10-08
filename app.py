import csv,io,json,random,os
from pathlib import Path
import streamlit as st
from knowledge import CONTENT,works,passages,search,audit
from providers import CONFIG,discuss,ProviderError
from quiz import QUESTIONS
ROOT=Path(__file__).parent
st.set_page_config(page_title='KathaVeda · Stories for life',page_icon='🪷',layout='wide')
st.markdown('''<style>.stApp {background:linear-gradient(130deg,#fff9f0,#f1edff 65%,#eefbf6)} h1,h2,h3{color:#633e83} div[data-testid="stVerticalBlockBorderWrapper"]{background:#ffffffb8;border-radius:18px} @media(prefers-reduced-motion:no-preference){h1{animation:arrive .6s ease-out}@keyframes arrive{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}} </style>''',unsafe_allow_html=True)
st.sidebar.image(str(ROOT/'assets/logo.svg'),width=120)
st.title('🪷 KathaVeda')
st.caption('Stories, study and thoughtful practice — together as a family')
page=st.sidebar.radio('Explore',['Situations','Story garden','Reading room','Learn & chant','Quiz studio','Converse','Coverage & sources'])
family=st.sidebar.toggle('Younger reader explanations',value=False)
st.sidebar.caption('Reading and prepared activities use the local database. Online conversation is optional.')
W=works();titles={w['id']:w['title'] for w in W}
G=CONTENT['guidance']['guidance'];S=CONTENT['scriptures']['stories']
journal=st.session_state.setdefault('_journal',{})
for k,v in list(st.session_state.items()):
 if k.startswith('reflection_') or any(k.startswith(g['id']+'_') for g in G):journal[k]=v
for k,v in journal.items():
 if k not in st.session_state:st.session_state[k]=v
def source(r):
 st.caption(r['reference']);st.link_button('Read source',r.get('source_url',r.get('sourceUrl','https://sa.wikisource.org')))
def render_passage(r):
 st.markdown('### '+r['reference']);st.text(r['original'])
 if r.get('transliteration') and r['transliteration']!=r['original']:
  with st.expander('IAST transliteration'):st.text(r['transliteration'])
 meta=json.loads(r['metadata']);meaning=meta.get('meaning')
 if meaning and not meaning.startswith('An editorially reviewed'):st.info('Explanatory paraphrase: '+meaning)
 else:st.caption('A reviewed English meaning is not available for this passage.')
 st.caption(meta.get('reviewStatus','Source transcription; not independently collated'));source(r)

if page=='Coverage & sources':
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
 st.header('Read the original text')
 wid=st.selectbox('Collection',[w['id'] for w in W],format_func=lambda i:titles[i])
 work=next(w for w in W if w['id']==wid);st.info(work.get('coverage','Coverage not verified'))
 rows=passages(wid);sections=sorted({r['section'] for r in rows})
 section=st.selectbox('Book / khanda number',sections,format_func=lambda i:'Unsectioned source' if i==0 else str(i))
 chapters=sorted({r['chapter'] for r in rows if r['section']==section});chapter=st.selectbox('Chapter',chapters)
 selected=[r for r in rows if r['section']==section and r['chapter']==chapter]
 if len(selected)>1:
  index=st.selectbox('Verse / reading unit',range(len(selected)),format_func=lambda i:selected[i]['reference']);render_passage(selected[index])
 else:render_passage(selected[0])
 term=st.text_input('Search original text, reference or indexed keywords')
 if term:
  found=search(term)
  if not found:st.info('No matching stored text. Search is literal; it does not infer translations.')
  for r in found:
   with st.expander(r['reference']):render_passage(r)

elif page=='Story garden':
 st.header('Take time with a story')
 themes=sorted({t for s in S for t in s['themes']});theme=st.selectbox('Theme',['All']+themes)
 choices=[s for s in S if theme=='All' or theme in s['themes']]
 sid=st.selectbox('Choose a story',[s['id'] for s in choices],format_func=lambda i:next(s['title'] for s in choices if s['id']==i))
 s=next(s for s in S if s['id']==sid);st.subheader(s['title']);st.caption(s['book']+' '+s['ref']+' · prepared retelling, awaiting scholarly review')
 st.markdown(s['child'] if family else s['text']);st.info(s['reflection']);st.link_button('Compare with source chapters',s['url'])
 st.text_area('A family conversation or personal reflection',key='reflection_'+sid)

elif page=='Situations':
 st.header('A situation you are facing')
 for start in range(0,len(G),3):
  for col,card in zip(st.columns(3),G[start:start+3]):
   with col.container(border=True):
    st.markdown('**'+card['title']+'**');st.caption(card['familyFeeling'] if family else card['feeling'])
    st.button('Explore this situation',key='card_'+card['id'],on_click=lambda selected=card['id']:st.session_state.update({'selected_situation':selected}))
 gid=st.selectbox('Choose a situation',[g['id'] for g in G],format_func=lambda i:next(g['title'] for g in G if g['id']==i),key='selected_situation')
 g=next(g for g in G if g['id']==gid);st.subheader(g['title']);st.write(g['familyFeeling'] if family else g['feeling'])
 tabs=st.tabs(['Teaching & context','The full story','Apply it','A week of practice'])
 with tabs[0]:
  st.info(g['familyPrinciple'] if family else g['principle']);st.write(g['teaching'])
  for ref in g['gita']:
   matches=[r for r in passages('gita') if r['reference']=='Bhagavad Gita '+ref]
   for r in matches:render_passage(r)
  st.caption('The guidance and worksheets are modern applications inspired by the sources; they are not literal scripture quotations.')
 with tabs[1]:
  story=next((s for s in S if s['id']==g['storyId']),None)
  if story:
   st.subheader(story['title']);st.markdown(story['child'] if family else story['text']);st.link_button('Check the story source',story['url'])
 with tabs[2]:
  st.write(g['example'])
  for n,step in enumerate(g['familySteps'] if family else g['steps']):
   with st.container(border=True):
    st.markdown(f'**Step {n+1}**');st.write(step);st.text_area('Your response',key=f'{gid}_step{n}')
  st.text_area(g['question'],key=gid+'_question')
  st.text_input('One small action I can take today',key=gid+'_action')
  st.text_input('Someone who can help me think this through',key=gid+'_help')
  st.caption(g['caution'])
 with tabs[3]:
  prompts=['Describe one real instance of the difficulty, without judging yourself.','Separate what happened from what you feared might happen.','Revisit the source passage and note a question about its context.','Try the small action you selected. Notice what changed.','Ask a trusted person for a different perspective.','Repeat what helped. Adjust what did not fit your circumstances.','Review your notes: what will you keep practising next week?']
  for day,prompt in enumerate(prompts,1):
   with st.expander(f'Day {day}: {prompt}'):
    st.text_area('Notes',key=f'{gid}_day{day}');st.checkbox('Practised',key=f'{gid}_done{day}')
  notes={k:v for k,v in st.session_state.items() if k.startswith(gid+'_')};st.download_button('Save my worksheet',json.dumps(notes,ensure_ascii=False,indent=2),gid+'-practice.json','application/json')
 st.button('Discuss this situation in Converse',on_click=lambda:st.session_state.update({'conversation_context':gid,'pending_question':g['question']}))

elif page=='Learn & chant':
 st.header('Learn a little, return often')
 courses=[i for i in ['vishnu','lalita','gita','narayaneeyam'] if i in titles]
 wid=st.selectbox('Course',courses,format_func=lambda i:titles[i]);units=passages(wid)
 position_key='position_'+wid
 if position_key not in st.session_state:st.session_state[position_key]=0
 def move(delta):st.session_state[position_key]=max(0,min(len(units)-1,st.session_state[position_key]+delta))
 if 'unit_'+wid not in st.session_state:st.session_state['unit_'+wid]=st.session_state[position_key]+1
 idx=st.number_input('Current reading unit',1,len(units),key='unit_'+wid)
 if idx-1!=st.session_state[position_key]:st.session_state[position_key]=idx-1
 r=units[st.session_state[position_key]];st.progress((idx-1)/len(units));st.caption(f'{idx} of {len(units)} · {r["reference"]}')
 st.write('1. Recall the previous unit. 2. Read one line of this unit slowly. 3. Try it from memory. 4. Join the lines, then review both units together.')
 reveal=st.toggle('Show text while practising',value=True)
 if reveal:render_passage(r)
 else:st.info('Try from memory, then reveal the text to compare.')
 def advance():
  st.session_state['practised_'+r['id']]=True;move(1);st.session_state['unit_'+wid]=st.session_state[position_key]+1
 a,b=st.columns(2)
 a.button('Previous unit',on_click=lambda:(move(-1),st.session_state.update({'unit_'+wid:st.session_state[position_key]+1})),disabled=idx==1)
 b.button('Practised · learn next',on_click=advance,disabled=idx==len(units))
 st.caption('Progress is kept in this browser session. Download it before closing. Narayaneeyam is grouped by dasakam; pronunciation audio has not been supplied or verified.')
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

elif page=='Quiz studio':
 st.header('Read, reason, then check')
 level=st.selectbox('Challenge level',['Growing readers','Reflective readers','Close readers'])
 if st.button('Start a new round') or 'round' not in st.session_state or st.session_state.get('round_level')!=level:
  pool=[q for q in QUESTIONS if q['level']==level];random.shuffle(pool)
  st.session_state.update({'round':pool[:6],'round_level':level,'answers':{},'question_index':0,'order':{}})
 round_=st.session_state['round'];index=st.session_state['question_index']
 st.caption(f'{level} · question {index+1} of {len(round_)} · {len(QUESTIONS)} curated questions across three levels')
 q=round_[index]
 if index not in st.session_state['order']:
  order=list(range(len(q['choices'])));random.shuffle(order);st.session_state['order'][index]=order
 order=st.session_state['order'][index];st.subheader(q['prompt'])
 selected=st.radio('Your answer',order,format_func=lambda i:q['choices'][i],key=f'choice_{level}_{index}')
 if st.button('Check reasoning'):st.session_state['answers'][index]=selected
 if index in st.session_state['answers']:
  correct=st.session_state['answers'][index]==q['answer']
  (st.success if correct else st.info)('Correct.' if correct else 'Revisit this distinction. The supported answer is: '+q['choices'][q['answer']])
  st.write(q['why']);st.caption(q['reference'])
  if index<len(round_)-1 and st.button('Next challenge'):st.session_state['question_index']+=1;st.rerun()
  elif index==len(round_)-1:
   score=sum(v==round_[i]['answer'] for i,v in st.session_state['answers'].items());st.metric('Round score',f'{score}/{len(round_)}')
   st.write('Review these sources:')
   for i,v in st.session_state['answers'].items():
    if v!=round_[i]['answer']:st.write('• '+round_[i]['reference']+' — '+round_[i]['why'])

elif page=='Converse':
 st.header('Continue the conversation')
 st.caption('Online discussion uses a key configured by the app owner, or an optional personal key for this session. Keys are not written to the database. Prepared reading and learning do not use them.')
 with st.expander('Conversation settings',expanded=True):
  provider=st.selectbox('Primary provider',list(CONFIG));key=st.text_input('Optional personal API key',type='password',key='key_'+provider)
  key=key or os.environ.get('KATHAVEDA_'+provider.upper()+'_API_KEY','')
  if key:st.caption('A provider key is available for this session.')
  model=st.text_input('Model',value=CONFIG[provider][1],key='model_'+provider)
  fallback=st.selectbox('Optional fallback',['None']+[p for p in CONFIG if p!=provider])
  fallback_key=(st.text_input('Optional personal fallback API key',type='password',key='fallback_key_'+fallback) or os.environ.get('KATHAVEDA_'+fallback.upper()+'_API_KEY','')) if fallback!='None' else ''
  fallback_model=st.text_input('Fallback model',value=CONFIG[fallback][1],key='fallback_model_'+fallback) if fallback!='None' else ''
 if 'history' not in st.session_state:st.session_state['history']=[]
 for m in st.session_state['history']:
  with st.chat_message(m['role']):st.markdown(m['content'])
 question=st.text_area('Your question',key='pending_question')
 if st.button('Send question',disabled=not question.strip()):
  prepared=next((a for a in CONTENT['corpus']['corpusAnswers'] if a['question']==question.lower().strip().rstrip('?!.') and not a['id'].startswith('guidance-')),None)
  context=search(question)
  gid=st.session_state.get('conversation_context');g=next((g for g in G if g['id']==gid),None)
  if g:
   context=[r for r in passages('gita') if r['reference'].removeprefix('Bhagavad Gita ') in g['gita']]+context
  settings=[(provider,key,model)]+([(fallback,fallback_key,fallback_model)] if fallback_key else [])
  try:
   if prepared:answer,used=prepared['answer'],'prepared local answer (no AI call)'
   else:
    with st.spinner('Considering your question…'):answer,used=discuss(question,context,st.session_state['history'],settings)
   st.session_state['history'] += [{'role':'user','content':question},{'role':'assistant','content':answer}]
   with st.chat_message('assistant'):st.markdown(answer)
   st.caption('Answered by '+used+('' if prepared else ' · model interpretation, not an independently reviewed commentary'))
   for i,r in enumerate(context,1):st.markdown(f'[{i}] [{r["reference"]}]({r["source_url"]})')
  except ProviderError as e:st.error(str(e))
 if st.button('Clear conversation and keys'):
  for k in list(st.session_state):
   if k.startswith(('key_','fallback_key_')) or k in ('history','pending_question'):del st.session_state[k]
  st.rerun()
