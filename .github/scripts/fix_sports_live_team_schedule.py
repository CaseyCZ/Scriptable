from pathlib import Path

p = Path('apps/Sports-Live/Sports-Live,js')
s = p.read_text(encoding='utf-8')

# Sports Live is a single-team view. Keep the Sports Info provider/API layer,
# but expand the Sports Info date window based on matches for the selected team,
# not merely on whether the league returned any events.
start = s.index('async function eventsFor(s){')
end = s.index('async function tableFor(s)', start)
new_events = '''async function eventsFor(s){
  const needs={recent:5,upcoming:clamp(Number(s.nextCount)||4,1,8)};
  let all=unique(await scoreboardFor(s,sportsLiveEventWindow(s,needs,0),needs));
  for(let level=1;level<=2;level++){
    const scoped=all.filter(e=>eventMatchesTeam(e,s)),now=Date.now();
    const upcoming=scoped.filter(e=>e.state!=="in"&&!e.completed&&e.state!=="post"&&new Date(e.date).getTime()>now-4*3600000).length;
    if(scoped.length&&upcoming>=needs.upcoming)break;
    try{all=unique([...all,...await scoreboardFor(s,sportsLiveEventWindow(s,needs,level),needs)])}catch(_){break}
  }
  return all
}
'''
s = s[:start] + new_events + s[end:]

start = s.index('async function prepareData(s){')
end = s.index('\n\nfunction dark(s)', start)
new_prepare = '''async function prepareData(s){
  if(!s.teamId&&!s.teamName)return{source:"error",reason:"team",current:null,nextGames:[]};
  const key=cacheKey(s);
  try{
    const events=await eventsFor(s);
    let rows=[];try{rows=await tableFor(s)}catch(e){console.log(e)}
    const all=events.filter(e=>eventMatchesTeam(e,s)).sort((a,b)=>new Date(a.date)-new Date(b.date)),now=Date.now();
    if(!all.length)throw new Error(`No team events · ${leagueName(s)} · ${sourceName(s)}`);
    const live=all.filter(e=>e.state==="in"),future=all.filter(e=>e.state!=="in"&&!e.completed&&e.state!=="post"&&new Date(e.date).getTime()>now-4*3600000),done=all.filter(e=>e.completed||e.state==="post").sort((a,b)=>new Date(b.date)-new Date(a.date));
    const current=live[0]||future[0]||done[0]||null;
    if(!current)throw new Error(`No current event · ${leagueName(s)}`);
    const my=teamIs(current.home,s)?current.home:current.away,op=teamIs(current.home,s)?current.away:current.home;
    const nextGames=future.filter(e=>e.id!==current.id).slice(0,s.nextCount).map(e=>{const opponent=teamIs(e.home,s)?e.away:e.home;return{gameDate:e.date,opponent}});
    const data={source:"online",current:{id:current.id,gameDate:current.date,gameStatus:current.status||"",state:current.state,venue:current.venue||"",homeTeam:Object.assign({},current.home,{record:recOf(current.home,rows)}),awayTeam:Object.assign({},current.away,{record:recOf(current.away,rows)}),myTeam:my,opponent:op,nextGames},nextGames};
    writeCache(key,data);return data
  }catch(e){console.log(e);return cached(key)||{source:"error",reason:String(e?.message||e),current:null,nextGames:[]}}
}'''
s = s[:start] + new_prepare + s[end:]

s = s.replace('// Sports Live v0.2.2', '// Sports Live v0.2.3', 1)
s = s.replace('const APP_VERSION = "0.2.2";', 'const APP_VERSION = "0.2.3";', 1)

p.write_text(s, encoding='utf-8')
