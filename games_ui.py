import random
import streamlit as st
from game_bank import QUIZ_BANK,CHARACTERS,DYNASTY,SEQUENCES
from settings_ui import saved,save

def games_ui():
 st.header('Games · read, remember and reason')
 mode=st.selectbox('Game',['Scripture Quiz','Guess the character','Build dynasty','Sequence of events'])
 book=st.selectbox('Choose your scripture quiz',['Gita','Narayaneeyam','Bhagavatam']) if mode=='Scripture Quiz' else 'All scriptures'
 level=st.select_slider('Level',options=list(range(1,26)),value=1)
 st.caption(f'Level {level} of 25 · '+('Moderate: use context and clues.' if level<=12 else 'Tough: fewer clues and more connections.'))
 st.write('Choose an answer, check it, then press **Next challenge**. Refresh starts a new mix. Questions are kept steady while you answer.')
 deck=f'{mode}:{book}:{level}'
 state=st.session_state.get('_game')
 refresh=st.button('Refresh · different challenges',type='primary')
 if not state or state['deck']!=deck or refresh:
  pool=[q for q in QUIZ_BANK if q['book']==book] if mode=='Scripture Quiz' else list(CHARACTERS if mode=='Guess the character' else DYNASTY if mode=='Build dynasty' else SEQUENCES)
  if mode=='Scripture Quiz' and level>12:
   hard=[q for q in pool if q['hard']]
   if len(hard)>=6:pool=hard
  previous=st.session_state.setdefault('_previous_rounds',{}).get(deck,[])
  fresh=[q for q in pool if q not in previous]
  if len(fresh)<6:fresh=pool
  selection=random.sample(fresh,min(6,len(fresh)));st.session_state['_previous_rounds'][deck]=selection
  state={'deck':deck,'items':selection,'index':0,'checked':False,'scores':[],'nonce':random.randrange(10**9),'orders':{}}
  st.session_state['_game']=state
 items=state['items'];index=state['index'];item=items[index];prefix=f"game_{state['nonce']}_{index}"
 st.progress(index/len(items));st.subheader(f'Challenge {index+1} / {len(items)}')
 correct=False;explanation='';ref=''
 if mode=='Scripture Quiz':
  st.write(item['prompt']);order=state['orders'].setdefault(index,random.sample(range(len(item['choices'])),len(item['choices'])))
  answer=st.radio('Your answer',order,index=None,format_func=lambda i:item['choices'][i],key=prefix)
  correct=answer==item['answer'];explanation=item['why']+' Supported answer: '+item['choices'][item['answer']];ref=item['reference'];ready=answer is not None
 elif mode=='Guess the character':
  name,clue,detail,ref=item;st.write(clue)
  if level<=12:st.info(detail)
  elif st.button('Reveal a hint',key=prefix+'_hint'):st.info(detail)
  choices=state['orders'].setdefault(index,random.sample([name]+random.sample([c[0] for c in CHARACTERS if c[0]!=name],5 if level>12 else 3),6 if level>12 else 4))
  answer=st.radio('Who is it?',choices,index=None,key=prefix);correct=answer==name;explanation=name+'. '+detail;ready=answer is not None
 elif mode=='Build dynasty':
  # Several labelled edges form one challenge; this is not a three-pair guessing game.
  edges=state['orders'].setdefault(index,random.sample(DYNASTY,5 if level>12 else 3));names=sorted({e[2] for e in DYNASTY});answers=[]
  st.write('Complete this family network. Keep birth and foster relationships separate.')
  for j,(child,relation,parent,reference) in enumerate(edges):
   answers.append(st.selectbox(f'{child} → {relation}',names,index=None,key=prefix+'_'+str(j)))
  ready=all(a is not None for a in answers);correct=all(a==e[2] for a,e in zip(answers,edges))
  explanation='\n\n'.join(f'{e[0]} → {e[1]} → {e[2]} · {e[3]}' for e in edges);ref='Sources shown beside each relationship.'
 else:
  title,events,ref=item;events=events if level>12 else events[:4];st.write('Put the events in order: **'+title+'**')
  shuffled=state['orders'].setdefault(index,random.sample(events,len(events)));positions=[]
  for j,event in enumerate(shuffled):positions.append(st.selectbox(event,list(range(1,len(events)+1)),index=None,key=prefix+'_'+str(j)))
  ready=all(v is not None for v in positions)
  correct=ready and all(pos==events.index(event)+1 for event,pos in zip(shuffled,positions))
  explanation='\n\n'.join(f'{i+1}. {event}' for i,event in enumerate(events))
 if st.button('Check answer',disabled=not ready or state['checked'],key=prefix+'_check'):
  state['checked']=True;state['scores'].append(correct);st.rerun()
 if state['checked']:
  (st.success if state['scores'][-1] else st.info)('Well reasoned.' if state['scores'][-1] else 'Here is the supported answer. Read the explanation before moving on.')
  st.markdown(explanation);st.caption(ref)
  if index<len(items)-1:
   if st.button('Next challenge',type='primary',key=prefix+'_next'):state['index']+=1;state['checked']=False;st.rerun()
  else:
   score=sum(state['scores']);st.metric('Round score',f'{score}/{len(items)}');st.progress(1.0)
   st.write('Refresh for another mix, or choose the next level.')
   if st.session_state.get('_profile'):save('game:'+deck,{'score':score,'total':len(items)})
 st.caption(f'{len(QUIZ_BANK)} authored quiz items · 25 levels for every game. Refresh avoids the previous round where the selected pool is large enough. Levels share a source-based bank; they are not 25 different scripture editions.')
