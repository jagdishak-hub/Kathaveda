import json,sqlite3,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).parent
if not (ROOT/'data/scriptures.sqlite').exists():subprocess.run([sys.executable,str(ROOT/'build_database.py')],check=True)
CONTENT=json.loads((ROOT/'data/content.json').read_text())
def connect():
 c=sqlite3.connect(f"file:{ROOT/'data/scriptures.sqlite'}?mode=ro",uri=True);c.row_factory=sqlite3.Row;return c
def works():
 with connect() as c:return [json.loads(r['metadata']) for r in c.execute('select * from works order by title')]
def passages(work_id,section=None,chapter=None):
 sql='select * from passages where work_id=?';args=[work_id]
 for name,v in [('section',section),('chapter',chapter)]:
  if v is not None:sql+=f' and {name}=?';args.append(v)
 with connect() as c:return [dict(r) for r in c.execute(sql+' order by section,chapter,verse',args)]
def search(text,limit=8):
 topic_words={'anger':['anger','angry','rage'],'decisions':['decide','decision','choices'],'learning':['focus','attention','distracted'],'results':['failure','results','success'],'self-worth':['compare','comparison','worth'],'friendship':['lonely','loneliness','friendship']}
 matching=[g for g in CONTENT['guidance']['guidance'] if any(word in text.lower() for word in topic_words.get(g['id'],[]))]
 preferred=[]
 for g in matching:
  for ref in g['gita']:
   preferred += [r for r in passages('gita') if r['reference']=='Bhagavad Gita '+ref]
 if preferred:return list({r['id']:r for r in preferred}.values())[:limit]
 stop={'the','and','that','this','with','from','have','what','which','how','can','could','would','should','about','please','help','for','you','your','are','was','not','why','does','feel'}
 words=[w for w in dict.fromkeys(re.findall(r'[\w]+',text.lower())) if len(w)>2 and w not in stop][:6]
 if not words:return []
 with connect() as c:
  clauses=[];args=[]
  for word in words:
   clauses.append('(lower(reference) like ? or lower(original) like ? or lower(metadata) like ?)');args.extend(['%'+word+'%']*3)
  return [dict(r) for r in c.execute('select * from passages where '+' OR '.join(clauses)+' limit ?',args+[limit])]
def audit():
 out=[]
 for w in works():
  rows=passages(w['id']);sections={}
  for r in rows:sections.setdefault(r['section'],set()).add(r['chapter'])
  gaps={str(s):[i for i in range(min(v),max(v)+1) if i not in v] for s,v in sections.items() if v}
  out.append({'Collection':w['title'],'Stored units':len(rows),'Sections':', '.join(map(str,sections)),'Coverage':w.get('coverage','Not verified'),'Internal numbering gaps':json.dumps(gaps),'Review':w.get('note','Not independently collated')})
 return out
