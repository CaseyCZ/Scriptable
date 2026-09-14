from pathlib import Path

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.12";' in s
s = s.replace('const APP_VERSION = "2.5.12";', 'const APP_VERSION = "2.5.13";', 1)
s = s.replace('// Sports Info v2.5.12', '// Sports Info v2.5.13', 1)

old_profiles = '''const TABLE_PROFILES={
  football:[["team","TÝM",110],["played","Z",18],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",40],["diff","RS",26],["points","B",28]],
  hockey:[["team","TÝM",110],["played","Z",18],["wins","V",18],["otWins","VP",22],["otLosses","PP",22],["losses","P",18],["score","SK",40],["points","B",28]],
  basketball:[["team","TÝM",126],["played","Z",20],["wins","V",20],["losses","P",20],["pct","%",42],["score","SK",48]],
  floorball:[["team","TÝM",136],["played","Z",18],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",40],["points","B",28]],
  baseball:[["team","TÝM",130],["played","Z",20],["wins","W",20],["losses","L",20],["pct","PCT",46],["gb","GB",40]]
};'''
new_profiles = '''const TABLE_PROFILES={
  football:[["team","TÝM"],["played","Z"],["wins","V"],["draws","R"],["losses","P"],["score","SK"],["diff","RS"],["points","B"]],
  hockey:[["team","TÝM"],["played","Z"],["wins","V"],["otWins","VP"],["otLosses","PP"],["losses","P"],["score","SK"],["points","B"]],
  basketball:[["team","TÝM"],["played","Z"],["wins","V"],["losses","P"],["pct","%"],["score","SK"]],
  floorball:[["team","TÝM"],["played","Z"],["wins","V"],["draws","R"],["losses","P"],["score","SK"],["points","B"]],
  baseball:[["team","TÝM"],["played","Z"],["wins","W"],["losses","L"],["pct","PCT"],["gb","GB"]]
};'''
assert old_profiles in s, 'TABLE_PROFILES block not found'
s = s.replace(old_profiles, new_profiles, 1)

marker = '''function standingValue(x,key){'''
idx = s.index(marker)
end = s.index('\nasync function table(parent,s,d,p){', idx)
standing_block = s[idx:end]

helpers = '''\nfunction tableTextWidth(value,size=10,bold=false){
  const text=String(value??"–"),factor=bold?.61:.58;
  return Math.ceil(text.length*size*factor)+8
}
function dynamicTableLayout(rows,cols,showLogos){
  const TOTAL=300,team=cols[0],stats=cols.slice(1);
  const statCols=stats.map(([key,label])=>{
    const widest=[label,...rows.map(r=>standingValue(r,key))].reduce((a,v)=>Math.max(a,tableTextWidth(v,10,key==="points")),0);
    const min=label.length>=3?32:label.length===2?25:22;
    const max=key==="score"?54:key==="pct"?50:key==="gb"?44:40;
    return [key,label,clamp(widest,min,max)]
  });
  const statsWidth=statCols.reduce((a,c)=>a+c[2],0);
  const logoSpace=showLogos?17:0;
  const wantedTeam=Math.max(86,...rows.map(r=>logoSpace+tableTextWidth(standingValue(r,"team"),11,false)));
  const maxTeam=Math.max(86,TOTAL-statsWidth);
  const teamWidth=Math.min(wantedTeam,maxTeam);
  return {teamCol:[team[0],team[1],teamWidth],statCols,statsWidth,total:teamWidth+statsWidth}
}
'''
s = s[:end] + helpers + s[end:]

old_table_start = s.index('async function table(parent,s,d,p){')
old_table_end = s.index('\nfunction autoRefreshMinutes', old_table_start)
old_table = s[old_table_start:old_table_end]
new_table = '''async function table(parent,s,d,p){
  let all=d.table||[];if(!all.length)return;
  const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1;
  const shownUpcoming=s.showNext&&d.current?Math.min(d.next.filter(x=>x.id!==d.current.id).length,2):0;
  const shownLast=s.showLast&&d.current?Math.min(d.done.filter(x=>x.id!==d.current.id).length,s.showTable?3:s.maxMatches):0;
  let capacity=d.current?14:17;if(shownUpcoming>1)capacity-=shownUpcoming-1;if(shownLast)capacity-=shownLast+1;if(s.showForm&&(s.teamId||s.teamName)&&d.form.length)capacity-=1;
  const maxRows=Math.min(all.length,clamp(capacity,6,17));
  let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);
  const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football,{teamCol,statCols}=dynamicTableLayout(rows,cols,s.showLogos);
  title(parent,tx(s,"standings"),p);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();
  {
    const [,label,width]=teamCol,c=h.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
    const t=txt(c,label,8,p.muted,true);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer()
  }
  for(const [key,label,width] of statCols){lineCell(h,label,width,p.muted,"center",true,8,1)}
  parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
    {
      const [key,,width]=teamCol,color=fav?p.accent:p.text,c=r.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
      if(s.showLogos&&x.logo){const img=await logo(x.logo,x.id||x.name);if(img){const im=c.addImage(img);im.imageSize=new Size(13,13);c.addSpacer(4)}}
      const t=txt(c,standingValue(x,key),11,color,fav);t.lineLimit=1;t.minimumScaleFactor=.62;c.addSpacer()
    }
    for(const [key,,width] of statCols){const color=fav?p.accent:p.muted;const t=lineCell(r,standingValue(x,key),width,color,"center",fav||key==="points",10,1);t.lineLimit=1}
    parent.addSpacer(1)
  }
}'''
s = s[:old_table_start] + new_table + s[old_table_end:]

p.write_text(s, encoding='utf-8')
print('Patched Sports Info to 2.5.13 with dynamic tables for all sports')
