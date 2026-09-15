from pathlib import Path

app = Path('apps/Sports-Info/Sports Info.js')
s = app.read_text(encoding='utf-8')
assert 'const APP_VERSION = "2.5.20";' in s

s = s.replace('// Sports Info v2.5.20', '// Sports Info v2.5.21', 1)
s = s.replace('const APP_VERSION = "2.5.20";', 'const APP_VERSION = "2.5.21";', 1)

old = '''async function logo(url,key){if(!url)return null;const p=fm.joinPath(fm.cacheDirectory(),`SportsInfo_${String(key).replace(/[^a-zA-Z0-9_-]/g,"_")}.png`);try{if(fm.fileExists(p))return fm.readImage(p);const r=new Request(url);r.timeoutInterval=API_TIMEOUT;const i=await r.loadImage();fm.writeImage(p,i);return i}catch(_){try{return fm.fileExists(p)?fm.readImage(p):null}catch(__){return null}}}'''
new = '''function logoCachePath(url,key){const safe=(String(key||"logo").replace(/[^a-zA-Z0-9_-]/g,"_").slice(0,48)||"logo");let h=2166136261,raw=String(url||"");for(let i=0;i<raw.length;i++){h^=raw.charCodeAt(i);h=Math.imul(h,16777619)}return fm.joinPath(fm.cacheDirectory(),`SportsInfo_${safe}_${(h>>>0).toString(36)}.png`)}
async function logo(url,key){if(!url)return null;const p=logoCachePath(url,key);try{if(fm.fileExists(p)){try{return fm.readImage(p)}catch(_){try{fm.remove(p)}catch(__){}}}const r=new Request(url);r.timeoutInterval=API_TIMEOUT;const i=await r.loadImage();fm.writeImage(p,i);return i}catch(_){return null}}'''
assert old in s, 'old logo cache implementation not found'
s = s.replace(old, new, 1)

app.write_text(s, encoding='utf-8')
