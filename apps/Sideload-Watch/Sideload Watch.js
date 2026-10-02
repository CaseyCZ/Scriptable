// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: download;
// ============================================================
// Sideload Watch v0.3.1
// CaseyCZ Scriptable Apps
// Watches selected apps from selected iOS-Hub sources.
// Settings UI follows the LockScreen Generator / Sports Info style.
// ============================================================

const APP_NAME = "Sideload Watch";
const APP_VERSION = "0.3.1";
const SETTINGS_FILE = "SideloadWatch_settings.json";
const STATE_FILE = "SideloadWatch_state.json";
const CATALOG_CACHE_FILE = "SideloadWatch_catalog.json";
const CATALOG_URL = "https://raw.githubusercontent.com/CaseyCZ/iOS-Hub/main/data/catalog.json";
const HUB_URL = "https://caseycz.github.io/iOS-Hub/";
const UPDATE_SOURCE_URL = "https://raw.githubusercontent.com/CaseyCZ/Scriptable/Master/apps/Sideload-Watch/Sideload%20Watch.js";
const UPDATE_MIN_BYTES = 12000;
const UPDATE_ENABLED = true;
const API_TIMEOUT = 12;

const DEFAULTS = {
  language: null,
  selectedSources: [],
  watchedApps: [],
  refreshMinutes: 30,
  widgetTitle: "Sideload Watch",
  footerLabel: "",
  showHeaderIcon: true,
  showTitle: true,
  showNewBadge: true,
  showVersion: true,
  showUpdateCount: true,
  showCheckedTime: true,
  useCustomColors: false,
  backgroundColor: "#0B1020",
  textColor: "#F8FAFC",
  secondaryTextColor: "#94A3B8",
  iconColor: "#0A84FF",
  newTextColor: "#34C759",
  newBackgroundColor: "#12351E",
  countColor: "#34C759",
  errorColor: "#FF453A",
};

const LANGS = [
  ["cs", "🇨🇿 Čeština"],
  ["en", "🇬🇧 English"],
  ["de", "🇩🇪 Deutsch"],
  ["es", "🇪🇸 Español"],
];

const UI = {
  cs: {
    subtitle: "Sleduj nové verze aplikací z vybraných iOS-Hub source.",
    sources: "Sources", apps: "Aplikace", tracking: "Sledování",
    sourcesDetail: "Vyber source, které chceš sledovat.",
    appsDetail: "V každém vybraném source zvol konkrétní aplikace.",
    preview: "Náhled widgetu", previewSub: "Vzhled widgetu zůstává stejný; tady ho můžeš jen otestovat.",
    real: "Reálný", demo: "Demo · 7 NEW", settings: "Nastavení", language: "Jazyk", appearance: "Vzhled widgetu", appearanceDetail: "Název, popisek, viditelnost prvků a barvy.", widgetTitle: "Název widgetu", footerLabel: "Vlastní spodní popisek", footerLabelDetail: "Nech prázdné pro automatický text podle jazyka.", showHeaderIcon: "Zobrazit ikonu", showTitle: "Zobrazit název", showNewBadge: "Zobrazit NEW", showVersion: "Zobrazit verzi", showUpdateCount: "Zobrazit počet aktualizací", showCheckedTime: "Zobrazit čas kontroly", useCustomColors: "Použít vlastní barvy", colors: "Barvy", backgroundColor: "Pozadí", textColor: "Hlavní text", secondaryTextColor: "Vedlejší text / verze", iconColor: "Ikona", newTextColor: "Text NEW", newBackgroundColor: "Pozadí NEW", countColor: "Počet aktualizací", errorColor: "Offline / chyba", resetAppearance: "Obnovit výchozí vzhled",
    refresh: "Obnova widgetu", minutes: "min", tools: "Nástroje",
    markSeen: "Označit vše jako přečtené", markSeenDetail: "Aktuální verze se uloží jako výchozí stav.",
    resetVersions: "Reset historie verzí", resetVersionsDetail: "Při další kontrole se vytvoří nový výchozí stav.",
    update: "Aktualizace", current: "Aktuální", available: "Dostupná verze", apply: "Aktualizovat", cancel: "Zrušit",
    updateTest: "Aktualizace se aktivují po přidání Sideload Watch do repozitáře.", updateFail: "Kontrola aktualizace selhala.", updatedOk: "Aktualizace nainstalována. Skript spusť znovu.",
    back: "Zpět", searchSources: "Hledat source…", searchApps: "Hledat aplikaci…", selected: "vybráno",
    noSources: "Nejdřív vyber alespoň jeden source.", noApps: "V tomto source nejsou aplikace.",
    selectAll: "Vybrat vše", clearAll: "Zrušit vše", saved: "Uloženo", done: "Hotovo",
    diagnostics: "Stav dat", catalogOnline: "iOS-Hub katalog je dostupný", catalogCache: "Používá se uložený katalog", catalogFail: "Katalog se nepodařilo načíst",
    trackedCount: n => `${n} ${n === 1 ? "aplikace" : (n >= 2 && n <= 4 ? "aplikace" : "aplikací")}`,
    sourceCount: n => `${n} ${n === 1 ? "source" : "sources"}`,
    updates: n => `${n} ${n === 1 ? "aktualizace" : (n >= 2 && n <= 4 ? "aktualizace" : "aktualizací")}`,
    upToDate: "Všechno je aktuální", noneSelected: "Nejsou vybrané aplikace", offline: "offline",
    markResult: n => `Uloženo ${n} aktuálních verzí.`, resetDone: "Historie verzí byla resetována.",
  },
  en: {
    subtitle: "Watch new app versions from selected iOS-Hub sources.",
    sources: "Sources", apps: "Apps", tracking: "Tracking",
    sourcesDetail: "Choose the sources you want to watch.", appsDetail: "Choose specific apps inside each selected source.",
    preview: "Widget preview", previewSub: "The widget design stays unchanged; preview it here.",
    real: "Real", demo: "Demo · 7 NEW", settings: "Settings", language: "Language", appearance: "Widget appearance", appearanceDetail: "Title, label, element visibility and colors.", widgetTitle: "Widget title", footerLabel: "Custom footer label", footerLabelDetail: "Leave empty for the automatic localized text.", showHeaderIcon: "Show icon", showTitle: "Show title", showNewBadge: "Show NEW", showVersion: "Show version", showUpdateCount: "Show update count", showCheckedTime: "Show checked time", useCustomColors: "Use custom colors", colors: "Colors", backgroundColor: "Background", textColor: "Primary text", secondaryTextColor: "Secondary text / version", iconColor: "Icon", newTextColor: "NEW text", newBackgroundColor: "NEW background", countColor: "Update count", errorColor: "Offline / error", resetAppearance: "Reset default appearance",
    refresh: "Widget refresh", minutes: "min", tools: "Tools",
    markSeen: "Mark all as seen", markSeenDetail: "Current versions become the new baseline.",
    resetVersions: "Reset version history", resetVersionsDetail: "A new baseline will be created on the next check.",
    update: "Update", current: "Current", available: "Available version", apply: "Update", cancel: "Cancel",
    updateTest: "Updates will be enabled after Sideload Watch is added to the repository.", updateFail: "Update check failed.", updatedOk: "Update installed. Run the script again.",
    back: "Back", searchSources: "Search sources…", searchApps: "Search apps…", selected: "selected",
    noSources: "Select at least one source first.", noApps: "There are no apps in this source.", selectAll: "Select all", clearAll: "Clear all", saved: "Saved", done: "Done",
    diagnostics: "Data status", catalogOnline: "iOS-Hub catalog is available", catalogCache: "Using cached catalog", catalogFail: "Could not load catalog",
    trackedCount: n => `${n} app${n === 1 ? "" : "s"}`, sourceCount: n => `${n} source${n === 1 ? "" : "s"}`,
    updates: n => `${n} update${n === 1 ? "" : "s"} available`, upToDate: "Everything is up to date", noneSelected: "No apps selected", offline: "offline",
    markResult: n => `Saved ${n} current versions.`, resetDone: "Version history was reset.",
  },
  de: {
    subtitle: "Neue App-Versionen aus ausgewählten iOS-Hub-Quellen überwachen.",
    sources: "Sources", apps: "Apps", tracking: "Überwachung", sourcesDetail: "Wähle die Sources, die du überwachen möchtest.", appsDetail: "Wähle in jeder Source die gewünschten Apps.",
    preview: "Widget-Vorschau", previewSub: "Das Widget-Design bleibt unverändert; hier kannst du es testen.", real: "Echt", demo: "Demo · 7 NEW", settings: "Einstellungen", language: "Sprache", appearance: "Widget-Aussehen", appearanceDetail: "Titel, Beschriftung, sichtbare Elemente und Farben.", widgetTitle: "Widget-Titel", footerLabel: "Eigene Fußzeile", footerLabelDetail: "Leer lassen für den automatisch lokalisierten Text.", showHeaderIcon: "Symbol anzeigen", showTitle: "Titel anzeigen", showNewBadge: "NEW anzeigen", showVersion: "Version anzeigen", showUpdateCount: "Update-Anzahl anzeigen", showCheckedTime: "Prüfzeit anzeigen", useCustomColors: "Eigene Farben verwenden", colors: "Farben", backgroundColor: "Hintergrund", textColor: "Haupttext", secondaryTextColor: "Sekundärtext / Version", iconColor: "Symbol", newTextColor: "NEW-Text", newBackgroundColor: "NEW-Hintergrund", countColor: "Update-Anzahl", errorColor: "Offline / Fehler", resetAppearance: "Standard-Aussehen wiederherstellen",
    refresh: "Widget-Aktualisierung", minutes: "Min", tools: "Werkzeuge", markSeen: "Alles als gesehen markieren", markSeenDetail: "Aktuelle Versionen werden als Ausgangsstand gespeichert.",
    resetVersions: "Versionsverlauf zurücksetzen", resetVersionsDetail: "Beim nächsten Prüfen wird ein neuer Ausgangsstand erstellt.", update: "Update", current: "Aktuell", available: "Verfügbare Version", apply: "Aktualisieren", cancel: "Abbrechen",
    updateTest: "Updates werden aktiviert, sobald Sideload Watch im Repository liegt.", updateFail: "Update-Prüfung fehlgeschlagen.", updatedOk: "Update installiert. Skript erneut starten.", back: "Zurück",
    searchSources: "Sources suchen…", searchApps: "Apps suchen…", selected: "ausgewählt", noSources: "Wähle zuerst mindestens eine Source.", noApps: "Keine Apps in dieser Source.", selectAll: "Alle auswählen", clearAll: "Alle abwählen", saved: "Gespeichert", done: "Fertig",
    diagnostics: "Datenstatus", catalogOnline: "iOS-Hub-Katalog ist erreichbar", catalogCache: "Gespeicherter Katalog wird verwendet", catalogFail: "Katalog konnte nicht geladen werden",
    trackedCount: n => `${n} App${n === 1 ? "" : "s"}`, sourceCount: n => `${n} Source${n === 1 ? "" : "s"}`, updates: n => `${n} Update${n === 1 ? "" : "s"}`,
    upToDate: "Alles ist aktuell", noneSelected: "Keine Apps ausgewählt", offline: "offline", markResult: n => `${n} aktuelle Versionen gespeichert.`, resetDone: "Versionsverlauf wurde zurückgesetzt.",
  },
  es: {
    subtitle: "Controla nuevas versiones de apps de las fuentes elegidas de iOS-Hub.",
    sources: "Sources", apps: "Apps", tracking: "Seguimiento", sourcesDetail: "Elige las sources que quieres seguir.", appsDetail: "Elige aplicaciones concretas dentro de cada source.",
    preview: "Vista previa", previewSub: "El diseño del widget no cambia; puedes probarlo aquí.", real: "Real", demo: "Demo · 7 NEW", settings: "Ajustes", language: "Idioma", appearance: "Apariencia del widget", appearanceDetail: "Título, etiqueta, visibilidad de elementos y colores.", widgetTitle: "Título del widget", footerLabel: "Etiqueta inferior personalizada", footerLabelDetail: "Déjalo vacío para usar el texto automático según el idioma.", showHeaderIcon: "Mostrar icono", showTitle: "Mostrar título", showNewBadge: "Mostrar NEW", showVersion: "Mostrar versión", showUpdateCount: "Mostrar número de actualizaciones", showCheckedTime: "Mostrar hora de comprobación", useCustomColors: "Usar colores personalizados", colors: "Colores", backgroundColor: "Fondo", textColor: "Texto principal", secondaryTextColor: "Texto secundario / versión", iconColor: "Icono", newTextColor: "Texto NEW", newBackgroundColor: "Fondo NEW", countColor: "Número de actualizaciones", errorColor: "Offline / error", resetAppearance: "Restablecer apariencia",
    refresh: "Actualización del widget", minutes: "min", tools: "Herramientas", markSeen: "Marcar todo como visto", markSeenDetail: "Las versiones actuales se guardarán como referencia.",
    resetVersions: "Restablecer historial", resetVersionsDetail: "En la próxima comprobación se creará una nueva referencia.", update: "Actualización", current: "Actual", available: "Versión disponible", apply: "Actualizar", cancel: "Cancelar",
    updateTest: "Las actualizaciones se activarán cuando Sideload Watch esté en el repositorio.", updateFail: "Falló la comprobación de actualización.", updatedOk: "Actualización instalada. Ejecuta el script de nuevo.", back: "Atrás",
    searchSources: "Buscar sources…", searchApps: "Buscar apps…", selected: "seleccionadas", noSources: "Primero elige al menos una source.", noApps: "No hay apps en esta source.", selectAll: "Seleccionar todo", clearAll: "Quitar todo", saved: "Guardado", done: "Hecho",
    diagnostics: "Estado de datos", catalogOnline: "El catálogo iOS-Hub está disponible", catalogCache: "Usando catálogo guardado", catalogFail: "No se pudo cargar el catálogo",
    trackedCount: n => `${n} app${n === 1 ? "" : "s"}`, sourceCount: n => `${n} source${n === 1 ? "" : "s"}`, updates: n => `${n} actualización${n === 1 ? "" : "es"}`,
    upToDate: "Todo está actualizado", noneSelected: "No hay apps seleccionadas", offline: "offline", markResult: n => `${n} versiones actuales guardadas.`, resetDone: "Se restableció el historial de versiones.",
  },
};

const fm = FileManager.local();
const settingsPath = fm.joinPath(fm.documentsDirectory(), SETTINGS_FILE);
const statePath = fm.joinPath(fm.documentsDirectory(), STATE_FILE);
const catalogCachePath = fm.joinPath(fm.cacheDirectory(), CATALOG_CACHE_FILE);

function deviceLang() {
  const l = String(Device.locale() || "en").slice(0, 2).toLowerCase();
  return ["cs", "en", "de", "es"].includes(l) ? l : "en";
}
function t(s, key) {
  const l = s.language || deviceLang();
  return (UI[l] || UI.en)[key] ?? UI.en[key] ?? key;
}
function clone(o) { return JSON.parse(JSON.stringify(o)); }
function mergeSettings(raw) {
  const input = raw || {};
  const s = Object.assign(clone(DEFAULTS), input);
  if (!["cs", "en", "de", "es"].includes(s.language)) s.language = null;
  s.selectedSources = Array.from(new Set(Array.isArray(s.selectedSources) ? s.selectedSources.map(String) : []));
  s.watchedApps = Array.isArray(s.watchedApps) ? s.watchedApps.filter(x => x && x.sourceId && x.bundle && x.appName).map(x => ({
    sourceId: String(x.sourceId), bundle: String(x.bundle), appName: String(x.appName), label: String(x.label || x.appName),
  })) : [];
  s.watchedApps = s.watchedApps.filter(x => s.selectedSources.includes(x.sourceId));
  s.refreshMinutes = Math.max(15, Math.min(120, Number(s.refreshMinutes) || 30));
  s.widgetTitle = String(s.widgetTitle ?? DEFAULTS.widgetTitle).slice(0, 40);
  s.footerLabel = String(s.footerLabel ?? "").slice(0, 40);
  for (const k of ["showHeaderIcon","showTitle","showNewBadge","showVersion","showUpdateCount","showCheckedTime","useCustomColors"]) s[k] = s[k] === true || (s[k] !== false && DEFAULTS[k] === true);
  for (const k of ["backgroundColor","textColor","secondaryTextColor","iconColor","newTextColor","newBackgroundColor","countColor","errorColor"]) {
    if (!/^#[0-9a-fA-F]{6}$/.test(String(s[k] || ""))) s[k] = DEFAULTS[k];
  }
  return s;
}
function loadSettings() {
  try { if (fm.fileExists(settingsPath)) return mergeSettings(JSON.parse(fm.readString(settingsPath))); } catch (e) { console.log(e); }
  return clone(DEFAULTS);
}
function saveSettings(s) {
  try { fm.writeString(settingsPath, JSON.stringify(mergeSettings(s), null, 2)); } catch (e) { console.log(e); }
}
async function firstLanguage(s) {
  if (s.language) return s;
  if (config.runsInWidget) { s.language = deviceLang(); saveSettings(s); return s; }
  const a = new Alert();
  a.title = APP_NAME;
  a.message = "Choose language / Vyber jazyk";
  LANGS.forEach(([, label]) => a.addAction(label));
  const i = await a.presentAlert();
  s.language = LANGS[Math.max(0, i)]?.[0] || "en";
  saveSettings(s);
  return s;
}

function loadState() {
  try {
    if (!fm.fileExists(statePath)) return { seen: {}, lastCurrent: {}, updatedAt: null };
    const p = JSON.parse(fm.readString(statePath));
    return { seen: p.seen || {}, lastCurrent: p.lastCurrent || {}, updatedAt: p.updatedAt || null };
  } catch (_) { return { seen: {}, lastCurrent: {}, updatedAt: null }; }
}
function saveState(s) { fm.writeString(statePath, JSON.stringify(s, null, 2)); }
function resetState() { if (fm.fileExists(statePath)) fm.remove(statePath); }
function appKey(x) { return `${x.sourceId}|${x.bundle}|${x.appName}`; }

async function requestJSON(url) {
  const r = new Request(url); r.timeoutInterval = API_TIMEOUT; return await r.loadJSON();
}
async function loadCatalogWithStatus() {
  try {
    const data = await requestJSON(CATALOG_URL);
    if (!data || !Array.isArray(data.sources)) throw new Error("Invalid catalog");
    try { fm.writeString(catalogCachePath, JSON.stringify(data)); } catch (_) {}
    return { catalog: data, mode: "online", error: null };
  } catch (e) {
    try {
      if (fm.fileExists(catalogCachePath)) {
        const data = JSON.parse(fm.readString(catalogCachePath));
        if (data && Array.isArray(data.sources)) return { catalog: data, mode: "cache", error: String(e) };
      }
    } catch (_) {}
    return { catalog: { sources: [] }, mode: "error", error: String(e) };
  }
}
function compactCatalog(catalog) {
  return (catalog.sources || []).map(src => ({
    id: String(src.id || ""), name: String(src.name || src.id || "Source"), iconURL: String(src.iconURL || ""),
    apps: (src.apps || []).map((app, index) => ({
      id: `${src.id}|${app.bundleIdentifier || ""}|${app.name || ""}|${index}`,
      name: String(app.name || "App"), bundle: String(app.bundleIdentifier || ""), version: String(app.version || "—"), iconURL: String(app.iconURL || ""),
    })),
  })).filter(x => x.id);
}
function resolveWatched(catalog, settings) {
  const bySource = new Map((catalog.sources || []).map(src => [String(src.id), src]));
  const out = [];
  for (const w of settings.watchedApps || []) {
    const src = bySource.get(w.sourceId); if (!src) continue;
    const apps = Array.isArray(src.apps) ? src.apps : [];
    let app = apps.find(a => String(a.bundleIdentifier || "") === w.bundle && String(a.name || "") === w.appName);
    if (!app) app = apps.find(a => String(a.bundleIdentifier || "") === w.bundle);
    if (!app) continue;
    out.push({ key: appKey(w), sourceId: w.sourceId, name: w.label || app.name, appName: String(app.name || w.appName), bundle: w.bundle, version: String(app.version || "—"), iconURL: app.iconURL || src.iconURL || "" });
  }
  return out;
}
async function getRealStatus(settings) {
  const state = loadState();
  if (!(settings.watchedApps || []).length) return { updates: [], total: 0, current: [], checkedAt: new Date(), offline: false, emptySelection: true };
  const loaded = await loadCatalogWithStatus();
  const current = resolveWatched(loaded.catalog, settings);
  let changed = false;
  for (const app of current) {
    if (!state.seen[app.key]) { state.seen[app.key] = app.version; changed = true; }
    state.lastCurrent[app.key] = { name: app.name, version: app.version, iconURL: app.iconURL };
  }
  state.updatedAt = new Date().toISOString();
  if (changed || current.length) saveState(state);
  const updates = current.filter(app => state.seen[app.key] !== app.version);
  if (loaded.mode === "error") {
    const cached = [];
    for (const w of settings.watchedApps) {
      const key = appKey(w), now = state.lastCurrent[key];
      if (now && state.seen[key] && now.version !== state.seen[key]) cached.push({ key, name: now.name || w.label, version: now.version, iconURL: now.iconURL || "" });
    }
    return { updates: cached, total: cached.length, current: [], checkedAt: state.updatedAt ? new Date(state.updatedAt) : null, offline: true, error: loaded.error };
  }
  return { updates, total: updates.length, current, checkedAt: new Date(), offline: loaded.mode !== "online", cache: loaded.mode === "cache" };
}
async function markAllSeen(settings) {
  const loaded = await loadCatalogWithStatus();
  if (!loaded.catalog.sources.length) throw new Error(loaded.error || "Catalog unavailable");
  const current = resolveWatched(loaded.catalog, settings), state = loadState();
  for (const app of current) { state.seen[app.key] = app.version; state.lastCurrent[app.key] = { name: app.name, version: app.version, iconURL: app.iconURL }; }
  state.updatedAt = new Date().toISOString(); saveState(state); return current.length;
}
function demoStatus() {
  const demo = [
    { name: "Stremio", version: "2.0.9" }, { name: "YouTubeRebornPlus", version: "20.06.1" }, { name: "Yattee", version: "2.1.0" },
    { name: "SideStore", version: "0.6.3" }, { name: "UTM", version: "4.8.0" }, { name: "Provenance", version: "3.4.0" }, { name: "VortX", version: "0.5.0" },
  ];
  return { updates: demo, total: demo.length, checkedAt: new Date(), offline: false, demo: true };
}

// Widget rendering intentionally kept visually identical to the first test build.
function widgetColors(settings) {
  if (!settings.useCustomColors) {
    return {
      bg: Color.dynamic(new Color("F5F7FB"), new Color("0B1020")), panel: Color.dynamic(new Color("FFFFFF"), new Color("111827")),
      text: Color.dynamic(new Color("111827"), new Color("F8FAFC")), muted: Color.dynamic(new Color("6B7280"), new Color("94A3B8")),
      border: Color.dynamic(new Color("E5E7EB"), new Color("263449")), green: new Color("34C759"), greenSoft: Color.dynamic(new Color("E8F8ED"), new Color("12351E")),
      count: new Color("34C759"), red: new Color("FF453A"), blue: new Color("0A84FF"),
    };
  }
  return {
    bg: new Color(settings.backgroundColor), panel: new Color(settings.backgroundColor),
    text: new Color(settings.textColor), muted: new Color(settings.secondaryTextColor),
    border: new Color(settings.secondaryTextColor), green: new Color(settings.newTextColor), greenSoft: new Color(settings.newBackgroundColor),
    count: new Color(settings.countColor), red: new Color(settings.errorColor), blue: new Color(settings.iconColor),
  };
}
function layoutForFamily(family) {
  if (family === "small") return { maxRows: 2, title: 14, row: 11, version: 10, footer: 9, pad: 11, rowGap: 5 };
  if (family === "large") return { maxRows: 9, title: 17, row: 14, version: 12, footer: 11, pad: 15, rowGap: 7 };
  return { maxRows: 4, title: 16, row: 13, version: 11, footer: 10, pad: 13, rowGap: 6 };
}
function widgetText(settings) {
  const l = settings.language || deviceLang(), U = UI[l] || UI.en;
  const updates = n => String(settings.footerLabel || "").trim() ? `${n} ${String(settings.footerLabel).trim()}` : U.updates(n);
  return { title: settings.widgetTitle || APP_NAME, new: "NEW", updates, upToDate: U.upToDate, noneSelected: U.noneSelected, offline: U.offline };
}
function addNewBadge(stack, c, fontSize) {
  const badge = stack.addStack(); badge.backgroundColor = c.greenSoft; badge.cornerRadius = 5; badge.setPadding(2, 5, 2, 5);
  const x = badge.addText("NEW"); x.font = Font.boldSystemFont(fontSize); x.textColor = c.green; x.lineLimit = 1;
}
function formatTime(date) {
  if (!date || isNaN(date.getTime())) return "—";
  const f = new DateFormatter(); f.locale = Device.locale(); f.useNoDateStyle(); f.useShortTimeStyle(); return f.string(date);
}
async function buildWidget(status, settings, familyOverride) {
  const family = familyOverride || config.widgetFamily || "medium", L = layoutForFamily(family), c = widgetColors(settings), T = widgetText(settings), w = new ListWidget();
  w.backgroundColor = c.bg; w.setPadding(L.pad, L.pad, L.pad, L.pad); w.url = HUB_URL;
  if (settings.showHeaderIcon || settings.showTitle || status.demo) {
    const header = w.addStack(); header.centerAlignContent();
    if (settings.showHeaderIcon) {
      const symbol = SFSymbol.named("arrow.triangle.2.circlepath"); symbol.applyFont(Font.semiboldSystemFont(L.title));
      const icon = header.addImage(symbol.image); icon.imageSize = new Size(L.title, L.title); icon.tintColor = c.blue;
      if (settings.showTitle) header.addSpacer(7);
    }
    if (settings.showTitle) {
      const title = header.addText(T.title); title.font = Font.boldSystemFont(L.title); title.textColor = c.text; title.lineLimit = 1;
    }
    header.addSpacer();
    if (status.demo) { const d = header.addText("DEMO"); d.font = Font.boldSystemFont(Math.max(8, L.footer)); d.textColor = c.muted; }
    w.addSpacer(family === "small" ? 8 : 10);
  }
  if (status.total === 0) {
    const body = w.addStack(); body.layoutVertically(); body.addSpacer();
    const ok = body.addText(status.emptySelection ? "○" : "✓"); ok.font = Font.boldSystemFont(family === "small" ? 24 : 30); ok.textColor = status.emptySelection ? c.muted : c.green; ok.centerAlignText(); body.addSpacer(4);
    const msg = body.addText(status.emptySelection ? T.noneSelected : T.upToDate); msg.font = Font.semiboldSystemFont(family === "small" ? 11 : 13); msg.textColor = c.text; msg.centerAlignText(); msg.lineLimit = 2; body.addSpacer();
  } else {
    const visible = status.updates.slice(0, L.maxRows);
    for (let i = 0; i < visible.length; i++) {
      const app = visible[i], row = w.addStack(); row.centerAlignContent(); row.size = new Size(0, family === "small" ? 21 : 24);
      const name = row.addText(app.name); name.font = Font.semiboldSystemFont(L.row); name.textColor = c.text; name.lineLimit = 1; name.minimumScaleFactor = 0.65;
      if (settings.showNewBadge) { row.addSpacer(6); addNewBadge(row, c, Math.max(8, L.footer)); }
      if (settings.showVersion) {
        row.addSpacer(6);
        const version = row.addText(app.version); version.font = Font.mediumSystemFont(L.version); version.textColor = c.muted; version.lineLimit = 1; version.minimumScaleFactor = 0.7;
      }
      if (i < visible.length - 1) w.addSpacer(L.rowGap);
    }
  }
  w.addSpacer();
  if (settings.showUpdateCount || settings.showCheckedTime || status.offline) {
    const footer = w.addStack(); footer.centerAlignContent();
    if (settings.showUpdateCount) {
      const count = footer.addText(T.updates(status.total)); count.font = Font.boldSystemFont(L.footer); count.textColor = status.total > 0 ? (c.count || c.green) : c.muted; count.lineLimit = 1; count.minimumScaleFactor = 0.7;
    }
    if (settings.showUpdateCount && (settings.showCheckedTime || status.offline)) footer.addSpacer();
    if (status.offline) { const off = footer.addText(`⚠︎ ${T.offline}`); off.font = Font.mediumSystemFont(L.footer); off.textColor = c.red; }
    else if (settings.showCheckedTime) { const checked = footer.addText(formatTime(status.checkedAt)); checked.font = Font.mediumSystemFont(L.footer); checked.textColor = c.muted; }
  }
  w.refreshAfterDate = new Date(Date.now() + settings.refreshMinutes * 60 * 1000);
  return w;
}
async function presentWidget(w, family) { if (family === "small") return await w.presentSmall(); if (family === "large") return await w.presentLarge(); return await w.presentMedium(); }

function esc(v) { return String(v ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }
function settingsHTML(settings, catalogModel, catalogMode) {
  const L = UI[settings.language || "en"] || UI.en;
  const langOptions = LANGS.map(([v, label]) => `<option value="${v}" ${v === settings.language ? "selected" : ""}>${label}</option>`).join("");
  const refreshOptions = [15, 30, 60, 120].map(v => `<option value="${v}" ${v === settings.refreshMinutes ? "selected" : ""}>${v} ${esc(L.minutes)}</option>`).join("");
  return `<!doctype html><html lang="${settings.language || "en"}"><head><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>
:root{color-scheme:dark;--bg:#0b1020;--panel:#111827;--panel2:#172033;--border:#2a3850;--text:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--accent2:#0284c7;--ok:#86efac;--danger:#fb7185;--shadow:0 24px 70px rgba(0,0,0,.45)}*{box-sizing:border-box}html,body{margin:0;min-height:100%;color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-tap-highlight-color:transparent}html{background:#070b14}body{padding:calc(14px + env(safe-area-inset-top)) 14px calc(36px + env(safe-area-inset-bottom));max-width:680px;margin:auto;background:radial-gradient(circle at top,#172554 0,#0b1020 42%,#070b14 100%);background-attachment:fixed}.screen{display:none}.screen.active{display:block}.topbar{display:flex;align-items:center;justify-content:space-between;min-height:42px;margin:0 2px 8px}.back{border:0;background:transparent;color:var(--accent);font:inherit;font-size:16px;font-weight:750;padding:7px 0}.hero{background:rgba(17,24,39,.96);border:1px solid var(--border);border-radius:22px;padding:22px;margin-bottom:14px;box-shadow:var(--shadow)}.heroTop{display:flex;align-items:center;justify-content:space-between;gap:10px}.eyebrow{display:inline-flex;align-items:center;gap:7px;padding:6px 10px;border:1px solid #1d4ed8;border-radius:999px;background:#0f1f46;color:#bfdbfe;font-size:.78rem;font-weight:700}.updateBtn{border:1px solid #1d4ed8;border-radius:999px;background:#0f1f46;color:#bfdbfe;padding:6px 10px;font:inherit;font-size:.78rem;font-weight:800}.updateStatus{min-height:17px;margin-top:8px;color:var(--muted);font-size:11px}.updateStatus.ok{color:var(--ok)}.updateStatus.error{color:var(--danger)}.hero h1,.screenTitle{font-size:27px;line-height:1.15;margin:14px 0 6px;font-weight:800;letter-spacing:-.45px}.screenTitle{margin:5px 2px 6px}.hero p,.screenSub{color:var(--muted);font-size:14px;line-height:1.5;margin:0}.screenSub{margin:0 2px 14px}.sectionTitle{font-size:11px;color:#9fb3ce;text-transform:uppercase;letter-spacing:.1em;font-weight:800;margin:19px 9px 8px}.card{background:rgba(17,24,39,.96);border:1px solid var(--border);border-radius:18px;overflow:hidden;margin-bottom:13px;box-shadow:0 12px 34px rgba(0,0,0,.24)}.navRow,.settingRow{min-height:54px;display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-bottom:1px solid rgba(42,56,80,.85)}.navRow:last-child,.settingRow:last-child{border-bottom:0}.navRow:active{background:var(--panel2)}.navLeft{display:flex;gap:11px;align-items:center;font-size:15px;font-weight:700;min-width:0}.navIcon{width:26px;text-align:center;flex:0 0 26px}.navRight{display:flex;align-items:center;gap:8px}.navDetail,.rowDetail{font-size:12px;color:var(--muted)}.navDetail{max-width:180px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.chevron{font-size:23px;color:#64748b}.rowText{min-width:0;padding-right:11px}.rowTitle{font-size:15px;font-weight:650}.rowDetail{margin-top:3px;line-height:1.35}.switch{position:relative;width:50px;height:30px;flex:0 0 50px}.switch input{display:none}.slider{position:absolute;inset:0;background:#243149;border:1px solid var(--border);border-radius:999px}.slider:before{content:"";position:absolute;width:24px;height:24px;left:2px;top:2px;background:#fff;border-radius:50%;transition:.18s}.switch input:checked+.slider{background:var(--accent2);border-color:var(--accent)}.switch input:checked+.slider:before{transform:translateX(20px)}.previewGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:8px}.previewBtn,.actionBtn{min-height:48px;border:1px solid #1d4ed8;border-radius:13px;background:linear-gradient(135deg,#0369a1,#0284c7);color:#fff;font:inherit;font-weight:800;font-size:13px}.actionBtn.secondary{background:#243149;border-color:var(--border)}.actionBtn.danger{background:#3a1720;border-color:#6b2738;color:#fecdd3}.actionGrid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:12px}.field{padding:12px 14px;border-bottom:1px solid rgba(42,56,80,.85)}.field:last-child{border-bottom:0}.field label{display:block;margin-bottom:7px;color:#dbeafe;font-size:.82rem;font-weight:650}select,input[type=search],input[type=text]{width:100%;min-height:46px;border:1px solid var(--border);border-radius:12px;background:#0b1220;color:var(--text);padding:0 13px;font:inherit;font-size:15px;outline:none}input[type=color]{width:58px;height:40px;border:1px solid var(--border);border-radius:10px;background:#0b1220;padding:3px}.colorRow{display:flex;align-items:center;gap:12px}.colorRow code{color:var(--muted);font-size:12px}select:focus,input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(56,189,248,.12)}.searchBox{margin:0 0 12px}.empty{padding:20px 14px;color:var(--muted);text-align:center;font-size:13px}.status{min-height:20px;color:var(--ok);font-size:12px;padding:0 14px 12px}.pill{display:inline-flex;padding:5px 8px;border:1px solid var(--border);border-radius:999px;background:#0b1220;color:var(--muted);font-size:11px;font-weight:700}.footer{color:#64748b;text-align:center;font-size:.76rem;margin:16px 4px 0}.diag{padding:12px 14px;display:flex;align-items:center;justify-content:space-between;gap:12px}.diag strong{font-size:14px}.diag span{font-size:11px;font-weight:800}.ok{color:var(--ok)}.warn{color:#facc15}.bad{color:var(--danger)}.sourceList,.appList{max-height:none}.hidden{display:none!important}@media(max-width:430px){.previewGrid{grid-template-columns:1fr}.actionGrid{grid-template-columns:1fr}.navDetail{max-width:120px}}
</style></head><body>
<div id="home" class="screen active">
  <div class="hero"><div class="heroTop"><span class="eyebrow">📲 iOS-Hub · Scriptable</span><button class="updateBtn" onclick="native({action:'update'})">↻ ${esc(L.update)}</button></div><h1>${APP_NAME}</h1><p>${esc(L.subtitle)}</p><div id="updateStatus" class="updateStatus">v${APP_VERSION}</div></div>
  <div class="sectionTitle">${esc(L.tracking)}</div>
  <div class="card">
    <div class="navRow" onclick="showScreen('sources')"><div class="navLeft"><span class="navIcon">🗂️</span><span>${esc(L.sources)}</span></div><div class="navRight"><span id="sourceCount" class="navDetail"></span><span class="chevron">›</span></div></div>
    <div class="navRow" onclick="showScreen('apps')"><div class="navLeft"><span class="navIcon">📱</span><span>${esc(L.apps)}</span></div><div class="navRight"><span id="appCount" class="navDetail"></span><span class="chevron">›</span></div></div>
  </div>
  <div class="sectionTitle">${esc(L.preview)}</div><div class="screenSub">${esc(L.previewSub)}</div>
  <div class="previewGrid"><button class="previewBtn" onclick="preview('small',false)">Small</button><button class="previewBtn" onclick="preview('medium',false)">Medium</button><button class="previewBtn" onclick="preview('large',false)">Large</button></div>
  <button class="actionBtn secondary" style="width:100%;margin-bottom:13px" onclick="preview('medium',true)">${esc(L.demo)}</button>
  <div class="sectionTitle">${esc(L.settings)}</div>
  <div class="card"><div class="navRow" onclick="showScreen('appearance')"><div class="navLeft"><span class="navIcon">🎨</span><span>${esc(L.appearance)}</span></div><div class="navRight"><span class="chevron">›</span></div></div><div class="field"><label>${esc(L.language)}</label><select id="language" onchange="setLanguage(this.value)">${langOptions}</select></div><div class="field"><label>${esc(L.refresh)}</label><select id="refreshMinutes" onchange="saveBasic()">${refreshOptions}</select></div></div>
  <div class="sectionTitle">${esc(L.diagnostics)}</div>
  <div class="card"><div class="diag"><div><strong>iOS-Hub catalog</strong><div class="rowDetail">data/catalog.json</div></div><span class="${catalogMode === "online" ? "ok" : catalogMode === "cache" ? "warn" : "bad"}">${catalogMode === "online" ? "● ONLINE" : catalogMode === "cache" ? "● CACHE" : "● ERROR"}</span></div></div>
  <div class="sectionTitle">${esc(L.tools)}</div>
  <div class="card"><div class="navRow" onclick="native({action:'markSeen'})"><div class="rowText"><div class="rowTitle">✓ ${esc(L.markSeen)}</div><div class="rowDetail">${esc(L.markSeenDetail)}</div></div><span class="chevron">›</span></div><div class="navRow" onclick="native({action:'resetVersions'})"><div class="rowText"><div class="rowTitle">↺ ${esc(L.resetVersions)}</div><div class="rowDetail">${esc(L.resetVersionsDetail)}</div></div><span class="chevron">›</span></div><div id="toolStatus" class="status"></div></div>
  <div class="footer">${APP_NAME} · v${APP_VERSION}</div>
</div>

<div id="appearance" class="screen">
  <div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div>
  <div class="screenTitle">${esc(L.appearance)}</div><div class="screenSub">${esc(L.appearanceDetail)}</div>
  <div class="card">
    <div class="field"><label>${esc(L.widgetTitle)}</label><input id="widgetTitle" type="text" maxlength="40" value="${esc(settings.widgetTitle)}" oninput="saveAppearance()"></div>
    <div class="field"><label>${esc(L.footerLabel)}</label><div class="rowDetail" style="margin:-2px 0 9px">${esc(L.footerLabelDetail)}</div><input id="footerLabel" type="text" maxlength="40" value="${esc(settings.footerLabel)}" oninput="saveAppearance()"></div>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showHeaderIcon)}</div></div><span class="switch"><input id="showHeaderIcon" type="checkbox" ${settings.showHeaderIcon?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showTitle)}</div></div><span class="switch"><input id="showTitle" type="checkbox" ${settings.showTitle?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showNewBadge)}</div></div><span class="switch"><input id="showNewBadge" type="checkbox" ${settings.showNewBadge?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showVersion)}</div></div><span class="switch"><input id="showVersion" type="checkbox" ${settings.showVersion?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showUpdateCount)}</div></div><span class="switch"><input id="showUpdateCount" type="checkbox" ${settings.showUpdateCount?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showCheckedTime)}</div></div><span class="switch"><input id="showCheckedTime" type="checkbox" ${settings.showCheckedTime?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
  </div>
  <div class="sectionTitle">${esc(L.colors)}</div>
  <div class="card">
    <label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.useCustomColors)}</div></div><span class="switch"><input id="useCustomColors" type="checkbox" ${settings.useCustomColors?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>
    ${[["backgroundColor",L.backgroundColor],["textColor",L.textColor],["secondaryTextColor",L.secondaryTextColor],["iconColor",L.iconColor],["newTextColor",L.newTextColor],["newBackgroundColor",L.newBackgroundColor],["countColor",L.countColor],["errorColor",L.errorColor]].map(([id,label])=>`<div class="field"><label>${esc(label)}</label><div class="colorRow"><input id="${id}" type="color" value="${esc(settings[id])}" oninput="colorChanged('${id}')"><code id="${id}Code">${esc(settings[id])}</code></div></div>`).join("")}
  </div>
  <button class="actionBtn secondary" style="width:100%;margin-bottom:13px" onclick="resetAppearance()">↺ ${esc(L.resetAppearance)}</button>
</div>

<div id="sources" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.sources)}</div><div class="screenSub">${esc(L.sourcesDetail)}</div><input id="sourceSearch" class="searchBox" type="search" placeholder="${esc(L.searchSources)}" oninput="renderSources()"><div id="sourceList" class="card sourceList"></div></div>
<div id="apps" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.apps)}</div><div class="screenSub">${esc(L.appsDetail)}</div><div id="selectedSourceList" class="card"></div></div>
<div id="sourceApps" class="screen"><div class="topbar"><button class="back" onclick="showScreen('apps')">‹ ${esc(L.back)}</button><span></span></div><div id="sourceAppsTitle" class="screenTitle"></div><div id="sourceAppsSub" class="screenSub"></div><input id="appSearch" class="searchBox" type="search" placeholder="${esc(L.searchApps)}" oninput="renderSourceApps()"><div class="actionGrid"><button class="actionBtn secondary" onclick="selectAllApps(true)">${esc(L.selectAll)}</button><button class="actionBtn secondary" onclick="selectAllApps(false)">${esc(L.clearAll)}</button></div><div id="sourceAppList" class="card appList"></div></div>

<script>
const CATALOG=${JSON.stringify(catalogModel)};
let state=${JSON.stringify(settings)};
let activeSourceId=null;
window.__nativeQueue=[];
function native(o){window.__nativeQueue.push(o)}
function norm(v){return String(v||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase()}
function appKey(sourceId,bundle,name){return sourceId+'|'+bundle+'|'+name}
function sourceById(id){return CATALOG.find(x=>x.id===id)}
function isWatched(sourceId,app){return state.watchedApps.some(x=>x.sourceId===sourceId&&x.bundle===app.bundle&&x.appName===app.name)}
function updateCounts(){document.getElementById('sourceCount').textContent=state.selectedSources.length+' ${esc(L.selected)}';document.getElementById('appCount').textContent=state.watchedApps.length+' ${esc(L.selected)}'}
function showScreen(id){document.querySelectorAll('.screen').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');if(id==='sources')renderSources();if(id==='apps')renderSelectedSources();window.scrollTo(0,0)}
function save(){native({action:'save',settings:state});updateCounts()}
function saveBasic(){state.refreshMinutes=Number(document.getElementById('refreshMinutes').value)||30;save()}
function saveAppearance(){const textIds=['widgetTitle','footerLabel'],boolIds=['showHeaderIcon','showTitle','showNewBadge','showVersion','showUpdateCount','showCheckedTime','useCustomColors'],colorIds=['backgroundColor','textColor','secondaryTextColor','iconColor','newTextColor','newBackgroundColor','countColor','errorColor'];for(const id of textIds){const e=document.getElementById(id);if(e)state[id]=e.value}for(const id of boolIds){const e=document.getElementById(id);if(e)state[id]=!!e.checked}for(const id of colorIds){const e=document.getElementById(id);if(e){state[id]=e.value.toUpperCase();const code=document.getElementById(id+'Code');if(code)code.textContent=state[id]}}save()}
function colorChanged(id){const e=document.getElementById(id),toggle=document.getElementById('useCustomColors');if(e){state[id]=e.value.toUpperCase();const code=document.getElementById(id+'Code');if(code)code.textContent=state[id]}if(toggle){toggle.checked=true;state.useCustomColors=true}save()}
function resetAppearance(){Object.assign(state,{widgetTitle:'Sideload Watch',footerLabel:'',showHeaderIcon:true,showTitle:true,showNewBadge:true,showVersion:true,showUpdateCount:true,showCheckedTime:true,useCustomColors:false,backgroundColor:'#0B1020',textColor:'#F8FAFC',secondaryTextColor:'#94A3B8',iconColor:'#0A84FF',newTextColor:'#34C759',newBackgroundColor:'#12351E',countColor:'#34C759',errorColor:'#FF453A'});save();native({action:'reload',settings:state})}
function setLanguage(v){state.language=v;save();native({action:'reload',settings:state})}
function renderSources(){const q=norm(document.getElementById('sourceSearch').value),root=document.getElementById('sourceList');const rows=CATALOG.filter(s=>!q||norm(s.name).includes(q));root.innerHTML=rows.length?'':'';if(!rows.length){root.innerHTML='<div class="empty">—</div>';return}rows.forEach(src=>{const on=state.selectedSources.includes(src.id),r=document.createElement('label');r.className='settingRow';r.innerHTML='<div class="rowText"><div class="rowTitle">'+escapeHtml(src.name)+'</div><div class="rowDetail">'+src.apps.length+' apps</div></div><span class="switch"><input type="checkbox" '+(on?'checked':'')+'><span class="slider"></span></span>';const input=r.querySelector('input');input.addEventListener('change',()=>{if(input.checked){if(!state.selectedSources.includes(src.id))state.selectedSources.push(src.id)}else{state.selectedSources=state.selectedSources.filter(x=>x!==src.id);state.watchedApps=state.watchedApps.filter(x=>x.sourceId!==src.id)}save()});root.appendChild(r)})}
function renderSelectedSources(){const root=document.getElementById('selectedSourceList'),rows=state.selectedSources.map(sourceById).filter(Boolean);root.innerHTML='';if(!rows.length){root.innerHTML='<div class="empty">${esc(L.noSources)}</div>';return}rows.forEach(src=>{const n=state.watchedApps.filter(x=>x.sourceId===src.id).length,r=document.createElement('div');r.className='navRow';r.innerHTML='<div class="navLeft"><span class="navIcon">📦</span><span>'+escapeHtml(src.name)+'</span></div><div class="navRight"><span class="navDetail">'+n+' / '+src.apps.length+'</span><span class="chevron">›</span></div>';r.onclick=()=>openSourceApps(src.id);root.appendChild(r)})}
function openSourceApps(id){activeSourceId=id;document.getElementById('appSearch').value='';renderSourceApps();showScreen('sourceApps')}
function renderSourceApps(){const src=sourceById(activeSourceId),root=document.getElementById('sourceAppList');if(!src){root.innerHTML='<div class="empty">—</div>';return}document.getElementById('sourceAppsTitle').textContent=src.name;const selected=state.watchedApps.filter(x=>x.sourceId===src.id).length;document.getElementById('sourceAppsSub').textContent=selected+' ${esc(L.selected)} · '+src.apps.length+' apps';const q=norm(document.getElementById('appSearch').value);const rows=src.apps.filter(a=>!q||norm(a.name+' '+a.bundle+' '+a.version).includes(q));root.innerHTML='';if(!rows.length){root.innerHTML='<div class="empty">${esc(L.noApps)}</div>';return}rows.forEach(app=>{const on=isWatched(src.id,app),r=document.createElement('label');r.className='settingRow';r.innerHTML='<div class="rowText"><div class="rowTitle">'+escapeHtml(app.name)+'</div><div class="rowDetail">v'+escapeHtml(app.version)+(app.bundle?' · '+escapeHtml(app.bundle):'')+'</div></div><span class="switch"><input type="checkbox" '+(on?'checked':'')+'><span class="slider"></span></span>';const input=r.querySelector('input');input.addEventListener('change',()=>toggleApp(src,app,input.checked));root.appendChild(r)})}
function toggleApp(src,app,on){state.watchedApps=state.watchedApps.filter(x=>!(x.sourceId===src.id&&x.bundle===app.bundle&&x.appName===app.name));if(on)state.watchedApps.push({sourceId:src.id,bundle:app.bundle,appName:app.name,label:app.name});save();renderSourceApps()}
function selectAllApps(on){const src=sourceById(activeSourceId);if(!src)return;state.watchedApps=state.watchedApps.filter(x=>x.sourceId!==src.id);if(on)src.apps.forEach(app=>state.watchedApps.push({sourceId:src.id,bundle:app.bundle,appName:app.name,label:app.name}));save();renderSourceApps();renderSelectedSources()}
function preview(family,demo){native({action:'preview',family,demo,settings:state})}
function escapeHtml(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function nativeMessage(m){if(!m)return;if(m.action==='status'){const e=document.getElementById('toolStatus');e.textContent=m.text||'';e.style.color=m.ok?'var(--ok)':'var(--danger)'}if(m.action==='update'){const e=document.getElementById('updateStatus');e.textContent=m.text||'';e.className='updateStatus '+(m.ok?'ok':'error')}}
updateCounts();
</script></body></html>`;
}

async function send(web, obj) { try { await web.evaluateJavaScript(`nativeMessage(${JSON.stringify(obj)})`, false); } catch (_) {} }
function compareVersions(a, b) {
  const A = String(a || "0").replace(/[^0-9.]/g, "").split(".").map(Number), B = String(b || "0").replace(/[^0-9.]/g, "").split(".").map(Number);
  for (let i = 0; i < Math.max(A.length, B.length); i++) { if ((A[i] || 0) > (B[i] || 0)) return 1; if ((A[i] || 0) < (B[i] || 0)) return -1; }
  return 0;
}
async function updateScript(settings) {
  if (!UPDATE_ENABLED) return { ok: true, text: t(settings, "updateTest") };
  try {
    const r = new Request(UPDATE_SOURCE_URL); r.timeoutInterval = API_TIMEOUT; const src = await r.loadString();
    if (!src || src.length < UPDATE_MIN_BYTES) throw new Error("Bad source");
    const m = src.match(/const APP_VERSION\s*=\s*["']([^"']+)["']/); if (!m) throw new Error("No version");
    const v = m[1]; if (compareVersions(v, APP_VERSION) <= 0) return { ok: true, text: `${t(settings, "current")} v${APP_VERSION}` };
    const a = new Alert(); a.title = APP_NAME; a.message = `${t(settings, "available")}: v${v}`; a.addAction(t(settings, "apply")); a.addCancelAction(t(settings, "cancel"));
    if (await a.presentAlert() !== 0) return { ok: true, text: `v${APP_VERSION} → v${v}` };
    const target = module.filename; if (!target) throw new Error("Current script path unavailable");
    const cloud = FileManager.iCloud(), local = FileManager.local(); let targetFm = local;
    if (cloud.fileExists(target)) { targetFm = cloud; if (!cloud.isFileDownloaded(target)) await cloud.downloadFileFromiCloud(target); }
    else if (!local.fileExists(target)) throw new Error("Current script file not found");
    const backup = /\.js$/i.test(target) ? target.replace(/\.js$/i, `_backup_v${APP_VERSION}.js`) : target + `_backup_v${APP_VERSION}.js`;
    try { targetFm.writeString(backup, targetFm.readString(target)); } catch (_) {}
    targetFm.writeString(target, src); return { ok: true, text: t(settings, "updatedOk") };
  } catch (e) { console.log(e); return { ok: false, text: t(settings, "updateFail") }; }
}

async function openSettings(settings) {
  const loaded = await loadCatalogWithStatus();
  const model = compactCatalog(loaded.catalog);
  const web = new WebView(); await web.loadHTML(settingsHTML(settings, model, loaded.mode));
  let dismissed = false, current = mergeSettings(settings);
  const presentPromise = web.present(false).then(() => { dismissed = true; });
  const sleep = ms => new Promise(resolve => Timer.schedule(ms, false, resolve));
  while (!dismissed) {
    await sleep(160); if (dismissed) break;
    let raw = null; try { raw = await web.evaluateJavaScript("JSON.stringify(window.__nativeQueue.shift()||null)"); } catch (_) { if (dismissed) break; continue; }
    if (!raw || raw === "null") continue;
    let msg = null; try { msg = JSON.parse(raw); } catch (_) { continue; }
    try {
      if (msg.action === "save") { current = mergeSettings(msg.settings); saveSettings(current); }
      else if (msg.action === "reload") { current = mergeSettings(msg.settings); saveSettings(current); await web.loadHTML(settingsHTML(current, model, loaded.mode)); }
      else if (msg.action === "preview") {
        current = mergeSettings(msg.settings || current); saveSettings(current); const family = ["small", "medium", "large"].includes(msg.family) ? msg.family : "medium";
        const status = msg.demo ? demoStatus() : await getRealStatus(current); const w = await buildWidget(status, current, family); await presentWidget(w, family);
      }
      else if (msg.action === "markSeen") { const n = await markAllSeen(current); await send(web, { action: "status", ok: true, text: t(current, "markResult")(n) }); }
      else if (msg.action === "resetVersions") { resetState(); await send(web, { action: "status", ok: true, text: t(current, "resetDone") }); }
      else if (msg.action === "update") { const r = await updateScript(current); await send(web, { action: "update", ok: r.ok, text: r.text }); }
    } catch (e) { await send(web, { action: "status", ok: false, text: String(e) }); }
  }
  try { await presentPromise; } catch (_) {}
  return current;
}

let SETTINGS = await firstLanguage(loadSettings());
if (config.runsInWidget) {
  const status = await getRealStatus(SETTINGS); const widget = await buildWidget(status, SETTINGS); Script.setWidget(widget);
} else {
  SETTINGS = await openSettings(SETTINGS);
}
Script.complete();