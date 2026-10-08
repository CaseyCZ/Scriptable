from pathlib import Path

JS = r'''function setupMobileMenu() {
  const header = document.querySelector('.topbar');
  const nav = header?.querySelector('.nav');
  const actions = header?.querySelector('.nav-actions');
  if (!header || !nav || !actions || document.getElementById('mobileMenuButton')) return;

  const button = document.createElement('button');
  button.id = 'mobileMenuButton';
  button.className = 'icon-btn mobile-menu-button';
  button.type = 'button';
  button.setAttribute('aria-label', 'Menu');
  button.setAttribute('aria-expanded', 'false');
  button.setAttribute('aria-controls', 'mobileNavPanel');
  button.innerHTML = '<span class="mobile-menu-icon" aria-hidden="true"></span>';
  actions.appendChild(button);

  const panel = document.createElement('div');
  panel.id = 'mobileNavPanel';
  panel.className = 'mobile-nav-panel';
  panel.setAttribute('aria-hidden', 'true');
  panel.innerHTML = '<div class="wrap mobile-nav-inner"><nav class="mobile-nav-links" aria-label="Mobile navigation">' + nav.innerHTML + '</nav></div>';
  header.appendChild(panel);

  const setOpen = (open, restoreFocus = false) => {
    const wasOpen = header.classList.contains('mobile-menu-open');
    header.classList.toggle('mobile-menu-open', open);
    panel.setAttribute('aria-hidden', String(!open));
    button.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('mobile-menu-visible', open);
    if (!open && wasOpen && restoreFocus) requestAnimationFrame(() => button.focus());
  };

  button.addEventListener('click', event => {
    event.stopPropagation();
    const settingsMenu = document.querySelector('.settings-menu');
    const settingsPanel = document.getElementById('settingsPanel');
    settingsMenu?.classList.remove('open');
    settingsPanel?.classList.remove('open');
    document.getElementById('settingsBtn')?.setAttribute('aria-expanded', 'false');
    settingsPanel?.setAttribute('aria-hidden', 'true');
    setOpen(!header.classList.contains('mobile-menu-open'));
  });

  panel.addEventListener('click', event => {
    if (event.target.closest('a')) setOpen(false);
  });

  document.addEventListener('click', event => {
    if (!header.contains(event.target)) setOpen(false);
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && header.classList.contains('mobile-menu-open')) {
      event.preventDefault();
      setOpen(false, true);
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) setOpen(false);
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', setupMobileMenu, { once: true });
} else {
  setupMobileMenu();
}
'''

CSS = r'''

/* Mobile navigation — synced 1:1 with iOS Hub */
.mobile-menu-button{display:none}
.mobile-menu-icon{position:relative;width:18px;height:2px;border-radius:999px;background:currentColor;display:block}
.mobile-menu-icon::before,.mobile-menu-icon::after{content:"";position:absolute;left:0;width:18px;height:2px;border-radius:999px;background:currentColor;transition:transform .18s ease,top .18s ease,opacity .18s ease}
.mobile-menu-icon::before{top:-6px}
.mobile-menu-icon::after{top:6px}
.mobile-menu-open .mobile-menu-icon{background:transparent}
.mobile-menu-open .mobile-menu-icon::before{top:0;transform:rotate(45deg)}
.mobile-menu-open .mobile-menu-icon::after{top:0;transform:rotate(-45deg)}
.mobile-nav-panel{display:none;position:absolute;right:16px;top:calc(100% + 8px);z-index:150;width:220px;padding:8px;border:1px solid var(--border);border-radius:14px;background:color-mix(in srgb,var(--panel) 98%,transparent);box-shadow:var(--shadow)}
.mobile-menu-open .mobile-nav-panel{display:block}
.mobile-nav-inner{width:100%;padding:0;margin:0}
.mobile-nav-links{display:grid;grid-template-columns:1fr;gap:4px}
.mobile-nav-links a{width:100%;min-height:40px;padding:0 10px;border:1px solid transparent;border-radius:10px;background:transparent;color:var(--text);display:flex;align-items:center;justify-content:flex-start;text-align:left;font-size:11px;font-weight:800}
.mobile-nav-links a:hover{background:var(--panel2);border-color:var(--border)}
.mobile-nav-links a.active{background:var(--accent-soft);border-color:color-mix(in srgb,var(--accent) 45%,var(--border));color:var(--accent)}
@media(max-width:900px){.mobile-menu-button{display:grid}.topbar{overflow:visible}}
@media(max-width:640px){.topbar-inner{gap:7px}.nav-actions{gap:5px}.mobile-nav-panel{right:10px;left:auto;top:calc(100% + 8px);width:220px}}
'''

Path('mobile-menu.js').write_text(JS)

css_path = Path('ios-hub-visual.css')
css = css_path.read_text()
marker = '/* Mobile navigation — synced 1:1 with iOS Hub */'
if marker not in css:
    css_path.write_text(css.rstrip() + CSS + '\n')

for filename in ('index.html', 'guide.html', 'credits.html'):
    path = Path(filename)
    text = path.read_text()
    tag = '<script src="mobile-menu.js"></script>'
    if tag not in text:
        if '</body>' not in text:
            raise SystemExit(f'{filename}: missing </body>')
        text = text.replace('</body>', f'{tag}\n</body>', 1)
        path.write_text(text)

# Validation
for filename in ('index.html', 'guide.html', 'credits.html'):
    text = Path(filename).read_text()
    assert '<script src="mobile-menu.js"></script>' in text
assert 'mobile-menu-button' in Path('ios-hub-visual.css').read_text()
assert "button.id = 'mobileMenuButton'" in Path('mobile-menu.js').read_text()
print('iOS Hub mobile menu installed on index, guide and credits')
