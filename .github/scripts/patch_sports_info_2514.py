from pathlib import Path

p = Path('apps/Sports-Info/Sports Info.js')
s = p.read_text(encoding='utf-8')

assert 'const APP_VERSION = "2.5.13";' in s
s = s.replace('const APP_VERSION = "2.5.13";', 'const APP_VERSION = "2.5.14";', 1)
s = s.replace('// Sports Info v2.5.13', '// Sports Info v2.5.14', 1)

old_state = '''function state(s,e){if(e.state==="in")return `${tx(s,"liveNow")} · ${e.status||""}`;if(e.completed||e.state==="post")return e.status||day(s,e.date);return `${day(s,e.date)} · ${time(s,e.date)}`}'''
new_state = '''function state(s,e){const when=`${day(s,e.date)} · ${time(s,e.date)}`;if(e.state==="in")return `${when} · ${tx(s,"liveNow")}${e.status?` · ${e.status}`:""}`;if(e.completed||e.state==="post")return `${when}${e.status?` · ${e.status}`:""}`;return when}'''
assert old_state in s, 'state() block not found'
s = s.replace(old_state, new_state, 1)

old_else = '''  }else{
    await teamCell(r,e.home,s,p,family,true,128);
    const mid=r.addStack();mid.layoutHorizontally();mid.centerAlignContent();mid.size=new Size(36,0);mid.addSpacer();
    const sc=txt(mid,score(e),20,p.text,true);sc.centerAlignText();mid.addSpacer();
    await teamCell(r,e.away,s,p,family,false,128)
  }'''
new_else = '''  }else{
    const scoreText=score(e),scoreW=clamp(tableTextWidth(scoreText,20,true),38,58),rowW=284,teamW=Math.floor((rowW-scoreW)/2);
    await teamCell(r,e.home,s,p,family,true,teamW);
    const mid=r.addStack();mid.layoutHorizontally();mid.centerAlignContent();mid.size=new Size(scoreW,0);mid.addSpacer();
    const sc=txt(mid,scoreText,20,p.text,true);sc.centerAlignText();sc.minimumScaleFactor=1;mid.addSpacer();
    await teamCell(r,e.away,s,p,family,false,teamW)
  }'''
assert old_else in s, 'matchCard large/medium block not found'
s = s.replace(old_else, new_else, 1)

p.write_text(s, encoding='utf-8')
print('Patched Sports Info to 2.5.14 with consistent date/time and dynamic score width')
