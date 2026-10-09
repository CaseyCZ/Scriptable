#!/usr/bin/env python3
from __future__ import annotations

import ipaddress
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets" / "js" / "index-page.js"
if not REGISTRY.exists():
    REGISTRY = ROOT / "index.html"
EXTRA = ROOT / "community-extra.js"
OUTPUT = ROOT / "data" / "community-status.json"
USER_AGENT = "CaseyCZ-Scriptable-Catalog (+https://caseycz.github.io/Scriptable/)"
MAX_WORKERS = 12
TIMEOUT = 15
SCRIPT_SAMPLE_BYTES = 131072
DEPENDENCY_SAMPLE_BYTES = 131072
MAX_RUNTIME_DEPENDENCIES = 4
SAFE_METHODS = {"GET", "HEAD"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def decode_js_string(raw: str) -> str:
    return raw.replace("\\/", "/").replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")


def js_strings(text: str) -> list[str]:
    out: list[str] = []
    pattern = re.compile(r"'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\"")
    for match in pattern.finditer(text):
        raw = match.group(1) if match.group(1) is not None else match.group(2)
        out.append(decode_js_string(raw))
    return out


def top_level_objects(text: str) -> list[str]:
    out: list[str] = []
    start: int | None = None
    depth = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(text):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in ("'", '"', "`"):
            quote = char
            continue
        if char == "{":
            if depth == 0:
                start = index
            depth += 1
        elif char == "}" and depth:
            depth -= 1
            if depth == 0 and start is not None:
                out.append(text[start:index + 1])
                start = None
    return out


def field_string(chunk: str, field: str) -> str | None:
    pattern = re.compile(rf"\b{re.escape(field)}\s*:\s*(?:'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\")")
    match = pattern.search(chunk)
    if not match:
        return None
    raw = match.group(1) if match.group(1) is not None else match.group(2)
    return decode_js_string(raw)


def variant_files(chunk: str) -> list[str]:
    if "variants" not in chunk:
        return []
    tail = chunk.split("variants", 1)[1]
    pattern = re.compile(r"\bfile\s*:\s*(?:'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\")")
    out: list[str] = []
    for match in pattern.finditer(tail):
        raw = match.group(1) if match.group(1) is not None else match.group(2)
        out.append(decode_js_string(raw))
    return out


def collect_projects() -> list[dict[str, object]]:
    projects: list[dict[str, object]] = []
    registry_text = REGISTRY.read_text(encoding="utf-8")
    try:
        community_block = registry_text.split("const communityApps=[", 1)[1].split("];\n    communityApps.push", 1)[0]
    except IndexError as exc:
        raise RuntimeError(f"Unable to locate communityApps in {REGISTRY.relative_to(ROOT)}") from exc

    for chunk in top_level_objects(community_block):
        name = field_string(chunk, "name")
        file_url = field_string(chunk, "file")
        if not name or not file_url:
            continue
        files = list(dict.fromkeys([file_url, *variant_files(chunk)]))
        projects.append({"name": name, "files": files})

    extra_text = EXTRA.read_text(encoding="utf-8")
    for line in extra_text.splitlines():
        if "communityItem(" not in line:
            continue
        chunk = line.split("communityItem(", 1)[1]
        values = js_strings(chunk)
        if len(values) < 5:
            continue
        files = list(dict.fromkeys([values[4], *variant_files(chunk)]))
        projects.append({"name": values[0], "files": files})

    dedup: dict[tuple[str, ...], dict[str, object]] = {}
    for project in projects:
        files = tuple(
            url for url in project["files"]
            if isinstance(url, str) and url.startswith(("https://", "http://"))
        )
        if files:
            project["files"] = list(files)
            dedup.setdefault(files, project)
    return list(dedup.values())


def request(url: str, sample_bytes: int, accept: str = "text/plain,*/*") -> tuple[int, str, bytes, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
            "Range": f"bytes=0-{sample_bytes - 1}",
            "Cache-Control": "no-cache",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        status = getattr(response, "status", 200)
        final_url = response.geturl()
        content_type = str(response.headers.get("Content-Type", ""))
        sample = response.read(sample_bytes)
    return status, final_url, sample, content_type


def scriptable_score(text: str) -> int:
    markers = [
        "Variables used by Scriptable", "ListWidget", "Script.setWidget", "Script.complete",
        "Script.name(", "config.runsInWidget", "args.widgetParameter", "FileManager.",
        "Notification(", "CalendarEvent.", "Reminder.", "Location.", "Photos.",
        "Safari.open", "WebView(", "Alert(",
    ]
    return sum(1 for marker in markers if marker in text)


def is_placeholder_or_local(url: str) -> bool:
    try:
        parsed = urllib.parse.urlparse(url)
        host = (parsed.hostname or "").lower().strip(".")
    except Exception:
        return True
    if not host:
        return True
    if host in {"localhost", "example.com", "www.example.com"} or host.endswith((".example.com", ".local", ".lan")):
        return True
    if any(token in url.lower() for token in ("your-domain", "your_domain", "yourhost", "example.com")):
        return True
    try:
        address = ipaddress.ip_address(host)
        if address.is_private or address.is_loopback or address.is_link_local:
            return True
    except ValueError:
        pass
    return False


def literal_request_matches(text: str) -> list[tuple[re.Match[str], str, str | None]]:
    pattern = re.compile(
        r"(?:(?:let|const|var)\s+([A-Za-z_$][\w$]*)\s*=\s*)?"
        r"(?:new\s+)?Request\s*\(\s*(?:'([^']+)'|\"([^\"]+)\"|`([^`$]+)`)\s*\)",
        re.IGNORECASE,
    )
    out: list[tuple[re.Match[str], str, str | None]] = []
    for match in pattern.finditer(text):
        url = next((value for value in match.groups()[1:] if value), "").strip()
        out.append((match, url, match.group(1)))
    return out


def direct_requests(text: str, install_url: str) -> list[dict[str, object]]:
    ignored_hosts = {
        "raw.githubusercontent.com", "github.com", "www.github.com", "api.github.com",
        "gist.githubusercontent.com", "scriptable.app", "www.buymeacoffee.com",
        "buymeacoffee.com", "ko-fi.com", "www.ko-fi.com",
    }
    out: list[dict[str, object]] = []
    seen: set[str] = set()
    for match, url, variable in literal_request_matches(text):
        if not url.startswith(("https://", "http://")) or url == install_url or is_placeholder_or_local(url):
            continue
        parsed = urllib.parse.urlparse(url)
        host = (parsed.hostname or "").lower()
        if host in ignored_hosts:
            continue
        if parsed.path in ("", "/") and not parsed.query:
            continue
        if any(token in url for token in ("${", "{", "}")):
            continue
        if re.search(r"\.(?:png|jpe?g|gif|webp|svg|ico)(?:$|[?#])", parsed.path, re.IGNORECASE):
            continue
        if url in seen:
            continue

        method = "GET"
        expects_html = False
        if variable:
            tail = text[match.end(): match.end() + 2500]
            method_match = re.search(
                rf"\b{re.escape(variable)}\.method\s*=\s*['\"]([A-Za-z]+)['\"]", tail,
                re.IGNORECASE,
            )
            if method_match:
                method = method_match.group(1).upper()
            expects_html = bool(re.search(rf"\b{re.escape(variable)}\.loadString\s*\(", tail))

        seen.add(url)
        out.append({"url": url, "method": method, "expectsHtml": expects_html})
        if len(out) >= MAX_RUNTIME_DEPENDENCIES:
            break
    return out


def html_markers(text: str) -> list[str]:
    if "loadString" not in text:
        return []
    normalized = text.replace("\\", "")
    markers: list[str] = []
    for match in re.finditer(r"(?:class|id)\s*=\s*[\"']([A-Za-z0-9_-]{5,})[\"']", normalized):
        marker = match.group(1)
        if marker not in markers:
            markers.append(marker)
        if len(markers) >= 6:
            break
    return markers


def selector_present(body: str, marker: str) -> bool:
    escaped = re.escape(marker)
    class_pattern = rf"\bclass\s*=\s*['\"][^'\"]*(?:^|\s){escaped}(?:\s|$)[^'\"]*['\"]"
    id_pattern = rf"\bid\s*=\s*['\"]{escaped}['\"]"
    return bool(re.search(class_pattern, body, re.IGNORECASE) or re.search(id_pattern, body, re.IGNORECASE))


def looks_like_html(body: str, content_type: str) -> bool:
    prefix = body.lstrip()[:1000].lower()
    return "text/html" in content_type.lower() or prefix.startswith("<!doctype html") or "<html" in prefix or "<body" in prefix


def probe_install(item: dict[str, str]) -> tuple[str, dict[str, object], str]:
    url = item["file"]
    checked_at = now_iso()
    last_error = None
    last_status = None
    for attempt in range(2):
        try:
            status, final_url, sample, _ = request(url, SCRIPT_SAMPLE_BYTES)
            if 200 <= status < 400 and sample.strip():
                text = sample.decode("utf-8", errors="replace")
                score = scriptable_score(text)
                return url, {
                    "name": item["name"], "online": True, "sourceOnline": True,
                    "checkedAt": checked_at, "httpStatus": status,
                    "finalUrl": final_url if final_url != url else None,
                    "scriptableScore": score,
                    "contentWarning": None if score else "No clear Scriptable API markers found in sampled source",
                    "error": None,
                }, text
            last_status = status
            last_error = "Empty response" if not sample.strip() else f"HTTP {status}"
        except urllib.error.HTTPError as exc:
            last_status = exc.code
            last_error = f"HTTPError: {exc.code} {exc.reason}"
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt == 0:
            time.sleep(0.25)

    return url, {
        "name": item["name"], "online": False, "sourceOnline": False,
        "checkedAt": checked_at, "httpStatus": last_status, "scriptableScore": 0,
        "contentWarning": None, "error": (last_error or "Unknown error")[:300],
    }, ""


def probe_dependency(meta: dict[str, object]) -> tuple[str, dict[str, object]]:
    url = str(meta["url"])
    method = str(meta.get("method") or "GET").upper()
    if method not in SAFE_METHODS:
        return url, {
            "reachable": None, "definiteBroken": False, "status": None, "finalUrl": url,
            "body": "", "contentType": "", "error": f"Not probed: script uses {method}",
        }

    last_error = None
    last_status = None
    final_url = url
    for attempt in range(2):
        try:
            status, final_url, sample, content_type = request(
                url, DEPENDENCY_SAMPLE_BYTES, "text/html,application/json,text/plain,*/*"
            )
            return url, {
                "reachable": 200 <= status < 500 and status not in (404, 410),
                "definiteBroken": status in (404, 410),
                "status": status, "finalUrl": final_url,
                "body": sample.decode("utf-8", errors="replace"),
                "contentType": content_type, "error": None,
            }
        except urllib.error.HTTPError as exc:
            last_status = exc.code
            last_error = f"HTTPError: {exc.code} {exc.reason}"
            if exc.code in (401, 403, 405, 429):
                return url, {
                    "reachable": True, "definiteBroken": False, "status": exc.code,
                    "finalUrl": url, "body": "", "contentType": "", "error": None,
                }
            if exc.code in (404, 410):
                return url, {
                    "reachable": False, "definiteBroken": True, "status": exc.code,
                    "finalUrl": url, "body": "", "contentType": "", "error": last_error,
                }
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt == 0:
            time.sleep(0.25)

    return url, {
        "reachable": None, "definiteBroken": False, "status": last_status,
        "finalUrl": final_url, "body": "", "contentType": "",
        "error": (last_error or "Dependency could not be verified")[:300],
    }


def dependency_is_homepage_redirect(original: str, final_url: str) -> bool:
    try:
        before = urllib.parse.urlparse(original)
        after = urllib.parse.urlparse(final_url)
    except Exception:
        return False
    before_path = before.path.rstrip("/")
    after_path = after.path.rstrip("/")
    return bool(before_path and before_path != after_path and not after_path)


def main() -> None:
    projects = collect_projects()
    if not projects:
        raise SystemExit("No community download URLs found")

    endpoints: dict[str, dict[str, str]] = {}
    for project in projects:
        for url in project["files"]:
            endpoints.setdefault(url, {"name": str(project["name"]), "file": url})

    results: dict[str, dict[str, object]] = {}
    samples: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(probe_install, item) for item in endpoints.values()]
        for future in as_completed(futures):
            url, status, sample_text = future.result()
            results[url] = status
            samples[url] = sample_text

    endpoint_dependencies: dict[str, list[dict[str, object]]] = {}
    dependency_meta: dict[str, dict[str, object]] = {}
    endpoint_markers: dict[str, list[str]] = {}
    for url, sample_text in samples.items():
        if not sample_text or not results[url].get("sourceOnline"):
            continue
        deps = direct_requests(sample_text, url)
        endpoint_dependencies[url] = deps
        for dep in deps:
            dependency_meta.setdefault(str(dep["url"]), dep)
        endpoint_markers[url] = html_markers(sample_text)
        module_matches = sorted(set(re.findall(r"\bimportModule\s*\(\s*['\"]([^'\"]+)['\"]", sample_text)))
        if module_matches:
            results[url]["moduleDependencies"] = module_matches[:8]
            results[url]["contentWarning"] = "Requires additional importModule file(s): " + ", ".join(module_matches[:3])

    dependency_results: dict[str, dict[str, object]] = {}
    if dependency_meta:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = [pool.submit(probe_dependency, meta) for meta in dependency_meta.values()]
            for future in as_completed(futures):
                url, state = future.result()
                dependency_results[url] = state

    runtime_warnings = 0
    for install_url, deps in endpoint_dependencies.items():
        hard_broken: list[str] = []
        checked: list[dict[str, object]] = []
        markers = endpoint_markers.get(install_url, [])
        for meta in deps:
            dep = str(meta["url"])
            state = dependency_results.get(dep, {})
            reachable = state.get("reachable")
            definite_broken = state.get("definiteBroken") is True
            final_url = str(state.get("finalUrl") or dep)
            reason = str(state.get("error") or "") or None
            body = str(state.get("body") or "")
            content_type = str(state.get("contentType") or "")

            if reachable is True and dependency_is_homepage_redirect(dep, final_url):
                reachable = False
                definite_broken = True
                reason = f"Redirected to homepage: {final_url}"

            if (
                reachable is True and meta.get("expectsHtml") is True and markers and
                body and looks_like_html(body, content_type)
            ):
                present = [marker for marker in markers if selector_present(body, marker)]
                if not present:
                    reachable = False
                    definite_broken = True
                    reason = "Expected HTML selector missing: " + ", ".join(markers[:3])

            public_state: dict[str, object] = {
                "url": dep,
                "method": meta.get("method") or "GET",
                "reachable": reachable,
                "httpStatus": state.get("status"),
                "finalUrl": final_url if final_url != dep else None,
                "error": reason,
            }
            checked.append(public_state)
            if definite_broken:
                fallback_reason = reason or ("HTTP " + str(state.get("status")))
                hard_broken.append(f"{dep} ({fallback_reason})")
            elif reachable is None:
                runtime_warnings += 1

        if checked:
            results[install_url]["runtimeDependencies"] = checked
        if hard_broken and results[install_url].get("sourceOnline") is True:
            results[install_url]["online"] = False
            results[install_url]["error"] = ("Runtime dependency failed: " + " | ".join(hard_broken))[:700]

    project_online = sum(
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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Checked {len(projects)} community projects / {len(results)} download endpoints / "
        f"{len(dependency_results)} runtime dependencies: "
        f"{project_online} projects online, {project_offline} offline, {runtime_warnings} unverified deps"
    )


if __name__ == "__main__":
    main()
