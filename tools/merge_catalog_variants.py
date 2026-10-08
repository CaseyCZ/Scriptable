#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
index_path=ROOT/'index.html'
extra_path=ROOT/'community-extra.js'

index=index_path.read_text(encoding='utf-8')
extra=extra_path.read_text(encoding='utf-8')

# Match the whole built-in object through its nested features object.
countdown_pattern=re.compile(r"\{name:'MyCountdowns',category:'calendar',author:'rushhiii'.*?features:\{cs:\[[^\]]*\],en:\[[^\]]*\]\}\},", re.S)
countdown_repl="""{name:'Countdown Widget',category:'calendar',author:'rushhiii',icon:'⏳',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Countdown%20Widget/MyCountdowns.js',filename:'MyCountdowns.js',source:'https://github.com/rushhiii/Scriptable-iOSWidgets/tree/main/Widgets/Countdown%20Widget',preview:'https://raw.githubusercontent.com/rushhiii/Scriptable-IOSWidgets/refs/heads/main/.assets/countdown/countdow_showcase.png',tags:['Countdown','Events','Google Sheets / Notion'],description:{cs:'Odpočty událostí ve třech variantách: Classic, v2 a přímá Notion verze.',en:'Event countdowns in three variants: Classic, v2 and direct Notion.'},features:{cs:['Classic přes Google Sheets','v2 s pokročilým workflow','Notion-only varianta','Offline cache a více velikostí'],en:['Classic via Google Sheets','v2 with advanced workflow','Notion-only variant','Offline cache and multiple sizes']},variants:[{label:'Classic',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Countdown%20Widget/MyCountdowns.js',filename:'MyCountdowns.js'},{label:'v2',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Countdown%20Widget/v2/MyCountdowns-v2.js',filename:'MyCountdowns-v2.js'},{label:'Notion',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Countdown%20Widget/v2/NotionCountdowns.js',filename:'NotionCountdowns.js'}]},"""
index,n=countdown_pattern.subn(countdown_repl,index,count=1)
if n!=1: raise SystemExit(f'Countdown built-in replacement count {n}')

quote_pattern=re.compile(r"\{name:'MyQuotes',category:'reading',author:'rushhiii'.*?features:\{cs:\[[^\]]*\],en:\[[^\]]*\]\}\},", re.S)
quote_repl="""{name:'Quote Widget',category:'reading',author:'rushhiii',icon:'💬',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Quote%20Widget/MyQuotes.js',filename:'MyQuotes.js',source:'https://github.com/rushhiii/Scriptable-iOSWidgets/tree/main/Widgets/Quote%20Widget',preview:'https://raw.githubusercontent.com/rushhiii/Scriptable-IOSWidgets/refs/heads/main/.assets/quotes/quote_showcase.png',tags:['Quotes','Google Sheets / Notion','ZenQuotes'],description:{cs:'Jedna rodina quote widgetu: vlastní Google Sheets, Notion nebo lehká ZenQuotes varianta.',en:'One quote-widget family: custom Google Sheets, Notion or lightweight ZenQuotes.'},features:{cs:['MyQuotes z Google Sheets','Přímá Notion varianta','Lehká ZenQuotes varianta','Small / Medium / Large'],en:['MyQuotes from Google Sheets','Direct Notion variant','Lightweight ZenQuotes variant','Small / Medium / Large']},variants:[{label:'MyQuotes',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Quote%20Widget/MyQuotes.js',filename:'MyQuotes.js'},{label:'Notion',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Quote%20Widget/NotionQuotes.js',filename:'NotionQuotes.js'},{label:'ZenQuotes Lite',file:'https://raw.githubusercontent.com/rushhiii/Scriptable-iOSWidgets/main/Widgets/Quote%20Widget/light%20version/quote.js',filename:'quote.js'}]},"""
index,n=quote_pattern.subn(quote_repl,index,count=1)
if n!=1: raise SystemExit(f'Quote built-in replacement count {n}')

for name in ['Countdown Widget','MyCountdowns v2','Notion Countdowns','Notion Quotes','Quote Light']:
    pattern=re.compile(r'^communityItem\("'+re.escape(name)+r'"[^\n]*\),\n?', re.M)
    extra,n=pattern.subn('',extra,count=1)
    if n!=1: raise SystemExit(f'Expected one extra entry for {name}, removed {n}')

blend_pattern=re.compile(r'^communityItem\("blend"[^\n]*\),\ncommunityItem\("blend widget"[^\n]*\),', re.M)
blend_repl='communityItem("Blend Installer","tools","unvsDev","🧰","https://raw.githubusercontent.com/unvsDev/blend/main/installer.js","Blend Installer.js","https://github.com/unvsDev/blend","https://user-images.githubusercontent.com/63099769/187044062-642ccbd5-f01e-4355-9fc5-9ce4155e93e3.jpg",["Tools","Widget builder","Installer"],"Oficiální Blend instalátor, který nainstaluje launcher i samotný widget.","Official Blend installer that installs both the launcher and widget."),'
extra,n=blend_pattern.subn(blend_repl,extra,count=1)
if n!=1: raise SystemExit(f'Blend replacement count {n}')

marker='    const FEATURE_DETAILS={'
if marker not in index: raise SystemExit('FEATURE_DETAILS marker missing')
insert="""    const FEATURE_DETAILS={
      'Countdown Widget':[['Tři oficiální varianty v jedné kartě','Three official variants in one card'],['Classic, v2 a přímé Notion napojení','Classic, v2 and direct Notion integration'],['Vyber instalaci podle požadovaného datového workflow','Choose the install for your preferred data workflow']],
      'Quote Widget':[['Tři varianty stejné quote rodiny','Three variants of the same quote-widget family'],['Google Sheets, Notion nebo ZenQuotes API','Google Sheets, Notion or ZenQuotes API'],['Small / Medium / Large widgety','Small / Medium / Large widgets']],
      'Blend Installer':[['Oficiální instalátor projektu Blend','Official installer for the Blend project'],['Automaticky nainstaluje Blend Widget i Blend launcher','Automatically installs Blend Widget and Blend launcher'],['Konfigurovatelný dashboard s počasím, kalendářem a dalšími prvky','Configurable dashboard with weather, calendar and more']],
"""
index=index.replace(marker,insert,1)

index_path.write_text(index,encoding='utf-8')
extra_path.write_text(extra,encoding='utf-8')
print('Merged Countdown, Quote and Blend project variants.')

# Trigger marker: remove-extra-countdown
