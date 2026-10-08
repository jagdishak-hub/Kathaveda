"""Rebuild the packaged SQLite database from the included attributed source archive."""
import gzip,json,sqlite3,hashlib
from pathlib import Path
ROOT=Path(__file__).parent
source=ROOT/'data/corpus.json.gz'
if not source.exists():
 parts=sorted((ROOT/'data/corpus-parts').glob('part-*'))
 if not parts:raise RuntimeError('The source archive is missing.')
 source.write_bytes(b''.join(p.read_bytes() for p in parts))
status=json.loads((ROOT/'data/import-status.json').read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==status['archiveSha256'],'Source archive failed its integrity check'
with gzip.open(source,'rt',encoding='utf-8') as f:data=json.load(f)
path=ROOT/'data/scriptures.sqlite'
output=path.with_suffix('.new.sqlite');output.unlink(missing_ok=True)
with sqlite3.connect(output) as c:
 c.executescript('CREATE TABLE works(id TEXT PRIMARY KEY,title TEXT,metadata TEXT); CREATE TABLE passages(id TEXT PRIMARY KEY,work_id TEXT,section INTEGER,chapter INTEGER,verse INTEGER,reference TEXT,original TEXT,transliteration TEXT,source_url TEXT,metadata TEXT);CREATE INDEX passage_lookup ON passages(work_id,section,chapter,verse);')
 for w in data['works']:c.execute('INSERT INTO works VALUES(?,?,?)',(w['id'],w['title'],json.dumps(w,ensure_ascii=False)))
 for r in data['passages']:
  assert r['original'] and r['source_url'],r['id']
  c.execute('INSERT INTO passages VALUES(?,?,?,?,?,?,?,?,?,?)',tuple(r[k] for k in ['id','work_id','section','chapter','verse','reference','original','transliteration','source_url','metadata']))
 c.commit();assert c.execute('pragma integrity_check').fetchone()[0]=='ok'
 assert not c.execute('select count(*) from passages where work_id not in(select id from works)').fetchone()[0]
output.replace(path)
print(len(data['works']),'collections;',len(data['passages']),'nonempty reading units')
