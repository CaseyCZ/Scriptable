from pathlib import Path

p = Path('apps/Sideload-Watch/Sideload Watch.js')
s = p.read_text(encoding='utf-8')

if 'const APP_VERSION = "0.2.25";' not in s:
    print('Sideload Watch source is already newer than v0.2.25; skipping one-time patch')
    raise SystemExit(0)

s = s.replace('// Sideload Watch v0.2.25', '// Sideload Watch v0.2.26', 1)
s = s.replace('const APP_VERSION = "0.2.25";', 'const APP_VERSION = "0.2.26";', 1)

old = '''function resetState(){try{if(fm.fileExists(statePath))fm.remove(statePath)}catch(_){}}

function cachedStatus(settings,error=null){'''
new = '''function resetState(){try{if(fm.fileExists(statePath))fm.remove(statePath)}catch(_){}}
function catalogWithWatchedFallback(catalog,settings){
  const base=normalizeCatalog(catalog||{}),sources=base.sources.slice(),knownIds=new Set(sources.map(src=>String(src.id||""))),state=loadState(),groups=new Map();
  for(const item of settings.watched||[]){
    const id=String(item.sourceId||"").trim();
    if(!id||knownIds.has(id))continue;
    if(!groups.has(id))groups.set(id,[]);
    groups.get(id).push(item)
  }
  for(const [id,items] of groups){
    const known=items.map(item=>state.lastCurrent?.[watchKey(item)]).find(Boolean)||{};
    const withURL=items.find(item=>String(item.sourceURL||"").trim());
    const sourceURL=String(withURL?.sourceURL||known.sourceURL||"");
    const apps=items.map(item=>{
      const prev=state.lastCurrent?.[watchKey(item)]||{};
      return{
        name:item.name,
        bundleIdentifier:item.bundleIdentifier||"",
        version:String(prev.version||"—"),
        iconURL:String(prev.iconURL||"")
      }
    });
    sources.push({
      id,
      name:String(known.sourceName||id),
      iconURL:String(known.iconURL||""),
      sourceURL,
      apps,
      missing:true
    })
  }
  return{...base,sources}
}

function cachedStatus(settings,error=null){'''
if old not in s:
    raise SystemExit('resetState insertion point not found')
s = s.replace(old, new, 1)

old = '''function sourceObj(id){return(catalog.sources||[]).find(x=>x.id===id)}
function sourceFailed(src){return failedSourceIds.has(String(src?.id||""))}
function updateSourceHealthUI(){const p=document.getElementById('sourceHealthPill');if(!p)return;if(sourceCacheOnly){p.hidden=false;p.textContent='⚠︎ '+${JSON.stringify('Cache')};return}const n=failedSourceIds.size;p.hidden=n===0;p.textContent=n?'⚠︎ '+n:''}'''
new = '''function sourceObj(id){return(catalog.sources||[]).find(x=>x.id===id)}
function missingWatchedSourceIds(){return new Set((catalog.sources||[]).filter(src=>src?.missing&&watchedForSource(src.id).length>0).map(src=>String(src.id||"")).filter(Boolean))}
function sourceFailed(src){return !!src?.missing||failedSourceIds.has(String(src?.id||""))}
function updateSourceHealthUI(){const p=document.getElementById('sourceHealthPill');if(!p)return;if(sourceCacheOnly){p.hidden=false;p.textContent='⚠︎ '+${JSON.stringify('Cache')};return}const ids=new Set([...failedSourceIds,...missingWatchedSourceIds()]);const n=ids.size;p.hidden=n===0;p.textContent=n?'⚠︎ '+n:''}'''
if old not in s:
    raise SystemExit('source health block not found')
s = s.replace(old, new, 1)

old = "  const rows=(catalog.sources||[]).filter(s=>!q||norm(s.name+' '+s.id).includes(q)).slice().sort((a,b)=>String(a.name||a.id||'').localeCompare(String(b.name||b.id||''),state.language||'en',{sensitivity:'base'}));"
new = """  const rows=(catalog.sources||[]).filter(s=>{
    const n=watchedForSource(s.id).length;
    if(s?.missing&&!n)return false;
    return !q||norm(s.name+' '+s.id).includes(q)
  }).slice().sort((a,b)=>String(a.name||a.id||'').localeCompare(String(b.name||b.id||''),state.language||'en',{sensitivity:'base'}));"""
if old not in s:
    raise SystemExit('renderSources rows line not found')
s = s.replace(old, new, 1)

old = "    const detail=document.createElement('div');detail.className='rowDetail';detail.textContent=(src.apps||[]).length+' '+${JSON.stringify(L.apps)}+' · '+n+' '+${JSON.stringify(L.selected)};"
new = "    const detail=document.createElement('div');detail.className='rowDetail';detail.textContent=(src.missing?${JSON.stringify(L.offline)}+' · ':'')+(src.apps||[]).length+' '+${JSON.stringify(L.apps)}+' · '+n+' '+${JSON.stringify(L.selected)};"
if old not in s:
    raise SystemExit('source detail line not found')
s = s.replace(old, new, 1)

old = '''  s=enrichWatchedSources(s,catalogResult.data);
  saveSettings(s);'''
new = '''  s=enrichWatchedSources(s,catalogResult.data);
  catalogResult={...catalogResult,data:catalogWithWatchedFallback(catalogResult.data,s)};
  saveSettings(s);'''
if old not in s:
    raise SystemExit('initial catalog merge point not found')
s = s.replace(old, new, 1)

old = '''          const r=await fetchCatalog(true);catalogResult=r;
          cur=enrichWatchedSources(cur,r.data);saveSettings(cur);
          await send(web,{action:"catalog",catalog:r.data,online:r.online,text:tx(cur,"catalogUpdated")});'''
new = '''          const r=await fetchCatalog(true);
          cur=enrichWatchedSources(cur,r.data);saveSettings(cur);
          const mergedCatalog=catalogWithWatchedFallback(r.data,cur);catalogResult={...r,data:mergedCatalog};
          await send(web,{action:"catalog",catalog:mergedCatalog,online:r.online,text:tx(cur,"catalogUpdated")});'''
if old not in s:
    raise SystemExit('refresh catalog merge point not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('Applied Sideload Watch v0.2.26 offline/missing source fix')
