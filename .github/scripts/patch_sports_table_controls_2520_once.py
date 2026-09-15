from pathlib import Path

app = Path('apps/Sports-Info/Sports Info.js')
s = app.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.5.19";' in s

s = s.replace('// Sports Info v2.5.19', '// Sports Info v2.5.20', 1)
s = s.replace('const APP_VERSION = "2.5.19";', 'const APP_VERSION = "2.5.20";', 1)

# The TEAM width must really control where the first stat column starts.
assert 'tableTeamWidth:[82,135]' in s
s = s.replace('tableTeamWidth:[82,135]', 'tableTeamWidth:[60,180]', 1)
assert 'tableNarrowWidth:[18,32]' in s
s = s.replace('tableNarrowWidth:[18,32]', 'tableNarrowWidth:[20,50]', 1)

# Make the setting wording explicit: TEAM width also defines the first-stat start position.
texts = {
    'tableTeamWidth:"Šířka sloupce TÝM"': 'tableTeamWidth:"Šířka TÝM / začátek statistik"',
    'tableTeamWidth:"TEAM column width"': 'tableTeamWidth:"TEAM width / stats start"',
    'tableTeamWidth:"TEAM-Spalte"': 'tableTeamWidth:"TEAM-Breite / Statistikstart"',
    'tableTeamWidth:"Ancho EQUIPO"': 'tableTeamWidth:"Ancho EQUIPO / inicio estadísticas"',
    'tableTeamWidth:"Určuje šířku levého sloupce TÝM v tabulce."': 'tableTeamWidth:"Určuje šířku levého sloupce TÝM a tím i místo, kde začíná první statistika Z."',
    'tableTeamWidth:"Sets the width of the left TEAM column in standings."': 'tableTeamWidth:"Sets the TEAM width and therefore where the first statistics column starts."',
    'tableTeamWidth:"Legt die Breite der linken TEAM-Spalte fest."': 'tableTeamWidth:"Legt die TEAM-Breite und damit den Start der ersten Statistikspalte fest."',
    'tableTeamWidth:"Define el ancho de la columna EQUIPO en la tabla."': 'tableTeamWidth:"Define el ancho de EQUIPO y dónde empieza la primera columna estadística."'
}
for old, new in texts.items():
    assert old in s, old
    s = s.replace(old, new, 1)

# Settings UI ranges.
old = 'layoutField(s,"layoutLargeTableTeamWidth",lt(s,"tableTeamWidth"),s.layout.large.tableTeamWidth,82,135,"tableTeamWidth")'
new = 'layoutField(s,"layoutLargeTableTeamWidth",lt(s,"tableTeamWidth"),s.layout.large.tableTeamWidth,60,180,"tableTeamWidth")'
assert old in s
s = s.replace(old, new, 1)
old = 'layoutField(s,"layoutLargeTableNarrowWidth",lt(s,"narrowWidth"),s.layout.large.tableNarrowWidth,18,32,"narrowWidth")'
new = 'layoutField(s,"layoutLargeTableNarrowWidth",lt(s,"narrowWidth"),s.layout.large.tableNarrowWidth,20,50,"narrowWidth")'
assert old in s
s = s.replace(old, new, 1)

# Remove flexible right-anchoring. A small fixed gap keeps TEAM and Z separated,
# while tableTeamWidth now directly moves the first statistics column.
old = '  h.addSpacer();\n  const hs=h.addStack();hs.layoutHorizontally();hs.size=new Size(statsWidth,0);'
new = '  h.addSpacer(4);\n  const hs=h.addStack();hs.layoutHorizontally();hs.size=new Size(statsWidth,0);'
assert old in s
s = s.replace(old, new, 1)
old = '    r.addSpacer();\n    const rs=r.addStack();rs.layoutHorizontally();rs.size=new Size(statsWidth,0);'
new = '    r.addSpacer(4);\n    const rs=r.addStack();rs.layoutHorizontally();rs.size=new Size(statsWidth,0);'
assert old in s
s = s.replace(old, new, 1)

# Reset must update the selected sport/family immediately and save exactly that profile.
old = "function resetLayout(family){state=collect();state.sportLayouts=state.sportLayouts||{};const profile=cloneProfile(state.sportLayouts[layoutSportId]||LAYOUT_DEFAULTS);profile[family]=cloneProfile(LAYOUT_DEFAULTS)[family];state.sportLayouts[layoutSportId]=profile;state.layout=cloneProfile(profile);writeLayoutProfile(profile);commitNow()}"
new = "function resetLayout(family){clearTimeout(timer);const current=collect(),sid=layoutSportId||current.sportId;current.sportLayouts=current.sportLayouts||{};const profile=cloneProfile(current.sportLayouts[sid]||LAYOUT_DEFAULTS);profile[family]=cloneProfile(LAYOUT_DEFAULTS)[family];current.sportLayouts[sid]=profile;if(current.sportId===sid)current.layout=cloneProfile(profile);state=current;writeLayoutProfile(profile);emit('save',{settings:state})}"
assert old in s
s = s.replace(old, new, 1)

app.write_text(s, encoding='utf-8')

# Strengthen the permanent release guard so these controls cannot silently regress.
wf = Path('.github/workflows/build-sports-info-package.yml')
w = wf.read_text(encoding='utf-8')
needle = "          assert 'tableWideWidth:30' in src and 'tableNarrowWidth:23' in src, 'wide/narrow standings widths missing'\n"
assert needle in w
extra = needle + "          assert 'tableTeamWidth:[60,180]' in src, 'TEAM/start-position range regressed'\n          assert 'tableNarrowWidth:[20,50]' in src, 'last-three-stat range regressed'\n          assert 'layoutLargeTableTeamWidth\",lt(s,\"tableTeamWidth\"),s.layout.large.tableTeamWidth,60,180' in src, 'TEAM/start-position UI range regressed'\n          assert 'layoutLargeTableNarrowWidth\",lt(s,\"narrowWidth\"),s.layout.large.tableNarrowWidth,20,50' in src, 'last-three-stat UI range regressed'\n          assert 'h.addSpacer(4);\\n  const hs=h.addStack()' in src, 'standings header first-stat gap is not fixed'\n          assert 'r.addSpacer(4);\\n    const rs=r.addStack()' in src, 'standings row first-stat gap is not fixed'\n"
w = w.replace(needle, extra, 1)
needle2 = "          assert 'profile[family]=cloneProfile(LAYOUT_DEFAULTS)[family]' in src, 'Layout reset is not scoped to current sport/family'\n"
assert needle2 in w
extra2 = needle2 + "          assert \"writeLayoutProfile(profile);emit('save',{settings:state})\" in src, 'Layout reset does not immediately save restored defaults'\n"
w = w.replace(needle2, extra2, 1)
wf.write_text(w, encoding='utf-8')
