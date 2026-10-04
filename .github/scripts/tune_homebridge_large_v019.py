from pathlib import Path
import re

p = Path('apps/Homebridge-Status/Homebridge Status.js')
s = p.read_text(encoding='utf-8')

s = s.replace('// Homebridge Status v0.1.8', '// Homebridge Status v0.1.9', 1)
s = s.replace('const APP_VERSION = "0.1.8";', 'const APP_VERSION = "0.1.9";', 1)

old = '''  const [cpu,ram,uptime,plugins,hbVersion,nodeVersion]=await Promise.all([\n    optionalApi(base,token,"/api/status/cpu",s),\n    optionalApi(base,token,"/api/status/ram",s),\n    optionalApi(base,token,"/api/status/uptime",s),\n    optionalApi(base,token,"/api/plugins",s),\n    optionalApi(base,token,"/api/status/homebridge-version",s),\n    optionalApi(base,token,"/api/status/nodejs",s)\n  ]);'''
new = '''  const [cpu,ram,uptime,plugins,hbVersion,nodeVersion,rpiHealth]=await Promise.all([\n    optionalApi(base,token,"/api/status/cpu",s),\n    optionalApi(base,token,"/api/status/ram",s),\n    optionalApi(base,token,"/api/status/uptime",s),\n    optionalApi(base,token,"/api/plugins",s),\n    optionalApi(base,token,"/api/status/homebridge-version",s),\n    optionalApi(base,token,"/api/status/nodejs",s),\n    optionalApi(base,token,"/api/status/rpi/throttled",s)\n  ]);'''
if old not in s:
    raise SystemExit('snapshot Promise block not found')
s = s.replace(old, new, 1)

old_return = 'return {connected:true,base,route,token,running,hbUtd,pluginsUtd,nodeUtd,cpu,ram,uptime,plugins,hbVersion,nodeVersion,updatedAt:Date.now()}'
new_return = 'return {connected:true,base,route,token,running,hbUtd,pluginsUtd,nodeUtd,cpu,ram,uptime,plugins,hbVersion,nodeVersion,rpiHealth,updatedAt:Date.now()}'
if old_return not in s:
    raise SystemExit('snapshot return not found')
s = s.replace(old_return, new_return, 1)

marker = 'function statusCount(snap){const values=[snap.running,snap.hbUtd,snap.pluginsUtd,snap.nodeUtd];return{bad:values.filter(v=>v===false).length,unknown:values.filter(v=>v===undefined).length}}\n'
helpers = '''function statusCount(snap){const values=[snap.running,snap.hbUtd,snap.pluginsUtd,snap.nodeUtd];return{bad:values.filter(v=>v===false).length,unknown:values.filter(v=>v===undefined).length}}\nfunction pluginUpdateCount(snap,s){if(!Array.isArray(snap.plugins))return snap.pluginsUtd===false?1:0;const ignored=ignoredSet(s);return snap.plugins.filter(p=>p.updateAvailable&&!ignored.has(p.name)).length}\nfunction rpiWarningKeys(snap){if(!snap.rpiHealth||typeof snap.rpiHealth!=="object")return null;return Object.entries(snap.rpiHealth).filter(([,v])=>v===true).map(([k])=>k)}\n'''
if marker not in s:
    raise SystemExit('statusCount marker not found')
s = s.replace(marker, helpers, 1)

pattern = re.compile(r'async function buildLarge\(snap,s\)\{.*?return w\}\nasync function buildAccessoryRectangular', re.S)
replacement = '''async function buildLarge(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(18,20,15,20);addHeader(w,s,c,snap,18);w.addSpacer(9);if(!snap.connected){addUnavailable(w,s,c,snap);return w}addStatusGrid(w,s,snap,c,11);w.addSpacer(9);const metrics=w.addStack();addMetricCard(metrics,tx(s,"cpuLoad"),fmt(cpuLoad(snap)),"%",snap.cpu?.cpuLoadHistory,c,s.showGraphs,"",true,145,true);metrics.addSpacer(10);addMetricCard(metrics,tx(s,"ramUsage"),fmt(ramUsed(snap)),"%",snap.ram?.memoryUsageHistory,c,s.showGraphs,"",true,145,true);w.addSpacer(9);addSystemPanel(w,s,snap,c);w.addSpacer(9);const section=w.addStack();section.layoutVertically();section.backgroundColor=c.card;section.cornerRadius=12;section.setPadding(8,10,7,10);addText(section,tx(s,"details"),8,c.muted,"semibold");section.addSpacer(5);const hb=snap.hbVersion,nd=snap.nodeVersion,pluginUpdates=pluginUpdateCount(snap,s),piWarnings=rpiWarningKeys(snap);const rows=[];if(hb)rows.push(["Homebridge",hb.installedVersion||hb.currentVersion||"—",hb.latestVersion||"—",snap.hbUtd]);if(nd)rows.push(["Node.js",nd.currentVersion||nd.installedVersion||"—",nd.latestVersion||"—",snap.nodeUtd]);rows.push([tx(s,"plugins"),pluginUpdates?`↑ ${pluginUpdates}`:"OK","",pluginUpdates===0]);rows.push(["Raspberry Pi",piWarnings===null?"—":piWarnings.length?`⚠ ${piWarnings.length}`:"OK","",piWarnings===null?undefined:piWarnings.length===0]);for(const [name,current,latest,ok] of rows.slice(0,4)){const r=section.addStack();r.centerAlignContent();const m=statusMeta(ok,c);addSymbol(r,m.icon,10,m.color);r.addSpacer(5);addText(r,name,10,c.text,"semibold");r.addSpacer();addText(r,latest?`${current} → ${latest}`:current,8,ok===false?c.warn:c.muted,"semibold");section.addSpacer(4)}w.addSpacer();if(s.showUpdated){const df=new DateFormatter();df.useNoDateStyle();df.useShortTimeStyle();const foot=w.addStack();foot.addSpacer();addText(foot,df.string(new Date(snap.updatedAt)),8,c.muted);foot.addSpacer()}return w}\nasync function buildAccessoryRectangular'''
s2, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit(f'buildLarge block replacement count={n}')
s = s2

p.write_text(s, encoding='utf-8')
print('Homebridge Status v0.1.9 Large health/details applied')
