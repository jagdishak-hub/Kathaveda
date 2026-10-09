import random
import streamlit as st
from game_bank import QUIZ_BANK,CHARACTERS,DYNASTY,SEQUENCES
from settings_ui import saved,save
from game_levels import level_title,level_pool

def games_ui():
 st.header('Games garden')
 st.write('Choose a trail, collect lotus points, and unlock harder connections. Every answer includes its source so play leads back to reading.')
 st.markdown('<div class="rr-game-map">🌱 1–8 &nbsp;→&nbsp; 🌿 9–18 &nbsp;→&nbsp; 🪷 19–24 &nbsp;→&nbsp; 🏆 25</div>',unsafe_allow_html=True)
 mode=st.selectbox('Choose a game trail',['Scripture Quiz','Guess the character','Build dynasty','Sequence of events'],format_func=lambda x:{'Scripture Quiz':'📜 Scripture quest','Guess the character':'🕵️ Who am I?','Build dynasty':'🌳 Family tree builder','Sequence of events':'🧩 Story timeline'}[x])
 book=st.selectbox('Choose your scripture quiz',['Gita','Narayaneeyam','Bhagavatam']) if mode=='Scripture Quiz' else 'All scriptures'
 level=st.selectbox('Learning stage',list(range(1,26)),format_func=lambda n:f'{n:02d} · {level_title(book if mode=="Scripture Quiz" else "All scriptures",n)}')
 st.caption(f'Stage {level} of 25 · '+('Build recognition and context.' if level<=8 else 'Connect characters, events and teachings.' if level<=18 else 'Close reading and cross-text reasoning.'))
 round_size=st.selectbox('Round length',[5,10],format_func=lambda n:f'{n} challenges')
 st.write('Choose an answer, check it, then continue. A new round draws a different mix from the question bank.')
 deck=f'{mode}:{book}:{level}:{round_size}'
 state=st.session_state.get('_game')
 refresh=st.button('Refresh · different challenges',type='primary')
 if not state or state['deck']!=deck or refresh:
  pool=[q for q in QUIZ_BANK if q['book']==book] if mode=='Scripture Quiz' else list(CHARACTERS if mode=='Guess the character' else DYNASTY if mode=='Build dynasty' else SEQUENCES)
  if mode=='Scripture Quiz':pool=level_pool(pool,book,level)
  # Some close-reading questions match more than one level filter; never deal the same card twice.
  pool=list({q.get('id',str(q)):q for q in pool}.values())
  previous=st.session_state.setdefault('_previous_rounds',{}).get(deck,[])
  fresh=[q for q in pool if q not in previous]
  if len(fresh)<min(round_size,len(pool)):fresh=pool
  selection=random.sample(fresh,min(round_size,len(fresh)));st.session_state['_previous_rounds'][deck]=selection
  state={'deck':deck,'items':selection,'index':0,'checked':False,'scores':[],'nonce':random.randrange(10**9),'orders':{}}
  st.session_state['_game']=state
 items=state['items'];index=state['index'];item=items[index];prefix=f"game_{state['nonce']}_{index}"
 streak=0
 for result in reversed(state['scores']):
  if not result:break
  streak+=1
 c1,c2,c3=st.columns(3);c1.metric('Challenge',f'{index+1}/{len(items)}');c2.metric('Lotus points',sum(state['scores'])*10);c3.metric('Current streak',('🔥 '+str(streak)) if streak else '—')
 st.progress(index/len(items));st.subheader('Your challenge')
 correct=False;explanation='';ref=''
 if mode=='Scripture Quiz':
  st.write(item['prompt']);order=state['orders'].setdefault(index,random.sample(range(len(item['choices'])),len(item['choices'])))
  answer=st.radio('Your answer',order,index=None,format_func=lambda i:item['choices'][i],key=prefix)
  correct=answer==item['answer'];explanation=item['why']+' Supported answer: '+item['choices'][item['answer']];ref=item['reference'];ready=answer is not None
 elif mode=='Guess the character':
  name,clue,detail,ref=item;st.write(clue)
  if level<=8:st.info(detail)
  elif st.button('Reveal one hint',key=prefix+'_hint'):st.info(detail)
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
   score=sum(state['scores']);points=score*10;st.metric('Round complete',f'{points} lotus points · {score}/{len(items)} correct');st.progress(1.0)
   if score==len(items):st.balloons();st.success('Perfect round — Master Gardener badge earned! 🏆')
   elif score>=max(1,len(items)-2):st.success('Wisdom Seeker badge earned! 🪷')
   else:st.info('Every explanation you read grows the next round. Try the same stage again or move along the trail.')
   st.write('Start a different mix, or choose the next learning stage.')
   if st.session_state.get('_profile'):save('game:'+deck,{'score':score,'total':len(items)})
 st.caption(f'{len(QUIZ_BANK)} sourced quiz items · 25 named learning stages. Each scripture quiz changes focus as you move through its stages; later stages emphasise connections and close reading.')
