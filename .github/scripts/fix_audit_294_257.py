from pathlib import Path
import json
import re

# LockScreen Generator 2.9.4
lock_path = Path('apps/LockScreenGenerator/LockScreenGenerator.js')
lock = lock_path.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.9.3";' in lock
lock = lock.replace('const APP_VERSION = "2.9.3";', 'const APP_VERSION = "2.9.4";', 1)
assert 'async function fetchCrypto(value)' in lock
lock = lock.replace('async function fetchCrypto(value)', 'async function fetchCrypto(settings,value)', 1)
assert 'fetchCrypto(settings.cryptoCoins)' in lock
lock = lock.replace('fetchCrypto(settings.cryptoCoins)', 'fetchCrypto(settings,settings.cryptoCoins)', 1)
lock_path.write_text(lock, encoding='utf-8')

# Sports Info 2.5.7
sports_path = Path('apps/Sports-Info/Sports Info.js')
sports = sports_path.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.5.6";' in sports
sports = sports.replace('const APP_VERSION = "2.5.6";', 'const APP_VERSION = "2.5.7";', 1)
sports = re.sub(r'// Sports Info v[^\n]+', '// Sports Info v2.5.7', sports, count=1)

bad1 = 'points:String(x.points??x.pts??x.wins??"")'
bad2 = 'points:String(x.points??x.wins??"")'
assert bad1 in sports
assert bad2 in sports
sports = sports.replace(bad1, 'points:String(x.points??x.pts??"")', 1)
sports = sports.replace(bad2, 'points:String(x.points??"")', 1)

old_result = 'function result(e,s){if(!(s.teamId||s.teamName)||!e.completed)return"";const h=Number(e.home.score),a=Number(e.away.score);if(Number.isNaN(h)||Number.isNaN(a))return"";const home=teamMatches(e.home,s),me=home?h:a,op=home?a:h;return me>op?"W":me<op?"L":"D"}'
new_result = 'function result(e,s){if(!(s.teamId||s.teamName)||!e.completed)return"";const h=Number(e.home.score),a=Number(e.away.score);if(Number.isNaN(h)||Number.isNaN(a))return"";const home=teamMatches(e.home,s),me=home?h:a,op=home?a:h;if(me>op)return"W";if(me<op){if(s.sportId==="hockey"&&/OT|SO|overtime|shootout|prodlou|nájezd/i.test(String(e.status||"")))return"OTL";return"L"}return["football","floorball"].includes(s.sportId)?"D":""}'
assert old_result in sports
sports = sports.replace(old_result, new_result, 1)
sports_path.write_text(sports, encoding='utf-8')

# Build synchronized public packages/surfaces.
exec(compile(Path('.github/scripts/build_scriptable_package.py').read_text(encoding='utf-8'), 'build_scriptable_package.py', 'exec'))
exec(compile(Path('.github/scripts/build_sports_info_package.py').read_text(encoding='utf-8'), 'build_sports_info_package.py', 'exec'))

# Release invariants.
lock = lock_path.read_text(encoding='utf-8')
sports = sports_path.read_text(encoding='utf-8')
lock_pkg = json.loads(Path('apps/LockScreenGenerator/LockScreenGenerator.scriptable').read_text(encoding='utf-8'))
sports_pkg = json.loads(Path('apps/Sports-Info/Sports Info.scriptable').read_text(encoding='utf-8'))
assert lock_pkg['script'] == lock
assert sports_pkg['script'] == sports
assert 'repr(' not in lock
assert 'falsewindow.__updateReady' not in lock
assert 'JSON.stringify(PHONE_TEXT.loading)' not in lock
assert 'async function fetchCrypto(settings,value)' in lock
assert 'fetchCrypto(settings,settings.cryptoCoins)' in lock
assert bad1 not in sports and bad2 not in sports
assert 'return"OTL"' in sports

root = Path('README.md').read_text(encoding='utf-8')
site = Path('index.html').read_text(encoding='utf-8')
assert '| 🪄 **LockScreen Generator** | ✅ v2.9.4 |' in root
assert '| 🏆 **Sports Info** | ✅ v2.5.7 |' in root
assert "{name:'LockScreen Generator',version:'2.9.4'" in site
assert "{name:'Sports Info',version:'2.5.7'" in site
print('Audit fixes prepared and release surfaces synchronized')
