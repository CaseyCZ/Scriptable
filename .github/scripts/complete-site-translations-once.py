from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

script_tag = '  <script src="./site-i18n.js?v=20261005-full1"></script>\n'
marker = '  <script src="./community-extra.js"></script>\n'
if script_tag not in html:
    if marker not in html:
        raise SystemExit('community-extra script marker not found')
    html = html.replace(marker, script_tag + marker, 1)

old_tr = "    const tr=(cs,en)=>lang==='cs'?cs:en;"
new_tr = "    const uiText=(cs,en)=>window.ScriptableI18n?.translate(cs,en,lang)||(lang==='cs'?cs:en);\n    const tr=(cs,en)=>uiText(cs,en);\n    const appTr=(cs,en)=>lang==='cs'?cs:en;"
if old_tr not in html:
    raise SystemExit('tr helper not found')
html = html.replace(old_tr, new_tr, 1)

old_set = "    function setLanguage(next){lang=SUPPORTED_LANGS.includes(next)?next:'en';localStorage.setItem('siteLang',lang);document.documentElement.lang=lang;document.querySelectorAll('[data-cs]').forEach(el=>{el.textContent=el.getAttribute('data-'+lang)||el.getAttribute('data-en')||el.getAttribute('data-cs')||el.textContent});const search=document.getElementById('communitySearch');if(search)search.placeholder=search.getAttribute('data-placeholder-'+lang)||search.getAttribute('data-placeholder-en')||search.getAttribute('data-placeholder-cs')||'';document.querySelectorAll('[data-language]').forEach(btn=>btn.classList.toggle('active',btn.dataset.language===lang));renderAll()}"
new_set = "    function setLanguage(next){lang=SUPPORTED_LANGS.includes(next)?next:'en';localStorage.setItem('siteLang',lang);document.documentElement.lang=lang;document.querySelectorAll('[data-cs]').forEach(el=>{el.textContent=el.getAttribute('data-'+lang)||uiText(el.getAttribute('data-cs'),el.getAttribute('data-en'))||el.textContent});const search=document.getElementById('communitySearch');if(search)search.placeholder=search.getAttribute('data-placeholder-'+lang)||uiText(search.getAttribute('data-placeholder-cs'),search.getAttribute('data-placeholder-en'))||'';document.querySelectorAll('[data-language]').forEach(btn=>btn.classList.toggle('active',btn.dataset.language===lang));const settings=document.getElementById('settingsBtn');if(settings){const label=uiText('Nastavení','Settings');settings.title=label;settings.setAttribute('aria-label',label)}const grid=document.getElementById('layoutGrid');if(grid)grid.title=uiText('Mřížka','Grid');const list=document.getElementById('layoutList');if(list)list.title=uiText('Seznam','List');const close=document.querySelector('[data-support-close]');if(close)close.setAttribute('aria-label',uiText('Zavřít','Close'));const nav=document.querySelector('nav.nav');if(nav)nav.setAttribute('aria-label',uiText('Hlavní navigace','Primary'));renderAll()}"
if old_set not in html:
    raise SystemExit('setLanguage helper not found')
html = html.replace(old_set, new_set, 1)

old_category = "    function categoryLabel(category){const x=CATEGORY_LABELS[category]||{cs:category,en:category};return x[lang]||x.en||x.cs||category}"
new_category = "    function categoryLabel(category){const x=CATEGORY_LABELS[category]||{cs:category,en:category};return uiText(x.cs||category,x.en||x.cs||category)}"
if old_category not in html:
    raise SystemExit('categoryLabel helper not found')
html = html.replace(old_category, new_category, 1)

start = html.find('    function researchedFeatures(')
end = html.find('    function cardHtml(', start)
if start < 0 or end < 0:
    raise SystemExit('researchedFeatures block not found')
block = html[start:end]
block2 = block.replace('tr(', 'appTr(')
if block == block2:
    raise SystemExit('no app-content tr calls found')
html = html[:start] + block2 + html[end:]

# The app descriptions/features intentionally remain CZ/EN only and fall back to English.
if "const rawFeatures=(app.features&&app.features[lang])||app.features?.en||app.features?.cs||[]" not in html:
    raise SystemExit('app feature fallback changed unexpectedly')
if "app.description?.[lang]||app.description?.en||app.description?.cs||''" not in html:
    raise SystemExit('app description fallback changed unexpectedly')

path.write_text(html, encoding='utf-8')
