from pathlib import Path

p = Path('apps/Sports-Live/Sports-Live,js')
s = p.read_text(encoding='utf-8')

old = 'logo:x.team?.logo||"",score:x.score==null?"":String(x.score)'
new = 'logo:x.team?.logos?.[0]?.href||x.team?.logo||"",score:x.score==null?"":String(x.score)'

if old not in s:
    raise SystemExit('ESPN team logo mapping not found')

s = s.replace(old, new, 1)
s = s.replace('// Sports Live v0.2.4', '// Sports Live v0.2.5', 1)
s = s.replace('const APP_VERSION = "0.2.4";', 'const APP_VERSION = "0.2.5";', 1)

p.write_text(s, encoding='utf-8')
