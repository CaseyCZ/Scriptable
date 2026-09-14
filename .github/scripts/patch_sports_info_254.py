from pathlib import Path

path = Path('apps/Sports-Info/Sports Info.js')
s = path.read_text(encoding='utf-8')

replacements = [
    ('// Sports Info v2.5.3', '// Sports Info v2.5.4'),
    ('const APP_VERSION = "2.5.3";', 'const APP_VERSION = "2.5.4";'),
    (
        'return {rank:Number(stat(q,["rank","position","playoffSeed"],i+1))||i+1,id:String(t.id||""),name:t.displayName||t.name||"",short:t.abbreviation||t.shortDisplayName||t.displayName||"",played:String(played??""),wins:String(wins??""),won:String(wins??""),draws:String(draws??""),drawn:String(draws??""),losses:String(losses??""),lost:String(losses??""),otWins:String(otWins??""),otLosses:String(otLosses??""),points:String(stat(q,["points","pts"],"")),pct:String(pct??""),gb:String(gb??""),gf:String(gf??""),ga:String(ga??""),diff:String(diff??"")}',
        'return {rank:Number(stat(q,["rank","position","playoffSeed"],i+1))||i+1,id:String(t.id||""),name:t.displayName||t.name||"",short:t.abbreviation||t.shortDisplayName||t.displayName||"",logo:t.logos?.[0]?.href||t.logo||"",played:String(played??""),wins:String(wins??""),won:String(wins??""),draws:String(draws??""),drawn:String(draws??""),losses:String(losses??""),lost:String(losses??""),otWins:String(otWins??""),otLosses:String(otLosses??""),points:String(stat(q,["points","pts"],"")),pct:String(pct??""),gb:String(gb??""),gf:String(gf??""),ga:String(ga??""),diff:String(diff??"")}'
    ),
    (
        'out.push({rank:Number(x.idx||x.rank||out.length+1),id,name:x.name||x.teamName||"",short:x.shortName||x.name||x.teamName||"",played:String(x.played??""),wins:String(wins),won:String(wins),draws:String(draws),drawn:String(draws),losses:String(losses),lost:String(losses),otWins:String(x.otWins??""),otLosses:String(x.otLosses??x.otl??""),points:String(x.pts??x.points??""),pct:String(x.pct??x.winPercentage??""),gb:String(x.gb??x.gamesBehind??""),gf:String(gf),ga:String(ga),diff:String(x.goalDifference??x.diff??""),form:Array.isArray(x.form)?x.form:[]})',
        'out.push({rank:Number(x.idx||x.rank||out.length+1),id,name:x.name||x.teamName||"",short:x.shortName||x.name||x.teamName||"",logo:id?`https://images.fotmob.com/image_resources/logo/teamlogo/${id}.png`:"",played:String(x.played??""),wins:String(wins),won:String(wins),draws:String(draws),drawn:String(draws),losses:String(losses),lost:String(losses),otWins:String(x.otWins??""),otLosses:String(x.otLosses??x.otl??""),points:String(x.pts??x.points??""),pct:String(x.pct??x.winPercentage??""),gb:String(x.gb??x.gamesBehind??""),gf:String(gf),ga:String(ga),diff:String(x.goalDifference??x.diff??""),form:Array.isArray(x.form)?x.form:[]})'
    ),
    (
        'let table=[];if(s.showTable)try{table=await standingsFor(s)}catch(_){}if(!all.length&&!table.length)throw new Error("No data");',
        'let table=[];if(s.showTable)try{table=await standingsFor(s)}catch(_){}if(s.showTable&&s.showLogos&&table.length&&table.some(x=>!x.logo)){try{const teams=await teamsFor(s),logos=new Map(teams.filter(x=>x?.id&&x?.logo).map(x=>[String(x.id),x.logo]));table=table.map(x=>Object.assign({},x,{logo:x.logo||logos.get(String(x.id||""))||""}))}catch(_){}}if(!all.length&&!table.length)throw new Error("No data");'
    ),
    (
        'b.setPadding(family==="small"?8:10,10,family==="small"?8:10,10);',
        'b.setPadding(family==="small"?8:10,family==="small"?5:10,family==="small"?8:10,family==="small"?5:10);'
    ),
    ('const widths=family==="small"?[58,16,58]:[128,36,128];', 'const widths=family==="small"?[60,16,60]:[128,36,128];'),
    (
'''const TABLE_PROFILES={
  football:[["rank","#",15],["team","TÝM",100],["played","Z",19],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",39],["diff","RS",23],["points","B",22]],
  hockey:[["rank","#",15],["team","TÝM",92],["played","Z",18],["wins","V",18],["otWins","VP",21],["otLosses","PP",21],["losses","P",18],["score","SK",37],["points","B",22]],
  basketball:[["rank","#",15],["team","TÝM",108],["played","Z",22],["wins","V",22],["losses","P",22],["pct","%",38],["score","SK",47]],
  floorball:[["rank","#",15],["team","TÝM",104],["played","Z",19],["wins","V",18],["draws","R",18],["losses","P",18],["score","SK",40],["points","B",23]],
  baseball:[["rank","#",15],["team","TÝM",112],["played","Z",22],["wins","W",22],["losses","L",22],["pct","PCT",39],["gb","GB",31]]
};''',
'''const TABLE_PROFILES={
  football:[["rank","#",16],["team","TÝM",116],["played","Z",19],["wins","V",19],["draws","R",19],["losses","P",19],["score","SK",40],["diff","RS",24],["points","B",23]],
  hockey:[["rank","#",16],["team","TÝM",112],["played","Z",18],["wins","V",18],["otWins","VP",22],["otLosses","PP",22],["losses","P",18],["score","SK",38],["points","B",23]],
  basketball:[["rank","#",16],["team","TÝM",126],["played","Z",22],["wins","V",22],["losses","P",22],["pct","%",38],["score","SK",48]],
  floorball:[["rank","#",16],["team","TÝM",136],["played","Z",19],["wins","V",19],["draws","R",19],["losses","P",19],["score","SK",41],["points","B",23]],
  baseball:[["rank","#",16],["team","TÝM",134],["played","Z",22],["wins","W",22],["losses","L",22],["pct","PCT",40],["gb","GB",32]]
};'''
    ),
    (
'''  const h=parent.addStack();h.layoutHorizontally();for(const [key,label,width] of cols)lineCell(h,label,width,p.muted,key==="team"?"left":"center",true,7,.9);parent.addSpacer(2);
  for(const x of rows){const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();for(const [key,,width] of cols){const color=fav?p.accent:(key==="team"?p.text:p.muted),size=key==="team"?9:8,min=key==="team"?1:.8;lineCell(r,standingValue(x,key),width,color,key==="team"?"left":"center",fav||key==="points",size,min)}}
}''',
'''  const h=parent.addStack();h.layoutHorizontally();for(const [key,label,width] of cols)lineCell(h,label,width,p.muted,key==="team"?"left":"center",true,8,1);parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();
    for(const [key,,width] of cols){
      const color=fav?p.accent:(key==="team"?p.text:p.muted);
      if(key==="team"){
        const c=r.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);
        if(s.showLogos&&x.logo){const i=await logo(x.logo,x.id||x.name);if(i){const im=c.addImage(i);im.imageSize=new Size(12,12);c.addSpacer(4)}}
        const t=txt(c,standingValue(x,key),10,color,fav);t.lineLimit=1;t.minimumScaleFactor=1;c.addSpacer();
      }else lineCell(r,standingValue(x,key),width,color,"center",fav||key==="points",9,1)
    }
    parent.addSpacer(1)
  }
}'''
    ),
    ('function table(parent,s,d,p){', 'async function table(parent,s,d,p){'),
    (
        'async function widget(s,family){const d=await data(s),p=pal(s),w=new ListWidget();w.backgroundColor=p.bg;w.setPadding(s.compact?10:12,s.compact?10:12,s.compact?10:12,s.compact?10:12);',
        'async function widget(s,family){const d=await data(s),p=pal(s),w=new ListWidget();w.backgroundColor=p.bg;const sidePad=family==="small"?6:(family==="large"?8:(s.compact?10:12)),verticalPad=s.compact?10:12;w.setPadding(verticalPad,sidePad,verticalPad,sidePad);'
    ),
    ('{w.addSpacer(9);table(w,s,d,p)}Script.setWidget(w);return w}', '{w.addSpacer(9);await table(w,s,d,p)}Script.setWidget(w);return w}'),
    ('{w.addSpacer(9);table(w,s,d,p)}if(family==="large")', '{w.addSpacer(9);await table(w,s,d,p)}if(family==="large")'),
]

for old, new in replacements:
    if old not in s:
        raise SystemExit('Expected block not found:\n' + old[:240])
    s = s.replace(old, new, 1)

path.write_text(s, encoding='utf-8')

# Remove one-shot patch files in the same release commit.
Path('.github/scripts/patch_sports_info_254.py').unlink(missing_ok=True)
Path('.github/workflows/patch-sports-info-254-once.yml').unlink(missing_ok=True)
