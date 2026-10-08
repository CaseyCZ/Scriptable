from pathlib import Path

pages = [Path('index.html'), Path('guide.html'), Path('credits.html')]
old_css = 'ios-hub-visual.css?v=20261008-authorstatus1'
new_css = 'ios-hub-visual.css?v=20261008-mobile2'
old_js = '<script src="mobile-menu.js"></script>'
new_js = '<script src="mobile-menu.js?v=20261008-mobile2"></script>'

for page in pages:
    text = page.read_text(encoding='utf-8')
    text = text.replace(old_css, new_css)
    text = text.replace(old_js, new_js)
    if new_css not in text:
        raise SystemExit(f'CSS cache-buster missing in {page}')
    if new_js not in text:
        raise SystemExit(f'Mobile menu script missing in {page}')
    page.write_text(text, encoding='utf-8')

css_path = Path('ios-hub-visual.css')
css = css_path.read_text(encoding='utf-8')
marker = '/* Landscape/mobile navigation enforcement — same 900px behavior as iOS Hub */'
block = '''\n\n/* Landscape/mobile navigation enforcement — same 900px behavior as iOS Hub */\n@media (min-width:901px){\n  .topbar .nav{display:flex!important}\n  .topbar .mobile-menu-button{display:none!important}\n  .topbar .mobile-nav-panel{display:none!important}\n}\n@media (max-width:900px){\n  .topbar .nav{display:none!important}\n  .topbar .mobile-menu-button{display:grid!important}\n  .topbar.mobile-menu-open .mobile-nav-panel{display:block!important}\n}\n'''
if marker not in css:
    css += block
css_path.write_text(css, encoding='utf-8')

print('Landscape navigation and cache-busters updated.')
