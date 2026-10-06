from pathlib import Path
import json
import re
import subprocess

APP_DIR = Path("apps/Sports-Info")
SRC = APP_DIR / "Sports Info.js"
PACKAGE = APP_DIR / "Sports Info.scriptable"

script = SRC.read_text(encoding="utf-8")

# One-shot migration for v2.5.40. The modern Livesport table is loaded from
# the tournament/stage ids (ZE/ZC) already present in the summary feed.
if 'const APP_VERSION = "2.5.39";' in script:
    def one(old, new, label):
        global script
        count = script.count(old)
        assert count == 1, f"{label}: expected one match, got {count}"
        script = script.replace(old, new, 1)

    one('// Sports Info v2.5.39', '// Sports Info v2.5.40', 'version comment')
    one('const APP_VERSION = "2.5.39";', 'const APP_VERSION = "2.5.40";', 'version')
    one(
        '{id:"floorball.cz",provider:"floorball",lsPath:"/floorball/czech-republic/livesport-superliga/",sofaId:829,sofaSport:"floorball",sportsApiQuery:"Superliga Czechia",flag:"🇨🇿",cs:"Livesport Superliga",en:"Czech Livesport Superliga",de:"Tschechische Livesport Superliga",es:"Livesport Superliga Checa"}',
        '{id:"floorball.cz",provider:"livesport",lsPath:"/floorball/czech-republic/livesport-superliga/",flag:"🇨🇿",cs:"Livesport Superliga",en:"Czech Livesport Superliga",de:"Tschechische Livesport Superliga",es:"Livesport Superliga Checa"}',
        'Czech floorball mapping',
    )

    start = script.index('async function livesportBundle(s){')
    end = script.index('\n\nconst SPORTSAPI_MEM={};', start)
    livesport = r'''async function livesportDynamicTable(s,html){
  const feed=lsFeed(html,"summary-results")||lsFeed(html,"summary-fixtures"),head=String(feed||"").split("¬~AA÷")[0],meta=lsFields(head),tournament=meta.ZE||"",stage=meta.ZC||"";
  if(!tournament||!stage)throw new Error("Livesport table ids missing");
  const headers=Object.assign({},LIVESPORT_HEADERS,{"Accept":"*/*","Accept-Language":"cs-CZ,cs;q=0.9,en;q=0.8","Referer":"https://www.livesport.cz/","Origin":"https://www.livesport.cz","x-fsign":"SW9D1eZo"});
  const raw=await requestText(`https://global.flashscore.ninja/1/x/feed/to_${encodeURIComponent(tournament)}_${encodeURIComponent(stage)}_1`,headers),rows=lsRows(raw);
  if(!rows.length)throw new Error("Livesport standings returned 0 rows");
  return rows
}
async function livesportBundle(s){
  const m=league(s),key=`ls:${m.id}`;
  if(LIVESPORT_MEM[key])return LIVESPORT_MEM[key];
  if(!m.lsPath)throw new Error("No Livesport mapping");
  const base=`https://www.livesport.com${m.lsPath}`,pages=await Promise.allSettled([requestText(base,LIVESPORT_HEADERS),requestText(base+"standings/",LIVESPORT_HEADERS)]),html=pages[0].status==="fulfilled"?pages[0].value:"",standHtml=pages[1].status==="fulfilled"?pages[1].value:"",events=unique([...lsEvents(lsFeed(html,"summary-results")),...lsEvents(lsFeed(html,"summary-fixtures"))]);
  let table=[];
  for(const f of lsAllFeeds(standHtml)){const r=lsRows(f.data);if(r.length>table.length)table=r}
  if(!table.length)try{table=await livesportDynamicTable(s,html||standHtml)}catch(e){console.log(`Livesport standings: ${String(e?.message||e)}`)}
  if(!table.length&&m.sofaId)try{table=(await sofaBundle(s)).table||[]}catch(_){}
  if(!events.length&&!table.length)throw new Error("Livesport returned no data");
  const map=new Map();
  for(const x of table)if(x.id)map.set(x.id,{id:x.id,name:x.name,short:x.short,logo:""});
  for(const e of events)for(const t of[e.home,e.away])if(t.id)map.set(t.id,{id:t.id,name:t.name,short:t.short,logo:t.logo});
  const out={events,teams:[...map.values()].sort((a,b)=>a.name.localeCompare(b.name)),table};
  LIVESPORT_MEM[key]=out;
  return out
}'''
    script = script[:start] + livesport + script[end:]

    one(
        'if(m.provider==="livesport"){const d=await limited(()=>livesportBundle(s),9000,"Livesport");return `Livesport OK · ${d.events.length} events`}',
        'if(m.provider==="livesport"){const d=await limited(()=>livesportBundle(s),9000,"Livesport");return `Livesport OK · ${d.events.length} events · ${d.table.length} rows`}',
        'Livesport diagnostics',
    )

    SRC.write_text(script, encoding="utf-8")
    tmp = Path('/tmp/SportsInfo.mjs')
    tmp.write_text(script, encoding='utf-8')
    subprocess.run(['node', '--check', str(tmp)], check=True)
    assert 'id:"floorball.cz",provider:"livesport"' in script
    assert 'global.flashscore.ninja/1/x/feed/to_' in script

    subprocess.run(['git', 'config', 'user.name', 'CaseyCZ'], check=True)
    subprocess.run(['git', 'config', 'user.email', '25530709+CaseyCZ@users.noreply.github.com'], check=True)
    subprocess.run(['git', 'add', str(SRC)], check=True)
    subprocess.run(['git', 'commit', '-m', 'Fix Livesport standings and Czech floorball source'], check=True)
    subprocess.run(['git', 'push', 'origin', 'HEAD:Master'], check=True)
elif 'const APP_VERSION = "2.5.40";' not in script:
    raise AssertionError('Unexpected Sports Info version; refusing one-shot migration')

assert 'const APP_NAME = "Sports Info";' in script
version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script)
assert version_match, "APP_VERSION missing from Sports Info.js"
version = version_match.group(1)

package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "trophy"},
    "name": "Sports Info",
    "script": script,
    "share_sheet_inputs": [],
}
PACKAGE.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Sports Info v{version} package synchronized")
