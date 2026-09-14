from pathlib import Path
import re
import subprocess

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.7";' in s
assert 'range(-60,0)' in s and 'range(0,120)' in s
assert 'idx-4' in s and 'idx+7' in s

s = s.replace('// Sports Info v2.5.7', '// Sports Info v2.5.8', 1)
s = s.replace('const APP_VERSION = "2.5.7";', 'const APP_VERSION = "2.5.8";', 1)

old_of = re.search(r'async function oneFootballBundle\(s\)\{.*?\}\nasync function oneFootballHealth', s, re.S)
assert old_of, 'oneFootballBundle not found'
new_of = '''async function oneFootballBundle(s,needs={recent:1,upcoming:1}){
  const m=league(s),recent=clamp(Number(needs.recent)||1,1,8),upcoming=clamp(Number(needs.upcoming)||1,1,8),scoped=!!(s.teamId||s.teamName),key=`bundle:${m.id}:${recent}:${upcoming}:${scoped?"team":"league"}`;
  if(ONEFOOTBALL_MEM[key])return ONEFOOTBALL_MEM[key];
  const meta=await oneFootballMeta(s),scores=s.apiOneFootballScoresBase||DEFAULTS.apiOneFootballScoresBase,days=meta.matchdays||[];
  let idx=days.findIndex(x=>x?.isCurrentMatchday);if(idx<0)idx=0;
  const back=scoped?recent:1,forward=scoped?upcoming+1:2,from=Math.max(0,idx-back),to=Math.min(days.length,idx+forward+1),pick=days.slice(from,to);
  const parts=await Promise.allSettled(pick.map(x=>requestJSON(`${scores}/scores-mixer/v1/en/cn/matchdays/${encodeURIComponent(x.id)}`,BROWSER_HEADERS))),events=[];
  for(const p of parts)if(p.status==="fulfilled")for(const k of p.value?.kickoffs||[])for(const g of k.groups||[])for(const mm of g.matches||[]){const e=normOneFootballMatch(mm,k.kickoff);if(e)events.push(e)}
  const teams=meta.table.map(x=>({id:x.id,name:x.name,short:x.short,logo:x.logo})),out={events:unique(events),table:meta.table,teams,matchdaysLoaded:pick.length};ONEFOOTBALL_MEM[key]=out;return out
}
async function oneFootballHealth'''
s = s[:old_of.start()] + new_of + s[old_of.end():]

s = s.replace('async function scoreboardFor(s,dates){const m=league(s);if(m.provider==="soccer"){try{const d=await oneFootballBundle(s),a=d.events.filter(x=>inDateRange(x,dates));',
'''async function scoreboardFor(s,dates,needs=null){const m=league(s);if(m.provider==="soccer"){try{const d=await oneFootballBundle(s,needs||{recent:1,upcoming:1}),a=d.events.filter(x=>inDateRange(x,dates));''', 1)

s = s.replace('async function teamsFor(s){const m=league(s);if(m.provider==="soccer"){try{const a=(await oneFootballBundle(s)).teams;if(a.length)return a}catch(_){}',
'''async function teamsFor(s){const m=league(s);if(m.provider==="soccer"){try{const meta=await oneFootballMeta(s),a=meta.table.map(x=>({id:x.id,name:x.name,short:x.short,logo:x.logo}));if(a.length)return a}catch(_){}''', 1)

s = s.replace('async function standingsFor(s){const m=league(s);if(m.provider==="soccer"){try{const a=(await oneFootballBundle(s)).table;if(a.length)return a}catch(_){}',
'''async function standingsFor(s){const m=league(s);if(m.provider==="soccer"){try{const a=(await oneFootballMeta(s)).table;if(a.length)return a}catch(_){}''', 1)

old_data = re.search(r'async function data\(s\)\{.*?\}\n\nfunction timeoutAfter', s, re.S)
assert old_data, 'data() not found'
new_data = '''function eventNeeds(s){
  const scoped=!!(s.teamId||s.teamName),lastVisible=s.showLast?(s.showTable?Math.min(s.maxMatches,3):s.maxMatches):0,nextVisible=s.showNext?(s.showTable?Math.min(s.maxMatches,2):s.maxMatches):0;
  return{recent:clamp(Math.max(1,lastVisible,s.showForm&&scoped?5:0),1,8),upcoming:clamp(Math.max(1,nextVisible),1,8)}
}
function eventWindow(s,needs){
  const slow=s.sportId==="football"||s.sportId==="floorball",past=Math.max(slow?14:7,needs.recent*(slow?10:4)),future=Math.max(slow?28:10,needs.upcoming*(slow?14:7));
  return range(-past,future)
}
async function data(s){
  const key=`${s.sportId}|${s.leagueId}|${s.teamId||"all"}`;
  try{
    const needs=eventNeeds(s),window=eventWindow(s,needs),all=unique(await scoreboardFor(s,window,needs));
    let table=[];if(s.showTable)try{table=await standingsFor(s)}catch(_){}
    if(s.showTable&&s.showLogos&&table.length&&table.some(x=>!x.logo)){try{const teams=await teamsFor(s),logos=new Map(teams.filter(x=>x?.id&&x?.logo).map(x=>[String(x.id),x.logo]));table=table.map(x=>Object.assign({},x,{logo:x.logo||logos.get(String(x.id||""))||""}))}catch(_){}}
    if(!all.length&&!table.length)throw new Error("No data");
    const ev=all.filter(e=>!(s.teamId||s.teamName)||eventMatches(e,s)),now=Date.now(),live=ev.filter(e=>e.state==="in"),done=ev.filter(e=>e.completed||e.state==="post").sort((a,b)=>new Date(b.date)-new Date(a.date)).slice(0,needs.recent),next=ev.filter(e=>e.state!=="in"&&!(e.completed||e.state==="post")&&new Date(e.date).getTime()>now-4*3600000).sort((a,b)=>new Date(a.date)-new Date(b.date)).slice(0,needs.upcoming);
    const d={source:"online",at:Date.now(),live,done,next,current:(s.showLive?live[0]:null)||next[0]||done[0]||null,form:(s.teamId||s.teamName)?done.slice(0,5).map(e=>result(e,s)).filter(Boolean):[],table};cacheWrite(key,d);return d
  }catch(e){console.log(e);const c=cacheRead(key);return c?.data?Object.assign({},c.data,{source:"cache",at:c.ts||c.data.at}):{source:"error",at:Date.now(),live:[],done:[],next:[],current:null,form:[],table:[]}}
}

function timeoutAfter'''
s = s[:old_data.start()] + new_data + s[old_data.end():]

assert 'range(-60,0)' not in s and 'range(0,120)' not in s
assert 'idx-4' not in s and 'idx+7' not in s
assert 'function eventNeeds(s)' in s
assert 'oneFootballBundle(s,needs' in s
assert 'const APP_VERSION = "2.5.8";' in s

p.write_text(s, encoding='utf-8')
subprocess.run(['node','--check',str(p)], check=True)
subprocess.run(['python','.github/scripts/build_sports_info_package.py'], check=True)
print('Sports Info 2.5.8 focused event loading ready')
