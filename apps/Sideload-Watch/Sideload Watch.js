// Variables used by Scriptable.
// icon-color: deep-blue; icon-glyph: download;
// ============================================================
// Sideload Watch — test build
// Reads live versions from CaseyCZ/iOS-Hub and shows only apps
// whose version changed since the last acknowledged version.
// ============================================================

const APP_VERSION = "0.3.4";
const CATALOG_URL = "https://raw.githubusercontent.com/CaseyCZ/iOS-Hub/main/data/catalog.json";
const HUB_URL = "https://caseycz.github.io/iOS-Hub/";
const STATE_FILE = "SideloadWatch_state.json";
const REFRESH_MINUTES = 30;

// Test selection. Later this can be generated from a web picker.
const WATCHED = [
  { sourceId: "stremio-official-pal", bundle: "com.stremio.pal", label: "Stremio" },
  { sourceId: "youtuberebornplus", bundle: "com.google.ios.youtube", label: "YouTubeRebornPlus" },
  { sourceId: "yattee", bundle: "stream.yattee.app", label: "Yattee" },
  { sourceId: "sidestore-official", bundle: "com.SideStore.SideStore", label: "SideStore" },
  { sourceId: "utm", bundle: "com.utmapp.UTM", label: "UTM" },
  { sourceId: "provenance", bundle: "com.provenance-emu.provenance", label: "Provenance" },
  { sourceId: "vortx", bundle: "com.stremiox.app.native", label: "VortX" },
];

const fm = FileManager.local();
const statePath = fm.joinPath(fm.documentsDirectory(), STATE_FILE);

const locale = String(Device.locale() || "en").toLowerCase();
const isCS = locale.startsWith("cs");
const T = {
  title: "Sideload Watch",
  new: "NEW",
  updates: n => isCS ? `${n} ${n === 1 ? "aktualizace" : (n >= 2 && n <= 4 ? "aktualizace" : "aktualizací")}` : `${n} update${n === 1 ? "" : "s"} available`,
  upToDate: isCS ? "Všechno je aktuální" : "Everything is up to date",
  checked: isCS ? "Kontrola" : "Checked",
  offline: isCS ? "Nepodařilo se načíst katalog" : "Could not refresh catalog",
  baseline: isCS ? "Výchozí verze byly uloženy" : "Baseline versions saved",
};

function loadState() {
  try {
    if (!fm.fileExists(statePath)) return { seen: {}, lastCurrent: {}, updatedAt: null };
    const raw = fm.readString(statePath);
    const parsed = JSON.parse(raw);
    return {
      seen: parsed.seen || {},
      lastCurrent: parsed.lastCurrent || {},
      updatedAt: parsed.updatedAt || null,
    };
  } catch (_) {
    return { seen: {}, lastCurrent: {}, updatedAt: null };
  }
}

function saveState(state) {
  fm.writeString(statePath, JSON.stringify(state, null, 2));
}

function keyFor(item) {
  return `${item.sourceId}|${item.bundle}`;
}

async function loadCatalog() {
  const req = new Request(CATALOG_URL);
  req.timeoutInterval = 12;
  return await req.loadJSON();
}

function resolveWatched(catalog) {
  const sources = Array.isArray(catalog && catalog.sources) ? catalog.sources : [];
  const sourceMap = new Map(sources.map(s => [s.id, s]));
  const result = [];

  for (const item of WATCHED) {
    const src = sourceMap.get(item.sourceId);
    if (!src || !Array.isArray(src.apps)) continue;
    const app = src.apps.find(a => a.bundleIdentifier === item.bundle);
    if (!app) continue;
    result.push({
      key: keyFor(item),
      sourceId: item.sourceId,
      name: item.label || app.name,
      version: String(app.version || "—"),
      iconURL: app.iconURL || src.iconURL || "",
    });
  }
  return result;
}

async function getRealStatus() {
  const state = loadState();
  try {
    const catalog = await loadCatalog();
    const current = resolveWatched(catalog);
    let changedState = false;

    // First run or newly added watched app: establish baseline silently.
    for (const app of current) {
      if (!state.seen[app.key]) {
        state.seen[app.key] = app.version;
        changedState = true;
      }
      state.lastCurrent[app.key] = {
        name: app.name,
        version: app.version,
        iconURL: app.iconURL,
      };
    }
    state.updatedAt = new Date().toISOString();
    if (changedState || current.length) saveState(state);

    const updates = current.filter(app => state.seen[app.key] !== app.version);
    return {
      updates,
      total: updates.length,
      current,
      checkedAt: new Date(),
      offline: false,
    };
  } catch (error) {
    const cached = [];
    for (const item of WATCHED) {
      const key = keyFor(item);
      const now = state.lastCurrent[key];
      if (!now || !state.seen[key]) continue;
      if (now.version !== state.seen[key]) {
        cached.push({ key, name: now.name || item.label, version: now.version, iconURL: now.iconURL || "" });
      }
    }
    return {
      updates: cached,
      total: cached.length,
      current: [],
      checkedAt: state.updatedAt ? new Date(state.updatedAt) : null,
      offline: true,
      error: String(error),
    };
  }
}

async function markAllSeen() {
  const catalog = await loadCatalog();
  const current = resolveWatched(catalog);
  const state = loadState();
  for (const app of current) {
    state.seen[app.key] = app.version;
    state.lastCurrent[app.key] = { name: app.name, version: app.version, iconURL: app.iconURL };
  }
  state.updatedAt = new Date().toISOString();
  saveState(state);
  return current.length;
}

function resetState() {
  if (fm.fileExists(statePath)) fm.remove(statePath);
}

function demoStatus() {
  const demo = [
    { name: "Stremio", version: "2.0.9" },
    { name: "YouTubeRebornPlus", version: "20.06.1" },
    { name: "Yattee", version: "2.1.0" },
    { name: "SideStore", version: "0.6.3" },
    { name: "UTM", version: "4.8.0" },
    { name: "Provenance", version: "3.4.0" },
    { name: "VortX", version: "0.5.0" },
  ];
  return { updates: demo, total: demo.length, checkedAt: new Date(), offline: false, demo: true };
}

function colors() {
  return {
    bg: Color.dynamic(new Color("F5F7FB"), new Color("0B1020")),
    panel: Color.dynamic(new Color("FFFFFF"), new Color("111827")),
    text: Color.dynamic(new Color("111827"), new Color("F8FAFC")),
    muted: Color.dynamic(new Color("6B7280"), new Color("94A3B8")),
    border: Color.dynamic(new Color("E5E7EB"), new Color("263449")),
    green: new Color("34C759"),
    greenSoft: Color.dynamic(new Color("E8F8ED"), new Color("12351E")),
    red: new Color("FF453A"),
    blue: new Color("0A84FF"),
  };
}

function layoutForFamily(family) {
  if (family === "small") return { maxRows: 2, title: 14, row: 11, version: 10, footer: 9, pad: 11, rowGap: 5 };
  if (family === "large") return { maxRows: 9, title: 17, row: 14, version: 12, footer: 11, pad: 15, rowGap: 7 };
  return { maxRows: 4, title: 16, row: 13, version: 11, footer: 10, pad: 13, rowGap: 6 };
}

function addNewBadge(stack, c, fontSize) {
  const badge = stack.addStack();
  badge.backgroundColor = c.greenSoft;
  badge.cornerRadius = 5;
  badge.setPadding(2, 5, 2, 5);
  const t = badge.addText(T.new);
  t.font = Font.boldSystemFont(fontSize);
  t.textColor = c.green;
  t.lineLimit = 1;
}

function formatTime(date) {
  if (!date || isNaN(date.getTime())) return "—";
  const f = new DateFormatter();
  f.locale = Device.locale();
  f.useNoDateStyle();
  f.useShortTimeStyle();
  return f.string(date);
}

async function buildWidget(status, familyOverride) {
  const family = familyOverride || config.widgetFamily || "medium";
  const L = layoutForFamily(family);
  const c = colors();
  const w = new ListWidget();
  w.backgroundColor = c.bg;
  w.setPadding(L.pad, L.pad, L.pad, L.pad);
  w.url = HUB_URL;

  // Header
  const header = w.addStack();
  header.centerAlignContent();
  const symbol = SFSymbol.named("arrow.triangle.2.circlepath");
  symbol.applyFont(Font.semiboldSystemFont(L.title));
  const icon = header.addImage(symbol.image);
  icon.imageSize = new Size(L.title, L.title);
  icon.tintColor = c.blue;
  header.addSpacer(7);
  const title = header.addText(T.title);
  title.font = Font.boldSystemFont(L.title);
  title.textColor = c.text;
  title.lineLimit = 1;
  header.addSpacer();
  if (status.demo) {
    const d = header.addText("DEMO");
    d.font = Font.boldSystemFont(Math.max(8, L.footer));
    d.textColor = c.muted;
  }

  w.addSpacer(family === "small" ? 8 : 10);

  if (status.total === 0) {
    const body = w.addStack();
    body.layoutVertically();
    body.addSpacer();
    const ok = body.addText("✓");
    ok.font = Font.boldSystemFont(family === "small" ? 24 : 30);
    ok.textColor = c.green;
    ok.centerAlignText();
    body.addSpacer(4);
    const msg = body.addText(T.upToDate);
    msg.font = Font.semiboldSystemFont(family === "small" ? 11 : 13);
    msg.textColor = c.text;
    msg.centerAlignText();
    msg.lineLimit = 2;
    body.addSpacer();
  } else {
    const visible = status.updates.slice(0, L.maxRows);
    for (let i = 0; i < visible.length; i++) {
      const app = visible[i];
      const row = w.addStack();
      row.centerAlignContent();
      row.size = new Size(0, family === "small" ? 21 : 24);

      const name = row.addText(app.name);
      name.font = Font.semiboldSystemFont(L.row);
      name.textColor = c.text;
      name.lineLimit = 1;
      name.minimumScaleFactor = 0.65;

      row.addSpacer(6);
      addNewBadge(row, c, Math.max(8, L.footer));
      row.addSpacer(6);

      const version = row.addText(app.version);
      version.font = Font.mediumSystemFont(L.version);
      version.textColor = c.muted;
      version.lineLimit = 1;
      version.minimumScaleFactor = 0.7;

      if (i < visible.length - 1) w.addSpacer(L.rowGap);
    }
  }

  w.addSpacer();

  const footer = w.addStack();
  footer.centerAlignContent();
  const count = footer.addText(T.updates(status.total));
  count.font = Font.boldSystemFont(L.footer);
  count.textColor = status.total > 0 ? c.green : c.muted;
  count.lineLimit = 1;
  count.minimumScaleFactor = 0.7;

  footer.addSpacer();
  if (status.offline) {
    const off = footer.addText("⚠︎ offline");
    off.font = Font.mediumSystemFont(L.footer);
    off.textColor = c.red;
  } else {
    const checked = footer.addText(formatTime(status.checkedAt));
    checked.font = Font.mediumSystemFont(L.footer);
    checked.textColor = c.muted;
  }

  w.refreshAfterDate = new Date(Date.now() + REFRESH_MINUTES * 60 * 1000);
  return w;
}

async function choosePreviewSize() {
  const a = new Alert();
  a.title = "Preview size";
  a.addAction("Small");
  a.addAction("Medium");
  a.addAction("Large");
  a.addCancelAction("Cancel");
  const i = await a.presentSheet();
  return ["small", "medium", "large"][i] || null;
}

async function presentWidget(widget, family) {
  if (family === "small") return await widget.presentSmall();
  if (family === "large") return await widget.presentLarge();
  return await widget.presentMedium();
}

async function appMenu() {
  const a = new Alert();
  a.title = `Sideload Watch ${APP_VERSION}`;
  a.message = isCS
    ? "Testovací verze napojená na živý katalog iOS-Hub."
    : "Test build connected to the live iOS-Hub catalog.";
  a.addAction(isCS ? "Náhled reálného widgetu" : "Preview real widget");
  a.addAction(isCS ? "Demo — 7 aktualizací" : "Demo — 7 updates");
  a.addAction(isCS ? "Označit vše jako přečtené" : "Mark all as seen");
  a.addDestructiveAction(isCS ? "Resetovat uložené verze" : "Reset saved versions");
  a.addCancelAction(isCS ? "Zavřít" : "Close");
  const choice = await a.presentSheet();

  if (choice === 0 || choice === 1) {
    const family = await choosePreviewSize();
    if (!family) return;
    const status = choice === 1 ? demoStatus() : await getRealStatus();
    const widget = await buildWidget(status, family);
    await presentWidget(widget, family);
    return;
  }

  if (choice === 2) {
    try {
      const n = await markAllSeen();
      const ok = new Alert();
      ok.title = isCS ? "Hotovo" : "Done";
      ok.message = isCS ? `Uloženo ${n} aktuálních verzí.` : `Saved ${n} current versions.`;
      ok.addAction("OK");
      await ok.presentAlert();
    } catch (e) {
      const er = new Alert();
      er.title = "Error";
      er.message = String(e);
      er.addAction("OK");
      await er.presentAlert();
    }
    return;
  }

  if (choice === 3) {
    resetState();
    const ok = new Alert();
    ok.title = isCS ? "Resetováno" : "Reset";
    ok.message = isCS ? "Při příštím spuštění se vytvoří nová výchozí verze." : "A new baseline will be created on the next run.";
    ok.addAction("OK");
    await ok.presentAlert();
  }
}

if (config.runsInWidget) {
  const status = await getRealStatus();
  const widget = await buildWidget(status);
  Script.setWidget(widget);
} else {
  await appMenu();
}

Script.complete();