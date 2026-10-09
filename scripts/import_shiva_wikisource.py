"""Import the complete seven-samhita Sanskrit Shiva Purana from Sanskrit Wikisource.

The source pages are CC BY-SA. Original chapter structure and source URLs are retained.
No English translation is inferred or copied.
"""
import gzip,hashlib,json,re,time,unicodedata,urllib.parse,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
API='https://sa.wikisource.org/w/api.php'
UA={'User-Agent':'TheReadingRoom/1.0 (educational scripture reader)'}
DEV='१२३४५६७'

def get(params):
 payload=urllib.parse.urlencode(params).encode()
 for attempt in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(API,data=payload,headers=UA),timeout=90) as f:return json.load(f)
  except urllib.error.HTTPError as e:
   if attempt==3:raise
   time.sleep(max(int(e.headers.get('Retry-After','0') or 0),20*(attempt+1)) if e.code==429 else 4*(attempt+1))
  except Exception:
   if attempt==3:raise
   time.sleep(5*(attempt+1))

def number(s):return int(''.join(str(unicodedata.digit(c)) for c in s))

def all_titles():
 params={'action':'query','list':'allpages','apprefix':'शिवपुराणम्/','apnamespace':0,'aplimit':'max','format':'json','formatversion':'2'};out=[]
 while True:
  d=get(params);out.extend(x['title'] for x in d['query']['allpages'])
  if 'continue' not in d:return out
  params.update(d['continue'])

def chapters(titles):
 chosen={}
 for title in titles:
  sm=next(((i,d) for i,d in enumerate(DEV,1) if f'संहिता {d}' in title),None)
  cm=re.search(r'अध्यायः ([०-९]+)$',title)
  if not sm or not cm:continue
  samhita=sm[0];kh=re.search(r'खण्डः ([०-९]+)',title)
  part=1 if 'पूर्व भागः' in title else 2 if 'उत्तर भागः' in title else 0
  chapter=number(cm.group(1));sub=number(kh.group(1)) if kh else part
  key=(samhita,sub,chapter)
  # Prefer the zero-padded canonical spelling when both a redirect and page exist.
  if key not in chosen or len(cm.group(1))>len(re.search(r'अध्यायः ([०-९]+)$',chosen[key]).group(1)):chosen[key]=title
 return chosen

def clean(w):
 w=re.sub(r'^\s*\{\{header.*?\}\}\s*','',w,flags=re.S|re.I)
 w=re.sub(r'<ref[^>]*>.*?</ref>|<!--.*?-->','',w,flags=re.S|re.I)
 w=re.sub(r'<[^>]+>','',w)
 w=re.sub(r'\[\[(?:[^]|]+\|)?([^]]+)\]\]',r'\1',w)
 w=re.sub(r'\{\{[^{}]*\}\}','',w)
 w=re.sub(r'\[https?://[^ ]+ ([^]]+)\]',r'\1',w)
 w=re.sub(r'__\w+__|\[\[वर्गः.*','',w,flags=re.S)
 w=w.replace("'''",'').replace("''",'')
 lines=[re.sub(r'[ \t]+',' ',x).strip() for x in w.splitlines()]
 return '\n'.join(x for x in lines if x).strip()

def fetch_pages(mapping):
 titles=list(mapping.values());result={}
 for start in range(0,len(titles),50):
  batch=titles[start:start+50]
  d=get({'action':'query','prop':'revisions','rvprop':'content|ids','rvslots':'main','titles':'|'.join(batch),'redirects':1,'format':'json','formatversion':'2'})
  for page in d['query']['pages']:
   if page.get('missing'):continue
   content=page['revisions'][0]['slots']['main']['content'];result[page['title']]={'content':clean(content),'revid':page['revisions'][0]['revid']}
  # Map requested redirect titles to their canonical page.
  redirect={x['from']:x['to'] for x in d['query'].get('redirects',[])}
  for title in batch:
   canonical=redirect.get(title,title)
   if canonical in result:result[title]=result[canonical]
  print(min(start+50,len(titles)),'/',len(titles),flush=True)
  time.sleep(2)
 return result

if __name__=='__main__':
 mapping=chapters(all_titles());pages=fetch_pages(mapping)
 rows=[]
 names={1:'Vidyeshvara Samhita',2:'Rudra Samhita',3:'Shatarudra Samhita',4:'Kotirudra Samhita',5:'Uma Samhita',6:'Kailasa Samhita',7:'Vayaviya Samhita'}
 for (samhita,sub,chapter),title in sorted(mapping.items()):
  page=pages.get(title);body=page['content'] if page else ''
  if len(body)<80:raise ValueError('Missing chapter text: '+title)
  section=samhita*100+sub
  url='https://sa.wikisource.org/wiki/'+urllib.parse.quote(title.replace(' ','_'))
  meta={'language':'Sanskrit','readingTitle':names[samhita]+(f' · part {sub}' if sub else ''),'samhita':samhita,'subdivision':sub,'chapter':chapter,'sourceRevision':page['revid'],'reviewStatus':'Sanskrit Wikisource transcription; original numbering retained; not independently collated. No English translation is implied.'}
  rows.append({'id':f'shiva-complete-{samhita}-{sub}-{chapter}','work_id':'shiva-complete','section':section,'chapter':chapter,'verse':0,'reference':f'Shiva Purana · {names[samhita]}'+(f' · part {sub}' if sub else '')+f' · chapter {chapter}','original':body,'transliteration':'','source_url':url,'metadata':json.dumps(meta,ensure_ascii=False)})
 counts={str(s):len([r for r in rows if json.loads(r['metadata'])['samhita']==s]) for s in range(1,8)}
 work={'id':'shiva-complete','title':'Shiva Purana · complete Sanskrit edition','edition':'Sanskrit Wikisource transcription of the seven-samhita Venkatesvara Press tradition','sourceName':'Sanskrit Wikisource','sourceUrl':'https://sa.wikisource.org/wiki/शिवपुराणम्','rights':'CC BY-SA transcription; source-page attribution retained. Underlying 1906 Venkatesvara Press edition is public domain.','coverage':f'{len(rows)} chapters across all seven samhitas. Counts by samhita: '+', '.join(f'{k}: {v}' for k,v in counts.items())+'. Complete against this Wikisource edition structure.','note':'Complete Sanskrit source for this named edition. English meanings are not bundled; saved AI-assisted explanations are clearly labelled and require review. Text has not been independently collated against a critical edition.','language':'Sanskrit'}
 out={'works':[work],'passages':rows,'chapterCounts':counts,'sourceSnapshotSha256':hashlib.sha256(json.dumps(rows,ensure_ascii=False,sort_keys=True).encode()).hexdigest()}
 payload=json.dumps(out,ensure_ascii=False).encode('utf-8')
 target=ROOT/'data/shiva-complete.json.gz';temporary=target.with_suffix('.tmp')
 temporary.write_bytes(gzip.compress(payload,compresslevel=9));temporary.replace(target)
 print('wrote',len(rows),'chapters',counts)
