// Offline regression checks. Mocks validate geometry/contracts, not iOS rendering.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const src = fs.readFileSync('apps/Sports-Info/Sports Info.js', 'utf8');
new (Object.getPrototypeOf(async function(){}).constructor)(src);
const fm = {documentsDirectory:()=>'/tmp',cacheDirectory:()=>'/tmp',joinPath:(a,b)=>a+'/'+b,fileExists:()=>false};
class Stack {
  constructor(){this.children=[];}
  addStack(){const c=new Stack();this.children.push(c);return c;}
  addSpacer(length){this.children.push({spacer:true,length});}
  addText(value){const t={text:value};this.children.push(t);return t;}
  addImage(){const i={image:true};this.children.push(i);return i;}
  layoutHorizontally(){} layoutVertically(){} centerAlignContent(){}
  setPadding(...values){this.padding=values;}
}
let screen={width:430,height:932};
const fonts=Object.fromEntries(['systemFont','boldSystemFont','boldMonospacedSystemFont','regularMonospacedSystemFont'].map(k=>[k,size=>({kind:k,size})]));
const ctx={console,FileManager:{local:()=>fm},Device:{locale:()=> 'cs-CZ',screenSize:()=>screen},Font:fonts,
  Size:class{constructor(width,height){this.width=width;this.height=height;}},config:{runsInWidget:false},args:{queryParameters:{}}};
vm.createContext(ctx);
vm.runInContext(src.slice(0,src.indexOf('let SETTINGS=await firstLanguage(loadSettings());'))+
  '\nglobalThis.api={merge,DEFAULTS,TABLE_PROFILES,tableAvailableWidth,tableSlotLayout,tableStatWidth,standingValue,tableStatCell,table,html};',ctx);
const a=ctx.api;
const rows=[
  {name:'Slavia Prague',played:8,wins:6,draws:2,losses:0,score:'20:2',diff:18,points:20,pct:'0.000',gb:'12.5',otWins:2,otLosses:1},
  {name:'Philadelphia 76ers',played:82,wins:60,draws:0,losses:22,score:'12345:12345',diff:-123,points:123,pct:'.732',gb:0,otWins:12,otLosses:14},
  {name:'Washington Wizards',played:0,wins:0,losses:0,pct:0,score:'0:0'}
];
let cases=0;
for(const [width,height] of [[320,568],[375,667],[390,844],[393,852],[414,736],[414,896],[428,926],[430,932],[402,874],[440,956]]){
  screen={width,height};
  for(const sportId of Object.keys(a.TABLE_PROFILES))for(const compact of [true,false])for(const font of [8,10,14])for(const align of ['left','center','right']){
    const s=a.merge({...a.DEFAULTS,sportId,compact,layout:{large:{tableFont:font,tableAlign:align}}});
    const snapshot=JSON.stringify(s),cols=a.TABLE_PROFILES[sportId],g=a.tableSlotLayout(s,cols,rows);
    assert.equal(g.statCols.length,cols.length-1);
    assert.equal(g.teamCol[2]+4+g.statsWidth,a.tableAvailableWidth(s));
    assert.ok(g.teamCol[2]>=80);
    for(const [key,label,w] of g.statCols){
      assert.ok(w>=a.tableStatWidth(label,g.headerFont));
      for(const row of rows){
        const need=a.tableStatWidth(a.standingValue(row,key),g.font);
        // Extreme 11-character scores on SE-size screens may use the cell's native scaling.
        assert.ok(w>=need || (w-2)>=(need-8)*.5,`${sportId}/${width}/${key}`);
      }
    }
    assert.equal(JSON.stringify(s),snapshot,'AUTO must not overwrite manual layout');
    cases++;
  }
}
screen={width:430,height:932};
assert.equal(a.tableAvailableWidth({compact:false}),340);
assert.equal(a.tableAvailableWidth({compact:true}),344);
for(const sportId of ['football','basketball']){
  const s=a.merge({...a.DEFAULTS,sportId}),fixture=[{name:'Slovan Liberec',played:8,wins:6,draws:1,losses:1,score:'20:2',diff:18,points:20,pct:'0.000'}];
  const g=a.tableSlotLayout(s,a.TABLE_PROFILES[sportId],fixture);
  for(const [key,,w] of g.statCols)assert.ok(w>=a.tableStatWidth(a.standingValue(fixture[0],key),g.font),'screenshot values fit without shrinking');
}
screen={width:932,height:430};
assert.equal(a.tableAvailableWidth({compact:false}),340,'orientation invariant');
for(const align of ['left','center','right']){
  const parent=new Stack();a.tableStatCell(parent,'123:456',80,'white',align,true,10);
  const cell=parent.children[0];assert.equal(cell.size.width,80);assert.equal(cell.spacing,0);
  assert.equal(cell.padding.join(','),'0,0,0,0');
  const t=cell.children.find(x=>x.text);assert.equal(t.text,'123:456');assert.equal(t.font.kind,'boldMonospacedSystemFont');
  assert.ok(t.minimumScaleFactor<1);
  assert.equal(cell.children[0].spacer===true,align!=='left');
  assert.equal(cell.children.at(-1).spacer===true,align!=='right');
}
const html=a.html(a.merge({...a.DEFAULTS,language:'cs'}));
const ui=html.match(/<script>([\s\S]*?)<\/script>/)[1];new vm.Script(ui);
assert.ok(ui.includes("document.querySelectorAll('#layoutLargeTable input[id$=Width]')"));
assert.ok(!ui.includes("document.querySelectorAll('#layoutLargeTable input[type=number]')"));
for(const alignment of ['left','center','right'])assert.ok(html.includes(`option value="${alignment}"`));
fs.writeFileSync('/tmp/sports-settings.html',html);
fs.writeFileSync('/tmp/sports-settings-ui.js',ui);
(async()=>{
  for(const sportId of Object.keys(a.TABLE_PROFILES)){
    const s=a.merge({...a.DEFAULTS,sportId,showLogos:false,teamId:'',teamName:''});
    const p={text:'white',muted:'gray',accent:'blue'},root=new Stack();
    await a.table(root,s,{table:rows,current:null,form:[],next:[],done:[]},p);
    // Header and all data rows have a team slot, explicit 4pt gap, then statistics.
    const rendered=root.children.filter(x=>x.children?.length===3&&x.children[1].length===4);
    assert.equal(rendered.length,rows.length+1);
    const widths=rendered.map(r=>r.children[2].children.map(c=>c.size.width));
    for(const w of widths)assert.deepEqual(w,widths[0]);
    for(const r of rendered){
      assert.equal(r.children[0].size.width+4+r.children[2].size.width,a.tableAvailableWidth(s));
      assert.equal(r.children[2].children.length,a.TABLE_PROFILES[sportId].length-1);
    }
  }
  const pkg=JSON.parse(fs.readFileSync('apps/Sports-Info/Sports Info.scriptable','utf8'));
  assert.equal(pkg.script,src);assert.equal(pkg.name,'Sports Info');assert.equal(pkg.always_run_in_app,false);
  console.log(`PASS: ${cases} AUTO combinations, 5 native table-tree fixtures, alignments, UI syntax, package parity. Native iPhone visual check still required.`);
})().catch(e=>{console.error(e);process.exitCode=1;});
