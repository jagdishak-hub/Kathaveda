"""Import historical translations with source headings and licence retained."""
import re,json,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def roman(s):
 vals={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000};return sum(-vals[c] if i+1<len(s) and vals[c]<vals[s[i+1]] else vals[c] for i,c in enumerate(s))
def book(n,wid,title,author,kind):
 raw=Path('/tmp/pg'+str(n)+'.txt').read_bytes();text=raw.decode('utf-8-sig').replace('\r\n','\n')
 end=re.search(r'\*\*\* END OF (?:THE |THIS )?PROJECT GUTENBERG',text,re.I)
 if not end:raise ValueError('Missing Gutenberg end marker')
 license=text[end.start():];text=text[:end.start()]
 pattern=r'(?m)^Canto ([IVXLCDM]+)\.[^\n]*$' if kind=='ramayana' else r'(?mi)^SECTION ([IVXLCDM]+|[0-9]+)(?:\.|(?=\s|$))[^\n]*$'
 headings=list(re.finditer(pattern,text));rows=[];seen=set()
 if kind=='mahabharata':
  headings=sorted(headings+list(re.finditer(r'(?m)^([0-9]{1,3})\s*$',text)),key=lambda h:h.start())
 for i,h in enumerate(headings):
  if kind=='ramayana':
   books=list(re.finditer(r'(?m)^BOOK ([IVXLCDM]+)\.',text[:h.start()]));section=roman(books[-1][1]) if books else 0
  elif kind=='vishnu':
   books=list(re.finditer(r'(?m)^PART ([IVXLCDM]+)\.',text[:h.start()]));section=roman(books[-1][1]) if books else 0
   if h.start()<33378:continue
  else:
   books=list(re.finditer(r'(?m)^BOOK (\d+)\s*$',text[:h.start()]));section=int(books[-1][1]) if books else 0
  if not section:raise ValueError('Chapter without source book')
  chapter=int(h[1]) if h[1].isdigit() else roman(h[1].upper());finish=headings[i+1].start() if i+1<len(headings) else len(text)
  boundaries=list(re.finditer(r'(?m)^(?:BOOK [0-9]+\s*$|BOOK [IVXLCDM]+\.|PART [IVXLCDM]+\.)',text[h.end():finish]))
  if boundaries:finish=h.end()+boundaries[0].start()
  body=text[h.end():finish].strip()
  if len(body)<30:continue
  id=f'{wid}-{n}-{section}-{chapter}-{i}'
  label=h.group().strip();meta={'language':'English','readingTitle':label,'translator':author,'sourceSha256':hashlib.sha256(raw).hexdigest(),'reviewStatus':'Attributed historical translation; not simplified or independently collated. Source numbering retained.'}
  rows.append({'id':id,'work_id':wid,'section':section,'chapter':chapter,'verse':i,'reference':f'{title} · book {section}, '+label,'original':body,'transliteration':'','source_url':'https://www.gutenberg.org/ebooks/'+str(n),'metadata':json.dumps(meta)})
 w={'id':wid,'title':title,'edition':author+' · historical translation, Project Gutenberg transcription','sourceName':'Project Gutenberg','sourceUrl':'https://www.gutenberg.org/ebooks/'+str(n),'rights':'Public domain in the USA per source. Check local copyright terms outside the USA. Full Gutenberg licence retained in the source archive.','coverage':f'{len(rows)} indexed source sections; source headings and book numbering retained. Scope is this electronic edition, not every recension.','note':'English historical translation, older vocabulary and cultural assumptions. Not a modern child-friendly retelling or an independently collated edition.','language':'English'}
 return w,rows,license
if __name__=='__main__':
 data={'works':[],'passages':[],'sourceLicences':{}}
 sources=[(24869,'ramayana-english','Ramayana · English verse','Ralph T. H. Griffith','ramayana'),(66208,'vishnu-english','Vishnu Purana · English','M. N. Dutt, consulting H. H. Wilson','vishnu')]+[(n,'mahabharata-english','Mahabharata · English','Kisari Mohan Ganguli','mahabharata') for n in [15474,15475,15476,15477]]
 for args in sources:
  w,p,lic=book(*args)
  if w['id'] not in {x['id'] for x in data['works']}:data['works'].append(w)
  data['passages'].extend(p);data['sourceLicences'][str(args[0])]=lic;print(args[0],len(p),flush=True)
 for w in data['works']:
  subset=[r for r in data['passages'] if r['work_id']==w['id']];sections=sorted({r['section'] for r in subset});w['coverage']=f"{len(subset)} source readings across books {', '.join(map(str,sections))}. Historical translation with edition-specific headings; not every recension."
 with gzip.open(ROOT/'data/gutenberg-sources.json.gz','wt',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False)
