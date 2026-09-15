from pathlib import Path

p=Path('apps/Sports-Info/Sports Info.js')
s=p.read_text(encoding='utf-8')


def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'missing patch marker: {label}')
    if s.count(old)!=1:
        raise SystemExit(f'patch marker not unique ({s.count(old)}): {label}')
    s=s.replace(old,new,1)

rep('// Sports Info v2.5.24','// Sports Info v2.5.25','header version')
rep('const APP_VERSION = "2.5.24";','const APP_VERSION = "2.5.25";','app version')
rep('const CACHE_FILE = "SportsInfo_cache.json";','const CACHE_FILE = "SportsInfo_cache.json";\nconst RUNTIME_FILE = "SportsInfo_runtime.json";','runtime constant')

rep(
'''const cachePath=fm.joinPath(fm.cacheDirectory(),CACHE_FILE);\nconst clone=o=>JSON.parse(JSON.stringify(o));''',
'''const cachePath=fm.joinPath(fm.cacheDirectory(),CACHE_FILE);\nconst runtimePath=fm.joinPath(fm.documentsDirectory(),RUNTIME_FILE);\nfunction runtimeRead(){try{return fm.fileExists(runtimePath)?JSON.parse(fm.readString(runtimePath))||{}:{}}catch(_){return{}}}\nfunction runtimeWrite(v){try{fm.writeString(runtimePath,JSON.stringify(v||{}))}catch(_){}}\nfunction runtimeError(e){return String(e?.message||e||"").slice(0,180)}\nfunction recordRuntime(d,mode,family){runtimeWrite({lastRun:Date.now(),version:APP_VERSION,mode:mode||"foreground",family:family||"medium",source:d?.source||"unknown",lastError:d?.error||""})}\nfunction recordRuntimeFailure(e,mode,family){runtimeWrite({lastRun:Date.now(),version:APP_VERSION,mode:mode||"foreground",family:family||"medium",source:"error",lastError:runtimeError(e)})}\nconst clone=o=>JSON.parse(JSON.stringify(o));''',
'runtime helpers')

rep(
'''const d={source:"online",at:Date.now(),live,done,next,current:(s.showLive?live[0]:null)||next[0]||done[0]||null,form:(s.teamId||s.teamName)?done.slice(0,5).map(e=>result(e,s)).filter(Boolean):[],table};cacheWrite(key,d);return d\n  }catch(e){console.log(e);const c=cacheRead(key);return c?.data?Object.assign({},c.data,{source:"cache",at:c.ts||c.data.at}):{source:"error",at:Date.now(),live:[],done:[],next:[],current:null,form:[],table:[]}}''',
'''const d={source:"online",at:Date.now(),error:"",live,done,next,current:(s.showLive?live[0]:null)||next[0]||done[0]||null,form:(s.teamId||s.teamName)?done.slice(0,5).map(e=>result(e,s)).filter(Boolean):[],table};cacheWrite(key,d);return d\n  }catch(e){console.log(e);const err=runtimeError(e),c=cacheRead(key);return c?.data?Object.assign({},c.data,{source:"cache",at:c.ts||c.data.at,error:err}):{source:"error",at:Date.now(),error:err,live:[],done:[],next:[],current:null,form:[],table:[]}}''',
'data error propagation')

old_diag='''function diagnosticPlaceholders(s){return[{label:`🌐 ${tx(s,"diagSource")}`,state:"idle",detail:sourceLabel(s)},{label:`👥 ${tx(s,"diagTeams")}`,state:"idle",detail:""},{label:`📊 ${tx(s,"diagTable")}`,state:"idle",detail:""},{label:`💾 ${tx(s,"diagCache")}`,state:fm.fileExists(cachePath)?"ok":"off",detail:fm.fileExists(cachePath)?tx(s,"cache"):""}]}\nasync function collectDiagnostics(s,onUpdate=null){let rows=[{label:`🌐 ${tx(s,"diagSource")}`,state:"checking",detail:sourceLabel(s)},{label:`👥 ${tx(s,"diagTeams")}`,state:"checking",detail:""},{label:`📊 ${tx(s,"diagTable")}`,state:"checking",detail:""},{label:`💾 ${tx(s,"diagCache")}`,state:fm.fileExists(cachePath)?"ok":"off",detail:fm.fileExists(cachePath)?tx(s,"cache"):""}];const publish=async()=>{if(onUpdate)try{await onUpdate(rows.map(x=>Object.assign({},x)))}catch(_){}};await publish();const jobs=[probe(`🌐 ${tx(s,"diagSource")}`,()=>sourceHealth(s),9000).then(async r=>{rows[0]=r;await publish()}),probe(`👥 ${tx(s,"diagTeams")}`,async()=>{const a=await teamsFor(s);return `${a.length} teams · endpoint OK`},10000).then(async r=>{rows[1]=r;await publish()}),probe(`📊 ${tx(s,"diagTable")}`,async()=>{const a=await standingsFor(s);return a.length?`${a.length} rows`:`0 rows · source does not expose standings here`},10000).then(async r=>{rows[2]=r;await publish()})];await Promise.all(jobs);return rows}'''
new_diag='''function runtimeLabels(s){const l=s.language||lang(),m={cs:{run:"Poslední spuštění",ver:"Verze skriptu",err:"Poslední chyba",none:"Bez chyby",bg:"pozadí",fg:"aplikace"},en:{run:"Last run",ver:"Script version",err:"Last error",none:"No error",bg:"background",fg:"app"},de:{run:"Letzter Lauf",ver:"Skriptversion",err:"Letzter Fehler",none:"Kein Fehler",bg:"Hintergrund",fg:"App"},es:{run:"Última ejecución",ver:"Versión del script",err:"Último error",none:"Sin error",bg:"segundo plano",fg:"app"}};return m[l]||m.en}\nfunction runtimeRows(s){const r=runtimeRead(),q=runtimeLabels(s),when=r.lastRun?new Date(r.lastRun).toLocaleString(s.language||"en",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"}):"–",mode=r.mode==="background"?q.bg:q.fg,detail=r.lastRun?`${when} · ${mode}${r.family?` · ${r.family}`:""}${r.source?` · ${r.source}`:""}`:"–";return[{label:`🕒 ${q.run}`,state:r.lastRun?"ok":"idle",detail},{label:`🧩 ${q.ver}`,state:(r.version||APP_VERSION)===APP_VERSION?"ok":"off",detail:`v${r.version||APP_VERSION}`},{label:`⚠️ ${q.err}`,state:r.lastError?"error":"ok",detail:r.lastError||q.none}]}\nfunction diagnosticPlaceholders(s){return[...runtimeRows(s),{label:`🌐 ${tx(s,"diagSource")}`,state:"idle",detail:sourceLabel(s)},{label:`👥 ${tx(s,"diagTeams")}`,state:"idle",detail:""},{label:`📊 ${tx(s,"diagTable")}`,state:"idle",detail:""},{label:`💾 ${tx(s,"diagCache")}`,state:fm.fileExists(cachePath)?"ok":"off",detail:fm.fileExists(cachePath)?tx(s,"cache"):""}]}\nasync function collectDiagnostics(s,onUpdate=null){const fixed=runtimeRows(s),base=fixed.length;let rows=[...fixed,{label:`🌐 ${tx(s,"diagSource")}`,state:"checking",detail:sourceLabel(s)},{label:`👥 ${tx(s,"diagTeams")}`,state:"checking",detail:""},{label:`📊 ${tx(s,"diagTable")}`,state:"checking",detail:""},{label:`💾 ${tx(s,"diagCache")}`,state:fm.fileExists(cachePath)?"ok":"off",detail:fm.fileExists(cachePath)?tx(s,"cache"):""}];const publish=async()=>{if(onUpdate)try{await onUpdate(rows.map(x=>Object.assign({},x)))}catch(_){}};await publish();const jobs=[probe(`🌐 ${tx(s,"diagSource")}`,()=>sourceHealth(s),9000).then(async r=>{rows[base]=r;await publish()}),probe(`👥 ${tx(s,"diagTeams")}`,async()=>{const a=await teamsFor(s);return `${a.length} teams · endpoint OK`},10000).then(async r=>{rows[base+1]=r;await publish()}),probe(`📊 ${tx(s,"diagTable")}`,async()=>{const a=await standingsFor(s);return a.length?`${a.length} rows`:`0 rows · source does not expose standings here`},10000).then(async r=>{rows[base+2]=r;await publish()})];await Promise.all(jobs);return rows}'''
rep(old_diag,new_diag,'runtime diagnostics')

rep(
'''function autoRefreshMinutes(s,d){if((d.live||[]).length)return 2;const n=(d.next||[])[0];if(n?.date){const ms=new Date(n.date).getTime()-Date.now();if(ms>0&&ms<=30*60000)return 5}return s.refreshMinutes}\nasync function widget(s,family){const d=await data(s),p=pal(s),w=new ListWidget();''',
'''function autoRefreshMinutes(s,d){if(d?.source==="cache"||d?.source==="error")return Math.min(5,s.refreshMinutes);if((d.live||[]).length)return 2;const n=(d.next||[])[0];if(n?.date){const ms=new Date(n.date).getTime()-Date.now();if(ms>0&&ms<=30*60000)return 5}return s.refreshMinutes}\nasync function widget(s,family){const d=await data(s),p=pal(s),w=new ListWidget();recordRuntime(d,config.runsInWidget?"background":"foreground",family);try{const u=URLScheme.forRunningScript();w.url=u+(u.includes("?")?"&":"?")+`sportsTap=1&sportsFamily=${encodeURIComponent(family)}`}catch(_){}''',
'refresh retry and tap url')

old_main='''let SETTINGS=await firstLanguage(loadSettings());\nconst PREVIEW_FAMILY=String(args.queryParameters?.sportsPreview||"");\nif(config.runsInWidget){\n  const w=await widget(SETTINGS,config.widgetFamily||"medium");Script.setWidget(w)\n}else if(["small","medium","large"].includes(PREVIEW_FAMILY)){\n  const w=await widget(SETTINGS,PREVIEW_FAMILY);\n  if(PREVIEW_FAMILY==="small")await w.presentSmall();else if(PREVIEW_FAMILY==="large")await w.presentLarge();else await w.presentMedium();\n  await settings(SETTINGS)\n}else await settings(SETTINGS);\nScript.complete();'''
new_main='''let SETTINGS=await firstLanguage(loadSettings());\nconst PREVIEW_FAMILY=String(args.queryParameters?.sportsPreview||"");\nconst TAP_FAMILY=["small","medium","large"].includes(String(args.queryParameters?.sportsFamily||""))?String(args.queryParameters.sportsFamily):"medium";\nif(config.runsInWidget){\n  try{const w=await widget(SETTINGS,config.widgetFamily||"medium");Script.setWidget(w)}catch(e){recordRuntimeFailure(e,"background",config.widgetFamily||"medium");throw e}\n}else if(["small","medium","large"].includes(PREVIEW_FAMILY)){\n  const w=await widget(SETTINGS,PREVIEW_FAMILY);\n  if(PREVIEW_FAMILY==="small")await w.presentSmall();else if(PREVIEW_FAMILY==="large")await w.presentLarge();else await w.presentMedium();\n  await settings(SETTINGS)\n}else{\n  try{await widget(SETTINGS,TAP_FAMILY)}catch(e){console.log(e);recordRuntimeFailure(e,"foreground",TAP_FAMILY)}\n  await settings(SETTINGS)\n}\nScript.complete();'''
rep(old_main,new_main,'main foreground/background flow')

# Release must contain the exact intended contracts.
for marker in [
    'const APP_VERSION = "2.5.25";',
    'const RUNTIME_FILE = "SportsInfo_runtime.json";',
    'function runtimeRows(s)',
    'd?.source==="cache"||d?.source==="error"',
    'URLScheme.forRunningScript()',
    'sportsTap=1&sportsFamily=',
    'const TAP_FAMILY=',
    'try{await widget(SETTINGS,TAP_FAMILY)}',
    'recordRuntimeFailure(e,"background"',
]:
    assert marker in s, marker

p.write_text(s,encoding='utf-8')
print('patched Sports Info 2.5.25 refresh/runtime behavior')
