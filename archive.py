import concurrent.futures, datetime, hashlib, json, pathlib, time
from curl_cffi import requests
ROOT = pathlib.Path(__file__).parent
for name in ['threads', 'comments', 'bodies']:
 (ROOT/name).mkdir(exist_ok=True)
def get(url, payload=None):
 for attempt in range(4):
  try:
   time.sleep(0.4)
   r=requests.get(url,params={'input':json.dumps(payload)} if payload else None,impersonate='chrome',timeout=45)
   r.raise_for_status()
   if '<!DOCTYPE html>' in r.text[:100]: raise ValueError('HTML challenge')
   return r.text
  except Exception:
   if attempt==3: raise
   time.sleep(2**attempt)
def api(method,payload):
 return json.loads(get('https://common.xyz/api/internal/trpc/'+method,payload))['result']['data']
def save(path,data):
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
threads={t['id']:t for t in json.loads((ROOT/'inventory.json').read_text())}
errors=[]
def capture(t):
 ident=t['id']
 if (ROOT/'comments'/f'{ident}.json').exists(): return ident,0
 keep=['id','title','body','content_url','created_at','updated_at','last_edited','comment_count','profile_name','topic_id','archived_at']
 record={k:t.get(k) for k in keep}
 record['source']='https://common.xyz/edgeware/discussion/'+str(ident)
 record['body_complete']=False
 if t.get('content_url'):
  body=get(t['content_url']);(ROOT/'bodies'/f'{ident}.md').write_text(body);record['body_complete']=True
 elif len(t.get('body',''))<2000:
  (ROOT/'bodies'/f'{ident}.md').write_text(t.get('body',''));record['body_complete']=True
 save(ROOT/'threads'/f'{ident}.json',record)
 comments={}
 def walk(parent=None):
  page=1
  while True:
   p={'thread_id':ident,'limit':50,'cursor':page}
   if parent is not None:p['parent_id']=str(parent)
   d=api('comment.getComments',p)
   for c in d['results']:
    cid=c['id']
    if cid in comments:continue
    clean={k:v for k,v in c.items() if k in ['id','thread_id','parent_id','text','body','content_url','created_at','updated_at','deleted_at','reply_count','profile_name','address_id']}
    if c.get('content_url'):clean['full_text']=get(c['content_url'])
    comments[cid]=clean
    if c.get('reply_count',0):walk(cid)
   if page>=d['totalPages']:break
   page+=1
 walk()
 save(ROOT/'comments'/f'{ident}.json',list(comments.values()))
 return ident,len(comments)
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
 fs={pool.submit(capture,t):i for i,t in threads.items()}
 for n,f in enumerate(concurrent.futures.as_completed(fs),1):
  try:r=f.result()
  except Exception as e:errors.append({'thread':fs[f],'error':str(e)})
  if n%50==0:print('captured',n,'/',len(threads),'errors',len(errors),flush=True)
save(ROOT/'manifest.json',{'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'community':'edgeware','threads_discovered':len(threads),'errors':errors,'scope':'Public API-visible active and archived threads, full content URLs and paginated comments/replies. Deleted/private content is not recovered.'})
print('DONE',len(threads),'errors',len(errors),flush=True)
