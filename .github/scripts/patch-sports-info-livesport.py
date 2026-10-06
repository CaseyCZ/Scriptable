from pathlib import Path
import re

path = Path("apps/Sports-Info/Sports Info.js")
text = path.read_text(encoding="utf-8")


def once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    text = text.replace(old, new, 1)


def regex_once(pattern: str, replacement: str, label: str) -> None:
    global text
    text2, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    text = text2


once("// Sports Info v2.5.39", "// Sports Info v2.5.40", "version comment")
once('const APP_VERSION = "2.5.39";', 'const APP_VERSION = "2.5.40";', "app version")

once(
    '{id:"floorball.cz",provider:"floorball",lsPath:"/floorball/czech-republic/livesport-superliga/",sofaId:829,sofaSport:"floorball",sportsApiQuery:"Superliga Czechia",flag:"🇨🇿",cs:"Livesport Superliga",en:"Czech Livesport Superliga",de:"Tschechische Livesport Superliga",es:"Livesport Superliga Checa"}',
    '{id:"floorball.cz",provider:"livesport",lsPath:"/floorball/czech-republic/livesport-superliga/",flag:"🇨🇿",cs:"Livesport Superliga",en:"Czech Livesport Superliga",de:"Tschechische Livesport Superliga",es:"Livesport Superliga Checa"}',
    "Czech floorball mapping",
)

replacement = r'''async function livesportDynamicTable(s,html){
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
  if(!events.length&&!table.length)throw new Error("Livesport returned no data");
  const map=new Map();
  for(const x of table)if(x.id)map.set(x.id,{id:x.id,name:x.name,short:x.short,logo:""});
  for(const e of events)for(const t of[e.home,e.away])if(t.id)map.set(t.id,{id:t.id,name:t.name,short:t.short,logo:t.logo});
  const out={events,teams:[...map.values()].sort((a,b)=>a.name.localeCompare(b.name)),table};
  LIVESPORT_MEM[key]=out;
  return out
}'''
regex_once(
    r'async function livesportBundle\(s\)\{.*?\}\n\nconst SPORTSAPI_MEM=\{\};',
    replacement + "\n\nconst SPORTSAPI_MEM={};",
    "Livesport bundle",
)

regex_once(
    r'if\(m\.provider==="livesport"\)\{const a=\(await livesportBundle\(s\)\)\.table;.*?return\[\]\}if\(m\.provider==="floorball"\)',
    'if(m.provider==="livesport")return(await livesportBundle(s)).table;if(m.provider==="floorball")',
    "standingsFor Livesport branch",
)

old_diag = 'if(m.provider==="livesport"){const d=await limited(()=>livesportBundle(s),9000,"Livesport");return `Livesport OK · ${d.events.length} events`}'
new_diag = 'if(m.provider==="livesport"){const d=await limited(()=>livesportBundle(s),9000,"Livesport");return `Livesport OK · ${d.events.length} events · ${d.table.length} rows`}'
once(old_diag, new_diag, "Livesport diagnostics")

path.write_text(text, encoding="utf-8")
print("Patched Sports Info to v2.5.40")
