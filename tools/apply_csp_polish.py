#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
JS_DIR = ROOT / 'assets' / 'js'
JS_DIR.mkdir(parents=True, exist_ok=True)

PAGES = {
    'index.html': 'index-page.js',
    'guide.html': 'guide-page.js',
    'credits.html': 'credits-page.js',
    'privacy.html': 'privacy-page.js',
}

CSP = "default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; img-src 'self' https: data: blob:; connect-src 'self' https:; object-src 'none'; base-uri 'self'; form-action 'none'"
INLINE_SCRIPT = re.compile(r'<script(?![^>]*\bsrc\s*=)([^>]*)>(.*?)</script>', re.I | re.S)

for page_name, js_name in PAGES.items():
    path = ROOT / page_name
    text = path.read_text(encoding='utf-8')

    matches = list(INLINE_SCRIPT.finditer(text))
    if matches:
        scripts = []
        for match in matches:
            attrs = match.group(1) or ''
            if re.search(r'\btype\s*=\s*["\']application/(?:ld\+)?json["\']', attrs, re.I):
                continue
            body = match.group(2).strip()
            if body:
                scripts.append(body)

        if scripts:
            (JS_DIR / js_name).write_text('\n\n'.join(scripts) + '\n', encoding='utf-8')
            inserted = False
            def replace_inline(match):
                nonlocal_placeholder = None
                attrs = match.group(1) or ''
                if re.search(r'\btype\s*=\s*["\']application/(?:ld\+)?json["\']', attrs, re.I):
                    return match.group(0)
                body = match.group(2).strip()
                if not body:
                    return ''
                return '__PAGE_SCRIPT__' if not replace_inline.used else ''
            replace_inline.used = False
            def replacement(match):
                attrs = match.group(1) or ''
                if re.search(r'\btype\s*=\s*["\']application/(?:ld\+)?json["\']', attrs, re.I):
                    return match.group(0)
                if not match.group(2).strip():
                    return ''
                if not replacement.used:
                    replacement.used = True
                    return f'<script src="./assets/js/{js_name}?v=20261009-csp1"></script>'
                return ''
            replacement.used = False
            text = INLINE_SCRIPT.sub(replacement, text)

    if 'http-equiv="Content-Security-Policy"' not in text:
        marker = '<meta name="referrer" content="no-referrer">'
        if marker not in text:
            raise SystemExit(f'Referrer marker missing in {page_name}')
        text = text.replace(marker, marker + f'\n<meta http-equiv="Content-Security-Policy" content="{CSP}">', 1)

    path.write_text(text, encoding='utf-8')

print('Externalized inline JavaScript and enabled CSP on index, guide, credits and privacy pages.')
