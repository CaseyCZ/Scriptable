from pathlib import Path

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.14";' in s
s = s.replace('const APP_VERSION = "2.5.14";', 'const APP_VERSION = "2.6.0";', 1)
s = s.replace('// Sports Info v2.5.14', '// Sports Info v2.6.0', 1)

old_match = '''async function matchCard(parent,e,s,p,family="medium"){
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
    const scoreText=score(e),scoreW=clamp(tableTextWidth(scoreText,20,true),38,58),rowW=284,teamW=Math.floor((rowW-scoreW)/2);
    await teamCell(r,e.home,s,p,family,true,teamW);
    const mid=r.addStack();mid.layoutHorizontally();mid.centerAlignContent();mid.size=new Size(scoreW,0);mid.addSpacer();
    const sc=txt(mid,scoreText,20,p.text,true);sc.centerAlignText();sc.minimumScaleFactor=1;mid.addSpacer();
    await teamCell(r,e.away,s,p,family,false,teamW)
  }
}'''
new_match = '''async function matchCard(parent,e,s,p,family="medium"){
  const b=parent.addStack();b.layoutVertically();b.backgroundColor=p.panel;b.cornerRadius=14;b.setPadding(family==="small"?8:10,family==="small"?0:10,family==="small"?8:10,family==="small"?0:10);
  const h=b.addStack();h.layoutHorizontally();const st=txt(h,state(s,e),9,e.state==="in"?p.live:p.muted,true);st.minimumScaleFactor=1;h.addSpacer();if(e.state==="in")txt(h,"●",9,p.live,true);
  b.addSpacer(family==="small"?5:7);
  const r=b.addStack();r.layoutHorizontally();r.centerAlignContent();
  const scoreText=score(e),scoreSize=family==="small"?15:20,scoreW=clamp(tableTextWidth(scoreText,scoreSize,true),family==="small"?18:36,family==="small"?46:66);
  await teamCell(r,e.home,s,p,family,false,0);
  r.addSpacer(family==="small"?3:6);
  const mid=r.addStack();mid.layoutHorizontally();mid.centerAlignContent();mid.size=new Size(scoreW,0);mid.addSpacer();
  const sc=txt(mid,scoreText,scoreSize,p.text,true);sc.centerAlignText();sc.minimumScaleFactor=1;mid.addSpacer();
  r.addSpacer(family==="small"?3:6);
  await teamCell(r,e.away,s,p,family,false,0)
}'''
assert old_match in s, 'matchCard block not found'
s = s.replace(old_match, new_match, 1)

old_line = '''async function line(parent,e,s,p,family="large"){const r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();const dateW=40,teamW=106,scoreW=54;lineCell(r,day(s,e.date),dateW,p.muted,"left",true,9,.8);lineCell(r,teamLabel(e.home,family),teamW,p.text,"right",true,10,1);lineCell(r,score(e)==="–"?time(s,e.date):score(e),scoreW,e.state==="in"?p.live:p.text,"center",true,10,1);lineCell(r,teamLabel(e.away,family),teamW,p.text,"left",true,10,1)}'''
new_line = '''async function line(parent,e,s,p,family="large"){
  const r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
  const dateText=day(s,e.date),midText=score(e)==="–"?time(s,e.date):score(e),dateW=clamp(tableTextWidth(dateText,9,true),34,60),scoreW=clamp(tableTextWidth(midText,10,true),38,68);
  lineCell(r,dateText,dateW,p.muted,"left",true,9,1);r.addSpacer(4);
  const home=r.addStack();home.layoutHorizontally();home.centerAlignContent();home.addSpacer();const ht=txt(home,teamLabel(e.home,family),10,p.text,true);ht.lineLimit=1;ht.minimumScaleFactor=1;
  r.addSpacer(5);lineCell(r,midText,scoreW,e.state==="in"?p.live:p.text,"center",true,10,1);r.addSpacer(5);
  const away=r.addStack();away.layoutHorizontally();away.centerAlignContent();const at=txt(away,teamLabel(e.away,family),10,p.text,true);at.lineLimit=1;at.minimumScaleFactor=1;away.addSpacer()
}'''
assert old_line in s, 'line() block not found'
s = s.replace(old_line, new_line, 1)

old_layout = '''function dynamicTableLayout(rows,cols,showLogos){
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
}'''
new_layout = '''function dynamicTableLayout(rows,cols){
  const team=cols[0],stats=cols.slice(1);
  const statCols=stats.map(([key,label])=>{
    const widest=[label,...rows.map(r=>standingValue(r,key))].reduce((a,v)=>Math.max(a,tableTextWidth(v,10,key==="points")),0);
    const min=label.length>=3?32:label.length===2?25:22;
    const max=key==="score"?58:key==="pct"?52:key==="gb"?46:42;
    return [key,label,clamp(widest,min,max)]
  });
  const statsWidth=statCols.reduce((a,c)=>a+c[2],0);
  return {teamLabel:team[1],statCols,statsWidth}
}'''
assert old_layout in s, 'dynamicTableLayout block not found'
s = s.replace(old_layout, new_layout, 1)

start = s.index('async function table(parent,s,d,p){')
end = s.index('\nfunction autoRefreshMinutes', start)
new_table = '''async function table(parent,s,d,p){
  let all=d.table||[];if(!all.length)return;
  const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1;
  const shownUpcoming=s.showNext&&d.current?Math.min(d.next.filter(x=>x.id!==d.current.id).length,2):0;
  const shownLast=s.showLast&&d.current?Math.min(d.done.filter(x=>x.id!==d.current.id).length,s.showTable?3:s.maxMatches):0;
  let capacity=d.current?14:17;if(shownUpcoming>1)capacity-=shownUpcoming-1;if(shownLast)capacity-=shownLast+1;if(s.showForm&&(s.teamId||s.teamName)&&d.form.length)capacity-=1;
  const maxRows=Math.min(all.length,clamp(capacity,6,17));
  let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);
  const cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football,{teamLabel,statCols,statsWidth}=dynamicTableLayout(rows,cols);
  title(parent,tx(s,"standings"),p);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();const th=txt(h,teamLabel,8,p.muted,true);th.lineLimit=1;th.minimumScaleFactor=1;h.addSpacer();
  const hs=h.addStack();hs.layoutHorizontally();hs.size=new Size(statsWidth,0);for(const [key,label,width] of statCols)lineCell(hs,label,width,p.muted,"center",true,8,1);
  parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
    const color=fav?p.accent:p.text,c=r.addStack();c.layoutHorizontally();c.centerAlignContent();
    if(s.showLogos&&x.logo){const img=await logo(x.logo,x.id||x.name);if(img){const im=c.addImage(img);im.imageSize=new Size(13,13);c.addSpacer(4)}}
    const t=txt(c,standingValue(x,"team"),11,color,fav);t.lineLimit=1;t.minimumScaleFactor=.62;c.addSpacer();
    r.addSpacer();
    const rs=r.addStack();rs.layoutHorizontally();rs.size=new Size(statsWidth,0);
    for(const [key,,width] of statCols){const statColor=fav?p.accent:p.muted;const v=lineCell(rs,standingValue(x,key),width,statColor,"center",fav||key==="points",10,1);v.lineLimit=1}
    parent.addSpacer(1)
  }
}'''
s = s[:start] + new_table + s[end:]

p.write_text(s, encoding='utf-8')
print('Patched Sports Info to 2.6.0 fluid content-driven layout')
