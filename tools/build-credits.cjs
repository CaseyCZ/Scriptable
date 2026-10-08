const fs=require('fs');
const vm=require('vm');

const index=fs.readFileSync('index.html','utf8');
const extra=fs.readFileSync('community-extra.js','utf8');

const match=index.match(/const communityApps\s*=\s*(\[[\s\S]*?\n\s*\]);/);
if(!match) throw new Error('communityApps registry not found in index.html');
const builtIn=vm.runInNewContext('('+match[1]+')',Object.create(null),{timeout:1000});

const sandbox={window:{}};
vm.createContext(sandbox);
vm.runInContext(extra,sandbox,{timeout:3000});
const extended=Array.isArray(sandbox.window.communityExtraApps)?sandbox.window.communityExtraApps:[];

const clean=v=>String(v||'').trim();
const seen=new Set();
const items=[];
for(const app of [...builtIn,...extended]){
  const name=clean(app.name),author=clean(app.author),source=clean(app.source),file=clean(app.file);
  const key=(source||file||author+'|'+name).toLowerCase();
  if(!name||!author||seen.has(key)) continue;
  seen.add(key);
  items.push({name,author,source,file,category:clean(app.category)});
}
items.sort((a,b)=>a.author.localeCompare(b.author,'en',{sensitivity:'base'})||a.name.localeCompare(b.name,'en',{sensitivity:'base'}));
const authors={};
for(const item of items){
  (authors[item.author]??=[]).push({name:item.name,source:item.source||item.file});
}
const output={generatedAt:new Date().toISOString(),total:items.length,authorCount:Object.keys(authors).length,authors};
fs.mkdirSync('data',{recursive:true});
fs.writeFileSync('data/credits.json',JSON.stringify(output,null,2)+'\n');
console.log(`Credits generated: ${output.total} projects / ${output.authorCount} authors`);
