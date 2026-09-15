from pathlib import Path

js = Path('apps/LockScreenGenerator/LockScreenGenerator.js')
readme = Path('apps/LockScreenGenerator/README.md')
workflow = Path('.github/workflows/build-scriptable-package.yml')

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

wf = workflow.read_text(encoding='utf-8')
old_guard = """          # Scriptable only documents Shortcut file-path outputs for files stored in iCloud.
          assert 'LockScreenOverlay.png' in src, 'Shortcut overlay PNG output missing'
          assert 'fm.documentsDirectory()' in src, 'Shortcut overlay is not written to Scriptable iCloud Documents'
          assert 'local.temporaryDirectory()' not in src, 'Shortcut overlay must not use a local temporary path'
          assert 'Script.setShortcutOutput(out)' in src, 'Shortcut overlay file is not returned to Shortcuts'
          assert 'Data.fromPNG(image)' in src, 'Shortcut overlay is not encoded as PNG data'
"""
new_guard = """          # Shortcuts overlay output: return the transparent PNG as Base64 text.
          assert 'const overlayBase64=png.toBase64String()' in src, 'Shortcut overlay Base64 conversion missing'
          assert 'Script.setShortcutOutput(overlayBase64)' in src, 'Shortcut overlay Base64 is not returned to Shortcuts'
          assert 'Data.fromPNG(image)' in src, 'Shortcut overlay is not encoded as PNG data'
          assert 'Script.setShortcutOutput(out)' not in src, 'Old file-path Shortcut output still present'
"""
if old_guard not in wf:
    raise SystemExit('workflow guard block not found')
wf = wf.replace(old_guard, new_guard, 1)
workflow.write_text(wf, encoding='utf-8')

assert 'const APP_VERSION = "2.9.9";' in src
assert 'Script.setShortcutOutput(overlayBase64)' in src
assert 'LockScreenOverlay.png' not in src
print('LockScreen Generator v2.9.9 Base64 output patched')
