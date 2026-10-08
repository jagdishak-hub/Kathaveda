GITA_LEVELS=[
 'Arjuna names the conflict','Knowledge and steady action','Work without clinging','Learning through disciplined action','Action, renunciation and balance','Training the wandering mind','Knowledge, devotion and remembrance','The imperishable and the final thought','Offering ordinary life','Seeing the divine in the world','The universal form','Devotion in practice','Field, knower and discernment','The three qualities','The enduring self and highest aim','Divine and destructive tendencies','Faith, food and disciplined choice','Reflect, decide and act',
 'Speaker and listener','Match teaching to chapter','Apply without misquoting','Compare two teachings','Trace an idea across chapters','Close reading challenge','Whole Gita mastery']
NAR_LEVELS=[
 'Glory and form','Devotion and prayer','Yoga and attention','Creation begins','The cosmic form','Brahma and creation','Dissolution and renewal','Searching for origin','Variety of creation','Vaikuntha and the sages','Varaha lifts the Earth','Varaha and Hiranyaksha','Kapila appears','Kapila teaches','Nara, Narayana and Daksha','Dhruva’s devotion','Prithu and the Earth','The Prachetas','Rishabha’s life','Worlds and worship','Ajamila','Daksha and Chitraketu','Prahlada','Narasimha','Gajendra and connected mastery']
BHAG_LEVELS=[
 'Frame: Parikshit and Shukadeva','Creation and early sages','Kapila and Devahuti','Dhruva’s resolve','Prithu and responsibility','Ajamila and remembrance','Prahlada under pressure','Gajendra asks for help','Vamana and Bali','Krishna’s birth','Childhood in Vraja','Govardhana and pride','Brahma’s bewilderment','Kaliya and a poisoned river','Akrura’s journey','Learning with Sandipani','Sudama and friendship','Rantideva and generosity','Markandeya’s vision','Character connections','Family relationships','Order the episode','Source-reference challenge','Compare two episodes','Bhagavatam mastery']
GENERIC_LEVELS=['Four clear clues','People and places','Parents and children','Teachers and students','Promises and duties','Journeys begin','Help arrives','Choices and consequences','Recognise the episode','Complete the relationship','Order four events','Similar characters','Birth and foster families','Hidden first clue','Five-step sequence','Mixed canto challenge','Who said or did it?','Connect two episodes','Fewer clues','Six possible characters','Larger family network','Full event sequence','Source-reference round','Cross-scripture connections','Master challenge']
BHAG_TARGETS=[['1.19'],['3.22','3.24','3.25'],['3.24','3.25'],['4.8','4.9'],['4.17','4.18'],['6.1','Ajamila'],['7.5','7.7','7.8','7.9'],['8.2','8.3','8.4'],['8.18','8.19','8.20','8.21','8.22','8.23'],['10.3','10.5'],['10.9'],['10.24','10.25','10.26','10.27'],['10.13','10.14'],['10.16','10.17'],['10.38','10.39','10.40'],['10.45'],['10.80','10.81'],['9.21']]

def level_title(book,level):
 return {'Gita':GITA_LEVELS,'Narayaneeyam':NAR_LEVELS,'Bhagavatam':BHAG_LEVELS,'All scriptures':GENERIC_LEVELS}.get(book,GENERIC_LEVELS)[level-1]

def level_pool(pool,book,level):
 if book=='Gita' and level<=18:
  exact=[q for q in pool if f'Gita {level}.' in q['reference']]
  neighbours=[q for q in pool if any(f'Gita {n}.' in q['reference'] for n in {max(1,level-1),min(18,level+1)})]
  return exact+neighbours
 if book=='Narayaneeyam' and level<=25:
  targets={level,max(1,level-1),min(26,level+1)}
  focused=[q for q in pool if any(f'Dasakam {n}' in q['reference'] for n in targets)]
  return focused
 if book=='Bhagavatam' and level<=18:
  targets=BHAG_TARGETS[level-1]
  focused=[q for q in pool if any(t in q['reference'] for t in targets)]
  return focused or pool
 if level>=19:
  hard=[q for q in pool if q.get('hard')]
  return hard or pool
 return pool
