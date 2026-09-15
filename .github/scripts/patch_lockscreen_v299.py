from pathlib import Path

js = Path('apps/LockScreenGenerator/LockScreenGenerator.js')
readme = Path('apps/LockScreenGenerator/README.md')

src = js.read_text(encoding='utf-8')
old = 'const APP_VERSION = "2.9.8";'
new = 'const APP_VERSION = "2.9.9";'
if src.count(old) != 1:
    raise SystemExit(f'APP_VERSION match count={src.count(old)}')
src = src.replace(old, new, 1)

old_main = 'if(shortcutRun){const out=fm.joinPath(fm.documentsDirectory(),"LockScreenOverlay.png");fm.write(out,png);Script.setShortcutOutput(out);Script.complete();return}'
new_main = 'if(shortcutRun){const overlayBase64=png.toBase64String();Script.setShortcutOutput(overlayBase64);Script.complete();return}'
if src.count(old_main) != 1:
    raise SystemExit(f'shortcut output match count={src.count(old_main)}')
src = src.replace(old_main, new_main, 1)
js.write_text(src, encoding='utf-8')

md = readme.read_text(encoding='utf-8')
old_md = 'Skript uloží `LockScreenWallpaper.png` a vrátí cestu k výsledku. Ve Zkratkách pak stačí přibližně: **Spustit Scriptable skript → získat obrázek → Nastavit tapetu Lock Screenu**.'
new_md = 'Pro Zkratky použij parametr `overlay`. Skript vrátí průhledné PNG jako **Base64 text** (stejný princip jako původní LSWeather), takže nejsme závislí na předávání cesty k souboru. Ve Zkratkách použij: **Spustit Scriptable skript (`overlay`) → Base64: Dekódovat → Získat obrázek ze vstupu → Překrýt původní fotku → Nastavit tapetu Lock Screenu**.'
if old_md not in md:
    raise SystemExit('README automation paragraph not found')
md = md.replace(old_md, new_md, 1)
readme.write_text(md, encoding='utf-8')

assert 'const APP_VERSION = "2.9.9";' in src
assert 'Script.setShortcutOutput(overlayBase64)' in src
assert 'LockScreenOverlay.png' not in src
print('LockScreen Generator v2.9.9 Base64 output patched')
