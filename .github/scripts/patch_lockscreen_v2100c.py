import runpy
from pathlib import Path

runpy.run_path('.github/scripts/patch_lockscreen_v2100b.py', run_name='__main__')

p = Path('apps/LockScreenGenerator/LockScreenGenerator.js')
s = p.read_text(encoding='utf-8')
replacements = {
    '${settings.wallpaperSource===\\"generator\\"?\\"selected\\":\\"\\"}': '${settings.wallpaperSource==="generator"?"selected":""}',
    '${settings.wallpaperSource!==\\"generator\\"?\\"selected\\":\\"\\"}': '${settings.wallpaperSource!=="generator"?"selected":""}',
}
for old,new in replacements.items():
    if old not in s:
        raise SystemExit(f'missing generated wallpaper expression: {old}')
    s = s.replace(old,new,1)
p.write_text(s, encoding='utf-8')
print('Corrected wallpaper template expressions')
