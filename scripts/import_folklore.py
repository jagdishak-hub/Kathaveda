import json,re,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
raw=Path('/tmp/pg7128.txt').read_bytes();text=raw.decode('utf-8-sig').replace('\r\n','\n')
start=text.index('The Lion and the Crane',11000);end=text.index('Notes and References',300000);body=text[start:end]
headings=list(re.finditer(r'(?:^|\n{4,})([^\n]{5,120})\n{2,}',body))
assert len(headings)==29
stories=[];passages=[]
for i,h in enumerate(headings,1):
 title=h[1].strip().rstrip('.');content=body[h.end():headings[i].start() if i<len(headings) else len(body)].strip()
 content=re.sub(r'\[Illustration[^\]]*\]','',content).strip()
 story={'id':'folk-'+str(i),'title':title,'ref':'Jacobs, Indian Fairy Tales (1892), tale '+str(i),'themes':['Folktales'],'book':'Indian folktales','text':content,'child':content,'reflection':'What choice changed the outcome? Which part would you question or handle differently today?','url':'https://www.gutenberg.org/ebooks/7128','genre':'Folklore','reviewStatus':'Historical compiled tale, not scripture or a newly reviewed teaching.'}
 stories.append(story)
 passages.append({'id':story['id'],'work_id':'indian-folktales','section':0,'chapter':i,'verse':0,'reference':story['ref']+' · '+title,'original':content,'transliteration':'','source_url':story['url'],'metadata':json.dumps({'language':'English','readingTitle':title,'reviewStatus':story['reviewStatus'],'sourceSha256':hashlib.sha256(raw).hexdigest()})})
work={'id':'indian-folktales','title':'Indian Fairy Tales · regional folklore','edition':'Joseph Jacobs, 1892; Project Gutenberg transcription','sourceName':'Project Gutenberg','sourceUrl':'https://www.gutenberg.org/ebooks/7128','rights':'Public domain in the USA per source; full Project Gutenberg licence retained. Check local terms outside the USA.','coverage':'All 29 tales of this collection. This includes diverse Indian storytelling traditions; it is not a Purana or a scripture.','note':'Historical compiled folklore. Some tales contain violence and dated social assumptions; use family discussion and context.','language':'English'}
license=text[text.index('*** END OF'):]
with gzip.open(ROOT/'data/folk-stories.json.gz','wt',encoding='utf-8') as f:json.dump({'works':[work],'passages':passages,'stories':stories,'sourceLicence':license},f,ensure_ascii=False)
print(len(stories),'complete folktales')
