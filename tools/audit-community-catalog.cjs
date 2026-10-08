#!/usr/bin/env node
const fs=require('fs');
const vm=require('vm');

const index=fs.readFileSync('index.html','utf8');
const extraSource=fs.readFileSync('community-extra.js','utf8');

const startToken='const communityApps=[';
const start=index.indexOf(startToken);
if(start<0)throw new Error('communityApps start not found in index.html');
const guard=index.indexOf('function canonicalCommunityUrl',start);
if(guard<0)throw new Error('community duplicate runtime guard not found in index.html');
const between=index.slice(start+startToken.length,guard);
const end=between.lastIndexOf('];');
if(end<0)throw new Error('communityApps end not found in index.html');

const builtCtx={};
vm.runInNewContext(`communityApps=[${between.slice(0,end)}]`,builtCtx,{timeout:2000});
const builtins=builtCtx.communityApps||[];

const extraCtx={window:{}};
vm.runInNewContext(extraSource,extraCtx,{timeout:2000});
const extras=extraCtx.window.communityExtraApps||[];

function canonicalUrl(value){
  if(!value)return '';
  try{
    const u=new URL(String(value));
    u.hash='';
    u.search='';
    u.hostname=u.hostname.toLowerCase();
    if(u.hostname==='raw.githubusercontent.com'){
      const p=u.pathname.split('/').filter(Boolean);
      if(p.length>=4){
        p[0]=p[0].toLowerCase();
        p[1]=p[1].toLowerCase();
        if(p[2]==='refs'&&p[3]==='heads'&&p.length>=6)p.splice(2,2);
        u.pathname='/'+p.join('/');
      }
    }
    return u.toString().replace(/\/$/,'');
  }catch(_){return String(value).trim()}
}

function normalizedText(value){
  return String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();
}
function nameKey(app){return normalizedText(app.author)+'|'+normalizedText(app.name)}

const rows=[...builtins.map(app=>({app,where:'index.html'})),...extras.map(app=>({app,where:'community-extra.js'}))];
const seenUrls=new Map();
const seenNames=new Map();
const errors=[];

for(const {app,where} of rows){
  const label=`${where}: ${app.author||'?'} / ${app.name||'?'}`;
  const url=canonicalUrl(app.file);
  if(!url){errors.push(`${label} has no install URL`)}
  else if(seenUrls.has(url)){errors.push(`duplicate install URL\n  first: ${seenUrls.get(url)}\n  again: ${label}\n  URL: ${url}`)}
  else seenUrls.set(url,label);

  const nk=nameKey(app);
  if(nk!=='|'){
    if(seenNames.has(nk)){errors.push(`duplicate author + name\n  first: ${seenNames.get(nk)}\n  again: ${label}`)}
    else seenNames.set(nk,label);
  }
}

console.log(`Community catalog audit: ${builtins.length} built-in + ${extras.length} extra = ${rows.length} projects`);
if(errors.length){
  console.error(`Found ${errors.length} duplicate/catalog error(s):`);
  for(const err of errors)console.error(`\n- ${err}`);
  process.exit(1);
}
console.log('OK: no duplicate install URLs or author/name identities found.');
