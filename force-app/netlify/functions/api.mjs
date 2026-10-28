// Force Receiving server: sign-in, one shared state document in Netlify Blobs, and change ops.
// Env: FC_ADMIN_PASS, FC_WAREHOUSE_PASS, FC_SECRET (any long random string).
import {getStore} from '@netlify/blobs';
import {createHmac,timingSafeEqual,randomUUID} from 'node:crypto';

const COLS=['items','orders','arrivals','recv','units','issues','log'];
const ACCTS={fcadmin:{role:'office',env:'FC_ADMIN_PASS'},fcwarehouse:{role:'shop',env:'FC_WAREHOUSE_PASS'}};
const LOG_MAX=4000,TOKEN_DAYS=180;
const json=(o,s=200)=>new Response(JSON.stringify(o),{status:s,headers:{'content-type':'application/json','cache-control':'no-store'}});
const env=k=>(globalThis.Netlify?.env?.get(k))??process.env[k]??'';
const b64=s=>Buffer.from(s).toString('base64url');
const sign=p=>createHmac('sha256',env('FC_SECRET')).update(p).digest('base64url');
function same(a,b){const x=Buffer.from(String(a)),y=Buffer.from(String(b));return x.length===y.length&&timingSafeEqual(x,y)}
function makeToken(u,role){const p=b64(JSON.stringify({u,role,exp:Date.now()+TOKEN_DAYS*864e5}));return p+'.'+sign(p)}
function readToken(req){const t=(req.headers.get('authorization')||'').replace(/^Bearer /,'');const [p,s]=t.split('.');if(!p||!s||!env('FC_SECRET')||!same(s,sign(p)))return null;
 try{const o=JSON.parse(Buffer.from(p,'base64url').toString());return o.exp>Date.now()?o:null}catch(e){return null}}
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
   if(!a||!env(a.env)||!env('FC_SECRET')||!same(p||'',env(a.env)))return json({error:'no'},401);
   const name=String(u).toLowerCase();return json({u:name,role:a.role,token:makeToken(name,a.role)})}
  const who=readToken(req);if(!who)return json({error:'Sign in again'},401);
  if(path==='state'){const {doc}=await load();const v=new URL(req.url).searchParams.get('v');if(v&&v===doc.v)return new Response(null,{status:304});return json(doc)}
  if(path==='ops'&&req.method==='POST'){const {ops}=await req.json();if(!Array.isArray(ops)||ops.length>400)return json({error:'Bad request'},400);
   for(let i=0;i<25;i++){const {doc,etag}=await load();apply(doc.state,ops,who.role);doc.v=randomUUID();
    const r=await store().setJSON('state',doc,etag?{onlyIfMatch:etag}:{onlyIfNew:true});if(r.modified!==false)return json(doc);await new Promise(z=>setTimeout(z,60+Math.random()*120))}
   return json({error:'Busy, try again'},409)}
  return json({error:'Not found'},404)
 }catch(e){return json({error:e.message||'Server error'},400)}};
export const config={path:'/api/*'};
