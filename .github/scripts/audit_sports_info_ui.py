from pathlib import Path
import re, json

src = Path('apps/Sports-Info/Sports Info.js').read_text(encoding='utf-8')
html = Path('/tmp/sports-settings.html').read_text(encoding='utf-8')
script_m = re.search(r'<script>([\s\S]*?)</script>', html)
assert script_m, 'settings <script> missing'
ui = script_m.group(1)

ids = re.findall(r'\bid="([^"]+)"', html)
duplicates = sorted({x for x in ids if ids.count(x) > 1})
assert not duplicates, f'duplicate HTML ids: {duplicates}'
screens = set(re.findall(r'class="screen(?: active)?" id="([^"]+)"', html))
expected = {'home','sport','content','layout','layoutSmall','layoutMedium','layoutLarge','layoutLargeMatch','layoutLargeTable','layoutLargeLists','appearance','api','diagnostics','maintenance'}
assert expected <= screens, f'missing screens: {sorted(expected-screens)}'

onclick = re.findall(r'onclick="\s*([A-Za-z_$][\w$]*)\s*\(', html)
functions = set(re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', ui))
missing_funcs = sorted(set(onclick)-functions)
assert not missing_funcs, f'onclick without function: {missing_funcs}'

targets = set(re.findall(r"showScreen\('([^']+)'\)", html)) | set(re.findall(r"showScreen\('([^']+)'\)", ui))
assert targets <= screens, f'showScreen target missing: {sorted(targets-screens)}'

emitted = set(re.findall(r"emit\(['\"]([A-Za-z0-9_]+)['\"]", ui))
handled_native = set(re.findall(r"m\.action\s*={2,3}\s*['\"]([A-Za-z0-9_]+)['\"]", src))
assert not (emitted-handled_native), f'UI emits actions with no native handler: {sorted(emitted-handled_native)}'

sent = set(re.findall(r"send\(web,\{action:['\"]([A-Za-z0-9_]+)['\"]", src))
handled_web = set(re.findall(r"m\.action\s*={2,3}\s*['\"]([A-Za-z0-9_]+)['\"]", ui))
assert not (sent-handled_web), f'native sends actions with no WebView handler: {sorted(sent-handled_web)}'

refs = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", ui))
optional = {'previewMeta'}
assert not (refs-set(ids)-optional), f'getElementById references missing elements: {sorted(refs-set(ids)-optional)}'

for fn in ['showScreen','commitNow','save','fillLeagues','loadTeams','preview','runDiagnostics','exportJSON','importJSON','resetPart','resetLayout','resetLayoutSection','clearCache','recommendedWidget','requestUpdate','renderDiag','setTableAuto','markTableManual']:
    assert fn in functions, f'critical UI function missing: {fn}'
for action in ['save','teams','preview','diagnostics','export','import','reset','clearCache','update']:
    assert action in emitted, f'critical emitted action missing: {action}'

assert "x.addEventListener('input',save)" in ui, 'numeric/color live saving missing'
assert "function preview(f){state=commitNow();" in ui, 'preview must commit settings first'
assert 'function switchLayoutSport(id)' in ui, 'per-sport layout switch missing'
assert 'state.sportLayouts[layoutSportId]=readLayoutProfile' in ui, 'per-sport layout persistence missing'
assert "document.querySelectorAll('.previewBtn').forEach(b=>b.disabled=true)" not in ui, 'preview disables unrelated buttons'
assert "document.querySelectorAll('.previewAction[data-preview=\"'+f+'\"]')" in ui, 'preview busy state is not scoped by family'
assert "m.action==='previewDone'" in ui, 'preview completion callback missing'
assert "m.action==='autoTableInfo'" in ui, 'AUTO table measurement callback missing'
assert "addEventListener('touchstart'" in ui, 'iPhone pressed-state touch handler missing'
assert "setAttribute('inputmode','numeric')" in ui, 'iPhone numeric keyboard hint missing'
assert 'tableAutoBySport' in ui, 'per-sport AUTO/MANUAL state missing from UI'

print(json.dumps({
  'version': re.search(r'APP_VERSION\s*=\s*"([^"]+)"',src).group(1),
  'screens': len(screens),
  'html_ids': len(ids),
  'onclick_handlers': len(onclick),
  'onclick_functions': sorted(set(onclick)),
  'emitted_actions': sorted(emitted),
  'native_to_web_actions': sorted(sent),
}, ensure_ascii=False, indent=2))
