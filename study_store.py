"""Persistent chapter readings and password-encrypted private study profiles."""
import os,json,sqlite3,base64,secrets,hashlib
from pathlib import Path
from cryptography.fernet import Fernet,InvalidToken
DEFAULT=Path(os.environ.get('KATHAVEDA_STUDY_DIR',str(Path(__file__).parent/'study-data')))
class StudyStore:
 def __init__(self,directory=DEFAULT):
  directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);self.path=directory/'study.sqlite'
  with self.db() as c:c.executescript('CREATE TABLE IF NOT EXISTS profiles(name TEXT PRIMARY KEY,salt BLOB NOT NULL,check_token BLOB NOT NULL);CREATE TABLE IF NOT EXISTS private_data(profile TEXT,name TEXT,value BLOB,PRIMARY KEY(profile,name));CREATE TABLE IF NOT EXISTS readings(id TEXT PRIMARY KEY,body TEXT,provider TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP);')
 def db(self):return sqlite3.connect(self.path,timeout=20)
 def unlock(self,name,password,create=False):
  name=name.strip().lower()
  if not name or len(name)>64 or len(password)<10:raise ValueError('Choose a profile name and a private passphrase of at least 10 characters.')
  with self.db() as c:
   row=c.execute('SELECT salt,check_token FROM profiles WHERE name=?',(name,)).fetchone()
   if not row:
    if not create:raise ValueError('This profile does not exist. Select Create profile first.')
    salt=secrets.token_bytes(32)
   else:salt=row[0]
   key=base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256',password.encode(),salt,600000));cipher=Fernet(key)
   if row:
    try:cipher.decrypt(row[1])
    except InvalidToken:raise ValueError('The profile name or passphrase was not accepted.') from None
   else:c.execute('INSERT INTO profiles VALUES(?,?,?)',(name,salt,cipher.encrypt(b'KathaVeda private profile')))
  return name,cipher
 def save(self,profile,cipher,name,value):
  with self.db() as c:c.execute('INSERT INTO private_data VALUES(?,?,?) ON CONFLICT(profile,name) DO UPDATE SET value=excluded.value',(profile,name,cipher.encrypt(json.dumps(value).encode())))
 def get(self,profile,cipher,name,default=None):
  with self.db() as c:row=c.execute('SELECT value FROM private_data WHERE profile=? AND name=?',(profile,name)).fetchone()
  if not row:return default
  try:return json.loads(cipher.decrypt(row[0]))
  except InvalidToken:raise ValueError('Unlock your own profile to read these saved settings.') from None
 def forget(self,profile,name):
  with self.db() as c:c.execute('DELETE FROM private_data WHERE profile=? AND name=?',(profile,name))
 def cached(self,id):
  with self.db() as c:r=c.execute('SELECT body,provider FROM readings WHERE id=?',(id,)).fetchone()
  return {'body':r[0],'provider':r[1]} if r else None
 def cache(self,id,body,provider):
  with self.db() as c:c.execute('INSERT INTO readings(id,body,provider) VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET body=excluded.body,provider=excluded.provider',(id,body,provider))
