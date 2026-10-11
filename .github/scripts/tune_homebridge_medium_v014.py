from pathlib import Path

p = Path('apps/Homebridge-Status/Homebridge Status.js')
s = p.read_text(encoding='utf-8')

s = s.replace('// Homebridge Status v0.1.3', '// Homebridge Status v0.1.4', 1)
s = s.replace('const APP_VERSION = "0.1.3";', 'const APP_VERSION = "0.1.4";', 1)

marker = 'function addStatusGrid(w,s,snap,c,font=11){const card=w.addStack();card.backgroundColor=c.card;card.cornerRadius=12;card.setPadding(8,10,8,10);const row=card.addStack();const left=row.addStack();left.layoutVertically();addStatusRow(left,tx(s,"running"),snap.running,c,font);left.addSpacer(5);addStatusRow(left,tx(s,"plugins"),snap.pluginsUtd,c,font);row.addSpacer();const right=row.addStack();right.layoutVertically();addStatusRow(right,"Homebridge",snap.hbUtd,c,font);right.addSpacer(5);addStatusRow(right,"Node.js",snap.nodeUtd,c,font);return card}\n'

addition = marker + '''function installedVersion(info,node=false){const raw=String(info?.installedVersion||info?.currentVersion||"").trim();if(!raw)return"—";return node&&!/^v/i.test(raw)?"v"+raw:raw}\nfunction addMediumVersionRow(parent,label,value,version,c,font=10){const r=parent.addStack();r.centerAlignContent();const m=statusMeta(value,c);addSymbol(r,m.icon,font+1,m.color);r.addSpacer(5);addText(r,label,font,c.text,"semibold");r.addSpacer(7);addText(r,version,font-1,c.muted,"semibold");return r}\nfunction addMediumStatusGrid(w,s,snap,c,font=10){const row=w.addStack();const left=row.addStack();left.layoutVertically();addStatusRow(left,tx(s,"running"),snap.running,c,font);left.addSpacer(5);addStatusRow(left,tx(s,"plugins"),snap.pluginsUtd,c,font);row.addSpacer();const right=row.addStack();right.layoutVertically();addMediumVersionRow(right,"Homebridge",snap.hbUtd,installedVersion(snap.hbVersion),c,font);right.addSpacer(5);addMediumVersionRow(right,"Node.js",snap.nodeUtd,installedVersion(snap.nodeVersion,true),c,font);return row}\n'''
if 'function addMediumStatusGrid(' not in s:
    if marker not in s:
        raise SystemExit('status grid marker not found')
    s = s.replace(marker, addition, 1)

old = 'async function buildMedium(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(15,18,13,18);addHeader(w,s,c,snap,16);w.addSpacer(9);if(!snap.connected){addUnavailable(w,s,c,snap);return w}addStatusGrid(w,s,snap,c,10);w.addSpacer(9);const metrics=w.addStack();const temp=cpuTemp(snap);addMetricCard(metrics,tx(s,"cpuLoad"),fmt(cpuLoad(snap)),"%",snap.cpu?.cpuLoadHistory,c,s.showGraphs,s.showTemperature&&temp!==null?fmt(temp)+" °C":"");metrics.addSpacer(9);addMetricCard(metrics,tx(s,"ramUsage"),fmt(ramUsed(snap)),"%",snap.ram?.memoryUsageHistory,c,s.showGraphs);w.addSpacer();if(s.showUptime&&snap.uptime){const foot=w.addStack();addText(foot,"Pi "+formatSeconds(snap.uptime?.time?.uptime),9,c.muted,"semibold");foot.addSpacer();addText(foot,"UI "+formatSeconds(snap.uptime?.processUptime),9,c.muted,"semibold")}return w}'
new = 'async function buildMedium(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(13,13,11,13);addHeader(w,s,c,snap,16);w.addSpacer(9);if(!snap.connected){addUnavailable(w,s,c,snap);return w}addMediumStatusGrid(w,s,snap,c,10);w.addSpacer(9);const metrics=w.addStack();const temp=cpuTemp(snap);addMetricCard(metrics,tx(s,"cpuLoad"),fmt(cpuLoad(snap)),"%",snap.cpu?.cpuLoadHistory,c,s.showGraphs,s.showTemperature&&temp!==null?fmt(temp)+" °C":"");metrics.addSpacer(9);addMetricCard(metrics,tx(s,"ramUsage"),fmt(ramUsed(snap)),"%",snap.ram?.memoryUsageHistory,c,s.showGraphs);w.addSpacer();if(s.showUptime&&snap.uptime){const foot=w.addStack();addText(foot,"Pi "+formatSeconds(snap.uptime?.time?.uptime),9,c.muted,"semibold");foot.addSpacer();addText(foot,"UI "+formatSeconds(snap.uptime?.processUptime),9,c.muted,"semibold")}return w}'
if old not in s:
    raise SystemExit('buildMedium v0.1.3 block not found')
s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('Homebridge Status v0.1.4 medium widget applied')
