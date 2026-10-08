"""Import the public-domain 1922 Besant edition, preserving its own numbering."""
import urllib.request,json,re,concurrent.futures,hashlib
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
BASE='https://en.wikisource.org/wiki/Bhagavad-Gita_(Besant_4th)'
def chapter(n):
 url=BASE+'/Discourse_'+str(n)
 cache=Path('/tmp/besant-'+str(n)+'.html')
 if cache.exists():raw=cache.read_bytes()
 else:
  raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'TheReadingRoom/1.0 attributed study importer'}),timeout=60).read();cache.write_bytes(raw)
 root=html.fromstring(raw)
 for e in root.xpath('//style|//script|//sup|//*[contains(@class,"pagenum")]'):e.drop_tree()
 node=root.xpath('//div[contains(@class,"mw-parser-output")]')[0];verses=[];pending=[]
 english=[]
 def flush():
  if not pending or not english:return
  numbered=re.findall(r'॥\s*([०-९0-9]+)\s*॥',' '.join(pending))
  if not numbered:raise ValueError('Missing Sanskrit number '+str(n)+' '+str(pending))
  verse=int(numbered[-1]);body='\n\n'.join(english)
  verses.append({'id':f'gita-besant-{n}-{verse}','work_id':'gita-besant','section':0,'chapter':n,'verse':verse,'reference':f'Bhagavad Gita · Besant edition {n}.{verse}','original':'\n'.join(pending),'transliteration':'','source_url':url,'metadata':json.dumps({'meaning':body,'meaningType':'Attributed 1922 English translation; older language','translator':'Annie Besant','reviewStatus':'Wikisource transcription, not independently collated','sourceSha256':hashlib.sha256(raw).hexdigest()})})
  pending.clear();english.clear()
 for p in node.xpath('.//p'):
  text=' '.join(p.text_content().split()).replace('\u200b','')
  if re.search('[\u0900-\u097f]',text):
   if english:flush()
   pending.append(text);continue
  if text.startswith('Thus in the glorious'):flush();break
  if not pending or not text or text.endswith('said:'):continue
  if not re.search(r'॥\s*[०-९0-9]+\s*॥',' '.join(pending)):continue
  text=re.sub(r'\(\d+\)?\s*$','',text).strip()
  if text:english.append(text)
 flush()
 if not verses:raise ValueError('Empty chapter '+str(n))
 nums=[r['verse'] for r in verses]
 if len(nums)!=len(set(nums)):raise ValueError('Duplicate verse numbers')
 missing=[v for v in range(1,max(nums)+1) if v not in nums]
 if missing:raise ValueError(f'Incomplete chapter {n}: {missing}')
 return n,verses
if __name__=='__main__':
 result=[];counts={}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  for n,rows in ex.map(chapter,range(1,19)):result.extend(rows);counts[n]=len(rows);print(n,len(rows),flush=True)
 work={'id':'gita-besant','title':'Bhagavad Gita · Sanskrit & English (Besant)','edition':'Annie Besant, fourth edition, 1922; Wikisource transcription','sourceName':'English Wikisource','sourceUrl':BASE,'rights':'1922 translation public domain in the US and life-plus-92-or-shorter jurisdictions per source; Wikisource transcription CC BY-SA. Attribution retained.','coverage':'All 18 discourses in this edition. Numbering is edition-specific; do not silently equate it with other editions.','note':'Attributed historical English translation; older vocabulary. Not a modern simple-language commentary. Sanskrit transcription not independently collated.'}
 (ROOT/'data/gita-besant.json').write_text(json.dumps({'works':[work],'passages':result,'chapterCounts':counts},ensure_ascii=False))
 print('Imported',len(result),'paired verses')
