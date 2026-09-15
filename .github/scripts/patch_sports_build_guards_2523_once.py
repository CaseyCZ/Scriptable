from pathlib import Path
p=Path('.github/workflows/build-sports-info-package.yml')
s=p.read_text(encoding='utf-8')
needle="""          assert 'function setTableAuto()' in src and 'function markTableManual()' in src, 'AUTO/MANUAL UI switching missing'\n          assert \"state.tableAutoBySport[layoutSportId]=!!auto\" in src, 'AUTO/MANUAL state not scoped to sport'\n          assert 'id=\"tableModeBadge\"' in src and 'id=\"autoTableInfo\"' in src, 'AUTO/MANUAL status UI missing'\n          assert 'resetLayoutSection' in src, 'focused Large reset missing'\n"""
replacement="""          assert 'function setTableAuto()' in src and 'function markTableManual()' in src, 'AUTO/MANUAL UI switching missing'\n          assert \"state.tableAutoBySport[layoutSportId]=!!auto\" in src, 'AUTO/MANUAL state not scoped to sport'\n          assert 'id=\"tableModeBadge\"' in src and 'id=\"autoTableInfo\"' in src, 'AUTO/MANUAL status UI missing'\n          assert \"!['left','center','right'].includes(L.tableAlign)\" in src, 'left/center/right table alignment normalization missing'\n          assert '[[\"left\",lt(s,\"left\")],[\"center\",lt(s,\"center\")],[\"right\",lt(s,\"right\")]]' in src, 'left/center/right table alignment UI missing'\n          assert \"document.querySelectorAll('#layoutLargeTable input[type=number]')\" in src, 'alignment change incorrectly forces MANUAL mode'\n          assert 'let slack=target-(teamWidth+4+statsWidth)' in src and 'while(slack>0)' in src, 'AUTO layout does not fill available table width'\n          assert 'teamMin=96,teamMax=150' in src, 'AUTO team width bounds missing'\n          assert 'resetLayoutSection' in src, 'focused Large reset missing'\n"""
if needle not in s: raise SystemExit('AUTO guard block not found')
s=s.replace(needle,replacement,1)
needle2="""          assert 'https://raw.githubusercontent.com/CaseyCZ/Scriptable/Master/apps/Sports-Info/Sports%20Info.js' in src, 'updater is not pinned to Master'\n"""
replacement2=needle2+"""          assert 'if(config.runsInWidget)' in src, 'Home Screen widget execution branch missing'\n          assert 'const target=module.filename' in src, 'in-place updater script identity contract missing'\n"""
if needle2 not in s: raise SystemExit('identity guard marker not found')
s=s.replace(needle2,replacement2,1)
p.write_text(s,encoding='utf-8')
print('updated Sports Info 2.5.23 permanent guards')
