from pathlib import Path
import re

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.10";' in s
s = s.replace('const APP_VERSION = "2.5.10";', 'const APP_VERSION = "2.5.11";', 1)
s = s.replace('// Sports Info v2.5.10', '// Sports Info v2.5.11', 1)

profiles_new = r'''const TABLE_PROFILES={
  football:[["team","TÝM",116],["played","Z",20],["wins","V",20],["draws","R",20],["losses","P",20],["score","SK",42],["diff","RS",28],["points","B",28]],
  hockey:[["team","TÝM",118],["played","Z",20],["wins","V",20],["otWins","VP",22],["otLosses","PP",22],["losses","P",20],["score","SK",40],["points","B",28]],
  basketball:[["team","TÝM",130],["played","Z",22],["wins","V",22],["losses","P",22],["pct","%",44],["score","SK",52]],
  floorball:[["team","TÝM",124],["played","Z",20],["wins","V",20],["draws","R",20],["losses","P",20],["score","SK",42],["points","B",28]],
  baseball:[["team","TÝM",138],["played","Z",22],["wins","W",22],["losses","L",22],["pct","PCT",48],["gb","GB",40]]
};
'''
s, n = re.subn(r'const TABLE_PROFILES=\{[\s\S]*?\n\};\n(?=function standingTeamLabel)', profiles_new, s, count=1)
assert n == 1, 'TABLE_PROFILES block not replaced'

table_new = r'''async function table(parent,s,d,p){
  let all=d.table||[];if(!all.length)return;
  const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1;
  const shownUpcoming=s.showNext&&d.current?Math.min(d.next.filter(x=>x.id!==d.current.id).length,2):0;
  const shownLast=s.showLast&&d.current?Math.min(d.done.filter(x=>x.id!==d.current.id).length,s.showTable?3:s.maxMatches):0;
  let capacity=d.current?13:16;if(shownUpcoming>1)capacity-=shownUpcoming-1;if(shownLast)capacity-=shownLast+1;if(s.showForm&&(s.teamId||s.teamName)&&d.form.length)capacity-=1;
  const maxRows=Math.min(all.length,clamp(capacity,6,16));
  let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);
  const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football,teamCol=cols[0],statCols=cols.slice(1);
  title(parent,tx(s,"standings"),p);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();
  {
    const [,label,width]=teamCol,c=h.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
    const t=txt(c,label,8,p.muted,true);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer()
  }
  h.addSpacer();
  for(const [key,label,width] of statCols)lineCell(h,label,width,p.muted,"center",true,8,1);
  parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
    {
      const [key,,width]=teamCol,color=fav?p.accent:p.text,c=r.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
      if(s.showLogos&&x.logo){const img=await logo(x.logo,x.id||x.name);if(img){const im=c.addImage(img);im.imageSize=new Size(13,13);c.addSpacer(4)}}
      const t=txt(c,standingValue(x,key),11,color,fav);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer()
    }
    r.addSpacer();
    for(const [key,,width] of statCols){const color=fav?p.accent:p.muted;lineCell(r,standingValue(x,key),width,color,"center",fav||key==="points",10,1)}
    parent.addSpacer(1)
  }
}
'''
s, n = re.subn(r'async function table\(parent,s,d,p\)\{[\s\S]*?\n\}\n(?=function autoRefreshMinutes)', table_new, s, count=1)
assert n == 1, 'table block not replaced'

p.write_text(s, encoding='utf-8')
print('Patched Sports Info to 2.5.11')
