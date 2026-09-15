from pathlib import Path
import re

p=Path('apps/Sports-Info/Sports Info.js')
s=p.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.5.18";' in s
assert 'function layoutRangeDetail' in s
assert 'function commitNow()' in s

s=s.replace('// Sports Info v2.5.18','// Sports Info v2.5.19',1)
s=s.replace('const APP_VERSION = "2.5.18";','const APP_VERSION = "2.5.19";',1)

old='const DEFAULTS={language:null,sportId:"football",leagueId:"cze.1",teamId:"",teamName:"",showLive:true,showLast:true,showNext:true,showTable:true,showForm:true,showLogos:true,maxMatches:4,theme:"auto",accent:"#38bdf8",background:"#0b1020",panelColor:"#111827",textColor:"#f8fafc",mutedColor:"#94a3b8",liveColor:"#f87171",winColor:"#86efac",compact:false,refreshMinutes:15,layout:LAYOUT_DEFAULTS,apiEspnBase:'
new='const DEFAULTS={language:null,sportId:"football",leagueId:"cze.1",teamId:"",teamName:"",showLive:true,showLast:true,showNext:true,showTable:true,showForm:true,showLogos:true,maxMatches:4,theme:"auto",accent:"#38bdf8",background:"#0b1020",panelColor:"#111827",textColor:"#f8fafc",mutedColor:"#94a3b8",liveColor:"#f87171",winColor:"#86efac",compact:false,refreshMinutes:15,layout:LAYOUT_DEFAULTS,sportLayouts:{},apiEspnBase:'
assert old in s
s=s.replace(old,new,1)

new_merge=r'''const LAYOUT_RANGES={teamWidth:[48,150],scoreWidth:[14,70],teamFont:[7,15],scoreFont:[10,26],logoSize:[8,24],logoGap:[0,10],cardPaddingX:[0,18],listDateWidth:[30,60],listTeamWidth:[72,135],listScoreWidth:[36,70],tableTeamWidth:[82,135],tableWideWidth:[24,38],tableNarrowWidth:[18,32],tableHeaderFont:[7,12],tableFont:[8,14],tableTeamFont:[9,14]};
function normalizeLayout(raw){
  const out=clone(LAYOUT_DEFAULTS),input=raw||{};
  for(const family of ["small","medium","large"]){
    Object.assign(out[family],input?.[family]||{});const L=out[family];
    for(const [k,r] of Object.entries(LAYOUT_RANGES))if(k in L){const n=Number(L[k]),fallback=LAYOUT_DEFAULTS[family][k]??r[0];L[k]=clamp(Number.isFinite(n)?n:fallback,r[0],r[1])}
    if(!["edge","center","left","right"].includes(L.teamAlign))L.teamAlign=LAYOUT_DEFAULTS[family].teamAlign;
    if(family==="large"&&!['center','right'].includes(L.tableAlign))L.tableAlign='center'
  }
  return out
}
function merge(raw){
  const input=raw||{},s=Object.assign(clone(DEFAULTS),input);
  if(!["cs","en","de","es"].includes(s.language))s.language=null;
  if(!SPORTS.some(x=>x.id===s.sportId))s.sportId=DEFAULTS.sportId;
  const ls=leaguesForSport(s.sportId);if(!ls.some(x=>x.id===s.leagueId))s.leagueId=ls[0]?.id||DEFAULTS.leagueId;
  const legacy=normalizeLayout(input.layout||LAYOUT_DEFAULTS),profiles=input.sportLayouts&&typeof input.sportLayouts==="object"?input.sportLayouts:{};
  s.sportLayouts={};for(const sp of SPORTS)s.sportLayouts[sp.id]=normalizeLayout(profiles[sp.id]||legacy);
  s.layout=clone(s.sportLayouts[s.sportId]);
  s.maxMatches=clamp(Number(s.maxMatches)||4,1,8);s.refreshMinutes=clamp(Number(s.refreshMinutes)||15,5,60);if(!["auto","dark","light","custom"].includes(s.theme))s.theme="auto";for(const k of["accent","background","panelColor","textColor","mutedColor","liveColor","winColor"])if(!/^#[0-9a-fA-F]{6}$/.test(String(s[k]||"")))s[k]=DEFAULTS[k];
  for(const k of["apiEspnBase","apiFotmobBase","apiSofaBase","apiSportsApiBase"])s[k]=String(s[k]||DEFAULTS[k]).replace(/\/+$/,"");s.sportsApiKey=String(s.sportsApiKey||"").trim();return s
}'''
s,n=re.subn(r'function merge\(raw\)\{.*?\n\}\n(?=function loadSettings)',new_merge+'\n',s,count=1,flags=re.S)
assert n==1, f'merge replacement count {n}'

old='function layoutFor(s,family){return s.layout?.[family]||LAYOUT_DEFAULTS[family]||LAYOUT_DEFAULTS.medium}'
new='function layoutFor(s,family){return s.sportLayouts?.[s.sportId]?.[family]||s.layout?.[family]||LAYOUT_DEFAULTS[family]||LAYOUT_DEFAULTS.medium}'
assert old in s
s=s.replace(old,new,1)

subs={
'layoutSub:"Každá velikost widgetu má vlastní nastavení."':'layoutSub:"Každý sport i každá velikost widgetu má vlastní Layout. Změny se ukládají jen pro právě vybraný sport."',
'layoutSub:"Each widget size has its own independent layout settings."':'layoutSub:"Each sport and widget size has its own Layout. Changes are saved only for the currently selected sport."',
'layoutSub:"Jede Widget-Größe hat eigene Layout-Einstellungen."':'layoutSub:"Jede Sportart und Widget-Größe hat ein eigenes Layout. Änderungen gelten nur für die aktuell gewählte Sportart."',
'layoutSub:"Cada tamaño tiene su propia configuración de diseño."':'layoutSub:"Cada deporte y tamaño de widget tiene su propio Layout. Los cambios se guardan solo para el deporte seleccionado."'
}
for a,b in subs.items():
    assert a in s
    s=s.replace(a,b,1)

old='function html(s){const L=T[s.language||"en"],H=WIDGET_HELP[s.language||"en"]||WIDGET_HELP.en,sp=sport(s),lm=league(s),sportOpts='
new='function html(s){const L=T[s.language||"en"],H=WIDGET_HELP[s.language||"en"]||WIDGET_HELP.en,sp=sport(s),lm=league(s),layoutSportLabel=`${sp.icon} ${sportName(s)}`,sportOpts='
assert old in s
s=s.replace(old,new,1)

replacements=[
('<div class="screen" id="layout">${back}<div class="screenTitle">📐 ${esc(lt(s,"layout"))}</div><div class="screenSub">${esc(lt(s,"layoutSub"))}</div><div class="card">','<div class="screen" id="layout">${back}<div class="screenTitle">📐 ${esc(lt(s,"layout"))}</div><div class="screenSub">${esc(lt(s,"layoutSub"))}</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b></div><div class="card">'),
('<div class="screen" id="layoutSmall">${back.replace("showScreen(\'home\')","showScreen(\'layout\')")}<div class="screenTitle">▣ ${esc(lt(s,"small"))}</div><button class="previewBtn presetBtn" onclick="preview(\'small\')">👁 ${esc(lt(s,"preview"))}</button><div class="card">','<div class="screen" id="layoutSmall">${back.replace("showScreen(\'home\')","showScreen(\'layout\')")}<div class="screenTitle">▣ ${esc(lt(s,"small"))}</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b></div><button class="previewBtn presetBtn" onclick="preview(\'small\')">👁 ${esc(lt(s,"preview"))}</button><div class="card">'),
('<div class="screen" id="layoutMedium">${back.replace("showScreen(\'home\')","showScreen(\'layout\')")}<div class="screenTitle">▰ ${esc(lt(s,"medium"))}</div><button class="previewBtn presetBtn" onclick="preview(\'medium\')">👁 ${esc(lt(s,"preview"))}</button><div class="card">','<div class="screen" id="layoutMedium">${back.replace("showScreen(\'home\')","showScreen(\'layout\')")}<div class="screenTitle">▰ ${esc(lt(s,"medium"))}</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b></div><button class="previewBtn presetBtn" onclick="preview(\'medium\')">👁 ${esc(lt(s,"preview"))}</button><div class="card">'),
('<div class="screen" id="layoutLarge">${back.replace("showScreen(\'home\')","showScreen(\'layout\')")}<div class="screenTitle">▦ ${esc(lt(s,"large"))}</div><button class="previewBtn presetBtn" onclick="preview(\'large\')">👁 ${esc(lt(s,"preview"))}</button>','<div class="screen" id="layoutLarge">${back.replace("showScreen(\'home\')","showScreen(\'layout\')")}<div class="screenTitle">▦ ${esc(lt(s,"large"))}</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b></div><button class="previewBtn presetBtn" onclick="preview(\'large\')">👁 ${esc(lt(s,"preview"))}</button>')]
for a,b in replacements:
    assert a in s, a[:80]
    s=s.replace(a,b,1)

new_collect=r'''const LAYOUT_MAP={small:['TeamWidth','ScoreWidth','TeamFont','ScoreFont','LogoSize','LogoGap','CardPaddingX'],medium:['TeamWidth','ScoreWidth','TeamFont','ScoreFont','LogoSize','LogoGap','CardPaddingX','ListDateWidth','ListTeamWidth','ListScoreWidth'],large:['TeamWidth','ScoreWidth','TeamFont','ScoreFont','LogoSize','LogoGap','CardPaddingX','ListDateWidth','ListTeamWidth','ListScoreWidth','TableTeamWidth','TableWideWidth','TableNarrowWidth','TableHeaderFont','TableFont','TableTeamFont']};let layoutSportId=state.sportId;
function cloneProfile(v){return JSON.parse(JSON.stringify(v||LAYOUT_DEFAULTS))}
function readLayoutProfile(base){const out=cloneProfile(base);for(const [f,keys] of Object.entries(LAYOUT_MAP)){for(const suffix of keys){const id='layout'+f[0].toUpperCase()+f.slice(1)+suffix,e=document.getElementById(id);if(e&&String(e.value).trim()!==''){const key=suffix[0].toLowerCase()+suffix.slice(1),n=Number(e.value);if(Number.isFinite(n))out[f][key]=n}}const ae=document.getElementById('layout'+f[0].toUpperCase()+f.slice(1)+'TeamAlign');if(ae)out[f].teamAlign=ae.value}const ta=document.getElementById('layoutLargeTableAlign');if(ta)out.large.tableAlign=ta.value;return out}
function writeLayoutProfile(profile){const q=cloneProfile(profile);for(const [f,keys] of Object.entries(LAYOUT_MAP)){for(const suffix of keys){const id='layout'+f[0].toUpperCase()+f.slice(1)+suffix,e=document.getElementById(id),key=suffix[0].toLowerCase()+suffix.slice(1);if(e&&q[f]?.[key]!==undefined)e.value=q[f][key]}const ae=document.getElementById('layout'+f[0].toUpperCase()+f.slice(1)+'TeamAlign');if(ae&&q[f]?.teamAlign)ae.value=q[f].teamAlign}const ta=document.getElementById('layoutLargeTableAlign');if(ta&&q.large?.tableAlign)ta.value=q.large.tableAlign}
function sportLayoutLabel(id){const x=CATALOG.find(v=>v.id===id)||CATALOG[0];return `${x.icon||''} ${x[initial.language]||x.en||x.id}`.trim()}
function updateLayoutSportBadges(id){document.querySelectorAll('.layoutSportName').forEach(e=>e.textContent=sportLayoutLabel(id))}
function switchLayoutSport(id){state.sportLayouts=state.sportLayouts||{};state.sportLayouts[layoutSportId]=readLayoutProfile(state.sportLayouts[layoutSportId]||state.layout||LAYOUT_DEFAULTS);layoutSportId=id;const next=cloneProfile(state.sportLayouts[id]||LAYOUT_DEFAULTS);state.sportLayouts[id]=next;state.layout=cloneProfile(next);writeLayoutProfile(next);updateLayoutSportBadges(id)}
function collect(){const z={...state};z.sportId=document.getElementById('sportId')?.value||z.sportId;z.leagueId=document.getElementById('leagueId')?.value||z.leagueId;const t=document.getElementById('teamId');if(t){z.teamId=t.value;z.teamName=t.value?(t.options[t.selectedIndex]?.text||''):''}['showLive','showLast','showNext','showTable','showForm','showLogos','compact'].forEach(k=>{const e=document.getElementById(k);if(e)z[k]=e.checked});for(const k of['maxMatches','refreshMinutes']){const e=document.getElementById(k);if(e)z[k]=Number(e.value)};z.sportLayouts=JSON.parse(JSON.stringify(state.sportLayouts||{}));z.sportLayouts[layoutSportId]=readLayoutProfile(z.sportLayouts[layoutSportId]||state.layout||LAYOUT_DEFAULTS);z.layout=cloneProfile(z.sportLayouts[z.sportId]||LAYOUT_DEFAULTS);for(const k of['theme','accent','background','panelColor','textColor','mutedColor','liveColor','winColor','apiEspnBase','apiFotmobBase','apiOneFootballFeedBase','apiOneFootballScoresBase','apiSofaBase','apiSportsApiBase','sportsApiKey']){const e=document.getElementById(k);if(e)z[k]=e.value}return z}'''
s,n=re.subn(r'function collect\(\)\{.*?return z\}(?=let timer;)',new_collect,s,count=1,flags=re.S)
assert n==1, f'collect replacement count {n}'

old="function fillLeagues(){const sid=document.getElementById('sportId').value,l=document.getElementById('leagueId'),items=leagues(sid);l.innerHTML='';items.forEach((x,i)=>{const o=document.createElement('option');o.value=x.id;o.textContent=(x.flag||'')+' '+(x[initial.language]||x.en||x.id);l.appendChild(o)});resetTeam();save()}"
new="function fillLeagues(){const sid=document.getElementById('sportId').value,l=document.getElementById('leagueId'),items=leagues(sid);state=collect();switchLayoutSport(sid);state.sportId=sid;l.innerHTML='';items.forEach((x,i)=>{const o=document.createElement('option');o.value=x.id;o.textContent=(x.flag||'')+' '+(x[initial.language]||x.en||x.id);l.appendChild(o)});resetTeam();save()}"
assert old in s
s=s.replace(old,new,1)

old="function resetLayout(family){state=collect();state.layout=state.layout||JSON.parse(JSON.stringify(LAYOUT_DEFAULTS));state.layout[family]=JSON.parse(JSON.stringify(LAYOUT_DEFAULTS[family]));const prefix='layout'+family[0].toUpperCase()+family.slice(1);for(const [k,v] of Object.entries(state.layout[family])){const id=prefix+k[0].toUpperCase()+k.slice(1),e=document.getElementById(id);if(e)e.value=v}save()}"
new="function resetLayout(family){state=collect();state.sportLayouts=state.sportLayouts||{};const profile=cloneProfile(state.sportLayouts[layoutSportId]||LAYOUT_DEFAULTS);profile[family]=cloneProfile(LAYOUT_DEFAULTS)[family];state.sportLayouts[layoutSportId]=profile;state.layout=cloneProfile(profile);writeLayoutProfile(profile);commitNow()}"
assert old in s
s=s.replace(old,new,1)

needle="document.getElementById('teamId').addEventListener('change',save);"
assert needle in s
init="state.sportLayouts=state.sportLayouts||{};state.sportLayouts[layoutSportId]=cloneProfile(state.sportLayouts[layoutSportId]||state.layout||LAYOUT_DEFAULTS);state.layout=cloneProfile(state.sportLayouts[layoutSportId]);writeLayoutProfile(state.layout);updateLayoutSportBadges(layoutSportId);"
s=s.replace(needle,needle+init,1)

for marker in ['const APP_VERSION = "2.5.19";','sportLayouts:{}','function normalizeLayout(raw)','s.sportLayouts[sp.id]=normalizeLayout','function switchLayoutSport(id)','z.sportLayouts[layoutSportId]=readLayoutProfile','state=collect();switchLayoutSport(sid)','class="layoutSportName"']:
    assert marker in s, marker
p.write_text(s,encoding='utf-8')
