from pathlib import Path

navs = {
    'index.html': '''<nav class="nav" aria-label="Primary">
        <a href="#ourApps"><span data-cs="Naše aplikace" data-en="Our apps" data-de="Unsere Apps" data-es="Nuestras apps" data-fr="Nos apps">Naše aplikace</span></a>
        <a href="guide.html"><span data-cs="Průvodce" data-en="Guide" data-de="Anleitung" data-es="Guía" data-fr="Guide">Průvodce</span></a>
        <a href="#community"><span data-cs="Komunita" data-en="Community" data-de="Community" data-es="Comunidad" data-fr="Communauté">Komunita</span></a>
        <a href="credits.html">Credits</a>
      </nav>''',
    'guide.html': '''<nav class="nav" aria-label="Primary">
        <a href="./#ourApps"><span data-cs="Naše aplikace" data-en="Our apps" data-de="Unsere Apps" data-es="Nuestras apps" data-fr="Nos apps">Naše aplikace</span></a>
        <a href="guide.html" class="active" aria-current="page"><span data-cs="Průvodce" data-en="Guide" data-de="Anleitung" data-es="Guía" data-fr="Guide">Průvodce</span></a>
        <a href="./#community"><span data-cs="Komunita" data-en="Community" data-de="Community" data-es="Comunidad" data-fr="Communauté">Komunita</span></a>
        <a href="credits.html">Credits</a>
      </nav>''',
    'credits.html': '''<nav class="nav" aria-label="Primary">
      <a href="./#ourApps"><span data-cs="Naše aplikace" data-en="Our apps" data-de="Unsere Apps" data-es="Nuestras apps" data-fr="Nos apps">Naše aplikace</span></a>
      <a href="guide.html"><span data-cs="Průvodce" data-en="Guide" data-de="Anleitung" data-es="Guía" data-fr="Guide">Průvodce</span></a>
      <a href="./#community"><span data-cs="Komunita" data-en="Community" data-de="Community" data-es="Comunidad" data-fr="Communauté">Komunita</span></a>
      <a href="credits.html" class="active" aria-current="page">Credits</a>
    </nav>''',
}

for filename, new_nav in navs.items():
    p = Path(filename)
    text = p.read_text()
    start = text.index('<nav class="nav"')
    end = text.index('</nav>', start) + len('</nav>')
    p.write_text(text[:start] + new_nav + text[end:])

css = Path('ios-hub-visual.css')
text = css.read_text()
active = '.nav a.active{background:var(--accent-soft);color:var(--accent)}'
if active not in text:
    marker = '.nav a:hover{background:var(--panel2);color:var(--text)}'
    if marker not in text:
        raise RuntimeError('nav hover marker not found')
    css.write_text(text.replace(marker, marker + '\n' + active, 1))

for filename in ('index.html', 'guide.html', 'credits.html'):
    text = Path(filename).read_text()
    start = text.index('<nav class="nav"')
    end = text.index('</nav>', start)
    nav = text[start:end]
    assert 'scriptable.app' not in nav
    assert nav.index('ourApps') < nav.index('guide.html') < nav.index('community') < nav.index('credits.html')

assert 'guide.html" class="active" aria-current="page"' in Path('guide.html').read_text()
assert 'credits.html" class="active" aria-current="page"' in Path('credits.html').read_text()
print('Header navigation synced with iOS Hub behavior.')
