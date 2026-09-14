from pathlib import Path
import re

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.12";' in s, 'Expected Sports Info 2.5.12 base'
s = s.replace('// Sports Info v2.5.12', '// Sports Info v2.5.15', 1)
s = s.replace('const APP_VERSION = "2.5.12";', 'const APP_VERSION = "2.5.15";', 1)

layout_constants = r'''const LAYOUT_TEXT={
  cs:{layout:"Layout",layoutSub:"Každá velikost widgetu má vlastní nezávislé rozložení.",small:"Small",medium:"Medium",large:"Large",general:"Widget",match:"Hlavní zápas",lists:"Seznam zápasů",table:"Tabulka",preview:"Náhled",reset:"Obnovit výchozí",sidePadding:"Boční odsazení widgetu",verticalPadding:"Svislé odsazení widgetu",sectionSpacing:"Mezera mezi bloky",cardPaddingX:"Vnitřní odsazení karty do stran",cardPaddingY:"Vnitřní odsazení karty nahoře/dole",teamWidth:"Šířka týmu",scoreWidth:"Minimální šířka skóre",teamFont:"Velikost názvu týmu",scoreFont:"Velikost skóre",logoSize:"Velikost loga",logoGap:"Mezera logo–název",teamAlign:"Umístění týmů",edges:"Ke krajům",center:"Ke středu",listDateWidth:"Šířka data",listTeamWidth:"Šířka týmu v seznamu",listScoreWidth:"Min. šířka skóre/času",listFont:"Velikost textu seznamu",tableWidth:"Celková pracovní šířka tabulky",tableInsetLeft:"Odsazení tabulky vlevo",tableInsetRight:"Odsazení tabulky vpravo",tableTeamWidth:"Šířka sloupce TÝM",tableWideWidth:"Základ pozic 1–4",tableNarrowWidth:"Základ pozic 5–7",tableTeamFont:"Velikost názvu týmu v tabulce",tableStatFont:"Velikost statistik",tableHeaderFont:"Velikost hlavičky",tableRowSpacing:"Mezera mezi řádky",tableTeamAlign:"Zarovnání TÝM",tableStatAlign:"Zarovnání hodnot",tableHeaderAlign:"Zarovnání hlaviček",left:"Vlevo",right:"Vpravo",layoutHelp:"Změny platí pouze pro tuto velikost widgetu. Hodnoty jsou omezené tak, aby obsah zůstal uvnitř widgetu.",tableHelp:"Tabulka má až 7 statistických pozic. Pozice 1–4 mají vlastní širší základ, 5–7 užší. Sporty s méně sloupci automaticky využijí volné místo."},
  en:{layout:"Layout",layoutSub:"Each widget size has its own independent layout.",small:"Small",medium:"Medium",large:"Large",general:"Widget",match:"Main match",lists:"Match lists",table:"Standings",preview:"Preview",reset:"Reset defaults",sidePadding:"Widget side padding",verticalPadding:"Widget vertical padding",sectionSpacing:"Section spacing",cardPaddingX:"Card horizontal padding",cardPaddingY:"Card vertical padding",teamWidth:"Team width",scoreWidth:"Minimum score width",teamFont:"Team-name size",scoreFont:"Score size",logoSize:"Logo size",logoGap:"Logo–name gap",teamAlign:"Team placement",edges:"To edges",center:"Toward center",listDateWidth:"Date width",listTeamWidth:"List team width",listScoreWidth:"Min. score/time width",listFont:"List text size",tableWidth:"Standings working width",tableInsetLeft:"Standings left inset",tableInsetRight:"Standings right inset",tableTeamWidth:"TEAM column width",tableWideWidth:"Base slots 1–4",tableNarrowWidth:"Base slots 5–7",tableTeamFont:"Standings team text size",tableStatFont:"Statistics text size",tableHeaderFont:"Header text size",tableRowSpacing:"Row spacing",tableTeamAlign:"TEAM alignment",tableStatAlign:"Value alignment",tableHeaderAlign:"Header alignment",left:"Left",right:"Right",layoutHelp:"Changes apply only to this widget size. Values are constrained so content stays inside the widget.",tableHelp:"Standings use up to 7 statistic slots. Slots 1–4 have a wider base and 5–7 a narrower base. Sports with fewer columns automatically use the free space."},
  de:{layout:"Layout",layoutSub:"Jede Widget-Größe hat ein eigenes unabhängiges Layout.",small:"Small",medium:"Medium",large:"Large",general:"Widget",match:"Hauptspiel",lists:"Spiellisten",table:"Tabelle",preview:"Vorschau",reset:"Standard wiederherstellen",sidePadding:"Seitlicher Widget-Abstand",verticalPadding:"Vertikaler Widget-Abstand",sectionSpacing:"Abstand zwischen Blöcken",cardPaddingX:"Kartenabstand horizontal",cardPaddingY:"Kartenabstand vertikal",teamWidth:"Teambreite",scoreWidth:"Minimale Ergebnisbreite",teamFont:"Teamname-Größe",scoreFont:"Ergebnisgröße",logoSize:"Logogröße",logoGap:"Logo–Name Abstand",teamAlign:"Teamposition",edges:"Zu den Rändern",center:"Zur Mitte",listDateWidth:"Datumsbreite",listTeamWidth:"Teambreite in Listen",listScoreWidth:"Min. Ergebnis/Zeit-Breite",listFont:"Listentextgröße",tableWidth:"Arbeitsbreite der Tabelle",tableInsetLeft:"Tabelle links einrücken",tableInsetRight:"Tabelle rechts einrücken",tableTeamWidth:"Breite TEAM",tableWideWidth:"Basis Positionen 1–4",tableNarrowWidth:"Basis Positionen 5–7",tableTeamFont:"Teamtextgröße",tableStatFont:"Statistikgröße",tableHeaderFont:"Kopfzeilengröße",tableRowSpacing:"Zeilenabstand",tableTeamAlign:"TEAM-Ausrichtung",tableStatAlign:"Werteausrichtung",tableHeaderAlign:"Kopfzeilenausrichtung",left:"Links",right:"Rechts",layoutHelp:"Änderungen gelten nur für diese Widget-Größe. Sichere Grenzen halten den Inhalt im Widget.",tableHelp:"Die Tabelle nutzt bis zu 7 Statistikpositionen. Positionen 1–4 sind breiter, 5–7 schmaler. Weniger Spalten nutzen den freien Platz automatisch."},
  es:{layout:"Layout",layoutSub:"Cada tamaño de widget tiene su propio diseño independiente.",small:"Small",medium:"Medium",large:"Large",general:"Widget",match:"Partido principal",lists:"Listas de partidos",table:"Clasificación",preview:"Vista previa",reset:"Restablecer",sidePadding:"Margen lateral del widget",verticalPadding:"Margen vertical del widget",sectionSpacing:"Espacio entre bloques",cardPaddingX:"Margen horizontal de tarjeta",cardPaddingY:"Margen vertical de tarjeta",teamWidth:"Ancho del equipo",scoreWidth:"Ancho mínimo del marcador",teamFont:"Tamaño del nombre",scoreFont:"Tamaño del marcador",logoSize:"Tamaño del logo",logoGap:"Espacio logo–nombre",teamAlign:"Posición de equipos",edges:"A los bordes",center:"Al centro",listDateWidth:"Ancho de fecha",listTeamWidth:"Ancho del equipo en lista",listScoreWidth:"Ancho mín. marcador/hora",listFont:"Tamaño de texto de lista",tableWidth:"Ancho de trabajo de tabla",tableInsetLeft:"Margen izquierdo de tabla",tableInsetRight:"Margen derecho de tabla",tableTeamWidth:"Ancho EQUIPO",tableWideWidth:"Base posiciones 1–4",tableNarrowWidth:"Base posiciones 5–7",tableTeamFont:"Tamaño de equipo en tabla",tableStatFont:"Tamaño de estadísticas",tableHeaderFont:"Tamaño de cabecera",tableRowSpacing:"Espacio entre filas",tableTeamAlign:"Alineación EQUIPO",tableStatAlign:"Alineación de valores",tableHeaderAlign:"Alineación de cabeceras",left:"Izquierda",right:"Derecha",layoutHelp:"Los cambios solo afectan a este tamaño. Los límites seguros mantienen el contenido dentro del widget.",tableHelp:"La tabla usa hasta 7 posiciones estadísticas. Las posiciones 1–4 son más anchas y 5–7 más estrechas. Los deportes con menos columnas aprovechan automáticamente el espacio libre."}
};
function lh(s,k){const l=s.language||lang();return(LAYOUT_TEXT[l]||LAYOUT_TEXT.en)[k]||LAYOUT_TEXT.en[k]||k}
const LAYOUT_DEFAULTS={
  small:{sidePadding:6,verticalPadding:12,sectionSpacing:6,cardPaddingX:0,cardPaddingY:8,teamWidth:58,scoreWidth:18,teamFont:9,scoreFont:15,logoSize:12,logoGap:3,teamAlign:"edges"},
  medium:{sidePadding:12,verticalPadding:12,sectionSpacing:8,cardPaddingX:10,cardPaddingY:10,teamWidth:118,scoreWidth:40,teamFont:11,scoreFont:20,logoSize:17,logoGap:5,teamAlign:"center",listDateWidth:40,listTeamWidth:100,listScoreWidth:54,listFont:10},
  large:{sidePadding:10,verticalPadding:10,sectionSpacing:8,cardPaddingX:10,cardPaddingY:10,teamWidth:118,scoreWidth:44,teamFont:11,scoreFont:20,logoSize:17,logoGap:5,teamAlign:"center",listDateWidth:40,listTeamWidth:100,listScoreWidth:54,listFont:10,tableWidth:314,tableInsetLeft:0,tableInsetRight:0,tableTeamWidth:100,tableWideWidth:33,tableNarrowWidth:27,tableTeamFont:10,tableStatFont:9,tableHeaderFont:8,tableRowSpacing:1,tableTeamAlign:"left",tableStatAlign:"center",tableHeaderAlign:"center"}
};
const LAYOUT_LIMITS={
  small:{sidePadding:[0,20],verticalPadding:[6,24],sectionSpacing:[2,16],cardPaddingX:[0,20],cardPaddingY:[4,18],teamWidth:[42,78],scoreWidth:[14,42],teamFont:[7,12],scoreFont:[12,21],logoSize:[8,18],logoGap:[0,8]},
  medium:{sidePadding:[0,20],verticalPadding:[6,24],sectionSpacing:[2,18],cardPaddingX:[0,20],cardPaddingY:[4,18],teamWidth:[80,140],scoreWidth:[28,72],teamFont:[8,13],scoreFont:[14,25],logoSize:[10,22],logoGap:[0,10],listDateWidth:[30,60],listTeamWidth:[70,125],listScoreWidth:[38,80],listFont:[8,12]},
  large:{sidePadding:[0,20],verticalPadding:[6,24],sectionSpacing:[2,18],cardPaddingX:[0,20],cardPaddingY:[4,18],teamWidth:[80,140],scoreWidth:[28,72],teamFont:[8,13],scoreFont:[14,25],logoSize:[10,22],logoGap:[0,10],listDateWidth:[30,60],listTeamWidth:[70,125],listScoreWidth:[38,80],listFont:[8,12],tableWidth:[270,330],tableInsetLeft:[0,18],tableInsetRight:[0,18],tableTeamWidth:[78,150],tableWideWidth:[22,42],tableNarrowWidth:[18,36],tableTeamFont:[8,12],tableStatFont:[8,11],tableHeaderFont:[7,10],tableRowSpacing:[0,4]}
};
'''

assert 'const DEFAULTS={' in s
s = s.replace('const DEFAULTS={', layout_constants + '\nconst DEFAULTS={', 1)

new_defaults = 'const DEFAULTS={language:null,sportId:"football",leagueId:"cze.1",teamId:"",teamName:"",showLive:true,showLast:true,showNext:true,showTable:true,showForm:true,showLogos:true,maxMatches:4,theme:"auto",accent:"#38bdf8",background:"#0b1020",panelColor:"#111827",textColor:"#f8fafc",mutedColor:"#94a3b8",liveColor:"#f87171",winColor:"#86efac",compact:false,refreshMinutes:15,apiEspnBase:"https://site.api.espn.com",apiFotmobBase:"https://www.fotmob.com/api/data",apiOneFootballFeedBase:"https://feedmonster.onefootball.com",apiOneFootballScoresBase:"https://api.onefootball.com",apiSofaBase:"https://api.sofascore.com/api/v1",apiSportsApiBase:"https://v2.floorball.sportsapipro.com",sportsApiKey:"",layout:LAYOUT_DEFAULTS};'
s, n = re.subn(r'const DEFAULTS=\{[^\n]*\};', new_defaults, s, count=1)
assert n == 1, 'DEFAULTS replacement failed'

merge_new = r'''function normalizeLayout(raw){
  const out=clone(LAYOUT_DEFAULTS),src=raw&&typeof raw==="object"?raw:{};
  for(const fam of ["small","medium","large"]){
    const x=src[fam]&&typeof src[fam]==="object"?src[fam]:{};
    for(const [k,lim] of Object.entries(LAYOUT_LIMITS[fam])){const n=Number(x[k]);if(Number.isFinite(n))out[fam][k]=clamp(n,lim[0],lim[1])}
    if(["edges","center"].includes(x.teamAlign))out[fam].teamAlign=x.teamAlign;
  }
  const lg=src.large&&typeof src.large==="object"?src.large:{};
  if(["left","center","right"].includes(lg.tableTeamAlign))out.large.tableTeamAlign=lg.tableTeamAlign;
  if(["left","center","right"].includes(lg.tableStatAlign))out.large.tableStatAlign=lg.tableStatAlign;
  if(["left","center","right"].includes(lg.tableHeaderAlign))out.large.tableHeaderAlign=lg.tableHeaderAlign;
  return out
}
function merge(raw){
  const s=Object.assign(clone(DEFAULTS),raw||{});s.layout=normalizeLayout(raw?.layout);
  if(!["cs","en","de","es"].includes(s.language))s.language=null;
  if(!SPORTS.some(x=>x.id===s.sportId))s.sportId=DEFAULTS.sportId;
  const ls=leaguesForSport(s.sportId);if(!ls.some(x=>x.id===s.leagueId))s.leagueId=ls[0]?.id||DEFAULTS.leagueId;
  s.maxMatches=clamp(Number(s.maxMatches)||4,1,8);s.refreshMinutes=clamp(Number(s.refreshMinutes)||15,5,60);
  if(!["auto","dark","light","custom"].includes(s.theme))s.theme="auto";
  for(const k of["accent","background","panelColor","textColor","mutedColor","liveColor","winColor"])if(!/^#[0-9a-fA-F]{6}$/.test(String(s[k]||"")))s[k]=DEFAULTS[k];
  for(const k of["apiEspnBase","apiFotmobBase","apiOneFootballFeedBase","apiOneFootballScoresBase","apiSofaBase","apiSportsApiBase"])s[k]=String(s[k]||DEFAULTS[k]).replace(/\/+$/,"");
  s.sportsApiKey=String(s.sportsApiKey||"").trim();return s
}'''
s, n = re.subn(r'function merge\(raw\)\{[^\n]*\}', merge_new, s, count=1)
assert n == 1, 'merge replacement failed'

state_new = 'function state(s,e){const when=`${day(s,e.date)} · ${time(s,e.date)}`;if(e.state==="in")return `${when} · ${tx(s,"liveNow")}${e.status?` · ${e.status}`:""}`;if(e.completed||e.state==="post")return `${when}${e.status?` · ${e.status}`:""}`;return when}'
s, n = re.subn(r'function state\(s,e\)\{[^\n]*\}', state_new, s, count=1)
assert n == 1, 'state replacement failed'

match_block = r'''function familyLayout(s,family){return s?.layout?.[family]||LAYOUT_DEFAULTS[family]||LAYOUT_DEFAULTS.medium}
function approxTextWidth(value,size){const text=String(value??"");let units=0;for(const ch of text){if(/[MW@#%]/.test(ch))units+=.82;else if(/[ilI1\.\s]/.test(ch))units+=.34;else units+=.56}return Math.ceil(units*size)+4}
function teamLabel(t,family,s=null,width=0){
  const full=t.name||t.short||t.abbr||"",short=t.short&&t.short!==full?t.short:"",abbr=t.abbr&&t.abbr!==full?t.abbr:"";
  if(!s||!width)return family==="small"?full:(full.length<=22?full:(short||abbr||full));
  const L=familyLayout(s,family),font=L.teamFont,logoSpace=s.showLogos?(L.logoSize+L.logoGap):0,usable=Math.max(18,width-logoSpace-2),lines=family==="small"?2:1;
  for(const v of [full,short,abbr].filter(Boolean))if(approxTextWidth(v,font)<=usable*lines*.94)return v;
  return abbr||short||full
}
async function teamCell(parent,t,s,p,family,right=false,width=0,L=familyLayout(s,family)){
  const r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();if(width)r.size=new Size(width,0);if(right)r.addSpacer();
  if(s.showLogos){const i=await logo(t.logo,t.id||t.abbr);if(i){const v=r.addImage(i);v.imageSize=new Size(L.logoSize,L.logoSize);if(L.logoGap)r.addSpacer(L.logoGap)}}
  const z=txt(r,teamLabel(t,family,s,width),L.teamFont,p.text,true);z.lineLimit=family==="small"?2:1;z.minimumScaleFactor=1;
  if(!right)r.addSpacer()
}
async function matchCard(parent,e,s,p,family="medium"){
  const L=familyLayout(s,family),b=parent.addStack();b.layoutVertically();b.backgroundColor=p.panel;b.cornerRadius=14;b.setPadding(L.cardPaddingY,L.cardPaddingX,L.cardPaddingY,L.cardPaddingX);
  const h=b.addStack();h.layoutHorizontally();txt(h,state(s,e),9,e.state==="in"?p.live:p.muted,true);h.addSpacer();if(e.state==="in")txt(h,"●",9,p.live,true);
  b.addSpacer(Math.max(3,L.sectionSpacing-1));
  const r=b.addStack();r.layoutHorizontally();r.centerAlignContent(),value=score(e),needed=approxTextWidth(value,L.scoreFont)+8,scoreW=clamp(Math.max(L.scoreWidth,needed),L.scoreWidth,family==="small"?46:78),extra=Math.max(0,scoreW-L.scoreWidth),teamW=Math.max(family==="small"?38:68,L.teamWidth-Math.ceil(extra/2));
  const mid=()=>{const m=r.addStack();m.layoutHorizontally();m.centerAlignContent();m.size=new Size(scoreW,0);m.addSpacer();const sc=txt(m,value,L.scoreFont,p.text,true);sc.minimumScaleFactor=1;sc.centerAlignText();m.addSpacer()};
  if(L.teamAlign==="edges"){
    await teamCell(r,e.home,s,p,family,false,teamW,L);r.addSpacer();mid();r.addSpacer();await teamCell(r,e.away,s,p,family,true,teamW,L)
  }else{
    await teamCell(r,e.home,s,p,family,true,teamW,L);mid();await teamCell(r,e.away,s,p,family,false,teamW,L)
  }
}
function lineCell(parent,value,width,p,align="left",bold=false,size=10,minScale=.62){const c=parent.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);if(align==="right"||align==="center")c.addSpacer();const t=txt(c,value,size,p,bold);t.minimumScaleFactor=minScale;if(align==="center"){t.centerAlignText();c.addSpacer()}else if(align==="left")c.addSpacer();return t}
async function line(parent,e,s,p,family="large"){
  const L=familyLayout(s,family),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent(),midValue=score(e)==="–"?time(s,e.date):score(e),needed=approxTextWidth(midValue,L.listFont)+8,scoreW=clamp(Math.max(L.listScoreWidth,needed),L.listScoreWidth,86),extra=Math.max(0,scoreW-L.listScoreWidth),teamW=Math.max(58,L.listTeamWidth-Math.ceil(extra/2));
  lineCell(r,day(s,e.date),L.listDateWidth,p.muted,"left",true,Math.max(8,L.listFont-1),.85);lineCell(r,teamLabel(e.home,family,s,teamW),teamW,p.text,"right",true,L.listFont,1);lineCell(r,midValue,scoreW,e.state==="in"?p.live:p.text,"center",true,L.listFont,1);lineCell(r,teamLabel(e.away,family,s,teamW),teamW,p.text,"left",true,L.listFont,1)
}'''
s, n = re.subn(r'function teamLabel\(t,family\)\{[\s\S]*?(?=\nfunction title\()', match_block, s, count=1)
assert n == 1, 'match/team/list layout replacement failed'

s = s.replace('function title(parent,v,p){const r=parent.addStack();r.layoutHorizontally();txt(r,String(v).toUpperCase(),9,p.muted,true);r.addSpacer()}', 'function title(parent,v,p,inset=0){const r=parent.addStack();r.layoutHorizontally();if(inset)r.addSpacer(inset);txt(r,String(v).toUpperCase(),9,p.muted,true);r.addSpacer()}', 1)

profiles_new = r'''const TABLE_PROFILES={
  football:[["team","TÝM"],["played","Z"],["wins","V"],["draws","R"],["losses","P"],["score","SK"],["diff","RS"],["points","B"]],
  hockey:[["team","TÝM"],["played","Z"],["wins","V"],["otWins","VP"],["otLosses","PP"],["losses","P"],["score","SK"],["points","B"]],
  basketball:[["team","TÝM"],["played","Z"],["wins","V"],["losses","P"],["pct","%"],["score","SK"]],
  floorball:[["team","TÝM"],["played","Z"],["wins","V"],["draws","R"],["losses","P"],["score","SK"],["points","B"]],
  baseball:[["team","TÝM"],["played","Z"],["wins","W"],["losses","L"],["pct","PCT"],["gb","GB"]]
};
'''
s, n = re.subn(r'const TABLE_PROFILES=\{[\s\S]*?\n\};\n(?=function standingTeamLabel)', profiles_new, s, count=1)
assert n == 1, 'TABLE_PROFILES replacement failed'

# Keep a stable 7-slot grid while letting real values claim minimum readable width.
table_new = r'''function standingNameForWidth(x,width,font,showLogo){const full=x.name||x.short||"",short=x.short&&x.short!==full?x.short:"",usable=Math.max(20,width-(showLogo?17:0)-3);for(const v of [full,short].filter(Boolean))if(approxTextWidth(v,font)<=usable)return v;return short||full}
function tableSlotWidths(s,rows,statCols){
  const L=familyLayout(s,"large"),count=clamp(statCols.length,1,7),budget=clamp(L.tableWidth-L.tableInsetLeft-L.tableInsetRight,240,330),teamWidth=clamp(L.tableTeamWidth,70,Math.max(70,budget-112)),statsBudget=Math.max(112,budget-teamWidth),fullBase=[L.tableWideWidth,L.tableWideWidth,L.tableWideWidth,L.tableWideWidth,L.tableNarrowWidth,L.tableNarrowWidth,L.tableNarrowWidth],target=Math.min(fullBase.reduce((a,b)=>a+b,0),statsBudget),active=fullBase.slice(0,count),sum=active.reduce((a,b)=>a+b,0)||1;
  let widths=active.map(x=>Math.max(16,Math.floor(x*target/sum)));
  const required=statCols.map(([key,label])=>{let need=approxTextWidth(label,L.tableHeaderFont)+6;for(const row of rows)need=Math.max(need,approxTextWidth(standingValue(row,key),L.tableStatFont)+6);return clamp(need,16,56)});
  for(let i=0;i<widths.length;i++)widths[i]=Math.max(widths[i],required[i]);
  let total=widths.reduce((a,b)=>a+b,0);
  if(total>statsBudget){let overflow=total-statsBudget;for(let pass=0;pass<3&&overflow>0;pass++)for(let i=0;i<widths.length&&overflow>0;i++){const floor=Math.max(16,Math.min(required[i],widths[i])),can=Math.max(0,widths[i]-floor),take=Math.min(can,overflow);widths[i]-=take;overflow-=take}}
  total=widths.reduce((a,b)=>a+b,0);
  if(total<target){let left=target-total,i=0;while(left>0&&widths.length){widths[i%widths.length]++;left--;i++}}
  return{teamWidth,widths,statsWidth:widths.reduce((a,b)=>a+b,0),budget}
}
function addTeamTableCell(parent,x,width,s,p,fav,L){const c=parent.addStack();c.layoutHorizontally();c.centerAlignContent();c.size=new Size(width,0);const align=L.tableTeamAlign;if(align==="right"||align==="center")c.addSpacer();if(s.showLogos&&x.logo){return logo(x.logo,x.id||x.name).then(img=>{if(img){const im=c.addImage(img);im.imageSize=new Size(13,13);c.addSpacer(4)}const t=txt(c,standingNameForWidth(x,width,L.tableTeamFont,s.showLogos),L.tableTeamFont,fav?p.accent:p.text,fav);t.minimumScaleFactor=1;if(align==="center")c.addSpacer();else if(align==="left")c.addSpacer();return t})}const t=txt(c,standingNameForWidth(x,width,L.tableTeamFont,false),L.tableTeamFont,fav?p.accent:p.text,fav);t.minimumScaleFactor=1;if(align==="center")c.addSpacer();else if(align==="left")c.addSpacer();return Promise.resolve(t)}
async function table(parent,s,d,p){
  let all=d.table||[];if(!all.length)return;
  const hasFav=!!(s.teamId||s.teamName),favIndex=hasFav?all.findIndex(x=>teamMatches(x,s)):-1;
  const shownUpcoming=s.showNext&&d.current?Math.min(d.next.filter(x=>x.id!==d.current.id).length,2):0;
  const shownLast=s.showLast&&d.current?Math.min(d.done.filter(x=>x.id!==d.current.id).length,s.showTable?3:s.maxMatches):0;
  let capacity=d.current?14:17;if(shownUpcoming>1)capacity-=shownUpcoming-1;if(shownLast)capacity-=shownLast+1;if(s.showForm&&(s.teamId||s.teamName)&&d.form.length)capacity-=1;
  const maxRows=Math.min(all.length,clamp(capacity,6,17));
  let rows;if(hasFav&&favIndex>=0&&maxRows<all.length){const start=Math.max(0,Math.min(favIndex-Math.floor(maxRows/2),all.length-maxRows));rows=all.slice(start,start+maxRows)}else rows=all.slice(0,maxRows);
  const L=familyLayout(s,"large"),cols=TABLE_PROFILES[s.sportId]||TABLE_PROFILES.football,teamCol=cols[0],statCols=cols.slice(1),grid=tableSlotWidths(s,rows,statCols);
  title(parent,tx(s,"standings"),p,L.tableInsetLeft);parent.addSpacer(3);
  const h=parent.addStack();h.layoutHorizontally();if(L.tableInsetLeft)h.addSpacer(L.tableInsetLeft);lineCell(h,teamCol[1],grid.teamWidth,p.muted,L.tableTeamAlign,true,L.tableHeaderFont,1);h.addSpacer();const hs=h.addStack();hs.layoutHorizontally();hs.size=new Size(grid.statsWidth,0);for(let i=0;i<statCols.length;i++)lineCell(hs,statCols[i][1],grid.widths[i],p.muted,L.tableHeaderAlign,true,L.tableHeaderFont,.85);if(L.tableInsetRight)h.addSpacer(L.tableInsetRight);
  parent.addSpacer(3);
  for(const x of rows){
    const fav=hasFav&&teamMatches(x,s),r=parent.addStack();r.layoutHorizontally();r.centerAlignContent();if(L.tableInsetLeft)r.addSpacer(L.tableInsetLeft);await addTeamTableCell(r,x,grid.teamWidth,s,p,fav,L);r.addSpacer();const rs=r.addStack();rs.layoutHorizontally();rs.size=new Size(grid.statsWidth,0);for(let i=0;i<statCols.length;i++){const key=statCols[i][0],color=fav?p.accent:p.muted;lineCell(rs,standingValue(x,key),grid.widths[i],color,L.tableStatAlign,fav||key==="points",L.tableStatFont,.78)}if(L.tableInsetRight)r.addSpacer(L.tableInsetRight);if(L.tableRowSpacing)parent.addSpacer(L.tableRowSpacing)
  }
}'''
s, n = re.subn(r'async function table\(parent,s,d,p\)\{[\s\S]*?\n\}(?=\nfunction autoRefreshMinutes)', table_new, s, count=1)
assert n == 1, 'table replacement failed'

widget_new = r'''async function widget(s,family){const d=await data(s),p=pal(s),L=familyLayout(s,family),w=new ListWidget();w.backgroundColor=p.bg;const sidePad=Math.max(0,L.sidePadding-(s.compact?2:0)),verticalPad=Math.max(4,L.verticalPadding-(s.compact?2:0));w.setPadding(verticalPad,sidePad,verticalPad,sidePad);w.refreshAfterDate=new Date(Date.now()+autoRefreshMinutes(s,d)*60000);const h=w.addStack();h.layoutHorizontally();h.centerAlignContent();txt(h,sport(s).icon,14,p.text,true);h.addSpacer(5);txt(h,`${league(s).flag||""} ${leagueName(s)}`.trim(),family==="small"?10:12,p.text,true);h.addSpacer();txt(h,d.source==="cache"?tx(s,"cache"):d.source==="error"?tx(s,"error"):d.live.length?tx(s,"liveNow"):wh(s,"currentData"),8,d.live.length?p.live:d.source==="error"?p.live:p.accent,true);w.addSpacer(L.sectionSpacing);if(!d.current){const b=w.addStack();b.layoutVertically();b.backgroundColor=p.panel;b.cornerRadius=14;b.setPadding(12,12,12,12);txt(b,tx(s,"noData"),11,p.text,true);if(family==="large"&&s.showTable&&d.table.length){w.addSpacer(L.sectionSpacing);await table(w,s,d,p)}Script.setWidget(w);return w}await matchCard(w,d.current,s,p,family);if(s.showForm&&s.teamId){w.addSpacer(Math.max(3,L.sectionSpacing-2));form(w,s,d,p)}if(family==="small"){Script.setWidget(w);return w}const upcoming=s.showNext?d.next.filter(x=>x.id!==d.current.id).slice(0,family==="large"&&s.showTable?Math.min(s.maxMatches,2):family==="large"?s.maxMatches:2):[];if(upcoming.length){w.addSpacer(L.sectionSpacing);title(w,tx(s,"nextTitle"),p);w.addSpacer(Math.max(2,L.sectionSpacing-4));for(const e of upcoming){await line(w,e,s,p,family);if(family==="large")w.addSpacer(2)}}if(family==="large"&&s.showLast&&d.done.length){w.addSpacer(L.sectionSpacing);title(w,tx(s,"lastTitle"),p);w.addSpacer(Math.max(2,L.sectionSpacing-4));for(const e of d.done.filter(x=>x.id!==d.current.id).slice(0,s.showTable?Math.min(s.maxMatches,3):s.maxMatches)){await line(w,e,s,p,family);w.addSpacer(2)}}if(family==="large"&&s.showTable&&d.table.length){w.addSpacer(L.sectionSpacing);await table(w,s,d,p)}Script.setWidget(w);return w}'''
s, n = re.subn(r'async function widget\(s,family\)\{[^\n]*\}', widget_new, s, count=1)
assert n == 1, 'widget replacement failed'

# HTML helpers for per-size layout controls.
helper_anchor = 'function colorField(id,label,value){return `<div class="field"><label for="${id}">${esc(label)}</label><div class="colorRow"><input id="${id}" type="color" value="${esc(value)}"><code>${esc(value)}</code></div></div>`}\n'
assert helper_anchor in s
layout_helpers = r'''function selectField(id,label,value,options,attrs="",detail=""){return `<div class="field"><label for="${id}">${esc(label)}</label>${detail?`<div class="rowDetail" style="margin:-2px 0 9px">${esc(detail)}</div>`:""}<select id="${id}" ${attrs}>${options.map(([v,n])=>`<option value="${esc(v)}" ${v===value?"selected":""}>${esc(n)}</option>`).join("")}</select></div>`}
function layoutNumberField(s,fam,key,label){const lim=LAYOUT_LIMITS[fam][key],step=/Font/.test(key)?"0.5":"1",attrs=`min="${lim[0]}" max="${lim[1]}" step="${step}" data-layout-family="${fam}" data-layout-key="${key}"`;return field(`layout_${fam}_${key}`,label,s.layout[fam][key],"number",attrs)}
function layoutSelectField(s,fam,key,label,options){return selectField(`layout_${fam}_${key}`,label,s.layout[fam][key],options,`data-layout-family="${fam}" data-layout-key="${key}"`)}
function layoutFields(s,fam){const Y=LAYOUT_TEXT[s.language||"en"]||LAYOUT_TEXT.en,L=s.layout[fam],align=[["edges",Y.edges],["center",Y.center]],textAlign=[["left",Y.left],["center",Y.center],["right",Y.right]];let out=`<div class="sectionTitle">${esc(Y.general)}</div><div class="card">${layoutNumberField(s,fam,"sidePadding",Y.sidePadding)}${layoutNumberField(s,fam,"verticalPadding",Y.verticalPadding)}${layoutNumberField(s,fam,"sectionSpacing",Y.sectionSpacing)}</div><div class="sectionTitle">${esc(Y.match)}</div><div class="card">${layoutNumberField(s,fam,"cardPaddingX",Y.cardPaddingX)}${layoutNumberField(s,fam,"cardPaddingY",Y.cardPaddingY)}${layoutNumberField(s,fam,"teamWidth",Y.teamWidth)}${layoutNumberField(s,fam,"scoreWidth",Y.scoreWidth)}${layoutNumberField(s,fam,"teamFont",Y.teamFont)}${layoutNumberField(s,fam,"scoreFont",Y.scoreFont)}${layoutNumberField(s,fam,"logoSize",Y.logoSize)}${layoutNumberField(s,fam,"logoGap",Y.logoGap)}${layoutSelectField(s,fam,"teamAlign",Y.teamAlign,align)}</div>`;if(fam!=="small")out+=`<div class="sectionTitle">${esc(Y.lists)}</div><div class="card">${layoutNumberField(s,fam,"listDateWidth",Y.listDateWidth)}${layoutNumberField(s,fam,"listTeamWidth",Y.listTeamWidth)}${layoutNumberField(s,fam,"listScoreWidth",Y.listScoreWidth)}${layoutNumberField(s,fam,"listFont",Y.listFont)}</div>`;if(fam==="large")out+=`<div class="sectionTitle">${esc(Y.table)}</div><div class="info">${esc(Y.tableHelp)}</div><div class="card">${layoutNumberField(s,fam,"tableWidth",Y.tableWidth)}${layoutNumberField(s,fam,"tableInsetLeft",Y.tableInsetLeft)}${layoutNumberField(s,fam,"tableInsetRight",Y.tableInsetRight)}${layoutNumberField(s,fam,"tableTeamWidth",Y.tableTeamWidth)}${layoutNumberField(s,fam,"tableWideWidth",Y.tableWideWidth)}${layoutNumberField(s,fam,"tableNarrowWidth",Y.tableNarrowWidth)}${layoutNumberField(s,fam,"tableTeamFont",Y.tableTeamFont)}${layoutNumberField(s,fam,"tableStatFont",Y.tableStatFont)}${layoutNumberField(s,fam,"tableHeaderFont",Y.tableHeaderFont)}${layoutNumberField(s,fam,"tableRowSpacing",Y.tableRowSpacing)}${layoutSelectField(s,fam,"tableTeamAlign",Y.tableTeamAlign,textAlign)}${layoutSelectField(s,fam,"tableStatAlign",Y.tableStatAlign,textAlign)}${layoutSelectField(s,fam,"tableHeaderAlign",Y.tableHeaderAlign,textAlign)}</div>`;return out}
'''
s = s.replace(helper_anchor, helper_anchor + layout_helpers, 1)

old_html_prefix = 'function html(s){const L=T[s.language||"en"],H=WIDGET_HELP[s.language||"en"]||WIDGET_HELP.en,sp=sport(s),'
new_html_prefix = 'function html(s){const L=T[s.language||"en"],H=WIDGET_HELP[s.language||"en"]||WIDGET_HELP.en,Y=LAYOUT_TEXT[s.language||"en"]||LAYOUT_TEXT.en,sp=sport(s),'
assert old_html_prefix in s
s = s.replace(old_html_prefix, new_html_prefix, 1)

appearance_marker = '<div class="sectionTitle">${esc(L.appearance)}</div><div class="card">${nav("appearance","🎨",L.appearance,s.theme==="custom"?H.customTheme:s.theme)}</div>'
assert appearance_marker in s
s = s.replace(appearance_marker, '<div class="sectionTitle">${esc(Y.layout)}</div><div class="card">${nav("layout","📐",Y.layout,Y.layoutSub)}</div>' + appearance_marker, 1)

appearance_screen = '<div class="screen" id="appearance">'
assert appearance_screen in s
layout_screens = r'''<div class="screen" id="layout">${back}<div class="screenTitle">📐 ${esc(Y.layout)}</div><div class="screenSub">${esc(Y.layoutSub)}</div><div class="card">${nav("layoutSmall","▣",Y.small,`${s.layout.small.teamFont}px · ${s.layout.small.teamWidth}pt`)}${nav("layoutMedium","▰",Y.medium,`${s.layout.medium.teamFont}px · ${s.layout.medium.teamWidth}pt`)}${nav("layoutLarge","▦",Y.large,`${s.layout.large.tableTeamWidth}pt · 7 slots`)}</div></div>
<div class="screen" id="layoutSmall"><div class="topbar"><button class="back" onclick="showScreen('layout')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">▣ ${esc(Y.small)} · ${esc(Y.layout)}</div><div class="screenSub">${esc(Y.layoutHelp)}</div>${layoutFields(s,"small")}<div class="actionGrid"><button class="actionBtn" onclick="preview('small')">👁 ${esc(Y.preview)}</button><button class="actionBtn secondary" onclick="resetLayout('small')">↺ ${esc(Y.reset)}</button></div></div>
<div class="screen" id="layoutMedium"><div class="topbar"><button class="back" onclick="showScreen('layout')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">▰ ${esc(Y.medium)} · ${esc(Y.layout)}</div><div class="screenSub">${esc(Y.layoutHelp)}</div>${layoutFields(s,"medium")}<div class="actionGrid"><button class="actionBtn" onclick="preview('medium')">👁 ${esc(Y.preview)}</button><button class="actionBtn secondary" onclick="resetLayout('medium')">↺ ${esc(Y.reset)}</button></div></div>
<div class="screen" id="layoutLarge"><div class="topbar"><button class="back" onclick="showScreen('layout')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">▦ ${esc(Y.large)} · ${esc(Y.layout)}</div><div class="screenSub">${esc(Y.layoutHelp)}</div>${layoutFields(s,"large")}<div class="actionGrid"><button class="actionBtn" onclick="preview('large')">👁 ${esc(Y.preview)}</button><button class="actionBtn secondary" onclick="resetLayout('large')">↺ ${esc(Y.reset)}</button></div></div>
'''
s = s.replace(appearance_screen, layout_screens + appearance_screen, 1)

collect_new = r'''function collect(){const z=JSON.parse(JSON.stringify(state));z.layout=z.layout||{};for(const fam of["small","medium","large"])z.layout[fam]=z.layout[fam]||{};z.sportId=document.getElementById('sportId')?.value||z.sportId;z.leagueId=document.getElementById('leagueId')?.value||z.leagueId;const t=document.getElementById('teamId');if(t){z.teamId=t.value;z.teamName=t.value?(t.options[t.selectedIndex]?.text||''):''}['showLive','showLast','showNext','showTable','showForm','showLogos','compact'].forEach(k=>{const e=document.getElementById(k);if(e)z[k]=e.checked});for(const k of['maxMatches','refreshMinutes']){const e=document.getElementById(k);if(e)z[k]=Number(e.value)}for(const k of['theme','accent','background','panelColor','textColor','mutedColor','liveColor','winColor','apiEspnBase','apiFotmobBase','apiOneFootballFeedBase','apiOneFootballScoresBase','apiSofaBase','apiSportsApiBase','sportsApiKey']){const e=document.getElementById(k);if(e)z[k]=e.value}document.querySelectorAll('[data-layout-family]').forEach(e=>{const fam=e.dataset.layoutFamily,key=e.dataset.layoutKey;if(!fam||!key)return;z.layout[fam][key]=e.type==='number'?Number(e.value):e.value});return z}'''
s, n = re.subn(r'function collect\(\)\{const z=\{\.\.\.state\};[\s\S]*?return z\}', collect_new, s, count=1)
assert n == 1, 'collect replacement failed'

reset_part = "function resetPart(part){emit('reset',{part,settings:collect()})}"
assert reset_part in s
s = s.replace(reset_part, reset_part + "function resetLayout(family){emit('reset',{part:'layout:'+family,settings:collect()})}", 1)

reset_native = r'''}else if(m.action==="reset"){
        cur=merge(m.settings||cur);const l=cur.language||lang();
        if(m.part==="appearance")cur=Object.assign({},cur,{theme:DEFAULTS.theme,accent:DEFAULTS.accent,background:DEFAULTS.background,panelColor:DEFAULTS.panelColor,textColor:DEFAULTS.textColor,mutedColor:DEFAULTS.mutedColor,liveColor:DEFAULTS.liveColor,winColor:DEFAULTS.winColor,compact:DEFAULTS.compact,refreshMinutes:DEFAULTS.refreshMinutes});
        else if(m.part==="sport")cur=Object.assign({},cur,{sportId:DEFAULTS.sportId,leagueId:DEFAULTS.leagueId,teamId:"",teamName:""});
        else if(String(m.part||"").startsWith("layout:")){const fam=String(m.part).split(":")[1];if(LAYOUT_DEFAULTS[fam])cur.layout[fam]=clone(LAYOUT_DEFAULTS[fam])}
        else{cur=clone(DEFAULTS);cur.language=l}
        cur=merge(cur);saveSettings(cur);await send(web,{action:"status",ok:true,text:tx(cur,"resetDone")});await send(web,{action:"replace",settings:cur})
      ''']
s, n = re.subn(r'}else if\(m\.action==="reset"\)\{[\s\S]*?(?=}else if\(m\.action==="update"\))', reset_native[0], s, count=1)
assert n == 1, 'native reset replacement failed'

# README: document the new independent profiles.
readme = Path('apps/Sports-Info/README.md')
r = readme.read_text(encoding='utf-8')
if '## 📐 Layout podle velikosti' not in r:
    marker = '\n## Sporty\n'
    block = '\n## 📐 Layout podle velikosti\n\nVerze 2.5.15 přidává samostatné nastavení **Small / Medium / Large**. Každá velikost má vlastní odsazení, velikosti log a textů, šířky týmů a skóre. Large navíc používá bezpečný rastr až 7 statistických pozic s širšími pozicemi 1–4 a samostatným nastavením tabulky.\n'
    if marker in r:r = r.replace(marker, block + marker, 1)
    else:r += block
    readme.write_text(r, encoding='utf-8')

# Update persistent release guards to the 2.5.15 architecture.
wf = Path('.github/workflows/build-sports-info-package.yml')
w = wf.read_text(encoding='utf-8')
old = '''          assert 'const widths=family==="small"?[62,14,62]' in src, 'Small safe-width layout missing'\n          assert 'football:[["rank","#",14],["team","TÝM",116]' in src, 'football table width profile changed unexpectedly'\n'''
new = '''          assert 'const LAYOUT_DEFAULTS={' in src, 'per-size layout defaults missing'\n          assert 'small:{sidePadding:' in src and 'medium:{sidePadding:' in src and 'large:{sidePadding:' in src, 'Small/Medium/Large layout profiles missing'\n          assert 'function tableSlotWidths(s,rows,statCols)' in src, '7-slot standings layout missing'\n          assert 'football:[["team","TÝM"],["played","Z"]' in src, 'football standings profile missing'\n          assert 'data-layout-family' in src, 'layout settings UI is not wired to saved settings'\n'''
assert old in w, 'old build regression guards not found'
w = w.replace(old, new, 1)
wf.write_text(w, encoding='utf-8')

p.write_text(s, encoding='utf-8')
print('Patched Sports Info to 2.5.15 with independent Small/Medium/Large layouts')
