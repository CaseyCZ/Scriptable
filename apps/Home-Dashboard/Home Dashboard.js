// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: house;
// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: deep-blue; icon-glyph: house;
// ============================================================
// Home Dashboard v0.3.13
// CaseyCZ Scriptable Apps
// Universal website / server / JSON API / GitHub monitor.
// UI based on Sideload Watch.
// ============================================================

const APP_NAME = "Home Dashboard";
const APP_VERSION = "0.3.13";
const SETTINGS_FILE = "HomeDashboard_settings.json";
const STATE_FILE = "HomeDashboard_state.json";
const API_TIMEOUT = 8;
const GITHUB_TOKEN_KEY = "HomeDashboard_GitHubToken";
const NETWORK_SOURCE_AUTH_KEY = "HomeDashboard_NetworkSourceAuth";
const UPDATE_SOURCE_URL = "https://raw.githubusercontent.com/CaseyCZ/Scriptable/Master/apps/Home-Dashboard/Home%20Dashboard.js";
const UPDATE_MIN_BYTES = 50000;

const fm = FileManager.local();
const settingsPath = fm.joinPath(fm.documentsDirectory(), SETTINGS_FILE);
const statePath = fm.joinPath(fm.documentsDirectory(), STATE_FILE);

const T = {
  cs:{
    settings:"Nastavení",update:"Aktualizace",current:"Aktuální verze",available:"Dostupná aktualizace",apply:"Aktualizovat",cancel:"Zrušit",updatedOk:"Aktualizace nainstalována. Skript spusť znovu.",updateFail:"Kontrola aktualizace selhala.",subtitle:"Sleduj vlastní weby, servery a JSON API na jednom místě.",
    monitors:"Monitory",monitorsDetail:"Přidej vlastní služby a vyber, které se mají zobrazit.",
    preview:"Náhled widgetu",previewDetail:"Small / Medium / Large + demo.",
    appearance:"Vzhled widgetu",appearanceDetail:"Název, barvy a zobrazované údaje.",
    behavior:"Chování",behaviorDetail:"Interval kontroly, timeout a jazyk.",
    tools:"Nástroje",toolsDetail:"Test monitorů, export, import a reset cache.",
    back:"Zpět",add:"Přidat",save:"Uložit",delete:"Smazat",edit:"Upravit",help:"Nápověda",templates:"Vyber šablonu",advanced:"Pokročilé",advancedDetail:"Většina uživatelů tato pole nemusí měnit.",defaultTimeoutHint:"0 = použít výchozí timeout z Chování.",templateWeb:"Web / HTTP",templateWebDetail:"Nejjednodušší kontrola, zda web nebo služba odpovídá.",templateHomebridge:"Homebridge",templateHomebridgeDetail:"Předvyplní běžný Homebridge port 8581.",templateLocal:"Lokální služba",templateLocalDetail:"NAS, router, server nebo jiná webová služba v LAN.",templateJson:"JSON API",templateJsonDetail:"Kontrola hodnoty z JSON odpovědi.",templateCustom:"Vlastní",templateCustomDetail:"Prázdný formulář se všemi možnostmi.",helpIntro:"Jak Home Dashboard nastavit",helpIntroDetail:"Začni šablonou. Pro běžný web stačí název a URL.",helpWebTitle:"1. Web / HTTP",helpWebBody:"Příklad: Název Můj web, URL https://example.com. Metodu, hlavičky ani timeout nemusíš měnit.",helpHomebridgeTitle:"2. Homebridge",helpHomebridgeBody:"Příklad: http://192.168.1.50:8581. Pokud se otevře webové rozhraní Homebridge, je URL správně.",helpJsonTitle:"3. JSON API",helpJsonBody:"Když API vrací { status: online }, nastav JSON cestu na status a očekávanou hodnotu na online.",helpNetworkTitle:"4. Místní síť",helpNetworkBody:"Použij Najít v místní síti a klepni na Najít zařízení automaticky. IP adresu, subnet ani porty běžně znát nemusíš.",helpGithubTitle:"5. GitHub",helpGithubBody:"Zadej owner/repository. U veřejných repozitářů token není potřeba; token pro soukromá repo se ukládá do Keychain.",
    name:"Název",icon:"Ikona",type:"Typ",url:"URL",method:"Metoda",
    http:"HTTP / web",json:"JSON API",jsonPath:"JSON cesta",expected:"Očekávaná hodnota",
    expectedHint:"Prázdné = stačí platná odpověď. Příklad: online",
    headers:"HTTP hlavičky (JSON)",headersHint:'Např. {"Authorization":"Bearer …"}',
    enabled:"Zapnuto",showWidget:"Zobrazit ve widgetu",timeout:"Timeout",seconds:"s",
    addMonitor:"Přidat monitor",editMonitor:"Upravit monitor",none:"Zatím nejsou žádné monitory.",
    noSelection:"Žádné monitory ve widgetu",noSelectionDetail:"Přidej monitor a zapni Zobrazit ve widgetu.",
    small:"Small",medium:"Medium",large:"Large",realPreview:"Reálná data",demoPreview:"Demo",
    widgetTitle:"Název widgetu",visibility:"Viditelnost",showLatency:"Zobrazit odezvu",
    showValue:"Zobrazit hodnotu z JSON",showTime:"Zobrazit čas kontroly",
    customColors:"Vlastní barvy",useCustomColors:"Použít vlastní barvy",
    backgroundColor:"Barva pozadí",textColor:"Barva textu",mutedColor:"Barva vedlejšího textu",okColor:"Barva Online / OK",failColor:"Barva Offline / chyba",
    resetAppearance:"Obnovit vzhled",refresh:"Obnova widgetu",refreshDetail:"Požadovaný interval. iOS může widget obnovit později.",
    minutes:"min",language:"Jazyk",languageDetail:"Jazyk aplikace a widgetu.",defaultTimeout:"Výchozí timeout",
    testAll:"Otestovat všechny monitory",resetCache:"Resetovat cache",export:"Export nastavení",import:"Import nastavení",exportWarning:"Export slouží jako úplná záloha nastavení. Může obsahovat soukromé IP adresy, URL, vlastní URL scheme a HTTP hlavičky. Export nesdílej veřejně.",
    copied:"Nastavení zkopírováno.",imported:"Nastavení importováno.",invalid:"Neplatný JSON.",cacheReset:"Cache byla resetována.",
    online:"Online",offline:"Offline",checked:"Kontrola",allGood:"Vše v pořádku",problems:n=>`${n} ${n===1?"problém":"problémy"}`,
    saveHint:"Změny se ukládají automaticky.",firstRun:"Vyber jazyk",testResult:"Výsledek testu",addType:"Přidat monitor",manualAdd:"Ručně",manualAddDetail:"HTTP nebo JSON API",networkScan:"Najít v místní síti",networkScanDetail:"Vyhledá HTTP/HTTPS služby v celé místní síti.",scanMode:"Režim hledání",scanQuick:"Rychlé",scanNormal:"Běžné",scanDeep:"Důkladné",scanWhole:"Celá síť .1–.254",scanProgress:"Prohledávám",scanHosts:"Zařízení",scanServices:"Služby",scanActive:"aktivních",scanLimits:"Scriptable umí najít HTTP/HTTPS služby. Zařízení bez webového rozhraní se nemusí zobrazit.",githubAdd:"GitHub",githubAddDetail:"Repository, Actions nebo poslední release.",deviceSource:"Zdroj zařízení",deviceSourceDetail:"Volitelný JSON seznam klientů z routeru, controlleru nebo serveru. Doplní hostname, MAC a výrobce.",deviceSourceConfigured:"Zdroj zařízení nastaven",deviceSourceNone:"Bez zdroje zařízení",deviceSourceUse:"Používat zdroj zařízení",deviceSourceUrl:"URL seznamu zařízení",deviceSourceUrlHint:"JSON endpoint. Home Dashboard se pokusí pole rozpoznat automaticky.",deviceSourceAdvanced:"Pokročilé mapování JSON",deviceSourceListPath:"Cesta k seznamu",deviceSourceIpPath:"Pole IP",deviceSourceNamePath:"Pole názvu / hostname",deviceSourceMacPath:"Pole MAC",deviceSourceVendorPath:"Pole výrobce",deviceSourceAuth:"Authorization",deviceSourceAuthHint:"Volitelné. Např. Bearer … nebo Basic …; ukládá se pouze do Keychain.",deviceSourceTest:"Otestovat zdroj",deviceSourceSaved:"Zdroj zařízení uložen.",deviceSourceFound:"zařízení nalezeno",deviceSourceEmpty:"Zdroj nevrátil použitelná zařízení.",networkDevice:"Síťové zařízení",mac:"MAC",vendor:"Výrobce",hostname:"Hostname",autoFind:"Najít zařízení automaticky",autoFindDetail:"Nemusíš znát IP adresu, subnet ani porty. Home Dashboard se pokusí síť najít a nabídne služby ke sledování.",autoDetecting:"Hledám tvoji síť",autoDetected:"Nalezena síť",autoSearching:"Hledám zařízení a služby",autoFailed:"Síť se nepodařilo určit automaticky. Otevři Pokročilé a zadej síť ručně.",recommended:"Doporučeno ke sledování",watch:"Sledovat",watching:"Sleduji",manualScan:"Ruční hledání",expertOptions:"Pokročilé",expertDetail:"Ruční subnet, porty a externí zdroj zařízení. Pro běžné použití není potřeba.",nothingFound:"Nenašel jsem službu, kterou lze automaticky sledovat.",servicesOnDevice:"Služby na zařízení",watchDevice:"Sledovat zařízení",servicePorts:"porty",openNow:"Otevřít",openAction:"Otevření z Home Dashboardu",openActionDetail:"Nastav, co se má otevřít tlačítkem Otevřít v seznamu monitorů.",openDefault:"Výchozí adresa monitoru",openCustom:"Vlastní URL / aplikace",openNone:"Neotvírat nic",openCustomUrl:"Vlastní URL nebo URL scheme",openCustomHint:"Např. https://example.com nebo mojeaplikace://...",openShortcut:"Zkratka",shortcutName:"Název Zkratky",shortcutHint:"Zkratka může otevřít libovolnou aplikaci pomocí akce Otevřít aplikaci.",subnet:"Síť / subnet",range:"Rozsah hostů",ports:"Porty",scan:"Hledat",scanHint:"Pro běžnou domácí síť použij rozsah 1–254. Rychlé hledání zkouší nejčastější porty, Důkladné výrazně více.",scanNone:"Nenalezeny žádné HTTP služby.",scanFound:"Nalezené služby",addThis:"Přidat",added:"Přidáno",addDevice:"Přidat zařízení",services:"služby",device:"Zařízení",unknownService:"Neznámá webová služba",githubRepo:"Repository",githubRepoHint:"owner/repository",githubMode:"Co sledovat",githubRepoStatus:"Dostupnost repozitáře",githubActions:"Poslední GitHub Action",githubRelease:"Poslední release",githubToken:"GitHub token (volitelný)",githubTokenHint:"Token se ukládá jen do Scriptable Keychain a není součástí exportu.",saveToken:"Uložit token",removeToken:"Smazat token",tokenSaved:"Token je uložen v Keychain.",tokenMissing:"Bez tokenu – veřejná repo fungují přes GitHub API.",tokenStored:"GitHub token uložen.",tokenRemoved:"GitHub token odstraněn.",error:"Chyba"
  },
  en:{
    settings:"Settings",update:"Update",current:"Current version",available:"Update available",apply:"Update",cancel:"Cancel",updatedOk:"Update installed. Run the script again.",updateFail:"Update check failed.",subtitle:"Monitor your own websites, servers and JSON APIs in one place.",
    monitors:"Monitors",monitorsDetail:"Add your own services and choose what appears.",
    preview:"Widget preview",previewDetail:"Small / Medium / Large + demo.",
    appearance:"Widget appearance",appearanceDetail:"Title, colors and visible details.",
    behavior:"Behavior",behaviorDetail:"Refresh interval, timeout and language.",
    tools:"Tools",toolsDetail:"Test monitors, export, import and cache reset.",
    back:"Back",add:"Add",save:"Save",delete:"Delete",edit:"Edit",help:"Help",templates:"Choose a template",advanced:"Advanced",advancedDetail:"Most users do not need to change these fields.",defaultTimeoutHint:"0 = use the default timeout from Behavior.",templateWeb:"Website / HTTP",templateWebDetail:"Simple check that a website or service responds.",templateHomebridge:"Homebridge",templateHomebridgeDetail:"Prefills the common Homebridge port 8581.",templateLocal:"Local service",templateLocalDetail:"NAS, router, server or another LAN web service.",templateJson:"JSON API",templateJsonDetail:"Check a value from a JSON response.",templateCustom:"Custom",templateCustomDetail:"Blank form with all options.",helpIntro:"How to set up Home Dashboard",helpIntroDetail:"Start with a template. For a normal website, name and URL are enough.",helpWebTitle:"1. Website / HTTP",helpWebBody:"Example: Name My website, URL https://example.com. You normally do not need to change method, headers or timeout.",helpHomebridgeTitle:"2. Homebridge",helpHomebridgeBody:"Example: http://192.168.1.50:8581. If the Homebridge UI opens there, the URL is correct.",helpJsonTitle:"3. JSON API",helpJsonBody:"If the API returns { status: online }, set JSON path to status and expected value to online.",helpNetworkTitle:"4. Local network",helpNetworkBody:"Use Find on local network and tap Find devices automatically. You normally do not need to know the IP address, subnet or ports.",helpGithubTitle:"5. GitHub",helpGithubBody:"Enter owner/repository. Public repositories need no token; a token for private repos is stored in Keychain.",
    name:"Name",icon:"Icon",type:"Type",url:"URL",method:"Method",
    http:"HTTP / website",json:"JSON API",jsonPath:"JSON path",expected:"Expected value",
    expectedHint:"Blank = any valid response. Example: online",
    headers:"HTTP headers (JSON)",headersHint:'Example: {"Authorization":"Bearer …"}',
    enabled:"Enabled",showWidget:"Show in widget",timeout:"Timeout",seconds:"s",
    addMonitor:"Add monitor",editMonitor:"Edit monitor",none:"No monitors yet.",
    noSelection:"No monitors in widget",noSelectionDetail:"Add a monitor and enable Show in widget.",
    small:"Small",medium:"Medium",large:"Large",realPreview:"Live data",demoPreview:"Demo",
    widgetTitle:"Widget title",visibility:"Visibility",showLatency:"Show response time",
    showValue:"Show JSON value",showTime:"Show checked time",
    customColors:"Custom colors",useCustomColors:"Use custom colors",
    backgroundColor:"Background color",textColor:"Text color",mutedColor:"Secondary text color",okColor:"Online / OK color",failColor:"Offline / error color",
    resetAppearance:"Reset appearance",refresh:"Widget refresh",refreshDetail:"Requested interval. iOS may refresh later.",
    minutes:"min",language:"Language",languageDetail:"Language used by the app and widget.",defaultTimeout:"Default timeout",
    testAll:"Test all monitors",resetCache:"Reset cache",export:"Export settings",import:"Import settings",exportWarning:"Export is a complete settings backup. It may contain private IP addresses, URLs, custom URL schemes and HTTP headers. Do not share the export publicly.",
    copied:"Settings copied.",imported:"Settings imported.",invalid:"Invalid JSON.",cacheReset:"Cache reset.",
    online:"Online",offline:"Offline",checked:"Checked",allGood:"Everything is OK",problems:n=>`${n} problem${n===1?"":"s"}`,
    saveHint:"Changes are saved automatically.",firstRun:"Choose language",testResult:"Test result",addType:"Add monitor",manualAdd:"Manual",manualAddDetail:"HTTP or JSON API",networkScan:"Find on local network",networkScanDetail:"Find HTTP/HTTPS services across your local network.",scanMode:"Scan mode",scanQuick:"Quick",scanNormal:"Normal",scanDeep:"Deep",scanWhole:"Whole network .1–.254",scanProgress:"Scanning",scanHosts:"Devices",scanServices:"Services",scanActive:"active",scanLimits:"Scriptable can discover HTTP/HTTPS services. Devices without a web interface may not appear.",githubAdd:"GitHub",githubAddDetail:"Repository, Actions or latest release.",deviceSource:"Device source",deviceSourceDetail:"Optional JSON client list from a router, controller or server. Adds hostname, MAC and vendor.",deviceSourceConfigured:"Device source configured",deviceSourceNone:"No device source",deviceSourceUse:"Use device source",deviceSourceUrl:"Device list URL",deviceSourceUrlHint:"JSON endpoint. Home Dashboard will try to detect fields automatically.",deviceSourceAdvanced:"Advanced JSON mapping",deviceSourceListPath:"List path",deviceSourceIpPath:"IP field",deviceSourceNamePath:"Name / hostname field",deviceSourceMacPath:"MAC field",deviceSourceVendorPath:"Vendor field",deviceSourceAuth:"Authorization",deviceSourceAuthHint:"Optional. For example Bearer … or Basic …; stored only in Keychain.",deviceSourceTest:"Test source",deviceSourceSaved:"Device source saved.",deviceSourceFound:"devices found",deviceSourceEmpty:"The source returned no usable devices.",networkDevice:"Network device",mac:"MAC",vendor:"Vendor",hostname:"Hostname",autoFind:"Find devices automatically",autoFindDetail:"You do not need to know an IP address, subnet or ports. Home Dashboard will try to find the network and suggest services to monitor.",autoDetecting:"Finding your network",autoDetected:"Network found",autoSearching:"Finding devices and services",autoFailed:"The network could not be detected automatically. Open Advanced and enter it manually.",recommended:"Recommended to monitor",watch:"Monitor",watching:"Monitoring",manualScan:"Manual scan",expertOptions:"Advanced",expertDetail:"Manual subnet, ports and external device source. Not needed for normal use.",nothingFound:"No automatically monitorable service was found.",servicesOnDevice:"Services on device",watchDevice:"Monitor device",servicePorts:"ports",openNow:"Open",openAction:"Open from Home Dashboard",openActionDetail:"Choose what the Open button in the monitor list should launch.",openDefault:"Monitor default address",openCustom:"Custom URL / app",openNone:"Open nothing",openCustomUrl:"Custom URL or URL scheme",openCustomHint:"For example https://example.com or myapp://...",openShortcut:"Shortcut",shortcutName:"Shortcut name",shortcutHint:"A Shortcut can open almost any app using the Open App action.",subnet:"Network / subnet",range:"Host range",ports:"Ports",scan:"Scan",scanHint:"For a typical home network use range 1–254. Quick scans common ports; Deep scans many more.",scanNone:"No HTTP services found.",scanFound:"Discovered services",addThis:"Add",added:"Added",addDevice:"Add device",services:"services",device:"Device",unknownService:"Unknown web service",githubRepo:"Repository",githubRepoHint:"owner/repository",githubMode:"What to monitor",githubRepoStatus:"Repository availability",githubActions:"Latest GitHub Action",githubRelease:"Latest release",githubToken:"GitHub token (optional)",githubTokenHint:"The token is stored only in Scriptable Keychain and is not exported.",saveToken:"Save token",removeToken:"Remove token",tokenSaved:"A token is stored in Keychain.",tokenMissing:"No token – public repositories work through the GitHub API.",tokenStored:"GitHub token saved.",tokenRemoved:"GitHub token removed.",error:"Error"
  },
  de:{
    settings:"Einstellungen",update:"Update",current:"Aktuelle Version",available:"Update verfügbar",apply:"Aktualisieren",cancel:"Abbrechen",updatedOk:"Update installiert. Skript erneut starten.",updateFail:"Update-Prüfung fehlgeschlagen.",subtitle:"Eigene Websites, Server und JSON-APIs an einem Ort überwachen.",
    monitors:"Monitore",monitorsDetail:"Eigene Dienste hinzufügen und Anzeige auswählen.",preview:"Widget-Vorschau",previewDetail:"Small / Medium / Large + Demo.",
    appearance:"Widget-Aussehen",appearanceDetail:"Titel, Farben und sichtbare Details.",behavior:"Verhalten",behaviorDetail:"Intervall, Timeout und Sprache.",
    tools:"Werkzeuge",toolsDetail:"Monitore testen, Export, Import und Cache-Reset.",back:"Zurück",add:"Hinzufügen",save:"Speichern",delete:"Löschen",edit:"Bearbeiten",help:"Hilfe",templates:"Vorlage wählen",advanced:"Erweitert",advancedDetail:"Die meisten Benutzer müssen diese Felder nicht ändern.",defaultTimeoutHint:"0 = Standard-Timeout aus Verhalten verwenden.",templateWeb:"Website / HTTP",templateWebDetail:"Einfache Prüfung, ob Website oder Dienst antwortet.",templateHomebridge:"Homebridge",templateHomebridgeDetail:"Üblicher Homebridge-Port 8581 wird vorbelegt.",templateLocal:"Lokaler Dienst",templateLocalDetail:"NAS, Router, Server oder anderer Webdienst im LAN.",templateJson:"JSON API",templateJsonDetail:"Wert aus einer JSON-Antwort prüfen.",templateCustom:"Benutzerdefiniert",templateCustomDetail:"Leeres Formular mit allen Optionen.",helpIntro:"Home Dashboard einrichten",helpIntroDetail:"Mit einer Vorlage beginnen. Für eine normale Website reichen Name und URL.",helpWebTitle:"1. Website / HTTP",helpWebBody:"Beispiel: Name Meine Website, URL https://example.com. Methode, Header und Timeout müssen normalerweise nicht geändert werden.",helpHomebridgeTitle:"2. Homebridge",helpHomebridgeBody:"Beispiel: http://192.168.1.50:8581. Wenn dort die Homebridge-Oberfläche erscheint, ist die URL korrekt.",helpJsonTitle:"3. JSON API",helpJsonBody:"Wenn die API { status: online }, JSON-Pfad status und erwarteten Wert online setzen.",helpNetworkTitle:"4. Lokales Netzwerk",helpNetworkBody:"Im lokalen Netzwerk suchen verwenden. Erste drei IP-Teile eingeben, z. B. 192.168.1.",helpGithubTitle:"5. GitHub",helpGithubBody:"owner/repository eingeben. Öffentliche Repositories benötigen keinen Token; private Tokens werden im Keychain gespeichert.",
    name:"Name",icon:"Icon",type:"Typ",url:"URL",method:"Methode",http:"HTTP / Website",json:"JSON API",jsonPath:"JSON-Pfad",expected:"Erwarteter Wert",
    expectedHint:"Leer = jede gültige Antwort.",headers:"HTTP-Header (JSON)",headersHint:'Beispiel: {"Authorization":"Bearer …"}',enabled:"Aktiv",showWidget:"Im Widget anzeigen",
    timeout:"Timeout",seconds:"s",addMonitor:"Monitor hinzufügen",editMonitor:"Monitor bearbeiten",none:"Noch keine Monitore.",noSelection:"Keine Monitore im Widget",
    noSelectionDetail:"Monitor hinzufügen und Im Widget anzeigen aktivieren.",small:"Small",medium:"Medium",large:"Large",realPreview:"Live-Daten",demoPreview:"Demo",
    widgetTitle:"Widget-Titel",visibility:"Sichtbarkeit",showLatency:"Antwortzeit anzeigen",showValue:"JSON-Wert anzeigen",showTime:"Prüfzeit anzeigen",
    customColors:"Eigene Farben",useCustomColors:"Eigene Farben verwenden",backgroundColor:"Hintergrundfarbe",textColor:"Textfarbe",mutedColor:"Sekundärtextfarbe",okColor:"Online / OK Farbe",failColor:"Offline / Fehler Farbe",
    resetAppearance:"Aussehen zurücksetzen",refresh:"Widget-Aktualisierung",refreshDetail:"Gewünschtes Intervall. iOS kann später aktualisieren.",minutes:"Min",language:"Sprache",
    languageDetail:"Sprache der App und des Widgets.",defaultTimeout:"Standard-Timeout",testAll:"Alle Monitore testen",resetCache:"Cache zurücksetzen",
    export:"Einstellungen exportieren",import:"Einstellungen importieren",exportWarning:"Der Export ist eine vollständige Sicherung der Einstellungen. Er kann private IP-Adressen, URLs, eigene URL-Schemata und HTTP-Header enthalten. Nicht öffentlich teilen.",copied:"Einstellungen kopiert.",imported:"Einstellungen importiert.",invalid:"Ungültiges JSON.",cacheReset:"Cache zurückgesetzt.",
    online:"Online",offline:"Offline",checked:"Geprüft",allGood:"Alles in Ordnung",problems:n=>`${n} Problem${n===1?"":"e"}`,saveHint:"Änderungen werden automatisch gespeichert.",firstRun:"Sprache wählen",testResult:"Testergebnis",addType:"Monitor hinzufügen",manualAdd:"Manuell",manualAddDetail:"HTTP oder JSON API",networkScan:"Im lokalen Netzwerk suchen",networkScanDetail:"Findet HTTP/HTTPS-Dienste im gesamten lokalen Netzwerk.",scanMode:"Scan-Modus",scanQuick:"Schnell",scanNormal:"Normal",scanDeep:"Gründlich",scanWhole:"Ganzes Netz .1–.254",scanProgress:"Suche",scanHosts:"Geräte",scanServices:"Dienste",scanActive:"aktiv",scanLimits:"Scriptable findet HTTP/HTTPS-Dienste. Geräte ohne Weboberfläche werden möglicherweise nicht angezeigt.",githubAdd:"GitHub",githubAddDetail:"Repository, Actions oder letzter Release.",deviceSource:"Gerätequelle",deviceSourceDetail:"Optionale JSON-Clientliste von Router, Controller oder Server. Ergänzt Hostname, MAC und Hersteller.",deviceSourceConfigured:"Gerätequelle eingerichtet",deviceSourceNone:"Keine Gerätequelle",deviceSourceUse:"Gerätequelle verwenden",deviceSourceUrl:"URL der Geräteliste",deviceSourceUrlHint:"JSON-Endpunkt. Home Dashboard versucht die Felder automatisch zu erkennen.",deviceSourceAdvanced:"Erweitertes JSON-Mapping",deviceSourceListPath:"Pfad zur Liste",deviceSourceIpPath:"IP-Feld",deviceSourceNamePath:"Name-/Hostname-Feld",deviceSourceMacPath:"MAC-Feld",deviceSourceVendorPath:"Hersteller-Feld",deviceSourceAuth:"Authorization",deviceSourceAuthHint:"Optional. Z. B. Bearer … oder Basic …; nur im Keychain gespeichert.",deviceSourceTest:"Quelle testen",deviceSourceSaved:"Gerätequelle gespeichert.",deviceSourceFound:"Geräte gefunden",deviceSourceEmpty:"Die Quelle lieferte keine verwendbaren Geräte.",networkDevice:"Netzwerkgerät",mac:"MAC",vendor:"Hersteller",hostname:"Hostname",autoFind:"Geräte automatisch finden",autoFindDetail:"Du musst weder IP-Adresse, Subnetz noch Ports kennen. Home Dashboard versucht das Netzwerk zu finden und schlägt Dienste zur Überwachung vor.",autoDetecting:"Netzwerk wird gesucht",autoDetected:"Netzwerk gefunden",autoSearching:"Geräte und Dienste werden gesucht",autoFailed:"Das Netzwerk konnte nicht automatisch erkannt werden. Öffne Erweitert und gib es manuell ein.",recommended:"Zur Überwachung empfohlen",watch:"Überwachen",watching:"Überwacht",manualScan:"Manuelle Suche",expertOptions:"Erweitert",expertDetail:"Manuelles Subnetz, Ports und externe Gerätequelle. Für normale Nutzung nicht nötig.",nothingFound:"Kein automatisch überwachbarer Dienst gefunden.",servicesOnDevice:"Dienste auf Gerät",watchDevice:"Gerät überwachen",servicePorts:"Ports",openNow:"Öffnen",openAction:"Aus Home Dashboard öffnen",openActionDetail:"Lege fest, was die Schaltfläche Öffnen in der Monitorliste startet.",openDefault:"Standardadresse des Monitors",openCustom:"Eigene URL / App",openNone:"Nichts öffnen",openCustomUrl:"Eigene URL oder URL-Schema",openCustomHint:"Zum Beispiel https://example.com oder meineapp://...",openShortcut:"Kurzbefehl",shortcutName:"Name des Kurzbefehls",shortcutHint:"Ein Kurzbefehl kann mit der Aktion App öffnen fast jede App starten.",subnet:"Netz / Subnetz",range:"Host-Bereich",ports:"Ports",scan:"Suchen",scanHint:"Für ein typisches Heimnetz Bereich 1–254 verwenden. Schnell prüft häufige Ports; Gründlich deutlich mehr.",scanNone:"Keine HTTP-Dienste gefunden.",scanFound:"Gefundene Dienste",addThis:"Hinzufügen",added:"Hinzugefügt",addDevice:"Gerät hinzufügen",services:"Dienste",device:"Gerät",unknownService:"Unbekannter Webdienst",githubRepo:"Repository",githubRepoHint:"owner/repository",githubMode:"Überwachung",githubRepoStatus:"Repository-Erreichbarkeit",githubActions:"Letzte GitHub Action",githubRelease:"Letzter Release",githubToken:"GitHub-Token (optional)",githubTokenHint:"Der Token wird nur im Scriptable Keychain gespeichert und nicht exportiert.",saveToken:"Token speichern",removeToken:"Token löschen",tokenSaved:"Token ist im Keychain gespeichert.",tokenMissing:"Ohne Token – öffentliche Repositories funktionieren über die GitHub API.",tokenStored:"GitHub-Token gespeichert.",tokenRemoved:"GitHub-Token entfernt.",error:"Fehler"
  },
  es:{
    settings:"Ajustes",update:"Actualización",current:"Versión actual",available:"Actualización disponible",apply:"Actualizar",cancel:"Cancelar",updatedOk:"Actualización instalada. Ejecuta el script otra vez.",updateFail:"Falló la búsqueda de actualización.",subtitle:"Supervisa tus webs, servidores y APIs JSON en un solo lugar.",monitors:"Monitores",monitorsDetail:"Añade servicios y elige qué mostrar.",
    preview:"Vista previa",previewDetail:"Small / Medium / Large + demo.",appearance:"Apariencia",appearanceDetail:"Título, colores y detalles visibles.",behavior:"Comportamiento",behaviorDetail:"Intervalo, timeout e idioma.",
    tools:"Herramientas",toolsDetail:"Prueba monitores, exportación, importación y caché.",back:"Atrás",add:"Añadir",save:"Guardar",delete:"Eliminar",edit:"Editar",help:"Ayuda",templates:"Elegir plantilla",advanced:"Avanzado",advancedDetail:"La mayoría de usuarios no necesita cambiar estos campos.",defaultTimeoutHint:"0 = usar el timeout predeterminado de Comportamiento.",templateWeb:"Web / HTTP",templateWebDetail:"Comprueba de forma sencilla si una web o servicio responde.",templateHomebridge:"Homebridge",templateHomebridgeDetail:"Rellena el puerto habitual 8581 de Homebridge.",templateLocal:"Servicio local",templateLocalDetail:"NAS, router, servidor u otro servicio web de la LAN.",templateJson:"API JSON",templateJsonDetail:"Comprueba un valor de una respuesta JSON.",templateCustom:"Personalizado",templateCustomDetail:"Formulario vacío con todas las opciones.",helpIntro:"Cómo configurar Home Dashboard",helpIntroDetail:"Empieza con una plantilla. Para una web normal bastan nombre y URL.",helpWebTitle:"1. Web / HTTP",helpWebBody:"Ejemplo: Nombre Mi web, URL https://example.com. Normalmente no hace falta cambiar método, cabeceras ni timeout.",helpHomebridgeTitle:"2. Homebridge",helpHomebridgeBody:"Ejemplo: http://192.168.1.50:8581. Si allí abre Homebridge, la URL es correcta.",helpJsonTitle:"3. API JSON",helpJsonBody:"Si la API devuelve { status: online }, usa ruta JSON status y valor esperado online.",helpNetworkTitle:"4. Red local",helpNetworkBody:"Usa Buscar en red local. Introduce las tres primeras partes de la IP, p. ej. 192.168.1.",helpGithubTitle:"5. GitHub",helpGithubBody:"Introduce owner/repository. Los repos públicos no necesitan token; los privados usan Keychain.",
    name:"Nombre",icon:"Icono",type:"Tipo",url:"URL",method:"Método",http:"HTTP / web",json:"JSON API",jsonPath:"Ruta JSON",expected:"Valor esperado",
    expectedHint:"Vacío = cualquier respuesta válida.",headers:"Cabeceras HTTP (JSON)",headersHint:'Ejemplo: {"Authorization":"Bearer …"}',enabled:"Activo",showWidget:"Mostrar en widget",
    timeout:"Timeout",seconds:"s",addMonitor:"Añadir monitor",editMonitor:"Editar monitor",none:"Todavía no hay monitores.",noSelection:"Sin monitores en el widget",
    noSelectionDetail:"Añade un monitor y activa Mostrar en widget.",small:"Small",medium:"Medium",large:"Large",realPreview:"Datos reales",demoPreview:"Demo",
    widgetTitle:"Título del widget",visibility:"Visibilidad",showLatency:"Mostrar respuesta",showValue:"Mostrar valor JSON",showTime:"Mostrar hora",
    customColors:"Colores personalizados",useCustomColors:"Usar colores personalizados",backgroundColor:"Color de fondo",textColor:"Color del texto",mutedColor:"Color del texto secundario",okColor:"Color Online / OK",failColor:"Color Offline / error",
    resetAppearance:"Restablecer apariencia",refresh:"Actualización",refreshDetail:"Intervalo solicitado. iOS puede actualizar más tarde.",minutes:"min",language:"Idioma",
    languageDetail:"Idioma de la app y del widget.",defaultTimeout:"Timeout predeterminado",testAll:"Probar todos",resetCache:"Restablecer caché",
    export:"Exportar ajustes",import:"Importar ajustes",exportWarning:"La exportación es una copia de seguridad completa de los ajustes. Puede contener IP privadas, URLs, esquemas URL personalizados y cabeceras HTTP. No la compartas públicamente.",copied:"Ajustes copiados.",imported:"Ajustes importados.",invalid:"JSON no válido.",cacheReset:"Caché restablecida.",
    online:"Online",offline:"Offline",checked:"Comprobado",allGood:"Todo correcto",problems:n=>`${n} problema${n===1?"":"s"}`,saveHint:"Los cambios se guardan automáticamente.",firstRun:"Elige idioma",testResult:"Resultado",addType:"Añadir monitor",manualAdd:"Manual",manualAddDetail:"HTTP o API JSON",networkScan:"Buscar en red local",networkScanDetail:"Busca servicios HTTP/HTTPS en toda la red local.",scanMode:"Modo de búsqueda",scanQuick:"Rápido",scanNormal:"Normal",scanDeep:"Profundo",scanWhole:"Toda la red .1–.254",scanProgress:"Buscando",scanHosts:"Dispositivos",scanServices:"Servicios",scanActive:"activos",scanLimits:"Scriptable puede detectar servicios HTTP/HTTPS. Los dispositivos sin interfaz web pueden no aparecer.",githubAdd:"GitHub",githubAddDetail:"Repositorio, Actions o último release.",deviceSource:"Fuente de dispositivos",deviceSourceDetail:"Lista JSON opcional de clientes de un router, controlador o servidor. Añade hostname, MAC y fabricante.",deviceSourceConfigured:"Fuente configurada",deviceSourceNone:"Sin fuente de dispositivos",deviceSourceUse:"Usar fuente de dispositivos",deviceSourceUrl:"URL de lista de dispositivos",deviceSourceUrlHint:"Endpoint JSON. Home Dashboard intentará detectar los campos automáticamente.",deviceSourceAdvanced:"Mapeo JSON avanzado",deviceSourceListPath:"Ruta de la lista",deviceSourceIpPath:"Campo IP",deviceSourceNamePath:"Campo nombre / hostname",deviceSourceMacPath:"Campo MAC",deviceSourceVendorPath:"Campo fabricante",deviceSourceAuth:"Authorization",deviceSourceAuthHint:"Opcional. Por ejemplo Bearer … o Basic …; se guarda solo en Keychain.",deviceSourceTest:"Probar fuente",deviceSourceSaved:"Fuente guardada.",deviceSourceFound:"dispositivos encontrados",deviceSourceEmpty:"La fuente no devolvió dispositivos utilizables.",networkDevice:"Dispositivo de red",mac:"MAC",vendor:"Fabricante",hostname:"Hostname",autoFind:"Buscar dispositivos automáticamente",autoFindDetail:"No necesitas conocer IP, subred ni puertos. Home Dashboard intentará encontrar la red y sugerirá servicios para vigilar.",autoDetecting:"Buscando tu red",autoDetected:"Red encontrada",autoSearching:"Buscando dispositivos y servicios",autoFailed:"No se pudo detectar la red automáticamente. Abre Avanzado e introdúcela manualmente.",recommended:"Recomendado para vigilar",watch:"Vigilar",watching:"Vigilando",manualScan:"Búsqueda manual",expertOptions:"Avanzado",expertDetail:"Subred manual, puertos y fuente externa. No es necesario para el uso normal.",nothingFound:"No se encontró ningún servicio que se pueda vigilar automáticamente.",servicesOnDevice:"Servicios del dispositivo",watchDevice:"Vigilar dispositivo",servicePorts:"puertos",openNow:"Abrir",openAction:"Abrir desde Home Dashboard",openActionDetail:"Elige qué debe abrir el botón Abrir de la lista de monitores.",openDefault:"Dirección predeterminada del monitor",openCustom:"URL / app personalizada",openNone:"No abrir nada",openCustomUrl:"URL o esquema de URL personalizado",openCustomHint:"Por ejemplo https://example.com o miapp://...",openShortcut:"Atajo",shortcutName:"Nombre del atajo",shortcutHint:"Un atajo puede abrir casi cualquier app mediante la acción Abrir app.",subnet:"Red / subnet",range:"Rango de hosts",ports:"Puertos",scan:"Buscar",scanHint:"Para una red doméstica típica usa 1–254. Rápido prueba puertos comunes; Profundo prueba muchos más.",scanNone:"No se encontraron servicios HTTP.",scanFound:"Servicios encontrados",addThis:"Añadir",added:"Añadido",addDevice:"Añadir dispositivo",services:"servicios",device:"Dispositivo",unknownService:"Servicio web desconocido",githubRepo:"Repositorio",githubRepoHint:"owner/repository",githubMode:"Qué supervisar",githubRepoStatus:"Disponibilidad del repositorio",githubActions:"Última GitHub Action",githubRelease:"Último release",githubToken:"Token de GitHub (opcional)",githubTokenHint:"El token se guarda solo en Scriptable Keychain y no se exporta.",saveToken:"Guardar token",removeToken:"Eliminar token",tokenSaved:"Hay un token guardado en Keychain.",tokenMissing:"Sin token – los repositorios públicos funcionan mediante la API de GitHub.",tokenStored:"Token de GitHub guardado.",tokenRemoved:"Token de GitHub eliminado.",error:"Error"
  }
};

const DEFAULTS={language:null,refreshMinutes:30,defaultTimeout:6,widgetTitle:"Home Dashboard",showLatency:true,showValue:true,showTime:true,useCustomColors:false,backgroundColor:"#0B1020",textColor:"#F8FAFC",mutedColor:"#94A3B8",okColor:"#34C759",failColor:"#FF453A",networkSource:{enabled:false,url:"",listPath:"",ipPath:"",namePath:"",macPath:"",vendorPath:""},monitors:[]};
function clone(x){return JSON.parse(JSON.stringify(x))}
function clamp(n,a,b){return Math.max(a,Math.min(b,n))}
function esc(s){return String(s??"").replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[m]))}
function lang(){const l=(Device.language()||"en").slice(0,2).toLowerCase();return["cs","en","de","es"].includes(l)?l:"en"}
function tx(s,k){const L=T[s.language||lang()]||T.en;return L[k]??T.en[k]??k}
function uid(){return `m${Date.now().toString(36)}${Math.random().toString(36).slice(2,7)}`}
function normalizeNetworkSource(raw){
  const x=raw&&typeof raw==="object"?raw:{};
  return{
    enabled:x.enabled===true,
    url:String(x.url||"").trim(),
    listPath:String(x.listPath||"").trim(),
    ipPath:String(x.ipPath||"").trim(),
    namePath:String(x.namePath||"").trim(),
    macPath:String(x.macPath||"").trim(),
    vendorPath:String(x.vendorPath||"").trim()
  }
}
function normalizeMonitor(raw){
  const type=["http","json","github","network"].includes(raw?.type)?raw.type:"http";
  return{
    id:String(raw?.id||uid()),
    name:String(raw?.name||"").trim().slice(0,60),
    icon:String(raw?.icon||"🌐").trim().slice(0,8)||"🌐",
    type,
    url:String(raw?.url||"").trim(),
    method:["GET","HEAD"].includes(raw?.method)?raw.method:"GET",
    headers:String(raw?.headers||"{}"),
    jsonPath:String(raw?.jsonPath||"").trim(),
    expected:String(raw?.expected??"").trim(),
    githubRepo:String(raw?.githubRepo||"").trim(),
    githubMode:["repo","actions","release"].includes(raw?.githubMode)?raw.githubMode:"repo",
    networkIp:String(raw?.networkIp||"").trim(),
    networkMac:String(raw?.networkMac||"").trim(),
    networkVendor:String(raw?.networkVendor||"").trim(),
    openMode:(raw?.openMode==="livecontainer"?"custom":(["default","custom","shortcut","none"].includes(raw?.openMode)?raw.openMode:(type==="network"?"none":"default"))),
    openUrl:String(raw?.openUrl||"").trim(),
    openShortcut:String(raw?.openShortcut||"").trim(),
    enabled:raw?.enabled!==false,
    showWidget:raw?.showWidget!==false,
    timeout:clamp(Number(raw?.timeout)||0,0,30)
  }
}
function merge(raw){
  const s=Object.assign(clone(DEFAULTS),raw||{});
  if(!["cs","en","de","es"].includes(s.language))s.language=null;
  s.refreshMinutes=clamp(Number(s.refreshMinutes)||30,15,180);
  s.defaultTimeout=clamp(Number(s.defaultTimeout)||6,2,30);
  s.widgetTitle=String(s.widgetTitle||"Home Dashboard").slice(0,40);
  for(const k of["showLatency","showValue","showTime","useCustomColors"])if(typeof s[k]!=="boolean")s[k]=DEFAULTS[k];
  for(const k of["backgroundColor","textColor","mutedColor","okColor","failColor"])if(!/^#[0-9a-fA-F]{6}$/.test(String(s[k]||"")))s[k]=DEFAULTS[k];
  s.networkSource=normalizeNetworkSource(s.networkSource);
  s.monitors=(Array.isArray(s.monitors)?s.monitors:[])
    .map(normalizeMonitor)
    .filter(m=>m.name&&(m.type==="network"?!!m.networkIp:!!m.url));
  return s
}
function loadSettings(){try{if(fm.fileExists(settingsPath))return merge(JSON.parse(fm.readString(settingsPath)))}catch(e){console.log(e)}return clone(DEFAULTS)}
function saveSettings(s){try{fm.writeString(settingsPath,JSON.stringify(merge(s),null,2))}catch(e){console.log(e)}}
async function firstLanguage(s){if(s.language)return s;if(config.runsInWidget){s.language=lang();saveSettings(s);return s}const a=new Alert();a.title=APP_NAME;a.message=tx({...s,language:lang()},"firstRun");["🇨🇿 Čeština","🇬🇧 English","🇩🇪 Deutsch","🇪🇸 Español"].forEach(x=>a.addAction(x));const i=await a.presentAlert();s.language=["cs","en","de","es"][Math.max(0,i)]||"en";saveSettings(s);return s}
function loadState(){try{if(!fm.fileExists(statePath))return{last:{},updatedAt:null};const p=JSON.parse(fm.readString(statePath));return{last:p.last||{},updatedAt:p.updatedAt||null}}catch(_){return{last:{},updatedAt:null}}}
function saveState(s){try{fm.writeString(statePath,JSON.stringify(s,null,2))}catch(_){}}
function resetState(){try{if(fm.fileExists(statePath))fm.remove(statePath)}catch(_){}}
function parseHeaders(text){try{const x=JSON.parse(String(text||"{}"));if(!x||Array.isArray(x)||typeof x!=="object")return{};const out={};for(const[k,v]of Object.entries(x))out[String(k)]=String(v);return out}catch(_){return{}}}
function getPath(obj,path){if(!path)return obj;const parts=String(path).replace(/\[(\d+)\]/g,".$1").split(".").filter(Boolean);let v=obj;for(const p of parts){if(v==null)return undefined;v=v[p]}return v}
function valueText(v){if(v===undefined)return"—";if(v===null)return"null";if(typeof v==="object"){try{return JSON.stringify(v).slice(0,80)}catch(_){return"[object]"}}return String(v).slice(0,80)}
function timeoutAfter(ms,label="Monitor"){return new Promise((_,reject)=>Timer.schedule(ms,false,()=>reject(new Error(`${label} timeout`))))}
function githubHeaders(){const h={"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2022-11-28","User-Agent":"Home-Dashboard"};try{if(Keychain.contains(GITHUB_TOKEN_KEY)){const t=Keychain.get(GITHUB_TOKEN_KEY);if(t)h.Authorization=`Bearer ${t}`}}catch(_){}return h}
async function checkGitHub(m,defaultTimeout){const started=Date.now(),timeout=clamp(Number(m.timeout)||Number(defaultTimeout)||6,2,30),repo=String(m.githubRepo||"").trim();try{if(!/^[^/\s]+\/[^/\s]+$/.test(repo))throw new Error("Invalid repository");let url=`https://api.github.com/repos/${repo}`,value="",ok=true;if(m.githubMode==="actions")url+=`/actions/runs?per_page=1`;else if(m.githubMode==="release")url+=`/releases/latest`;const r=new Request(url);r.timeoutInterval=timeout;r.headers=githubHeaders();const data=await r.loadJSON();const status=Number(r.response?.statusCode||200);ok=status>=200&&status<400;if(m.githubMode==="actions"){const run=Array.isArray(data?.workflow_runs)?data.workflow_runs[0]:null;if(run){const state=String(run.conclusion||run.status||"unknown");value=state;ok=ok&&!['failure','cancelled','timed_out','action_required','stale','startup_failure'].includes(state)}else value="no runs"}else if(m.githubMode==="release"){value=String(data?.tag_name||data?.name||"no release")}else value=String(data?.default_branch||data?.full_name||repo);return{id:m.id,name:m.name,icon:m.icon,kind:"github",ok,status,latency:Date.now()-started,value,checkedAt:Date.now(),cached:false}}catch(e){return{id:m.id,name:m.name,icon:m.icon,kind:"github",ok:false,status:0,latency:Date.now()-started,value:"",checkedAt:Date.now(),cached:false,error:String(e?.message||e).slice(0,120)}}}
async function checkOne(m,defaultTimeout){if(m.type==="github")return await checkGitHub(m,defaultTimeout);const started=Date.now(),timeout=clamp(Number(m.timeout)||Number(defaultTimeout)||6,2,30);try{const r=new Request(m.url);r.method=m.method||"GET";r.timeoutInterval=timeout;r.headers=parseHeaders(m.headers);let value="";if(m.type==="json"){const data=await r.loadJSON();value=m.jsonPath?getPath(data,m.jsonPath):data}else await r.load();const status=Number(r.response?.statusCode||200);let ok=status>=200&&status<400;if(ok&&m.type==="json"&&m.expected!=="")ok=String(value)===String(m.expected);return{id:m.id,name:m.name,icon:m.icon,kind:m.type,ok,status,latency:Date.now()-started,value:m.type==="json"?valueText(value):"",checkedAt:Date.now(),cached:false}}catch(e){return{id:m.id,name:m.name,icon:m.icon,kind:m.type,ok:false,status:0,latency:Date.now()-started,value:"",checkedAt:Date.now(),cached:false,error:String(e?.message||e).slice(0,120)}}}
function decodeHtmlText(v){
  return String(v||"")
    .replace(/&nbsp;/gi," ")
    .replace(/&amp;/gi,"&")
    .replace(/&quot;/gi,'"')
    .replace(/&#39;/gi,"'")
    .replace(/&lt;/gi,"<")
    .replace(/&gt;/gi,">")
    .replace(/\s+/g," ")
    .trim()
}
function scanJsonName(raw){
  try{
    const j=JSON.parse(raw);
    const candidates=[
      j?.name,j?.title,j?.hostname,j?.host,j?.deviceName,j?.device_name,
      j?.productName,j?.product,j?.model,j?.serviceName,j?.serverName,
      j?.application,j?.appName,j?.instanceName,j?.friendly_name
    ];
    for(const v of candidates){
      if(typeof v==="string"&&v.trim())return v.trim().slice(0,80)
    }
  }catch(_){}
  return ""
}
function scanHtmlTitle(raw){
  const m=String(raw||"").match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  return m?decodeHtmlText(m[1]).slice(0,80):""
}
function scanHtmlMeta(raw){
  const s=String(raw||"");
  const patterns=[
    /<meta[^>]+name=["']application-name["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']application-name["']/i,
    /<meta[^>]+name=["']apple-mobile-web-app-title["'][^>]+content=["']([^"']+)["']/i,
    /<meta[^>]+content=["']([^"']+)["'][^>]+name=["']apple-mobile-web-app-title["']/i
  ];
  for(const re of patterns){
    const m=s.match(re);
    if(m&&m[1])return decodeHtmlText(m[1]).slice(0,80)
  }
  return ""
}
function scanHtmlH1(raw){
  const m=String(raw||"").match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  if(!m)return "";
  return decodeHtmlText(String(m[1]).replace(/<[^>]+>/g," ")).slice(0,80)
}
function scanHeader(headers,key){
  if(!headers||typeof headers!=="object")return "";
  const wanted=String(key).toLowerCase();
  for(const [k,v] of Object.entries(headers)){
    if(String(k).toLowerCase()===wanted)return String(v||"")
  }
  return ""
}
function cleanProductName(v){
  let s=decodeHtmlText(v||"")
    .replace(/<[^>]+>/g," ")
    .replace(/\s+/g," ")
    .replace(/\s*[|–—-]\s*(login|sign in|dashboard|web interface|administration).*$/i,"")
    .trim();

  if(!s)return "";

  const lower=s.toLowerCase();
  const exactJunk=[
    "home","login","index","dashboard","welcome","web service",
    "not found","page not found","error"
  ];
  if(exactJunk.includes(lower))return "";
  if(lower.startsWith("404")||lower.startsWith("400")||lower.startsWith("401")||
     lower.startsWith("403")||lower.startsWith("500"))return "";

  const serverPrefixes=["httpd/","apache/","nginx/","caddy/","lighttpd/","openresty/","microsoft-iis/","goahead-webs/"];
  if(serverPrefixes.some(p=>lower.startsWith(p)))return "";
  if(["httpd","apache","nginx","caddy","lighttpd","openresty","microsoft-iis","goahead-webs"].includes(lower))return "";

  return s.slice(0,80)
}
function fingerprintKnownService(raw,meta={}){
  const hay=[
    raw||"",meta.title||"",meta.htmlMeta||"",meta.h1||"",
    meta.jsonName||"",meta.server||"",meta.poweredBy||"",
    meta.auth||"",meta.location||""
  ].join(" ").toLowerCase();

  const signatures=[
    [["homebridge"],"Homebridge","🏠"],
    [["atvloadly","atv loadly"],"ATVLoadly","📺"],
    [["tailscale"],"Tailscale","🔗"],
    [["home assistant","home-assistant"],"Home Assistant","🏠"],
    [["proxmox"],"Proxmox","🖥️"],
    [["synology","diskstation","dsm"],"Synology NAS","💾"],
    [["qnap","qts"],"QNAP NAS","💾"],
    [["truenas","freenas"],"TrueNAS","💾"],
    [["portainer"],"Portainer","🐳"],
    [["docker"],"Docker service","🐳"],
    [["grafana"],"Grafana","📊"],
    [["prometheus"],"Prometheus","📊"],
    [["jellyfin"],"Jellyfin","🎬"],
    [["plex"],"Plex","🎬"],
    [["emby"],"Emby","🎬"],
    [["nextcloud"],"Nextcloud","☁️"],
    [["immich"],"Immich","📷"],
    [["frigate"],"Frigate","📹"],
    [["esphome"],"ESPHome","🔌"],
    [["node-red","nodered"],"Node-RED","🔴"],
    [["uptime kuma","uptime-kuma"],"Uptime Kuma","📈"],
    [["adguard home","adguardhome"],"AdGuard Home","🛡️"],
    [["pi-hole","pihole"],"Pi-hole","🛡️"],
    [["openwrt","luci"],"OpenWrt / LuCI","📡"],
    [["opnsense"],"OPNsense","🛡️"],
    [["pfsense"],"pfSense","🛡️"],
    [["unifi","ubiquiti"],"UniFi","📡"],
    [["omada"],"TP-Link Omada","📡"],
    [["cockpit"],"Cockpit","🖥️"],
    [["nginx proxy manager"],"Nginx Proxy Manager","🌐"],
    [["sonarr"],"Sonarr","📺"],
    [["radarr"],"Radarr","🎬"],
    [["lidarr"],"Lidarr","🎵"],
    [["prowlarr"],"Prowlarr","🔎"],
    [["sabnzbd"],"SABnzbd","📥"],
    [["qbittorrent"],"qBittorrent","⬇️"],
    [["transmission"],"Transmission","⬇️"],
    [["syncthing"],"Syncthing","🔄"],
    [["paperless"],"Paperless-ngx","📄"],
    [["vaultwarden","bitwarden"],"Vaultwarden","🔐"]
  ];
  for(const [needles,name,icon] of signatures){
    if(needles.some(n=>hay.includes(n)))return{name,icon,confidence:"signature"}
  }
  return null
}
function guessServiceName({port,title,jsonName,server,htmlMeta,h1,poweredBy,auth,location,raw}){
  const fp=fingerprintKnownService(raw,{title,jsonName,server,htmlMeta,h1,poweredBy,auth,location});
  if(fp)return fp;

  for(const candidate of [jsonName,htmlMeta,title,h1]){
    const cleaned=cleanProductName(candidate);
    if(cleaned)return{name:cleaned,icon:jsonName?"🖥️":"🌐",confidence:"page"}
  }

  const portNames={
    1880:["Node-RED?","🔴"],
    3000:["Grafana / web app?","📊"],
    3001:["Web app?","🌐"],
    5000:["Synology / web service?","💾"],
    5001:["Synology HTTPS?","💾"],
    5252:["Tailscale Web?","🔗"],
    5533:["ATVLoadly?","📺"],
    6052:["ESPHome?","🔌"],
    8006:["Proxmox?","🖥️"],
    8080:["Web service","🌐"],
    8096:["Jellyfin?","🎬"],
    8123:["Home Assistant?","🏠"],
    8384:["Syncthing?","🔄"],
    8581:["Homebridge?","🏠"],
    8686:["Lidarr?","🎵"],
    7878:["Radarr?","🎬"],
    8989:["Sonarr?","📺"],
    9000:["Portainer / web service?","🐳"],
    9090:["Prometheus / web service?","📊"],
    9091:["Transmission?","⬇️"],
    9443:["Portainer HTTPS?","🐳"],
    9696:["Prowlarr?","🔎"],
    32400:["Plex?","🎬"]
  };
  if(portNames[Number(port)])return{name:portNames[Number(port)][0],icon:portNames[Number(port)][1],confidence:"port"};

  const srv=cleanProductName(server);
  if(srv&&!/^(nginx|apache|caddy|lighttpd|openresty|microsoft-iis)$/i.test(srv)){
    return{name:srv,icon:"🌐",confidence:"server"}
  }
  return{name:"Web service",icon:"🌐",confidence:"generic"}
}
async function fetchFingerprintPath(baseUrl,path,timeoutSec=0.8){
  try{
    const u=String(baseUrl).replace(/\/$/,"")+path;
    const r=new Request(u);
    r.method="GET";
    r.timeoutInterval=timeoutSec;
    if(u.startsWith("https://"))r.allowInsecureRequest=true;
    const data=await r.load();
    let raw="";
    try{raw=data?.toRawString?data.toRawString():""}catch(_){}
    raw=String(raw||"").slice(0,12000);
    const headers=r.response?.headers||{};
    return{
      raw,
      status:Number(r.response?.statusCode||0),
      server:scanHeader(headers,"server"),
      poweredBy:scanHeader(headers,"x-powered-by"),
      auth:scanHeader(headers,"www-authenticate"),
      location:scanHeader(headers,"location"),
      jsonName:scanJsonName(raw),
      title:scanHtmlTitle(raw),
      htmlMeta:scanHtmlMeta(raw),
      h1:scanHtmlH1(raw)
    }
  }catch(_){return null}
}
async function enrichGenericService(result,timeoutSec=0.8){
  if(!result||result.confidence!=="generic")return result;
  const paths=["/api/status","/api/info","/status"];
  for(const path of paths){
    const probe=await fetchFingerprintPath(result.url,path,timeoutSec);
    if(!probe)continue;
    const fp=fingerprintKnownService(probe.raw,probe);
    if(fp)return{...result,name:fp.name,icon:fp.icon,confidence:"fingerprint",fingerprintPath:path};
    const candidate=cleanProductName(probe.jsonName||probe.htmlMeta||probe.title||probe.h1);
    if(candidate)return{...result,name:candidate,icon:"🖥️",confidence:"fingerprint",fingerprintPath:path}
  }
  return result
}
function scanProtocol(port){
  return [443,5001,8006,8443,9443,10443].includes(Number(port))?"https":"http"
}
function scanUrl(ip,port){
  const protocol=scanProtocol(port);
  const defaultPort=(protocol==="https"&&Number(port)===443)||(protocol==="http"&&Number(port)===80);
  return `${protocol}://${ip}${defaultPort?"":":"+port}/`
}
async function probeEndpoint(ip,port,timeoutSec=0.55){
  const url=scanUrl(ip,port),protocol=scanProtocol(port),started=Date.now();
  try{
    const r=new Request(url);
    r.method="HEAD";
    r.timeoutInterval=timeoutSec;
    if(protocol==="https")r.allowInsecureRequest=true;
    await r.load();
    const status=Number(r.response?.statusCode||0);
    if(status<=0)return null;
    return{ip,port:Number(port),url,status,latency:Date.now()-started}
  }catch(_){
    return null
  }
}
async function scanEndpoint(ip,port,timeoutSec=1.0){
  const url=scanUrl(ip,port),protocol=scanProtocol(port),started=Date.now();
  try{
    const r=new Request(url);
    r.method="GET";
    r.timeoutInterval=timeoutSec;
    if(protocol==="https")r.allowInsecureRequest=true;
    const data=await r.load();
    const status=Number(r.response?.statusCode||0);
    if(status<=0)return null;

    let raw="";
    try{raw=data?.toRawString?data.toRawString():""}catch(_){}
    raw=String(raw||"").slice(0,24000);

    const headers=r.response?.headers||{};
    const contentType=scanHeader(headers,"content-type").toLowerCase();
    const server=scanHeader(headers,"server");
    const poweredBy=scanHeader(headers,"x-powered-by");
    const auth=scanHeader(headers,"www-authenticate");
    const location=scanHeader(headers,"location");
    const jsonName=(contentType.includes("json")||raw.trim().startsWith("{"))?scanJsonName(raw):"";
    const title=scanHtmlTitle(raw);
    const htmlMeta=scanHtmlMeta(raw);
    const h1=scanHtmlH1(raw);
    const meta=guessServiceName({port,title,jsonName,server,htmlMeta,h1,poweredBy,auth,location,raw});

    let result={
      ip,port:Number(port),url,status,latency:Date.now()-started,
      name:meta.name,icon:meta.icon,confidence:meta.confidence||"",
      title,jsonName,htmlMeta,h1,
      server:String(server||"").slice(0,80),
      poweredBy:String(poweredBy||"").slice(0,80),
      location:String(location||"").slice(0,120)
    };

    if(result.confidence==="generic"){
      result=await enrichGenericService(result,Math.min(0.9,timeoutSec))
    }
    return result
  }catch(_){
    return null
  }
}
function normalizeScanPorts(ports){
  const ps=(Array.isArray(ports)?ports:String(ports||"").split(","))
    .map(x=>Number(String(x).trim()))
    .filter(x=>Number.isInteger(x)&&x>0&&x<=65535);
  return [...new Set(ps)].slice(0,40)
}
async function runPool(items,limit,worker,onProgress=null){
  const out=[];
  let next=0,done=0,lastReport=0;
  async function runner(){
    while(true){
      const i=next++;
      if(i>=items.length)return;
      let value=null;
      try{value=await worker(items[i],i)}catch(_){}
      if(value!==null&&value!==undefined){
        if(Array.isArray(value))out.push(...value);
        else out.push(value)
      }
      done++;
      const now=Date.now();
      if(onProgress&&(done===items.length||done-lastReport>=4||now-lastReport>700)){
        lastReport=done;
        try{await onProgress(done,items.length,out.length)}catch(_){}
      }
    }
  }
  const n=Math.min(Math.max(1,limit),Math.max(1,items.length));
  await Promise.all(Array.from({length:n},()=>runner()));
  return out
}
async function discoverHost(ip,probePorts,timeoutSec){
  // Probe only a few ports at a time. This avoids hundreds of simultaneous
  // requests, which can make the Scriptable WebView/network stack stall.
  for(let i=0;i<probePorts.length;i+=2){
    const group=probePorts.slice(i,i+2);
    const hits=await Promise.all(group.map(port=>probeEndpoint(ip,port,timeoutSec)));
    const hit=hits.find(Boolean);
    if(hit)return hit
  }
  return null
}
const AUTO_SUBNET_CANDIDATES=[
  "192.168.1","192.168.0","10.0.0","10.0.1",
  "192.168.50","192.168.68","192.168.31","192.168.8",
  "192.168.2","192.168.100","10.1.1","172.16.0"
];
const AUTO_SCAN_PORTS=[80,443,1880,3000,5000,5001,5252,5533,8000,8006,8080,8081,8096,8123,8384,8443,8581,8888,9000,9090,9443,9696,32400];

async function detectLocalSubnet(onProgress=null){
  const targets=[];
  const sampleHosts=[1,254,2,10,100];
  const probePorts=[80,443,8080];

  for(const base of AUTO_SUBNET_CANDIDATES){
    for(const host of sampleHosts){
      for(const port of probePorts){
        targets.push({base,ip:`${base}.${host}`,port})
      }
    }
  }

  const hits=await runPool(
    targets,
    10,
    async x=>{
      const r=await probeEndpoint(x.ip,x.port,0.42);
      return r?{base:x.base,hit:r}:null
    },
    async(done,total,count)=>{
      if(onProgress)await onProgress(done,total,count)
    }
  );

  if(!hits.length)return null;

  const score=new Map();
  for(const h of hits){
    const cur=score.get(h.base)||{base:h.base,count:0,router:false};
    cur.count++;
    if(h.hit&&((h.hit.ip.endsWith(".1"))||(h.hit.ip.endsWith(".254"))))cur.router=true;
    score.set(h.base,cur)
  }

  return [...score.values()]
    .sort((a,b)=>(Number(b.router)-Number(a.router))||(b.count-a.count))[0]?.base||null
}
async function scanLocalNetwork(base,startHost,endHost,ports,mode="quick",onProgress=null){
  base=String(base||"").trim().replace(/\.$/,"");
  if(!/^\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(base))throw new Error("Invalid subnet");

  let a=clamp(Number(startHost)||1,1,254),b=clamp(Number(endHost)||254,1,254);
  if(b<a)[a,b]=[b,a];

  let ps=normalizeScanPorts(ports);
  if(!ps.length)ps=[80,443,8080,8581,3000,8123,8006];

  const allHosts=[];
  for(let h=a;h<=b;h++)allHosts.push(`${base}.${h}`);

  // Phase 1: find hosts that expose at least one likely web service.
  const quickCore=[80,443,8080,8581,8123,8006,5000,5001,5252,5533,3000];
  const normalCore=[80,443,8080,8581,8123,8006,5000,5001,5252,5533,3000,8443,32400,9000];
  const deepCore=ps;
  const probePorts=mode==="deep"?deepCore:(mode==="normal"?normalCore:quickCore);
  const probeTimeout=mode==="deep"?0.8:(mode==="normal"?0.65:0.5);
  const hostWorkers=mode==="deep"?6:(mode==="normal"?8:10);

  const active=await runPool(
    allHosts,
    hostWorkers,
    async ip=>await discoverHost(ip,probePorts,probeTimeout),
    async(done,total,found)=>{
      if(onProgress)await onProgress("hosts",done,total,found)
    }
  );

  if(!active.length)return[];

  // Phase 2: only scan the requested ports on hosts that actually answered.
  const activeIps=[...new Set(active.map(x=>x.ip))];
  const endpoints=[];
  for(const ip of activeIps)for(const port of ps)endpoints.push({ip,port});

  const detailTimeout=mode==="deep"?1.3:(mode==="normal"?1.05:0.85);
  const endpointWorkers=mode==="deep"?8:10;

  const found=await runPool(
    endpoints,
    endpointWorkers,
    async e=>await scanEndpoint(e.ip,e.port,detailTimeout),
    async(done,total,count)=>{
      if(onProgress)await onProgress("services",done,total,count,activeIps.length)
    }
  );

  const unique=new Map();
  for(const x of found)unique.set(`${x.ip}:${x.port}`,x);
  return [...unique.values()].sort((x,y)=>x.ip.localeCompare(y.ip,{numeric:true})||x.port-y.port)
}
function getNetworkSourceAuth(){
  try{return Keychain.contains(NETWORK_SOURCE_AUTH_KEY)?String(Keychain.get(NETWORK_SOURCE_AUTH_KEY)||""):""}catch(_){return ""}
}
function firstPathValue(obj,paths){
  for(const p of paths){
    if(!p)continue;
    const v=getPath(obj,p);
    if(v!==undefined&&v!==null&&String(v).trim()!=="")return v
  }
  return undefined
}
function autoDeviceRows(data,source){
  if(source?.listPath){
    const x=getPath(data,source.listPath);
    if(Array.isArray(x))return x
  }
  if(Array.isArray(data))return data;

  for(const p of["clients","devices","hosts","leases","nodes","stations","items","results","data.clients","data.devices","data.hosts","data.items","result.clients","result.devices"]){
    const x=getPath(data,p);
    if(Array.isArray(x))return x
  }

  const queue=[{v:data,d:0}];
  while(queue.length){
    const cur=queue.shift();
    if(!cur.v||typeof cur.v!=="object"||cur.d>2)continue;
    for(const v of Object.values(cur.v)){
      if(Array.isArray(v)&&v.length){
        const sample=v.find(x=>x&&typeof x==="object"&&!Array.isArray(x));
        if(sample){
          const keys=Object.keys(sample).map(x=>x.toLowerCase());
          if(keys.some(x=>["ip","ipaddress","ip_address","ipv4","address","hostname","mac","macaddress","mac_address"].includes(x)))return v
        }
      }else if(v&&typeof v==="object"&&!Array.isArray(v)){
        queue.push({v,d:cur.d+1})
      }
    }
  }
  return []
}
function normalizeMac(v){
  const s=String(v||"").trim().toUpperCase().split("-").join(":");
  const parts=s.split(":");
  return parts.length===6&&parts.every(x=>x.length===2)?s:String(v||"").trim()
}
function normalizeInventoryDevice(row,source){
  if(!row||typeof row!=="object")return null;

  const ip=String(firstPathValue(row,[
    source?.ipPath,"ip","ipAddress","ip_address","ipv4","ipv4Address","address","hostIp","host_ip","lanIp","localIp"
  ])||"").trim();
  const parts=ip.split(".");
  if(parts.length!==4||!parts.every(x=>x!==""&&Number(x)>=0&&Number(x)<=255))return null;

  const name=String(firstPathValue(row,[
    source?.namePath,"name","hostname","hostName","host_name","deviceName","device_name","clientName","client_name","alias","friendlyName","friendly_name"
  ])||"").trim();
  const mac=normalizeMac(firstPathValue(row,[
    source?.macPath,"mac","macAddress","mac_address","hwaddr","hardwareAddress","hardware_address"
  ])||"");
  const vendor=String(firstPathValue(row,[
    source?.vendorPath,"vendor","vendorName","vendor_name","manufacturer","brand","ouiVendor","oui_vendor"
  ])||"").trim();

  return{ip,name:name.slice(0,80),mac:mac.slice(0,32),vendor:vendor.slice(0,80)}
}
async function fetchNetworkInventory(source){
  source=normalizeNetworkSource(source);
  if(!source.enabled||!source.url)return[];

  const r=new Request(source.url);
  r.method="GET";
  r.timeoutInterval=6;
  if(source.url.startsWith("https://"))r.allowInsecureRequest=true;
  const auth=getNetworkSourceAuth();
  if(auth)r.headers={Authorization:auth};

  const data=await r.loadJSON();
  const rows=autoDeviceRows(data,source);
  const out=[],seen=new Set();
  for(const row of rows){
    const d=normalizeInventoryDevice(row,source);
    if(!d)continue;
    const key=d.mac||d.ip;
    if(seen.has(key))continue;
    seen.add(key);
    out.push(d)
  }
  return out
}
function inventoryMatch(inventory,m){
  const mac=normalizeMac(m.networkMac||"");
  if(mac){
    const hit=inventory.find(d=>normalizeMac(d.mac||"")===mac);
    if(hit)return hit
  }
  return inventory.find(d=>d.ip===m.networkIp)||null
}
function networkMonitorResult(m,inventory){
  const hit=inventoryMatch(inventory,m);
  return{
    id:m.id,name:m.name,icon:m.icon,kind:"network",
    ok:!!hit,status:hit?200:0,latency:0,
    value:hit?(hit.vendor||hit.name||hit.mac||hit.ip):"",
    checkedAt:Date.now(),cached:false,
    error:hit?"":"Device not found"
  }
}
function cachedResults(settings){const st=loadState(),out=[];for(const m of settings.monitors.filter(x=>x.enabled)){const c=st.last[m.id];if(c)out.push({...c,cached:true});else out.push({id:m.id,name:m.name,icon:m.icon,ok:false,status:0,latency:0,value:"",checkedAt:0,cached:true,error:"No cached data"})}return out}
async function checkAll(settings,budgetMs=null){
  const monitors=settings.monitors.filter(m=>m.enabled);
  if(!monitors.length)return[];

  const task=(async()=>{
    let inventory=[];
    if(monitors.some(m=>m.type==="network")){
      try{inventory=await fetchNetworkInventory(settings.networkSource)}catch(e){console.log("Network source: "+e)}
    }
    return await Promise.all(monitors.map(m=>m.type==="network"?Promise.resolve(networkMonitorResult(m,inventory)):checkOne(m,settings.defaultTimeout)))
  })();

  let results;
  if(budgetMs){
    try{results=await Promise.race([task,timeoutAfter(budgetMs,"Widget")])}
    catch(e){console.log(e);return cachedResults(settings)}
  }else results=await task;

  const st=loadState();
  for(const r of results)st.last[r.id]=r;
  st.updatedAt=new Date().toISOString();
  saveState(st);
  return results
}

function cmp(a,b){const A=String(a).split(".").map(Number),B=String(b).split(".").map(Number);for(let i=0;i<Math.max(A.length,B.length);i++){if((A[i]||0)>(B[i]||0))return 1;if((A[i]||0)<(B[i]||0))return-1}return 0}
async function getString(url){const r=new Request(url);r.timeoutInterval=API_TIMEOUT;return await r.loadString()}
async function updater(s){try{const src=await getString(UPDATE_SOURCE_URL);if(!src||src.length<UPDATE_MIN_BYTES||!src.includes('const APP_NAME = "Home Dashboard"'))throw new Error("Bad source");const m=src.match(/const APP_VERSION\s*=\s*"([^"]+)"/);if(!m)throw new Error("No version");const v=m[1];if(cmp(v,APP_VERSION)<=0)return{ok:true,text:`${tx(s,"current")} v${APP_VERSION}`};const a=new Alert();a.title=APP_NAME;a.message=`${tx(s,"available")}: v${v}`;a.addAction(tx(s,"apply"));a.addCancelAction(tx(s,"cancel"));if(await a.presentAlert()!==0)return{ok:true,text:`v${APP_VERSION} → v${v}`};const target=module.filename;if(!target)throw new Error("Current script path unavailable");const cloud=FileManager.iCloud(),local=FileManager.local();let targetFm=local;if(cloud.fileExists(target)){targetFm=cloud;if(!cloud.isFileDownloaded(target))await cloud.downloadFileFromiCloud(target)}else if(!local.fileExists(target))throw new Error("Current script file not found");const b=/\.js$/i.test(target)?target.replace(/\.js$/i,`_backup_v${APP_VERSION}.js`):target+`_backup_v${APP_VERSION}.js`;try{targetFm.writeString(b,targetFm.readString(target))}catch(_){}targetFm.writeString(target,src);return{ok:true,text:tx(s,"updatedOk")}}catch(e){console.log(e);return{ok:false,text:tx(s,"updateFail")}}}
function demoResults(){return[{id:"1",name:"Homebridge",icon:"🏠",ok:true,status:200,latency:43,value:"",checkedAt:Date.now()},{id:"2",name:"NAS",icon:"💾",ok:true,status:200,latency:18,value:"",checkedAt:Date.now()},{id:"3",name:"Server",icon:"🖥️",ok:false,status:0,latency:1200,value:"",checkedAt:Date.now(),error:"timeout"},{id:"4",name:"Internet",icon:"🌐",ok:true,status:204,latency:27,value:"",checkedAt:Date.now()},{id:"5",name:"Temperature",icon:"🌡️",ok:true,status:200,latency:31,value:"42.5",checkedAt:Date.now()}]}
function colors(s){if(s.useCustomColors)return{bg:new Color(s.backgroundColor),text:new Color(s.textColor),muted:new Color(s.mutedColor),ok:new Color(s.okColor),fail:new Color(s.failColor),blue:new Color("0A84FF")};return{bg:Color.dynamic(new Color("F5F7FB"),new Color("0B1020")),text:Color.dynamic(new Color("111827"),new Color("F8FAFC")),muted:Color.dynamic(new Color("6B7280"),new Color("94A3B8")),ok:new Color("34C759"),fail:new Color("FF453A"),blue:new Color("0A84FF")}}
function layoutForFamily(f){if(f==="small")return{maxRows:0,title:14,row:11,detail:9,pad:11,gap:5};if(f==="large")return{maxRows:8,title:17,row:14,detail:11,pad:15,gap:7};return{maxRows:4,title:16,row:13,detail:10,pad:13,gap:6}}
async function buildWidget(results,settings,familyOverride,showAllResults=false){const family=familyOverride||config.widgetFamily||"medium",L=layoutForFamily(family),c=colors(settings),w=new ListWidget();w.backgroundColor=c.bg;w.setPadding(L.pad,L.pad,L.pad,L.pad);try{w.url=URLScheme.forRunningScript()}catch(_){w.url="scriptable://"}const shownIds=new Set(settings.monitors.filter(m=>m.enabled&&m.showWidget).map(m=>m.id));let rows=showAllResults?results.slice():results.filter(r=>shownIds.has(r.id));const bad=rows.filter(r=>!r.ok).length,good=rows.length-bad;const header=w.addStack();header.setPadding(0,0,0,8);header.centerAlignContent();const sym=SFSymbol.named("house.fill");sym.applyFont(Font.semiboldSystemFont(L.title));const img=header.addImage(sym.image);img.imageSize=new Size(L.title,L.title);img.tintColor=c.blue;header.addSpacer(7);const title=header.addText(settings.widgetTitle||APP_NAME);title.font=Font.boldSystemFont(L.title);title.textColor=c.text;title.lineLimit=1;header.addSpacer();if(bad){const b=header.addText(String(bad));b.font=Font.boldSystemFont(L.detail+1);b.textColor=c.fail}else if(rows.length){const ok=header.addText("✓");ok.font=Font.boldSystemFont(L.title);ok.textColor=c.ok;if(family==="medium")header.addSpacer(56)}w.addSpacer(family==="small"?8:10);if(!rows.length){const body=w.addStack();body.layoutVertically();body.addSpacer();const plus=body.addText("＋");plus.font=Font.boldSystemFont(family==="small"?24:30);plus.textColor=c.blue;plus.centerAlignText();body.addSpacer(4);const msg=body.addText(tx(settings,"noSelection"));msg.font=Font.semiboldSystemFont(family==="small"?10:13);msg.textColor=c.text;msg.centerAlignText();msg.lineLimit=2;body.addSpacer()}else if(family==="small"){const body=w.addStack();body.layoutVertically();body.addSpacer();const big=body.addText(bad?`⚠ ${bad}`:`✓ ${good}`);big.font=Font.boldSystemFont(24);big.textColor=bad?c.fail:c.ok;big.centerAlignText();body.addSpacer(5);const sub=body.addText(bad?tx(settings,"problems")(bad):tx(settings,"allGood"));sub.font=Font.semiboldSystemFont(10);sub.textColor=c.text;sub.centerAlignText();sub.lineLimit=2;body.addSpacer()}else{rows=rows.slice(0,L.maxRows);for(let i=0;i<rows.length;i++){const r=rows[i],line=w.addStack();line.setPadding(0,8,0,8);line.centerAlignContent();const icon=line.addText(r.icon||"•");icon.font=Font.systemFont(L.row);line.addSpacer(7);const name=line.addText(r.name);name.font=Font.semiboldSystemFont(L.row);name.textColor=c.text;name.lineLimit=1;line.addSpacer();let detail="";if(settings.showValue&&r.value)detail+=r.value+" · ";if(settings.showLatency&&r.latency)detail+=`${r.latency} ms · `;detail+=r.kind==="github"?(r.ok?"OK":tx(settings,"error")):(r.ok?tx(settings,"online"):tx(settings,"offline"));const d=line.addText(detail);d.font=Font.systemFont(L.detail);d.textColor=r.ok?c.ok:c.fail;d.lineLimit=1;if(i<rows.length-1)w.addSpacer(L.gap)}}w.addSpacer();if(settings.showTime){const st=loadState(),when=st.updatedAt?new Date(st.updatedAt):new Date();const df=new DateFormatter();df.useNoDateStyle();df.useShortTimeStyle();const footRow=w.addStack();footRow.addSpacer();const foot=footRow.addText(df.string(when));foot.font=Font.systemFont(L.detail);foot.textColor=c.muted;foot.lineLimit=1;footRow.addSpacer()}w.refreshAfterDate=new Date(Date.now()+settings.refreshMinutes*60000);return w}
async function presentWidget(w,f){if(f==="small")return await w.presentSmall();if(f==="large")return await w.presentLarge();return await w.presentMedium()}
function nav(screen,icon,title,detail=""){return `<div class="navRow" onclick="showScreen('${screen}')"><div class="navLeft"><span class="navIcon">${icon}</span><span>${esc(title)}</span></div><div class="navRight"><span class="navDetail">${esc(detail)}</span><span class="chevron">›</span></div></div>`}
function githubTokenConfigured(){try{return Keychain.contains(GITHUB_TOKEN_KEY)}catch(_){return false}}
function settingsHTML(s){const L=T[s.language||"en"]||T.en;return `<!doctype html><html lang="${s.language||"en"}"><head><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>
:root{color-scheme:dark;--bg:#0b1020;--panel:#111827;--panel2:#172033;--border:#2a3850;--text:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--ok:#86efac;--danger:#fb7185}*{box-sizing:border-box}html,body{margin:0;min-height:100%;color:var(--text);font-family:system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-tap-highlight-color:transparent}html{background:#070b14}body{padding:calc(14px + env(safe-area-inset-top)) 14px calc(36px + env(safe-area-inset-bottom));max-width:680px;margin:auto;background:radial-gradient(circle at top,#172554 0,#0b1020 42%,#070b14 100%);background-attachment:fixed}.screen{display:none}.screen.active{display:block}.topbar{display:flex;align-items:center;justify-content:space-between;min-height:42px;margin:0 2px 8px}.back{border:0;background:transparent;color:var(--accent);font:inherit;font-size:16px;font-weight:750;padding:7px 0}.hero{background:rgba(17,24,39,.96);border:1px solid var(--border);border-radius:22px;padding:22px;margin-bottom:14px;box-shadow:0 24px 70px rgba(0,0,0,.45)}.eyebrow{display:inline-flex;align-items:center;padding:6px 10px;border:1px solid #1d4ed8;border-radius:999px;background:#0f1f46;color:#bfdbfe;font-size:.78rem;font-weight:700}.hero h1,.screenTitle{font-size:27px;line-height:1.15;margin:14px 0 6px;font-weight:800;letter-spacing:-.45px}.screenTitle{margin:5px 2px 6px}.hero p,.screenSub{color:var(--muted);font-size:14px;line-height:1.5;margin:0}.screenSub{margin:0 2px 14px}.updateStatus{min-height:17px;margin-top:8px;color:var(--muted);font-size:11px}.updateStatus.ok{color:var(--ok)}.updateStatus.error{color:var(--danger)}.sectionTitle{font-size:11px;color:#9fb3ce;text-transform:uppercase;letter-spacing:.1em;font-weight:800;margin:19px 9px 8px}.card{background:rgba(17,24,39,.96);border:1px solid var(--border);border-radius:18px;overflow:hidden;margin-bottom:13px;box-shadow:0 12px 34px rgba(0,0,0,.24)}.navRow,.settingRow,.monitorRow{min-height:54px;display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-bottom:1px solid rgba(42,56,80,.85)}.navRow:last-child,.settingRow:last-child,.monitorRow:last-child{border-bottom:0}.navRow:active,.monitorRow:active{background:var(--panel2)}.navLeft{display:flex;gap:11px;align-items:center;font-size:15px;font-weight:700;min-width:0}.navIcon{width:26px;text-align:center}.navRight{display:flex;align-items:center;gap:8px}.navDetail,.rowDetail{font-size:12px;color:var(--muted)}.navDetail{max-width:190px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.chevron{font-size:23px;color:#64748b}.rowText{min-width:0;padding-right:11px}.rowTitle{font-size:15px;font-weight:650;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.rowDetail{margin-top:3px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.field{padding:12px 14px;border-bottom:1px solid rgba(42,56,80,.85)}.field:last-child{border-bottom:0}.field label{display:block;margin-bottom:7px;color:#dbeafe;font-size:.82rem;font-weight:650}input[type=text],input[type=url],input[type=number],input[type=password],select,textarea{width:100%;min-height:46px;border:1px solid var(--border);border-radius:12px;background:#0b1220;color:var(--text);padding:0 13px;font:inherit;font-size:15px;outline:none}textarea{min-height:100px;padding:12px;resize:vertical;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px}.colorControl{display:grid;grid-template-columns:58px 1fr;gap:10px;align-items:center}.colorPicker{width:58px;height:46px;border:1px solid var(--border);border-radius:12px;background:#0b1220;padding:4px;overflow:hidden}.colorPicker::-webkit-color-swatch-wrapper{padding:0}.colorPicker::-webkit-color-swatch{border:0;border-radius:8px}.colorCode{text-transform:uppercase;font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.previewGrid,.actionGrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:13px}.actionGrid{grid-template-columns:1fr 1fr;padding:12px}.btn{min-height:48px;border:1px solid #1d4ed8;border-radius:13px;background:linear-gradient(135deg,#0369a1,#0284c7);color:#fff;font:inherit;font-weight:800;font-size:13px}.btn.secondary{background:#243149;border-color:var(--border)}.btn.danger{background:#3a1720;border-color:#6b2738;color:#fecdd3}.btn.full{grid-column:1/-1}.switch{position:relative;width:48px;height:28px;flex:0 0 48px}.switch input{opacity:0;width:0;height:0}.slider{position:absolute;inset:0;border-radius:999px;background:#334155;transition:.2s}.slider:before{content:"";position:absolute;width:22px;height:22px;left:3px;top:3px;border-radius:50%;background:white;transition:.2s}.switch input:checked+.slider{background:#0a84ff}.switch input:checked+.slider:before{transform:translateX(20px)}.choiceIcon{width:38px;height:38px;border-radius:11px;background:#0f1f46;display:grid;place-items:center;font-size:20px;flex:0 0 38px}.scanResult{min-height:58px;display:flex;align-items:center;justify-content:space-between;padding:9px 14px;border-bottom:1px solid rgba(42,56,80,.85)}.deviceGroup{border-bottom:1px solid rgba(42,56,80,.9)}.deviceGroup:last-child{border-bottom:0}.deviceHead{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:13px 14px;background:rgba(15,31,70,.28)}.deviceName{font-size:16px;font-weight:800}.deviceMeta{font-size:12px;color:var(--muted);margin-top:3px}.serviceRow{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:9px 14px 9px 22px;border-top:1px solid rgba(42,56,80,.55)}.serviceInfo{min-width:0}.serviceTitle{font-size:14px;font-weight:800}.serviceDetail{font-size:11px;color:var(--muted);margin-top:2px}.deviceBtn{min-height:34px;border:1px solid #2563eb;border-radius:12px;background:#0f1f46;color:#bfdbfe;font:inherit;font-size:12px;font-weight:800;padding:0 11px;white-space:nowrap}.deviceBtn:disabled{opacity:.55}.scanResult:last-child{border-bottom:0}.miniBtn{border:1px solid #1d4ed8;border-radius:10px;background:#0f1f46;color:#bfdbfe;padding:7px 10px;font:inherit;font-size:12px;font-weight:800}.pill{font-size:11px;font-weight:800;color:#bfdbfe;background:#0f1f46;border:1px solid #1d4ed8;padding:5px 8px;border-radius:999px;white-space:nowrap}.heroTop{display:flex;align-items:center;justify-content:space-between;gap:10px}.updateBtn{border:1px solid #1d4ed8;border-radius:999px;background:#0f1f46;color:#bfdbfe;padding:6px 10px;font:inherit;font-size:12px;font-weight:800}.templateIcon{width:42px;height:42px;border-radius:12px;background:#0f1f46;display:grid;place-items:center;font-size:22px;flex:0 0 42px}.hintBox{margin:0 0 13px;padding:12px 14px;border:1px solid var(--border);border-radius:14px;background:var(--panel2);color:#cbd5e1;font-size:13px;line-height:1.5}.hintBox b{color:#f8fafc}.advanced{margin:0;border-top:1px solid rgba(42,56,80,.85)}.advanced summary{list-style:none;cursor:pointer;padding:14px;font-size:14px;font-weight:750;color:#dbeafe;display:flex;justify-content:space-between;align-items:center}.advanced summary::-webkit-details-marker{display:none}.advanced summary:after{content:"›";font-size:22px;color:#64748b;transform:rotate(90deg)}.advanced[open] summary:after{transform:rotate(270deg)}.advancedNote{padding:0 14px 10px;color:var(--muted);font-size:12px;line-height:1.4}.status{min-height:20px;color:var(--ok);font-size:12px;padding:0 14px 12px}.empty{padding:22px;text-align:center;color:var(--muted);font-size:13px}.footer{color:#64748b;text-align:center;font-size:.76rem;margin:16px 4px 0}@media(max-width:430px){.hero{padding:18px}.navDetail{max-width:128px}.previewGrid,.actionGrid{grid-template-columns:1fr}.btn.full{grid-column:auto}}
</style></head><body>
<div id="home" class="screen active"><div class="hero"><div class="heroTop"><span class="eyebrow">🏠 CaseyCZ · Scriptable</span><button class="updateBtn" onclick="post({action:'update'})">${esc(L.update)}</button></div><h1>${esc(APP_NAME)}</h1><p>${esc(L.subtitle)}</p><div id="updateStatus" class="updateStatus">${esc(L.current)} · v${esc(APP_VERSION)}</div></div><div class="sectionTitle">${esc(L.settings)}</div><div class="card">${nav("monitors","🖥️",L.monitors,`${s.monitors.length}`)}${nav("preview","👁",L.preview,L.previewDetail)}${nav("appearance","🎨",L.appearance,L.appearanceDetail)}${nav("behavior","⚙️",L.behavior,`${s.refreshMinutes} ${L.minutes}`)}${nav("tools","🧰",L.tools,L.toolsDetail)}${nav("help","❓",L.help,L.helpIntroDetail)}</div><div class="footer">${esc(L.saveHint)}</div></div>
<div id="monitors" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><button class="btn" style="min-height:34px;padding:0 14px" onclick="showScreen('addType')">＋ ${esc(L.add)}</button></div><div class="screenTitle">${esc(L.monitors)}</div><div class="screenSub">${esc(L.monitorsDetail)}</div><div id="monitorList" class="card"></div></div>
<div id="addType" class="screen"><div class="topbar"><button class="back" onclick="showScreen('monitors')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.addType)}</div><div class="card"><div class="navRow" onclick="showScreen('templates')"><div class="navLeft"><span class="choiceIcon">✍️</span><div class="rowText"><div class="rowTitle">${esc(L.manualAdd)}</div><div class="rowDetail">${esc(L.manualAddDetail)}</div></div></div><span class="chevron">›</span></div><div class="navRow" onclick="openNetworkScan()"><div class="navLeft"><span class="choiceIcon">📡</span><div class="rowText"><div class="rowTitle">${esc(L.networkScan)}</div><div class="rowDetail">${esc(L.networkScanDetail)}</div></div></div><span class="chevron">›</span></div><div class="navRow" onclick="newGithub()"><div class="navLeft"><span class="choiceIcon">🐙</span><div class="rowText"><div class="rowTitle">${esc(L.githubAdd)}</div><div class="rowDetail">${esc(L.githubAddDetail)}</div></div></div><span class="chevron">›</span></div></div></div>
<div id="templates" class="screen"><div class="topbar"><button class="back" onclick="showScreen('addType')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.templates)}</div><div class="screenSub">${esc(L.helpIntroDetail)}</div><div class="card">
<div class="navRow" onclick="newMonitor('web')"><div class="navLeft"><span class="templateIcon">🌐</span><div class="rowText"><div class="rowTitle">${esc(L.templateWeb)}</div><div class="rowDetail">${esc(L.templateWebDetail)}</div></div></div><span class="chevron">›</span></div>
<div class="navRow" onclick="newMonitor('homebridge')"><div class="navLeft"><span class="templateIcon">🏠</span><div class="rowText"><div class="rowTitle">${esc(L.templateHomebridge)}</div><div class="rowDetail">${esc(L.templateHomebridgeDetail)}</div></div></div><span class="chevron">›</span></div>
<div class="navRow" onclick="newMonitor('local')"><div class="navLeft"><span class="templateIcon">🖥️</span><div class="rowText"><div class="rowTitle">${esc(L.templateLocal)}</div><div class="rowDetail">${esc(L.templateLocalDetail)}</div></div></div><span class="chevron">›</span></div>
<div class="navRow" onclick="newMonitor('json')"><div class="navLeft"><span class="templateIcon">{ }</span><div class="rowText"><div class="rowTitle">${esc(L.templateJson)}</div><div class="rowDetail">${esc(L.templateJsonDetail)}</div></div></div><span class="chevron">›</span></div>
<div class="navRow" onclick="newMonitor('custom')"><div class="navLeft"><span class="templateIcon">⚙️</span><div class="rowText"><div class="rowTitle">${esc(L.templateCustom)}</div><div class="rowDetail">${esc(L.templateCustomDetail)}</div></div></div><span class="chevron">›</span></div>
</div></div>
<div id="help" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.helpIntro)}</div><div class="screenSub">${esc(L.helpIntroDetail)}</div>
<div class="hintBox"><b>${esc(L.helpWebTitle)}</b><br>${esc(L.helpWebBody)}</div>
<div class="hintBox"><b>${esc(L.helpHomebridgeTitle)}</b><br>${esc(L.helpHomebridgeBody)}</div>
<div class="hintBox"><b>${esc(L.helpJsonTitle)}</b><br>${esc(L.helpJsonBody)}</div>
<div class="hintBox"><b>${esc(L.helpNetworkTitle)}</b><br>${esc(L.helpNetworkBody)}</div>
<div class="hintBox"><b>${esc(L.helpGithubTitle)}</b><br>${esc(L.helpGithubBody)}</div>
</div>
<div id="network" class="screen">
<div class="topbar"><button class="back" onclick="showScreen('addType')">‹ ${esc(L.back)}</button><span></span></div>
<div class="screenTitle">${esc(L.networkScan)}</div>
<div class="screenSub">${esc(L.autoFindDetail)}</div>

<div class="card">
  <div class="field" style="padding:16px">
    <button id="autoScanBtn" class="btn full" style="width:100%;font-size:15px;min-height:58px" onclick="startAutoNetworkScan()">🔎 ${esc(L.autoFind)}</button>
  </div>
  <div id="scanStatus" class="status" style="padding:0 14px 14px"></div>
</div>

<div class="sectionTitle">${esc(L.recommended)}</div>
<div id="scanResults" class="card"><div class="empty">${esc(L.nothingFound)}</div></div>

<details class="advanced" style="margin-top:16px">
  <summary>${esc(L.expertOptions)}</summary>
  <div class="screenSub" style="margin:10px 2px 12px">${esc(L.expertDetail)}</div>

  <div class="card">
    <div class="navRow" onclick="openNetworkSource()">
      <div class="navLeft"><span class="navIcon">📋</span><div class="rowText">
        <div class="rowTitle">${esc(L.deviceSource)}</div>
        <div id="deviceSourceSummary" class="rowDetail">${esc(s.networkSource.enabled&&s.networkSource.url?L.deviceSourceConfigured:L.deviceSourceNone)}</div>
      </div></div><span class="chevron">›</span>
    </div>
  </div>

  <div class="card">
    <div class="field"><label>${esc(L.subnet)}</label><input id="scanBase" type="text" value="192.168.1" placeholder="192.168.1"></div>
    <div class="field"><label>${esc(L.range)}</label><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><input id="scanStart" type="number" min="1" max="254" value="1"><input id="scanEnd" type="number" min="1" max="254" value="254"></div></div>
    <div class="field"><label>${esc(L.scanMode)}</label><select id="scanMode" onchange="applyScanMode()"><option value="quick">${esc(L.scanQuick)}</option><option value="normal" selected>${esc(L.scanNormal)}</option><option value="deep">${esc(L.scanDeep)}</option></select></div>
    <div class="field"><label>${esc(L.ports)}</label><input id="scanPorts" type="text" value="80,443,1880,3000,5000,5001,5252,5533,8000,8006,8080,8081,8096,8123,8384,8443,8581,8888,9000,9090,9443,9696,32400"></div>
    <div class="field"><button id="scanBtn" class="btn secondary" style="width:100%" onclick="startNetworkScan()">📡 ${esc(L.manualScan)}</button></div>
  </div>
</details>
</div>
<div id="networkSource" class="screen">
<div class="topbar"><button class="back" onclick="showScreen('network')">‹ ${esc(L.back)}</button><span></span></div>
<div class="screenTitle">${esc(L.deviceSource)}</div><div class="screenSub">${esc(L.deviceSourceDetail)}</div>
<div class="card">
<label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.deviceSourceUse)}</div></div><span class="switch"><input id="nsEnabled" type="checkbox" ${s.networkSource.enabled?"checked":""}><span class="slider"></span></span></label>
<div class="field"><label>${esc(L.deviceSourceUrl)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.deviceSourceUrlHint)}</div><input id="nsUrl" type="url" value="${esc(s.networkSource.url||"")}" placeholder="http://192.168.1.1/api/clients"></div>
</div>
<div class="card"><details class="advanced"><summary>${esc(L.deviceSourceAdvanced)}</summary>
<div class="field"><label>${esc(L.deviceSourceListPath)}</label><input id="nsListPath" type="text" value="${esc(s.networkSource.listPath||"")}" placeholder="clients"></div>
<div class="field"><label>${esc(L.deviceSourceIpPath)}</label><input id="nsIpPath" type="text" value="${esc(s.networkSource.ipPath||"")}" placeholder="ip"></div>
<div class="field"><label>${esc(L.deviceSourceNamePath)}</label><input id="nsNamePath" type="text" value="${esc(s.networkSource.namePath||"")}" placeholder="hostname"></div>
<div class="field"><label>${esc(L.deviceSourceMacPath)}</label><input id="nsMacPath" type="text" value="${esc(s.networkSource.macPath||"")}" placeholder="mac"></div>
<div class="field"><label>${esc(L.deviceSourceVendorPath)}</label><input id="nsVendorPath" type="text" value="${esc(s.networkSource.vendorPath||"")}" placeholder="vendor"></div>
</details></div>
<div class="card">
<div class="field"><label>${esc(L.deviceSourceAuth)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.deviceSourceAuthHint)}</div><input id="nsAuth" type="text" value="" placeholder="Bearer …"></div>
<div class="actionGrid"><button class="btn secondary" onclick="saveNetworkAuth()">${esc(L.saveToken)}</button><button class="btn secondary" onclick="removeNetworkAuth()">${esc(L.removeToken)}</button></div>
<div id="nsAuthStatus" class="status"></div>
</div>
<div class="actionGrid"><button class="btn" onclick="saveNetworkSource()">${esc(L.save)}</button><button class="btn secondary" onclick="testNetworkSource()">${esc(L.deviceSourceTest)}</button></div>
<div id="nsStatus" class="status"></div>
</div>

<div id="networkEditor" class="screen">
<div class="topbar"><button class="back" onclick="showScreen('monitors')">‹ ${esc(L.back)}</button><span></span></div>
<div class="screenTitle">${esc(L.networkDevice)}</div>
<div class="card">
<div class="field"><label>${esc(L.name)}</label><input id="nName" type="text"></div>
<div class="field"><label>${esc(L.icon)}</label><input id="nIcon" type="text" value="🖥️"></div>
<div class="field"><label>IP</label><input id="nIp" type="text" readonly></div>
<div class="field"><label>${esc(L.mac)}</label><input id="nMac" type="text" readonly></div>
<div class="field"><label>${esc(L.vendor)}</label><input id="nVendor" type="text" readonly></div>
<label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.enabled)}</div></div><span class="switch"><input id="nEnabled" type="checkbox" checked><span class="slider"></span></span></label>
<label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showWidget)}</div></div><span class="switch"><input id="nShowWidget" type="checkbox" checked><span class="slider"></span></span></label>
</div>
<div class="sectionTitle">${esc(L.openAction)}</div><div class="card">
<div class="field"><label>${esc(L.openAction)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.openActionDetail)}</div><select id="nOpenMode" onchange="toggleOpenFields('n')"><option value="default">${esc(L.openDefault)}</option><option value="custom">${esc(L.openCustom)}</option><option value="shortcut">${esc(L.openShortcut)}</option><option value="none">${esc(L.openNone)}</option></select></div>
<div id="nOpenUrlField" class="field" style="display:none"><label>${esc(L.openCustomUrl)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.openCustomHint)}</div><input id="nOpenUrl" type="text" placeholder="myapp://..."></div>

<div id="nShortcutField" class="field" style="display:none"><label>${esc(L.shortcutName)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.shortcutHint)}</div><input id="nOpenShortcut" type="text" placeholder="${esc(L.shortcutName)}"></div>
</div><div class="actionGrid"><button class="btn" onclick="saveNetworkMonitor()">${esc(L.save)}</button><button class="btn danger" onclick="deleteMonitor()">${esc(L.delete)}</button></div>
</div>
<div id="githubEditor" class="screen"><div class="topbar"><button class="back" onclick="showScreen('monitors')">‹ ${esc(L.back)}</button><span></span></div><div id="githubTitle" class="screenTitle">${esc(L.githubAdd)}</div><div class="card"><div class="field"><label>${esc(L.name)}</label><input id="gName" type="text" placeholder="My GitHub"></div><div class="field"><label>${esc(L.icon)}</label><input id="gIcon" type="text" value="🐙"></div><div class="field"><label>${esc(L.githubRepo)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.githubRepoHint)}</div><input id="gRepo" type="text" placeholder="owner/repository"></div><div class="field"><label>${esc(L.githubMode)}</label><select id="gMode"><option value="repo">${esc(L.githubRepoStatus)}</option><option value="actions">${esc(L.githubActions)}</option><option value="release">${esc(L.githubRelease)}</option></select></div><label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.enabled)}</div></div><span class="switch"><input id="gEnabled" type="checkbox" checked><span class="slider"></span></span></label><label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showWidget)}</div></div><span class="switch"><input id="gShowWidget" type="checkbox" checked><span class="slider"></span></span></label></div><div class="sectionTitle">${esc(L.openAction)}</div><div class="card">
<div class="field"><label>${esc(L.openAction)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.openActionDetail)}</div><select id="gOpenMode" onchange="toggleOpenFields('g')"><option value="default">${esc(L.openDefault)}</option><option value="custom">${esc(L.openCustom)}</option><option value="shortcut">${esc(L.openShortcut)}</option><option value="none">${esc(L.openNone)}</option></select></div>
<div id="gOpenUrlField" class="field" style="display:none"><label>${esc(L.openCustomUrl)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.openCustomHint)}</div><input id="gOpenUrl" type="text" placeholder="github://..."></div>

<div id="gShortcutField" class="field" style="display:none"><label>${esc(L.shortcutName)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.shortcutHint)}</div><input id="gOpenShortcut" type="text" placeholder="${esc(L.shortcutName)}"></div>
</div><div class="sectionTitle">GitHub API</div><div class="card"><div class="field"><label>${esc(L.githubToken)}</label><div id="tokenHint" class="rowDetail" style="margin-bottom:8px">${githubTokenConfigured()?esc(L.tokenSaved):esc(L.tokenMissing)}</div><input id="gToken" type="password" autocomplete="off" placeholder="github_pat_…"></div><div class="actionGrid"><button class="btn secondary" onclick="saveGithubToken()">${esc(L.saveToken)}</button><button class="btn danger" onclick="removeGithubToken()">${esc(L.removeToken)}</button></div></div><div class="actionGrid"><button class="btn" onclick="saveGithubMonitor()">${esc(L.save)}</button><button id="gDeleteBtn" class="btn danger" onclick="deleteMonitor()">${esc(L.delete)}</button></div></div>
<div id="editor" class="screen"><div class="topbar"><button class="back" onclick="showScreen('monitors')">‹ ${esc(L.back)}</button><span></span></div><div id="editorTitle" class="screenTitle">${esc(L.addMonitor)}</div><div id="templateHint" class="hintBox"></div><div class="card">
<div class="field"><label>${esc(L.name)}</label><input id="mName" type="text" placeholder="Homebridge"></div>
<div class="field"><label>${esc(L.icon)}</label><input id="mIcon" type="text" value="🌐"></div>
<div class="field"><label>${esc(L.type)}</label><select id="mType" onchange="toggleJsonFields()"><option value="http">${esc(L.http)}</option><option value="json">${esc(L.json)}</option></select></div>
<div class="field"><label>${esc(L.url)}</label><input id="mUrl" type="url" placeholder="https://example.com"></div>
<div id="jsonFields"><div class="field"><label>${esc(L.jsonPath)}</label><input id="mJsonPath" type="text" placeholder="status"></div><div class="field"><label>${esc(L.expected)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.expectedHint)}</div><input id="mExpected" type="text" placeholder="online"></div></div>
<label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.enabled)}</div></div><span class="switch"><input id="mEnabled" type="checkbox" checked><span class="slider"></span></span></label>
<label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showWidget)}</div></div><span class="switch"><input id="mShowWidget" type="checkbox" checked><span class="slider"></span></span></label>
<div class="sectionTitle">${esc(L.openAction)}</div><div class="card">
<div class="field"><label>${esc(L.openAction)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.openActionDetail)}</div><select id="mOpenMode" onchange="toggleOpenFields('m')"><option value="default">${esc(L.openDefault)}</option><option value="custom">${esc(L.openCustom)}</option><option value="shortcut">${esc(L.openShortcut)}</option><option value="none">${esc(L.openNone)}</option></select></div>
<div id="mOpenUrlField" class="field" style="display:none"><label>${esc(L.openCustomUrl)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.openCustomHint)}</div><input id="mOpenUrl" type="text" placeholder="myapp://..."></div>

<div id="mShortcutField" class="field" style="display:none"><label>${esc(L.shortcutName)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.shortcutHint)}</div><input id="mOpenShortcut" type="text" placeholder="${esc(L.shortcutName)}"></div>
</div><details id="advancedFields" class="advanced"><summary>${esc(L.advanced)}</summary><div class="advancedNote">${esc(L.advancedDetail)}</div>
<div class="field"><label>${esc(L.method)}</label><select id="mMethod"><option>GET</option><option>HEAD</option></select></div>
<div class="field"><label>${esc(L.headers)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.headersHint)}</div><textarea id="mHeaders">{}</textarea></div>
<div class="field"><label>${esc(L.timeout)} (${esc(L.seconds)})</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.defaultTimeoutHint)}</div><input id="mTimeout" type="number" min="0" max="30" value="0"></div>
</details></div><div class="actionGrid"><button class="btn" onclick="saveMonitor()">${esc(L.save)}</button><button id="deleteBtn" class="btn danger" onclick="deleteMonitor()">${esc(L.delete)}</button></div></div>
<div id="preview" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.preview)}</div><div class="screenSub">${esc(L.previewDetail)}</div><div class="sectionTitle">${esc(L.realPreview)}</div><div class="previewGrid"><button class="btn" onclick="preview('small',false)">${esc(L.small)}</button><button class="btn" onclick="preview('medium',false)">${esc(L.medium)}</button><button class="btn" onclick="preview('large',false)">${esc(L.large)}</button></div><div class="sectionTitle">${esc(L.demoPreview)}</div><div class="previewGrid"><button class="btn secondary" onclick="preview('small',true)">${esc(L.small)}</button><button class="btn secondary" onclick="preview('medium',true)">${esc(L.medium)}</button><button class="btn secondary" onclick="preview('large',true)">${esc(L.large)}</button></div><div id="previewStatus" class="status"></div></div>
<div id="appearance" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.appearance)}</div><div class="screenSub">${esc(L.appearanceDetail)}</div><div class="card"><div class="field"><label>${esc(L.widgetTitle)}</label><input id="widgetTitle" type="text" maxlength="40" value="${esc(s.widgetTitle)}" oninput="saveAppearance()"></div></div><div class="sectionTitle">${esc(L.visibility)}</div><div class="card"><label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showLatency)}</div></div><span class="switch"><input id="showLatency" type="checkbox" ${s.showLatency?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label><label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showValue)}</div></div><span class="switch"><input id="showValue" type="checkbox" ${s.showValue?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label><label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.showTime)}</div></div><span class="switch"><input id="showTime" type="checkbox" ${s.showTime?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label></div><div class="sectionTitle">${esc(L.customColors)}</div><div class="card"><label class="settingRow"><div class="rowText"><div class="rowTitle">${esc(L.useCustomColors)}</div></div><span class="switch"><input id="useCustomColors" type="checkbox" ${s.useCustomColors?"checked":""} onchange="saveAppearance()"><span class="slider"></span></span></label>${["backgroundColor","textColor","mutedColor","okColor","failColor"].map(id=>`<div class="field"><label>${esc(L[id])}</label><div class="colorControl"><input id="${id}Picker" class="colorPicker" type="color" value="${esc(s[id])}" oninput="syncColorFromPicker('${id}')"><input id="${id}" class="colorCode" type="text" maxlength="7" value="${esc(s[id])}" oninput="syncColorFromText('${id}')"></div></div>`).join("")}</div><div class="actionGrid"><button class="btn secondary full" onclick="resetAppearance()">${esc(L.resetAppearance)}</button></div></div>
<div id="behavior" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.behavior)}</div><div class="screenSub">${esc(L.behaviorDetail)}</div><div class="card"><div class="field"><label>${esc(L.refresh)}</label><div class="rowDetail" style="margin-bottom:8px">${esc(L.refreshDetail)}</div><select id="refreshMinutes" onchange="saveBehavior()">${[15,30,60,120,180].map(v=>`<option value="${v}" ${s.refreshMinutes===v?"selected":""}>${v} ${esc(L.minutes)}</option>`).join("")}</select></div><div class="field"><label>${esc(L.defaultTimeout)} (${esc(L.seconds)})</label><input id="defaultTimeout" type="number" min="2" max="30" value="${s.defaultTimeout}" onchange="saveBehavior()"></div><div class="field"><label>${esc(L.language)}</label><select id="language" onchange="setLanguage(this.value)">${[["cs","Čeština"],["en","English"],["de","Deutsch"],["es","Español"]].map(([v,n])=>`<option value="${v}" ${s.language===v?"selected":""}>${n}</option>`).join("")}</select></div></div></div>
<div id="tools" class="screen"><div class="topbar"><button class="back" onclick="showScreen('home')">‹ ${esc(L.back)}</button><span></span></div><div class="screenTitle">${esc(L.tools)}</div><div class="screenSub">${esc(L.toolsDetail)}</div><div class="hintBox">⚠️ ${esc(L.exportWarning)}</div><div class="actionGrid"><button class="btn full" onclick="post({action:'testAll',settings:state})">${esc(L.testAll)}</button><button class="btn secondary" onclick="post({action:'export'})">${esc(L.export)}</button><button class="btn secondary" onclick="importSettings()">${esc(L.import)}</button><button class="btn danger full" onclick="post({action:'resetCache'})">${esc(L.resetCache)}</button></div><div id="toolStatus" class="status"></div><div class="card"><div class="field"><textarea id="jsonBox">${esc(JSON.stringify(s,null,2))}</textarea></div></div></div>
<script>
let state=${JSON.stringify(s)},editingId=null;window.__nativeQueue=[];function post(m){window.__nativeQueue.push({...m,nonce:Date.now()+Math.random()})}function showScreen(id){document.querySelectorAll('.screen').forEach(x=>x.classList.remove('active'));document.getElementById(id).classList.add('active');if(id==='monitors')renderMonitors()}function saveState(){post({action:'save',settings:state});const b=document.getElementById('jsonBox');if(b)b.value=JSON.stringify(state,null,2)}function defaultOpenUrl(m){
  if(!m)return "";
  if(m.type==="github"&&m.githubRepo)return "https://github.com/"+m.githubRepo;
  if(m.type==="http"||m.type==="json")return m.url||"";
  return ""
}
function shortcutUrl(name,target){
  name=String(name||"").trim();
  if(!name)return "";
  let u="shortcuts://run-shortcut?name="+encodeURIComponent(name);
  target=String(target||"").trim();
  if(target)u+="&input=text&text="+encodeURIComponent(target);
  return u
}
function resolvedOpenUrl(m){
  if(!m)return "";
  const mode=m.openMode||((m.type==="network")?"none":"default");
  if(mode==="none")return "";

  const def=defaultOpenUrl(m);
  const target=String(m.openUrl||"").trim()||def;

  if(mode==="custom")return String(m.openUrl||"").trim();
  if(mode==="shortcut")return shortcutUrl(m.openShortcut,target);
  return def
}
function openMonitor(id){
  const m=state.monitors.find(x=>x.id===id);
  if(!m)return;
  const url=resolvedOpenUrl(m);
  if(url)post({action:'openUrl',url})
}
function toggleOpenFields(prefix){
  const modeEl=document.getElementById(prefix+'OpenMode');
  const mode=modeEl?modeEl.value:'default';
  const urlField=document.getElementById(prefix+'OpenUrlField');
  const shortcutField=document.getElementById(prefix+'ShortcutField');

  if(urlField)urlField.style.display=(mode==='custom'||mode==='shortcut')?'block':'none';
  if(shortcutField)shortcutField.style.display=mode==='shortcut'?'block':'none'
}
function setOpenControls(prefix,m,defaultMode){
  const mode=document.getElementById(prefix+'OpenMode');
  const url=document.getElementById(prefix+'OpenUrl');
  const shortcut=document.getElementById(prefix+'OpenShortcut');
  if(mode)mode.value=(m&&m.openMode)||defaultMode||'default';
  if(url)url.value=(m&&m.openUrl)||'';
  if(shortcut)shortcut.value=(m&&m.openShortcut)||'';
  toggleOpenFields(prefix)
}
function monitorDetail(m){if(m.type==='github')return 'GitHub · '+(m.githubRepo||'');if(m.type==='network')return '${esc(L.networkDevice)} · '+(m.networkIp||'')+(m.networkVendor?' · '+m.networkVendor:'');return(m.type==='json'?'JSON':'HTTP')+' · '+m.url}function renderMonitors(){
  const root=document.getElementById('monitorList');
  root.innerHTML='';
  if(!state.monitors.length){
    root.innerHTML='<div class="empty">${esc(L.none)}</div>';
    return
  }

  for(const m of state.monitors){
    const row=document.createElement('div');row.className='monitorRow';
    row.onclick=()=>editMonitor(m.id);

    const left=document.createElement('div');left.className='navLeft';
    const icon=document.createElement('span');icon.className='navIcon';icon.textContent=m.icon||'🌐';
    const txt=document.createElement('div');txt.className='rowText';
    const t=document.createElement('div');t.className='rowTitle';t.textContent=m.name;
    const d=document.createElement('div');d.className='rowDetail';d.textContent=monitorDetail(m);
    txt.append(t,d);left.append(icon,txt);

    const right=document.createElement('div');right.className='navRight';
    if(m.showWidget){
      const p=document.createElement('span');p.className='pill';p.textContent='Widget';right.appendChild(p)
    }

    if(resolvedOpenUrl(m)){
      const open=document.createElement('button');
      open.className='miniBtn';
      open.textContent='${esc(L.openNow)}';
      open.onclick=e=>{e.stopPropagation();openMonitor(m.id)};
      right.appendChild(open)
    }

    const ch=document.createElement('span');ch.className='chevron';ch.textContent='›';
    right.appendChild(ch);
    row.append(left,right);
    root.appendChild(row)
  }
}
function newMonitor(template='custom'){
  editingId=null;
  const presets={
    web:{name:'',icon:'🌐',type:'http',url:'https://',hint:"\ud83c\udf10 Web / HTTP: Sta\u010d\u00ed zadat n\u00e1zev a URL. Ostatn\u00ed m\u016f\u017ee z\u016fstat v\u00fdchoz\u00ed."},
    homebridge:{name:'Homebridge',icon:'🏠',type:'http',url:'http://192.168.1.50:8581',hint:"\ud83c\udfe0 Homebridge: Nahra\u010f IP adresu adresou sv\u00e9ho Homebridge. B\u011b\u017en\u00fd port je 8581."},
    local:{name:'',icon:'🖥️',type:'http',url:'http://192.168.1.',hint:"\ud83d\udda5\ufe0f Lok\u00e1ln\u00ed slu\u017eba: Zadej IP a port, nap\u0159\u00edklad http://192.168.1.20:8080."},
    json:{name:'',icon:'{ }',type:'json',url:'https://',hint:"{ } JSON API: Zadej URL API. JSON cesta m\u016f\u017ee b\u00fdt t\u0159eba status nebo cpu.temperature."},
    custom:{name:'',icon:'⚙️',type:'http',url:'',hint:"\u2699\ufe0f Vlastn\u00ed monitor: Vypl\u0148 si typ a URL ru\u010dn\u011b."}
  };
  const p=presets[template]||presets.custom;
  document.getElementById('editorTitle').textContent="P\u0159idat monitor";
  document.getElementById('templateHint').textContent=p.hint;
  document.getElementById('mName').value=p.name;
  document.getElementById('mIcon').value=p.icon;
  document.getElementById('mType').value=p.type;
  document.getElementById('mUrl').value=p.url;
  document.getElementById('mMethod').value='GET';
  document.getElementById('mJsonPath').value=template==='json'?'status':'';
  document.getElementById('mExpected').value='';
  document.getElementById('mHeaders').value='{}';
  document.getElementById('mTimeout').value='0';
  document.getElementById('mEnabled').checked=true;
  document.getElementById('mShowWidget').checked=true;
  setOpenControls('m',null,'default');
  document.getElementById('deleteBtn').style.display='none';
  document.getElementById('advancedFields').open=false;
  toggleJsonFields();
  showScreen('editor')
}
function editMonitor(id){
  const m=state.monitors.find(x=>x.id===id);if(!m)return;
  if(m.type==='github'){editGithub(id);return}if(m.type==='network'){editNetwork(id);return}
  editingId=id;
  document.getElementById('editorTitle').textContent="Upravit monitor";
  document.getElementById('templateHint').textContent=m.type==='json'?'JSON API':'HTTP / web';
  document.getElementById('mName').value=m.name;
  document.getElementById('mIcon').value=m.icon;
  document.getElementById('mType').value=m.type;
  document.getElementById('mUrl').value=m.url;
  document.getElementById('mMethod').value=m.method;
  document.getElementById('mJsonPath').value=m.jsonPath||'';
  document.getElementById('mExpected').value=m.expected||'';
  document.getElementById('mHeaders').value=m.headers||'{}';
  document.getElementById('mTimeout').value=m.timeout||0;
  document.getElementById('mEnabled').checked=m.enabled!==false;
  document.getElementById('mShowWidget').checked=m.showWidget!==false;
  setOpenControls('m',m,'default');
  document.getElementById('deleteBtn').style.display='';
  document.getElementById('advancedFields').open=!!(m.method==='HEAD'||(m.headers&&m.headers!=='{}')||m.timeout);
  toggleJsonFields();
  showScreen('editor')
}
function editNetwork(id){
  const m=state.monitors.find(x=>x.id===id);if(!m)return;
  editingId=id;
  document.getElementById('nName').value=m.name||'';
  document.getElementById('nIcon').value=m.icon||'🖥️';
  document.getElementById('nIp').value=m.networkIp||'';
  document.getElementById('nMac').value=m.networkMac||'';
  document.getElementById('nVendor').value=m.networkVendor||'';
  document.getElementById('nEnabled').checked=m.enabled!==false;
  document.getElementById('nShowWidget').checked=m.showWidget!==false;
  setOpenControls('n',m,'none');
  showScreen('networkEditor')
}
function saveNetworkMonitor(){
  if(!editingId)return;
  const i=state.monitors.findIndex(x=>x.id===editingId);if(i<0)return;
  state.monitors[i]={...state.monitors[i],
    name:document.getElementById('nName').value.trim()||state.monitors[i].name,
    icon:document.getElementById('nIcon').value.trim()||'🖥️',
    enabled:document.getElementById('nEnabled').checked,
    showWidget:document.getElementById('nShowWidget').checked,
    openMode:document.getElementById('nOpenMode').value,
    openUrl:document.getElementById('nOpenUrl').value.trim(),
    openShortcut:document.getElementById('nOpenShortcut').value.trim()
  };
  saveState();showScreen('monitors')
}
function newGithub(){
  editingId=null;
  const title=document.getElementById('githubTitle');
  if(title)title.textContent=${JSON.stringify(L.githubAdd)};

  const name=document.getElementById('gName');
  const icon=document.getElementById('gIcon');
  const repo=document.getElementById('gRepo');
  const mode=document.getElementById('gMode');
  const enabled=document.getElementById('gEnabled');
  const show=document.getElementById('gShowWidget');
  const token=document.getElementById('gToken');
  const del=document.getElementById('gDeleteBtn');

  if(name)name.value='';
  if(icon)icon.value='🐙';
  if(repo)repo.value='';
  if(mode)mode.value='repo';
  if(enabled)enabled.checked=true;
  if(show)show.checked=true;
  setOpenControls('g',null,'default');
  if(token)token.value='';
  if(del)del.style.display='none';

  showScreen('githubEditor')
}
function editGithub(id){const m=state.monitors.find(x=>x.id===id);if(!m)return;editingId=id;document.getElementById('githubTitle').textContent=${JSON.stringify(L.editMonitor)};document.getElementById('gName').value=m.name;document.getElementById('gIcon').value=m.icon||'🐙';document.getElementById('gRepo').value=m.githubRepo||'';document.getElementById('gMode').value=m.githubMode||'repo';document.getElementById('gEnabled').checked=m.enabled!==false;document.getElementById('gShowWidget').checked=m.showWidget!==false;setOpenControls('g',m,'default');document.getElementById('gDeleteBtn').style.display='';document.getElementById('gToken').value='';showScreen('githubEditor')}function toggleJsonFields(){const j=document.getElementById('jsonFields');if(j)j.style.display=document.getElementById('mType').value==='json'?'block':'none'}function saveMonitor(){const m={id:editingId||('m'+Date.now()+Math.random().toString(36).slice(2,6)),name:document.getElementById('mName').value.trim(),icon:document.getElementById('mIcon').value.trim()||'🌐',type:document.getElementById('mType').value,url:document.getElementById('mUrl').value.trim(),method:document.getElementById('mMethod').value,headers:document.getElementById('mHeaders').value||'{}',jsonPath:document.getElementById('mJsonPath').value.trim(),expected:document.getElementById('mExpected').value.trim(),timeout:Number(document.getElementById('mTimeout').value)||0,openMode:document.getElementById('mOpenMode').value,openUrl:document.getElementById('mOpenUrl').value.trim(),openShortcut:document.getElementById('mOpenShortcut').value.trim(),enabled:document.getElementById('mEnabled').checked,showWidget:document.getElementById('mShowWidget').checked};if(!m.name||!m.url)return;const i=state.monitors.findIndex(x=>x.id===m.id);if(i>=0)state.monitors[i]=m;else state.monitors.push(m);saveState();showScreen('monitors')}function saveGithubMonitor(){let repo=document.getElementById('gRepo').value.trim();if(repo.startsWith('https://github.com/'))repo=repo.slice('https://github.com/'.length);else if(repo.startsWith('http://github.com/'))repo=repo.slice('http://github.com/'.length);while(repo.endsWith('/'))repo=repo.slice(0,-1);if(!repo.includes('/'))return;const m={id:editingId||('g'+Date.now()+Math.random().toString(36).slice(2,6)),name:document.getElementById('gName').value.trim()||repo,icon:document.getElementById('gIcon').value.trim()||'🐙',type:'github',url:'https://api.github.com/repos/'+repo,githubRepo:repo,githubMode:document.getElementById('gMode').value,openMode:document.getElementById('gOpenMode').value,openUrl:document.getElementById('gOpenUrl').value.trim(),openShortcut:document.getElementById('gOpenShortcut').value.trim(),enabled:document.getElementById('gEnabled').checked,showWidget:document.getElementById('gShowWidget').checked,timeout:0};const i=state.monitors.findIndex(x=>x.id===m.id);if(i>=0)state.monitors[i]=m;else state.monitors.push(m);saveState();showScreen('monitors')}function deleteMonitor(){if(!editingId)return;state.monitors=state.monitors.filter(x=>x.id!==editingId);editingId=null;saveState();showScreen('monitors')}function openNetworkSource(){
  const ns=state.networkSource||{};
  document.getElementById('nsEnabled').checked=ns.enabled===true;
  document.getElementById('nsUrl').value=ns.url||'';
  document.getElementById('nsListPath').value=ns.listPath||'';
  document.getElementById('nsIpPath').value=ns.ipPath||'';
  document.getElementById('nsNamePath').value=ns.namePath||'';
  document.getElementById('nsMacPath').value=ns.macPath||'';
  document.getElementById('nsVendorPath').value=ns.vendorPath||'';
  document.getElementById('nsAuth').value='';
  document.getElementById('nsStatus').textContent='';
  showScreen('networkSource')
}
function collectNetworkSource(){
  return{
    enabled:document.getElementById('nsEnabled').checked,
    url:document.getElementById('nsUrl').value.trim(),
    listPath:document.getElementById('nsListPath').value.trim(),
    ipPath:document.getElementById('nsIpPath').value.trim(),
    namePath:document.getElementById('nsNamePath').value.trim(),
    macPath:document.getElementById('nsMacPath').value.trim(),
    vendorPath:document.getElementById('nsVendorPath').value.trim()
  }
}
function saveNetworkSource(){
  state.networkSource=collectNetworkSource();
  saveState();
  const e=document.getElementById('deviceSourceSummary');
  if(e)e.textContent=state.networkSource.enabled&&state.networkSource.url?'${esc(L.deviceSourceConfigured)}':'${esc(L.deviceSourceNone)}';
  document.getElementById('nsStatus').textContent='${esc(L.deviceSourceSaved)}'
}
function testNetworkSource(){
  state.networkSource=collectNetworkSource();saveState();
  document.getElementById('nsStatus').textContent='…';
  post({action:'testNetworkSource',source:state.networkSource})
}
function saveNetworkAuth(){post({action:'saveNetworkAuth',value:document.getElementById('nsAuth').value})}
function removeNetworkAuth(){post({action:'removeNetworkAuth'})}
function openNetworkScan(){document.getElementById('scanResults').innerHTML='<div class="empty">${esc(L.scanNone)}</div>';document.getElementById('scanStatus').textContent='';showScreen('network')}const SCAN_PORTS={
  quick:[80,443,8080,8581,5533,5252,3000,8123,8006],
  normal:[80,81,443,1880,3000,5000,5001,5252,5533,8000,8006,8080,8081,8096,8123,8384,8443,8581,8888,9000,9090,9443,32400],
  deep:[80,81,443,1880,3000,3001,5000,5001,5252,5533,6052,7878,8000,8001,8006,8080,8081,8082,8096,8123,8181,8200,8300,8384,8443,8581,8686,8888,8920,8989,9000,9001,9090,9091,9443,9696,10000,10443,12000,32400,49152]
};
function applyScanMode(){
  const mode=document.getElementById('scanMode').value||'quick';
  document.getElementById('scanPorts').value=(SCAN_PORTS[mode]||SCAN_PORTS.quick).join(',')
}
function wholeNetwork(){
  document.getElementById('scanStart').value='1';
  document.getElementById('scanEnd').value='254'
}
function startAutoNetworkScan(){
  const b=document.getElementById('autoScanBtn');
  if(b)b.disabled=true;
  const manual=document.getElementById('scanBtn');
  if(manual)manual.disabled=true;
  scanItems=[];scanInventory=[];
  const root=document.getElementById('scanResults');
  if(root)root.innerHTML='<div class="empty">…</div>';
  document.getElementById('scanStatus').textContent='${esc(L.autoDetecting)}…';
  post({action:'autoScanNetwork'})
}
function startNetworkScan(){
  const b=document.getElementById('scanBtn');
  b.disabled=true;
  scanItems=[];scanInventory=[];
  const mode=document.getElementById('scanMode').value||'quick';
  document.getElementById('scanStatus').textContent='${esc(L.scan)}…';
  post({
    action:'scanNetwork',
    base:document.getElementById('scanBase').value,
    start:Number(document.getElementById('scanStart').value),
    end:Number(document.getElementById('scanEnd').value),
    ports:document.getElementById('scanPorts').value,
    mode
  })
}
let scanItems=[],scanInventory=[];
function confidenceScore(x){
  const map={signature:100,fingerprint:95,page:80,port:60,server:40,generic:10};
  let score=map[x&&x.confidence]||0;
  const n=String((x&&x.name)||"").toLowerCase();
  if(n.endsWith("?"))score-=10;
  if(n.includes("web service")||n.includes("not found")||n.includes("httpd")||n.includes("nginx")||n.includes("apache"))score-=25;
  if([8581,8123,8006,5001,9443,32400].includes(Number(x&&x.port)))score+=5;
  return score
}
function cleanDeviceName(v){
  let s=String(v||"").trim();
  if(!s)return "";
  if(s.endsWith("?"))s=s.slice(0,-1).trim();
  const l=s.toLowerCase();
  const exact=[
    "web service","unknown web service","not found","page not found",
    "http service","https service","httpd","nginx","apache"
  ];
  if(exact.includes(l))return "";
  if(l.startsWith("httpd/")||l.startsWith("nginx/")||l.startsWith("apache/"))return "";
  return s
}
function groupScanItems(items){
  const map=new Map();

  for(const d of scanInventory||[]){
    map.set(d.ip,{ip:d.ip,services:[],inventory:d})
  }
  for(const x of items||[]){
    if(!map.has(x.ip))map.set(x.ip,{ip:x.ip,services:[],inventory:null});
    map.get(x.ip).services.push(x)
  }

  return [...map.values()].map(g=>{
    g.services.sort((a,b)=>confidenceScore(b)-confidenceScore(a)||Number(a.port)-Number(b.port));
    const best=g.services[0]||null;
    let named=g.services.find(s=>cleanDeviceName(s.name));
    let name=g.inventory&&String(g.inventory.name||"").trim();
    if(!name)name=named?cleanDeviceName(named.name):"";
    if(!name)name='${esc(L.device)} '+g.ip;

    let icon=(named||best)&&((named||best).icon)||'🖥️';
    const vendor=String(g.inventory?.vendor||"").toLowerCase();
    if(vendor.includes("apple"))icon="🍎";
    else if(vendor.includes("raspberry"))icon="🥧";
    else if(vendor.includes("synology")||vendor.includes("qnap"))icon="💾";
    else if(vendor.includes("tuya"))icon="💡";

    return{ip:g.ip,name,icon,services:g.services,best,inventory:g.inventory}
  }).sort((a,b)=>a.ip.localeCompare(b.ip,undefined,{numeric:true}))
}
function canonicalServiceName(x){
  let n=cleanDeviceName(x&&x.name)||"";
  n=String(n).trim();
  if(n.endsWith("?"))n=n.slice(0,-1).trim();

  const suffix=" / web app";
  if(n.toLowerCase().endsWith(suffix))n=n.slice(0,-suffix.length).trim();

  if(!n){
    const p=Number(x&&x.port);
    if(p===8581)n="Homebridge";
    else if(p===5533)n="ATVLoadly";
    else if(p===5252)n="Tailscale";
    else n="Web service";
  }

  const low=n.toLowerCase();
  if(low.includes("homebridge"))return "Homebridge";
  if(low.includes("atvloadly")||low.includes("atv loadly"))return "ATVLoadly";
  if(low.includes("tailscale"))return "Tailscale";
  if(low.includes("home assistant"))return "Home Assistant";
  if(low.includes("proxmox"))return "Proxmox";
  if(low.includes("portainer"))return "Portainer";
  if(low.includes("jellyfin"))return "Jellyfin";
  if(low.includes("plex"))return "Plex";
  if(low.includes("grafana"))return "Grafana";
  return n
}
function canonicalServiceIcon(name,services){
  const low=String(name||"").toLowerCase();
  if(low==="homebridge")return "🏠";
  if(low==="atvloadly")return "📺";
  if(low==="tailscale")return "🔗";
  if(low==="home assistant")return "🏠";
  if(low==="proxmox")return "🖥️";
  if(low==="portainer")return "🐳";
  if(low==="jellyfin")return "🎬";
  if(low==="plex")return "🎬";
  if(low==="grafana")return "📊";
  const withIcon=(services||[]).find(x=>x&&x.icon);
  return withIcon?withIcon.icon:"🌐"
}
function preferredPortScore(name,port){
  const n=String(name||"").toLowerCase(),p=Number(port);
  if(n==="homebridge"&&p===8581)return 100;
  if(n==="atvloadly"&&p===5533)return 100;
  if(n==="tailscale"&&p===5252)return 100;
  if(n==="home assistant"&&p===8123)return 100;
  if(n==="proxmox"&&p===8006)return 100;
  if(n==="portainer"&&(p===9443||p===9000))return 100;
  return 0
}
function serviceOrder(name){
  const n=String(name||"").toLowerCase();
  const order={"homebridge":1,"atvloadly":2,"tailscale":3,"home assistant":4,"proxmox":5,"portainer":6};
  return order[n]||50
}
function pickServiceEndpoint(group){
  const exact=(group.endpoints||[]).find(x=>preferredPortScore(group.name,x.port)>=100);
  if(exact)return exact;
  const signed=(group.endpoints||[]).find(x=>x.confidence==="signature"||x.confidence==="fingerprint");
  return signed||(group.endpoints||[])[0]||null
}
function serviceGroupsForDevice(g){
  const map=new Map();
  for(const s of g.services||[]){
    const name=canonicalServiceName(s);
    const key=name.toLowerCase();
    if(!map.has(key))map.set(key,{name,icon:canonicalServiceIcon(name,[s]),endpoints:[]});
    map.get(key).endpoints.push(s)
  }
  const groups=[...map.values()];
  for(const sg of groups){
    sg.endpoints.sort((a,b)=>confidenceScore(b)-confidenceScore(a)||preferredPortScore(sg.name,b.port)-preferredPortScore(sg.name,a.port)||Number(a.port)-Number(b.port));
    sg.primary=pickServiceEndpoint(sg)
  }
  return groups.sort((a,b)=>serviceOrder(a.name)-serviceOrder(b.name)||a.name.localeCompare(b.name))
}
function serviceAlreadyAdded(group){
  return (group.endpoints||[]).some(x=>monitorAlreadyAdded(x))
}
function monitorAlreadyAdded(x){
  return (state.monitors||[]).some(m=>m.url===x.url)
}
function deviceAlreadyAdded(group){
  if(!group.inventory)return false;
  const mac=String(group.inventory.mac||"").toUpperCase();
  return (state.monitors||[]).some(m=>m.type==='network'&&((mac&&String(m.networkMac||"").toUpperCase()===mac)||m.networkIp===group.ip))
}
function preferredService(group){
  const exactKnown=group.services.find(s=>s.confidence==='signature'||s.confidence==='fingerprint');
  if(exactKnown)return exactKnown;
  const knownPort=group.services.find(s=>[8581,8123,8006,5001,9443,32400].includes(Number(s.port)));
  return knownPort||group.best||group.services[0]
}
function renderScanResults(items){
  if(Array.isArray(items)&&items.length)scanItems=items;
  const groups=groupScanItems(scanItems);
  const root=document.getElementById('scanResults');
  root.innerHTML='';
  const manualBtn=document.getElementById('scanBtn');if(manualBtn)manualBtn.disabled=false;
  const autoBtn=document.getElementById('autoScanBtn');if(autoBtn)autoBtn.disabled=false;
  document.getElementById('scanStatus').textContent=groups.length?groups.length+' ${esc(L.scanFound)}':'${esc(L.nothingFound)}';

  if(!groups.length){
    root.innerHTML='<div class="empty">${esc(L.nothingFound)}</div>';
    return
  }

  for(const g of groups){
    const wrap=document.createElement('div');wrap.className='deviceGroup';

    const head=document.createElement('div');head.className='deviceHead';
    const left=document.createElement('div');left.className='rowText';
    const name=document.createElement('div');name.className='deviceName';
    name.textContent=(g.icon?g.icon+' ':'')+g.name;

    const meta=document.createElement('div');meta.className='deviceMeta';
    const parts=[g.ip];
    if(g.inventory&&g.inventory.vendor)parts.push(g.inventory.vendor);
    if(g.inventory&&g.inventory.mac)parts.push(g.inventory.mac);
    meta.textContent=parts.join(' · ');
    left.append(name,meta);
    head.appendChild(left);

    if(g.inventory){
      const addDevice=document.createElement('button');addDevice.className='deviceBtn';
      const already=deviceAlreadyAdded(g);
      addDevice.textContent=already?'✓ ${esc(L.watching)}':'${esc(L.watchDevice)}';
      addDevice.disabled=already;
      addDevice.onclick=()=>addNetworkDevice(g);
      head.appendChild(addDevice)
    }
    wrap.appendChild(head);

    const serviceGroups=serviceGroupsForDevice(g);
    if(serviceGroups.length){
      const cap=document.createElement('div');cap.className='serviceDetail';
      cap.style.padding='8px 14px 4px 22px';
      cap.textContent='${esc(L.servicesOnDevice)}';
      wrap.appendChild(cap)
    }

    for(const sg of serviceGroups){
      const row=document.createElement('div');row.className='serviceRow';
      const info=document.createElement('div');info.className='serviceInfo';

      const title=document.createElement('div');title.className='serviceTitle';
      title.textContent=(sg.icon?sg.icon+' ':'')+sg.name;

      const detail=document.createElement('div');detail.className='serviceDetail';
      const ports=[...new Set(sg.endpoints.map(x=>Number(x.port)))].sort((a,b)=>a-b);
      const best=sg.primary;
      const bits=[];
      if(ports.length)bits.push('${esc(L.servicePorts)}: '+ports.join(', '));
      if(best)bits.push((best.url.startsWith('https://')?'HTTPS':'HTTP')+' '+best.status+' · '+best.latency+' ms');
      detail.textContent=bits.join(' · ');
      info.append(title,detail);

      const btn=document.createElement('button');btn.className='deviceBtn';
      const added=serviceAlreadyAdded(sg);
      btn.textContent=added?'✓ ${esc(L.watching)}':'${esc(L.watch)}';
      btn.disabled=added;
      btn.onclick=()=>addServiceGroup(sg);

      row.append(info,btn);
      wrap.appendChild(row)
    }

    if(!serviceGroups.length&&!g.inventory){
      const empty=document.createElement('div');empty.className='serviceRow';
      const d=document.createElement('div');d.className='serviceDetail';
      d.textContent='${esc(L.nothingFound)}';
      empty.appendChild(d);
      wrap.appendChild(empty)
    }
    root.appendChild(wrap)
  }
}
function addNetworkDevice(g){
  if(!g.inventory||deviceAlreadyAdded(g)){renderScanResults(scanItems);return}
  const d=g.inventory;
  state.monitors.push({
    id:'d'+Date.now()+Math.random().toString(36).slice(2,6),
    name:g.name||d.name||g.ip,
    icon:g.icon||'🖥️',
    type:'network',
    url:'',
    networkIp:g.ip,
    networkMac:d.mac||'',
    networkVendor:d.vendor||'',
    enabled:true,
    showWidget:true,
    timeout:0
  });
  saveState();renderScanResults(scanItems)
}
function addServiceGroup(sg){
  if(!sg||serviceAlreadyAdded(sg)){renderScanResults(scanItems);return}
  const x=sg.primary||sg.endpoints[0];
  if(!x)return;
  addScanned(x,sg.name,sg.icon)
}
function addScanned(x,deviceName=null,deviceIcon=null){
  if(!x||monitorAlreadyAdded(x)){
    renderScanResults(scanItems);
    return
  }
  const m={
    id:'n'+Date.now()+Math.random().toString(36).slice(2,6),
    name:deviceName||cleanDeviceName(x.name)||x.ip+':'+x.port,
    icon:deviceIcon||x.icon||'🖥️',
    type:'http',
    url:x.url,
    method:'GET',
    headers:'{}',
    jsonPath:'',
    expected:'',
    timeout:0,
    enabled:true,
    showWidget:true
  };
  state.monitors.push(m);
  saveState();
  renderScanResults(scanItems);
}
function saveGithubToken(){const token=document.getElementById('gToken').value.trim();if(token)post({action:'saveGithubToken',token})}function removeGithubToken(){post({action:'removeGithubToken'})}function preview(family,demo){document.getElementById('previewStatus').textContent='…';post({action:'preview',family,demo,settings:state})}function enableCustomColors(){const toggle=document.getElementById('useCustomColors');if(toggle){toggle.checked=true;state.useCustomColors=true}}
function syncColorFromPicker(id){const picker=document.getElementById(id+'Picker'),text=document.getElementById(id);if(!picker||!text)return;text.value=picker.value.toUpperCase();enableCustomColors();saveAppearance()}
function syncColorFromText(id){const text=document.getElementById(id),picker=document.getElementById(id+'Picker');if(!text||!picker)return;let v=String(text.value||'').trim().toUpperCase();if(v&&!v.startsWith('#'))v='#'+v;text.value=v;if(/^#[0-9A-F]{6}$/.test(v)){picker.value=v;enableCustomColors();saveAppearance()}}
function saveAppearance(){state.widgetTitle=document.getElementById('widgetTitle').value||'Home Dashboard';for(const id of['showLatency','showValue','showTime','useCustomColors'])state[id]=document.getElementById(id).checked;const defaults={backgroundColor:'#0B1020',textColor:'#F8FAFC',mutedColor:'#94A3B8',okColor:'#34C759',failColor:'#FF453A'};for(const id of Object.keys(defaults)){let v=String(document.getElementById(id).value||'').trim().toUpperCase();if(v&&!v.startsWith('#'))v='#'+v;if(/^#[0-9A-F]{6}$/.test(v))state[id]=v;else if(!state[id])state[id]=defaults[id]}saveState()}
function resetAppearance(){state.widgetTitle='Home Dashboard';state.showLatency=true;state.showValue=true;state.showTime=true;state.useCustomColors=false;state.backgroundColor='#0B1020';state.textColor='#F8FAFC';state.mutedColor='#94A3B8';state.okColor='#34C759';state.failColor='#FF453A';saveState();post({action:'reload',settings:state})}function saveBehavior(){state.refreshMinutes=Number(document.getElementById('refreshMinutes').value)||30;state.defaultTimeout=Number(document.getElementById('defaultTimeout').value)||6;saveState()}function setLanguage(l){state.language=l;saveState();post({action:'reload',settings:state})}function importSettings(){post({action:'import',raw:document.getElementById('jsonBox').value})}window.__native=function(m){if(!m)return;if(m.action==='previewDone')document.getElementById('previewStatus').textContent='';if(m.action==='status'){const e=document.getElementById('toolStatus');if(e)e.textContent=m.text||''}if(m.action==='update'){const e=document.getElementById('updateStatus');if(e){e.textContent=m.text||'';e.className='updateStatus '+(m.ok?'ok':'error')}}if(m.action==='scanProgress'){const e=document.getElementById('scanStatus');if(e){if(m.phase==='detect')e.textContent='${esc(L.autoDetecting)}… '+m.done+' / '+m.total;else if(m.phase==='hosts')e.textContent='${esc(L.scanHosts)} '+m.done+' / '+m.total+' · '+m.found+' ${esc(L.scanActive)}';else e.textContent='${esc(L.scanServices)} '+m.done+' / '+m.total+' · '+m.found+' ${esc(L.scanFound).toLowerCase()}'}}if(m.action==='scanDetected'){const e=document.getElementById('scanStatus');if(e)e.textContent='${esc(L.autoDetected)} '+m.base+'.x · ${esc(L.autoSearching)}…';const base=document.getElementById('scanBase');if(base)base.value=m.base||base.value}if(m.action==='autoScanFailed'){const e=document.getElementById('scanStatus');if(e)e.textContent='${esc(L.autoFailed)}';const a=document.getElementById('autoScanBtn');if(a)a.disabled=false;const b=document.getElementById('scanBtn');if(b)b.disabled=false}if(m.action==='scanResults'){scanItems=m.items||[];scanInventory=m.inventory||[];renderScanResults(scanItems);}if(m.action==='tokenStatus'){const e=document.getElementById('tokenHint');if(e)e.textContent=m.text||'';document.getElementById('gToken').value=''}if(m.action==='networkSourceTest'){const e=document.getElementById('nsStatus');if(e)e.textContent=m.ok?(m.count+' ${esc(L.deviceSourceFound)}'):(m.text||'${esc(L.deviceSourceEmpty)}')}if(m.action==='networkAuthStatus'){const e=document.getElementById('nsAuthStatus');if(e)e.textContent=m.text||'';const a=document.getElementById('nsAuth');if(a)a.value=''}};renderMonitors();
</script></body></html>`}
async function send(web,o){try{await web.evaluateJavaScript(`window.__native(${JSON.stringify(o)})`,false)}catch(_){}}
async function settings(s){const web=new WebView();await web.loadHTML(settingsHTML(s));let dismissed=false,cur=merge(s);const presentPromise=web.present(false).then(()=>{dismissed=true});const sleep=ms=>new Promise(resolve=>Timer.schedule(ms,false,resolve));while(!dismissed){await sleep(160);if(dismissed)break;let raw=null;try{raw=await web.evaluateJavaScript("JSON.stringify(window.__nativeQueue.shift()||null)")}catch(_){if(dismissed)break;continue}if(!raw||raw==="null")continue;let m=null;try{m=JSON.parse(raw)}catch(_){continue}if(!m?.action)continue;try{if(m.action==="save"){cur=merge(m.settings);saveSettings(cur)}else if(m.action==="openUrl"){
  let u=String(m.url||"").trim();
  if(u){
    if(!u.includes(":"))u="https://"+u;
    Safari.open(u)
  }
}else if(m.action==="update"){cur=merge(cur);saveSettings(cur);const r=await updater(cur);await send(web,{action:"update",ok:r.ok,text:r.text})}else if(m.action==="preview"){cur=merge(m.settings||cur);saveSettings(cur);const family=["small","medium","large"].includes(m.family)?m.family:"medium";const results=m.demo?demoResults():await checkAll(cur);const w=await buildWidget(results,cur,family,m.demo===true);try{await presentWidget(w,family)}finally{await send(web,{action:"previewDone"})}}else if(m.action==="testAll"){cur=merge(m.settings||cur);saveSettings(cur);const r=await checkAll(cur);const bad=r.filter(x=>!x.ok).length;await send(web,{action:"status",text:bad?tx(cur,"problems")(bad):tx(cur,"allGood")})}else if(m.action==="autoScanNetwork"){try{
  const base=await detectLocalSubnet(async(done,total,found)=>{await send(web,{action:"scanProgress",phase:"detect",done,total,found})});
  if(!base){
    await send(web,{action:"autoScanFailed"});
  }else{
    await send(web,{action:"scanDetected",base});
    const inventoryPromise=fetchNetworkInventory(cur.networkSource).catch(e=>{console.log("Network source: "+e);return[]});
    const items=await scanLocalNetwork(base,1,254,AUTO_SCAN_PORTS,"normal",async(phase,done,total,found,active)=>{
      await send(web,{action:"scanProgress",phase,done,total,found,active:active||0})
    });
    let inventory=await inventoryPromise;
    inventory=inventory.filter(d=>String(d.ip||"").startsWith(base+"."));
    await send(web,{action:"scanResults",items,inventory,base})
  }
}catch(e){
  console.log("Auto network scan: "+e);
  await send(web,{action:"autoScanFailed"})
}}else if(m.action==="scanNetwork"){try{
  const inventoryPromise=fetchNetworkInventory(cur.networkSource).catch(e=>{console.log("Network source: "+e);return[]});
  const items=await scanLocalNetwork(m.base,m.start,m.end,m.ports,m.mode||"quick",async(phase,done,total,found,active)=>{await send(web,{action:"scanProgress",phase,done,total,found,active:active||0})});
  let inventory=await inventoryPromise;
  const prefix=String(m.base||"").trim().replace(/\.$/,"")+".";
  if(prefix!==".")inventory=inventory.filter(d=>String(d.ip||"").startsWith(prefix));
  await send(web,{action:"scanResults",items,inventory})
}catch(e){
  await send(web,{action:"scanResults",items:[],inventory:[]});
  await send(web,{action:"status",text:String(e?.message||e)})
}}else if(m.action==="testNetworkSource"){
  try{
    const source=normalizeNetworkSource(m.source||cur.networkSource);
    const items=await fetchNetworkInventory(source);
    await send(web,{action:"networkSourceTest",ok:items.length>0,count:items.length,text:items.length?"":tx(cur,"deviceSourceEmpty")})
  }catch(e){await send(web,{action:"networkSourceTest",ok:false,count:0,text:String(e?.message||e)})}
}else if(m.action==="saveNetworkAuth"){
  try{
    Keychain.set(NETWORK_SOURCE_AUTH_KEY,String(m.value||""));
    await send(web,{action:"networkAuthStatus",text:tx(cur,"tokenStored")})
  }catch(e){await send(web,{action:"networkAuthStatus",text:String(e?.message||e)})}
}else if(m.action==="removeNetworkAuth"){
  try{
    if(Keychain.contains(NETWORK_SOURCE_AUTH_KEY))Keychain.remove(NETWORK_SOURCE_AUTH_KEY);
    await send(web,{action:"networkAuthStatus",text:tx(cur,"tokenRemoved")})
  }catch(e){await send(web,{action:"networkAuthStatus",text:String(e?.message||e)})}
}else if(m.action==="saveGithubToken"){try{Keychain.set(GITHUB_TOKEN_KEY,String(m.token||""));await send(web,{action:"tokenStatus",text:tx(cur,"tokenStored")})}catch(e){await send(web,{action:"tokenStatus",text:String(e?.message||e)})}}else if(m.action==="removeGithubToken"){try{if(Keychain.contains(GITHUB_TOKEN_KEY))Keychain.remove(GITHUB_TOKEN_KEY);await send(web,{action:"tokenStatus",text:tx(cur,"tokenRemoved")})}catch(e){await send(web,{action:"tokenStatus",text:String(e?.message||e)})}}else if(m.action==="resetCache"){resetState();await send(web,{action:"status",text:tx(cur,"cacheReset")})}else if(m.action==="export"){Pasteboard.copyString(JSON.stringify(cur,null,2));await send(web,{action:"status",text:tx(cur,"copied")})}else if(m.action==="import"){try{const imported=merge(JSON.parse(m.raw||""));if(!imported.language)imported.language=cur.language||lang();cur=imported;saveSettings(cur);await web.loadHTML(settingsHTML(cur))}catch(_){await send(web,{action:"status",text:tx(cur,"invalid")})}}else if(m.action==="reload"){cur=merge(m.settings||cur);saveSettings(cur);await web.loadHTML(settingsHTML(cur))}}catch(e){console.log(e);await send(web,{action:"status",text:String(e?.message||e)})}}try{await presentPromise}catch(_){}return cur}
let SETTINGS=await firstLanguage(loadSettings());if(config.runsInWidget){const family=config.widgetFamily||"medium";try{const results=await checkAll(SETTINGS,6000);const w=await buildWidget(results,SETTINGS,family);Script.setWidget(w)}catch(e){const w=await buildWidget(cachedResults(SETTINGS),SETTINGS,family);Script.setWidget(w)}}else SETTINGS=await settings(SETTINGS);Script.complete();
