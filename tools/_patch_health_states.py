from pathlib import Path

checker = Path("tools/update_community_status.py")
text = checker.read_text(encoding="utf-8")

module_block = '''        module_matches = sorted(set(re.findall(r"\\bimportModule\\s*\\(\\s*['\\\"]([^'\\\"]+)['\\\"]", sample_text)))
        if module_matches:
            results[url]["moduleDependencies"] = module_matches[:8]
            results[url]["contentWarning"] = "Requires additional importModule file(s): " + ", ".join(module_matches[:3])
'''
module_new = module_block + '''        requires_setup = bool(re.search(r"['\\\"]Authorization['\\\"]\\s*:", sample_text, re.IGNORECASE))
        requires_setup = requires_setup or bool(
            re.search(r"\\b(?:username|password|api[_-]?key|client[_-]?secret)\\b", sample_text, re.IGNORECASE)
            and re.search(r"\\bRequest\\s*\\(", sample_text)
        )
        if requires_setup:
            results[url]["requiresSetup"] = True
'''
if module_block not in text:
    raise SystemExit("module block not found")
text = text.replace(module_block, module_new, 1)

counts_old = '''    project_online = sum(
        1 for project in projects
        if any(results.get(url, {}).get("online") is True for url in project["files"])
    )
    project_offline = len(projects) - project_online
    endpoint_online = sum(1 for item in results.values() if item.get("online") is True)
    endpoint_offline = len(results) - endpoint_online

    payload = {
        "generatedAt": now_iso(),
        "total": len(projects), "online": project_online, "offline": project_offline,
        "endpointsTotal": len(results), "endpointsOnline": endpoint_online,
        "endpointsOffline": endpoint_offline,
        "runtimeDependenciesChecked": len(dependency_results),
        "runtimeWarnings": runtime_warnings,
        "items": dict(sorted(results.items())),
    }
'''
counts_new = '''    for item in results.values():
        if item.get("online") is not True:
            item["health"] = "offline"
            item["verificationReason"] = item.get("error")
            continue

        limited_reasons: list[str] = []
        if item.get("requiresSetup") is True:
            limited_reasons.append("Requires credentials or account-specific setup")
        if item.get("moduleDependencies"):
            limited_reasons.append("Requires additional Scriptable module file(s)")
        if item.get("contentWarning"):
            limited_reasons.append(str(item["contentWarning"]))
        for dep in item.get("runtimeDependencies", []):
            if isinstance(dep, dict) and dep.get("reachable") is None:
                limited_reasons.append("At least one runtime dependency could not be verified safely")
                break

        if limited_reasons:
            item["health"] = "limited"
            item["verificationReason"] = "; ".join(dict.fromkeys(limited_reasons))[:500]
        else:
            item["health"] = "online"
            item["verificationReason"] = None

    def project_health(project: dict[str, object]) -> str:
        healths = [str(results.get(url, {}).get("health") or "offline") for url in project["files"]]
        if "online" in healths:
            return "online"
        if "limited" in healths:
            return "limited"
        return "offline"

    project_health_values = [project_health(project) for project in projects]
    project_online = project_health_values.count("online")
    project_limited = project_health_values.count("limited")
    project_offline = project_health_values.count("offline")
    endpoint_online = sum(1 for item in results.values() if item.get("health") == "online")
    endpoint_limited = sum(1 for item in results.values() if item.get("health") == "limited")
    endpoint_offline = sum(1 for item in results.values() if item.get("health") == "offline")

    payload = {
        "generatedAt": now_iso(),
        "total": len(projects), "online": project_online, "limited": project_limited, "offline": project_offline,
        "endpointsTotal": len(results), "endpointsOnline": endpoint_online,
        "endpointsLimited": endpoint_limited, "endpointsOffline": endpoint_offline,
        "runtimeDependenciesChecked": len(dependency_results),
        "runtimeWarnings": runtime_warnings,
        "items": dict(sorted(results.items())),
    }
'''
if counts_old not in text:
    raise SystemExit("count block not found")
text = text.replace(counts_old, counts_new, 1)

print_old = '''        f"{project_online} projects online, {project_offline} offline, {runtime_warnings} unverified deps"
'''
print_new = '''        f"{project_online} online, {project_limited} limited, {project_offline} offline, "
        f"{runtime_warnings} unverified deps"
'''
if print_old not in text:
    raise SystemExit("print block not found")
text = text.replace(print_old, print_new, 1)
checker.write_text(text, encoding="utf-8")

js = Path("assets/js/index-page.js")
js_text = js.read_text(encoding="utf-8")
old_status = '''    let communityStatus={generatedAt:null,total:0,online:0,offline:0,items:{}};
    function communityStatusFor(app){const urls=[app.file,...(app.variants||[]).map(v=>v.file)].filter(Boolean);const states=urls.map(url=>communityStatus?.items?.[url]).filter(Boolean);if(!states.length)return null;if(states.some(item=>item?.online===true))return {online:true,checkedAt:states.find(item=>item?.checkedAt)?.checkedAt||null};if(states.every(item=>item?.checkedAt))return {online:false,checkedAt:states[0]?.checkedAt||null};return states[0]||null}
    function communityStatusBadge(app){const item=communityStatusFor(app);if(item?.online===true)return `<span class=\"communityAvailability online\">● Online</span>`;if(item?.checkedAt)return `<span class=\"communityAvailability offline\">● Offline</span>`;return `<span class=\"communityAvailability checking\">● ${tr('Čeká na kontrolu','Checking')}</span>`}
    function renderCommunityHealth(){const host=document.getElementById('communityHealth');if(!host)return;const online=Number.isFinite(communityStatus.online)?communityStatus.online:0;const offline=Number.isFinite(communityStatus.offline)?communityStatus.offline:0;const checked=online+offline;let stamp='';if(communityStatus.generatedAt){const date=new Date(communityStatus.generatedAt);if(!Number.isNaN(date.getTime())){const locale={cs:'cs-CZ',en:'en-GB',de:'de-DE',es:'es-ES',fr:'fr-FR'}[lang]||'en-GB';stamp=new Intl.DateTimeFormat(locale,{day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}).format(date)}}host.innerHTML=checked?`<span class=\"communityAvailability online\">● Online ${online}</span><span class=\"communityAvailability offline\">● Offline ${offline}</span>${stamp?`<span class=\"communityChecked\">${tr('Poslední kontrola','Last checked')}: ${stamp}</span>`:''}`:`<span class=\"communityAvailability checking\">● ${tr('Čeká na kontrolu','Checking')}</span>`}
'''
new_status = '''    let communityStatus={generatedAt:null,total:0,online:0,limited:0,offline:0,items:{}};
    function communityStatusFor(app){const urls=[app.file,...(app.variants||[]).map(v=>v.file)].filter(Boolean);const states=urls.map(url=>communityStatus?.items?.[url]).filter(Boolean);if(!states.length)return null;const verified=states.find(item=>item?.health==='online');if(verified)return {health:'online',online:true,checkedAt:verified.checkedAt||null};const limited=states.find(item=>item?.health==='limited');if(limited)return {health:'limited',online:true,checkedAt:limited.checkedAt||null,reason:limited.verificationReason||null};const offline=states.find(item=>item?.health==='offline');if(offline)return {health:'offline',online:false,checkedAt:offline.checkedAt||null,reason:offline.verificationReason||offline.error||null};if(states.some(item=>item?.online===true))return {health:'online',online:true,checkedAt:states.find(item=>item?.checkedAt)?.checkedAt||null};if(states.every(item=>item?.checkedAt))return {health:'offline',online:false,checkedAt:states[0]?.checkedAt||null};return states[0]||null}
    function communityStatusBadge(app){const item=communityStatusFor(app);if(item?.health==='online')return `<span class=\"communityAvailability online\">● Online</span>`;if(item?.health==='limited')return `<span class=\"communityAvailability limited\" title=\"${esc(item.reason||tr('Vyžaduje nastavení nebo část kontroly nelze provést automaticky','Requires setup or cannot be fully checked automatically'))}\">● ${tr('Omezeně ověřeno','Limited check')}</span>`;if(item?.checkedAt)return `<span class=\"communityAvailability offline\" title=\"${esc(item.reason||'')}\">● Offline</span>`;return `<span class=\"communityAvailability checking\">● ${tr('Čeká na kontrolu','Checking')}</span>`}
    function renderCommunityHealth(){const host=document.getElementById('communityHealth');if(!host)return;const online=Number.isFinite(communityStatus.online)?communityStatus.online:0;const limited=Number.isFinite(communityStatus.limited)?communityStatus.limited:0;const offline=Number.isFinite(communityStatus.offline)?communityStatus.offline:0;const checked=online+limited+offline;let stamp='';if(communityStatus.generatedAt){const date=new Date(communityStatus.generatedAt);if(!Number.isNaN(date.getTime())){const locale={cs:'cs-CZ',en:'en-GB',de:'de-DE',es:'es-ES',fr:'fr-FR'}[lang]||'en-GB';stamp=new Intl.DateTimeFormat(locale,{day:'2-digit',month:'2-digit',year:'numeric',hour:'2-digit',minute:'2-digit'}).format(date)}}host.innerHTML=checked?`<span class=\"communityAvailability online\">● Online ${online}</span>${limited?`<span class=\"communityAvailability limited\">● ${tr('Omezeně','Limited')} ${limited}</span>`:''}<span class=\"communityAvailability offline\">● Offline ${offline}</span>${stamp?`<span class=\"communityChecked\">${tr('Poslední kontrola','Last checked')}: ${stamp}</span>`:''}`:`<span class=\"communityAvailability checking\">● ${tr('Čeká na kontrolu','Checking')}</span>`}
'''
if old_status not in js_text:
    raise SystemExit("community status UI block not found")
js.write_text(js_text.replace(old_status, new_status, 1), encoding="utf-8")

html = Path("index.html")
html_text = html.read_text(encoding="utf-8")
css_old = '.communityAvailability.online{color:var(--ok);border-color:color-mix(in srgb,var(--ok) 45%,var(--border));background:color-mix(in srgb,var(--ok) 10%,transparent)}.communityAvailability.offline{'
css_new = '.communityAvailability.online{color:var(--ok);border-color:color-mix(in srgb,var(--ok) 45%,var(--border));background:color-mix(in srgb,var(--ok) 10%,transparent)}.communityAvailability.limited{color:var(--warn);border-color:color-mix(in srgb,var(--warn) 45%,var(--border));background:color-mix(in srgb,var(--warn) 10%,transparent)}.communityAvailability.offline{'
if css_old not in html_text:
    raise SystemExit("availability CSS block not found")
html.write_text(html_text.replace(css_old, css_new, 1), encoding="utf-8")

print("Three-state health checks patched")
