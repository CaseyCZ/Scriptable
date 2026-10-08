from pathlib import Path
import re

p = Path('credits.html')
s = p.read_text()

pattern = re.compile(r"function renderCommunityCredits\(\)\{.*?\}\nasync function loadCredits", re.S)
new = '''function renderCommunityCredits(){if(!creditsData)return;const authors=creditsData.authors||{};document.getElementById('creditsSummary').innerHTML=`<span class="pill">${creditsData.total} ${esc(t('projektů','projects','Projekte','proyectos','projets'))}</span><span class="pill">${creditsData.authorCount} ${esc(t('autorů','authors','Autoren','autores','auteurs'))}</span>`;const groups=Object.entries(authors).sort(([a],[b])=>a.localeCompare(b,undefined,{sensitivity:'base'}));document.getElementById('communityCredits').innerHTML=groups.map(([author,projects])=>{const sorted=[...projects].sort((a,b)=>a.name.localeCompare(b.name,undefined,{sensitivity:'base'}));const links=sorted.map(project=>`<a class="catalog-credit-project" href="${esc(project.source)}" target="_blank" rel="noopener noreferrer" title="${esc(project.name)}">${esc(project.name)}</a>`).join('<span class="catalog-credit-sep">, </span>');return `<span class="catalog-credit-pill" title="${esc(author)}"><span class="catalog-credit-author">${esc(author)}</span><span class="catalog-credit-dot">·</span><span class="catalog-credit-projects">${links}</span></span>`}).join('')}
async function loadCredits'''

s2, n = pattern.subn(new, s, count=1)
if n != 1:
    raise SystemExit(f'renderCommunityCredits replacement count={n}')

if '.catalog-credit-projects{' not in s2:
    s2 = s2.replace(
        '.catalog-credit-project{color:var(--accent);font-weight:900;overflow:hidden;text-overflow:ellipsis}',
        '.catalog-credit-projects{display:inline-flex;align-items:center;gap:0;min-width:0;max-width:100%;overflow:hidden}.catalog-credit-project{color:var(--accent);font-weight:900;overflow:hidden;text-overflow:ellipsis}.catalog-credit-project:hover{text-decoration:underline;text-underline-offset:2px}.catalog-credit-sep{color:var(--muted);flex:0 0 auto}',
        1,
    )

for needle in ['const groups=Object.entries(authors)', 'catalog-credit-projects', 'catalog-credit-sep']:
    if needle not in s2:
        raise SystemExit('missing ' + needle)

p.write_text(s2)
