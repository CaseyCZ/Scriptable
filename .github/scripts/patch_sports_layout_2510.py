from pathlib import Path
import re

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.9";' in s
s = s.replace('const APP_VERSION = "2.5.9";', 'const APP_VERSION = "2.5.10";', 1)
s = s.replace('// Sports Info v2.5.9', '// Sports Info v2.5.10', 1)

match_new = r'''async function matchCard(parent,e,s,p,family="medium"){
  const b=parent.addStack();b.layoutVertically();b.backgroundColor=p.panel;b.cornerRadius=14;b.setPadding(family==="small"?8:10,family==="small"?0:10,family==="small"?8:10,family==="small"?0:10);
  const h=b.addStack();h.layoutHorizontally();txt(h,state(s,e),9,e.state==="in"?p.live:p.muted,true);h.addSpacer();if(e.state==="in")txt(h,"●",9,p.live,true);
  b.addSpacer(family==="small"?5:7);
  const r=b.addStack();r.layoutHorizontally();r.centerAlignContent();
  if(family==="small"){
    await teamCell(r,e.home,s,p,family,false,64);
    r.addSpacer();
    const mid=r.addStack();mid.layoutHorizontally();mid.centerAlignContent();mid.size=new Size(14,0);mid.addSpacer();
    const sc=txt(mid,score(e),15,p.text,true);sc.centerAlignText();mid.addSpacer();
    r.addSpacer();
    await teamCell(r,e.away,s,p,family,true,64)
  }else{
    await teamCell(r,e.home,s,p,family,true,128);
    const mid=r.addStack();mid.layoutHorizontally();mid.centerAlignContent();mid.size=new Size(36,0);mid.addSpacer();
    const sc=txt(mid,score(e),20,p.text,true);sc.centerAlignText();mid.addSpacer();
    await teamCell(r,e.away,s,p,family,false,128)
  }
}
'''

s, n = re.subn(r'async function matchCard\(parent,e,s,p,family="medium"\)\{[\s\S]*?\n\}\n(?=function lineCell)', match_new, s, count=1)
assert n == 1, 'matchCard block not replaced'

profiles_new = r'''const TABLE_PROFILES={
  football:[["team","TÝM",136],["played","Z",22],["wins","V",22],["draws","R",22],["losses","P",22],["score","SK",44],["diff","RS",30],["points","B",24]],
  hockey:[["team","TÝM",148],["played","Z",20],["wins","V",20],["otWins","VP",24],["otLosses","PP",24],["losses","P",20],["score","SK",42],["points","B",24]],
  basketball:[["team","TÝM",150],["played","Z",24],["wins","V",24],["losses","P",24],["pct","%",48],["score","SK",52]],
  floorball:[["team","TÝM",136],["played","Z",22],["wins","V",22],["draws","R",22],["losses","P",22],["score","SK",44],["points","B",24]],
  baseball:[["team","TÝM",160],["played","Z",24],["wins","W",24],["losses","L",24],["pct","PCT",50],["gb","GB",40]]
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
  const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football;
  title(parent,tx(s,"standings"),p);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();
  for(const [key,label,width] of cols){
    if(key==="team"){
      const c=h.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
      c.addSpacer(17);const t=txt(c,label,8,p.muted,true);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer()
    }else lineCell(h,label,width,p.muted,"center",true,8,1)
  }
  parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
    for(const [key,,width] of cols){
      const color=fav?p.accent:(key==="team"?p.text:p.muted);
      if(key==="team"){
        const c=r.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
        if(s.showLogos&&x.logo){const img=await logo(x.logo,x.id||x.name);if(img){const im=c.addImage(img);im.imageSize=new Size(13,13);c.addSpacer(4)}}
        const t=txt(c,standingValue(x,key),11,color,fav);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer();
      }else lineCell(r,standingValue(x,key),width,color,"center",fav||key==="points",10,1)
    }
    parent.addSpacer(1)
  }
}
'''
s, n = re.subn(r'async function table\(parent,s,d,p\)\{[\s\S]*?\n\}\n(?=function autoRefreshMinutes)', table_new, s, count=1)
assert n == 1, 'table block not replaced'

p.write_text(s, encoding='utf-8')
print('Patched Sports Info to 2.5.10')
