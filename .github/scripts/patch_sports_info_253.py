from pathlib import Path
import re

path = Path('apps/Sports-Info/Sports Info.js')
s = path.read_text(encoding='utf-8')

assert '// Sports Info v2.5.2' in s
assert 'const APP_VERSION = "2.5.2";' in s
s = s.replace('// Sports Info v2.5.2', '// Sports Info v2.5.3', 1)
s = s.replace('const APP_VERSION = "2.5.2";', 'const APP_VERSION = "2.5.3";', 1)

pat = r'async function espnStandings\(s\)\{.*?\}\n\nconst FOTMOB_MEM='
repl = '''async function espnStandings(s){
  const m=league(s),base=s.apiEspnBase||DEFAULTS.apiEspnBase;
  const d=await requestJSON(`${base}/apis/v2/sports/${encodeURIComponent(m.espnSport)}/${encodeURIComponent(m.espnLeague)}/standings?region=us&lang=en&contentorigin=espn&isqualified=true&type=0&level=0`);
  return standingsEntries(d).map((e,i)=>{
    const t=e.team||{},q=e.stats||[];
    const played=stat(q,["gamesPlayed","gamesplayed","gp"],"");
    const wins=stat(q,["wins","w"],"");
    const losses=stat(q,["losses","l"],"");
    const draws=stat(q,["ties","draws","d"],"");
    const otWins=stat(q,["overtimeWins","otWins","row"],"");
    const otLosses=stat(q,["overtimeLosses","otl"],"");
    const gf=stat(q,["pointsFor","goalsFor","runsFor","pf","gf","rf"],"");
    const ga=stat(q,["pointsAgainst","goalsAgainst","runsAgainst","pa","ga","ra"],"");
    const pct=stat(q,["winPercent","winPercentage","pct"],"");
    const gb=stat(q,["gamesBehind","gb"],"");
    const diff=stat(q,["pointDifferential","goalDifferential","runDifferential","diff"],"");
    return {rank:Number(stat(q,["rank","position","playoffSeed"],i+1))||i+1,id:String(t.id||""),name:t.displayName||t.name||"",short:t.abbreviation||t.shortDisplayName||t.displayName||"",played:String(played??""),wins:String(wins??""),won:String(wins??""),draws:String(draws??""),drawn:String(draws??""),losses:String(losses??""),lost:String(losses??""),otWins:String(otWins??""),otLosses:String(otLosses??""),points:String(stat(q,["points","pts"],"")),pct:String(pct??""),gb:String(gb??""),gf:String(gf??""),ga:String(ga??""),diff:String(diff??"")}
  }).filter(x=>x.name)
}

const FOTMOB_MEM='''
s,n = re.subn(pat,repl,s,count=1,flags=re.S)
assert n == 1, 'espnStandings patch failed'

pat = r'function fotmobRows\(d\)\{.*?\}\nfunction normFotmob'
repl = '''function fotmobRows(d){const out=[],seen=new Set(),groups=Array.isArray(d?.table)?d.table:(d?.table?[d.table]:[]);const addRows=a=>{for(const x of Array.isArray(a)?a:[]){const id=String(x?.id||"");if(!id||seen.has(id))continue;seen.add(id);const wins=x.wins??x.won??"",draws=x.draws??x.drawn??"",losses=x.losses??x.lost??"",gf=x.gf??x.goalsFor??"",ga=x.ga??x.goalsAgainst??"";out.push({rank:Number(x.idx||x.rank||out.length+1),id,name:x.name||x.teamName||"",short:x.shortName||x.name||x.teamName||"",played:String(x.played??""),wins:String(wins),won:String(wins),draws:String(draws),drawn:String(draws),losses:String(losses),lost:String(losses),otWins:String(x.otWins??""),otLosses:String(x.otLosses??x.otl??""),points:String(x.pts??x.points??""),pct:String(x.pct??x.winPercentage??""),gb:String(x.gb??x.gamesBehind??""),gf:String(gf),ga:String(ga),diff:String(x.goalDifference??x.diff??""),form:Array.isArray(x.form)?x.form:[]})}};for(const g of groups){const d0=g?.data||g||{};if(d0.composite&&Array.isArray(d0.tables)){for(const sub of d0.tables)addRows(sub?.table?.all||sub?.table||[])}else addRows(d0?.table?.all||d0?.table||[])}return out.filter(x=>x.name)}
function normFotmob'''
s,n = re.subn(pat,repl,s,count=1,flags=re.S)
assert n == 1, 'fotmobRows patch failed'

old = '''function lsFields(rec){const o={};for(const part of String(rec||"").split("¬")){const i=part.indexOf("÷");if(i>0)o[part.slice(0,i)]=part.slice(i+1)}return o}\nfunction lsEvents(feed){const out=[];for(const tail of String(feed||"").split("¬~AA÷").slice(1)){const f=lsFields("AA÷"+tail);if(!f.AA||!f.AD||!f.AE||!f.AF)continue;const code=Number(f.AB||1),completed=code===3,state=code===2?"in":completed?"post":"pre",logo=x=>x?`https://static.flashscore.com/res/image/data/${x}`:"";out.push({id:String(f.AA),date:new Date(Number(f.AD)*1000).toISOString(),state,completed,status:f.ER||"",home:{id:String(f.PX||f.WM||f.AE),name:f.AE||"",short:f.WM||f.AE||"",abbr:f.WM||"",logo:logo(f.OA),score:f.AG==null?"":String(f.AG)},away:{id:String(f.PY||f.WN||f.AF),name:f.AF||"",short:f.WN||f.AF||"",abbr:f.WN||"",logo:logo(f.OB),score:f.AH==null?"":String(f.AH)}})}return out}\nasync function livesportBundle(s){const m=league(s),key=`ls:${m.id}`;if(LIVESPORT_MEM[key])return LIVESPORT_MEM[key];if(!m.lsPath)throw new Error("No Livesport mapping");const html=await requestText(`https://www.livesport.com${m.lsPath}`,LIVESPORT_HEADERS),events=unique([...lsEvents(lsFeed(html,"summary-results")),...lsEvents(lsFeed(html,"summary-fixtures"))]);if(!events.length)throw new Error("Livesport returned no events");const map=new Map();for(const e of events)for(const t of[e.home,e.away])if(t.id)map.set(t.id,{id:t.id,name:t.name,short:t.short,logo:t.logo});const out={events,teams:[...map.values()].sort((a,b)=>a.name.localeCompare(b.name)),table:[]};LIVESPORT_MEM[key]=out;return out}'''
new = '''function lsFields(rec){const o={};for(const part of String(rec||"").split("¬")){const i=part.indexOf("÷");if(i>0)o[part.slice(0,i)]=part.slice(i+1)}return o}\nfunction lsAllFeeds(html){const out=[],re=/cjs\\.initialFeeds\\["([^"]+)"\\]\\s*=\\s*\\{\\s*data:\\s*`([\\s\\S]*?)`/g;let m;while((m=re.exec(String(html||""))))out.push({name:m[1],data:m[2]});return out}\nfunction lsEvents(feed){const out=[];for(const tail of String(feed||"").split("¬~AA÷").slice(1)){const f=lsFields("AA÷"+tail);if(!f.AA||!f.AD||!f.AE||!f.AF)continue;const code=Number(f.AB||1),completed=code===3,state=code===2?"in":completed?"post":"pre",logo=x=>x?`https://static.flashscore.com/res/image/data/${x}`:"";out.push({id:String(f.AA),date:new Date(Number(f.AD)*1000).toISOString(),state,completed,status:f.ER||"",home:{id:String(f.PX||f.WM||f.AE),name:f.AE||"",short:f.WM||f.AE||"",abbr:f.WM||"",logo:logo(f.OA),score:f.AG==null?"":String(f.AG)},away:{id:String(f.PY||f.WN||f.AF),name:f.AF||"",short:f.WN||f.AF||"",abbr:f.WN||"",logo:logo(f.OB),score:f.AH==null?"":String(f.AH)}})}return out}\nfunction lsRows(feed){const rows=[],seen=new Set();for(const raw of String(feed||"").split("~")){const f=lsFields(raw);if(!f.TI||!f.TN||seen.has(f.TI))continue;seen.add(f.TI);let gf="",ga="";if(f.TG&&f.TG.includes(":")){const q=f.TG.split(":");gf=q[0];ga=q[1]}rows.push({rank:Number(f.TR||rows.length+1),id:String(f.TI),name:f.TN,short:f.TN,played:String(f.TM??""),wins:String(f.TW??""),won:String(f.TW??""),draws:String(f.TDR??""),drawn:String(f.TDR??""),losses:String(f.TL??""),lost:String(f.TL??""),otWins:String(f.TWO??""),otLosses:String(f.TLO??""),points:String(f.TP??""),pct:String(f.TAP??""),gb:String(f.TGB??f.TB??""),gf:String(gf),ga:String(ga),diff:String(f.TPF??"")})}return rows}\nasync function livesportBundle(s){const m=league(s),key=`ls:${m.id}`;if(LIVESPORT_MEM[key])return LIVESPORT_MEM[key];if(!m.lsPath)throw new Error("No Livesport mapping");const base=`https://www.livesport.com${m.lsPath}`,pages=await Promise.allSettled([requestText(base,LIVESPORT_HEADERS),requestText(base+"standings/",LIVESPORT_HEADERS)]),html=pages[0].status==="fulfilled"?pages[0].value:"",standHtml=pages[1].status==="fulfilled"?pages[1].value:"",events=unique([...lsEvents(lsFeed(html,"summary-results")),...lsEvents(lsFeed(html,"summary-fixtures"))]);let table=[];for(const f of lsAllFeeds(standHtml)){const r=lsRows(f.data);if(r.length>table.length)table=r}if(!events.length&&!table.length)throw new Error("Livesport returned no data");const map=new Map();for(const x of table)if(x.id)map.set(x.id,{id:x.id,name:x.name,short:x.short,logo:""});for(const e of events)for(const t of[e.home,e.away])if(t.id)map.set(t.id,{id:t.id,name:t.name,short:t.short,logo:t.logo});const out={events,teams:[...map.values()].sort((a,b)=>a.name.localeCompare(b.name)),table};LIVESPORT_MEM[key]=out;return out}'''
assert old in s, 'Livesport source block not found'
s = s.replace(old,new,1)

pat = r'function lineCell\(parent,value,width,p,align="left",bold=false,size=10,minScale=\.62\)\{.*?\nfunction autoRefreshMinutes'
repl = '''function lineCell(parent,value,width,p,align="left",bold=false,size=10,minScale=.62){const c=parent.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);if(align==="right"||align==="center")c.addSpacer();const t=txt(c,value,size,p,bold);t.minimumScaleFactor=minScale;if(align==="center"){t.centerAlignText();c.addSpacer()}else if(align==="left")c.addSpacer();return t}
async function line(parent,e,s,p,family="large"){const r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();const dateW=40,teamW=106,scoreW=54;lineCell(r,day(s,e.date),dateW,p.muted,"left",true,9,.8);lineCell(r,teamLabel(e.home,family),teamW,p.text,"right",true,10,1);lineCell(r,score(e)==="–"?time(s,e.date):score(e),scoreW,e.state==="in"?p.live:p.text,"center",true,10,1);lineCell(r,teamLabel(e.away,family),teamW,p.text,"left",true,10,1)}
function title(parent,v,p){const r=parent.addStack();r.layoutHorizontally();txt(r,String(v).toUpperCase(),9,p.muted,true);r.addSpacer()}
function form(parent,s,d,p){if(!(s.teamId||s.teamName)||!d.form.length)return;const r=parent.addStack();r.layoutHorizontally();txt(r,tx(s,"formTitle")+":",9,p.muted,true);r.addSpacer(6);for(const x of d.form){txt(r,x,10,x==="W"?p.ok:x==="L"?p.live:p.muted,true);r.addSpacer(4)}r.addSpacer()}
const TABLE_PROFILES={
  football:[["rank","#",15],["team","TÝM",100],["played","Z",19],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",39],["diff","RS",23],["points","B",22]],
  hockey:[["rank","#",15],["team","TÝM",92],["played","Z",18],["wins","V",18],["otWins","VP",21],["otLosses","PP",21],["losses","P",18],["score","SK",37],["points","B",22]],
  basketball:[["rank","#",15],["team","TÝM",108],["played","Z",22],["wins","V",22],["losses","P",22],["pct","%",38],["score","SK",47]],
  floorball:[["rank","#",15],["team","TÝM",104],["played","Z",19],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",40],["points","B",23]],
  baseball:[["rank","#",15],["team","TÝM",112],["played","Z",22],["wins","W",22],["losses","L",22],["pct","PCT",39],["gb","GB",31]]
};
function standingTeamLabel(x){const full=x.name||x.short||"";if(full.length<=20)return full;return x.short&&x.short!==full?x.short:full}
function standingValue(x,key){
  const val=k=>x?.[k]!==undefined&&x?.[k]!==null&&x?.[k]!==""?String(x[k]):"";
  if(key==="rank")return val("rank")||"–";
  if(key==="team")return standingTeamLabel(x);
  if(key==="wins")return val("wins")||val("won")||"–";
  if(key==="draws")return val("draws")||val("drawn")||"–";
  if(key==="losses")return val("losses")||val("lost")||"–";
  if(key==="score"){const direct=val("score");if(direct)return direct;const a=val("gf"),b=val("ga");return a||b?`${a||"–"}:${b||"–"}`:"–"}
  if(key==="diff"){const direct=val("diff");if(direct)return direct;const a=Number(val("gf")),b=Number(val("ga"));return Number.isFinite(a)&&Number.isFinite(b)?String(a-b):"–"}
  if(key==="pct"){let v=val("pct");if(v){let n=Number(v);if(Number.isFinite(n)){if(n>1)n=n/100;return n.toFixed(3)}return v}const w=Number(val("wins")||val("won")),g=Number(val("played"));return Number.isFinite(w)&&Number.isFinite(g)&&g>0?(w/g).toFixed(3):"–"}
  return val(key)||"–"
}
function table(parent,s,d,p){
  let all=d.table||[];if(!all.length)return;
  const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1;
  const shownUpcoming=s.showNext&&d.current?Math.min(d.next.filter(x=>x.id!==d.current.id).length,2):0;
  const shownLast=s.showLast&&d.current?Math.min(d.done.filter(x=>x.id!==d.current.id).length,s.showTable?3:s.maxMatches):0;
  let capacity=d.current?15:16;if(shownUpcoming>1)capacity-=shownUpcoming-1;if(shownLast)capacity-=shownLast+1;if(s.showForm&&(s.teamId||s.teamName)&&d.form.length)capacity-=1;
  const maxRows=Math.min(all.length,clamp(capacity,6,16));
  let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);
  const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football;
  title(parent,tx(s,"standings"),p);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();for(const [key,label,width] of cols)lineCell(h,label,width,p.muted,key==="team"?"left":"center",true,7,.9);parent.addSpacer(2);
  for(const x of rows){const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();for(const [key,,width] of cols){const color=fav?p.accent:(key==="team"?p.text:p.muted),size=key==="team"?9:8,min=key==="team"?1:.8;lineCell(r,standingValue(x,key),width,color,key==="team"?"left":"center",fav||key==="points",size,min)}}
}
function autoRefreshMinutes'''
s,n = re.subn(pat,repl,s,count=1,flags=re.S)
assert n == 1, 'renderer patch failed'

path.write_text(s, encoding='utf-8')
Path('.github/scripts/patch_sports_info_253.py').unlink()
Path('.github/workflows/patch-sports-info-tables-once.yml').unlink()
