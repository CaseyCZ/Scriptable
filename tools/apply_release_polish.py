#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# One-time release polish helper.
# 2) Remove a known non-widget config entry from the curated catalog.
extra = ROOT / 'community-extra.js'
text = extra.read_text(encoding='utf-8')
lines = text.splitlines()
lines = [line for line in lines if 'communityItem(".eslintrc by Honye"' not in line]
text = '\n'.join(lines) + '\n'
text = text.replace('// Honye — 31', '// Honye — 30')
extra.write_text(text, encoding='utf-8')

# Shared accessibility CSS, matching iOS Hub.
css = ROOT / 'ios-hub-visual.css'
text = css.read_text(encoding='utf-8')
if '.skip-link{' not in text:
    text = '.skip-link{position:fixed;left:12px;top:10px;z-index:1200;padding:9px 12px;border:1px solid var(--accent);border-radius:10px;background:var(--panel);color:var(--text);font-size:11px;font-weight:900;transform:translateY(-160%);transition:transform .15s}.skip-link:focus{transform:translateY(0);outline:3px solid color-mix(in srgb,var(--accent) 35%,transparent);outline-offset:2px}\n' + text
css.write_text(text, encoding='utf-8')

PAGES = {
    'index.html': {
        'canonical': 'https://caseycz.github.io/Scriptable/',
        'title': 'Scriptable Apps',
        'description': 'Useful Scriptable apps and a curated catalog of community widgets for iPhone.',
        'analytics': 'Scriptable Apps',
    },
    'guide.html': {
        'canonical': 'https://caseycz.github.io/Scriptable/guide.html',
        'title': 'Guide · Scriptable Apps',
        'description': 'Getting started with Scriptable Apps and community widgets.',
        'analytics': 'Guide · Scriptable Apps',
    },
    'credits.html': {
        'canonical': 'https://caseycz.github.io/Scriptable/credits.html',
        'title': 'Credits & Acknowledgements · Scriptable Apps',
        'description': 'Credits and acknowledgements for Scriptable Apps, upstream projects and the community catalog.',
        'analytics': 'Credits & Acknowledgements · Scriptable Apps',
    },
}

for filename, meta in PAGES.items():
    path = ROOT / filename
    text = path.read_text(encoding='utf-8')

    if 'rel="canonical"' not in text:
        viewport_marker = '<meta id="themeColor" name="theme-color" content="#070b14">'
        if viewport_marker not in text:
            viewport_marker = '  <meta id="themeColor" name="theme-color" content="#070b14">'
        block = (
            f'\n<meta name="referrer" content="no-referrer">'
            f'\n<link rel="canonical" href="{meta["canonical"]}">'
            f'\n<meta property="og:type" content="website">'
            f'\n<meta property="og:site_name" content="Scriptable Apps">'
            f'\n<meta property="og:title" content="{meta["title"]}">'
            f'\n<meta property="og:description" content="{meta["description"]}">'
            f'\n<meta property="og:url" content="{meta["canonical"]}">'
            f'\n<meta name="twitter:card" content="summary">'
            f'\n<meta name="analytics-page-title" content="{meta["analytics"]}">'
        )
        if viewport_marker not in text:
            raise SystemExit(f'theme-color marker not found in {filename}')
        text = text.replace(viewport_marker, viewport_marker + block, 1)

    if 'class="skip-link"' not in text:
        text = text.replace('<body>', '<body>\n<a class="skip-link" href="#top" data-cs="Přeskočit na obsah" data-en="Skip to content" data-de="Zum Inhalt springen" data-es="Saltar al contenido" data-fr="Aller au contenu">Přeskočit na obsah</a>', 1)

    text = text.replace('id="settingsPanel" class="settings-panel" role="dialog" aria-hidden="true"', 'id="settingsPanel" class="settings-panel" role="dialog" aria-labelledby="settingsTitle" aria-hidden="true"')
    text = text.replace('<div class="settings-title">', '<div id="settingsTitle" class="settings-title">', 1)

    for code, element_id in [('cs','langCs'),('en','langEn'),('de','langDe'),('es','langEs'),('fr','langFr')]:
        old = f'<button id="{element_id}" type="button" data-language="{code}">'
        new = f'<button id="{element_id}" type="button" data-language="{code}" role="radio" aria-checked="false">'
        text = text.replace(old, new)

    for element_id in ('themeDark','themeLight','layoutGrid','layoutList'):
        text = text.replace(f'<button id="{element_id}" type="button"', f'<button id="{element_id}" type="button" aria-pressed="false"', 1)

    if 'href="privacy.html"' not in text:
        marker = '<button class="footer-link-button" type="button" data-cookie-settings>'
        if marker in text:
            text = text.replace(marker, '<a href="privacy.html">Privacy &amp; Cookies</a>' + marker, 1)
        else:
            raise SystemExit(f'cookie footer marker not found in {filename}')

    a11y_script = '''<script id="settingsA11ySync">\n(()=>{\n  const sync=()=>{\n    const lang=(localStorage.getItem('siteLang')||document.documentElement.lang||'en').slice(0,2);\n    document.querySelectorAll('[data-language]').forEach(btn=>btn.setAttribute('aria-checked',String(btn.dataset.language===lang)));\n    const theme=document.documentElement.dataset.theme||localStorage.getItem('siteTheme')||'dark';\n    document.getElementById('themeDark')?.setAttribute('aria-pressed',String(theme==='dark'));\n    document.getElementById('themeLight')?.setAttribute('aria-pressed',String(theme==='light'));\n    const layout=localStorage.getItem('siteLayout')||'grid';\n    document.getElementById('layoutGrid')?.setAttribute('aria-pressed',String(layout==='grid'));\n    document.getElementById('layoutList')?.setAttribute('aria-pressed',String(layout==='list'));\n  };\n  sync();\n  document.addEventListener('click',e=>{if(e.target.closest('[data-language],#themeDark,#themeLight,#layoutGrid,#layoutList'))requestAnimationFrame(sync)});\n})();\n</script>\n'''
    if 'id="settingsA11ySync"' not in text:
        pos = text.rfind('<script src="mobile-menu.js')
        if pos < 0:
            pos = text.rfind('<script src="./mobile-menu.js')
        if pos < 0:
            raise SystemExit(f'mobile menu script marker not found in {filename}')
        text = text[:pos] + a11y_script + text[pos:]

    path.write_text(text, encoding='utf-8')

print('Release polish applied: catalog quality, SEO metadata, Privacy links and accessibility.')
