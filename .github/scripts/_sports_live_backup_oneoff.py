from pathlib import Path
import re

p = Path('apps/Sports-Live/Sports-Live,js')
s = p.read_text(encoding='utf-8')

s = s.replace('// Sports Live v0.3.1', '// Sports Live v0.3.2', 1)
s = s.replace('const APP_VERSION = "0.3.1";', 'const APP_VERSION = "0.3.2";', 1)

replacements = {
    'export:"Exportovat",import:"Importovat"': 'export:"Uložit zálohu",import:"Importovat zálohu"',
    'copied:"Nastavení bylo zkopírováno."': 'copied:"Záloha byla uložena do souboru."',
    'export:"Export",import:"Import"': 'export:"Save backup",import:"Import backup"',
    'copied:"Settings copied."': 'copied:"Backup file saved."',
    'export:"Exportieren",import:"Importieren"': 'export:"Backup speichern",import:"Backup importieren"',
    'copied:"Einstellungen kopiert."': 'copied:"Backup-Datei gespeichert."',
    'export:"Exportar",import:"Importar"': 'export:"Guardar copia",import:"Importar copia"',
    'copied:"Ajustes copiados."': 'copied:"Archivo de copia guardado."',
}
for old, new in replacements.items():
    s = s.replace(old, new, 1)

maintenance_pattern = r'<div class="screen" id="maintenance">.*?<script>'
maintenance_new = '''<div class="screen" id="maintenance">${back}<div class="screenTitle">💾 ${esc(L.maintenance)}</div><div class="card"><div class="actionGrid"><button class="actionBtn full" onclick="exportJSON()">💾 ${esc(L.export)}</button><button class="actionBtn secondary full" onclick="importJSON()">📥 ${esc(L.import)}</button><button class="actionBtn secondary" onclick="clearCache()">🧹 ${esc(L.clearCache)}</button><button class="actionBtn secondary" onclick="resetPart('appearance')">🎨 ${esc(L.resetAppearance)}</button><button class="actionBtn secondary" onclick="resetPart('team')">🏆 ${esc(L.resetTeam)}</button><button class="actionBtn danger" onclick="resetPart('all')">↺ ${esc(L.resetAll)}</button></div><div id="toolStatus" class="status"></div></div></div>

<script>'''
s, count = re.subn(maintenance_pattern, maintenance_new, s, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f'maintenance block replacements: {count}')

old = "function exportJSON(){emit('export',{settings:collect()})}function importJSON(){emit('import',{raw:document.getElementById('jsonBox').value})}"
new = "function exportJSON(){emit('export',{settings:collect()})}function importJSON(){emit('importFile',{settings:collect()})}"
if old not in s:
    raise SystemExit('web backup handlers not found')
s = s.replace(old, new, 1)

old_export = 'else if(m.action==="export"){cur=merge(m.settings||cur);saveSettings(cur);Pasteboard.copyString(JSON.stringify(cur,null,2));await send(web,{action:"status",ok:true,text:tx(cur,"copied")})}'
new_export = '''else if(m.action==="export"){
        cur=merge(m.settings||cur);saveSettings(cur);
        const now=new Date(),pad=n=>String(n).padStart(2,"0");
        const stamp=now.getFullYear()+"-"+pad(now.getMonth()+1)+"-"+pad(now.getDate())+"_"+pad(now.getHours())+"-"+pad(now.getMinutes());
        const backup={app:APP_NAME,version:APP_VERSION,exportedAt:now.toISOString(),settings:cur};
        await DocumentPicker.exportString(JSON.stringify(backup,null,2),"Sports Live backup "+stamp+".json");
        await send(web,{action:"status",ok:true,text:tx(cur,"copied")})
      }'''
if old_export not in s:
    raise SystemExit('native export handler not found')
s = s.replace(old_export, new_export, 1)

old_import = 'else if(m.action==="import"){try{cur=merge(JSON.parse(m.raw||""));if(!cur.language)cur.language=s.language||lang();saveSettings(cur);await send(web,{action:"status",ok:true,text:tx(cur,"imported")});await send(web,{action:"replace",settings:cur})}catch(_){await send(web,{action:"status",ok:false,text:tx(cur,"invalid")})}}'
new_import = '''else if(m.action==="importFile"){
        try{
          const path=await DocumentPicker.openFile();
          if(!path)throw new Error(tx(cur,"invalid"));
          const raw=FileManager.local().readString(path);
          const parsed=JSON.parse(raw||"");
          const incoming=parsed&&parsed.app===APP_NAME&&parsed.settings?parsed.settings:parsed;
          if(!incoming||typeof incoming!=="object"||Array.isArray(incoming))throw new Error(tx(cur,"invalid"));
          cur=merge(incoming);if(!cur.language)cur.language=s.language||lang();saveSettings(cur);
          await send(web,{action:"status",ok:true,text:tx(cur,"imported")});await send(web,{action:"replace",settings:cur})
        }catch(_){await send(web,{action:"status",ok:false,text:tx(cur,"invalid")})}
      }'''
if old_import not in s:
    raise SystemExit('native import handler not found')
s = s.replace(old_import, new_import, 1)

if 'textarea id="jsonBox"' in s:
    raise SystemExit('json editor still present')
if 'DocumentPicker.exportString' not in s or 'DocumentPicker.openFile' not in s:
    raise SystemExit('DocumentPicker backup functions missing')

p.write_text(s, encoding='utf-8')
