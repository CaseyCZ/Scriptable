from pathlib import Path
import re

p = Path('apps/LockScreenGenerator/LockScreenGenerator.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.9.5";' in s
s = s.replace('const APP_VERSION = "2.9.5";', 'const APP_VERSION = "2.9.6";', 1)

# New installations start below the iOS lock-screen widget area.
s = s.replace('const DEFAULT_SETTINGS={settingsVersion:7,', 'const DEFAULT_SETTINGS={settingsVersion:8,', 1)
s = s.replace('startY:950,marginX:60', 'startY:1200,marginX:60', 1)

old_load = r'''async function loadSettings(){const fm=FileManager.iCloud(),path=fm.joinPath(fm.documentsDirectory(),SETTINGS_FILE);let saved={};try{if(fm.fileExists(path)){if(!fm.isFileDownloaded(path))await fm.downloadFileFromiCloud(path);saved=JSON.parse(fm.readString(path))}}catch(_){saved={}}const merged={...DEFAULT_SETTINGS,...saved};merged.sectionStyle=deepMergeStyle(saved.sectionStyle);merged.lastNameDays=saved.lastNameDays||{};merged.lastF1=saved.lastF1||[];let order=Array.isArray(saved.sectionOrder)?[...saved.sectionOrder]:[...DEFAULT_SETTINGS.sectionOrder];for(const key of Object.keys(MODULES))if(!order.includes(key))order.push(key);merged.sectionOrder=order.filter(key=>MODULES[key]);merged.settingsVersion=7;return merged}'''
new_load = r'''async function loadSettings(){const fm=FileManager.iCloud(),path=fm.joinPath(fm.documentsDirectory(),SETTINGS_FILE);let saved={};try{if(fm.fileExists(path)){if(!fm.isFileDownloaded(path))await fm.downloadFileFromiCloud(path);saved=JSON.parse(fm.readString(path))}}catch(_){saved={}}const previousVersion=Number(saved.settingsVersion)||0,merged={...DEFAULT_SETTINGS,...saved};merged.sectionStyle=deepMergeStyle(saved.sectionStyle);merged.lastNameDays=saved.lastNameDays||{};merged.lastF1=saved.lastF1||[];let order=Array.isArray(saved.sectionOrder)?[...saved.sectionOrder]:[...DEFAULT_SETTINGS.sectionOrder];for(const key of Object.keys(MODULES))if(!order.includes(key))order.push(key);merged.sectionOrder=order.filter(key=>MODULES[key]);const migrateStart=previousVersion<8&&Number(saved.startY)===950;if(migrateStart)merged.startY=1200;merged.settingsVersion=8;if(migrateStart)saveSettings(merged);return merged}'''
assert old_load in s, 'loadSettings block not found'
s = s.replace(old_load, new_load, 1)

s = s.replace('settingsVersion:7};saveSettings(settings)', 'settingsVersion:8};saveSettings(settings)', 1)
s = s.replace("startY:parseFloat(v('startY'))||950", "startY:parseFloat(v('startY'))||1200", 1)

old_f1 = r'''async function fetchF1Next(settings){try{const data=await timedRequest(`${apiBase(settings.apiF1Base,"https://api.jolpi.ca/ergast/f1")}/current/next.json`).loadJSON(),race=data?.MRData?.RaceTable?.Races?.[0];if(!race)return[];const out=[],add=(key,obj)=>{if(obj?.date)out.push({title:`🏎 ${race.raceName} · ${f1SessionLabel(settings.language,key)}`,date:new Date(obj.date+"T"+(obj.time||"00:00:00Z")),isF1:true})};if(settings.showF1Practice){add("p1",race.FirstPractice);add("p2",race.SecondPractice);add("p3",race.ThirdPractice)}if(settings.showF1Qualifying)add("q",race.Qualifying);if(settings.showF1Sprint)add("s",race.Sprint);if(settings.showF1Race)add("r",{date:race.date,time:race.time});settings.lastF1=out;if(!settings.__preview)saveSettings(settings);return out}catch(_){return(settings.lastF1||[]).map(x=>({...x,date:new Date(x.date)}))}}'''
new_f1 = r'''function filterF1ToVisibleRange(rows,settings){const start=new Date();start.setHours(0,0,0,0);const end=new Date(start);end.setDate(end.getDate()+Math.min(7,Math.max(1,Number(settings.daysToShow)||2)));return(rows||[]).map(x=>({...x,date:x.date instanceof Date?x.date:new Date(x.date)})).filter(x=>Number.isFinite(x.date?.getTime())&&x.date>=start&&x.date<end)}
async function fetchF1Next(settings){try{const data=await timedRequest(`${apiBase(settings.apiF1Base,"https://api.jolpi.ca/ergast/f1")}/current/next.json`).loadJSON(),race=data?.MRData?.RaceTable?.Races?.[0];if(!race)return[];const out=[],add=(key,obj)=>{if(obj?.date)out.push({title:`🏎 ${race.raceName} · ${f1SessionLabel(settings.language,key)}`,date:new Date(obj.date+"T"+(obj.time||"00:00:00Z")),isF1:true})};if(settings.showF1Practice){add("p1",race.FirstPractice);add("p2",race.SecondPractice);add("p3",race.ThirdPractice)}if(settings.showF1Qualifying)add("q",race.Qualifying);if(settings.showF1Sprint)add("s",race.Sprint);if(settings.showF1Race)add("r",{date:race.date,time:race.time});settings.lastF1=out;if(!settings.__preview)saveSettings(settings);return filterF1ToVisibleRange(out,settings)}catch(_){return filterF1ToVisibleRange(settings.lastF1||[],settings)}}'''
assert old_f1 in s, 'fetchF1Next block not found'
s = s.replace(old_f1, new_f1, 1)

p.write_text(s, encoding='utf-8')
print('Patched LockScreen Generator to 2.9.6')
