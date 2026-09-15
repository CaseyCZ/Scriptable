from pathlib import Path

p=Path('apps/Sports-Info/Sports Info.js')
s=p.read_text(encoding='utf-8')

repls=[
('// Sports Info v2.5.22','// Sports Info v2.5.23'),
('const APP_VERSION = "2.5.22";','const APP_VERSION = "2.5.23";'),
("if(family===\"large\"&&!['center','right'].includes(L.tableAlign))L.tableAlign='center'","if(family===\"large\"&&!['left','center','right'].includes(L.tableAlign))L.tableAlign='center'"),
('selectField("layoutLargeTableAlign",lt(s,"tableAlign"),s.layout.large.tableAlign,[["center",lt(s,"center")],["right",lt(s,"right")]],lh(s,"tableAlign"))','selectField("layoutLargeTableAlign",lt(s,"tableAlign"),s.layout.large.tableAlign,[["left",lt(s,"left")],["center",lt(s,"center")],["right",lt(s,"right")]],lh(s,"tableAlign"))'),
("document.querySelectorAll('[id^=layoutLargeTable]').forEach(e=>{e.addEventListener('input',markTableManual);e.addEventListener('change',markTableManual)})","document.querySelectorAll('#layoutLargeTable input[type=number]').forEach(e=>{e.addEventListener('input',markTableManual);e.addEventListener('change',markTableManual)})")
]
for old,new in repls:
    if old not in s:
        raise SystemExit(f'missing marker: {old[:100]}')
    s=s.replace(old,new,1)

old='''function automaticTableSlotLayout(s,cols,rows=[]){
  const L=layoutFor(s,"large"),stats=cols.slice(1,8),target=303,teamValues=[cols[0]?.[1]||"TÝM",...rows.map(x=>standingValue(x,"team"))];
  let teamWidth=clamp(Math.max(...teamValues.map(v=>tableTextWidth(v,L.tableTeamFont,true)))+(s.showLogos?18:0),60,180);
  const statCols=stats.map(([key,label])=>{const vals=[label,...rows.map(x=>standingValue(x,key))],need=Math.max(tableTextWidth(label,L.tableHeaderFont,true),...vals.map(v=>tableTextWidth(v,L.tableFont,key==="points")));const min=key==="score"?30:20,max=key==="score"?80:56;return[key,label,clamp(need,min,max)]});
  const minFor=key=>key==="score"?30:20;
  let statsWidth=statCols.reduce((a,c)=>a+c[2],0),overflow=teamWidth+4+statsWidth-target;
  if(overflow>0){const take=Math.min(overflow,teamWidth-60);teamWidth-=take;overflow-=take}
  while(overflow>0){let changed=false;for(const c of [...statCols].sort((a,b)=>b[2]-a[2])){const min=minFor(c[0]);if(c[2]>min){c[2]--;overflow--;changed=true;if(overflow<=0)break}}if(!changed)break}
  statsWidth=statCols.reduce((a,c)=>a+c[2],0);
  LAST_AUTO_TABLE_LAYOUT={teamWidth,statsWidth,totalWidth:teamWidth+4+statsWidth,columns:Object.fromEntries(statCols.map(c=>[c[0],c[2]]))};
  return {teamCol:[cols[0][0],cols[0][1],teamWidth],statCols,statsWidth,auto:true}
}'''
new='''function automaticTableSlotLayout(s,cols,rows=[]){
  const L=layoutFor(s,"large"),stats=cols.slice(1,8),target=303,teamValues=[cols[0]?.[1]||"TÝM",...rows.map(x=>standingValue(x,"team"))],teamMin=96,teamMax=150;
  let teamWidth=clamp(Math.max(...teamValues.map(v=>tableTextWidth(v,L.tableTeamFont,true)))+(s.showLogos?18:0),teamMin,teamMax);
  const limits={};
  const statCols=stats.map(([key,label])=>{const vals=[label,...rows.map(x=>standingValue(x,key))],need=Math.max(tableTextWidth(label,L.tableHeaderFont,true),...vals.map(v=>tableTextWidth(v,L.tableFont,key==="points"))),min=key==="score"?30:(key==="pct"?28:20),max=key==="score"?80:(key==="pct"?50:56);limits[key]={min,max};return[key,label,clamp(need,min,max)]});
  let statsWidth=statCols.reduce((a,c)=>a+c[2],0),overflow=teamWidth+4+statsWidth-target;
  if(overflow>0){const take=Math.min(overflow,teamWidth-teamMin);teamWidth-=take;overflow-=take}
  while(overflow>0){let changed=false;for(const c of [...statCols].sort((a,b)=>b[2]-a[2])){const min=limits[c[0]].min;if(c[2]>min){c[2]--;overflow--;changed=true;if(overflow<=0)break}}if(!changed)break}
  statsWidth=statCols.reduce((a,c)=>a+c[2],0);
  let slack=target-(teamWidth+4+statsWidth);
  while(slack>0){let changed=false;for(const c of statCols){const max=limits[c[0]].max;if(c[2]<max){c[2]++;slack--;changed=true;if(slack<=0)break}}if(!changed)break}
  if(slack>0){const add=Math.min(slack,teamMax-teamWidth);teamWidth+=add;slack-=add}
  if(slack>0&&statCols.length){let i=0;while(slack>0){statCols[i%statCols.length][2]++;slack--;i++}}
  statsWidth=statCols.reduce((a,c)=>a+c[2],0);
  LAST_AUTO_TABLE_LAYOUT={teamWidth,statsWidth,totalWidth:teamWidth+4+statsWidth,columns:Object.fromEntries(statCols.map(c=>[c[0],c[2]]))};
  return {teamCol:[cols[0][0],cols[0][1],teamWidth],statCols,statsWidth,auto:true}
}'''
if old not in s:
    raise SystemExit('automaticTableSlotLayout marker missing')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('patched Sports Info 2.5.23')
