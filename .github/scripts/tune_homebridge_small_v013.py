from pathlib import Path

p = Path('apps/Homebridge-Status/Homebridge Status.js')
s = p.read_text(encoding='utf-8')

s = s.replace('// Homebridge Status v0.1.2', '// Homebridge Status v0.1.3', 1)
s = s.replace('const APP_VERSION = "0.1.2";', 'const APP_VERSION = "0.1.3";', 1)

old = '''async function buildSmall(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(14,16,11,16);addHeader(w,s,c,snap,13);w.addSpacer(7);if(!snap.connected){addUnavailable(w,s,c,snap);return w}const count=statusCount(snap),panel=w.addStack();panel.layoutVertically();panel.backgroundColor=c.card;panel.cornerRadius=12;panel.setPadding(7,8,6,8);const big=panel.addText(count.bad?`⚠ ${count.bad}`:"✓");big.font=Font.boldSystemFont(22);big.textColor=count.bad?c.warn:c.ok;big.centerAlignText();panel.addSpacer(3);let line=panel.addText(`CPU ${fmt(cpuLoad(snap))}%  ·  RAM ${fmt(ramUsed(snap))}%`);line.font=Font.semiboldSystemFont(9);line.textColor=c.text;line.centerAlignText();panel.addSpacer(3);const temp=cpuTemp(snap),up=formatSeconds(snap.uptime?.time?.uptime);line=panel.addText(`${s.showTemperature&&temp!==null?fmt(temp)+" °C":"—"}  ·  Pi ${up}`);line.font=Font.systemFont(8);line.textColor=c.muted;line.centerAlignText();w.addSpacer();if(s.showUpdated){const df=new DateFormatter();df.useNoDateStyle();df.useShortTimeStyle();const f=w.addText(df.string(new Date(snap.updatedAt)));f.font=Font.systemFont(8);f.textColor=c.muted;f.centerAlignText()}return w}'''

new = '''function centeredPanelText(parent,text,size,color,weight="regular"){const r=parent.addStack();r.addSpacer();const t=addText(r,text,size,color,weight);r.addSpacer();return t}
function smallUpdateCount(snap,s){let n=0;if(snap.hbUtd===false)n++;if(snap.nodeUtd===false)n++;if(Array.isArray(snap.plugins)){n+=snap.plugins.filter(p=>p.updateAvailable&&!ignoredSet(s).has(p.name)).length}else if(snap.pluginsUtd===false)n++;return n}
function smallUpdateText(s,n){const lang=s.language||"cs";const words={cs:n===1?"aktualizace":"aktualizace",en:n===1?"update":"updates",de:n===1?"Update":"Updates",es:n===1?"actualización":"actualizaciones"};return `↑ ${n} ${words[lang]||words.cs}`}
function smallProblemText(s){return {cs:"⚠ Homebridge neběží",en:"⚠ Homebridge stopped",de:"⚠ Homebridge gestoppt",es:"⚠ Homebridge detenido"}[s.language||"cs"]}
async function buildSmall(snap,s){const c=colors(s),w=new ListWidget();configureWidget(w,s,c);w.setPadding(14,16,11,16);addHeader(w,s,c,snap,13);w.addSpacer(7);if(!snap.connected){addUnavailable(w,s,c,snap);return w}const updates=smallUpdateCount(snap,s),stopped=snap.running===false,panel=w.addStack();panel.layoutVertically();panel.backgroundColor=c.card;panel.cornerRadius=12;panel.setPadding(7,8,7,8);centeredPanelText(panel,stopped?"!":"✓",22,stopped?c.fail:(updates?c.warn:c.ok),"bold");panel.addSpacer(3);centeredPanelText(panel,`CPU ${fmt(cpuLoad(snap))}%  ·  RAM ${fmt(ramUsed(snap))}%`,9,c.text,"semibold");panel.addSpacer(3);const temp=cpuTemp(snap),up=formatSeconds(snap.uptime?.time?.uptime);centeredPanelText(panel,`${s.showTemperature&&temp!==null?fmt(temp)+" °C":"—"}  ·  Pi ${up}`,8,c.muted);if(stopped||updates){panel.addSpacer(4);centeredPanelText(panel,stopped?smallProblemText(s):smallUpdateText(s,updates),8,stopped?c.fail:c.warn,"semibold")}w.addSpacer();if(s.showUpdated){const df=new DateFormatter();df.useNoDateStyle();df.useShortTimeStyle();const f=w.addText(df.string(new Date(snap.updatedAt)));f.font=Font.systemFont(8);f.textColor=c.muted;f.centerAlignText()}return w}'''

if old not in s:
    raise SystemExit('buildSmall v0.1.2 block not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Homebridge Status v0.1.3 small widget applied')
