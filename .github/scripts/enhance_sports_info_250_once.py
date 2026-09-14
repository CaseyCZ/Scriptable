from pathlib import Path

root = Path('.')
app = root / 'apps/Sports-Info/Sports Info.js'
s = app.read_text(encoding='utf-8')
orig = s

def rep(old, new, count=None):
    global s
    n = s.count(old)
    if count is not None and n != count:
        raise SystemExit(f'Expected {count} occurrences, found {n}: {old[:100]}')
    if n == 0:
        raise SystemExit(f'Missing marker: {old[:120]}')
    s = s.replace(old, new)

rep('// Sports Info v2.4.0', '// Sports Info v2.5.0', 1)
rep('const APP_VERSION = "2.4.0";', 'const APP_VERSION = "2.5.0";', 1)

# Add verified OneFootball mappings for every football competition currently in Sports Info.
for old, new in {
    'fm:122,ccode:"CZE"':'fm:122,ofCompetition:159,ofSeason:39284,ccode:"CZE"',
    'fm:47,ccode:"ENG"':'fm:47,ofCompetition:9,ofSeason:39301,ccode:"ENG"',
    'fm:87,ccode:"ESP"':'fm:87,ofCompetition:10,ofSeason:39319,ccode:"ESP"',
    'fm:54,ccode:"GER"':'fm:54,ofCompetition:1,ofSeason:39285,ccode:"GER"',
    'fm:55,ccode:"ITA"':'fm:55,ofCompetition:13,ofSeason:39325,ccode:"ITA"',
    'fm:53,ccode:"FRA"':'fm:53,ofCompetition:23,ofSeason:39245,ccode:"FRA"',
    'fm:42,ccode:"INT"':'fm:42,ofCompetition:5,ofSeason:39356,ccode:"INT"',
    'fm:73,ccode:"INT"':'fm:73,ofCompetition:7,ofSeason:39357,ccode:"INT"',
}.items():
    rep(old, new, 1)

# Source descriptions.
rep('sourceInfo:"ESPN + FotMob pro fotbal, ESPN pro hokej/basketbal/baseball a Livesport pro florbal. SportsAPI Pro je jen volitelná záloha. Vše fail-open s cache."',
    'sourceInfo:"OneFootball + ESPN + FotMob pro fotbal, ESPN pro NHL/NCAA a Livesport pro evropské soutěže. SportsAPI Pro je jen volitelná záloha. Vše fail-open s cache."', 1)
rep('sourceInfo:"ESPN + FotMob for football, ESPN for hockey/basketball/baseball and Livesport for floorball. SportsAPI Pro is an optional fallback. Fail-open with cache."',
    'sourceInfo:"OneFootball + ESPN + FotMob for football, ESPN for NHL/NCAA and Livesport for European competitions. SportsAPI Pro is an optional fallback. Fail-open with cache."', 1)
rep('sourceInfo:"ESPN + FotMob für Fußball, ESPN für Hockey/Basketball/Baseball und Livesport für Floorball. SportsAPI Pro ist optionaler Fallback."',
    'sourceInfo:"OneFootball + ESPN + FotMob für Fußball, ESPN für NHL/NCAA und Livesport für europäische Wettbewerbe. SportsAPI Pro ist optionaler Fallback."', 1)
rep('sourceInfo:"ESPN + FotMob para fútbol, ESPN para hockey/baloncesto/béisbol y Livesport para floorball. SportsAPI Pro es un respaldo opcional."',
    'sourceInfo:"OneFootball + ESPN + FotMob para fútbol, ESPN para NHL/NCAA y Livesport para competiciones europeas. SportsAPI Pro es un respaldo opcional."', 1)

# Better widget help for the adaptive table.
rep('tableDetail:"Pouze Large. Bez oblíbeného týmu ukáže čelo tabulky; s týmem jeho okolí."',
    'tableDetail:"Pouze Large. Automaticky ukáže tolik řádků, kolik se vejde; když nejsou zápasy, až 16 týmů. Oblíbený tým zvýrazní."', 1)
rep('tableDetail:"Large only. With no favorite team show the top; with a team show rows around its position."',
    'tableDetail:"Large only. Automatically shows as many rows as fit; when there are no matches, up to 16 teams. The favorite team is highlighted."', 1)
rep('tableDetail:"Nur Large. Ohne Lieblingsteam Tabellenspitze, mit Team dessen Umgebung."',
    'tableDetail:"Nur Large. Zeigt automatisch so viele Zeilen wie passen; ohne Spiele bis zu 16 Teams. Das Lieblingsteam wird markiert."', 1)
rep('tableDetail:"Solo Large. Sin equipo favorito muestra la parte alta; con equipo muestra su zona."',
    'tableDetail:"Solo Large. Muestra automáticamente las filas que caben; sin partidos, hasta 16 equipos. El favorito queda resaltado."', 1)

rep('apiFotmobBase:"https://www.fotmob.com/api/data",apiSofaBase:',
    'apiFotmobBase:"https://www.fotmob.com/api/data",apiOneFootballFeedBase:"https://feedmonster.onefootball.com",apiOneFootballScoresBase:"https://api.onefootball.com",apiSofaBase:', 1)

rep('function sourceLabel(s){const m=league(s);return m.provider==="soccer"?"ESPN + FotMob":',
    'function sourceLabel(s){const m=league(s);return m.provider==="soccer"?"OneFootball + ESPN + FotMob":', 1)

# Insert OneFootball adapter after FotMob. These endpoints were verified against all eight mapped leagues.
marker = '\n\nconst LIVESPORT_MEM={};'
if marker not in s:
    raise SystemExit('Livesport insertion marker missing')
onefootball = r'''

const ONEFOOTBALL_MEM={};
function oneFootballRows(d){const ranking=(d?.groups?.[0]?.ranking)||[];return ranking.map((x,i)=>{const t=x?.team||{},q=t.teamstats||{};return{rank:Number(x.rank||x.ranking||i+1)||i+1,id:String(t.idInternal||t.id||""),name:t.name||"",short:t.shortName||t.name||"",played:String(q.played??""),points:String(q.points??""),won:String(q.won??""),drawn:String(q.drawn??""),lost:String(q.lost??""),gf:String(q.goalsShot??""),ga:String(q.goalsGot??""),diff:String(q.diff??""),logo:(t.idInternal||t.id)?`https://images.onefootball.com/icons/teams/56/${t.idInternal||t.id}.png`:""}}).filter(x=>x.id&&x.name)}
function normOneFootballMatch(m,kickoff){try{const h=m.team_home||{},a=m.team_away||{},period=String(m.period||"PreMatch"),completed=period==="FullTime",state=completed?"post":period==="PreMatch"?"pre":"in",sv=x=>Number(x)<0||x==null?"":String(x);return{id:String(m.id||`${kickoff}|${h.id}|${a.id}`),date:kickoff||"",state,completed,status:m.minute_display||m.minute?`${period}${m.minute?` · ${m.minute}'`:""}`:period,home:{id:String(h.id||""),name:h.name||"",short:h.name||"",abbr:"",logo:h.id?`https://images.onefootball.com/icons/teams/56/${h.id}.png`:"",score:sv(m.score_home)},away:{id:String(a.id||""),name:a.name||"",short:a.name||"",abbr:"",logo:a.id?`https://images.onefootball.com/icons/teams/56/${a.id}.png`:"",score:sv(m.score_away)}}}catch(_){return null}}
async function oneFootballMeta(s){const m=league(s);if(!m.ofCompetition||!m.ofSeason)throw new Error("No OneFootball mapping");const feed=s.apiOneFootballFeedBase||DEFAULTS.apiOneFootballFeedBase,key=`meta:${m.id}`;if(ONEFOOTBALL_MEM[key])return ONEFOOTBALL_MEM[key];const base=`${feed}/feeds/il/en/competitions/${m.ofCompetition}/${m.ofSeason}`,parts=await Promise.all([requestJSON(`${base}/standings.json`,BROWSER_HEADERS),requestJSON(`${base}/matchdaysOverview.json`,BROWSER_HEADERS)]),out={table:oneFootballRows(parts[0]),matchdays:parts[1]?.matchdays||[]};ONEFOOTBALL_MEM[key]=out;return out}
async function oneFootballBundle(s){const m=league(s),key=`bundle:${m.id}`;if(ONEFOOTBALL_MEM[key])return ONEFOOTBALL_MEM[key];const meta=await oneFootballMeta(s),scores=s.apiOneFootballScoresBase||DEFAULTS.apiOneFootballScoresBase,days=meta.matchdays||[];let idx=days.findIndex(x=>x?.isCurrentMatchday);if(idx<0)idx=0;const from=Math.max(0,idx-4),to=Math.min(days.length,idx+7),pick=days.slice(from,to),parts=await Promise.allSettled(pick.map(x=>requestJSON(`${scores}/scores-mixer/v1/en/cn/matchdays/${encodeURIComponent(x.id)}`,BROWSER_HEADERS))),events=[];for(const p of parts)if(p.status==="fulfilled")for(const k of p.value?.kickoffs||[])for(const g of k.groups||[])for(const mm of g.matches||[]){const e=normOneFootballMatch(mm,k.kickoff);if(e)events.push(e)}const teams=meta.table.map(x=>({id:x.id,name:x.name,short:x.short,logo:x.logo}));const out={events:unique(events),table:meta.table,teams,matchdaysLoaded:pick.length};ONEFOOTBALL_MEM[key]=out;return out}
async function oneFootballHealth(s){const d=await oneFootballMeta(s);if(!d.table.length||!d.matchdays.length)throw new Error("OneFootball returned incomplete data");return `${d.table.length} teams · ${d.matchdays.length} matchdays`}
'''
s = s.replace(marker, onefootball + marker, 1)

# Prefer OneFootball for complete football data, retain ESPN/FotMob as fallbacks.
old = 'async function scoreboardFor(s,dates){const m=league(s);if(m.provider==="soccer"){try{const a=await espnScoreboard(s,dates);if(a.length)return a}catch(_){}const d=await fotmobLeague(s);return fotmobMatches(d).filter(x=>inDateRange(x,dates))}'
new = 'async function scoreboardFor(s,dates){const m=league(s);if(m.provider==="soccer"){try{const d=await oneFootballBundle(s),a=d.events.filter(x=>inDateRange(x,dates));if(a.length)return a}catch(_){}try{const a=await espnScoreboard(s,dates);if(a.length)return a}catch(_){}const d=await fotmobLeague(s);return fotmobMatches(d).filter(x=>inDateRange(x,dates))}'
rep(old,new,1)
old = 'async function teamsFor(s){const m=league(s);if(m.provider==="soccer"){try{const a=await espnTeams(s);if(a.length)return a}catch(_){}const rows=fotmobRows(await fotmobLeague(s));return rows.map(x=>({id:x.id,name:x.name,short:x.short,logo:`https://images.fotmob.com/image_resources/logo/teamlogo/${x.id}.png` })).sort((a,b)=>a.name.localeCompare(b.name))}'
new = 'async function teamsFor(s){const m=league(s);if(m.provider==="soccer"){try{const a=(await oneFootballBundle(s)).teams;if(a.length)return a}catch(_){}try{const a=await espnTeams(s);if(a.length)return a}catch(_){}const rows=fotmobRows(await fotmobLeague(s));return rows.map(x=>({id:x.id,name:x.name,short:x.short,logo:`https://images.fotmob.com/image_resources/logo/teamlogo/${x.id}.png` })).sort((a,b)=>a.name.localeCompare(b.name))}'
rep(old,new,1)
old = 'async function standingsFor(s){const m=league(s);if(m.provider==="soccer"){try{const a=await espnStandings(s);if(a.length)return a}catch(_){}return fotmobRows(await fotmobLeague(s))}'
new = 'async function standingsFor(s){const m=league(s);if(m.provider==="soccer"){try{const a=(await oneFootballBundle(s)).table;if(a.length)return a}catch(_){}try{const a=await espnStandings(s);if(a.length)return a}catch(_){}return fotmobRows(await fotmobLeague(s))}'
rep(old,new,1)

# Favorite-team matching survives the provider-ID migration by also matching the saved team name.
old = 'function result(e,id){if(!id||!e.completed)return"";const h=Number(e.home.score),a=Number(e.away.score);if(Number.isNaN(h)||Number.isNaN(a))return"";const me=e.home.id===id?h:a,op=e.home.id===id?a:h;return me>op?"W":me<op?"L":"D"}'
new = 'function normTeamName(v){return String(v||"").normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase().replace(/[^a-z0-9]+/g," ").trim()}\nfunction teamMatches(t,s){if(!t)return false;if(s.teamId&&String(t.id||"")===String(s.teamId))return true;const a=normTeamName(t.name||t.short),b=normTeamName(s.teamName);return !!b&&(a===b||a.includes(b)||b.includes(a))}\nfunction eventMatches(e,s){return teamMatches(e?.home,s)||teamMatches(e?.away,s)}\nfunction result(e,s){if(!(s.teamId||s.teamName)||!e.completed)return"";const h=Number(e.home.score),a=Number(e.away.score);if(Number.isNaN(h)||Number.isNaN(a))return"";const home=teamMatches(e.home,s),me=home?h:a,op=home?a:h;return me>op?"W":me<op?"L":"D"}'
rep(old,new,1)
rep('scoreboardFor(s,range(-21,0)),scoreboardFor(s,range(0,21))', 'scoreboardFor(s,range(-60,0)),scoreboardFor(s,range(0,120))', 1)
rep('const ev=all.filter(e=>!s.teamId||e.home.id===s.teamId||e.away.id===s.teamId)', 'const ev=all.filter(e=>!(s.teamId||s.teamName)||eventMatches(e,s))', 1)
rep('form:s.teamId?done.slice(0,5).map(e=>result(e,s.teamId)).filter(Boolean):[]', 'form:(s.teamId||s.teamName)?done.slice(0,5).map(e=>result(e,s)).filter(Boolean):[]', 1)
rep('function form(parent,s,d,p){if(!s.teamId||!d.form.length)return;', 'function form(parent,s,d,p){if(!(s.teamId||s.teamName)||!d.form.length)return;', 1)

# Richer adaptive standings with full football stats and many more visible rows when space allows.
old_table = 'function table(parent,s,d,p){let rows=d.table||[];if(!rows.length)return;if(s.teamId){const i=rows.findIndex(x=>x.id===s.teamId),start=i<0?0:Math.max(0,Math.min(i-2,rows.length-6));rows=rows.slice(start,start+6)}else rows=rows.slice(0,6);title(parent,tx(s,"standings"),p);parent.addSpacer(4);for(const x of rows){const r=parent.addStack();r.layoutHorizontally();const fav=s.teamId&&x.id===s.teamId;txt(r,x.rank,9,fav?p.accent:p.muted,fav);r.addSpacer(6);txt(r,x.name||x.short,10,fav?p.accent:p.text,fav);r.addSpacer();txt(r,`${tx(s,"played")} ${x.played||"–"}  ${tx(s,"points")} ${x.points||"–"}`,9,p.muted,true)}}'
new_table = r'''function table(parent,s,d,p){let all=d.table||[];if(!all.length)return;const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1,maxRows=Math.min(all.length,d.current?8:16);let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);title(parent,tx(s,"standings"),p);parent.addSpacer(3);const detailed=rows.some(x=>x.won!==undefined&&x.won!=="");if(detailed){const h=parent.addStack();h.layoutHorizontally();lineCell(h,"#",17,p.muted,"left",true,8);lineCell(h,(s.language==="cs"?"TÝM":s.language==="de"?"TEAM":s.language==="es"?"EQUIPO":"TEAM"),119,p.muted,"left",true,8);lineCell(h,tx(s,"played"),22,p.muted,"center",true,8);lineCell(h,(s.language==="cs"?"V/R/P":"W/D/L"),51,p.muted,"center",true,8);lineCell(h,(s.language==="de"?"TORE":s.language==="es"?"GOL":"GÓLY"),43,p.muted,"center",true,8);lineCell(h,tx(s,"points"),26,p.muted,"right",true,8);parent.addSpacer(2)}for(const x of rows){const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();if(detailed){lineCell(r,String(x.rank),17,fav?p.accent:p.muted,"left",fav,8);const nm=lineCell(r,x.name||x.short,119,fav?p.accent:p.text,"left",fav,9);nm.minimumScaleFactor=.5;lineCell(r,x.played||"–",22,p.muted,"center",true,8);lineCell(r,`${x.won||"0"}/${x.drawn||"0"}/${x.lost||"0"}`,51,p.muted,"center",false,8);lineCell(r,`${x.gf||"–"}:${x.ga||"–"}`,43,p.muted,"center",false,8);lineCell(r,x.points||"–",26,fav?p.accent:p.muted,"right",true,9)}else{txt(r,x.rank,9,fav?p.accent:p.muted,fav);r.addSpacer(6);const nm=txt(r,x.name||x.short,10,fav?p.accent:p.text,fav);nm.minimumScaleFactor=.55;r.addSpacer();txt(r,`${tx(s,"played")} ${x.played||"–"}  ${tx(s,"points")} ${x.points||"–"}`,9,p.muted,true)}}}'''
rep(old_table,new_table,1)

# Preserve room for the expanded table on Large.
rep('d.next.filter(x=>x.id!==d.current.id).slice(0,family==="large"?s.maxMatches:2)', 'd.next.filter(x=>x.id!==d.current.id).slice(0,family==="large"&&s.showTable?Math.min(s.maxMatches,2):family==="large"?s.maxMatches:2)', 1)
rep('d.done.filter(x=>x.id!==d.current.id).slice(0,s.maxMatches)', 'd.done.filter(x=>x.id!==d.current.id).slice(0,s.showTable?Math.min(s.maxMatches,3):s.maxMatches)', 1)

# Diagnostics include OneFootball explicitly.
old_health = 'if(m.provider==="soccer"){const [e,f]=await Promise.allSettled([limited(()=>espnScoreboard(s,today),7500,"ESPN"),limited(()=>fotmobLeague(s),7500,"FotMob")]);const es=e.status==="fulfilled"?"ESPN OK":"ESPN ERROR",fs=f.status==="fulfilled"?"FotMob OK":"FotMob ERROR";if(e.status!=="fulfilled"&&f.status!=="fulfilled")throw new Error(`${es} · ${fs}`);return `${es} · ${fs}`}'
new_health = 'if(m.provider==="soccer"){const [o,e,f]=await Promise.allSettled([limited(()=>oneFootballHealth(s),7500,"OneFootball"),limited(()=>espnScoreboard(s,today),7500,"ESPN"),limited(()=>fotmobLeague(s),7500,"FotMob")]);const os=o.status==="fulfilled"?`OneFootball OK · ${o.value}`:"OneFootball ERROR",es=e.status==="fulfilled"?"ESPN OK":"ESPN ERROR",fs=f.status==="fulfilled"?"FotMob OK":"FotMob ERROR";if(o.status!=="fulfilled"&&e.status!=="fulfilled"&&f.status!=="fulfilled")throw new Error(`${os} · ${es} · ${fs}`);return `${os} · ${es} · ${fs}`}'
rep(old_health,new_health,1)

# Advanced endpoints and setting collection.
rep('${field("apiEspnBase","ESPN",s.apiEspnBase)}${field("apiFotmobBase","FotMob",s.apiFotmobBase)}${field("apiSofaBase","SofaScore",s.apiSofaBase)}',
    '${field("apiEspnBase","ESPN",s.apiEspnBase)}${field("apiFotmobBase","FotMob",s.apiFotmobBase)}${field("apiOneFootballFeedBase","OneFootball Feed",s.apiOneFootballFeedBase)}${field("apiOneFootballScoresBase","OneFootball Scores",s.apiOneFootballScoresBase)}${field("apiSofaBase","SofaScore",s.apiSofaBase)}', 1)
rep("'apiEspnBase','apiFotmobBase','apiSofaBase'", "'apiEspnBase','apiFotmobBase','apiOneFootballFeedBase','apiOneFootballScoresBase','apiSofaBase'", 1)

# When team IDs change between providers, select the same saved club by name and migrate its ID automatically.
old_native = "(m.teams||[]).forEach(t=>{const o=document.createElement('option');o.value=t.id;o.textContent=t.name;if(t.id===old)o.selected=true;sel.appendChild(o)});const e=document.getElementById('sourceStatus');"
new_native = "let matched=null;(m.teams||[]).forEach(t=>{const o=document.createElement('option');o.value=t.id;o.textContent=t.name;if(t.id===old||((state.teamName||'').trim().toLowerCase()===String(t.name||'').trim().toLowerCase())){o.selected=true;matched=t}sel.appendChild(o)});if(matched&&matched.id!==state.teamId){state.teamId=matched.id;state.teamName=matched.name;save()}const e=document.getElementById('sourceStatus');"
rep(old_native,new_native,1)

if s == orig:
    raise SystemExit('No changes made')
app.write_text(s, encoding='utf-8')

# Docs/catalog version and source labels.
for path in [root/'apps/Sports-Info/README.md', root/'README.md', root/'index.html']:
    txt = path.read_text(encoding='utf-8')
    txt = txt.replace('2.4.0','2.5.0')
    txt = txt.replace('ESPN + FotMob', 'OneFootball + ESPN + FotMob')
    path.write_text(txt, encoding='utf-8')

print('Sports Info 2.5.0 patch applied')
