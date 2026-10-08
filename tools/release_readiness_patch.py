#!/usr/bin/env python3
from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
extra_path=root/'community-extra.js'
index_path=root/'index.html'
readme_path=root/'README.md'
readme_en_path=root/'README_EN.md'

extra=extra_path.read_text(encoding='utf-8')
index=index_path.read_text(encoding='utf-8')
readme=readme_path.read_text(encoding='utf-8')
readme_en=readme_en_path.read_text(encoding='utf-8')

# ONE-Friday still exists upstream, but the encoded filename was removed.
old='https://raw.githubusercontent.com/Nicolasking007/Scriptable/main/ONE-Friday/ONE-Friday.Enc.js'
new='https://raw.githubusercontent.com/Nicolasking007/Scriptable/main/ONE-Friday/ONE-Friday.js'
if old not in extra:
    raise SystemExit('ONE-Friday legacy URL not found')
extra=extra.replace(old,new,1).replace('"ONE-Friday.Enc.js"','"ONE-Friday.js"',1)

# These projects no longer have an installable script in the current upstream tree.
for name in ['ONE-Memorandum','ONE-LOLMATCH','ONE-FOOTMATCH']:
    pattern=re.compile(r'^communityItem\("'+re.escape(name)+r'"[^\n]*\),\n?',re.M)
    extra,n=pattern.subn('',extra,count=1)
    if n!=1:
        raise SystemExit(f'Expected one {name} entry, removed {n}')

# Add the Getting Started guide to the hero actions.
old_hero='<div class="heroActions"><a class="btn primary" href="#ourApps">⬇️ <span data-cs="Naše aplikace" data-en="Our apps">Naše aplikace</span></a><a class="btn secondary" href="#community">🌍 <span data-cs="Ostatní vývojáři" data-en="Other developers">Ostatní vývojáři</span></a></div>'
new_hero='<div class="heroActions"><a class="btn primary" href="#ourApps">⬇️ <span data-cs="Naše aplikace" data-en="Our apps">Naše aplikace</span></a><a class="btn secondary" href="#community">🌍 <span data-cs="Ostatní vývojáři" data-en="Other developers">Ostatní vývojáři</span></a><a class="btn secondary" href="guide.html">📘 <span data-cs="Jak začít" data-en="Getting started">Jak začít</span></a></div>'
if 'href="guide.html"' not in index:
    if old_hero not in index:
        raise SystemExit('Hero actions marker not found')
    index=index.replace(old_hero,new_hero,1)

# Add release documentation to the footer.
footer_marker='          <a href="https://caseycz.github.io/" target="_blank" rel="noopener">Website</a>\n          <a href="https://github.com/CaseyCZ/Scriptable" target="_blank" rel="noopener">GitHub · Scriptable</a>'
footer_repl='          <a href="https://caseycz.github.io/" target="_blank" rel="noopener">Website</a>\n          <a href="guide.html">Guide</a>\n          <a href="CHANGELOG.md">Changelog</a>\n          <a href="COMPLIANCE.md">Compliance</a>\n          <a href="https://github.com/CaseyCZ/Scriptable" target="_blank" rel="noopener">GitHub · Scriptable</a>'
if 'href="COMPLIANCE.md">Compliance</a>' not in index:
    if footer_marker not in index:
        raise SystemExit('Footer marker not found')
    index=index.replace(footer_marker,footer_repl,1)

# Make release documentation visible from both root READMEs.
cz_docs='''## Dokumentace\n\n- 📘 [Jak začít](https://caseycz.github.io/Scriptable/guide.html)\n- 📝 [Changelog](CHANGELOG.md)\n- 🛡️ [Community catalog compliance](COMPLIANCE.md)\n- 🔐 [Security](SECURITY.md)\n- 🤝 [Contributing](CONTRIBUTING.md)\n\n'''
if '## Dokumentace' not in readme:
    if '## Aplikace\n' not in readme: raise SystemExit('README Apps marker missing')
    readme=readme.replace('## Aplikace\n',cz_docs+'## Aplikace\n',1)

en_docs='''## Documentation\n\n- 📘 [Getting started](https://caseycz.github.io/Scriptable/guide.html)\n- 📝 [Changelog](CHANGELOG.md)\n- 🛡️ [Community catalog compliance](COMPLIANCE.md)\n- 🔐 [Security](SECURITY.md)\n- 🤝 [Contributing](CONTRIBUTING.md)\n\n'''
if '## Documentation' not in readme_en:
    if '## Apps\n' not in readme_en: raise SystemExit('README_EN Apps marker missing')
    readme_en=readme_en.replace('## Apps\n',en_docs+'## Apps\n',1)

extra_path.write_text(extra,encoding='utf-8')
index_path.write_text(index,encoding='utf-8')
readme_path.write_text(readme,encoding='utf-8')
readme_en_path.write_text(readme_en,encoding='utf-8')
print('Release readiness patch applied: Friday fixed, three dead entries removed, guide/docs linked.')
