from pathlib import Path

p=Path('apps/Sports-Info/Sports Info.js')
s=p.read_text(encoding='utf-8')

def rep(old,new,label):
    global s
    if old not in s:
        raise SystemExit(f'missing patch target: {label}')
    s=s.replace(old,new,1)

assert 'const APP_VERSION = "2.5.21";' in s, 'expected Sports Info 2.5.21'
rep('// Sports Info v2.5.21','// Sports Info v2.5.22','header version')
rep('const APP_VERSION = "2.5.21";','const APP_VERSION = "2.5.22";','app version')

# Per-sport AUTO/MANUAL mode for Large standings. Missing legacy value intentionally migrates to AUTO.
rep('layout:LAYOUT_DEFAULTS,sportLayouts:{},apiEspnBase:', 'layout:LAYOUT_DEFAULTS,sportLayouts:{},tableAutoBySport:{},apiEspnBase:', 'default auto map')
rep('s.sportLayouts={};for(const sp of SPORTS)s.sportLayouts[sp.id]=normalizeLayout(profiles[sp.id]||legacy);\n  s.layout=clone(s.sportLayouts[s.sportId]);',
'''s.sportLayouts={};for(const sp of SPORTS)s.sportLayouts[sp.id]=normalizeLayout(profiles[sp.id]||legacy);
  const autoProfiles=input.tableAutoBySport&&typeof input.tableAutoBySport==="object"?input.tableAutoBySport:{};s.tableAutoBySport={};for(const sp of SPORTS)s.tableAutoBySport[sp.id]=autoProfiles[sp.id]===undefined?true:!!autoProfiles[sp.id];
  s.layout=clone(s.sportLayouts[s.sportId]);''','merge auto map')

# Dynamic standings widths. AUTO packs columns according to actual visible data; MANUAL keeps stored values.
old='''function tableSlotLayout(s,cols){
  const L=layoutFor(s,"large"),stats=cols.slice(1,8),wide=L.tableWideWidth,narrow=L.tableNarrowWidth,total=4*wide+3*narrow,base=stats.reduce((a,_,i)=>a+(i<4?wide:narrow),0),scale=base?total/base:1;
  const statCols=stats.map(([key,label],i)=>[key,label,Math.max(18,Math.floor((i<4?wide:narrow)*scale))]);
  const used=statCols.reduce((a,c)=>a+c[2],0);if(statCols.length)statCols[statCols.length-1][2]+=total-used;
  return {teamCol:[cols[0][0],cols[0][1],L.tableTeamWidth],statCols,statsWidth:total}
}'''
new='''let LAST_AUTO_TABLE_LAYOUT=null;
function tableAutoEnabled(s){return s.tableAutoBySport?.[s.sportId]!==false}
function textWidthUnits(v){let u=0;for(const ch of String(v??"")){if(" 1Il|.,:'".includes(ch))u+=.36;else if("MW@%#".includes(ch))u+=.92;else if(/[0-9]/.test(ch))u+=.61;else if(/[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ]/.test(ch))u+=.69;else u+=.56}return u}
function tableTextWidth(v,font,bold=false){return Math.ceil(textWidthUnits(v)*font*(bold?1.06:1)+6)}
function automaticTableSlotLayout(s,cols,rows=[]){
  const L=layoutFor(s,"large"),stats=cols.slice(1,8),target=303,teamValues=[cols[0]?.[1]||"TÝM",...rows.map(x=>standingValue(x,"team"))];
  let teamWidth=clamp(Math.max(...teamValues.map(v=>tableTextWidth(v,L.tableTeamFont,true)))+(s.showLogos?18:0),60,180);
  const statCols=stats.map(([key,label])=>{const vals=[label,...rows.map(x=>standingValue(x,key))],need=Math.max(tableTextWidth(label,L.tableHeaderFont,true),...vals.map(v=>tableTextWidth(v,L.tableFont,key==="points")));const min=key==="score"?30:20,max=key==="score"?80:56;return[key,label,clamp(need,min,max)]});
  const minFor=key=>key==="score"?30:20;
  let statsWidth=statCols.reduce((a,c)=>a+c[2],0),overflow=teamWidth+4+statsWidth-target;
  if(overflow>0){const take=Math.min(overflow,teamWidth-60);teamWidth-=take;overflow-=take}
  while(overflow>0){let changed=false;for(const c of [...statCols].sort((a,b)=>b[2]-a[2])){const min=minFor(c[0]);if(c[2]>min){c[2]--;overflow--;changed=true;if(overflow<=0)break}}if(!changed)break}
  statsWidth=statCols.reduce((a,c)=>a+c[2],0);
  LAST_AUTO_TABLE_LAYOUT={teamWidth,statsWidth,totalWidth:teamWidth+4+statsWidth,columns:Object.fromEntries(statCols.map(c=>[c[0],c[2]]))};
  return {teamCol:[cols[0][0],cols[0][1],teamWidth],statCols,statsWidth,auto:true}
}
function tableSlotLayout(s,cols,rows=[]){
  if(tableAutoEnabled(s))return automaticTableSlotLayout(s,cols,rows);
  const L=layoutFor(s,"large"),stats=cols.slice(1,8),wide=L.tableWideWidth,narrow=L.tableNarrowWidth,total=4*wide+3*narrow,base=stats.reduce((a,_,i)=>a+(i<4?wide:narrow),0),scale=base?total/base:1;
  const statCols=stats.map(([key,label],i)=>[key,label,Math.max(18,Math.floor((i<4?wide:narrow)*scale))]);
  const used=statCols.reduce((a,c)=>a+c[2],0);if(statCols.length)statCols[statCols.length-1][2]+=total-used;
  LAST_AUTO_TABLE_LAYOUT=null;
  return {teamCol:[cols[0][0],cols[0][1],L.tableTeamWidth],statCols,statsWidth:total,auto:false}
}'''
rep(old,new,'table auto algorithm')
rep('const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football,{teamCol,statCols,statsWidth}=tableSlotLayout(s,cols),TL=layoutFor(s,"large");',
    'const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football,{teamCol,statCols,statsWidth}=tableSlotLayout(s,cols,rows),TL=layoutFor(s,"large");','table rows to layout')

# iPhone interaction styling.
rep('.previewBtn,.actionBtn{min-height:46px;', '.previewBtn,.actionBtn{min-height:48px;touch-action:manipulation;-webkit-tap-highlight-color:transparent;transition:transform .08s ease,opacity .08s ease;', 'button touch css')
rep('.navRow:active{background:var(--panel2)}', '.navRow:active{background:var(--panel2)}.navRow,button{touch-action:manipulation;-webkit-tap-highlight-color:transparent}.pressed{transform:scale(.97)!important;opacity:.72!important}.modeBox{margin:0 0 12px;padding:12px 14px;border:1px solid var(--border);border-radius:14px;background:var(--panel2)}.modeLine{display:flex;align-items:center;justify-content:space-between;gap:8px}.modeBadge{font-size:12px;font-weight:900;padding:5px 9px;border-radius:999px}.modeBadge.auto{color:#bbf7d0;background:#123523;border:1px solid #237a45}.modeBadge.manual{color:#fed7aa;background:#3a2412;border:1px solid #9a5b20}.modeInfo{font-size:12px;color:var(--muted);line-height:1.45;margin-top:7px}', 'touch and mode css')

# Replace only the Large layout screen with a mobile submenu + three focused screens.
start=s.index('<div class="screen" id="layoutLarge">')
end=s.index('<div class="screen" id="appearance">',start)
large='''<div class="screen" id="layoutLarge">${back.replace("showScreen('home')","showScreen('layout')")}<div class="screenTitle">▦ ${esc(lt(s,"large"))}</div><div class="screenSub">${esc(lt(s,"layoutSub"))}</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b></div><div class="card">${nav("layoutLargeMatch","🏟️","Match card")}${nav("layoutLargeTable","📊",lt(s,"table"))}${nav("layoutLargeLists","☷","Lists")}</div><button class="previewBtn presetBtn previewAction" data-preview="large" onclick="preview('large')">👁 ${esc(lt(s,"preview"))}</button></div>
<div class="screen" id="layoutLargeMatch">${back.replace("showScreen('home')","showScreen('layoutLarge')")}<div class="screenTitle">🏟️ Match card</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b> · Large</div><button class="previewBtn presetBtn previewAction" data-preview="large" onclick="preview('large')">👁 ${esc(lt(s,"preview"))}</button><div class="card">${layoutField(s,"layoutLargeTeamWidth",lt(s,"teamWidth"),s.layout.large.teamWidth,48,150,"teamWidth")}${layoutField(s,"layoutLargeScoreWidth",lt(s,"scoreWidth"),s.layout.large.scoreWidth,14,70,"scoreWidth")}${layoutField(s,"layoutLargeTeamFont",lt(s,"teamFont"),s.layout.large.teamFont,7,15,"teamFont")}${layoutField(s,"layoutLargeScoreFont",lt(s,"scoreFont"),s.layout.large.scoreFont,10,26,"scoreFont")}${layoutField(s,"layoutLargeLogoSize",lt(s,"logoSize"),s.layout.large.logoSize,8,24,"logoSize")}${layoutField(s,"layoutLargeLogoGap",lt(s,"logoGap"),s.layout.large.logoGap,0,10,"logoGap")}${layoutField(s,"layoutLargeCardPaddingX",lt(s,"cardPaddingX"),s.layout.large.cardPaddingX,0,18,"cardPaddingX")}${selectField("layoutLargeTeamAlign",lt(s,"teamAlign"),s.layout.large.teamAlign,[["edge",lt(s,"edge")],["center",lt(s,"center")],["left",lt(s,"left")],["right",lt(s,"right")]],lh(s,"teamAlign"))}</div><button class="actionBtn secondary presetBtn" onclick="resetLayoutSection('match')">↺ ${esc(lt(s,"reset"))}</button></div>
<div class="screen" id="layoutLargeTable">${back.replace("showScreen('home')","showScreen('layoutLarge')")}<div class="screenTitle">📊 ${esc(lt(s,"table"))}</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b> · Large</div><div class="modeBox"><div class="modeLine"><b>Layout tabulky</b><span id="tableModeBadge" class="modeBadge auto">AUTO</span></div><div id="tableModeInfo" class="modeInfo">AUTO počítá šířky z aktuálně zobrazených týmů a statistik.</div><div id="autoTableInfo" class="modeInfo"></div></div><button class="previewBtn presetBtn previewAction" data-preview="large" onclick="preview('large')">👁 ${esc(lt(s,"preview"))}</button><button class="actionBtn presetBtn" onclick="setTableAuto()">🤖 Automatický layout</button><div class="card">${layoutField(s,"layoutLargeTableTeamWidth",lt(s,"tableTeamWidth"),s.layout.large.tableTeamWidth,60,180,"tableTeamWidth")}${layoutField(s,"layoutLargeTableWideWidth",lt(s,"wideWidth"),s.layout.large.tableWideWidth,24,50,"wideWidth")}${layoutField(s,"layoutLargeTableNarrowWidth",lt(s,"narrowWidth"),s.layout.large.tableNarrowWidth,20,50,"narrowWidth")}${layoutField(s,"layoutLargeTableHeaderFont",lt(s,"headerFont"),s.layout.large.tableHeaderFont,7,12,"headerFont")}${layoutField(s,"layoutLargeTableFont",lt(s,"tableFont"),s.layout.large.tableFont,8,14,"tableFont")}${layoutField(s,"layoutLargeTableTeamFont",lt(s,"tableTeamFont"),s.layout.large.tableTeamFont,9,14,"tableTeamFont")}${selectField("layoutLargeTableAlign",lt(s,"tableAlign"),s.layout.large.tableAlign,[["center",lt(s,"center")],["right",lt(s,"right")]],lh(s,"tableAlign"))}</div><button class="actionBtn secondary presetBtn" onclick="resetLayoutSection('table')">↺ ${esc(lt(s,"reset"))}</button></div>
<div class="screen" id="layoutLargeLists">${back.replace("showScreen('home')","showScreen('layoutLarge')")}<div class="screenTitle">☷ Lists</div><div class="info">🏆 <b class="layoutSportName">${esc(layoutSportLabel)}</b> · Large</div><button class="previewBtn presetBtn previewAction" data-preview="large" onclick="preview('large')">👁 ${esc(lt(s,"preview"))}</button><div class="card">${layoutField(s,"layoutLargeListDateWidth",lt(s,"dateWidth"),s.layout.large.listDateWidth,30,60,"dateWidth")}${layoutField(s,"layoutLargeListTeamWidth",lt(s,"listTeamWidth"),s.layout.large.listTeamWidth,72,135,"listTeamWidth")}${layoutField(s,"layoutLargeListScoreWidth",lt(s,"listScoreWidth"),s.layout.large.listScoreWidth,36,70,"listScoreWidth")}</div><button class="actionBtn secondary presetBtn" onclick="resetLayoutSection('lists')">↺ ${esc(lt(s,"reset"))}</button></div>
'''
s=s[:start]+large+s[end:]

# Preview buttons outside Large get the dedicated preview class too.
s=s.replace('class="previewBtn presetBtn" onclick="preview(\'small\')"','class="previewBtn presetBtn previewAction" data-preview="small" onclick="preview(\'small\')"')
s=s.replace('class="previewBtn presetBtn" onclick="preview(\'medium\')"','class="previewBtn presetBtn previewAction" data-preview="medium" onclick="preview(\'medium\')"')

# WebView JS: nested Large screens save on exit; AUTO/MANUAL per sport; tactile iPhone feedback.
rep("/^layout(?:Small|Medium|Large)$/.test(active)", "/^layout(?:Small|Medium|Large)(?:Match|Table|Lists)?$/.test(active)", 'nested layout commit')
rep("function updateLayoutSportBadges(id){document.querySelectorAll('.layoutSportName').forEach(e=>e.textContent=sportLayoutLabel(id))}",
'''function updateLayoutSportBadges(id){document.querySelectorAll('.layoutSportName').forEach(e=>e.textContent=sportLayoutLabel(id));updateTableModeUI()}
function tableAutoUI(){state.tableAutoBySport=state.tableAutoBySport||{};return state.tableAutoBySport[layoutSportId]!==false}
function updateTableModeUI(){const b=document.getElementById('tableModeBadge'),i=document.getElementById('tableModeInfo');if(!b||!i)return;const a=tableAutoUI();b.textContent=a?'AUTO':'MANUAL';b.className='modeBadge '+(a?'auto':'manual');i.textContent=a?'AUTO počítá šířky z aktuálně zobrazených týmů a statistik.':'MANUAL používá uložené hodnoty tohoto sportu. Ruční změna zůstane jen u tohoto sportu.'}
function setTableMode(auto,commit=true){state.tableAutoBySport=state.tableAutoBySport||{};state.tableAutoBySport[layoutSportId]=!!auto;updateTableModeUI();if(commit)commitNow()}
function setTableAuto(){setTableMode(true,true);const x=document.getElementById('autoTableInfo');if(x)x.textContent='AUTO aktivní · skutečné šířky se zobrazí po Náhledu.'}
function markTableManual(){if(tableAutoUI())setTableMode(false,false);updateTableModeUI()}''','table mode UI')

# Add explicit iPhone input mode after DOM exists and mark table edits manual.
needle="document.getElementById('teamId').addEventListener('change',save);state.sportLayouts=state.sportLayouts||{};"
repl="document.getElementById('teamId').addEventListener('change',save);document.querySelectorAll('input[type=number]').forEach(e=>e.setAttribute('inputmode','numeric'));document.querySelectorAll('[id^=layoutLargeTable]').forEach(e=>{e.addEventListener('input',markTableManual);e.addEventListener('change',markTableManual)});document.addEventListener('touchstart',e=>{const x=e.target.closest('button,.navRow');if(x)x.classList.add('pressed')},{passive:true});for(const ev of['touchend','touchcancel'])document.addEventListener(ev,e=>{const x=e.target.closest('button,.navRow');if(x)x.classList.remove('pressed')},{passive:true});state.sportLayouts=state.sportLayouts||{};"
rep(needle,repl,'iphone listeners')

# Replace preview, recommended/reset helpers and add focused Large resets.
old="function preview(f){state=commitNow();const e=document.getElementById('previewMeta');if(e)e.textContent=UI.loading;document.querySelectorAll('.previewBtn').forEach(b=>b.disabled=true);emit('preview',{family:f,settings:state})}"
new="function preview(f){state=commitNow();const e=document.getElementById('previewMeta');if(e)e.textContent=UI.loading;document.querySelectorAll('.previewAction[data-preview=\"'+f+'\"]').forEach(b=>{b.disabled=true;if(!b.dataset.label)b.dataset.label=b.textContent;b.textContent='⏳ '+UI.loading});emit('preview',{family:f,settings:state})}"
rep(old,new,'preview scoped busy')
rep("function resetLayout(family){clearTimeout(timer);const current=collect(),sid=layoutSportId||current.sportId;current.sportLayouts=current.sportLayouts||{};const profile=cloneProfile(current.sportLayouts[sid]||LAYOUT_DEFAULTS);profile[family]=cloneProfile(LAYOUT_DEFAULTS)[family];current.sportLayouts[sid]=profile;if(current.sportId===sid)current.layout=cloneProfile(profile);state=current;writeLayoutProfile(profile);emit('save',{settings:state})}",
'''function resetLayout(family){clearTimeout(timer);const current=collect(),sid=layoutSportId||current.sportId;current.sportLayouts=current.sportLayouts||{};const profile=cloneProfile(current.sportLayouts[sid]||LAYOUT_DEFAULTS);profile[family]=cloneProfile(LAYOUT_DEFAULTS)[family];current.sportLayouts[sid]=profile;if(current.sportId===sid)current.layout=cloneProfile(profile);state=current;writeLayoutProfile(profile);emit('save',{settings:state})}
function resetLayoutSection(section){const keys={match:['teamWidth','scoreWidth','teamFont','scoreFont','logoSize','logoGap','cardPaddingX','teamAlign'],table:['tableTeamWidth','tableWideWidth','tableNarrowWidth','tableHeaderFont','tableFont','tableTeamFont','tableAlign'],lists:['listDateWidth','listTeamWidth','listScoreWidth']}[section]||[];const current=collect(),sid=layoutSportId||current.sportId,profile=cloneProfile(current.sportLayouts?.[sid]||LAYOUT_DEFAULTS),d=LAYOUT_DEFAULTS.large;for(const k of keys)profile.large[k]=d[k];current.sportLayouts=current.sportLayouts||{};current.sportLayouts[sid]=profile;if(current.sportId===sid)current.layout=cloneProfile(profile);state=current;writeLayoutProfile(profile);if(section==='table'){state.tableAutoBySport=state.tableAutoBySport||{};state.tableAutoBySport[sid]=true;updateTableModeUI()}commitNow()}''','section reset')
rep("save();const st=document.getElementById('widgetPresetStatus');", "commitNow();const st=document.getElementById('widgetPresetStatus');", 'recommended immediate save')

# Native callbacks: restore preview buttons, show AUTO measurements.
rep("if(m.action==='replace'){state=m.settings;location.reload()}};", 
"if(m.action==='previewDone'){document.querySelectorAll('.previewAction[data-preview=\"'+m.family+'\"]').forEach(b=>{b.disabled=false;if(b.dataset.label)b.textContent=b.dataset.label});const e=document.getElementById('previewMeta');if(e)e.textContent=''}if(m.action==='autoTableInfo'){const e=document.getElementById('autoTableInfo'),q=m.info;if(e&&q)e.textContent='AUTO · TÝM '+q.teamWidth+' pt · statistiky '+Object.values(q.columns||{}).join(' / ')+' pt'}if(m.action==='replace'){state=m.settings;location.reload()}};", 'native preview callbacks')

# Native preview is presented directly above the settings WebView instead of relaunching Scriptable by URL scheme.
old='''}else if(m.action==="preview"){
        cur=merge(m.settings||cur);saveSettings(cur);const fam=["small","medium","large"].includes(m.family)?m.family:"medium",base=URLScheme.forRunningScript(),sep=base.includes("?")?"&":"?";Safari.open(base+`${sep}sportsPreview=${encodeURIComponent(fam)}`);return cur'''
new='''}else if(m.action==="preview"){
        cur=merge(m.settings||cur);saveSettings(cur);const fam=["small","medium","large"].includes(m.family)?m.family:"medium";LAST_AUTO_TABLE_LAYOUT=null;try{const w=await widget(cur,fam);if(LAST_AUTO_TABLE_LAYOUT)await send(web,{action:"autoTableInfo",info:LAST_AUTO_TABLE_LAYOUT});if(fam==="small")await w.presentSmall();else if(fam==="large")await w.presentLarge();else await w.presentMedium()}finally{await send(web,{action:"previewDone",family:fam})}'''
rep(old,new,'direct preview')

# Maintenance reset starts from current unsaved form state; clear both data and all logo caches.
old='''}else if(m.action==="clearCache"){
        try{if(fm.fileExists(cachePath))fm.remove(cachePath)}catch(_){}await send(web,{action:"status",ok:true,text:tx(cur,"cacheCleared")})
      }else if(m.action==="reset"){
        const l=cur.language||lang();if(m.part==="appearance")cur=Object.assign({},cur,{theme:DEFAULTS.theme,accent:DEFAULTS.accent,background:DEFAULTS.background,panelColor:DEFAULTS.panelColor,textColor:DEFAULTS.textColor,mutedColor:DEFAULTS.mutedColor,liveColor:DEFAULTS.liveColor,winColor:DEFAULTS.winColor,compact:DEFAULTS.compact,refreshMinutes:DEFAULTS.refreshMinutes});else if(m.part==="sport")cur=Object.assign({},cur,{sportId:DEFAULTS.sportId,leagueId:DEFAULTS.leagueId,teamId:"",teamName:""});else{cur=clone(DEFAULTS);cur.language=l}saveSettings(cur);await send(web,{action:"status",ok:true,text:tx(cur,"resetDone")});await send(web,{action:"replace",settings:cur})'''
new='''}else if(m.action==="clearCache"){
        try{const dir=fm.cacheDirectory();for(const name of fm.listContents(dir))if(name===CACHE_FILE||(name.startsWith("SportsInfo_")&&name.endsWith(".png"))||name.startsWith("logo_")){try{fm.remove(fm.joinPath(dir,name))}catch(_){}}}catch(_){}await send(web,{action:"status",ok:true,text:tx(cur,"cacheCleared")})
      }else if(m.action==="reset"){
        const base=merge(m.settings||cur),l=base.language||lang();if(m.part==="appearance")cur=Object.assign({},base,{theme:DEFAULTS.theme,accent:DEFAULTS.accent,background:DEFAULTS.background,panelColor:DEFAULTS.panelColor,textColor:DEFAULTS.textColor,mutedColor:DEFAULTS.mutedColor,liveColor:DEFAULTS.liveColor,winColor:DEFAULTS.winColor,compact:DEFAULTS.compact,refreshMinutes:DEFAULTS.refreshMinutes});else if(m.part==="sport")cur=Object.assign({},base,{sportId:DEFAULTS.sportId,leagueId:DEFAULTS.leagueId,teamId:"",teamName:""});else{cur=clone(DEFAULTS);cur.language=l}saveSettings(cur);await send(web,{action:"status",ok:true,text:tx(cur,"resetDone")});await send(web,{action:"replace",settings:cur})'''
rep(old,new,'maintenance fixes')

# Manual first-four table width range also reaches 50 in data validation.
rep('tableWideWidth:[24,38]', 'tableWideWidth:[24,50]', 'wide range')

# Strong regression assertions before write.
assert 'const APP_VERSION = "2.5.22";' in s
assert 'function automaticTableSlotLayout' in s
assert 'tableAutoBySport' in s
assert 'id="layoutLargeTable"' in s and 'id="layoutLargeMatch"' in s and 'id="layoutLargeLists"' in s
assert "document.querySelectorAll('.previewBtn').forEach(b=>b.disabled=true)" not in s
assert 'Safari.open(base+' not in s
assert 'await w.presentLarge()' in s
assert 'touchstart' in s and "inputmode','numeric" in s
assert 'resetLayoutSection' in s
assert 'name.startsWith("SportsInfo_")&&name.endsWith(".png")' in s
p.write_text(s,encoding='utf-8')
print('Sports Info 2.5.22 iPhone AUTO/MANUAL layout patch applied')
