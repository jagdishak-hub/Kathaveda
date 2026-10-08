"""One online call per question; optional single fallback. Keys are supplied by the encrypted profile settings layer."""
import json,urllib.request,urllib.error,urllib.parse
CONFIG={
 'OpenRouter':('https://openrouter.ai/api/v1/chat/completions','openrouter/auto'),
 'Gemini':('https://generativelanguage.googleapis.com/v1beta/models/','gemini-3.8-flash'),
 'Groq':('https://api.groq.com/openai/v1/chat/completions','openai/gpt-oss-120b'),
 'Grok':('https://api.x.ai/v1/chat/completions','grok-4.7')}
class ProviderError(Exception):pass
def request(provider,key,model,messages,opener=urllib.request.urlopen):
 if not key:raise ProviderError('Enter an API key in Settings to discuss further.')
 url=CONFIG[provider][0];headers={'Content-Type':'application/json'}
 if provider=='Gemini':
  url+=urllib.parse.quote(model,safe='')+':generateContent';headers['x-goog-api-key']=key
  system='\n'.join(m['content'] for m in messages if m['role']=='system')
  body={'systemInstruction':{'parts':[{'text':system}]},'contents':[{'role':'model' if m['role']=='assistant' else 'user','parts':[{'text':m['content']}]} for m in messages if m['role']!='system'],'generationConfig':{'maxOutputTokens':4096}}
 else:
  headers['Authorization']='Bearer '+key;body={'model':model,'messages':messages,'max_tokens':2400}
 try:
  with opener(urllib.request.Request(url,data=json.dumps(body).encode(),headers=headers),timeout=40) as r:raw=r.read()
 except urllib.error.HTTPError as e:
  explanations={401:'The API key was not accepted.',403:'This key or account cannot access this model.',404:'The selected model was not found.',429:'The provider has reached a rate or credit limit.'}
  raise ProviderError(explanations.get(e.code,f'The provider returned HTTP {e.code}.')+' Try another connected provider or model.') from None
 except (urllib.error.URLError,TimeoutError):raise ProviderError('The provider could not be reached. Your question is kept; you can retry.') from None
 try:
  data=json.loads(raw)
  answer='\n'.join(p.get('text','') for p in data['candidates'][0]['content']['parts'] if not p.get('thought')) if provider=='Gemini' else data['choices'][0]['message']['content']
  if not isinstance(answer,str) or not answer.strip():raise ValueError()
  return answer.strip()
 except (ValueError,KeyError,IndexError,TypeError):raise ProviderError('The provider returned no readable answer. Your question is kept; try another model.') from None

def discuss(question,context,history,settings):
 sources='\n\n'.join(f"[{i+1}] {r['reference']}\n{r['original'][:5000]}" for i,r in enumerate(context[:6]))
 system='You are a warm scripture study companion for Hindu families. Ask clarifying questions when useful. Distinguish source text, tradition-specific interpretation and modern practical advice. Do not invent quotations, verses, Sanskrit, references, or guarantees of divine rewards. If retrieved text does not support a claim, say so. Cite only supplied numbered sources. Be suitable for children when requested. Use short sentences and familiar words suitable for kids and elders. Explain Sanskrit terms when first used. For a life problem: briefly acknowledge the difficulty, explain one supported teaching, give three concrete steps the person can try today, and one everyday example. Avoid abstract philosophical speeches. Do not tell someone to accept abuse or replace professional help with chanting. For a story or verse, explain the events and meaning before any modern application.\nRetrieved original passages:\n'+sources
 messages=[{'role':'system','content':system}]+history[-8:]+[{'role':'user','content':question}]
 attempts=[]
 for provider,key,model in settings[:2]:
  try:return request(provider,key,model,messages),provider
  except ProviderError as e:attempts.append(provider+': '+str(e))
 raise ProviderError('\n'.join(attempts) or 'Configure an online provider first.')
