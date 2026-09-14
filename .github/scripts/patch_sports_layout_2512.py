from pathlib import Path
import re

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.11";' in s
s = s.replace('const APP_VERSION = "2.5.11";', 'const APP_VERSION = "2.5.12";', 1)
s = s.replace('// Sports Info v2.5.11', '// Sports Info v2.5.12', 1)

profiles_new = r'''const TABLE_PROFILES={
  football:[["team","TÝM",110],["played","Z",18],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",40],["diff","RS",26],["points","B",28]],
  hockey:[["team","TÝM",110],["played","Z",18],["wins","V",18],["otWins","VP",22],["otLosses","PP",22],["losses","P",18],["score","SK",40],["points","B",28]],
  basketball:[["team","TÝM",126],["played","Z",20],["wins","V",20],["losses","P",20],["pct","%",42],["score","SK",48]],
  floorball:[["team","TÝM",136],["played","Z",18],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",40],["points","B",28]],
  baseball:[["team","TÝM",130],["played","Z",20],["wins","W",20],["losses","L",20],["pct","PCT",46],["gb","GB",40]]
};
'''
s, n = re.subn(r'const TABLE_PROFILES=\{[\s\S]*?\n\};\n(?=function standingTeamLabel)', profiles_new, s, count=1)
assert n == 1, 'TABLE_PROFILES block not replaced'

table_new = r'''async function table(parent,s,d,p){
  let all=d.table||[];if(!all.length)return;
  const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1;
  const shownUpcoming=s.showNext&&d.current?Math.min(d.next.filter(x=>x.id!==d.current.id).length,2):0;
  const shownLast=s.showLast&&d.current?Math.min(d.done.filter(x=>x.id!==d.current.id).length,s.showTable?3:s.maxMatches):0;
  let capacity=d.current?14:17;if(shownUpcoming>1)capacity-=shownUpcoming-1;if(shownLast)capacity-=shownLast+1;if(s.showForm&&(s.teamId||s.teamName)&&d.form.length)capacity-=1;
  const maxRows=Math.min(all.length,clamp(capacity,6,17));
  let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);
  const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football,teamCol=cols[0],statCols=cols.slice(1),statsWidth=statCols.reduce((a,c)=>a+c[2],0);
  title(parent,tx(s,"standings"),p);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();
  {
    const [,label,width]=teamCol,c=h.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
    const t=txt(c,label,8,p.muted,true);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer()
  }
  h.addSpacer();
  const hs=h.addStack();hs.layoutHorizontally();hs.size=new Size(statsWidth,0);
  for(const [key,label,width] of statCols)lineCell(hs,label,width,p.muted,"center",true,8,.8);
  parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
    {
      const [key,,width]=teamCol,color=fav?p.accent:p.text,c=r.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
      if(s.showLogos&&x.logo){const img=await logo(x.logo,x.id||x.name);if(img){const im=c.addImage(img);im.imageSize=new Size(13,13);c.addSpacer(4)}}
      const t=txt(c,standingValue(x,key),11,color,fav);t.lineLimit=1;t.minimumScaleFactor=.85;c.addSpacer()
    }
    r.addSpacer();
    const rs=r.addStack();rs.layoutHorizontally();rs.size=new Size(statsWidth,0);
    for(const [key,,width] of statCols){const color=fav?p.accent:p.muted;lineCell(rs,standingValue(x,key),width,color,"center",fav||key==="points",10,.8)}
    parent.addSpacer(1)
  }
}
'''
s, n = re.subn(r'async function table\(parent,s,d,p\)\{[\s\S]*?\n\}\n(?=function autoRefreshMinutes)', table_new, s, count=1)
assert n == 1, 'table block not replaced'

old_footer = 'if(family==="large"){w.addSpacer();const f=w.addStack();f.addSpacer();txt(f,`${tx(s,"updated")}: ${new Date(d.at||Date.now()).toLocaleTimeString(s.language||"en",{hour:"2-digit",minute:"2-digit"})}`,8,p.muted);f.addSpacer()}'
assert old_footer in s, 'large footer not found'
s = s.replace(old_footer, '', 1)

p.write_text(s, encoding='utf-8')
print('Patched Sports Info to 2.5.12')
