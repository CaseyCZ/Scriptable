from pathlib import Path

js_path = Path('apps/LockScreenGenerator/LockScreenGenerator.js')
readme_path = Path('apps/LockScreenGenerator/README.md')
src = js_path.read_text(encoding='utf-8')


def rep(old, new, label):
    global src
    n = src.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    src = src.replace(old, new, 1)

rep('const APP_VERSION = "2.9.9";', 'const APP_VERSION = "2.10.0";', 'version')
rep('const STEPS_FILE = "LockScreenGenerator_steps.txt";', 'const STEPS_FILE = "LockScreenGenerator_steps.txt";\nconst BACKGROUND_FILE = "LockScreenGenerator_background.png";', 'background constant')
rep('const DEFAULT_SETTINGS={settingsVersion:8,', 'const DEFAULT_SETTINGS={settingsVersion:9,wallpaperSource:"shortcut",', 'settings defaults')

old_main = '''async function main(){const shortcutOverlay=String(args.shortcutParameter??"").trim().toLowerCase()==="overlay";let settings=await loadSettings();if(config.runsInApp&&!shortcutOverlay){const fm=FileManager.iCloud(),settingsPath=fm.joinPath(fm.documentsDirectory(),SETTINGS_FILE),firstRun=!fm.fileExists(settingsPath);if(firstRun){settings.language=await chooseFirstRunLanguage(settings.language);saveSettings(settings)}settings=await openSettingsScreen(settings)}const size=resolveResolution();const image=await buildImage(size,settings),png=Data.fromPNG(image);const fm=FileManager.iCloud(),path=fm.joinPath(fm.documentsDirectory(),OUTPUT_FILE);fm.write(path,png);const shortcutRun=shortcutOverlay||(!config.runsInApp&&!config.runsInWidget&&!config.runsInNotification&&!config.runsFromHomeScreen);if(shortcutRun){const overlayBase64=png.toBase64String();Script.setShortcutOutput(overlayBase64);Script.complete();return}if(config.runsInApp)await QuickLook.present(image);Script.setShortcutOutput(path);Script.complete()}'''
new_main = '''async function main(){const shortcutOverlay=String(args.shortcutParameter??"").trim().toLowerCase()==="overlay";let settings=await loadSettings();if(config.runsInApp&&!shortcutOverlay){const fm=FileManager.iCloud(),settingsPath=fm.joinPath(fm.documentsDirectory(),SETTINGS_FILE),firstRun=!fm.fileExists(settingsPath);if(firstRun){settings.language=await chooseFirstRunLanguage(settings.language);saveSettings(settings)}settings=await openSettingsScreen(settings)}const size=resolveResolution(),overlay=await buildImage(size,settings);const shortcutImage=Array.isArray(args.images)&&args.images.length?args.images[0]:null,background=settings.wallpaperSource==="generator"?await loadStoredBackground():shortcutImage,finalImage=background?composeWallpaper(size,background,overlay):overlay,png=Data.fromPNG(finalImage);const fm=FileManager.iCloud(),path=fm.joinPath(fm.documentsDirectory(),OUTPUT_FILE);fm.write(path,png);const shortcutRun=shortcutOverlay||(!config.runsInApp&&!config.runsInWidget&&!config.runsInNotification&&!config.runsFromHomeScreen);if(shortcutRun){if(background){Script.setShortcutOutput(path)}else{const overlayBase64=png.toBase64String();Script.setShortcutOutput(overlayBase64)}Script.complete();return}if(config.runsInApp)await QuickLook.present(finalImage);Script.setShortcutOutput(path);Script.complete()}\nasync function loadStoredBackground(){const fm=FileManager.iCloud(),path=fm.joinPath(fm.documentsDirectory(),BACKGROUND_FILE);if(!fm.fileExists(path))return null;try{if(!fm.isFileDownloaded(path))await fm.downloadFileFromiCloud(path);return fm.readImage(path)}catch(e){console.error("Background load failed: "+e);return null}}\nfunction composeWallpaper(size,background,overlay){const ctx=new DrawContext();ctx.size=new Size(size.width,size.height);ctx.opaque=true;ctx.respectScreenScale=true;const iw=Math.max(1,background.size.width),ih=Math.max(1,background.size.height),scale=Math.max(size.width/iw,size.height/ih),w=iw*scale,h=ih*scale,x=(size.width-w)/2,y=(size.height-h)/2;ctx.drawImageInRect(background,new Rect(x,y,w,h));ctx.drawImageInRect(overlay,new Rect(0,0,size.width,size.height));return ctx.getImage()}'''
rep(old_main, new_main, 'main')

# Add localized wallpaper UI as a separate object so the existing translation table stays stable.
anchor = 'const API_UI={'
wallpaper_ui = '''const WALLPAPER_UI={\n  cs:{title:"Tapeta",sub:"Vyber zdroj základní fotky. Generátor umí použít jednu uloženou fotku, nebo přijmout obrázek ze Zkratek — třeba náhodně vybraný z alba.",source:"Zdroj tapety",generator:"Fotka uložená v generátoru",shortcut:"Fotka ze Zkratek",pick:"Vybrat fotku",replace:"Změnit fotku",clear:"Odstranit uloženou fotku",ready:"Uložená fotka je připravená.",missing:"Zatím není vybraná žádná fotka.",shortcutHint:"Ve Zkratkách vyber fotku (klidně náhodně z alba) a vlož ji do pole Images u akce Run Script. LockScreen Generator ji sám spojí s překrytím."},\n  en:{title:"Wallpaper",sub:"Choose the base photo source. The generator can use one saved photo or accept an image from Shortcuts, including a random photo from an album.",source:"Wallpaper source",generator:"Photo saved in generator",shortcut:"Photo from Shortcuts",pick:"Choose photo",replace:"Change photo",clear:"Remove saved photo",ready:"Saved photo is ready.",missing:"No saved photo selected yet.",shortcutHint:"In Shortcuts choose a photo (random from an album is fine) and pass it in the Images field of Run Script. LockScreen Generator composites it automatically."},\n  de:{title:"Hintergrund",sub:"Wähle die Quelle des Hintergrundfotos: ein im Generator gespeichertes Foto oder ein Bild aus Kurzbefehle, auch zufällig aus einem Album.",source:"Hintergrundquelle",generator:"Im Generator gespeichertes Foto",shortcut:"Foto aus Kurzbefehle",pick:"Foto auswählen",replace:"Foto ändern",clear:"Gespeichertes Foto entfernen",ready:"Gespeichertes Foto ist bereit.",missing:"Noch kein Foto ausgewählt.",shortcutHint:"Wähle in Kurzbefehle ein Foto und übergib es im Feld Images der Aktion Run Script. LockScreen Generator setzt alles automatisch zusammen."},\n  es:{title:"Fondo",sub:"Elige la fuente de la foto base: una foto guardada en el generador o una imagen de Atajos, incluso aleatoria desde un álbum.",source:"Fuente del fondo",generator:"Foto guardada en el generador",shortcut:"Foto de Atajos",pick:"Elegir foto",replace:"Cambiar foto",clear:"Eliminar foto guardada",ready:"La foto guardada está lista.",missing:"Aún no hay ninguna foto guardada.",shortcutHint:"En Atajos elige una foto y pásala en el campo Images de Run Script. LockScreen Generator la combina automáticamente."}\n};\n\n'''
if anchor not in src:
    raise SystemExit('API_UI anchor missing')
src = src.replace(anchor, wallpaper_ui + anchor, 1)

# Settings screen state + localization.
rep('const lang=settings.language||"cs",t=LOCALIZATION[lang]||LOCALIZATION.en,u=key=>tr(lang,key),a=API_UI[lang]||API_UI.en,up=UPDATE_UI[lang]||UPDATE_UI.en,diagnostics=diagnosticPlaceholders(settings);', 'const lang=settings.language||"cs",t=LOCALIZATION[lang]||LOCALIZATION.en,u=key=>tr(lang,key),a=API_UI[lang]||API_UI.en,up=UPDATE_UI[lang]||UPDATE_UI.en,wp=WALLPAPER_UI[lang]||WALLPAPER_UI.en,diagnostics=diagnosticPlaceholders(settings),wallpaperFM=FileManager.iCloud(),wallpaperPath=wallpaperFM.joinPath(wallpaperFM.documentsDirectory(),BACKGROUND_FILE),hasWallpaper=wallpaperFM.fileExists(wallpaperPath);', 'settings screen vars')

# Add wallpaper entry to Appearance.
old_appearance = '${nav("layout","📐",u("layout"),settings.responsiveLayout?u("automatic"):u("manual"))}${nav("style","🎨",u("colorsFonts"))}${nav("texts","🌐",u("textsLocalization"),settings.language.toUpperCase())}'
new_appearance = '${nav("wallpaper","🖼",wp.title,settings.wallpaperSource==="generator"?wp.generator:wp.shortcut)}${nav("layout","📐",u("layout"),settings.responsiveLayout?u("automatic"):u("manual"))}${nav("style","🎨",u("colorsFonts"))}${nav("texts","🌐",u("textsLocalization"),settings.language.toUpperCase())}'
rep(old_appearance, new_appearance, 'appearance nav')

# Insert wallpaper settings screen before layout screen.
layout_screen = '<div class=\\"screen\\" id=\\"layout\\">${back}'
wallpaper_screen = '''<div class=\\"screen\\" id=\\"wallpaper\\">${back}<div class=\\"screenTitle\\">${wp.title}</div><div class=\\"screenSub\\">${wp.sub}</div><div class=\\"sectionTitle\\">${wp.source}</div><div class=\\"card\\"><div class=\\"field\\"><label>${wp.source}</label><select id=\\"wallpaperSource\\"><option value=\\"generator\\" ${settings.wallpaperSource===\\"generator\\"?\\"selected\\":\\"\\"}>🖼 ${wp.generator}</option><option value=\\"shortcut\\" ${settings.wallpaperSource!==\\"generator\\"?\\"selected\\":\\"\\"}>🎲 ${wp.shortcut}</option></select></div></div><div class=\\"sectionTitle\\">${wp.generator}</div><div class=\\"info\\" id=\\"wallpaperState\\">${hasWallpaper?wp.ready:wp.missing}</div><button type=\\"button\\" class=\\"previewBtn\\" onclick=\\"nativeAction('pickWallpaper')\\">🖼 ${hasWallpaper?wp.replace:wp.pick}</button><button type=\\"button\\" class=\\"previewBtn\\" onclick=\\"nativeAction('clearWallpaper')\\">🗑 ${wp.clear}</button><div class=\\"sectionTitle\\">${wp.shortcut}</div><div class=\\"info\\">${wp.shortcutHint}</div></div>\n  ''' + layout_screen
rep(layout_screen, wallpaper_screen, 'wallpaper screen')

# collectSettings includes the new choice.
rep("language:v('language'),showEvents", "language:v('language'),wallpaperSource:v('wallpaperSource')||'shortcut',showEvents", 'collect wallpaper source')

# Add JS callbacks before collectSettings.
collect_anchor = '  function collectSettings(){'
callbacks = '''  function wallpaperPicked(){const e=document.getElementById('wallpaperState'),s=document.getElementById('wallpaperSource');if(e)e.textContent=${JSON.stringify(wp.ready)};if(s)s.value='generator'}\n  function wallpaperCleared(){const e=document.getElementById('wallpaperState');if(e)e.textContent=${JSON.stringify(wp.missing)}}\n'''
if collect_anchor not in src:
    raise SystemExit('collectSettings anchor missing')
src = src.replace(collect_anchor, callbacks + collect_anchor, 1)

# Native WebView actions for photo picker and clear.
old_actions = '}else if(msg.action==="openURL"&&msg.url){Safari.open(msg.url)}else if(msg.action==="calendarSources")'
new_actions = '''}else if(msg.action==="openURL"&&msg.url){Safari.open(msg.url)}else if(msg.action==="pickWallpaper"){try{const img=await Photos.fromLibrary(),fm=FileManager.iCloud(),p=fm.joinPath(fm.documentsDirectory(),BACKGROUND_FILE);fm.write(p,Data.fromPNG(img));settings.wallpaperSource="generator";try{await wv.evaluateJavaScript("wallpaperPicked()") }catch(_){}}catch(e){console.error("Wallpaper picker: "+e)}}else if(msg.action==="clearWallpaper"){try{const fm=FileManager.iCloud(),p=fm.joinPath(fm.documentsDirectory(),BACKGROUND_FILE);if(fm.fileExists(p))fm.remove(p);try{await wv.evaluateJavaScript("wallpaperCleared()") }catch(_){}}catch(e){console.error("Wallpaper clear: "+e)}}else if(msg.action==="calendarSources")'''
rep(old_actions, new_actions, 'native wallpaper actions')

# Saved settings schema bump.
rep('settingsVersion:8};saveSettings(settings)', 'settingsVersion:9};saveSettings(settings)', 'settings save version')

# Preview should show the stored background in generator mode.
old_preview = 'const image=await buildImage(resolveResolution(),draft);const dataUrl="data:image/png;base64,"+Data.fromPNG(image).toBase64String();'
new_preview = 'const previewSize=resolveResolution(),overlay=await buildImage(previewSize,draft),bg=draft.wallpaperSource==="generator"?await loadStoredBackground():null,image=bg?composeWallpaper(previewSize,bg,overlay):overlay;const dataUrl="data:image/png;base64,"+Data.fromPNG(image).toBase64String();'
rep(old_preview, new_preview, 'preview composition')

js_path.write_text(src, encoding='utf-8')

readme = readme_path.read_text(encoding='utf-8')
section = '''\n## 🖼 Zdroje tapety (v2.10.0)\n\nLockScreen Generator má dva režimy základní fotografie:\n\n- **Fotka uložená v generátoru** – v Nastavení → Tapeta jednou vyber fotografii. Při spuštění ze Zkratek není potřeba žádný vstupní obrázek; skript vytvoří hotovou tapetu.\n- **Fotka ze Zkratek** – Zkratka může vybrat libovolnou nebo náhodnou fotografii z alba a předat ji do pole **Images** akce **Run Script**. Generátor fotografii sám ořízne na poměr displeje a spojí s překrytím.\n\nPokud je dostupná základní fotka, skript uloží hotový výsledek do `LockScreenWallpaper.png` a vrátí jeho iCloud cestu. Starý režim `overlay`/Base64 zůstává jako kompatibilní fallback, když není předaná ani uložená fotka.\n'''
if '## 🖼 Zdroje tapety (v2.10.0)' not in readme:
    readme += section
readme_path.write_text(readme, encoding='utf-8')

# Basic migration assertions.
assert 'const APP_VERSION = "2.10.0";' in src
assert 'wallpaperSource:"shortcut"' in src
assert 'Array.isArray(args.images)&&args.images.length?args.images[0]:null' in src
assert 'Photos.fromLibrary()' in src
assert 'composeWallpaper(size,background,overlay)' in src
assert 'const overlayBase64=png.toBase64String()' in src
print('LockScreen Generator v2.10.0 wallpaper sources patched')
