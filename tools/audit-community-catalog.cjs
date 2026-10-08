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
function installUrls(app){return [...new Set([app.file,...((app.variants||[]).map(v=>v&&v.file))].map(canonicalUrl).filter(Boolean))]}
function githubRepoKey(value){
  if(!value)return '';
  try{
    const u=new URL(String(value));
    if(u.hostname.toLowerCase()!=='github.com')return '';
    const p=u.pathname.split('/').filter(Boolean);
    return p.length>=2?`${p[0].toLowerCase()}/${p[1].toLowerCase()}`:'';
  }catch(_){return ''}
}
function variantCoreName(value){
  const stop=new Set(['widget','widgets','script','scriptable','ios','official','open','openf1','classic','legacy','new','old','lite','pro','free','plus','v1','v2','v3','version','variant']);
  const tokens=normalizedText(value).split(' ').filter(Boolean).filter(t=>!stop.has(t)&&!/^v\d+$/.test(t));
  const out=[];
  for(const token of tokens)if(out[out.length-1]!==token)out.push(token);
  return out.join(' ');
}
function previewKey(value){
  const url=canonicalUrl(value);
  if(!url||url.includes('opengraph.githubassets.com'))return '';
  return url;
}

const rows=[...builtins.map(app=>({app,where:'index.html'})),...extras.map(app=>({app,where:'community-extra.js'}))];
const seenUrls=new Map();
const seenNames=new Map();
const repoCoreGroups=new Map();
const previewGroups=new Map();
const errors=[];
const warnings=[];

for(const {app,where} of rows){
  const label=`${where}: ${app.author||'?'} / ${app.name||'?'}`;
  const urls=installUrls(app);
  if(!urls.length)errors.push(`${label} has no install URL`);
  for(const url of urls){
    if(seenUrls.has(url))errors.push(`duplicate install URL\n  first: ${seenUrls.get(url)}\n  again: ${label}\n  URL: ${url}`);
    else seenUrls.set(url,label);
  }

  const nk=nameKey(app);
  if(nk!=='|'){
    if(seenNames.has(nk))errors.push(`duplicate author + name\n  first: ${seenNames.get(nk)}\n  again: ${label}`);
    else seenNames.set(nk,label);
  }

  const repo=githubRepoKey(app.source);
  const core=variantCoreName(app.name);
  if(repo&&core){
    const key=`${repo}|${core}`;
    const list=repoCoreGroups.get(key)||[];
    list.push({label,name:app.name,urls});
    repoCoreGroups.set(key,list);
  }

  const preview=previewKey(app.preview);
  if(repo&&preview){
    const key=`${repo}|${preview}`;
    const list=previewGroups.get(key)||[];
    list.push({label,name:app.name});
    previewGroups.set(key,list);
  }
}

for(const [key,items] of repoCoreGroups){
  if(items.length<2)continue;
  const [repo,core]=key.split('|');
  warnings.push(`possible variants: same GitHub project + normalized name\n  repo: ${repo}\n  core: ${core}\n  ${items.map(x=>x.label).join('\n  ')}`);
}
for(const [key,items] of previewGroups){
  if(items.length<2)continue;
  const [repo]=key.split('|');
  const names=new Set(items.map(x=>normalizedText(x.name)));
  if(names.size<2)continue;
  warnings.push(`possible duplicate/variant: same project + same preview image\n  repo: ${repo}\n  ${items.map(x=>x.label).join('\n  ')}`);
}

console.log(`Community catalog audit: ${builtins.length} built-in + ${extras.length} extra = ${rows.length} projects`);
if(warnings.length){
  console.warn(`Review ${warnings.length} possible duplicate/variant group(s):`);
  for(const warning of warnings)console.warn(`\n- ${warning}`);
}
if(errors.length){
  console.error(`Found ${errors.length} duplicate/catalog error(s):`);
  for(const err of errors)console.error(`\n- ${err}`);
  process.exit(1);
}
console.log('OK: no duplicate install URLs or author/name identities found.');
