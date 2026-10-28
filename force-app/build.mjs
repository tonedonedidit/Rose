// Copies the app into public/ for the company site. The in-page password hashes are only for the
// claude.ai preview; the site checks passwords on the server, so they are blanked here.
import {readFileSync,writeFileSync,mkdirSync,copyFileSync,existsSync} from 'node:fs';
mkdirSync('public',{recursive:true});
let html=readFileSync('index.html','utf8').replace(/const PREVIEW_HASHES=\{[^}]*\};/,'const PREVIEW_HASHES={};');
const head='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><link rel="manifest" href="/manifest.webmanifest"><link rel="apple-touch-icon" href="/icon-192.png"><link rel="icon" href="/icon-192.png"><style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}</style></head><body>';
writeFileSync('public/index.html',head+html+'</body></html>');
for(const f of ['manifest.webmanifest','icon-192.png','icon-512.png'])if(existsSync('assets/'+f))copyFileSync('assets/'+f,'public/'+f);
console.log('built public/');
