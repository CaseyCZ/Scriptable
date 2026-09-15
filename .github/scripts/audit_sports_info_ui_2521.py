from pathlib import Path
import re, json

src = Path('apps/Sports-Info/Sports Info.js').read_text(encoding='utf-8')
html = Path('/tmp/sports-settings.html').read_text(encoding='utf-8')
script_m = re.search(r'<script>([\s\S]*?)</script>', html)
assert script_m, 'settings <script> missing'
ui = script_m.group(1)

# HTML structure / IDs
ids = re.findall(r'\bid="([^"]+)"', html)
duplicates = sorted({x for x in ids if ids.count(x) > 1})
assert not duplicates, f'duplicate HTML ids: {duplicates}'
screens = set(re.findall(r'class="screen(?: active)?" id="([^"]+)"', html))
expected_screens = {'home','sport','content','layout','layoutSmall','layoutMedium','layoutLarge','appearance','api','diagnostics','maintenance'}
assert expected_screens <= screens, f'missing screens: {sorted(expected_screens-screens)}'

# Every literal onclick function must exist in the rendered JS.
onclick = re.findall(r'onclick="\s*([A-Za-z_$][\w$]*)\s*\(', html)
functions = set(re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', ui))
missing_funcs = sorted(set(onclick)-functions)
assert not missing_funcs, f'onclick without function: {missing_funcs}'

# Every literal showScreen target must exist.
targets = set(re.findall(r"showScreen\('([^']+)'\)", html)) | set(re.findall(r"showScreen\('([^']+)'\)", ui))
assert targets <= screens, f'showScreen target missing: {sorted(targets-screens)}'

# Emitted UI actions must be consumed by native settings loop.
emitted = set(re.findall(r"emit\(['\"]([A-Za-z0-9_]+)['\"]", ui))
handled_native = set(re.findall(r"m\.action\s*={2,3}\s*['\"]([A-Za-z0-9_]+)['\"]", src))
missing_native = sorted(emitted-handled_native)
assert not missing_native, f'UI emits actions with no native handler: {missing_native}'

# Native messages back to the WebView must be handled by window.__native.
sent = set(re.findall(r"send\(web,\{action:['\"]([A-Za-z0-9_]+)['\"]", src))
handled_web = set(re.findall(r"m\.action\s*={2,3}\s*['\"]([A-Za-z0-9_]+)['\"]", ui))
missing_web = sorted(sent-handled_web)
assert not missing_web, f'native sends actions with no WebView handler: {missing_web}'

# Literal DOM IDs referenced by JS should exist, except explicitly optional legacy placeholder.
refs = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", ui))
optional = {'previewMeta'}
missing_ids = sorted(refs-set(ids)-optional)
assert not missing_ids, f'getElementById references missing elements: {missing_ids}'

# Critical controls/functions currently expected.
for fn in ['showScreen','commitNow','save','fillLeagues','loadTeams','preview','runDiagnostics','exportJSON','importJSON','resetPart','resetLayout','clearCache','recommendedWidget','requestUpdate','renderDiag']:
    assert fn in functions, f'critical UI function missing: {fn}'
for action in ['save','teams','preview','diagnostics','export','import','reset','clearCache','update']:
    assert action in emitted, f'critical emitted action missing: {action}'

# Persistence / sport-specific layout guards.
assert "x.addEventListener('input',save)" in ui, 'numeric/color live saving missing'
assert "function preview(f){state=commitNow();" in ui, 'preview must commit settings first'
assert 'function resetLayout(family)' in ui and "emit('save',{settings:state})" in ui, 'layout reset save missing'
assert 'function switchLayoutSport(id)' in ui, 'per-sport layout switch missing'
assert 'state.sportLayouts[layoutSportId]=readLayoutProfile' in ui, 'per-sport layout persistence missing'

# Known interaction hazard: preview must not disable unrelated .previewBtn controls indefinitely.
if "document.querySelectorAll('.previewBtn').forEach(b=>b.disabled=true)" in ui:
    raise AssertionError('preview() disables every .previewBtn (also Load teams / Recommended / Diagnostics) with no guaranteed re-enable')

print(json.dumps({
  'version': re.search(r'APP_VERSION\s*=\s*"([^"]+)"',src).group(1),
  'screens': len(screens),
  'html_ids': len(ids),
  'onclick_handlers': len(onclick),
  'onclick_functions': sorted(set(onclick)),
  'emitted_actions': sorted(emitted),
  'native_to_web_actions': sorted(sent),
  'optional_missing_ids': sorted(refs-set(ids)),
}, ensure_ascii=False, indent=2))
