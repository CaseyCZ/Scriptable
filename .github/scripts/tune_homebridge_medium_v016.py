from pathlib import Path

p = Path('apps/Homebridge-Status/Homebridge Status.js')
s = p.read_text(encoding='utf-8')

s = s.replace('// Homebridge Status v0.1.5', '// Homebridge Status v0.1.6', 1)
s = s.replace('const APP_VERSION = "0.1.5";', 'const APP_VERSION = "0.1.6";', 1)

old_metric = '''function addMetricCard(parent,title,value,unit,history,c,showGraph=true,tempText=""){const card=parent.addStack();card.layoutVertically();card.backgroundColor=c.card;card.cornerRadius=12;card.setPadding(9,10,8,10);addText(card,title,9,c.muted,"semibold");card.addSpacer(3);const v=card.addStack();v.centerAlignContent();addText(v,value,18,c.text,"bold");v.addSpacer(3);addText(v,unit,9,c.muted);if(tempText){v.addSpacer();addText(v,tempText,9,c.muted,"semibold")}if(showGraph&&Array.isArray(history)&&history.length>1){card.addSpacer(6);const img=new LineChart(320,60,history).image(c.accent);const ih=card.addImage(img);ih.imageSize=new Size(120,22)}return card}'''
new_metric = '''function addMetricCard(parent,title,value,unit,history,c,showGraph=true,tempText="",centerTitle=false,graphWidth=120){const card=parent.addStack();card.layoutVertically();card.backgroundColor=c.card;card.cornerRadius=12;card.setPadding(9,10,8,10);if(centerTitle){const titleRow=card.addStack();titleRow.addSpacer();addText(titleRow,title,9,c.muted,"semibold");titleRow.addSpacer()}else addText(card,title,9,c.muted,"semibold");card.addSpacer(3);const v=card.addStack();v.centerAlignContent();addText(v,value,18,c.text,"bold");v.addSpacer(3);addText(v,unit,9,c.muted);if(tempText){v.addSpacer();addText(v,tempText,9,c.muted,"semibold")}if(showGraph&&Array.isArray(history)&&history.length>1){card.addSpacer(6);const img=new LineChart(320,60,history).image(c.accent);const ih=card.addImage(img);ih.imageSize=new Size(graphWidth,22)}return card}'''
if old_metric not in s:
    raise SystemExit('metric card block not found')
s = s.replace(old_metric, new_metric, 1)

old_top = '''function addMediumTop(w,s,snap,c){const top=w.addStack();top.centerAlignContent();const brand=top.addStack();brand.centerAlignContent();addSymbol(brand,"house.fill",15,c.accent);brand.addSpacer(6);addText(brand,s.widgetTitle||APP_NAME,15,c.text,"bold");if(s.showRoute&&snap.route){brand.addSpacer(6);addText(brand,snap.route,8,snap.route==="VPN"?c.warn:c.muted,"semibold")}top.addSpacer(12);const grid=top.addStack();grid.layoutVertically();let r=grid.addStack();addMediumCompactStatus(r,tx(s,"running"),snap.running,"",c,9);r.addSpacer(10);addMediumCompactStatus(r,"Homebridge",snap.hbUtd,installedVersion(snap.hbVersion),c,9);grid.addSpacer(4);r=grid.addStack();addMediumCompactStatus(r,tx(s,"plugins"),snap.pluginsUtd,"",c,9);r.addSpacer(10);addMediumCompactStatus(r,"Node.js",snap.nodeUtd,installedVersion(snap.nodeVersion,true),c,9);return top}'''
new_top = '''function addMediumTop(w,s,snap,c){const top=w.addStack();top.centerAlignContent();const brand=top.addStack();brand.centerAlignContent();addSymbol(brand,"house.fill",15,c.accent);brand.addSpacer(6);addText(brand,s.widgetTitle||APP_NAME,15,c.text,"bold");if(s.showRoute&&snap.route){brand.addSpacer(6);addText(brand,snap.route,8,snap.route==="VPN"?c.warn:c.muted,"semibold")}top.addSpacer();const grid=top.addStack();grid.layoutVertically();let r=grid.addStack();addMediumCompactStatus(r,tx(s,"running"),snap.running,"",c,9);r.addSpacer(10);addMediumCompactStatus(r,"Homebridge",snap.hbUtd,installedVersion(snap.hbVersion),c,9);grid.addSpacer(4);r=grid.addStack();addMediumCompactStatus(r,tx(s,"plugins"),snap.pluginsUtd,"",c,9);r.addSpacer(10);addMediumCompactStatus(r,"Node.js",snap.nodeUtd,installedVersion(snap.nodeVersion,true),c,9);return top}'''
if old_top not in s:
    raise SystemExit('medium top block not found')
s = s.replace(old_top, new_top, 1)

old_build = '''async function buildMedium(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(11,13,9,13);if(!snap.connected){addHeader(w,s,c,snap,16);addUnavailable(w,s,c,snap);return w}addMediumTop(w,s,snap,c);w.addSpacer(8);const metrics=w.addStack();addMetricCard(metrics,tx(s,"cpuLoad"),fmt(cpuLoad(snap)),"%",snap.cpu?.cpuLoadHistory,c,s.showGraphs,"");metrics.addSpacer(9);addMetricCard(metrics,tx(s,"ramUsage"),fmt(ramUsed(snap)),"%",snap.ram?.memoryUsageHistory,c,s.showGraphs);w.addSpacer();addMediumFooter(w,s,snap,c);return w}'''
new_build = '''async function buildMedium(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(11,10,9,10);if(!snap.connected){addHeader(w,s,c,snap,16);addUnavailable(w,s,c,snap);return w}addMediumTop(w,s,snap,c);w.addSpacer(8);const metrics=w.addStack();addMetricCard(metrics,tx(s,"cpuLoad"),fmt(cpuLoad(snap)),"%",snap.cpu?.cpuLoadHistory,c,s.showGraphs,"",true,136);metrics.addSpacer(7);addMetricCard(metrics,tx(s,"ramUsage"),fmt(ramUsed(snap)),"%",snap.ram?.memoryUsageHistory,c,s.showGraphs,"",true,136);w.addSpacer();addMediumFooter(w,s,snap,c);return w}'''
if old_build not in s:
    raise SystemExit('medium build block not found')
s = s.replace(old_build, new_build, 1)

p.write_text(s, encoding='utf-8')
print('Homebridge Status v0.1.6 medium alignment applied')
