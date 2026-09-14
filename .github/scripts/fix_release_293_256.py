from pathlib import Path
import json
import re

# ---- LockScreen Generator 2.9.3 ----
lock_path = Path('apps/LockScreenGenerator/LockScreenGenerator.js')
lock = lock_path.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.9.2";' in lock
lock = lock.replace('const APP_VERSION = "2.9.2";', 'const APP_VERSION = "2.9.3";', 1)
old = "document.getElementById('phoneSourcesStatus').textContent=${JSON.stringify(PHONE_TEXT.loading)};"
new = "document.getElementById('phoneSourcesStatus').textContent=PHONE_TEXT.loading;"
assert old in lock
lock = lock.replace(old, new, 1)
assert 'window.__sourcesLoaded=falsewindow.__updateReady=false;' in lock
lock = lock.replace('window.__sourcesLoaded=falsewindow.__updateReady=false;', 'window.__sourcesLoaded=false;window.__updateReady=false;', 1)
lock_path.write_text(lock, encoding='utf-8')

# ---- Sports Info 2.5.6 ----
sports_path = Path('apps/Sports-Info/Sports Info.js')
s = sports_path.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.5.5";' in s
s = s.replace('const APP_VERSION = "2.5.5";', 'const APP_VERSION = "2.5.6";', 1)
s = re.sub(r'// Sports Info v[^\n]+', '// Sports Info v2.5.6', s, count=1)

# Restore normal widget margins. The table itself will use the available width.
old = 'const sidePad=family==="small"?3:(family==="large"?8:(s.compact?10:12))'
new = 'const sidePad=family==="small"?6:(s.compact?10:12)'
assert old in s
s = s.replace(old, new, 1)

old = 'b.setPadding(family==="small"?8:10,family==="small"?2:10,family==="small"?8:10,family==="small"?2:10);'
new = 'b.setPadding(family==="small"?8:10,family==="small"?3:10,family==="small"?8:10,family==="small"?3:10);'
assert old in s
s = s.replace(old, new, 1)
assert 'const widths=family==="small"?[67,14,67]:[128,36,128];' in s
s = s.replace('const widths=family==="small"?[67,14,67]:[128,36,128];', 'const widths=family==="small"?[62,14,62]:[128,36,128];', 1)

profiles = '''const TABLE_PROFILES={
  football:[["rank","#",14],["team","TÝM",116],["played","Z",16],["wins","V",16],["draws","R",16],["losses","P",16],["score","SK",36],["diff","RS",22],["points","B",20]],
  hockey:[["rank","#",14],["team","TÝM",108],["played","Z",16],["wins","V",16],["otWins","VP",19],["otLosses","PP",19],["losses","P",16],["score","SK",34],["points","B",20]],
  basketball:[["rank","#",14],["team","TÝM",122],["played","Z",18],["wins","V",18],["losses","P",18],["pct","%",38],["score","SK",46]],
  floorball:[["rank","#",14],["team","TÝM",116],["played","Z",16],["wins","V",16],["draws","R",16],["losses","P",16],["score","SK",36],["points","B",20]],
  baseball:[["rank","#",14],["team","TÝM",124],["played","Z",18],["wins","W",18],["losses","L",18],["pct","PCT",38],["gb","GB",30]]
};
function standingTeamLabel'''
s, n = re.subn(r'const TABLE_PROFILES=\{[\s\S]*?\n\};\nfunction standingTeamLabel', profiles, s, count=1)
assert n == 1

table_fn = '''async function table(parent,s,d,p){
  let all=d.table||[];if(!all.length)return;
  const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1;
  const shownUpcoming=s.showNext&&d.current?Math.min(d.next.filter(x=>x.id!==d.current.id).length,2):0;
  const shownLast=s.showLast&&d.current?Math.min(d.done.filter(x=>x.id!==d.current.id).length,s.showTable?3:s.maxMatches):0;
  let capacity=d.current?13:16;if(shownUpcoming>1)capacity-=shownUpcoming-1;if(shownLast)capacity-=shownLast+1;if(s.showForm&&(s.teamId||s.teamName)&&d.form.length)capacity-=1;
  const maxRows=Math.min(all.length,clamp(capacity,6,16));
  let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);
  const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football;
  const addGap=(stack,key,index)=>{if(key!=="rank"&&index<cols.length-1)stack.addSpacer()};
  title(parent,tx(s,"standings"),p);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();
  for(let i=0;i<cols.length;i++){const [key,label,width]=cols[i];lineCell(h,label,width,p.muted,key==="team"?"left":"center",true,8,1);addGap(h,key,i)}
  parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
    for(let i=0;i<cols.length;i++){
      const [key,,width]=cols[i],color=fav?p.accent:(key==="team"?p.text:p.muted);
      if(key==="team"){
        const c=r.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
        if(s.showLogos&&x.logo){const img=await logo(x.logo,x.id||x.name);if(img){const im=c.addImage(img);im.imageSize=new Size(13,13);c.addSpacer(4)}}
        const t=txt(c,standingValue(x,key),11,color,fav);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer();
      }else lineCell(r,standingValue(x,key),width,color,"center",fav||key==="points",10,1);
      addGap(r,key,i)
    }
    parent.addSpacer(1)
  }
}
function autoRefreshMinutes'''
s, n = re.subn(r'async function table\(parent,s,d,p\)\{[\s\S]*?\n\}\nfunction autoRefreshMinutes', table_fn, s, count=1)
assert n == 1
sports_path.write_text(s, encoding='utf-8')

# Build exact .scriptable packages.
def build_package(app_dir, src_name, out_name, name, color, glyph):
    app = Path(app_dir)
    src = (app/src_name).read_text(encoding='utf-8')
    pkg = {
        'always_run_in_app': False,
        'icon': {'color': color, 'glyph': glyph},
        'name': name,
        'script': src,
        'share_sheet_inputs': [],
    }
    (app/out_name).write_text(json.dumps(pkg, ensure_ascii=False, indent=2), encoding='utf-8')

build_package('apps/LockScreenGenerator','LockScreenGenerator.js','LockScreenGenerator.scriptable','LockScreen Generator','deep-blue','magic')
build_package('apps/Sports-Info','Sports Info.js','Sports Info.scriptable','Sports Info','deep-blue','trophy')

# Release metadata.
root = Path('README.md')
t = root.read_text(encoding='utf-8')
t, n1 = re.subn(r'(\| 🪄 \*\*LockScreen Generator\*\* \| ✅ v)[^ |]+( \|)', r'\g<1>2.9.3\2', t, count=1)
t, n2 = re.subn(r'(\| 🏆 \*\*Sports Info\*\* \| ✅ v)[^ |]+( \|)', r'\g<1>2.5.6\2', t, count=1)
assert n1 == n2 == 1
root.write_text(t, encoding='utf-8')

lr = Path('apps/LockScreenGenerator/README.md')
t = lr.read_text(encoding='utf-8')
t, n = re.subn(r'version-[0-9.]+-0284c7', 'version-2.9.3-0284c7', t, count=1)
assert n == 1
lr.write_text(t, encoding='utf-8')

sr = Path('apps/Sports-Info/README.md')
t = sr.read_text(encoding='utf-8')
t, n = re.subn(r'(\*\*Sports Info v)[^ ]+( — Production\*\*)', r'\g<1>2.5.6\2', t, count=1)
assert n == 1
sr.write_text(t, encoding='utf-8')

site = Path('index.html')
t = site.read_text(encoding='utf-8')
t, n1 = re.subn(r"(\{name:'LockScreen Generator',version:')[^']+(')", r"\g<1>2.9.3\2", t, count=1)
t, n2 = re.subn(r"(\{name:'Sports Info',version:')[^']+(')", r"\g<1>2.5.6\2", t, count=1)
assert n1 == n2 == 1
site.write_text(t, encoding='utf-8')

print('Patched LockScreen 2.9.3 and Sports Info 2.5.6')
