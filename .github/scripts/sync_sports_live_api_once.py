from pathlib import Path

info_path = Path('apps/Sports-Info/Sports Info.js')
live_path = Path('apps/Sports-Live/Sports-Live,js')
info = info_path.read_text(encoding='utf-8')
live = live_path.read_text(encoding='utf-8')

info_s0 = info.index('const SPORTS = [')
info_s1 = info.index('\n\nconst T = {', info_s0)
live_s0 = live.index('const SPORTS = [')
live_s1 = live.index('\n\nconst T = {', live_s0)
live = live[:live_s0] + info[info_s0:info_s1] + live[live_s1:]

info_d0 = info.index('function dateKey(d)')
info_d1 = info.index('function cacheRead(', info_d0)
provider_block = info[info_d0:info_d1]
live_d0 = live.index('function dateKey(d)')
live_d1 = live.index('function norm(v)', live_d0)

live_adapter = '''function sportsLiveEventWindow(s,needs,level=0){
  const slow=s.sportId==="football"||s.sportId==="floorball",past=Math.max(slow?14:7,needs.recent*(slow?10:4)),baseFuture=Math.max(slow?28:10,needs.upcoming*(slow?14:7));
  const future=level<=0?baseFuture:level===1?Math.max(baseFuture,30):Math.max(baseFuture,60);
  return range(-past,future)
}
async function eventsFor(s){
  const needs={recent:5,upcoming:clamp(Number(s.nextCount)||4,1,8)};
  let all=[];
  for(let level=0;level<3&&!all.length;level++){
    try{all=unique(await scoreboardFor(s,sportsLiveEventWindow(s,needs,level),needs))}catch(e){if(level===2)throw e}
  }
  return all
}
async function tableFor(s){return await standingsFor(s)}

'''

live = live[:live_d0] + provider_block + live_adapter + live[live_d1:]
live = live.replace('const API_TIMEOUT = 8;', 'const API_TIMEOUT = 7;', 1)
live = live.replace('// Sports Live v0.2.0', '// Sports Live v0.2.1', 1)
live = live.replace('const APP_VERSION = "0.2.0";', 'const APP_VERSION = "0.2.1";', 1)

expected = {
    'apiEspnBase':'https://site.api.espn.com',
    'apiFotmobBase':'https://www.fotmob.com/api/data',
    'apiOneFootballFeedBase':'https://feedmonster.onefootball.com',
    'apiOneFootballScoresBase':'https://api.onefootball.com',
    'apiSofaBase':'https://api.sofascore.com/api/v1',
    'apiSportsApiBase':'https://v2.floorball.sportsapipro.com',
}
for key, value in expected.items():
    token = f'{key}:"{value}"'
    if token not in live:
        raise SystemExit(f'Missing Sports Info API default in Sports Live: {token}')

live_path.write_text(live, encoding='utf-8')
out = live_path.read_text(encoding='utf-8')
out_s0 = out.index('const SPORTS = [')
out_s1 = out.index('\n\nconst T = {', out_s0)
if out[out_s0:out_s1] != info[info_s0:info_s1]:
    raise SystemExit('SPORTS catalogue differs from Sports Info')
out_d0 = out.index('function dateKey(d)')
if out[out_d0:out_d0 + len(provider_block)] != provider_block:
    raise SystemExit('Provider/API block differs from Sports Info')
