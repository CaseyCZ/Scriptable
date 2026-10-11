# CaseyCZ Scriptable Template

Společný výchozí template pro nové Scriptable aplikace v repozitáři `CaseyCZ/Scriptable`.

Template není samostatný produkt pro běžné uživatele. Slouží jako základ, ze kterého se zakládají nové aplikace, aby měly stejné nastavení, vzhled, aktualizace, zálohy a chování.

## Co už template obsahuje

- jednotný CaseyCZ WebView vzhled podle Home Dashboard / Sports Info / Sports Live
- hero s názvem, verzí a kontrolou aktualizace
- náhled Small / Medium / Large
- společné obrazovky `Aplikace`, `Vzhled widgetu`, `Chování`, `API a zdroje`, `Diagnostika`, `Záloha a údržba`, `Nápověda`
- automatické ukládání nastavení
- `APP_VERSION` oddělený od `SETTINGS_VERSION`
- migrace settings přes `SETTINGS_VERSION`
- feature flags přes `FEATURES`
- volbu `local` / `icloud` úložiště
- jazyky CS / EN / DE / ES + výběr jazyka při prvním spuštění
- vlastní barvy s pickerem + HEX
- citlivé hodnoty přes Scriptable Keychain (`SECRET_KEYS`)
- file backup/import přes `.json`; Keychain secrets se do zálohy nedávají
- společný diagnostický renderer `checking / ok / warning / error / off`
- updater přes `version.json`, cache-busting a kontrolu staženého JS
- automatickou zálohu staré JS verze před aktualizací
- build workflow pro `.scriptable` balíček

## Jak z template založit novou aplikaci

1. Zkopíruj `apps/_Template` do nové složky aplikace.
2. Přejmenuj `CaseyCZ Template.js` a změň `APP_NAME`, `APP_SLUG`, ikonu a update URL.
3. Nastav `FEATURES` podle toho, co aplikace skutečně používá.
4. Uprav `DEFAULTS` a vlastní obrazovku `Aplikace`.
5. Citlivé hodnoty nepřidávej do settings. Přidej jejich názvy do `SECRET_KEYS` a ukládej je do Keychain.
6. Při změně struktury nastavení zvyš `SETTINGS_VERSION` a přidej migraci. Běžná release verze patří do `APP_VERSION`.
7. Uprav build workflow nebo vytvoř workflow aplikace podle `_Template`.

## Standardní struktura nastavení

Doporučené pořadí hlavní obrazovky:

1. Hero + Update
2. Náhled widgetu
3. vlastní nastavení aplikace
4. Vzhled widgetu
5. Chování
6. API a zdroje (pokud jsou potřeba)
7. Diagnostika
8. Záloha a údržba
9. Nápověda

## Standardní barvy

| Prvek | Barva |
| --- | --- |
| root | `#070B14` |
| background | `#0B1020` |
| panel | `#111827` |
| secondary panel | `#172033` |
| border | `#2A3850` |
| text | `#F8FAFC` |
| muted | `#94A3B8` |
| accent | `#38BDF8` |
| OK | `#34C759` |
| warning | `#FF9F0A` |
| error | `#FF453A` |

## Backup formát

```json
{
  "format": "CaseyCZ.Scriptable.Backup",
  "schema": 1,
  "app": "App Name",
  "appVersion": "1.0.0",
  "settingsVersion": 1,
  "exportedAt": "2026-10-05T12:00:00.000Z",
  "settings": {}
}
```

Citlivá data uložená v Keychain nejsou součástí exportu.

## Build

Workflow `.github/workflows/build-caseycz-template-package.yml` kontroluje syntaxi JavaScriptu, synchronizuje `version.json`, vytvoří `.scriptable` balíček a ověří, že balíček obsahuje přesně aktuální JS.

Při změně template workflow commitne pouze soubory v `apps/_Template`; ostatních aplikací se nedotýká.
