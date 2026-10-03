// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: house-signal;
// ============================================================
// Homebridge Status v0.1.0
// CaseyCZ Scriptable Apps
// Homebridge status widget with LAN -> VPN fallback.
// Homebridge API logic based on homebridgeStatusWidget by lwitzani.
// ============================================================

const APP_NAME = "Homebridge Status";
const APP_VERSION = "0.1.0";
const SETTINGS_FILE = "HomebridgeStatus_settings.json";
const STATE_FILE = "HomebridgeStatus_state.json";
const PASSWORD_KEY = "HomebridgeStatus_Password";
const UPDATE_SOURCE_URL = "https://raw.githubusercontent.com/CaseyCZ/Scriptable/Master/apps/Homebridge-Status/Homebridge%20Status.js";
const UPDATE_MIN_BYTES = 18000;

const fm = FileManager.local();
const settingsPath = fm.joinPath(fm.documentsDirectory(), SETTINGS_FILE);
const statePath = fm.joinPath(fm.documentsDirectory(), STATE_FILE);

const DEFAULTS = {
  primaryUrl: "",
  fallbackUrl: "",
  username: "",
  requestTimeout: 3,
  allowInsecure: false,
  refreshMinutes: 15,
  widgetTitle: "Homebridge",
  theme: "system",
  useCustomColors: false,
  backgroundColor: "#0B1020",
  cardColor: "#141B2D",
  textColor: "#F8FAFC",
  mutedColor: "#94A3B8",
  accentColor: "#0A84FF",
  okColor: "#34C759",
  warningColor: "#FF9F0A",
  failColor: "#FF453A",
  showGraphs: true,
  showTemperature: true,
  showUptime: true,
  showUpdated: true,
  showRoute: true,
  notificationEnabled: true,
  notificationIntervalHours: 24,
  recoveryNotifications: false,
  ignoredUpdates: "",
  legacyChecked: false
};

function clone(v){return JSON.parse(JSON.stringify(v))}
function clamp(v,min,max){return Math.max(min,Math.min(max,v))}
function merge(raw){
  const s=Object.assign(clone(DEFAULTS),raw||{});
  s.primaryUrl=normalizeBaseUrl(s.primaryUrl);
  s.fallbackUrl=normalizeBaseUrl(s.fallbackUrl);
  s.username=String(s.username||"").trim();
  s.requestTimeout=clamp(Number(s.requestTimeout)||3,1,30);
  s.refreshMinutes=clamp(Number(s.refreshMinutes)||15,5,180);
  s.widgetTitle=String(s.widgetTitle||"Homebridge").slice(0,40);
  s.theme=["system","dark","black","custom"].includes(s.theme)?s.theme:"system";
  s.notificationIntervalHours=clamp(Number(s.notificationIntervalHours)||24,0,720);
  for(const k of ["allowInsecure","useCustomColors","showGraphs","showTemperature","showUptime","showUpdated","showRoute","notificationEnabled","recoveryNotifications","legacyChecked"]){
    if(typeof s[k]!=="boolean")s[k]=DEFAULTS[k];
  }
  for(const k of ["backgroundColor","cardColor","textColor","mutedColor","accentColor","okColor","warningColor","failColor"]){
    if(!/^#[0-9a-fA-F]{6}$/.test(String(s[k]||"")))s[k]=DEFAULTS[k];
  }
  s.ignoredUpdates=String(s.ignoredUpdates||"");
  return s
}
function normalizeBaseUrl(v){return String(v||"").trim().replace(/\/+$/,"")}
function loadSettings(){try{if(fm.fileExists(settingsPath))return merge(JSON.parse(fm.readString(settingsPath)))}catch(e){console.log(e)}return clone(DEFAULTS)}
function saveSettings(s){try{fm.writeString(settingsPath,JSON.stringify(merge(s),null,2))}catch(e){console.log(e)}}
function loadState(){try{if(fm.fileExists(statePath))return JSON.parse(fm.readString(statePath))}catch(_){}return{notifications:{},lastRoute:null,lastUpdated:null}}
function saveState(s){try{fm.writeString(statePath,JSON.stringify(s,null,2))}catch(_){}}
function ignoredSet(s){return new Set(String(s.ignoredUpdates||"").split(",").map(x=>x.trim()).filter(Boolean))}
function passwordStored(){try{return Keychain.contains(PASSWORD_KEY)}catch(_){return false}}
function getPassword(){try{return Keychain.contains(PASSWORD_KEY)?Keychain.get(PASSWORD_KEY):""}catch(_){return""}}
function setPassword(v){try{if(String(v||"").length)Keychain.set(PASSWORD_KEY,String(v));return true}catch(_){return false}}
function removePassword(){try{if(Keychain.contains(PASSWORD_KEY))Keychain.remove(PASSWORD_KEY)}catch(_){}}

async function migrateLegacy(s){
  if(s.legacyChecked)return s;
  const managers=[FileManager.local(),FileManager.iCloud()];
  for(const m of managers){
    try{
      const dir=m.joinPath(m.documentsDirectory(),"homebridgeStatus");
      const p=m.joinPath(dir,"black.json");
      if(!m.fileExists(p))continue;
      if(m.isFileDownloaded&&!(await m.isFileDownloaded(p)))await m.downloadFileFromiCloud(p);
      const old=JSON.parse(m.readString(p));
      if(!s.primaryUrl&&old.hbServiceMachineBaseUrl&&!String(old.hbServiceMachineBaseUrl).includes("enter the ip"))s.primaryUrl=normalizeBaseUrl(old.hbServiceMachineBaseUrl);
      if(!s.username&&old.userName&&!String(old.userName).includes("enter username"))s.username=String(old.userName);
      if(!passwordStored()&&old.password&&!String(old.password).includes("enter password"))setPassword(old.password);
      if(typeof old.notificationEnabled==="boolean")s.notificationEnabled=old.notificationEnabled;
      if(Number.isFinite(Number(old.notificationIntervalInDays)))s.notificationIntervalHours=Math.max(0,Number(old.notificationIntervalInDays)*24);
      if(typeof old.disableStateBackToNormalNotifications==="boolean")s.recoveryNotifications=!old.disableStateBackToNormalNotifications;
      if(Number(old.requestTimeoutInterval)>0)s.requestTimeout=Number(old.requestTimeoutInterval);
      if(Array.isArray(old.pluginsOrSwUpdatesToIgnore))s.ignoredUpdates=old.pluginsOrSwUpdatesToIgnore.join(", ");
      break;
    }catch(e){console.log("Legacy migration: "+e)}
  }
  s.legacyChecked=true;
  s=merge(s);saveSettings(s);return s
}

function requestFor(url,s){const r=new Request(url);r.timeoutInterval=s.requestTimeout;if(s.allowInsecure)r.allowInsecureRequest=true;return r}
async function authenticate(base,s){
  let req=requestFor(base+"/api/auth/noauth",s);
  req.method="POST";req.headers={"accept":"*/*","Content-Type":"application/json"};req.body="{}";
  let data=await req.loadJSON();
  if(data&&data.access_token)return data.access_token;
  req=requestFor(base+"/api/auth/login",s);
  req.method="POST";req.headers={"accept":"*/*","Content-Type":"application/json"};
  req.body=JSON.stringify({username:s.username,password:getPassword(),otp:"string"});
  data=await req.loadJSON();
  if(!data||!data.access_token)throw new Error("Authentication failed");
  return data.access_token
}
async function apiJson(base,token,path,s){const r=requestFor(base+path,s);r.headers={"accept":"*/*","Content-Type":"application/json","Authorization":"Bearer "+token};return await r.loadJSON()}
async function optionalApi(base,token,path,s){try{return await apiJson(base,token,path,s)}catch(e){console.log(path+": "+e);return undefined}}
function candidates(s){const out=[];if(s.primaryUrl)out.push({base:s.primaryUrl,route:"LAN"});if(s.fallbackUrl&&s.fallbackUrl!==s.primaryUrl)out.push({base:s.fallbackUrl,route:"VPN"});return out}

async function snapshotFrom(base,route,s){
  const token=await authenticate(base,s);
  const overall=await apiJson(base,token,"/api/status/homebridge",s);
  const [cpu,ram,uptime,plugins,hbVersion,nodeVersion]=await Promise.all([
    optionalApi(base,token,"/api/status/cpu",s),
    optionalApi(base,token,"/api/status/ram",s),
    optionalApi(base,token,"/api/status/uptime",s),
    optionalApi(base,token,"/api/plugins",s),
    optionalApi(base,token,"/api/status/homebridge-version",s),
    optionalApi(base,token,"/api/status/nodejs",s)
  ]);
  const ignored=ignoredSet(s);
  const running=overall&&(["ok","up"].includes(String(overall.status||"").toLowerCase()));
  const hbUtd=ignored.has("HOMEBRIDGE_UTD")?true:(hbVersion? !hbVersion.updateAvailable:undefined);
  let pluginsUtd=undefined;
  if(Array.isArray(plugins))pluginsUtd=!plugins.some(p=>!ignored.has(p.name)&&p.updateAvailable);
  const nodeUtd=ignored.has("NODEJS_UTD")?true:(nodeVersion? !nodeVersion.updateAvailable:undefined);
  return {connected:true,base,route,token,running,hbUtd,pluginsUtd,nodeUtd,cpu,ram,uptime,plugins,hbVersion,nodeVersion,updatedAt:Date.now()}
}
async function getSnapshot(s){
  if(!s.primaryUrl&&!s.fallbackUrl)return{connected:false,setup:true,updatedAt:Date.now(),error:"Not configured"};
  let lastError="";
  for(const c of candidates(s)){
    try{return await snapshotFrom(c.base,c.route,s)}catch(e){lastError=String(e?.message||e);console.log(c.route+" connection failed: "+lastError)}
  }
  return{connected:false,updatedAt:Date.now(),error:lastError||"Homebridge unavailable"}
}

function cpuLoad(snap){const v=Number(snap?.cpu?.currentLoad);return Number.isFinite(v)?v:null}
function cpuTemp(snap){const v=Number(snap?.cpu?.cpuTemperature?.main);return Number.isFinite(v)&&v>=0?v:null}
function ramUsed(snap){const a=Number(snap?.ram?.mem?.available),t=Number(snap?.ram?.mem?.total);return Number.isFinite(a)&&Number.isFinite(t)&&t>0?100-(100*a/t):null}
function fmt(v,d=1){return Number.isFinite(Number(v))?Number(v).toFixed(d).replace(/\.0$/,""):"—"}
function formatSeconds(v){v=Number(v);if(!Number.isFinite(v))return"—";if(v>=864000)return fmt(v/86400,0)+"d";if(v>=86400)return fmt(v/86400,1)+"d";if(v>=3600)return fmt(v/3600,1)+"h";if(v>=60)return fmt(v/60,1)+"m";return fmt(v,0)+"s"}
function statusCount(snap){const values=[snap.running,snap.hbUtd,snap.pluginsUtd,snap.nodeUtd];return{bad:values.filter(v=>v===false).length,unknown:values.filter(v=>v===undefined).length}}

function colors(s){
  if(s.theme==="custom"||s.useCustomColors)return{bg:new Color(s.backgroundColor),card:new Color(s.cardColor),text:new Color(s.textColor),muted:new Color(s.mutedColor),accent:new Color(s.accentColor),ok:new Color(s.okColor),warn:new Color(s.warningColor),fail:new Color(s.failColor)};
  if(s.theme==="black")return{bg:new Color("000000"),card:new Color("111111"),text:new Color("FFFFFF"),muted:new Color("8E8E93"),accent:new Color("0A84FF"),ok:new Color("34C759"),warn:new Color("FF9F0A"),fail:new Color("FF453A")};
  if(s.theme==="dark")return{bg:new Color("0B1020"),card:new Color("141B2D"),text:new Color("F8FAFC"),muted:new Color("94A3B8"),accent:new Color("0A84FF"),ok:new Color("34C759"),warn:new Color("FF9F0A"),fail:new Color("FF453A")};
  return{bg:Color.dynamic(new Color("F5F7FB"),new Color("0B1020")),card:Color.dynamic(new Color("FFFFFF"),new Color("141B2D")),text:Color.dynamic(new Color("111827"),new Color("F8FAFC")),muted:Color.dynamic(new Color("6B7280"),new Color("94A3B8")),accent:new Color("0A84FF"),ok:new Color("34C759"),warn:new Color("FF9F0A"),fail:new Color("FF453A")}
}
function symImage(name,size,color){const sf=SFSymbol.named(name);sf.applyFont(Font.semiboldSystemFont(size));return{image:sf.image,size,color}}
function addSymbol(stack,name,size,color){const x=symImage(name,size,color),im=stack.addImage(x.image);im.imageSize=new Size(size,size);im.tintColor=color;return im}
function addText(stack,text,size,color,weight="regular"){const t=stack.addText(String(text));t.font=weight==="bold"?Font.boldSystemFont(size):weight==="semibold"?Font.semiboldSystemFont(size):Font.systemFont(size);t.textColor=color;t.lineLimit=1;return t}
function addHeader(w,s,c,snap,size=16){const h=w.addStack();h.centerAlignContent();addSymbol(h,"house.fill",size,c.accent);h.addSpacer(7);addText(h,s.widgetTitle||APP_NAME,size,c.text,"bold");h.addSpacer();if(snap.connected&&s.showRoute){const r=addText(h,snap.route,9,snap.route==="VPN"?c.warn:c.muted,"semibold");r.lineLimit=1}else if(!snap.connected)addSymbol(h,"exclamationmark.triangle.fill",size-1,c.fail)}
function statusMeta(value,c){if(value===true)return{icon:"checkmark.circle.fill",color:c.ok};if(value===false)return{icon:"exclamationmark.triangle.fill",color:c.warn};return{icon:"questionmark.circle.fill",color:c.muted}}
function addStatusRow(parent,label,value,c,font=11){const r=parent.addStack();r.centerAlignContent();const m=statusMeta(value,c);addSymbol(r,m.icon,font+1,m.color);r.addSpacer(5);addText(r,label,font,c.text,"semibold");return r}
function addStatusGrid(w,snap,c,font=11){const row=w.addStack();const left=row.addStack();left.layoutVertically();addStatusRow(left,"Running",snap.running,c,font);left.addSpacer(5);addStatusRow(left,"Plugins",snap.pluginsUtd,c,font);row.addSpacer();const right=row.addStack();right.layoutVertically();addStatusRow(right,"Homebridge",snap.hbUtd,c,font);right.addSpacer(5);addStatusRow(right,"Node.js",snap.nodeUtd,c,font)}

class LineChart{
  constructor(width,height,values){this.ctx=new DrawContext();this.ctx.size=new Size(width,height);this.ctx.opaque=false;this.values=(Array.isArray(values)?values:[]).map(Number).filter(Number.isFinite)}
  path(){const p=new Path();if(this.values.length<2){p.move(new Point(0,this.ctx.size.height/2));p.addLine(new Point(this.ctx.size.width,this.ctx.size.height/2));return p}const max=Math.max(...this.values),min=Math.min(...this.values),diff=(max-min)||1,step=this.ctx.size.width/(this.values.length-1);const pts=this.values.map((v,i)=>new Point(step*i,this.ctx.size.height-((v-min)/diff*this.ctx.size.height)));p.move(pts[0]);for(let i=0;i<pts.length-1;i++){const a=pts[i],b=pts[i+1],mid=new Point((a.x+b.x)/2,(a.y+b.y)/2);p.addQuadCurve(mid,new Point((a.x+mid.x)/2,a.y));p.addQuadCurve(b,new Point((b.x+mid.x)/2,b.y))}return p}
  image(color){const p=this.path();this.ctx.addPath(p);this.ctx.setStrokeColor(color);this.ctx.setLineWidth(5);this.ctx.strokePath();return this.ctx.getImage()}
}
function addMetricCard(parent,title,value,unit,history,c,showGraph=true,tempText=""){const card=parent.addStack();card.layoutVertically();card.backgroundColor=c.card;card.cornerRadius=12;card.setPadding(9,10,8,10);addText(card,title,9,c.muted,"semibold");card.addSpacer(3);const v=card.addStack();v.centerAlignContent();addText(v,value,18,c.text,"bold");v.addSpacer(3);addText(v,unit,9,c.muted);if(tempText){v.addSpacer();addText(v,tempText,9,c.muted,"semibold")}if(showGraph&&Array.isArray(history)&&history.length>1){card.addSpacer(6);const img=new LineChart(320,60,history).image(c.accent);const ih=card.addImage(img);ih.imageSize=new Size(120,22)}return card}
function configureWidget(w,s,c){w.backgroundColor=c.bg;w.refreshAfterDate=new Date(Date.now()+s.refreshMinutes*60000);try{w.url=URLScheme.forRunningScript()}catch(_){}}
function addUnavailable(w,s,c,snap){w.addSpacer();const st=w.addStack();st.layoutVertically();st.addSpacer();const icon=st.addStack();icon.addSpacer();addSymbol(icon,snap.setup?"gearshape.fill":"wifi.exclamationmark",26,snap.setup?c.accent:c.fail);icon.addSpacer();st.addSpacer(8);const t=addText(st,snap.setup?"Otevři skript a nastav Homebridge":"Homebridge není dostupný",11,c.text,"semibold");t.centerAlignText();st.addSpacer()}

async function buildSmall(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(12,12,12,12);addHeader(w,s,c,snap,14);w.addSpacer(9);if(!snap.connected){addUnavailable(w,s,c,snap);return w}const count=statusCount(snap);const body=w.addStack();body.layoutVertically();body.addSpacer();const big=body.addText(count.bad?`⚠ ${count.bad}`:"✓");big.font=Font.boldSystemFont(27);big.textColor=count.bad?c.warn:c.ok;big.centerAlignText();body.addSpacer(5);const cpu=cpuLoad(snap),ram=ramUsed(snap);const sub=body.addText(`CPU ${fmt(cpu)}%  ·  RAM ${fmt(ram)}%`);sub.font=Font.semiboldSystemFont(10);sub.textColor=c.text;sub.centerAlignText();body.addSpacer();if(s.showUpdated){const df=new DateFormatter();df.useNoDateStyle();df.useShortTimeStyle();const f=w.addText(df.string(new Date(snap.updatedAt)));f.font=Font.systemFont(8);f.textColor=c.muted;f.centerAlignText()}return w}
async function buildMedium(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(13,13,11,13);addHeader(w,s,c,snap,16);w.addSpacer(9);if(!snap.connected){addUnavailable(w,s,c,snap);return w}addStatusGrid(w,snap,c,10);w.addSpacer(9);const metrics=w.addStack();const temp=cpuTemp(snap);addMetricCard(metrics,"CPU LOAD",fmt(cpuLoad(snap)),"%",snap.cpu?.cpuLoadHistory,c,s.showGraphs,s.showTemperature&&temp!==null?fmt(temp)+" °C":"");metrics.addSpacer(9);addMetricCard(metrics,"RAM USAGE",fmt(ramUsed(snap)),"%",snap.ram?.memoryUsageHistory,c,s.showGraphs);w.addSpacer();if(s.showUptime&&snap.uptime){const foot=w.addStack();addText(foot,"Pi "+formatSeconds(snap.uptime?.time?.uptime),9,c.muted,"semibold");foot.addSpacer();addText(foot,"UI "+formatSeconds(snap.uptime?.processUptime),9,c.muted,"semibold")}return w}
async function buildLarge(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(15,15,13,15);addHeader(w,s,c,snap,18);w.addSpacer(12);if(!snap.connected){addUnavailable(w,s,c,snap);return w}addStatusGrid(w,snap,c,12);w.addSpacer(12);const metrics=w.addStack();const temp=cpuTemp(snap);addMetricCard(metrics,"CPU LOAD",fmt(cpuLoad(snap)),"%",snap.cpu?.cpuLoadHistory,c,s.showGraphs,s.showTemperature&&temp!==null?fmt(temp)+" °C":"");metrics.addSpacer(10);addMetricCard(metrics,"RAM USAGE",fmt(ramUsed(snap)),"%",snap.ram?.memoryUsageHistory,c,s.showGraphs);w.addSpacer(12);const updates=(Array.isArray(snap.plugins)?snap.plugins.filter(p=>p.updateAvailable&&!ignoredSet(s).has(p.name)):[]);const section=w.addStack();section.layoutVertically();addText(section,"DETAILS",9,c.muted,"semibold");section.addSpacer(6);const hb=snap.hbVersion,nd=snap.nodeVersion;const rows=[];if(hb)rows.push(["Homebridge",hb.installedVersion||hb.currentVersion||"—",hb.latestVersion||"—",snap.hbUtd]);if(nd)rows.push(["Node.js",nd.currentVersion||nd.installedVersion||"—",nd.latestVersion||"—",snap.nodeUtd]);for(const p of updates.slice(0,3))rows.push([p.name,p.installedVersion||"—",p.latestVersion||"—",false]);if(!rows.length)rows.push(["Updates","Everything is up to date","",true]);for(const [name,current,latest,ok] of rows){const r=section.addStack();r.centerAlignContent();const m=statusMeta(ok,c);addSymbol(r,m.icon,11,m.color);r.addSpacer(6);addText(r,name,11,c.text,"semibold");r.addSpacer();addText(r,latest?`${current} → ${latest}`:current,9,ok===false?c.warn:c.muted);section.addSpacer(5)}w.addSpacer();const foot=w.addStack();if(s.showUptime&&snap.uptime)addText(foot,"Pi "+formatSeconds(snap.uptime?.time?.uptime)+" · UI "+formatSeconds(snap.uptime?.processUptime),9,c.muted,"semibold");foot.addSpacer();if(s.showUpdated){const df=new DateFormatter();df.useNoDateStyle();df.useShortTimeStyle();addText(foot,df.string(new Date(snap.updatedAt)),9,c.muted)}return w}
async function buildAccessoryRectangular(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);const top=w.addStack();top.centerAlignContent();addSymbol(top,"house.fill",11,c.accent);top.addSpacer(5);addText(top,s.widgetTitle,11,c.text,"semibold");top.addSpacer();if(snap.connected)addText(top,snap.route,8,snap.route==="VPN"?c.warn:c.muted,"semibold");w.addSpacer(3);if(!snap.connected){addText(w,"Unavailable",10,c.fail,"semibold");return w}const row=w.addStack();addText(row,`CPU ${fmt(cpuLoad(snap))}%`,10,c.text,"semibold");row.addSpacer();addText(row,`RAM ${fmt(ramUsed(snap))}%`,10,c.text,"semibold");return w}
async function buildAccessoryInline(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);const bad=snap.connected?statusCount(snap).bad:1;const t=w.addText(snap.connected?`${bad?"⚠":"✓"} Homebridge · CPU ${fmt(cpuLoad(snap))}% · RAM ${fmt(ramUsed(snap))}%`:"⚠ Homebridge unavailable");t.font=Font.systemFont(11);t.textColor=bad?c.warn:c.text;return w}
async function buildAccessoryCircular(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);const st=w.addStack();st.layoutVertically();st.addSpacer();const r=st.addStack();r.addSpacer();addSymbol(r,snap.connected&&statusCount(snap).bad===0?"house.fill":"exclamationmark.triangle.fill",24,snap.connected&&statusCount(snap).bad===0?c.ok:c.warn);r.addSpacer();st.addSpacer();return w}
async function buildWidget(snap,s,family){if(family==="small")return await buildSmall(snap,s);if(family==="large")return await buildLarge(snap,s);if(family==="accessoryRectangular")return await buildAccessoryRectangular(snap,s);if(family==="accessoryInline")return await buildAccessoryInline(snap,s);if(family==="accessoryCircular")return await buildAccessoryCircular(snap,s);return await buildMedium(snap,s)}
async function presentWidget(w,f){if(f==="small")return await w.presentSmall();if(f==="large")return await w.presentLarge();if(f==="accessoryRectangular"&&typeof w.presentAccessoryRectangular==="function")return await w.presentAccessoryRectangular();if(f==="accessoryInline"&&typeof w.presentAccessoryInline==="function")return await w.presentAccessoryInline();if(f==="accessoryCircular"&&typeof w.presentAccessoryCircular==="function")return await w.presentAccessoryCircular();return await w.presentMedium()}

function notificationMessage(key,recovery){const bad={running:"Homebridge stopped 😱",hb:"Update available for Homebridge",plugins:"Update available for one of your plugins",node:"Update available for Node.js"};const good={running:"Homebridge is back online",hb:"Homebridge is up to date",plugins:"Plugins are up to date",node:"Node.js is up to date"};return(recovery?good:bad)[key]}
async function sendNotification(text,url){try{const n=new Notification();n.title="Homebridge Status changed";n.body=text;n.sound="event";if(url)n.openURL=url;await n.schedule()}catch(e){console.log(e)}}
async function handleNotifications(snap,s){if(!s.notificationEnabled||!snap.connected)return;const st=loadState();if(!st.notifications)st.notifications={};const now=Date.now(),interval=s.notificationIntervalHours*3600000;const current={running:snap.running,hb:snap.hbUtd,plugins:snap.pluginsUtd,node:snap.nodeUtd};for(const [key,val] of Object.entries(current)){if(val===undefined)continue;const prev=st.notifications[key]||{status:true,lastNotified:0};if(val===false){if(prev.status!==false||interval===0||now-Number(prev.lastNotified||0)>=interval){await sendNotification(notificationMessage(key,false),snap.base);prev.lastNotified=now}prev.status=false}else if(val===true&&prev.status===false){if(s.recoveryNotifications)await sendNotification(notificationMessage(key,true),snap.base);prev.status=true;prev.lastNotified=0}else prev.status=val;st.notifications[key]=prev}st.lastRoute=snap.route;st.lastUpdated=now;saveState(st)}

function cmp(a,b){const A=String(a).split(".").map(Number),B=String(b).split(".").map(Number);for(let i=0;i<Math.max(A.length,B.length);i++){if((A[i]||0)>(B[i]||0))return 1;if((A[i]||0)<(B[i]||0))return-1}return 0}
async function getRemoteSource(){const r=new Request(UPDATE_SOURCE_URL);r.timeoutInterval=8;return await r.loadString()}
async function updater(){try{const src=await getRemoteSource();if(!src||src.length<UPDATE_MIN_BYTES||!src.includes('const APP_NAME = "Homebridge Status"'))throw new Error("Bad source");const m=src.match(/const APP_VERSION\s*=\s*"([^"]+)"/);if(!m)throw new Error("No version");const v=m[1];if(cmp(v,APP_VERSION)<=0)return{ok:true,text:`Aktuální verze v${APP_VERSION}`};const a=new Alert();a.title=APP_NAME;a.message=`Dostupná aktualizace: v${v}`;a.addAction("Aktualizovat");a.addCancelAction("Zrušit");if(await a.presentAlert()!==0)return{ok:true,text:`v${APP_VERSION} → v${v}`};const target=module.filename;if(!target)throw new Error("Current script path unavailable");const cloud=FileManager.iCloud(),local=FileManager.local();let targetFm=local;if(cloud.fileExists(target)){targetFm=cloud;if(cloud.isFileDownloaded&&!(await cloud.isFileDownloaded(target)))await cloud.downloadFileFromiCloud(target)}else if(!local.fileExists(target))throw new Error("Current script file not found");const backup=/\.js$/i.test(target)?target.replace(/\.js$/i,`_backup_v${APP_VERSION}.js`):target+`_backup_v${APP_VERSION}.js`;try{targetFm.writeString(backup,targetFm.readString(target))}catch(_){}targetFm.writeString(target,src);return{ok:true,text:"Aktualizace nainstalována. Skript spusť znovu."}}catch(e){console.log(e);return{ok:false,text:"Kontrola aktualizace selhala: "+String(e?.message||e)}}}

function esc(v){return String(v??"").replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]))}
function settingsHTML(s){
  const json=JSON.stringify(s).replace(/</g,"\\u003c"),hasPassword=passwordStored();
  return `<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>
  *{box-sizing:border-box}body{margin:0;background:#0b1020;color:#f8fafc;font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text",sans-serif;padding:calc(env(safe-area-inset-top) + 16px) 14px calc(env(safe-area-inset-bottom) + 24px)}h1{font-size:28px;margin:4px 6px 2px}h2{font-size:14px;color:#94a3b8;margin:22px 8px 8px;text-transform:uppercase;letter-spacing:.08em}.sub{color:#94a3b8;margin:0 6px 18px;font-size:13px}.screen{display:none}.screen.active{display:block}.group{background:#141b2d;border-radius:16px;overflow:hidden}.row{display:flex;align-items:center;gap:12px;padding:13px 14px;border-bottom:1px solid #263044;min-height:52px}.row:last-child{border-bottom:0}.row.click{cursor:pointer}.ico{width:30px;height:30px;border-radius:8px;background:#0a84ff;display:flex;align-items:center;justify-content:center;font-size:16px}.grow{flex:1;min-width:0}.title{font-size:16px;font-weight:600}.detail{font-size:12px;color:#94a3b8;margin-top:2px;line-height:1.35}.chev{font-size:24px;color:#64748b}.field{padding:11px 14px;border-bottom:1px solid #263044}.field:last-child{border-bottom:0}label{display:block;font-size:12px;color:#94a3b8;margin-bottom:6px}input,select,textarea{width:100%;border:1px solid #334155;border-radius:10px;background:#0b1020;color:#f8fafc;padding:10px 11px;font-size:15px;outline:none}input[type=checkbox]{width:22px;height:22px}.switchrow{display:flex;align-items:center;padding:12px 14px;border-bottom:1px solid #263044}.switchrow:last-child{border-bottom:0}.switchrow span{flex:1}.btns{display:flex;gap:9px;flex-wrap:wrap}.btn{border:0;border-radius:11px;background:#0a84ff;color:white;padding:11px 14px;font-size:14px;font-weight:600}.btn.secondary{background:#263044}.btn.danger{background:#7f1d1d}.back{display:inline-block;color:#60a5fa;font-size:16px;margin:2px 6px 12px}.status{font-size:13px;color:#94a3b8;padding:8px 2px;min-height:28px}.ok{color:#34c759}.warn{color:#ff9f0a}.bad{color:#ff453a}.previewgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.previewgrid .btn{padding:11px 5px}.colorrow{display:grid;grid-template-columns:1fr 54px;gap:8px}.colorrow input[type=color]{padding:2px;height:42px}.foot{color:#64748b;text-align:center;font-size:11px;margin-top:22px}</style></head><body>
  <div id="main" class="screen active"><h1>Homebridge Status</h1><div class="sub">Homebridge monitoring · v${APP_VERSION}</div>
    <div class="group">
      ${nav("connection","🔗","Připojení","Primární LAN, záložní VPN a přihlášení")}
      ${nav("preview","▣","Náhled widgetu","Small / Medium / Large + Lock Screen")}
      ${nav("appearance","Aa","Vzhled widgetu","Motiv, barvy a zobrazované údaje")}
      ${nav("behavior","⏱","Chování","Obnova, timeout a ignorované aktualizace")}
      ${nav("notifications","🔔","Notifikace","Výpadky a dostupné aktualizace")}
      ${nav("update","↻","Aktualizace","Kontrola nové verze skriptu")}
    </div><div class="foot">Změny se ukládají automaticky.</div></div>

  ${screen("connection","Připojení",`
    <h2>Adresy</h2><div class="group">
      ${field("primaryUrl","Primární adresa (LAN)","http://192.168.1.50:8581")}
      ${field("fallbackUrl","Záložní adresa (VPN)","http://100.x.x.x:8581")}
    </div><div class="sub" style="margin-top:8px">Při každém obnovení se vždy nejdřív zkusí LAN. VPN se použije pouze pokud LAN neodpoví.</div>
    <h2>Přihlášení</h2><div class="group">${field("username","Uživatelské jméno","admin")}<div class="field"><label>Heslo ${hasPassword?"· uložené v Keychain":""}</label><input id="password" type="password" placeholder="${hasPassword?"Nech prázdné pro zachování":"Zadej heslo"}"></div><div class="switchrow"><span>Povolit neověřený HTTPS certifikát</span><input id="allowInsecure" type="checkbox"></div></div>
    <div class="btns" style="margin-top:12px"><button class="btn" onclick="saveConnection(true)">Otestovat připojení</button><button class="btn secondary" onclick="removePass()">Smazat heslo</button></div><div id="connectionStatus" class="status"></div>`)}

  ${screen("preview","Náhled widgetu",`<h2>Domovská obrazovka</h2><div class="previewgrid"><button class="btn" onclick="preview('small')">Small</button><button class="btn" onclick="preview('medium')">Medium</button><button class="btn" onclick="preview('large')">Large</button></div><h2>Lock Screen</h2><div class="previewgrid"><button class="btn secondary" onclick="preview('accessoryInline')">Inline</button><button class="btn secondary" onclick="preview('accessoryCircular')">Circular</button><button class="btn secondary" onclick="preview('accessoryRectangular')">Rectangular</button></div><div id="previewStatus" class="status"></div>`)}

  ${screen("appearance","Vzhled widgetu",`<h2>Vzhled</h2><div class="group"><div class="field"><label>Název widgetu</label><input id="widgetTitle"></div><div class="field"><label>Motiv</label><select id="theme"><option value="system">Systémový</option><option value="dark">Tmavě modrý</option><option value="black">Černý</option><option value="custom">Vlastní</option></select></div></div><h2>Zobrazení</h2><div class="group">${toggle("showGraphs","Grafy CPU / RAM")}${toggle("showTemperature","Teplota CPU")}${toggle("showUptime","Uptime")}${toggle("showUpdated","Čas poslední kontroly")}${toggle("showRoute","Zobrazit LAN / VPN")}</div><h2>Vlastní barvy</h2><div class="group">${colorField("backgroundColor","Pozadí")}${colorField("cardColor","Karty")}${colorField("textColor","Text")}${colorField("mutedColor","Vedlejší text")}${colorField("accentColor","Akcent")}${colorField("okColor","OK")}${colorField("warningColor","Varování")}${colorField("failColor","Chyba")}</div><div class="btns" style="margin-top:12px"><button class="btn secondary" onclick="resetAppearance()">Obnovit výchozí vzhled</button></div>`)}

  ${screen("behavior","Chování",`<h2>Obnova</h2><div class="group"><div class="field"><label>Interval widgetu (min)</label><input id="refreshMinutes" type="number" min="5" max="180"></div><div class="field"><label>Timeout požadavku (s)</label><input id="requestTimeout" type="number" min="1" max="30"></div></div><h2>Aktualizace Homebridge</h2><div class="group"><div class="field"><label>Ignorovat aktualizace</label><input id="ignoredUpdates" placeholder="homebridge-plugin, HOMEBRIDGE_UTD, NODEJS_UTD"><div class="detail">Odděl čárkou. Použij přesný npm název pluginu.</div></div></div>`)}

  ${screen("notifications","Notifikace",`<h2>Upozornění</h2><div class="group">${toggle("notificationEnabled","Zapnout notifikace")}${toggle("recoveryNotifications","Upozornit také při návratu do normálu")}<div class="field"><label>Opakovat stejnou chybu nejdříve za (hod)</label><input id="notificationIntervalHours" type="number" min="0" max="720"></div></div>`)}

  ${screen("update","Aktualizace",`<h2>Verze</h2><div class="group"><div class="row"><div class="grow"><div class="title">Homebridge Status</div><div class="detail">Aktuální verze v${APP_VERSION}</div></div></div></div><div class="btns" style="margin-top:12px"><button class="btn" onclick="post({action:'update'})">Zkontrolovat aktualizaci</button></div><div id="updateStatus" class="status"></div>`)}

<script>
const state=${json};const q=[];window.__nativeQueue=q;function post(x){q.push(x)}
function nav(id,icon,title,detail){return ''}
function show(id){document.querySelectorAll('.screen').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');sync()}
function back(){show('main')}
function sync(){for(const [k,v] of Object.entries(state)){const e=document.getElementById(k);if(!e)continue;if(e.type==='checkbox')e.checked=!!v;else e.value=v??''}}
function collect(){for(const k of Object.keys(state)){const e=document.getElementById(k);if(!e)continue;if(e.type==='checkbox')state[k]=e.checked;else if(e.type==='number')state[k]=Number(e.value);else state[k]=e.value}return state}
function save(){collect();post({action:'save',settings:state})}
function saveConnection(test){collect();const p=document.getElementById('password').value;post({action:test?'test':'saveConnection',settings:state,password:p});document.getElementById('password').value=''}
function removePass(){post({action:'removePassword'})}
function preview(f){collect();document.getElementById('previewStatus').textContent='Načítám…';post({action:'preview',family:f,settings:state})}
function resetAppearance(){Object.assign(state,{theme:'system',backgroundColor:'#0B1020',cardColor:'#141B2D',textColor:'#F8FAFC',mutedColor:'#94A3B8',accentColor:'#0A84FF',okColor:'#34C759',warningColor:'#FF9F0A',failColor:'#FF453A',showGraphs:true,showTemperature:true,showUptime:true,showUpdated:true,showRoute:true});sync();save()}
document.addEventListener('change',e=>{if(e.target.matches('input,select'))save()});window.__native=function(m){if(!m)return;if(m.action==='connection'){const e=document.getElementById('connectionStatus');e.textContent=m.text||'';e.className='status '+(m.ok?'ok':'bad')}if(m.action==='previewDone')document.getElementById('previewStatus').textContent='';if(m.action==='update'){const e=document.getElementById('updateStatus');e.textContent=m.text||'';e.className='status '+(m.ok?'ok':'bad')}if(m.action==='password'){const e=document.getElementById('connectionStatus');e.textContent=m.text||'';e.className='status'}};sync();
</script></body></html>`;

  function nav(id,icon,title,detail){return `<div class="row click" onclick="show('${id}')"><div class="ico">${icon}</div><div class="grow"><div class="title">${title}</div><div class="detail">${detail}</div></div><div class="chev">›</div></div>`}
  function screen(id,title,body){return `<div id="${id}" class="screen"><div class="back" onclick="back()">‹ Zpět</div><h1>${title}</h1>${body}</div>`}
  function field(id,label,placeholder){return `<div class="field"><label>${label}</label><input id="${id}" placeholder="${placeholder}"></div>`}
  function toggle(id,label){return `<div class="switchrow"><span>${label}</span><input id="${id}" type="checkbox"></div>`}
  function colorField(id,label){return `<div class="field"><label>${label}</label><div class="colorrow"><input id="${id}" oninput="document.getElementById('${id}Picker').value=this.value"><input id="${id}Picker" type="color" oninput="document.getElementById('${id}').value=this.value;state['${id}']=this.value;state.theme='custom';document.getElementById('theme').value='custom';save()"></div></div>`}
}
async function sendToWeb(web,o){try{await web.evaluateJavaScript(`window.__native(${JSON.stringify(o)})`,false)}catch(_){}}
async function settingsUI(s){const web=new WebView();await web.loadHTML(settingsHTML(s));let dismissed=false,cur=merge(s);const presented=web.present(false).then(()=>dismissed=true);const sleep=ms=>new Promise(resolve=>Timer.schedule(ms,false,resolve));while(!dismissed){await sleep(150);if(dismissed)break;let raw=null;try{raw=await web.evaluateJavaScript("JSON.stringify(window.__nativeQueue.shift()||null)")}catch(_){continue}if(!raw||raw==="null")continue;let m;try{m=JSON.parse(raw)}catch(_){continue}try{if(m.action==="save"||m.action==="saveConnection"){cur=merge(m.settings||cur);saveSettings(cur);if(m.password)setPassword(m.password)}else if(m.action==="test"){cur=merge(m.settings||cur);saveSettings(cur);if(m.password)setPassword(m.password);const snap=await getSnapshot(cur);await sendToWeb(web,{action:"connection",ok:snap.connected,text:snap.connected?`Připojeno přes ${snap.route}: ${snap.base}`:"Připojení se nezdařilo: "+(snap.error||"")})}else if(m.action==="removePassword"){removePassword();await sendToWeb(web,{action:"password",text:"Heslo bylo odstraněno z Keychain."})}else if(m.action==="preview"){cur=merge(m.settings||cur);saveSettings(cur);const snap=await getSnapshot(cur);const w=await buildWidget(snap,cur,m.family||"medium");try{await presentWidget(w,m.family||"medium")}finally{await sendToWeb(web,{action:"previewDone"})}}else if(m.action==="update"){const r=await updater();await sendToWeb(web,{action:"update",ok:r.ok,text:r.text})}}catch(e){console.log(e);await sendToWeb(web,{action:"connection",ok:false,text:String(e?.message||e)})}}
  try{await presented}catch(_){}return cur
}

let SETTINGS=await migrateLegacy(loadSettings());
if(config.runsInWidget){const family=config.widgetFamily||"medium";const snap=await getSnapshot(SETTINGS);await handleNotifications(snap,SETTINGS);const w=await buildWidget(snap,SETTINGS,family);Script.setWidget(w)}else{SETTINGS=await settingsUI(SETTINGS)}
Script.complete();
