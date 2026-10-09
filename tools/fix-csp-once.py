from pathlib import Path
import re


def must_replace(text, old, new, label):
    if old not in text:
        raise RuntimeError(f"Missing expected pattern: {label}")
    return text.replace(old, new)


p = Path("index.html")
html = p.read_text(encoding="utf-8")
html = must_replace(
    html,
    '<button class="filter-summary-clear" type="button" onclick="clearCommunityFilters(event)"></button>',
    '<button class="filter-summary-clear" type="button" data-community-clear></button>',
    "clear-filter onclick",
)
html = must_replace(
    html,
    ' placeholder="Hledat projekty…" oninput="setCommunitySearch(this.value)">',
    ' placeholder="Hledat projekty…">',
    "search oninput",
)
html = html.replace("index-page.js?v=20261009-csp1", "index-page.js?v=20261009-csp2")
p.write_text(html, encoding="utf-8")

p = Path("assets/js/index-page.js")
js = p.read_text(encoding="utf-8")

anchor = "    const appTr=(cs,en)=>lang==='cs'?cs:en;\n"
escape_helpers = "    const escapeAttr=value=>String(value??'').replace(/&/g,'&amp;').replace(/\\\"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');\n"
if "const escapeAttr=value=>" not in js:
    js = must_replace(js, anchor, anchor + escape_helpers, "escape helper anchor")

card_pattern = re.compile(r"    function cardHtml\(app,index,external\)\{.*?\}\n\n    function categoryLabel", re.S)
card_replacement = r'''    function cardHtml(app,index,external){const rawFeatures=(app.features&&app.features[lang])||app.features?.en||app.features?.cs||[];const visibleFeatures=external?researchedFeatures(app,rawFeatures):rawFeatures;const features=visibleFeatures.length?`<ul class="features">${visibleFeatures.map(x=>`<li title="${escapeAttr(x)}">${x}</li>`).join('')}</ul>`:'';const tags=app.tags.map(x=>`<span class="tag">${x}</span>`).join('');const statusId=(external?'externalStatus':'ourStatus')+index;const imgClass=external?'':' ourPreview';const badge=external?`<div class="externalBadge">${tr('Jiný vývojář','Third-party')}</div>`:`<div class="version">v${app.version}</div>`;const author=external?`<div class="authorStatusRow"><div class="author">${tr('Autor','Author')}: ${app.author}</div>`:'';const availability=external?communityStatusBadge(app)+`</div>`:'';let actions='';let actionClass=external?'':'ourActions';if(external){if(Array.isArray(app.variants)&&app.variants.length){actionClass='variantActions';const variantButtons=app.variants.map(v=>`<button class="btn primary" type="button" data-install-remote data-file="${escapeAttr(v.file)}" data-filename="${escapeAttr(v.filename||app.filename)}" data-name="${escapeAttr(app.name+' · '+(v.label||''))}" data-status-id="${escapeAttr(statusId)}">📲 ${v.label||tr('Varianta','Variant')}</button>`).join('');actions=`${variantButtons}<a class="btn secondary variantProject" href="${app.source}" target="_blank" rel="noopener">${tr('↗ Projekt','↗ Project')}</a>`}else{actions=`<button class="btn primary" type="button" data-install-remote data-file="${escapeAttr(app.file)}" data-filename="${escapeAttr(app.filename)}" data-name="${escapeAttr(app.name)}" data-status-id="${escapeAttr(statusId)}">${tr('📲 Instalovat','📲 Install')}</button><a class="btn secondary" href="${app.source}" target="_blank" rel="noopener">${tr('↗ Projekt','↗ Project')}</a>`}}else{actions=`<a class="btn primary" href="${app.install}" download>${tr('📲 Instalovat','📲 Install')}</a>`}return `<article class="card"><div class="preview${imgClass}"><img src="${app.preview}" alt="${escapeAttr(app.name)} preview" loading="lazy">${badge}</div><div class="body"><div class="titleRow"><div class="appIcon">${app.icon}</div><div class="appTitle"><h3 title="${escapeAttr(app.name)}">${app.name}</h3><p>${app.description?.[lang]||app.description?.en||app.description?.cs||''}</p>${author}${availability}</div></div><div class="tags">${tags}</div>${features}<div class="actions ${actionClass}">${actions}</div><div id="${statusId}" class="status"></div></div></article>`}

    function categoryLabel'''
js, n = card_pattern.subn(card_replacement, js, count=1)
if n != 1:
    raise RuntimeError(f"cardHtml replacement count was {n}")

filter_pattern = re.compile(r"    function communityFilterButton\(label,value,active,handler\)\{.*?\}\n")
filter_replacement = '''    function communityFilterButton(label,value,active,handler){return `<button class="filter ${active?'active':''}" type="button" aria-pressed="${active}" data-community-filter="${handler}" data-filter-value="${escapeAttr(value)}">${label}</button>`}
'''
js, n = filter_pattern.subn(filter_replacement, js, count=1)
if n != 1:
    raise RuntimeError(f"communityFilterButton replacement count was {n}")

pagination_pattern = re.compile(r"    function renderPagination\(\)\{.*?\}\n    function renderCommunity", re.S)
pagination_replacement = r'''    function renderPagination(){const rows=filteredCommunityApps();const pages=Math.max(1,Math.ceil(rows.length/PAGE_SIZE));if(communityPage>=pages)communityPage=pages-1;let html=`<button class="pageBtn" ${communityPage===0?'disabled':''} data-community-page="${communityPage-1}" aria-label="${tr('Předchozí stránka','Previous page')}">‹</button>`;for(let i=0;i<pages;i++)html+=`<button class="pageBtn ${i===communityPage?'active':''}" data-community-page="${i}" ${i===communityPage?'aria-current="page"':''}>${i+1}</button>`;html+=`<button class="pageBtn" ${communityPage===pages-1?'disabled':''} data-community-page="${communityPage+1}" aria-label="${tr('Další stránka','Next page')}">›</button>`;const info=rows.length?tr(`Stránka ${communityPage+1} z ${pages} · ${rows.length} vybraných`,`Page ${communityPage+1} of ${pages} · ${rows.length} selected`):tr('Žádné výsledky','No results');for(const id of ['pagination','paginationBottom'])document.getElementById(id).innerHTML=html;for(const id of ['pageInfo','pageInfoBottom'])document.getElementById(id).textContent=info;const currentPageCards=Math.max(0,Math.min(PAGE_SIZE,rows.length-communityPage*PAGE_SIZE));const bottom=document.getElementById('paginationBottom').closest('.catalogBottom');if(bottom)bottom.style.display=currentPageCards>=4?'':'none'}
    function renderCommunity'''
js, n = pagination_pattern.subn(pagination_replacement, js, count=1)
if n != 1:
    raise RuntimeError(f"renderPagination replacement count was {n}")

listener_anchor = "    document.querySelectorAll('[data-language]').forEach(btn=>btn.addEventListener('click',()=>setLanguage(btn.dataset.language)));\n"
delegated = '''    const communityFilterHandlers={setAvailabilityFilter,setCategory,setCommunitySort};
    document.querySelector('[data-community-clear]')?.addEventListener('click',clearCommunityFilters);
    document.getElementById('sourceSearch')?.addEventListener('input',event=>setCommunitySearch(event.currentTarget.value));
    document.addEventListener('click',event=>{const target=event.target instanceof Element?event.target:null;if(!target)return;const install=target.closest('[data-install-remote]');if(install){installRemote(install.dataset.file||'',install.dataset.filename||'',install.dataset.name||'',install.dataset.statusId||'');return}const filter=target.closest('[data-community-filter]');if(filter){const handler=communityFilterHandlers[filter.dataset.communityFilter];if(handler)handler(filter.dataset.filterValue||'all');return}const pageButton=target.closest('[data-community-page]');if(pageButton&&!pageButton.disabled){const page=Number.parseInt(pageButton.dataset.communityPage||'',10);if(Number.isFinite(page))setCommunityPage(page)}});
    document.addEventListener('error',event=>{const image=event.target;if(image instanceof HTMLImageElement&&image.closest('.preview'))image.style.display='none'},true);
'''
if "const communityFilterHandlers={" not in js:
    js = must_replace(js, listener_anchor, delegated + listener_anchor, "delegated listener anchor")

p.write_text(js, encoding="utf-8")

audit = '''const fs=require('fs');
const path=require('path');

const files=[];
for(const name of fs.readdirSync('.')){
  if(/\\.(?:html|js)$/i.test(name)&&fs.statSync(name).isFile())files.push(name);
}
if(fs.existsSync('assets/js')){
  for(const name of fs.readdirSync('assets/js')){
    if(/\\.js$/i.test(name))files.push(path.join('assets/js',name));
  }
}

const issues=[];
const inlineHandler=/<[^>]*\\son[a-z]+\\s*=\\s*["']/gi;
const javascriptUrl=/(?:href|src)\\s*=\\s*["']\\s*javascript:/gi;

for(const file of files){
  const text=fs.readFileSync(file,'utf8');
  for(const match of text.matchAll(inlineHandler))issues.push(`${file}: inline event handler: ${match[0].slice(0,120)}`);
  for(const match of text.matchAll(javascriptUrl))issues.push(`${file}: javascript: URL: ${match[0]}`);

  if(/\\.html$/i.test(file)&&/Content-Security-Policy/i.test(text)){
    if(/script-src[^;]*'unsafe-inline'/i.test(text))issues.push(`${file}: script-src must not contain unsafe-inline`);
    const inlineScripts=[...text.matchAll(/<script(?![^>]*\\bsrc\\s*=)[^>]*>([\\s\\S]*?)<\\/script>/gi)].filter(m=>m[1].trim());
    if(inlineScripts.length)issues.push(`${file}: ${inlineScripts.length} inline <script> block(s) blocked by CSP`);
  }
}

if(issues.length){
  console.error('Web CSP audit failed:');
  for(const issue of issues)console.error(`- ${issue}`);
  process.exit(1);
}
console.log(`Web CSP audit: OK (${files.length} website source files checked; no inline handlers/javascript URLs/blocked inline scripts).`);
'''
Path("tools/audit-web-csp.cjs").write_text(audit, encoding="utf-8")

p = Path(".github/workflows/pages.yml")
pages = p.read_text(encoding="utf-8")
audit_step = "      - name: Audit CSP-safe website interactions\n        run: node tools/audit-web-csp.cjs\n\n"
anchor_pages = "      - name: Generate Credits from catalog\n        run: node tools/build-credits.cjs\n\n"
if audit_step not in pages:
    pages = must_replace(pages, anchor_pages, audit_step + anchor_pages, "Pages audit insertion")
p.write_text(pages, encoding="utf-8")
