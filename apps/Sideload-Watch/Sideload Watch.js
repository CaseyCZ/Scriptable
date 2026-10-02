// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-purple; icon-glyph: magic;
// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: download;
// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: download;
// ============================================================
// Sideload Watch v0.2.10
// CaseyCZ Scriptable Apps
// iOS-Hub update watcher.
// Settings and updater follow the same UI pattern as Sports Info
// and LockScreen Generator. Widget appearance intentionally unchanged.
// ============================================================

const APP_NAME = "Sideload Watch";
const APP_VERSION = "0.2.10";
const SETTINGS_FILE = "SideloadWatch_settings.json";
const STATE_FILE = "SideloadWatch_state.json";
const CATALOG_CACHE_FILE = "SideloadWatch_catalog.json";
const CATALOG_META_FILE = "SideloadWatch_catalog_meta.json";
const CATALOG_URL = "https://raw.githubusercontent.com/CaseyCZ/iOS-Hub/main/data/catalog.json";
const CATALOG_META_URL = "https://raw.githubusercontent.com/CaseyCZ/iOS-Hub/main/data/catalog-meta.json";
const HUB_URL = "https://caseycz.github.io/iOS-Hub/";
const UPDATE_SOURCE_URL = "https://raw.githubusercontent.com/CaseyCZ/Scriptable/Master/apps/Sideload-Watch/Sideload%20Watch.js";
const UPDATE_MIN_BYTES = 12000;
const API_TIMEOUT = 12;

const T = {
  cs:{
    settings:"Nastavení",subtitle:"Vyber zdroje a konkrétní aplikace, které chceš sledovat.",
    watched:"Sledované aplikace",watchedDetail:"Vyber source a potom aplikace uvnitř.",
    preview:"Náhled widgetu",previewDetail:"Vzhled widgetu zůstává stejný.",
    appearance:"Vzhled widgetu",appearanceDetail:"Název, popisky, viditelnost a barvy widgetu.",
    widgetTitle:"Název widgetu",footerLabel:"Spodní popisek",footerLabelDetail:"Nech prázdné pro automatický text.",
    visibility:"Viditelnost",showNew:"Zobrazit NEW",showVersion:"Zobrazit verzi",showCount:"Zobrazit počet aktualizací",showTime:"Zobrazit čas kontroly",
    customColors:"Vlastní barvy",useCustomColors:"Použít vlastní barvy",backgroundColor:"Barva pozadí",textColor:"Barva textu",mutedColor:"Barva vedlejšího textu",newColor:"Barva NEW textu",newBgColor:"Barva NEW pozadí",countColor:"Barva počtu aktualizací",resetAppearance:"Obnovit výchozí vzhled",
    tools:"Nástroje",toolsDetail:"Aktualizace, export, reset a údržba.",
    sources:"Sources",sourcesSub:"Otevři source a vyber konkrétní aplikace, které chceš sledovat.",
    searchSource:"Hledat source…",searchApp:"Hledat aplikaci…",apps:"aplikací",selected:"vybráno",
    back:"Zpět",selectAll:"Vybrat vše",clearAll:"Zrušit vše",none:"Nic nenalezeno",
    widgetPreview:"Náhled",realPreview:"Reálná data",demoPreview:"Demo · 7 aktualizací",
    small:"Small",medium:"Medium",large:"Large",
    behavior:"Chování",refresh:"Obnova widgetu",refreshDetail:"Požadovaný interval obnovy. iOS může widget obnovit později.",
    minutes:"min",language:"Jazyk",languageDetail:"Jazyk nastavení a widgetu.",
    maintenance:"Údržba",markSeen:"Označit aktualizace jako přečtené",markSeenDetail:"Aktuální verze se uloží jako výchozí.",
    resetBaseline:"Resetovat uložené verze",resetBaselineDetail:"Při další kontrole se vytvoří nová výchozí verze.",
    refreshCatalog:"Obnovit katalog iOS-Hub",refreshCatalogDetail:"Načte nejnovější seznam sources a aplikací.",
    export:"Export nastavení",import:"Import nastavení",update:"Zkontrolovat aktualizaci",current:"Aktuální verze",
    available:"Dostupná aktualizace",apply:"Aktualizovat",cancel:"Zrušit",updatedOk:"Aktualizace nainstalována. Skript spusť znovu.",
    updateFail:"Kontrola aktualizace selhala.",copied:"Nastavení zkopírováno.",imported:"Nastavení importováno.",
    invalid:"Neplatný JSON.",done:"Hotovo",resetDone:"Uložené verze byly resetovány.",catalogUpdated:"Katalog byl obnoven.",
    catalogFail:"Katalog se nepodařilo načíst.",catalogCached:"Používá se uložený katalog.",online:"Online",cached:"Cache",
    selectedApps:"Sledováno",noSelection:"Nejsou vybrané žádné aplikace",noSelectionDetail:"Otevři Sledované aplikace a vyber alespoň jednu položku.",
    title:"Sideload Watch",new:"NEW",upToDate:"Všechno je aktuální",offline:"offline",
    updates:n=>`${n} ${n===1?"aktualizace":(n>=2&&n<=4?"aktualizace":"aktualizací")}`,
    firstRun:"Vyber jazyk",saveHint:"Změny se ukládají automaticky."
  },
  en:{
    settings:"Settings",subtitle:"Choose sources and the exact apps you want to watch.",
    watched:"Watched apps",watchedDetail:"Choose a source, then select apps inside it.",
    preview:"Widget preview",previewDetail:"Widget appearance stays unchanged.",
    appearance:"Widget appearance",appearanceDetail:"Title, labels, visibility and widget colors.",
    widgetTitle:"Widget title",footerLabel:"Footer label",footerLabelDetail:"Leave empty for automatic text.",
    visibility:"Visibility",showNew:"Show NEW",showVersion:"Show version",showCount:"Show update count",showTime:"Show checked time",
    customColors:"Custom colors",useCustomColors:"Use custom colors",backgroundColor:"Background color",textColor:"Text color",mutedColor:"Secondary text color",newColor:"NEW text color",newBgColor:"NEW background color",countColor:"Update count color",resetAppearance:"Reset appearance",
    tools:"Tools",toolsDetail:"Updates, export, reset and maintenance.",
    sources:"Sources",sourcesSub:"Open a source and choose the exact apps you want to watch.",
    searchSource:"Search sources…",searchApp:"Search apps…",apps:"apps",selected:"selected",
    back:"Back",selectAll:"Select all",clearAll:"Clear all",none:"Nothing found",
    widgetPreview:"Preview",realPreview:"Live data",demoPreview:"Demo · 7 updates",
    small:"Small",medium:"Medium",large:"Large",
    behavior:"Behavior",refresh:"Widget refresh",refreshDetail:"Requested refresh interval. iOS may refresh the widget later.",
    minutes:"min",language:"Language",languageDetail:"Language used by settings and widget.",
    maintenance:"Maintenance",markSeen:"Mark updates as seen",markSeenDetail:"Current versions become the new baseline.",
    resetBaseline:"Reset saved versions",resetBaselineDetail:"A new baseline will be created on the next check.",
    refreshCatalog:"Refresh iOS-Hub catalog",refreshCatalogDetail:"Loads the latest sources and app list.",
    export:"Export settings",import:"Import settings",update:"Check for update",current:"Current version",
    available:"Update available",apply:"Update",cancel:"Cancel",updatedOk:"Update installed. Run the script again.",
    updateFail:"Update check failed.",copied:"Settings copied.",imported:"Settings imported.",
    invalid:"Invalid JSON.",done:"Done",resetDone:"Saved versions were reset.",catalogUpdated:"Catalog refreshed.",
    catalogFail:"Catalog could not be loaded.",catalogCached:"Using cached catalog.",online:"Online",cached:"Cache",
    selectedApps:"Watching",noSelection:"No apps selected",noSelectionDetail:"Open Watched apps and select at least one item.",
    title:"Sideload Watch",new:"NEW",upToDate:"Everything is up to date",offline:"offline",
    updates:n=>`${n} update${n===1?"":"s"} available`,
    firstRun:"Choose language",saveHint:"Changes are saved automatically."
  },
  de:{
    settings:"Einstellungen",subtitle:"Wähle Quellen und konkrete Apps aus, die du beobachten möchtest.",
    watched:"Beobachtete Apps",watchedDetail:"Quelle öffnen und anschließend Apps darin auswählen.",
    preview:"Widget-Vorschau",previewDetail:"Das Aussehen des Widgets bleibt unverändert.",
    appearance:"Widget-Aussehen",appearanceDetail:"Titel, Texte, Sichtbarkeit und Farben des Widgets.",
    widgetTitle:"Widget-Titel",footerLabel:"Fußzeile",footerLabelDetail:"Leer lassen für automatischen Text.",
    visibility:"Sichtbarkeit",showNew:"NEW anzeigen",showVersion:"Version anzeigen",showCount:"Update-Anzahl anzeigen",showTime:"Prüfzeit anzeigen",
    customColors:"Eigene Farben",useCustomColors:"Eigene Farben verwenden",backgroundColor:"Hintergrundfarbe",textColor:"Textfarbe",mutedColor:"Sekundärtextfarbe",newColor:"NEW-Textfarbe",newBgColor:"NEW-Hintergrundfarbe",countColor:"Farbe der Update-Anzahl",resetAppearance:"Aussehen zurücksetzen",
    tools:"Werkzeuge",toolsDetail:"Updates, Export, Reset und Wartung.",
    sources:"Quellen",sourcesSub:"Öffne eine Quelle und wähle die Apps aus, die du beobachten möchtest.",
    searchSource:"Quelle suchen…",searchApp:"App suchen…",apps:"Apps",selected:"ausgewählt",
    back:"Zurück",selectAll:"Alle auswählen",clearAll:"Alle abwählen",none:"Nichts gefunden",
    widgetPreview:"Vorschau",realPreview:"Echte Daten",demoPreview:"Demo · 7 Updates",
    small:"Small",medium:"Medium",large:"Large",
    behavior:"Verhalten",refresh:"Widget-Aktualisierung",refreshDetail:"Gewünschtes Intervall. iOS kann das Widget später aktualisieren.",
    minutes:"Min",language:"Sprache",languageDetail:"Sprache für Einstellungen und Widget.",
    maintenance:"Wartung",markSeen:"Updates als gelesen markieren",markSeenDetail:"Aktuelle Versionen werden als neuer Ausgangspunkt gespeichert.",
    resetBaseline:"Gespeicherte Versionen zurücksetzen",resetBaselineDetail:"Bei der nächsten Prüfung wird ein neuer Ausgangspunkt erstellt.",
    refreshCatalog:"iOS-Hub-Katalog aktualisieren",refreshCatalogDetail:"Lädt die neuesten Quellen und Apps.",
    export:"Einstellungen exportieren",import:"Einstellungen importieren",update:"Auf Update prüfen",current:"Aktuelle Version",
    available:"Update verfügbar",apply:"Aktualisieren",cancel:"Abbrechen",updatedOk:"Update installiert. Skript erneut starten.",
    updateFail:"Update-Prüfung fehlgeschlagen.",copied:"Einstellungen kopiert.",imported:"Einstellungen importiert.",
    invalid:"Ungültiges JSON.",done:"Fertig",resetDone:"Gespeicherte Versionen wurden zurückgesetzt.",catalogUpdated:"Katalog aktualisiert.",
    catalogFail:"Katalog konnte nicht geladen werden.",catalogCached:"Gespeicherter Katalog wird verwendet.",online:"Online",cached:"Cache",
    selectedApps:"Beobachtet",noSelection:"Keine Apps ausgewählt",noSelectionDetail:"Öffne Beobachtete Apps und wähle mindestens eine App.",
    title:"Sideload Watch",new:"NEW",upToDate:"Alles ist aktuell",offline:"offline",
    updates:n=>`${n} Update${n===1?"":"s"} verfügbar`,
    firstRun:"Sprache wählen",saveHint:"Änderungen werden automatisch gespeichert."
  },
  es:{
    settings:"Ajustes",subtitle:"Elige las fuentes y las aplicaciones concretas que quieres vigilar.",
    watched:"Apps vigiladas",watchedDetail:"Abre una fuente y selecciona las apps dentro.",
    preview:"Vista previa",previewDetail:"El aspecto del widget no cambia.",
    appearance:"Apariencia del widget",appearanceDetail:"Título, textos, visibilidad y colores del widget.",
    widgetTitle:"Título del widget",footerLabel:"Etiqueta inferior",footerLabelDetail:"Déjalo vacío para usar texto automático.",
    visibility:"Visibilidad",showNew:"Mostrar NEW",showVersion:"Mostrar versión",showCount:"Mostrar número de actualizaciones",showTime:"Mostrar hora de comprobación",
    customColors:"Colores personalizados",useCustomColors:"Usar colores personalizados",backgroundColor:"Color de fondo",textColor:"Color del texto",mutedColor:"Color del texto secundario",newColor:"Color del texto NEW",newBgColor:"Color del fondo NEW",countColor:"Color del número de actualizaciones",resetAppearance:"Restablecer apariencia",
    tools:"Herramientas",toolsDetail:"Actualizaciones, exportación, reinicio y mantenimiento.",
    sources:"Fuentes",sourcesSub:"Abre una fuente y elige las apps concretas que quieres vigilar.",
    searchSource:"Buscar fuente…",searchApp:"Buscar app…",apps:"apps",selected:"seleccionadas",
    back:"Atrás",selectAll:"Seleccionar todo",clearAll:"Borrar todo",none:"Sin resultados",
    widgetPreview:"Vista previa",realPreview:"Datos reales",demoPreview:"Demo · 7 actualizaciones",
    small:"Small",medium:"Medium",large:"Large",
    behavior:"Comportamiento",refresh:"Actualización del widget",refreshDetail:"Intervalo solicitado. iOS puede actualizar el widget más tarde.",
    minutes:"min",language:"Idioma",languageDetail:"Idioma de los ajustes y del widget.",
    maintenance:"Mantenimiento",markSeen:"Marcar actualizaciones como vistas",markSeenDetail:"Las versiones actuales se guardan como nueva base.",
    resetBaseline:"Restablecer versiones guardadas",resetBaselineDetail:"En la próxima comprobación se creará una nueva base.",
    refreshCatalog:"Actualizar catálogo iOS-Hub",refreshCatalogDetail:"Carga las fuentes y apps más recientes.",
    export:"Exportar ajustes",import:"Importar ajustes",update:"Buscar actualización",current:"Versión actual",
    available:"Actualización disponible",apply:"Actualizar",cancel:"Cancelar",updatedOk:"Actualización instalada. Ejecuta el script otra vez.",
    updateFail:"Falló la búsqueda de actualización.",copied:"Ajustes copiados.",imported:"Ajustes importados.",
    invalid:"JSON no válido.",done:"Hecho",resetDone:"Versiones guardadas restablecidas.",catalogUpdated:"Catálogo actualizado.",
    catalogFail:"No se pudo cargar el catálogo.",catalogCached:"Usando catálogo guardado.",online:"Online",cached:"Caché",
    selectedApps:"Vigiladas",noSelection:"No hay apps seleccionadas",noSelectionDetail:"Abre Apps vigiladas y selecciona al menos una.",
    title:"Sideload Watch",new:"NEW",upToDate:"Todo está actualizado",offline:"offline",
    updates:n=>`${n} actualizaci${n===1?"ón":"ones"}`,
    firstRun:"Elige idioma",saveHint:"Los cambios se guardan automáticamente."
  }
};

const DEFAULTS = {
  language:null,
  watched:[],
  refreshMinutes:30,
  settingsVersion:1,

  widgetTitle:"Sideload Watch",
  footerLabel:"",
  showNew:true,
  showVersion:true,
  showCount:true,
  showTime:true,

  useCustomColors:false,
  backgroundColor:"#0B1020",
  textColor:"#F8FAFC",
  mutedColor:"#94A3B8",
  newColor:"#34C759",
  newBgColor:"#12351E",
  countColor:"#34C759"
};

const fm = FileManager.local();
const settingsPath = fm.joinPath(fm.documentsDirectory(), SETTINGS_FILE);
const statePath = fm.joinPath(fm.documentsDirectory(), STATE_FILE);
const catalogCachePath = fm.joinPath(fm.cacheDirectory(), CATALOG_CACHE_FILE);
const catalogMetaPath = fm.joinPath(fm.cacheDirectory(), CATALOG_META_FILE);

function clone(o){return JSON.parse(JSON.stringify(o))}
function lang(){const l=(Device.locale()||"en").slice(0,2).toLowerCase();return["cs","en","de","es"].includes(l)?l:"en"}
function tx(s,k){const l=s.language||lang();return(T[l]||T.en)[k]||T.en[k]||k}
function clamp(n,a,b){return Math.max(a,Math.min(b,n))}
function esc(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}

function watchKey(x){
  return `${String(x.sourceId||"")}|${String(x.bundleIdentifier||"")}|${String(x.name||"")}`;
}
function normalizeWatched(list){
  const out=[],seen=new Set();
  for(const raw of Array.isArray(list)?list:[]){
    const x={
      sourceId:String(raw?.sourceId||"").trim(),
      bundleIdentifier:String(raw?.bundleIdentifier||"").trim(),
      name:String(raw?.name||"").trim(),
      sourceURL:String(raw?.sourceURL||"").trim()
    };
    if(!x.sourceId||!x.name)continue;
    const k=watchKey(x);if(seen.has(k))continue;seen.add(k);out.push(x);
  }
  return out;
}
function merge(raw){
  const s=Object.assign(clone(DEFAULTS),raw||{});
  if(!["cs","en","de","es"].includes(s.language))s.language=null;
  s.refreshMinutes=clamp(Number(s.refreshMinutes)||30,15,180);
  s.watched=normalizeWatched(s.watched);
  s.widgetTitle=String(s.widgetTitle??DEFAULTS.widgetTitle).slice(0,40);
  s.footerLabel=String(s.footerLabel??"").slice(0,40);
  for(const k of ["showNew","showVersion","showCount","showTime","useCustomColors"]){
    if(typeof s[k]!=="boolean")s[k]=DEFAULTS[k]
  }
  for(const k of ["backgroundColor","textColor","mutedColor","newColor","newBgColor","countColor"]){
    if(!/^#[0-9a-fA-F]{6}$/.test(String(s[k]||"")))s[k]=DEFAULTS[k]
  }
  s.settingsVersion=1;
  return s;
}
function loadSettings(){
  try{if(fm.fileExists(settingsPath))return merge(JSON.parse(fm.readString(settingsPath)))}catch(e){console.log(e)}
  return clone(DEFAULTS);
}
function saveSettings(s){try{fm.writeString(settingsPath,JSON.stringify(merge(s),null,2))}catch(e){console.log(e)}}
async function firstLanguage(s){
  if(s.language)return s;
  if(config.runsInWidget){s.language=lang();saveSettings(s);return s}
  const a=new Alert();a.title=APP_NAME;a.message=tx({...s,language:lang()},"firstRun");
  ["🇨🇿 Čeština","🇬🇧 English","🇩🇪 Deutsch","🇪🇸 Español"].forEach(x=>a.addAction(x));
  const i=await a.presentAlert();s.language=["cs","en","de","es"][Math.max(0,i)]||"en";saveSettings(s);return s
}

async function requestJSON(url){
  const r=new Request(url);r.timeoutInterval=API_TIMEOUT;return await r.loadJSON()
}
async function getString(url){
  const r=new Request(url);r.timeoutInterval=API_TIMEOUT;return await r.loadString()
}
function normalizeCatalog(data){
  return {
    generatedAt:String(data?.generatedAt||""),
    sources:(Array.isArray(data?.sources)?data.sources:[]).map(src=>({
      id:String(src?.id||""),
      name:String(src?.name||src?.id||""),
      iconURL:String(src?.iconURL||""),
      sourceURL:String(src?.sourceURL||""),
      apps:(Array.isArray(src?.apps)?src.apps:[]).map(app=>({
        name:String(app?.name||""),
        bundleIdentifier:String(app?.bundleIdentifier||""),
        version:String(app?.version||"—"),
        iconURL:String(app?.iconURL||src?.iconURL||"")
      })).filter(a=>a.name)
    })).filter(s=>s.id&&s.name)
  };
}
function readCachedCatalog(){
  try{
    if(!fm.fileExists(catalogCachePath))return null;
    return normalizeCatalog(JSON.parse(fm.readString(catalogCachePath)));
  }catch(_){return null}
}
function readCatalogMeta(){
  try{
    if(!fm.fileExists(catalogMetaPath))return {version:""};
    const p=JSON.parse(fm.readString(catalogMetaPath));
    return {
      version:String(p?.version||p?.sha||""),
      checkedAt:String(p?.checkedAt||"")
    };
  }catch(_){return {version:""}}
}
function saveCatalogMeta(version){
  try{
    fm.writeString(catalogMetaPath,JSON.stringify({
      version:String(version||""),
      checkedAt:new Date().toISOString()
    }))
  }catch(_){}
}
async function fetchCatalogMeta(){
  const r=new Request(CATALOG_META_URL);
  r.timeoutInterval=config.runsInWidget?4:API_TIMEOUT;
  const p=await r.loadJSON();
  const version=String(p?.generatedAt||"");
  if(!version)throw new Error("Catalog version unavailable");
  return version
}
async function downloadCatalog(remoteVersion=""){
  const data=normalizeCatalog(await requestJSON(CATALOG_URL));
  if(!data.sources.length)throw new Error("Empty catalog");
  fm.writeString(catalogCachePath,JSON.stringify(data));
  saveCatalogMeta(remoteVersion||data.generatedAt||"");
  return data
}
async function fetchCatalog(force=false){
  const cached=readCachedCatalog();

  if(force){
    try{
      let remoteVersion="";
      try{remoteVersion=await fetchCatalogMeta()}catch(_){}
      const data=await downloadCatalog(remoteVersion);
      return {data,online:true,cached:false,updated:true,version:remoteVersion}
    }catch(e){
      if(cached)return {data:cached,online:false,cached:true,error:String(e)};
      throw e
    }
  }

  if(!cached){
    try{
      let remoteVersion="";
      try{remoteVersion=await fetchCatalogMeta()}catch(_){}
      const data=await downloadCatalog(remoteVersion);
      return {data,online:true,cached:false,updated:true,version:remoteVersion}
    }catch(e){throw e}
  }

  try{
    const remoteVersion=await fetchCatalogMeta();
    const localVersion=readCatalogMeta().version;

    if(localVersion&&remoteVersion===localVersion){
      return {data:cached,online:true,cached:true,updated:false,version:remoteVersion}
    }

    const data=await downloadCatalog(remoteVersion);
    return {data,online:true,cached:false,updated:true,version:remoteVersion}
  }catch(e){
    return {data:cached,online:false,cached:true,updated:false,error:String(e)}
  }
}
function sourceById(catalog,id){return(catalog?.sources||[]).find(x=>x.id===id)||null}
function resolveWatched(catalog,settings){
  const out=[];
  for(const item of settings.watched){
    const src=sourceById(catalog,item.sourceId);if(!src)continue;
    const app=(src.apps||[]).find(a=>a.name===item.name&&String(a.bundleIdentifier||"")===String(item.bundleIdentifier||""))
      ||(src.apps||[]).find(a=>String(a.bundleIdentifier||"")===String(item.bundleIdentifier||"")&&item.bundleIdentifier)
      ||(src.apps||[]).find(a=>a.name===item.name);
    if(!app)continue;
    out.push({
      key:watchKey(item),sourceId:item.sourceId,sourceName:src.name,sourceURL:item.sourceURL||src.sourceURL||"",
      name:item.name||app.name,version:String(app.version||"—"),
      iconURL:app.iconURL||src.iconURL||""
    });
  }
  return out;
}
function enrichWatchedSources(settings,catalog){
  const s=merge(settings),map=new Map((catalog?.sources||[]).map(src=>[src.id,src]));
  let changed=false;
  s.watched=s.watched.map(item=>{
    if(item.sourceURL)return item;
    const src=map.get(item.sourceId);
    if(!src?.sourceURL)return item;
    changed=true;
    return {...item,sourceURL:String(src.sourceURL)}
  });
  if(changed)saveSettings(s);
  return s
}

function loadState(){
  try{
    if(!fm.fileExists(statePath))return{seen:{},lastCurrent:{},updatedAt:null};
    const p=JSON.parse(fm.readString(statePath));
    return{seen:p.seen||{},lastCurrent:p.lastCurrent||{},updatedAt:p.updatedAt||null}
  }catch(_){return{seen:{},lastCurrent:{},updatedAt:null}}
}
function saveState(s){fm.writeString(statePath,JSON.stringify(s,null,2))}
function resetState(){try{if(fm.fileExists(statePath))fm.remove(statePath)}catch(_){}}

function cachedStatus(settings,error=null){
  const state=loadState(),updates=[],current=[];
  for(const item of settings.watched){
    const key=watchKey(item),now=state.lastCurrent[key];
    if(!now)continue;
    const app={key,name:now.name||item.name,version:now.version||"—",iconURL:now.iconURL||"",sourceName:now.sourceName||""};
    current.push(app);
    if(state.seen[key]&&app.version!==state.seen[key])updates.push(app)
  }
  return{
    updates,total:updates.length,current,
    checkedAt:state.updatedAt?new Date(state.updatedAt):null,
    offline:true,cached:true,error:error?String(error):null
  }
}
function timeoutAfter(ms,label="Widget"){
  return new Promise((_,reject)=>Timer.schedule(ms,false,()=>reject(new Error(label+" timeout"))))
}
function sourceVersion(app){
  const versions=Array.isArray(app?.versions)?app.versions.filter(x=>x&&typeof x==="object"):[];
  if(versions.length){
    versions.sort((a,b)=>{
      const da=Date.parse(a?.date||a?.versionDate||"")||0;
      const db=Date.parse(b?.date||b?.versionDate||"")||0;
      return db-da
    });
    if(versions[0]?.version)return String(versions[0].version)
  }
  return String(app?.version||app?.absoluteVersion||"—")
}
function sourceAppMatch(app,item){
  const bundle=String(app?.bundleIdentifier||app?.bundleID||"");
  if(item.bundleIdentifier&&bundle===item.bundleIdentifier)return true;
  return String(app?.name||"")===item.name
}
async function requestSourceJSON(url,timeout=3.5){
  const r=new Request(url);
  r.timeoutInterval=timeout;
  return await r.loadJSON()
}
async function getLiveStatus(settings){
  const state=loadState();
  const groups=new Map();
  for(const item of settings.watched){
    const url=String(item.sourceURL||"").trim();
    if(!url)continue;
    if(!groups.has(url))groups.set(url,[]);
    groups.get(url).push(item)
  }

  if(!groups.size)return cachedStatus(settings);

  const results=await Promise.allSettled([...groups.entries()].map(async([url,items])=>{
    const payload=await requestSourceJSON(url,3.5);
    const apps=Array.isArray(payload?.apps)?payload.apps:[];
    return{url,items,apps,sourceName:String(payload?.name||"")}
  }));

  const current=[],failedSourceIds=new Set();
  for(const result of results){
    if(result.status!=="fulfilled"){
      continue
    }
    const {items,apps,sourceName}=result.value;
    for(const item of items){
      const app=apps.find(a=>sourceAppMatch(a,item));
      if(!app)continue;
      current.push({
        key:watchKey(item),
        sourceId:item.sourceId,
        sourceName:sourceName||item.sourceId,
        sourceURL:item.sourceURL,
        name:item.name||String(app?.name||""),
        version:sourceVersion(app),
        iconURL:String(app?.iconURL||"")
      })
    }
  }

  // For a failed/missing live result, keep the last known value so the widget
  // remains complete instead of disappearing.
  const have=new Set(current.map(x=>x.key));
  for(const item of settings.watched){
    const key=watchKey(item);
    if(have.has(key))continue;
    const now=state.lastCurrent[key];
    if(!now)continue;
    current.push({
      key,
      sourceId:item.sourceId,
      sourceName:now.sourceName||item.sourceId,
      sourceURL:item.sourceURL||"",
      name:now.name||item.name,
      version:now.version||"—",
      iconURL:now.iconURL||""
    })
  }

  let changed=false;
  for(const app of current){
    if(!state.seen[app.key]){state.seen[app.key]=app.version;changed=true}
    state.lastCurrent[app.key]={
      name:app.name,version:app.version,iconURL:app.iconURL,
      sourceName:app.sourceName,sourceURL:app.sourceURL||""
    }
  }
  state.updatedAt=new Date().toISOString();
  if(changed||current.length)saveState(state);

  const updates=current.filter(app=>state.seen[app.key]&&state.seen[app.key]!==app.version);
  const offline=results.some(r=>r.status!=="fulfilled");
  return{updates,total:updates.length,current,checkedAt:new Date(),offline,cached:offline}
}
async function getLiveStatusWithBudget(settings,ms){
  try{
    return await Promise.race([
      getLiveStatus(settings),
      timeoutAfter(ms,"Widget data")
    ])
  }catch(error){
    console.log("Widget fallback: "+error);
    return cachedStatus(settings,error)
  }
}
async function markAllSeen(settings){
  const r=await getLiveStatus(settings),current=r.current||[],state=loadState();
  for(const app of current){
    state.seen[app.key]=app.version;
    state.lastCurrent[app.key]={name:app.name,version:app.version,iconURL:app.iconURL,sourceName:app.sourceName,sourceURL:app.sourceURL||""};
  }
  state.updatedAt=new Date().toISOString();saveState(state);return current.length
}
function demoStatus(){
  const demo=[
    {name:"Stremio",version:"2.0.9"},
    {name:"YouTubeRebornPlus",version:"20.06.1"},
    {name:"Yattee",version:"2.1.0"},
    {name:"SideStore",version:"0.6.3"},
    {name:"UTM",version:"4.8.0"},
    {name:"Provenance",version:"3.4.0"},
    {name:"VortX",version:"0.5.0"}
  ];
  return{updates:demo,total:demo.length,checkedAt:new Date(),offline:false,demo:true}
}

// ------------------------------------------------------------
// Widget appearance — intentionally kept the same as test v0.1.
// ------------------------------------------------------------
function widgetText(settings){
  const L=T[settings.language||lang()]||T.en;
  return{
    title:settings.widgetTitle||L.title,new:L.new,upToDate:L.upToDate,offline:L.offline,
    updates:n=>String(settings.footerLabel||"").trim()?String(settings.footerLabel).trim():L.updates(n)
  }
}
function colors(settings){
  if(settings.useCustomColors){
    return{
      bg:new Color(settings.backgroundColor||"#0B1020"),
      panel:new Color(settings.backgroundColor||"#0B1020"),
      text:new Color(settings.textColor||"#F8FAFC"),
      muted:new Color(settings.mutedColor||"#94A3B8"),
      border:new Color("263449"),
      green:new Color(settings.newColor||"#34C759"),
      greenSoft:new Color(settings.newBgColor||"#12351E"),
      red:new Color("FF453A"),
      blue:new Color("0A84FF"),
      count:new Color(settings.countColor||"#34C759")
    }
  }
  return{
    bg:Color.dynamic(new Color("F5F7FB"),new Color("0B1020")),
    panel:Color.dynamic(new Color("FFFFFF"),new Color("111827")),
    text:Color.dynamic(new Color("111827"),new Color("F8FAFC")),
    muted:Color.dynamic(new Color("6B7280"),new Color("94A3B8")),
    border:Color.dynamic(new Color("E5E7EB"),new Color("263449")),
    green:new Color("34C759"),
    greenSoft:Color.dynamic(new Color("E8F8ED"),new Color("12351E")),
    red:new Color("FF453A"),
    blue:new Color("0A84FF"),
    count:new Color("34C759")
  }
}
function layoutForFamily(family){
  if(family==="small")return{maxRows:2,title:14,row:11,version:10,footer:9,pad:11,rowGap:5};
  if(family==="large")return{maxRows:9,title:17,row:14,version:12,footer:11,pad:15,rowGap:7};
  return{maxRows:4,title:16,row:13,version:11,footer:10,pad:13,rowGap:6}
}
function addNewBadge(stack,c,fontSize,label){
  const badge=stack.addStack();badge.backgroundColor=c.greenSoft;badge.cornerRadius=5;badge.setPadding(2,5,2,5);
  const t=badge.addText(label);t.font=Font.boldSystemFont(fontSize);t.textColor=c.green;t.lineLimit=1
}
function formatTime(date){
  if(!date||isNaN(date.getTime()))return"—";
  const f=new DateFormatter();f.locale=Device.locale();f.useNoDateStyle();f.useShortTimeStyle();return f.string(date)
}
async function buildWidget(status,settings,familyOverride){
  const family=familyOverride||config.widgetFamily||"medium",L=layoutForFamily(family),c=colors(settings),W=widgetText(settings),w=new ListWidget();
  w.backgroundColor=c.bg;w.setPadding(L.pad,L.pad,L.pad,L.pad);
  try{w.url=URLScheme.forRunningScript()}catch(_){w.url="scriptable://"}

  const header=w.addStack();header.centerAlignContent();
  const symbol=SFSymbol.named("arrow.triangle.2.circlepath");symbol.applyFont(Font.semiboldSystemFont(L.title));
  const icon=header.addImage(symbol.image);icon.imageSize=new Size(L.title,L.title);icon.tintColor=c.blue;
  header.addSpacer(7);
  const title=header.addText(W.title);title.font=Font.boldSystemFont(L.title);title.textColor=c.text;title.lineLimit=1;
  header.addSpacer();
  if(status.demo){const d=header.addText("DEMO");d.font=Font.boldSystemFont(Math.max(8,L.footer));d.textColor=c.muted}

  w.addSpacer(family==="small"?8:10);

  if(!settings.watched.length){
    const body=w.addStack();body.layoutVertically();body.addSpacer();
    const mark=body.addText("＋");mark.font=Font.boldSystemFont(family==="small"?24:30);mark.textColor=c.blue;mark.centerAlignText();
    body.addSpacer(4);
    const msg=body.addText(tx(settings,"noSelection"));msg.font=Font.semiboldSystemFont(family==="small"?11:13);msg.textColor=c.text;msg.centerAlignText();msg.lineLimit=2;
    body.addSpacer();
  }else if(status.total===0){
    const body=w.addStack();body.layoutVertically();body.addSpacer();
    const ok=body.addText("✓");ok.font=Font.boldSystemFont(family==="small"?24:30);ok.textColor=c.green;ok.centerAlignText();
    body.addSpacer(4);
    const msg=body.addText(W.upToDate);msg.font=Font.semiboldSystemFont(family==="small"?11:13);msg.textColor=c.text;msg.centerAlignText();msg.lineLimit=2;
    body.addSpacer();
  }else{
    const visible=status.updates.slice(0,L.maxRows);
    for(let i=0;i<visible.length;i++){
      const app=visible[i],row=w.addStack();row.centerAlignContent();row.size=new Size(0,family==="small"?21:24);
      const name=row.addText(app.name);name.font=Font.semiboldSystemFont(L.row);name.textColor=c.text;name.lineLimit=1;name.minimumScaleFactor=.65;
      if(settings.showNew!==false){
        row.addSpacer(6);addNewBadge(row,c,Math.max(8,L.footer),W.new)
      }
      if(settings.showVersion!==false){
        row.addSpacer(6);
        const version=row.addText(app.version);version.font=Font.mediumSystemFont(L.version);version.textColor=c.muted;version.lineLimit=1;version.minimumScaleFactor=.7
      }
      if(i<visible.length-1)w.addSpacer(L.rowGap)
    }
  }

  w.addSpacer();
  if(settings.showCount!==false||settings.showTime!==false||status.offline){
    const footer=w.addStack();footer.centerAlignContent();
    if(settings.showCount!==false){
      const count=footer.addText(W.updates(status.total));count.font=Font.boldSystemFont(L.footer);count.textColor=status.total>0?(c.count||c.green):c.muted;count.lineLimit=1;count.minimumScaleFactor=.7
    }
    if(settings.showCount!==false&&(settings.showTime!==false||status.offline))footer.addSpacer();
    if(status.offline){
      const off=footer.addText("⚠︎ "+W.offline);off.font=Font.mediumSystemFont(L.footer);off.textColor=c.red
    }else if(settings.showTime!==false){
      const checked=footer.addText(formatTime(status.checkedAt));checked.font=Font.mediumSystemFont(L.footer);checked.textColor=c.muted
    }
  }
  w.refreshAfterDate=new Date(Date.now()+settings.refreshMinutes*60000);
  return w
}
function buildErrorWidget(settings,error){
  const family=config.widgetFamily||"medium",L=layoutForFamily(family),c=colors(settings),w=new ListWidget();
  w.backgroundColor=c.bg;w.setPadding(L.pad,L.pad,L.pad,L.pad);
  const title=w.addText(settings.widgetTitle||"Sideload Watch");
  title.font=Font.boldSystemFont(L.title);title.textColor=c.text;title.lineLimit=1;
  w.addSpacer(8);
  const msg=w.addText("⚠︎ "+(tx(settings,"offline")||"offline"));
  msg.font=Font.semiboldSystemFont(L.row);msg.textColor=c.red;msg.lineLimit=2;
  if(error){
    w.addSpacer(5);
    const detail=w.addText(String(error).slice(0,120));
    detail.font=Font.systemFont(Math.max(8,L.footer));detail.textColor=c.muted;detail.lineLimit=3;
  }
  w.refreshAfterDate=new Date(Date.now()+15*60000);
  return w
}
async function widget(settings,family){
  const fam=family||config.widgetFamily||"medium";
  const status=config.runsInWidget
    ? await getLiveStatusWithBudget(settings,6000)
    : await getLiveStatus(settings);
  const w=await buildWidget(status,settings,fam);
  Script.setWidget(w);
  return w
}
async function presentWidget(widget,family){
  if(family==="small")return await widget.presentSmall();
  if(family==="large")return await widget.presentLarge();
  return await widget.presentMedium()
}

// ------------------------------------------------------------
// Self updater — same pattern as Sports Info.
// ------------------------------------------------------------
function cmp(a,b){
  const A=String(a).split(".").map(Number),B=String(b).split(".").map(Number);
  for(let i=0;i<Math.max(A.length,B.length);i++){
    if((A[i]||0)>(B[i]||0))return 1;
    if((A[i]||0)<(B[i]||0))return-1
  }
  return 0
}
async function updater(s){
  try{
    const src=await getString(UPDATE_SOURCE_URL+"?t="+Date.now());
    if(!src||src.length<UPDATE_MIN_BYTES||!src.includes('const APP_NAME = "Sideload Watch"'))throw new Error("Bad source");
    const m=src.match(/const APP_VERSION\s*=\s*"([^"]+)"/);if(!m)throw new Error("No version");
    const v=m[1];
    if(cmp(v,APP_VERSION)<=0)return{ok:true,text:`${tx(s,"current")} v${APP_VERSION}`};
    const a=new Alert();a.title=APP_NAME;a.message=`${tx(s,"available")}: v${v}`;a.addAction(tx(s,"apply"));a.addCancelAction(tx(s,"cancel"));
    if(await a.presentAlert()!==0)return{ok:true,text:`v${APP_VERSION} → v${v}`};
    const target=module.filename;if(!target)throw new Error("Current script path unavailable");
    const cloud=FileManager.iCloud(),local=FileManager.local();let targetFm=local;
    if(cloud.fileExists(target)){targetFm=cloud;if(!cloud.isFileDownloaded(target))await cloud.downloadFileFromiCloud(target)}
    else if(!local.fileExists(target))throw new Error("Current script file not found");
    const backup=/\.js$/i.test(target)?target.replace(/\.js$/i,`_backup_v${APP_VERSION}.js`):target+`_backup_v${APP_VERSION}.js`;
    try{targetFm.writeString(backup,targetFm.readString(target))}catch(_){}
    targetFm.writeString(target,src);
    return{ok:true,text:tx(s,"updatedOk")}
  }catch(e){console.log(e);return{ok:false,text:tx(s,"updateFail")}}
}

// ------------------------------------------------------------
// Settings WebView — same visual language as Sports Info /
// LockScreen Generator: hero, cards, nested screens, live preview.
// ------------------------------------------------------------
function nav(screen,icon,title,detail=""){
  return `<div class="navRow" onclick="showScreen('${screen}')"><div class="navLeft"><span class="navIcon">${icon}</span><span>${esc(title)}</span></div><div class="navRight"><span class="navDetail">${esc(detail)}</span><span class="chevron">›</span></div></div>`
}
function settingsHTML(s,catalogResult){
  const L=T[s.language||"en"]||T.en;
  const initialCatalog=catalogResult.data||{sources:[]};
  const catalogMode=catalogResult.online?L.online:L.cached;
  const watchedCount=s.watched.length;
  return `<!doctype html><html lang="${s.language}"><head><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>
:root{color-scheme:dark;--bg:#0b1020;--panel:#111827;--panel2:#172033;--border:#2a3850;--text:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--accent2:#0284c7;--ok:#86efac;--danger:#fb7185;--shadow:0 24px 70px rgba(0,0,0,.45)}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-tap-highlight-color:transparent}
html{background:#070b14}body{padding:calc(14px + env(safe-area-inset-top)) 14px calc(36px + env(safe-area-inset-bottom));max-width:680px;margin:auto;background:radial-gradient(circle at top,#172554 0,#0b1020 42%,#070b14 100%);background-attachment:fixed}
.screen{display:none}.screen.active{display:block}.topbar{display:flex;align-items:center;justify-content:space-between;min-height:42px;margin:0 2px 8px}.back{border:0;background:transparent;color:var(--accent);font:inherit;font-size:16px;font-weight:750;padding:7px 0}
.hero{background:rgba(17,24,39,.96);border:1px solid var(--border);border-radius:22px;padding:22px;margin-bottom:14px;box-shadow:var(--shadow)}.heroTop{display:flex;align-items:center;justify-content:space-between;gap:10px}.eyebrow,.langBadge{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border:1px solid #1d4ed8;border-radius:999px;background:#0f1f46;color:#bfdbfe;font-size:.78rem;font-weight:700}.updateBtn{border:1px solid #1d4ed8;border-radius:999px;background:#0f1f46;color:#bfdbfe;padding:6px 10px;font:inherit;font-size:.78rem;font-weight:800}.updateStatus{min-height:17px;margin-top:8px;color:var(--muted);font-size:11px}.updateStatus.ok{color:var(--ok)}.updateStatus.error{color:var(--danger)}
.hero h1,.screenTitle{font-size:27px;line-height:1.15;margin:14px 0 6px;font-weight:800;letter-spacing:-.45px}.screenTitle{margin:5px 2px 6px}.hero p,.screenSub{color:var(--muted);font-size:14px;line-height:1.5;margin:0}.screenSub{margin:0 2px 14px}.sectionTitle{font-size:11px;color:#9fb3ce;text-transform:uppercase;letter-spacing:.1em;font-weight:800;margin:19px 9px 8px}
.card{background:rgba(17,24,39,.96);border:1px solid var(--border);border-radius:18px;overflow:hidden;margin-bottom:13px;box-shadow:0 12px 34px rgba(0,0,0,.24)}.navRow,.settingRow,.sourceRow,.appRow{min-height:54px;display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-bottom:1px solid rgba(42,56,80,.85)}.navRow:last-child,.settingRow:last-child,.sourceRow:last-child,.appRow:last-child{border-bottom:0}.navRow:active,.sourceRow:active{background:var(--panel2)}
.navLeft{display:flex;gap:11px;align-items:center;font-size:15px;font-weight:700;min-width:0}.navIcon{width:26px;text-align:center;flex:0 0 26px}.navRight{display:flex;align-items:center;gap:8px}.navDetail,.rowDetail{font-size:12px;color:var(--muted)}.navDetail{max-width:190px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.chevron{font-size:23px;color:#64748b}.rowText{min-width:0;padding-right:11px}.rowTitle{font-size:15px;font-weight:650;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.rowDetail{margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.field{padding:12px 14px;border-bottom:1px solid rgba(42,56,80,.85)}.field:last-child{border-bottom:0}.field label{display:block;margin-bottom:7px;color:#dbeafe;font-size:.82rem;font-weight:650}
input[type=text],input[type=search],input[type=number],select,textarea{width:100%;min-height:46px;border:1px solid var(--border);border-radius:12px;background:#0b1220;color:var(--text);padding:0 13px;font:inherit;font-size:15px;outline:none}textarea{min-height:165px;padding:12px;resize:vertical;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;line-height:1.4}input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(56,189,248,.12)}
.colorControl{display:grid;grid-template-columns:58px 1fr;gap:10px;align-items:center}.colorPicker{width:58px;height:46px;border:1px solid var(--border);border-radius:12px;background:#0b1220;padding:4px;overflow:hidden}.colorPicker::-webkit-color-swatch-wrapper{padding:0}.colorPicker::-webkit-color-swatch{border:0;border-radius:8px}.colorCode{text-transform:uppercase;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.switch{position:relative;width:50px;height:30px;flex:0 0 50px}.switch input{display:none}.slider{position:absolute;inset:0;background:#243149;border:1px solid var(--border);border-radius:999px}.slider:before{content:"";position:absolute;width:24px;height:24px;left:2px;top:2px;background:#fff;border-radius:50%;transition:.18s}.switch input:checked+.slider{background:var(--accent2);border-color:var(--accent)}.switch input:checked+.slider:before{transform:translateX(20px)}
.previewGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:13px}.actionGrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px}.previewBtn,.actionBtn{min-height:48px;border:1px solid #1d4ed8;border-radius:13px;background:linear-gradient(135deg,#0369a1,#0284c7);color:#fff;font:inherit;font-weight:800;font-size:13px;touch-action:manipulation}.actionBtn.secondary{background:#243149;border-color:var(--border)}.actionBtn.danger{background:#3a1720;border-color:#6b2738;color:#fecdd3}.actionBtn.full{grid-column:1/-1}
.info{margin:14px 0;padding:12px 14px;border:1px solid var(--border);border-radius:12px;background:var(--panel2);color:#cbd5e1;font-size:.86rem;line-height:1.45}.status{min-height:20px;color:var(--ok);font-size:12px;padding:0 14px 12px}.footer{color:#64748b;text-align:center;font-size:.76rem;margin:16px 4px 0}
.searchBox{margin:0 0 11px}.countPill{font-size:11px;font-weight:800;color:#bfdbfe;background:#0f1f46;border:1px solid #1d4ed8;padding:5px 8px;border-radius:999px;white-space:nowrap}.topbarActions{display:flex;align-items:center;gap:8px}.catalogRefreshBtn{width:32px;height:32px;border:1px solid #1d4ed8;border-radius:999px;background:#0f1f46;color:#38bdf8;font:inherit;font-size:20px;font-weight:700;line-height:1;padding:0;display:grid;place-items:center;touch-action:manipulation}.catalogRefreshBtn:disabled{opacity:.55}.catalogRefreshBtn.spinning{animation:catalogSpin .7s linear infinite}@keyframes catalogSpin{to{transform:rotate(360deg)}}.sourceIcon{width:34px;height:34px;border-radius:9px;background:#0f1f46;display:grid;place-items:center;flex:0 0 34px;font-size:17px}.empty{padding:22px;text-align:center;color:var(--muted);font-size:13px}
.langGrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px}.langBtn{min-height:48px;border:1px solid var(--border);border-radius:13px;background:#243149;color:#fff;font:inherit;font-weight:750}.langBtn.active{border-color:var(--accent);background:#0f1f46;color:#bfdbfe}
@media(max-width:430px){.hero{padding:18px}.navDetail{max-width:128px}.previewGrid{grid-template-columns:1fr}.actionGrid{grid-template-columns:1fr}.actionBtn.full{grid-column:auto}}
</style></head><body>
<div id="home" class="screen active">
  <div class="hero">
    <div class="heroTop"><span class="eyebrow">📲 CaseyCZ · Scriptable</span><button class="updateBtn" onclick="post({action:'update'})">${esc(L.update)}</button></div>
    <h1>${esc(APP_NAME)}</h1>
    <p>${esc(L.subtitle)}</p>
    <div id="updateStatus" class="updateStatus">${esc(L.current)} · v${esc(APP_VERSION)}</div>
  </div>
  <div class="sectionTitle">${esc(L.settings)}</div>
  <div class="card">
    ${nav("sources","📦",L.watched,`${watchedCount} ${L.selected}`)}
    ${nav("preview","👁",L.preview,L.previewDetail)}
    ${nav("appearance","🎨",L.appearance,L.appearanceDetail)}
    ${nav("behavior","⚙️",L.behavior,`${s.refreshMinutes} ${L.minutes}`)}
    ${nav("tools","🧰",L.tools,L.toolsDetail)}
  </div>
  <div class="info"><b>iOS-Hub:</b> <span id="catalogMode">${esc(catalogMode)}</span> · <span id="catalogCount">${initialCatalog.sources.length}</span> sources<br>${esc(L.saveHint)}</div>
  <div class="footer">${esc(APP_NAME)} · v${esc(APP_VERSION)}</div>
</div>

<div id="sources" class="screen">
  <div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><div class="topbarActions"><button id="catalogRefreshBtn" class="catalogRefreshBtn" type="button" title="${esc(L.refreshCatalog)}" aria-label="${esc(L.refreshCatalog)}" onclick="refreshCatalogTop()">↻</button><span id="watchedPill" class="countPill">${watchedCount} ${esc(L.selected)}</span></div></div>
  <div class="screenTitle">${esc(L.sources)}</div><div class="screenSub">${esc(L.sourcesSub)}</div>
  <input id="sourceSearch" class="searchBox" type="search" placeholder="${esc(L.searchSource)}" oninput="renderSources()">
  <div id="sourceList" class="card"></div>
</div>

<div id="apps" class="screen">
  <div class="topbar"><button class="back" onclick="showScreen('sources')">‹ ${esc(L.back)}</button><span id="appsPill" class="countPill"></span></div>
  <div id="appsTitle" class="screenTitle"></div><div id="appsSub" class="screenSub"></div>
  <input id="appSearch" class="searchBox" type="search" placeholder="${esc(L.searchApp)}" oninput="renderApps()">
  <div class="actionGrid" style="padding:0 0 12px"><button class="actionBtn secondary" onclick="selectCurrentSource(true)">${esc(L.selectAll)}</button><button class="actionBtn secondary" onclick="selectCurrentSource(false)">${esc(L.clearAll)}</button></div>
  <div id="appList" class="card"></div>
</div>

<div id="preview" class="screen">
  <div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div>
  <div class="screenTitle">${esc(L.widgetPreview)}</div><div class="screenSub">${esc(L.previewDetail)}</div>
  <div class="sectionTitle">${esc(L.realPreview)}</div>
  <div class="previewGrid"><button class="previewBtn" onclick="preview('small',false)">${esc(L.small)}</button><button class="previewBtn" onclick="preview('medium',false)">${esc(L.medium)}</button><button class="previewBtn" onclick="preview('large',false)">${esc(L.large)}</button></div>
  <div class="sectionTitle">${esc(L.demoPreview)}</div>
  <div class="previewGrid"><button class="previewBtn" onclick="preview('small',true)">${esc(L.small)}</button><button class="previewBtn" onclick="preview('medium',true)">${esc(L.medium)}</button><button class="previewBtn" onclick="preview('large',true)">${esc(L.large)}</button></div>
  <div id="previewStatus" class="status"></div>
</div>

<div id="appearance" class="screen">
  <div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div>
  <div class="screenTitle">${esc(L.appearance)}</div><div class="screenSub">${esc(L.appearanceDetail)}</div>

  <div class="card">
    <div class="field"><label>${esc(L.widgetTitle)}</label><input id="widgetTitle" type="text" maxlength="40" value="${esc(s.widgetTitle||"Sideload Watch")}" oninput="saveAppearance()"></div>
    <div class="field"><label>${esc(L.footerLabel)}</label><div class="rowDetail" style="margin:-2px 0 9px">${esc(L.footerLabelDetail)}</div><input id="footerLabel" type="text" maxlength="40" value="${esc(s.footerLabel||"")}" oninput="saveAppearance()"></div>
  </div>

  <div class="sectionTitle">${esc(L.visibility)}</div>
  <div class="card">
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showNew)}</div></div><span class="switch"><input id="showNew" type="checkbox" ${s.showNew!==false?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showVersion)}</div></div><span class="switch"><input id="showVersion" type="checkbox" ${s.showVersion!==false?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showCount)}</div></div><span class="switch"><input id="showCount" type="checkbox" ${s.showCount!==false?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showTime)}</div></div><span class="switch"><input id="showTime" type="checkbox" ${s.showTime!==false?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
  </div>

  <div class="sectionTitle">${esc(L.customColors)}</div>
  <div class="card">
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.useCustomColors)}</div></div><span class="switch"><input id="useCustomColors" type="checkbox" ${s.useCustomColors?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <div class="field"><label>${esc(L.backgroundColor)}</label><div class="colorControl"><input id="backgroundColorPicker" class="colorPicker" type="color" value="${esc(s.backgroundColor||"#0B1020")}" oninput="syncColorFromPicker('backgroundColor')"><input id="backgroundColor" class="colorCode" type="text" maxlength="7" value="${esc(s.backgroundColor||"#0B1020")}" oninput="syncColorFromText('backgroundColor')"></div></div>
    <div class="field"><label>${esc(L.textColor)}</label><div class="colorControl"><input id="textColorPicker" class="colorPicker" type="color" value="${esc(s.textColor||"#F8FAFC")}" oninput="syncColorFromPicker('textColor')"><input id="textColor" class="colorCode" type="text" maxlength="7" value="${esc(s.textColor||"#F8FAFC")}" oninput="syncColorFromText('textColor')"></div></div>
    <div class="field"><label>${esc(L.mutedColor)}</label><div class="colorControl"><input id="mutedColorPicker" class="colorPicker" type="color" value="${esc(s.mutedColor||"#94A3B8")}" oninput="syncColorFromPicker('mutedColor')"><input id="mutedColor" class="colorCode" type="text" maxlength="7" value="${esc(s.mutedColor||"#94A3B8")}" oninput="syncColorFromText('mutedColor')"></div></div>
    <div class="field"><label>${esc(L.newColor)}</label><div class="colorControl"><input id="newColorPicker" class="colorPicker" type="color" value="${esc(s.newColor||"#34C759")}" oninput="syncColorFromPicker('newColor')"><input id="newColor" class="colorCode" type="text" maxlength="7" value="${esc(s.newColor||"#34C759")}" oninput="syncColorFromText('newColor')"></div></div>
    <div class="field"><label>${esc(L.newBgColor)}</label><div class="colorControl"><input id="newBgColorPicker" class="colorPicker" type="color" value="${esc(s.newBgColor||"#12351E")}" oninput="syncColorFromPicker('newBgColor')"><input id="newBgColor" class="colorCode" type="text" maxlength="7" value="${esc(s.newBgColor||"#12351E")}" oninput="syncColorFromText('newBgColor')"></div></div>
    <div class="field"><label>${esc(L.countColor)}</label><div class="colorControl"><input id="countColorPicker" class="colorPicker" type="color" value="${esc(s.countColor||"#34C759")}" oninput="syncColorFromPicker('countColor')"><input id="countColor" class="colorCode" type="text" maxlength="7" value="${esc(s.countColor||"#34C759")}" oninput="syncColorFromText('countColor')"></div></div>
  </div>

  <div class="actionGrid">
    <button class="actionBtn secondary" onclick="resetAppearance()">↺ ${esc(L.resetAppearance)}</button>
    <button class="actionBtn" onclick="preview('medium',true)">${esc(L.preview)}</button>
  </div>
</div>

<div id="behavior" class="screen">
  <div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div>
  <div class="screenTitle">${esc(L.behavior)}</div>
  <div class="card">
    <div class="field"><label>${esc(L.refresh)}</label><div class="rowDetail" style="margin:-2px 0 9px">${esc(L.refreshDetail)}</div><select id="refreshMinutes" onchange="saveBehavior()">${[15,30,60,120,180].map(n=>`<option value="${n}" ${n===s.refreshMinutes?"selected":""}>${n} ${esc(L.minutes)}</option>`).join("")}</select></div>
  </div>
  <div class="sectionTitle">${esc(L.language)}</div>
  <div class="card"><div class="langGrid">
    <button class="langBtn ${s.language==="cs"?"active":""}" onclick="setLanguage('cs')">🇨🇿 Čeština</button>
    <button class="langBtn ${s.language==="en"?"active":""}" onclick="setLanguage('en')">🇬🇧 English</button>
    <button class="langBtn ${s.language==="de"?"active":""}" onclick="setLanguage('de')">🇩🇪 Deutsch</button>
    <button class="langBtn ${s.language==="es"?"active":""}" onclick="setLanguage('es')">🇪🇸 Español</button>
  </div></div>
  <div class="info">${esc(L.languageDetail)}</div>
</div>

<div id="tools" class="screen">
  <div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div>
  <div class="screenTitle">${esc(L.tools)}</div><div class="screenSub">${esc(L.toolsDetail)}</div>
  <div class="sectionTitle">${esc(L.maintenance)}</div>
  <div class="card">
    <div class="navRow" onclick="post({action:'refreshCatalog'})"><div class="navLeft"><span class="navIcon">🔄</span><div class="rowText"><div class="rowTitle">${esc(L.refreshCatalog)}</div><div class="rowDetail">${esc(L.refreshCatalogDetail)}</div></div></div><span class="chevron">›</span></div>
    <div class="navRow" onclick="post({action:'markSeen'})"><div class="navLeft"><span class="navIcon">✓</span><div class="rowText"><div class="rowTitle">${esc(L.markSeen)}</div><div class="rowDetail">${esc(L.markSeenDetail)}</div></div></div><span class="chevron">›</span></div>
    <div class="navRow" onclick="post({action:'resetBaseline'})"><div class="navLeft"><span class="navIcon">🗑</span><div class="rowText"><div class="rowTitle">${esc(L.resetBaseline)}</div><div class="rowDetail">${esc(L.resetBaselineDetail)}</div></div></div><span class="chevron">›</span></div>
  </div>
  <div class="sectionTitle">JSON</div>
  <div class="card"><div class="field"><textarea id="jsonBox">${esc(JSON.stringify(s,null,2))}</textarea></div><div class="actionGrid"><button class="actionBtn secondary" onclick="post({action:'export'})">${esc(L.export)}</button><button class="actionBtn secondary" onclick="post({action:'import',raw:document.getElementById('jsonBox').value})">${esc(L.import)}</button></div><div id="toolStatus" class="status"></div></div>
</div>

<script>
let state=${JSON.stringify(s)};
let catalog=${JSON.stringify(initialCatalog)};
let currentSourceId=null;
window.__nativeQueue=[];
function post(m){window.__nativeQueue.push({...m,nonce:Date.now()+Math.random()})}
function showScreen(id){document.querySelectorAll('.screen').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');if(id==='sources')renderSources()}
function norm(v){return String(v||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase()}
function key(x){return [x.sourceId||'',x.bundleIdentifier||'',x.name||''].join('|')}
function selectedSet(){return new Set((state.watched||[]).map(key))}
function watchedForSource(id){return(state.watched||[]).filter(x=>x.sourceId===id)}
function sourceObj(id){return(catalog.sources||[]).find(x=>x.id===id)}
function refreshCounts(){
  const n=(state.watched||[]).length;
  const p=document.getElementById('watchedPill');if(p)p.textContent=n+' '+${JSON.stringify(L.selected)};
}
function appKey(src,app){return key({sourceId:src.id,bundleIdentifier:app.bundleIdentifier,name:app.name})}
function saveState(){post({action:'save',settings:state});document.getElementById('jsonBox').value=JSON.stringify(state,null,2);refreshCounts()}
function renderSources(){
  const root=document.getElementById('sourceList'),q=norm(document.getElementById('sourceSearch').value);root.innerHTML='';
  const rows=(catalog.sources||[]).filter(s=>!q||norm(s.name+' '+s.id).includes(q));
  if(!rows.length){root.innerHTML='<div class="empty">'+${JSON.stringify(L.none)}+'</div>';return}
  for(const src of rows){
    const n=watchedForSource(src.id).length,row=document.createElement('div');row.className='sourceRow';row.onclick=()=>openSource(src.id);
    const left=document.createElement('div');left.className='navLeft';
    const icon=document.createElement('div');icon.className='sourceIcon';icon.textContent='📦';
    const txt=document.createElement('div');txt.className='rowText';
    const title=document.createElement('div');title.className='rowTitle';title.textContent=src.name;
    const detail=document.createElement('div');detail.className='rowDetail';detail.textContent=(src.apps||[]).length+' '+${JSON.stringify(L.apps)}+' · '+n+' '+${JSON.stringify(L.selected)};
    txt.append(title,detail);left.append(icon,txt);
    const right=document.createElement('div');right.className='navRight';
    if(n){const pill=document.createElement('span');pill.className='countPill';pill.textContent=String(n);right.appendChild(pill)}
    const ch=document.createElement('span');ch.className='chevron';ch.textContent='›';right.appendChild(ch);
    row.append(left,right);root.appendChild(row)
  }
}
function openSource(id){
  currentSourceId=id;document.getElementById('appSearch').value='';
  const src=sourceObj(id);if(!src)return;
  document.getElementById('appsTitle').textContent=src.name;
  document.getElementById('appsSub').textContent=(src.apps||[]).length+' '+${JSON.stringify(L.apps)};
  showScreen('apps');renderApps()
}
function renderApps(){
  const src=sourceObj(currentSourceId),root=document.getElementById('appList');if(!src)return;
  const set=selectedSet(),q=norm(document.getElementById('appSearch').value),rows=(src.apps||[]).filter(a=>!q||norm(a.name+' '+a.bundleIdentifier+' '+a.version).includes(q));
  root.innerHTML='';document.getElementById('appsPill').textContent=watchedForSource(src.id).length+' '+${JSON.stringify(L.selected)};
  if(!rows.length){root.innerHTML='<div class="empty">'+${JSON.stringify(L.none)}+'</div>';return}
  for(const app of rows){
    const item={sourceId:src.id,bundleIdentifier:app.bundleIdentifier||'',name:app.name,sourceURL:src.sourceURL||''},k=key(item);
    const row=document.createElement('label');row.className='appRow';
    const text=document.createElement('div');text.className='rowText';
    const title=document.createElement('div');title.className='rowTitle';title.textContent=app.name;
    const detail=document.createElement('div');detail.className='rowDetail';detail.textContent='v'+(app.version||'—')+(app.bundleIdentifier?' · '+app.bundleIdentifier:'');
    text.append(title,detail);
    const sw=document.createElement('span');sw.className='switch';
    const input=document.createElement('input');input.type='checkbox';input.checked=set.has(k);
    const slider=document.createElement('span');slider.className='slider';
    input.onchange=()=>toggleApp(item,input.checked);
    sw.append(input,slider);row.append(text,sw);root.appendChild(row)
  }
}
function toggleApp(item,on){
  const k=key(item),arr=(state.watched||[]).filter(x=>key(x)!==k);if(on)arr.push(item);state.watched=arr;saveState();renderSources();renderApps()
}
function selectCurrentSource(on){
  const src=sourceObj(currentSourceId);if(!src)return;
  const other=(state.watched||[]).filter(x=>x.sourceId!==src.id);
  state.watched=on?other.concat((src.apps||[]).map(a=>({sourceId:src.id,bundleIdentifier:a.bundleIdentifier||'',name:a.name,sourceURL:src.sourceURL||''}))):other;
  saveState();renderSources();renderApps()
}
function saveBehavior(){state.refreshMinutes=Number(document.getElementById('refreshMinutes').value)||30;saveState()}
function enableCustomColors(){
  const toggle=document.getElementById('useCustomColors');
  if(toggle){toggle.checked=true;state.useCustomColors=true}
}
function syncColorFromPicker(id){
  const picker=document.getElementById(id+'Picker'),text=document.getElementById(id);
  if(!picker||!text)return;
  text.value=picker.value.toUpperCase();
  enableCustomColors();
  saveAppearance()
}
function syncColorFromText(id){
  const text=document.getElementById(id),picker=document.getElementById(id+'Picker');
  if(!text||!picker)return;
  let v=String(text.value||"").trim().toUpperCase();
  if(v&&!v.startsWith('#'))v='#'+v;
  text.value=v;
  if(/^#[0-9A-F]{6}$/.test(v)){
    picker.value=v;
    enableCustomColors();
    saveAppearance()
  }
}
function saveAppearance(){
  state.widgetTitle=document.getElementById('widgetTitle').value||"Sideload Watch";
  state.footerLabel=document.getElementById('footerLabel').value||"";
  state.showNew=document.getElementById('showNew').checked;
  state.showVersion=document.getElementById('showVersion').checked;
  state.showCount=document.getElementById('showCount').checked;
  state.showTime=document.getElementById('showTime').checked;
  state.useCustomColors=document.getElementById('useCustomColors').checked;
  const colorDefaults={backgroundColor:"#0B1020",textColor:"#F8FAFC",mutedColor:"#94A3B8",newColor:"#34C759",newBgColor:"#12351E",countColor:"#34C759"};
  for(const id of Object.keys(colorDefaults)){
    let v=String(document.getElementById(id).value||"").trim().toUpperCase();
    if(v&&!v.startsWith("#"))v="#"+v;
    if(/^#[0-9A-F]{6}$/.test(v))state[id]=v;
    else if(!state[id])state[id]=colorDefaults[id]
  }
  saveState()
}
function resetAppearance(){
  state.widgetTitle="Sideload Watch";
  state.footerLabel="";
  state.showNew=true;
  state.showVersion=true;
  state.showCount=true;
  state.showTime=true;
  state.useCustomColors=false;
  state.backgroundColor="#0B1020";
  state.textColor="#F8FAFC";
  state.mutedColor="#94A3B8";
  state.newColor="#34C759";
  state.newBgColor="#12351E";
  state.countColor="#34C759";
  saveState();
  post({action:'reload',settings:state})
}
function setLanguage(l){state.language=l;document.querySelectorAll('.langBtn').forEach(b=>b.classList.remove('active'));const map={cs:0,en:1,de:2,es:3},buttons=document.querySelectorAll('.langBtn');if(buttons[map[l]])buttons[map[l]].classList.add('active');saveState();post({action:'language',language:l})}
function preview(family,demo){document.getElementById('previewStatus').textContent='…';post({action:'preview',family,demo,settings:state})}
function refreshCatalogTop(){
  const b=document.getElementById('catalogRefreshBtn');
  if(b){b.disabled=true;b.classList.add('spinning')}
  post({action:'refreshCatalog'})
}
function finishCatalogRefresh(){
  const b=document.getElementById('catalogRefreshBtn');
  if(b){b.disabled=false;b.classList.remove('spinning')}
}
window.__native=function(m){
  if(!m)return;
  if(m.action==='catalog'){catalog=m.catalog||{sources:[]};document.getElementById('catalogMode').textContent=m.online?${JSON.stringify(L.online)}:${JSON.stringify(L.cached)};document.getElementById('catalogCount').textContent=(catalog.sources||[]).length;renderSources();if(currentSourceId&&sourceObj(currentSourceId))renderApps();finishCatalogRefresh();const e=document.getElementById('toolStatus');if(e)e.textContent=m.text||''}
  if(m.action==='status'){finishCatalogRefresh();const e=document.getElementById('toolStatus');if(e)e.textContent=m.text||''}
  if(m.action==='previewDone'){document.getElementById('previewStatus').textContent=''}
  if(m.action==='update'){const e=document.getElementById('updateStatus');e.textContent=m.text||'';e.className='updateStatus '+(m.ok?'ok':'error')}
  if(m.action==='replace'){state=m.settings||state;document.getElementById('jsonBox').value=JSON.stringify(state,null,2);location.reload()}
};
renderSources();refreshCounts();
</script></body></html>`
}
async function send(web,o){try{await web.evaluateJavaScript(`window.__native(${JSON.stringify(o)})`,false)}catch(_){}}

async function settings(s){
  let catalogResult;
  try{catalogResult=await fetchCatalog()}catch(e){catalogResult={data:{sources:[]},online:false,cached:false,error:String(e)}}
  s=enrichWatchedSources(s,catalogResult.data);
  saveSettings(s);
  const web=new WebView();await web.loadHTML(settingsHTML(s,catalogResult));
  let dismissed=false,cur=merge(s);
  const presentPromise=web.present(false).then(()=>{dismissed=true});
  const sleep=ms=>new Promise(resolve=>Timer.schedule(ms,false,resolve));

  while(!dismissed){
    await sleep(160);if(dismissed)break;
    let raw=null;try{raw=await web.evaluateJavaScript("JSON.stringify(window.__nativeQueue.shift()||null)")}catch(_){if(dismissed)break;continue}
    if(!raw||raw==="null")continue;
    let m=null;try{m=JSON.parse(raw)}catch(_){continue}
    if(!m?.action)continue;
    try{
      if(m.action==="save"){
        cur=merge(m.settings);saveSettings(cur)
      }else if(m.action==="preview"){
        cur=merge(m.settings||cur);saveSettings(cur);
        const family=["small","medium","large"].includes(m.family)?m.family:"medium";
        const status=m.demo?demoStatus():await getLiveStatus(cur),w=await buildWidget(status,cur,family);
        try{await presentWidget(w,family)}finally{await send(web,{action:"previewDone"})}
      }else if(m.action==="refreshCatalog"){
        try{
          const r=await fetchCatalog(true);catalogResult=r;
          cur=enrichWatchedSources(cur,r.data);saveSettings(cur);
          await send(web,{action:"catalog",catalog:r.data,online:r.online,text:tx(cur,"catalogUpdated")})
        }catch(e){await send(web,{action:"status",text:tx(cur,"catalogFail")})}
      }else if(m.action==="markSeen"){
        const n=await markAllSeen(cur);await send(web,{action:"status",text:`${tx(cur,"done")} · ${n}`})
      }else if(m.action==="resetBaseline"){
        resetState();await send(web,{action:"status",text:tx(cur,"resetDone")})
      }else if(m.action==="export"){
        Pasteboard.copyString(JSON.stringify(cur,null,2));await send(web,{action:"status",text:tx(cur,"copied")})
      }else if(m.action==="import"){
        try{
          const imported=merge(JSON.parse(m.raw||""));if(!imported.language)imported.language=cur.language||lang();
          cur=imported;saveSettings(cur);await send(web,{action:"status",text:tx(cur,"imported")})
        }catch(_){await send(web,{action:"status",text:tx(cur,"invalid")})}
      }else if(m.action==="language"){
        cur.language=["cs","en","de","es"].includes(m.language)?m.language:cur.language;saveSettings(cur)
      }else if(m.action==="reload"){
        cur=merge(m.settings||cur);saveSettings(cur);await web.loadHTML(settingsHTML(cur,catalogResult))
      }else if(m.action==="update"){
        cur=merge(cur);saveSettings(cur);const r=await updater(cur);await send(web,{action:"update",ok:r.ok,text:r.text})
      }
    }catch(e){console.log(e);await send(web,{action:"status",text:String(e)})}
  }
  try{await presentPromise}catch(_){}
  return cur
}

let SETTINGS=await firstLanguage(loadSettings());

if(config.runsInWidget){
  const fam=config.widgetFamily||"medium";
  try{
    await widget(SETTINGS,fam);
  }catch(e){
    console.log("Widget error: "+e);
    Script.setWidget(buildErrorWidget(SETTINGS,e));
  }
}else{
  SETTINGS=await settings(SETTINGS);
}
Script.complete();
