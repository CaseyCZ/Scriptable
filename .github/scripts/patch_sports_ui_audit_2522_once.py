from pathlib import Path

app=Path('apps/Sports-Info/Sports Info.js')
s=app.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.5.21";' in s
s=s.replace('// Sports Info v2.5.21','// Sports Info v2.5.22',1)
s=s.replace('const APP_VERSION = "2.5.21";','const APP_VERSION = "2.5.22";',1)

old="function preview(f){state=commitNow();const e=document.getElementById('previewMeta');if(e)e.textContent=UI.loading;document.querySelectorAll('.previewBtn').forEach(b=>b.disabled=true);emit('preview',{family:f,settings:state})}"
new="function preview(f){state=commitNow();emit('preview',{family:f,settings:state})}"
assert old in s
s=s.replace(old,new,1)

old="function recommendedWidget(){const checks={showLive:true,showNext:true,showLast:true,showTable:true,showForm:true,showLogos:true};for(const [k,v] of Object.entries(checks)){const e=document.getElementById(k);if(e)e.checked=v}const n=document.getElementById('maxMatches');if(n)n.value=4;save();const st=document.getElementById('widgetPresetStatus');if(st)st.textContent=HELP.recommendedDone||'OK'}"
new="function recommendedWidget(){const checks={showLive:true,showNext:true,showLast:true,showTable:true,showForm:true,showLogos:true};for(const [k,v] of Object.entries(checks)){const e=document.getElementById(k);if(e)e.checked=v}const n=document.getElementById('maxMatches');if(n)n.value=4;state=commitNow();const st=document.getElementById('widgetPresetStatus');if(st)st.textContent=HELP.recommendedDone||'OK'}"
assert old in s
s=s.replace(old,new,1)

old='''      }else if(m.action==="clearCache"){
        try{if(fm.fileExists(cachePath))fm.remove(cachePath)}catch(_){}await send(web,{action:"status",ok:true,text:tx(cur,"cacheCleared")})
      }else if(m.action==="reset"){
        const l=cur.language||lang();if(m.part==="appearance")cur=Object.assign({},cur,{theme:DEFAULTS.theme,accent:DEFAULTS.accent,background:DEFAULTS.background,panelColor:DEFAULTS.panelColor,textColor:DEFAULTS.textColor,mutedColor:DEFAULTS.mutedColor,liveColor:DEFAULTS.liveColor,winColor:DEFAULTS.winColor,compact:DEFAULTS.compact,refreshMinutes:DEFAULTS.refreshMinutes});else if(m.part==="sport")cur=Object.assign({},cur,{sportId:DEFAULTS.sportId,leagueId:DEFAULTS.leagueId,teamId:"",teamName:""});else{cur=clone(DEFAULTS);cur.language=l}saveSettings(cur);await send(web,{action:"status",ok:true,text:tx(cur,"resetDone")});await send(web,{action:"replace",settings:cur})
'''
new='''      }else if(m.action==="clearCache"){
        try{const dir=fm.cacheDirectory();for(const name of fm.listContents(dir))if(name==CACHE_FILE||name.startsWith("SportsInfo_")){try{fm.remove(fm.joinPath(dir,name))}catch(_){}}}catch(_){try{if(fm.fileExists(cachePath))fm.remove(cachePath)}catch(__){}}await send(web,{action:"status",ok:true,text:tx(cur,"cacheCleared")})
      }else if(m.action==="reset"){
        cur=merge(m.settings||cur);const l=cur.language||lang();if(m.part==="appearance")cur=Object.assign({},cur,{theme:DEFAULTS.theme,accent:DEFAULTS.accent,background:DEFAULTS.background,panelColor:DEFAULTS.panelColor,textColor:DEFAULTS.textColor,mutedColor:DEFAULTS.mutedColor,liveColor:DEFAULTS.liveColor,winColor:DEFAULTS.winColor,compact:DEFAULTS.compact,refreshMinutes:DEFAULTS.refreshMinutes});else if(m.part==="sport")cur=Object.assign({},cur,{sportId:DEFAULTS.sportId,leagueId:DEFAULTS.leagueId,teamId:"",teamName:""});else{cur=clone(DEFAULTS);cur.language=l}saveSettings(cur);await send(web,{action:"status",ok:true,text:tx(cur,"resetDone")});await send(web,{action:"replace",settings:cur})
'''
assert old in s
s=s.replace(old,new,1)

app.write_text(s,encoding='utf-8')
