from pathlib import Path

p=Path('apps/Sports-Info/Sports Info.js')
s=p.read_text(encoding='utf-8')  # universal newline conversion also normalizes CRLF -> LF


def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'missing patch marker: {label}')
    if s.count(old)!=1:
        raise SystemExit(f'patch marker not unique ({s.count(old)}): {label}')
    s=s.replace(old,new,1)

rep('// Sports Info v2.5.26','// Sports Info v2.5.27','header version')
rep('const APP_VERSION = "2.5.26";','const APP_VERSION = "2.5.27";','app version')

rep(
'''async function logo(url,key){if(!url)return null;const p=logoCachePath(url,key);try{if(fm.fileExists(p)){try{return fm.readImage(p)}catch(_){try{fm.remove(p)}catch(__){}}}const r=new Request(url);r.timeoutInterval=API_TIMEOUT;const i=await r.loadImage();fm.writeImage(p,i);return i}catch(_){return null}}''',
'''async function logo(url,key){if(!url)return null;const p=logoCachePath(url,key);try{if(fm.fileExists(p)){try{return fm.readImage(p)}catch(_){try{fm.remove(p)}catch(__){}}}if(config.runsInWidget)return null;const r=new Request(url);r.timeoutInterval=API_TIMEOUT;const i=await r.loadImage();fm.writeImage(p,i);return i}catch(_){return null}}''',
'background logos cache-only')

rep(
'''function runStatusRow(s){const r=runStatusRead();if(!r)return{label:`🕓 ${tx(s,"diagLastRun")}`,state:"off",detail:tx(s,"neverRun")};const when=new Date(r.ts).toLocaleString(s.language||"en",{day:"2-digit",month:"2-digit",hour:"2-digit",minute:"2-digit"});const detail=`${when} · v${r.version||"?"}${r.ok?"":` · ${r.error||tx(s,"error")}`}`;return{label:`🕓 ${tx(s,"diagLastRun")}`,state:r.ok?"ok":"error",detail}}''',
'''function runStatusRow(s){const r=runStatusRead();if(!r)return{label:`🕓 ${tx(s,"diagLastRun")}`,state:"off",detail:tx(s,"neverRun")};const when=new Date(r.ts).toLocaleString(s.language||"en",{day:"2-digit",month:"2-digit",hour:"2-digit",minute:"2-digit"}),source=String(r.source||"").toUpperCase();const detail=`${when} · v${r.version||"?"}${source?` · ${source}`:""}${r.ok?"":` · ${r.error||tx(s,"error")}`}`;return{label:`🕓 ${tx(s,"diagLastRun")}`,state:r.ok?"ok":"error",detail}}''',
'diagnostics source')

rep(
'''async function widget(s,family){const budgetMs=config.runsInWidget?20000:28000;const d=await dataWithBudget(s,budgetMs);runStatusWrite(d.source!=="error",d.source,null,family);const p=pal(s),w=new ListWidget();w.backgroundColor=p.bg;''',
'''async function widget(s,family){const budgetMs=config.runsInWidget?12000:24000;const d=await dataWithBudget(s,budgetMs);runStatusWrite(d.source!=="error",d.source,null,family);const p=pal(s),w=new ListWidget();try{const u=URLScheme.forRunningScript();w.url=u+(u.includes("?")?"&":"?")+`sportsTap=1&sportsFamily=${encodeURIComponent(family)}`}catch(_){}w.backgroundColor=p.bg;''',
'widget budget and tap family')

rep(
'''function fillLeagues(){const sid=document.getElementById('sportId').value,l=document.getElementById('leagueId'),items=leagues(sid);state=collect();switchLayoutSport(sid);state.sportId=sid;l.innerHTML='';items.forEach((x,i)=>{const o=document.createElement('option');o.value=x.id;o.textContent=(x.flag||'')+' '+(x[initial.language]||x.en||x.id);l.appendChild(o)});resetTeam();save()}document.getElementById('sportId').addEventListener('change',fillLeagues);document.getElementById('leagueId').addEventListener('change',()=>{resetTeam();save()});document.querySelectorAll('input,select').forEach(x=>{if(['sportId','leagueId','teamId'].includes(x.id))return;x.addEventListener('change',save);if(x.type==='number'||x.type==='color')x.addEventListener('input',save)});document.getElementById('teamId').addEventListener('change',save);''',
'''function fillLeagues(){const sid=document.getElementById('sportId').value,l=document.getElementById('leagueId'),items=leagues(sid);state=collect();switchLayoutSport(sid);state.sportId=sid;l.innerHTML='';items.forEach((x,i)=>{const o=document.createElement('option');o.value=x.id;o.textContent=(x.flag||'')+' '+(x[initial.language]||x.en||x.id);l.appendChild(o)});resetTeam();commitNow()}document.getElementById('sportId').addEventListener('change',fillLeagues);document.getElementById('leagueId').addEventListener('change',()=>{resetTeam();commitNow()});document.querySelectorAll('input,select').forEach(x=>{if(['sportId','leagueId','teamId'].includes(x.id))return;x.addEventListener('change',commitNow);if(x.type==='number'||x.type==='color')x.addEventListener('input',save)});document.getElementById('teamId').addEventListener('change',commitNow);''',
'immediate settings persistence')

rep(
'''let SETTINGS=await firstLanguage(loadSettings());
const PREVIEW_FAMILY=String(args.queryParameters?.sportsPreview||"");
if(config.runsInWidget){
  await widget(SETTINGS,config.widgetFamily||"medium")
}else if(["small","medium","large"].includes(PREVIEW_FAMILY)){
  const w=await widget(SETTINGS,PREVIEW_FAMILY);
  if(PREVIEW_FAMILY==="small")await w.presentSmall();else if(PREVIEW_FAMILY==="large")await w.presentLarge();else await w.presentMedium();
  await settings(SETTINGS)
}else{
  // Tapped from the Home Screen / run manually: refresh data, prime the cache and
  // the widget for the next render, then open Settings. On an outage this falls
  // back to cache inside data(); autoRefreshMinutes() then asks iOS to retry sooner.
  try{await widget(SETTINGS,"medium")}catch(e){runStatusWrite(false,"error",e,"medium")}
  await settings(SETTINGS)
}
Script.complete();''',
'''let SETTINGS=await firstLanguage(loadSettings());
const PREVIEW_FAMILY=String(args.queryParameters?.sportsPreview||"");
const TAP_FAMILY=["small","medium","large"].includes(String(args.queryParameters?.sportsFamily||""))?String(args.queryParameters.sportsFamily):"medium";
if(config.runsInWidget){
  const fam=config.widgetFamily||"medium";
  try{await widget(SETTINGS,fam)}catch(e){runStatusWrite(false,"error",e,fam);throw e}
}else if(["small","medium","large"].includes(PREVIEW_FAMILY)){
  const w=await widget(SETTINGS,PREVIEW_FAMILY);
  if(PREVIEW_FAMILY==="small")await w.presentSmall();else if(PREVIEW_FAMILY==="large")await w.presentLarge();else await w.presentMedium();
  await settings(SETTINGS)
}else{
  // Home Screen tap/manual run: refresh the exact tapped family, then open Settings.
  try{await widget(SETTINGS,TAP_FAMILY)}catch(e){runStatusWrite(false,"error",e,TAP_FAMILY)}
  await settings(SETTINGS)
}
Script.complete();''',
'main tap/background flow')

for marker in [
    'const APP_VERSION = "2.5.27";',
    'if(config.runsInWidget)return null;',
    'config.runsInWidget?12000:24000',
    'URLScheme.forRunningScript()',
    'sportsTap=1&sportsFamily=',
    "resetTeam();commitNow()",
    "x.addEventListener('change',commitNow)",
    "document.getElementById('teamId').addEventListener('change',commitNow)",
    'const TAP_FAMILY=',
    'await widget(SETTINGS,TAP_FAMILY)',
]:
    assert marker in s, marker

# Explicitly keep LF so package parity is stable on Actions/Linux.
p.write_text(s.replace('\r\n','\n').replace('\r','\n'),encoding='utf-8',newline='\n')
print('patched Sports Info 2.5.27 refresh + current sport persistence')
