"""Import attributed TEI sources; keep edition-specific chapter numbering."""
import json,gzip,hashlib,re
from pathlib import Path
from collections import defaultdict
from lxml import etree
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[('ramayana-gretil','Valmiki Ramayana · GRETIL','sa_rAmAyaNa',3),('rigveda','Rigveda · Aufrecht edition','sa_Rgveda-edAufrecht',3),('narasimha','Narasimha Purana','sa_narasiMhapurANa',2)]
def import_source(wid,title,name,depth):
 raw=Path('/tmp/'+name+'.xml').read_bytes();root=etree.fromstring(raw,etree.XMLParser(collect_ids=False));ns={'t':'http://www.tei-c.org/ns/1.0'}
 groups=defaultdict(list);source='https://gretil.sub.uni-goettingen.de/gretil/corpustei/'+name+'.xml'
 for lg in root.xpath('//t:body//t:lg',namespaces=ns):
  sid=lg.get('{http://www.w3.org/XML/1998/namespace}id','');nums=re.findall(r'\d+',sid)
  if len(nums)<depth:raise ValueError('Cannot assign a source verse: '+sid)
  section,chapter=(int(nums[0]),int(nums[1])) if depth==3 else (0,int(nums[0]))
  lines=[' '.join(''.join(l.itertext()).split()) for l in lg.findall('t:l',ns)]
  if lines:groups[section,chapter].append(sid+'\n'+'\n'.join(lines))
 copyright=' '.join(root.xpath('string(//t:availability)',namespaces=ns).split())
 if 'NonCommercial-ShareAlike' not in copyright:raise ValueError('Review reuse terms before importing '+name)
 title_statement=' '.join(root.xpath('string(//t:titleStmt)',namespaces=ns).split())
 bibliography=' '.join(root.xpath('string(//t:sourceDesc)',namespaces=ns).split())
 work={'id':wid,'title':title,'edition':bibliography or title_statement,'sourceName':'GRETIL · Göttingen University Library','sourceUrl':source,'rights':copyright,'coverage':f'{len(groups)} chapter/hymn groups extracted from the supplied TEI body; all encoded verse groups retained. Completeness applies to this electronic source only, not every recension.','note':'Sanskrit/IAST source with edition-specific references. No complete English translation or pronunciation recording is attached. Not independently collated.'}
 rows=[]
 for (section,chapter),texts in sorted(groups.items()):
  original='\n\n'.join(texts);rows.append({'id':f'{wid}-{section}-{chapter}','work_id':wid,'section':section,'chapter':chapter,'verse':0,'reference':f'{title} {section}.{chapter}' if section else f'{title} {chapter}','original':original,'transliteration':original,'source_url':source,'metadata':json.dumps({'reviewStatus':work['note'],'sourceSha256':hashlib.sha256(raw).hexdigest(),'encodedVerseGroups':len(texts)})})
 return work,rows
if __name__=='__main__':
 result={'works':[],'passages':[]}
 for args in SOURCES:
  w,p=import_source(*args);result['works'].append(w);result['passages'].extend(p);print(w['title'],len(p))
 with gzip.open(ROOT/'data/additional-sources.json.gz','wt',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False)
