// Force Receiving server: sign-in, one shared state document in Netlify Blobs, and change ops.
// Env: FC_ADMIN_PASS, FC_WAREHOUSE_PASS, FC_SECRET (any long random string).
import {getStore} from '@netlify/blobs';
import {createHmac,timingSafeEqual,randomUUID,scryptSync,randomBytes} from 'node:crypto';

const COLS=['items','orders','arrivals','recv','units','issues','log'];
const ACCTS={fcadmin:{role:'office',env:'FC_ADMIN_PASS'},fcwarehouse:{role:'shop',env:'FC_WAREHOUSE_PASS'}};
const LOG_MAX=4000,TOKEN_DAYS=180;
const json=(o,s=200)=>new Response(JSON.stringify(o),{status:s,headers:{'content-type':'application/json','cache-control':'no-store'}});
const env=k=>(globalThis.Netlify?.env?.get(k))??process.env[k]??'';
const b64=s=>Buffer.from(s).toString('base64url');
const sign=p=>createHmac('sha256',env('FC_SECRET')).update(p).digest('base64url');
function same(a,b){const x=Buffer.from(String(a)),y=Buffer.from(String(b));return x.length===y.length&&timingSafeEqual(x,y)}
// Passwords changed in the app are stored hashed in the 'auth' blob and win over the env vars.
// Each change bumps that account's gen, which signs out every device holding an older token.
let AUTH=null,AUTH_AT=0;
async function auth(fresh){if(fresh||!AUTH||Date.now()-AUTH_AT>15000){AUTH=(await store().get('auth',{type:'json'}))||{};AUTH_AT=Date.now()}return AUTH}
const hashPw=(pw,salt)=>scryptSync(String(pw),salt,32).toString('hex');
async function checkPw(u,pw){const a=(await auth(true))[u];if(a&&a.hash)return same(hashPw(pw,a.salt),a.hash);const e=env(ACCTS[u].env);return !!e&&same(pw||'',e)}
function makeToken(u,role,gen=0){const p=b64(JSON.stringify({u,role,gen,exp:Date.now()+TOKEN_DAYS*864e5}));return p+'.'+sign(p)}
function readToken(req){const t=(req.headers.get('authorization')||'').replace(/^Bearer /,'');const [p,s]=t.split('.');if(!p||!s||!env('FC_SECRET')||!same(s,sign(p)))return null;
 try{const o=JSON.parse(Buffer.from(p,'base64url').toString());return o.exp>Date.now()?o:null}catch(e){return null}}
async function current(req){const o=readToken(req);if(!o)return null;const a=(await auth())[o.u];return (a&&a.gen||0)===(o.gen||0)?o:null}
const empty=()=>({v:randomUUID(),state:Object.fromEntries([...COLS.map(c=>[c,{}]),['meta',{}]])});
const store=()=>getStore({name:'force',consistency:'strong'});
async function load(){const r=await store().getWithMetadata('state',{type:'json'});return r?{doc:r.data,etag:r.etag}:{doc:empty(),etag:null}}

// Numbers the client changed (base → v) are applied as deltas to the newest copy, so two people
// putting away at once both count. Everything else is last writer wins.
function merge(cur,base,v){if(!cur||!base)return v;const out={...cur,...v};for(const k in v){if(typeof v[k]==='number'&&typeof base[k]==='number'&&typeof cur[k]==='number')out[k]=cur[k]+(v[k]-base[k])}
 if(typeof out.qty==='number'&&out.qty<=0&&out.kind)return null;return out}
function apply(st,ops,role){for(const o of ops){const {op,c,id}=o;
  if(c==='meta'){if(op!=='set')continue;if(role!=='office'){st.meta={...st.meta,people:Array.isArray(o.v?.people)?o.v.people.map(String).slice(0,200):st.meta.people};continue}st.meta={...o.v};continue}
  if(!COLS.includes(c)||typeof id!=='string'||!id||id.length>200)throw new Error('Bad change');
  if(c==='orders'&&role!=='office')throw new Error('Only the office changes orders');
  const col=st[c];
  if(op==='del')delete col[id];
  else if(op==='set')col[id]={...o.v,id};
  else if(op==='mut'){const r=merge(col[id]||null,o.base||null,o.v);if(r===null)delete col[id];else col[id]={...r,id}}}
 const L=Object.values(st.log);if(L.length>LOG_MAX){L.sort((a,b)=>a.t<b.t?-1:1).slice(0,L.length-LOG_MAX).forEach(e=>delete st.log[e.id])}}

export default async(req)=>{
 const path=new URL(req.url).pathname.replace(/^\/api\/?/,'');
 try{
  if(path==='ping')return json({ok:true});
  if(path==='login'&&req.method==='POST'){const {u,p}=await req.json().catch(()=>({}));const a=ACCTS[String(u||'').toLowerCase()];
   await new Promise(r=>setTimeout(r,400));
   const name=String(u||'').toLowerCase();if(!a||!env('FC_SECRET')||!(await checkPw(name,p)))return json({error:'no'},401);
   return json({u:name,role:a.role,token:makeToken(name,a.role,(await auth())[name]?.gen||0)})}
  const who=await current(req);if(!who)return json({error:'Sign in again'},401);
  if(path==='password'&&req.method==='POST'){if(who.role!=='office')return json({error:'Only the office can change passwords'},400);
   const {account,current:cur,next}=await req.json().catch(()=>({}));if(!ACCTS[account])return json({error:'Unknown account'},400);
   if(String(next||'').length<8)return json({error:'Use at least 8 characters.'},400);
   if(account==='fcadmin'&&!(await checkPw('fcadmin',cur)))return json({error:'The current office password is wrong.'},400);
   const A=await auth(true),salt=randomBytes(16).toString('hex'),gen=((A[account]&&A[account].gen)||0)+1;A[account]={salt,hash:hashPw(next,salt),gen,at:new Date().toISOString()};
   await store().setJSON('auth',A);AUTH=A;AUTH_AT=Date.now();
   return json({ok:true,token:account===who.u?makeToken(who.u,who.role,gen):undefined})}
  if(path==='state'){const {doc}=await load();const v=new URL(req.url).searchParams.get('v');if(v&&v===doc.v)return new Response(null,{status:304});return json(doc)}
  if(path==='ops'&&req.method==='POST'){const {ops}=await req.json();if(!Array.isArray(ops)||ops.length>400)return json({error:'Bad request'},400);
   for(let i=0;i<25;i++){const {doc,etag}=await load();apply(doc.state,ops,who.role);doc.v=randomUUID();
    const r=await store().setJSON('state',doc,etag?{onlyIfMatch:etag}:{onlyIfNew:true});if(r.modified!==false)return json(doc);await new Promise(z=>setTimeout(z,60+Math.random()*120))}
   return json({error:'Busy, try again'},409)}
  return json({error:'Not found'},404)
 }catch(e){return json({error:e.message||'Server error'},400)}};
export const config={path:'/api/*'};
