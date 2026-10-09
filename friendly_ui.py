"""Reader-first navigation and practical situation cards."""
import html,gzip,json
from pathlib import Path
import streamlit as st
from knowledge import CONTENT,works,passages
from chapter_guides import GITA,BOOK_INTROS,SHIVA_READINGS
from expansion import NEW_STORIES
from reader_ui import reader_ui as source_reader
from situation_bank import EXTRA_SCENARIOS
STORIES=CONTENT['scriptures']['stories']+[{'id':sid,'title':title,'ref':ref,'themes':themes,'book':'Bhagavatam','text':body,'child':body,'reflection':question,'url':'https://vedabase.io/en/library/sb/'+ref.split('.')[0]+'/'+ref.split('.')[1].split('–')[0]+'/'} for sid,title,ref,themes,body,question in NEW_STORIES]
_folk_file=Path(__file__).parent/'data/folk-stories.json.gz'
if _folk_file.exists():
 with gzip.open(_folk_file,'rt',encoding='utf-8') as _f:STORIES.extend(json.load(_f)['stories'])
SCENARIOS=[
('I keep putting off a task','Learning & work',3,'Pick a task that takes ten minutes. Write its first physical step. Set a timer and start before judging the whole project.','A student delays a large assignment. Opening the document and writing three headings makes a manageable start.','learning'),
('I am scared to ask a question','Learning & work',4,'Write the exact part you do not understand. Ask one person to explain that part. Repeat the explanation back in your own words.','Instead of saying “I understand nothing,” ask “Why does this step come before that one?”','learning'),
('My mind keeps wandering','Learning & work',6,'Choose one short task. Put away one distraction. When attention wanders, return to the next sentence or step without scolding yourself.','While learning a verse, practise one line for five minutes rather than switching between several videos.','learning'),
('I failed an exam or a project','Confidence & setbacks',2,'Separate the result from your value as a person. Identify one error you can practise. Ask for feedback and schedule a small retry.','A poor mark becomes a plan to practise fractions, rather than a verdict that you are stupid.','results'),
('Someone else seems better than me','Confidence & setbacks',10,'Name one skill you admire. Ask how that person practises it. Choose a small practice goal you can measure yourself.','A friend sings well. You can learn one useful exercise rather than comparing your whole life with theirs.','self-worth'),
('I have very little to give','Care & connection',9,'Ask what would actually help. Offer something you can afford: attention, time or a small useful task. Do not borrow money to impress someone.','Calling an older relative and listening can be more meaningful than an expensive present.','helping'),
('I am about to send an angry message','Relationships',17,'Save the message as a draft. Remove insults and guesses about motives. State what happened and what you need next.','“You never care” becomes “I waited for our call. Please tell me when plans change.”','relationships'),
('I become defensive when corrected','Relationships',13,'Ask for one specific example. Repeat what you heard before explaining yourself. Decide whether one change would improve the situation.','A teacher points out a mistake. Asking to see the step helps more than defending the whole answer.','relationships'),
('My responsibilities feel too big','Learning & work',11,'List what belongs to you and what needs others. Choose one next step. Ask a named person for a specific kind of help.','For a family event, share cooking, transport and shopping rather than trying to do all three alone.','overwhelmed'),
('I do not know which option to choose','Decisions & change',18,'Write two realistic options. Compare their likely effects and your responsibilities. Ask what information is missing, then choose one reversible next step.','Before changing a course, speak to a teacher and try one sample lesson.','decisions'),
('I judge someone by their background','Relationships',5,'Notice the label you are using. Ask what you actually know about this individual. Apply the same fair standard you would want for yourself.','Do not assume a new classmate cannot contribute because of their accent.','relationships'),
('I keep repeating an unhelpful habit','Habits & balance',14,'Notice when the habit starts. Change one trigger in your surroundings. Replace it with a small action and track it for three days.','Leave the phone outside the bedroom and put a book beside the bed.','learning'),
('I say yes to everything','Care & connection',3,'List your real responsibilities before agreeing. Say what you can do and by when. Offer a smaller commitment if the full request is too much.','“I can help for half an hour on Saturday” is clearer than a promise you cannot keep.','helping'),
('I feel disconnected from everyone','Care & connection',7,'Notice one person whose work supports your day. Thank them specifically. Arrange a small shared activity with someone you trust.','A short walk with a friend can begin a connection without a big social event.','friendship'),
('I forget what matters when busy','Habits & balance',8,'Write your most important responsibility for today. Keep it visible. Before adding a new task, check whether it serves that priority.','Protect time for a promised family call instead of filling every gap with work.','rest'),
('I want to hide a mistake','Confidence & setbacks',16,'Tell the relevant person what happened. Explain what you can repair. Set one safeguard so the same mistake is less likely.','If you broke an item, report it and help arrange a repair rather than blaming someone else.','promises'),
('I want a reward before I begin','Learning & work',3,'Name why the task matters even if praise is delayed. Complete one useful part. Let feedback improve the work rather than decide whether it is worth doing.','Practise a difficult passage even when nobody is watching.','results'),
('I am afraid to change my mind','Decisions & change',18,'Write what new information changed your view. Check it with a trusted person. Explain your revised decision without pretending the earlier one never happened.','Changing a plan after learning its cost is responsible reflection.','decisions'),
('I am exhausted by caring for someone','Care & connection',6,'List the care that is essential today. Ask someone to share one task. Protect food and sleep, and seek suitable outside support when needed.','A relative can handle one errand while you rest. Asking does not mean you care less.','helping'),
('I keep replaying a small embarrassment','Confidence & setbacks',2,'Describe the event without adding a judgment about your whole self. Repair anything that needs repair. Return to one ordinary activity today.','Forgetting a word while speaking does not erase the rest of what you know.','self-worth'),
('Someone will not listen to me','Relationships',17,'Choose a calm time. Give one specific example and one clear request. If discussion remains unsafe or disrespectful, ask a trusted person for support.','Ask for a turn to explain your point rather than raising your voice over the other person.','relationships'),
('I envy a friend’s success','Confidence & setbacks',12,'Acknowledge the feeling privately. Congratulate the friend without making a comparison. Pick one thing you want to practise for your own growth.','You can celebrate a friend’s prize and still work towards a goal of your own.','self-worth'),
('I keep buying things to feel better','Habits & balance',15,'Delay the purchase for one day. Name the feeling behind it. Check whether a conversation, rest or a useful activity addresses that need better.','Boredom may need a walk or a project rather than another online order.','uncertainty'),
('I need to begin again after a mistake','Confidence & setbacks',4,'Understand what went wrong. Make one concrete repair. Ask for guidance on the step that will prevent a repeat.','An apology followed by a changed routine gives others a reason to rebuild trust.','promises')]+EXTRA_SCENARIOS

def story_view(story):
 st.subheader(story['title']);st.caption(story['book']+' · '+story['ref'])
 st.markdown(story['text']);st.info('Think about it: '+story['reflection'])
 with st.expander('Source and reading notes'):
  st.caption('Historical collected folktale by Joseph Jacobs (1892). Folklore is separate from scripture; older language and cultural assumptions need context.' if story.get('genre')=='Folklore' else 'Original editorial retelling, not a word-for-word translation. Specialist review is pending. Modern applications are suggestions, not direct scripture commands.')
  st.code(story['url'],language=None)
 if st.button('Talk about this story',key='talk_'+story['id']):
  st.session_state['_conversation_question']='Help me understand '+story['title']+' and apply its teaching today.'
  st.session_state['_reading_context']=passages('bhagavatam',chapter=int(story['ref'].split('.')[1].split('–')[0]),section=int(story['ref'].split('.')[0])) if story['book']=='Bhagavatam' and story['ref'][0].isdigit() else []
  st.success('Open Converse to continue with this story.')

@st.dialog('Read a story',width='large')
def open_story(story):
 story_view(story)

def reading_room():
 st.header('Library')
 st.write('Open the stored scripture here. Source text, translation and explanation are separate so you can see exactly what is—and is not—available.')
 st.warning('This is not yet five complete reader-ready scriptures. Four Sanskrit source collections are stored; translations and reviewed explanations are incomplete. The Saraswati collection is not loaded yet.')
 coverage=[
  {'Collection':'Bhagavad Gita','Original text':'700 Sanskrit verses · 18 chapters','Translation':'Historical English edition stored separately','Simple explanations':'18 chapter guides; verse meanings incomplete','Learning':'Verse-by-verse; recorded pronunciation incomplete'},
  {'Collection':'Srimad Bhagavatam','Original text':'335 Sanskrit chapters · 12 cantos','Translation':'Not complete','Simple explanations':'Selected story guides only','Learning':'Not yet verse-by-verse'},
  {'Collection':'Narayaneeyam','Original text':'100 Sanskrit dasakams','Translation':'Not complete','Simple explanations':'Selected readings only','Learning':'Dasakam-level; verse splitting pending'},
  {'Collection':'Shiva Purana','Original text':'457 Sanskrit chapters · 7 samhitas','Translation':'Not complete','Simple explanations':'Only selected chapters','Learning':'Not yet available'},
  {'Collection':'Saraswati literature','Original text':'Not loaded','Translation':'Not loaded','Simple explanations':'Not loaded','Learning':'Not loaded'},
 ]
 with st.expander('Coverage of the five focused collections',expanded=True):st.dataframe(coverage,hide_index=True,width='stretch')
 a,b,c=st.columns(3);a.metric('Stored source collections',4);b.metric('Stories ready to read',len(STORIES));c.metric('Gita chapter guides',18)
 source_tab,books_tab,stories_tab=st.tabs(['🕉 Read the text','📚 About the collections','📖 Story shelf'])
 with stories_tab:
  find_col,theme_col,shelf_col=st.columns([2,2,1])
  term=find_col.text_input('Find a story or character',placeholder='Try Krishna, Dhruva, kindness…')
  theme=theme_col.selectbox('What interests you?',['All themes']+sorted({t for s in STORIES for t in s['themes']}))
  filtered=[s for s in STORIES if (theme=='All themes' or theme in s['themes']) and (not term or term.lower() in (s['title']+' '+s['text']).lower())]
  if not filtered:st.info('No story matches these filters. Try another word or choose All themes.')
  st.caption(f'{len(filtered)} readings · choose a card to open the full story')
  pages=max(1,(len(filtered)+8)//9)
  page=shelf_col.selectbox('Story shelf',range(1,pages+1),format_func=lambda n:f'Shelf {n} of {pages}')
  filtered=filtered[(page-1)*9:page*9]
  selected=st.session_state.get('_open_story')
  for start in range(0,len(filtered),3):
   for col,story in zip(st.columns(3),filtered[start:start+3]):
    with col.container(border=True):
     st.caption(story['book']+' · '+story['ref']);st.markdown('### '+story['title']);st.write(story['text'].split('\n')[0][:180]+'…')
     if st.button('Read story →',key='read_'+story['id'],type='primary'):
      open_story(story)
 with books_tab:
  available={w['id'] for w in works()}
  for wid in ['gita','bhagavatam','narayaneeyam','shiva-complete' if 'shiva-complete' in available else 'shiva','saraswati-literature']:
   with st.container(border=True):
    if wid=='saraswati-literature':
     st.markdown('<span class="rr-kicker">CURATED COLLECTION</span>',unsafe_allow_html=True);st.subheader('Saraswati Literature')
     st.write('A focused collection for learning, speech, music and knowledge: Sarasvati Rahasya Upanishad, attributed hymns and stotras, and Saraswati narratives from established scriptures. Every component keeps its own source identity.')
     st.info('The verified text inventory is being assembled. Only attributed components will enter the shared reader; use My text meanwhile for an edition you own.')
     continue
    title=next(w['title'] for w in works() if w['id']==wid);st.markdown('<span class="rr-kicker">FOUNDATIONAL COLLECTION</span>',unsafe_allow_html=True);st.subheader(title);st.write(BOOK_INTROS[wid])
    if wid=='gita':
     chapter=st.selectbox('Choose a chapter to understand',range(1,19),format_func=lambda n:f'{n}. {GITA[n-1][0]}')
     guide=GITA[chapter-1];st.markdown(guide[1]);st.info('Try this: '+guide[2]);st.caption('Focus passage: Bhagavad Gita '+guide[3])
    elif wid in ('shiva','shiva-complete'):
     st.success('The complete seven-samhita Sanskrit edition is available in the Original scripture texts tab.' if wid=='shiva-complete' else 'This older source import is partial. See its coverage note.')
     chapter=st.selectbox('Start with a prepared explanation',list(SHIVA_READINGS),format_func=lambda k:SHIVA_READINGS[k][0]);st.markdown(SHIVA_READINGS[chapter][1])
    else:
     choices=[s for s in STORIES if s['book']=='Bhagavatam'] if wid=='bhagavatam' else [s for s in STORIES if s['id'] in ('gajendra','narayaneeyam')]
     sid=st.selectbox('Choose a reading',[s['id'] for s in choices],format_func=lambda i,readings=choices:next(s['title'] for s in readings if s['id']==i),key='book_'+wid)
     s=next(s for s in choices if s['id']==sid);st.markdown(s['text']);st.caption(s['book']+' '+s['ref'])
  st.caption('The main Library intentionally shows only the five focused collections. Other attributed imports remain documented under Sources.')
  with st.expander('Historical English editions already stored'):
   english=[w for w in works() if w.get('language')=='English']
   if english:
    eid=st.selectbox('Choose an English book',[w['id'] for w in english],format_func=lambda i:next(w['title'] for w in english if w['id']==i))
    readings=passages(eid);books=sorted({r['section'] for r in readings});book=st.selectbox('Book / part',books)
    readings=[r for r in readings if r['section']==book]
    rids=[r['id'] for r in readings];reader_key='full_reading_'+eid+'_'+str(book)
    rid=st.selectbox('Choose a chapter or tale',rids,format_func=lambda i:next(r['reference'] for r in readings if r['id']==i),key=reader_key)
    current=rids.index(rid)
    def move_reading(delta):st.session_state[reader_key]=rids[max(0,min(len(rids)-1,current+delta))]
    prev_col,count_col,next_col=st.columns([1,2,1])
    prev_col.button('← Previous',disabled=current==0,key='prev_'+reader_key,on_click=move_reading,args=(-1,),use_container_width=True)
    count_col.caption(f'Reading {current+1} of {len(rids)} in book / part {book}')
    next_col.button('Next →',disabled=current==len(rids)-1,key='next_'+reader_key,on_click=move_reading,args=(1,),use_container_width=True)
    size=st.radio('Reading size',['Comfortable','Large','Extra large'],horizontal=True,key='size_'+eid)
    reading=next(r for r in readings if r['id']==rid)
    size_px={'Comfortable':'18px','Large':'21px','Extra large':'24px'}[size]
    paragraphs=''.join('<p>'+html.escape(p).replace('\n','<br>')+'</p>' for p in reading['original'].split('\n\n') if p.strip())
    st.markdown(f'<div class="rr-long-reader" style="font-size:{size_px}">{paragraphs}</div>',unsafe_allow_html=True)
    st.caption('Historical English edition; older vocabulary. Source: '+reading['source_url'])
 with source_tab:
  focus=st.session_state.pop('_library_work',None)
  source_reader(default_id=focus,allowed_ids=['gita','gita-besant','bhagavatam','narayaneeyam','shiva-complete'])

def situations_ui():
 st.header('What would help you today?')
 st.write('Choose a difficulty. Start with one practical step, then explore the teaching and a related story.')
 groups=['All situations','Decisions & change','Relationships','Learning & work','Confidence & setbacks','Habits & balance','Care & connection']
 group_col,search_col=st.columns(2)
 group=group_col.selectbox('Browse by need',groups)
 search=search_col.text_input('Find your situation',placeholder='Try anger, exam, tired, decision…')
 existing=CONTENT['guidance']['guidance']
 cards=[{'id':g['id'],'title':g['title'],'group':'Everyday difficulties','legacy':g} for g in existing]+[{'id':'scenario-'+str(i),'title':s[0],'group':s[1],'scenario':s} for i,s in enumerate(SCENARIOS)]
 filtered=[c for c in cards if (group=='All situations' or c['group']==group) and (not search or search.lower() in c['title'].lower())]
 st.caption(f'{len(cards)} practical situations available · {len(filtered)} match your selection')
 selected=st.session_state.get('_situation_open')
 if not selected:
  if not filtered:st.info('No matching situation. Try a different word or category.')
  pages=max(1,(len(filtered)+8)//9)
  page=st.selectbox('Situation page',range(1,pages+1),format_func=lambda n:f'Page {n} of {pages}')
  filtered=filtered[(page-1)*9:page*9]
  for start in range(0,len(filtered),3):
   for col,card in zip(st.columns(3),filtered[start:start+3]):
    with col.container(border=True):
     st.caption(card['group']);st.markdown('### '+card['title'])
     if st.button('Help me with this →',key='need_'+card['id']):
      st.session_state['_situation_open']=card['id'];st.rerun()
  return
 if st.button('← All situations'):
  st.session_state.pop('_situation_open',None);st.rerun()
 card=next(c for c in cards if c['id']==selected)
 with st.container(border=True):
  st.subheader(card['title'])
  if 'scenario' in card:
   title,category,chapter,steps,example,related=card['scenario'];guide=GITA[chapter-1]
   st.markdown('### Your next steps')
   for step in steps.split('. '):st.write('• '+step.rstrip('.')+'.')
   st.markdown('**An everyday example**');st.write(example)
   with st.expander('The scripture teaching behind this'):
    st.write(guide[1]);st.caption('Bhagavad Gita '+guide[3]+' · modern application inspired by this passage')
   original=next(g for g in existing if g['id']==related)
   story_ids={6:'ambarisha',7:'jada-bharata',9:'rukmini-letter',10:'trivakra',12:'bharata-deer',15:'ajamila',18:'bharata-deer',23:'ajamila'}
   scenario_index=int(card['id'].split('-')[-1]);story=next(s for s in STORIES if s['id']==story_ids.get(scenario_index,original['storyId']))
  else:
   original=card['legacy'];st.info(original['principle']);st.markdown('### Your next steps')
   for i,step in enumerate(original['steps'],1):st.write(f'{i}. {step}')
   st.write('**An everyday example**');st.write(original['example'])
   with st.expander('The scripture teaching behind this'):st.write(original['teaching']);st.caption('Bhagavad Gita '+', '.join(original['gita']))
   story=next(s for s in STORIES if s['id']==original['storyId'])
  with st.expander('Read a related story · '+story['title']):st.markdown(story['text']);st.caption(story['book']+' '+story['ref'])
  st.text_input('One small step I will take today',key='nextstep_'+selected)
  if st.button('Continue this in Converse',key='discuss_'+selected):
   st.session_state['_conversation_question']='I am facing this: '+card['title']+'. Help me make a practical plan.';st.session_state['conversation_context']=original['id'];st.success('Open Converse to discuss your own situation.')
