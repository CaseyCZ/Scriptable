from pathlib import Path

p = Path('apps/Sports-Live/Sports-Live,js')
s = p.read_text(encoding='utf-8')

old = '''async function eventsFor(s){
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

new = '''async function espnTeamSchedule(s){
  const m=league(s),base=s.apiEspnBase||DEFAULTS.apiEspnBase;
  let teamId=String(s.teamId||"");
  if(!teamId&&s.teamName){
    const wanted=norm(s.teamName),teams=await espnTeams(s);
    const hit=teams.find(t=>{const n=norm(t.name||t.short);return n===wanted||n.includes(wanted)||wanted.includes(n)});
    teamId=String(hit?.id||"")
  }
  if(!teamId)return[];
  const d=await requestJSON(`${base}/apis/site/v2/sports/${encodeURIComponent(m.espnSport)}/${encodeURIComponent(m.espnLeague)}/teams/${encodeURIComponent(teamId)}/schedule`);
  return unique((d.events||[]).map(normEvent).filter(Boolean))
}
async function eventsFor(s){
  const m=league(s);
  if(m.provider==="espn")return await espnTeamSchedule(s);
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

if old not in s:
    raise SystemExit('eventsFor block not found')

s = s.replace(old, new, 1)
s = s.replace('// Sports Live v0.2.3', '// Sports Live v0.2.4', 1)
s = s.replace('const APP_VERSION = "0.2.3";', 'const APP_VERSION = "0.2.4";', 1)
p.write_text(s, encoding='utf-8')
