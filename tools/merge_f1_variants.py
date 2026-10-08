#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
extra_path=ROOT/'community-extra.js'
index_path=ROOT/'index.html'

extra=extra_path.read_text(encoding='utf-8')
old_pattern=re.compile(r'communityItem\("F1 Widget Open F1"[^\n]*\),\ncommunityItem\("F1 Widget Official F1"[^\n]*\),')
replacement='''Object.assign(communityItem("F1 Scriptable Widget","sport","archive-sh","🏎️","https://raw.githubusercontent.com/archive-sh/F1-Scriptable-Widget/main/F1%20Widget%20OfficialF1.js","F1 Widget OfficialF1.js","https://github.com/archive-sh/F1-Scriptable-Widget","https://opengraph.githubassets.com/1/archive-sh/F1-Scriptable-Widget",["Sport","Formula 1","Live timing"],"Formula 1 widget se dvěma variantami živých dat: Official F1 a OpenF1.","Formula 1 widget with two live-data variants: Official F1 and OpenF1."),{variants:[{label:"Official F1",file:"https://raw.githubusercontent.com/archive-sh/F1-Scriptable-Widget/main/F1%20Widget%20OfficialF1.js",filename:"F1 Widget OfficialF1.js"},{label:"OpenF1",file:"https://raw.githubusercontent.com/archive-sh/F1-Scriptable-Widget/main/F1%20Widget%20OpenF1.js",filename:"F1 Widget OpenF1.js"}]}),'''
extra,new_count=old_pattern.subn(replacement,extra,count=1)
if new_count!=1:
    raise SystemExit(f'Expected to merge exactly one F1 pair, changed {new_count}')
extra_path.write_text(extra,encoding='utf-8')

index=index_path.read_text(encoding='utf-8')
old_status="    function communityStatusFor(app){return communityStatus?.items?.[app.file]||null}"
new_status="""    function communityStatusFor(app){const urls=[app.file,...(app.variants||[]).map(v=>v.file)].filter(Boolean);const states=urls.map(url=>communityStatus?.items?.[url]).filter(Boolean);if(!states.length)return null;if(states.some(item=>item?.online===true))return {online:true,checkedAt:states.find(item=>item?.checkedAt)?.checkedAt||null};if(states.every(item=>item?.checkedAt))return {online:false,checkedAt:states[0]?.checkedAt||null};return states[0]||null}"""
if old_status not in index:
    raise SystemExit('communityStatusFor marker not found')
index=index.replace(old_status,new_status,1)

old_guard="for(const app of (window.communityExtraApps||[])){const url=canonicalCommunityUrl(app.file),nameKey=normalizedCommunityIdentity(app);if((url&&communitySeenUrls.has(url))||(nameKey!=='|'&&communitySeenNames.has(nameKey)))continue;if(url)communitySeenUrls.add(url);if(nameKey!=='|')communitySeenNames.add(nameKey);communityApps.push(app)}"
new_guard="for(const app of (window.communityExtraApps||[])){const urls=[app.file,...(app.variants||[]).map(v=>v.file)].map(canonicalCommunityUrl).filter(Boolean),nameKey=normalizedCommunityIdentity(app);if(urls.some(url=>communitySeenUrls.has(url))||(nameKey!=='|'&&communitySeenNames.has(nameKey)))continue;urls.forEach(url=>communitySeenUrls.add(url));if(nameKey!=='|')communitySeenNames.add(nameKey);communityApps.push(app)}"
if old_guard not in index:
    raise SystemExit('runtime duplicate guard marker not found')
index=index.replace(old_guard,new_guard,1)

card_pattern=re.compile(r'    function cardHtml\(app,index,external\)\{.*?\n\n    function categoryLabel',re.S)
new_card=r'''    function cardHtml(app,index,external){const rawFeatures=(app.features&&app.features[lang])||app.features?.en||app.features?.cs||[];const visibleFeatures=external?researchedFeatures(app,rawFeatures):rawFeatures;const features=visibleFeatures.length?`<ul class="features">${visibleFeatures.map(x=>`<li title="${String(x).replace(/"/g,'&quot;')}">${x}</li>`).join('')}</ul>`:'';const tags=app.tags.map(x=>`<span class="tag">${x}</span>`).join('');const statusId=(external?'externalStatus':'ourStatus')+index;const imgClass=external?'':' ourPreview';const badge=external?`<div class="externalBadge">${tr('Jiný vývojář','Third-party')}</div>`:`<div class="version">v${app.version}</div>`;const author=external?`<div class="authorStatusRow"><div class="author">${tr('Autor','Author')}: ${app.author}</div>`:'';const availability=external?communityStatusBadge(app)+`</div>`:'';let actions='';let actionClass=external?'':'ourActions';if(external){if(Array.isArray(app.variants)&&app.variants.length){actionClass='variantActions';const variantButtons=app.variants.map(v=>`<button class="btn primary" type="button" onclick='installRemote(${JSON.stringify(v.file)},${JSON.stringify(v.filename||app.filename)},${JSON.stringify(app.name+' · '+(v.label||''))},${JSON.stringify(statusId)})'>📲 ${v.label||tr('Varianta','Variant')}</button>`).join('');actions=`${variantButtons}<a class="btn secondary variantProject" href="${app.source}" target="_blank" rel="noopener">${tr('↗ Projekt','↗ Project')}</a>`}else{actions=`<button class="btn primary" type="button" onclick='installRemote(${JSON.stringify(app.file)},${JSON.stringify(app.filename)},${JSON.stringify(app.name)},${JSON.stringify(statusId)})'>${tr('📲 Instalovat','📲 Install')}</button><a class="btn secondary" href="${app.source}" target="_blank" rel="noopener">${tr('↗ Projekt','↗ Project')}</a>`}}else{actions=`<a class="btn primary" href="${app.install}" download>${tr('📲 Instalovat','📲 Install')}</a>`}return `<article class="card"><div class="preview${imgClass}"><img src="${app.preview}" alt="${app.name} preview" loading="lazy" onerror="this.style.display='none'">${badge}</div><div class="body"><div class="titleRow"><div class="appIcon">${app.icon}</div><div class="appTitle"><h3 title="${app.name}">${app.name}</h3><p>${app.description?.[lang]||app.description?.en||app.description?.cs||''}</p>${author}${availability}</div></div><div class="tags">${tags}</div>${features}<div class="actions ${actionClass}">${actions}</div><div id="${statusId}" class="status"></div></div></article>`}

    function categoryLabel'''
index,new_card_count=card_pattern.subn(new_card,index,count=1)
if new_card_count!=1:
    raise SystemExit(f'cardHtml replacement count {new_card_count}')

css_marker='/* community-variant-actions */'
if css_marker not in index:
    css='''\n    /* community-variant-actions */\n    .actions.variantActions{grid-template-columns:repeat(2,minmax(0,1fr))}.actions.variantActions .variantProject{grid-column:1/-1}\n    @media(max-width:660px){.actions.variantActions{grid-template-columns:1fr}.actions.variantActions .variantProject{grid-column:auto}}\n'''
    index=index.replace('</style>',css+'  </style>',1)

index_path.write_text(index,encoding='utf-8')
print('Merged F1 variants and updated catalog renderer.')
