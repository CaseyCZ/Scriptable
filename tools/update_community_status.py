#!/usr/bin/env python3
from __future__ import annotations

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
    pattern = re.compile(
        rf"\b{re.escape(field)}\s*:\s*(?:'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\")"
    )
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
        files = [file_url, *variant_files(chunk)]
        files = list(dict.fromkeys(url.strip() for url in files if url.strip()))
        projects.append({"name": name, "files": files})

    extra_text = EXTRA.read_text(encoding="utf-8")
    for line in extra_text.splitlines():
        if "communityItem(" not in line:
            continue
        chunk = line.split("communityItem(", 1)[1]
        values = js_strings(chunk)
        if len(values) < 5:
            continue
        files = [values[4], *variant_files(chunk)]
        files = list(dict.fromkeys(url.strip() for url in files if url.strip()))
        projects.append({"name": values[0], "files": files})

    dedup: dict[tuple[str, ...], dict[str, object]] = {}
    for project in projects:
        files = tuple(
            url for url in project["files"]
            if isinstance(url, str) and url.startswith(("https://", "http://"))
        )
        if not files:
            continue
        project["files"] = list(files)
        dedup.setdefault(files, project)

    return list(dedup.values())


def request(url: str, sample_bytes: int, accept: str = "text/plain,*/*") -> tuple[int, str, bytes]:
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
        sample = response.read(sample_bytes)
    return status, final_url, sample


def scriptable_score(text: str) -> int:
    markers = [
        "Variables used by Scriptable",
        "ListWidget",
        "Script.setWidget",
        "Script.complete",
        "Script.name(",
        "config.runsInWidget",
        "args.widgetParameter",
        "FileManager.",
        "Notification(",
        "CalendarEvent.",
        "Reminder.",
        "Location.",
        "Photos.",
        "Safari.open",
        "WebView(",
        "Alert(",
    ]
    return sum(1 for marker in markers if marker in text)


def direct_request_urls(text: str, install_url: str) -> list[str]:
    pattern = re.compile(
        r"(?:new\s+)?Request\s*\(\s*(?:'([^']+)'|\"([^\"]+)\"|`([^`$]+)`)\s*\)",
        re.IGNORECASE,
    )
    ignored_hosts = {
        "raw.githubusercontent.com",
        "github.com",
        "www.github.com",
        "api.github.com",
        "gist.githubusercontent.com",
        "scriptable.app",
        "www.buymeacoffee.com",
        "buymeacoffee.com",
        "ko-fi.com",
        "www.ko-fi.com",
    }
    out: list[str] = []
    for match in pattern.finditer(text):
        url = next((value for value in match.groups() if value), "").strip()
        if not url.startswith(("https://", "http://")) or url == install_url:
            continue
        try:
            parsed = urllib.parse.urlparse(url)
        except Exception:
            continue
        host = (parsed.hostname or "").lower()
        if host in ignored_hosts:
            continue
        if parsed.path in ("", "/") and not parsed.query:
            # Usually a base URL that is combined with a runtime path later.
            continue
        if any(token in url for token in ("${", "{", "}")):
            continue
        if re.search(r"\.(?:png|jpe?g|gif|webp|svg|ico)(?:$|[?#])", parsed.path, re.IGNORECASE):
            continue
        if url not in out:
            out.append(url)
        if len(out) >= MAX_RUNTIME_DEPENDENCIES:
            break
    return out


def html_markers(text: str) -> list[str]:
    if "loadString" not in text:
        return []
    # HTML scrapers often depend on a class/id name. Remove regex escaping first,
    # then capture those stable selectors and verify that the remote page still has one.
    normalized = text.replace("\\", "")
    markers: list[str] = []
    for match in re.finditer(r"(?:class|id)\s*=\s*[\"']([A-Za-z0-9_-]{5,})[\"']", normalized):
        marker = match.group(1)
        if marker not in markers:
            markers.append(marker)
        if len(markers) >= 5:
            break
    return markers


def probe_install(item: dict[str, str]) -> tuple[str, dict[str, object], str]:
    url = item["file"]
    checked_at = now_iso()
    last_error = None
    last_status = None

    for attempt in range(2):
        try:
            status, final_url, sample = request(url, SCRIPT_SAMPLE_BYTES)
            if 200 <= status < 400 and sample.strip():
                text = sample.decode("utf-8", errors="replace")
                score = scriptable_score(text)
                return url, {
                    "name": item["name"],
                    "online": True,
                    "sourceOnline": True,
                    "checkedAt": checked_at,
                    "httpStatus": status,
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
        "name": item["name"],
        "online": False,
        "sourceOnline": False,
        "checkedAt": checked_at,
        "httpStatus": last_status,
        "scriptableScore": 0,
        "contentWarning": None,
        "error": (last_error or "Unknown error")[:300],
    }, ""


def probe_dependency(url: str) -> tuple[str, dict[str, object]]:
    last_error = None
    last_status = None
    final_url = url
    sample = b""

    for attempt in range(2):
        try:
            status, final_url, sample = request(url, DEPENDENCY_SAMPLE_BYTES, "text/html,application/json,text/plain,*/*")
            # Protected endpoints are still alive. A script may authenticate at runtime.
            return url, {
                "reachable": 200 <= status < 500 and status not in (404, 410),
                "status": status,
                "finalUrl": final_url,
                "body": sample.decode("utf-8", errors="replace"),
                "error": None,
            }
        except urllib.error.HTTPError as exc:
            last_status = exc.code
            last_error = f"HTTPError: {exc.code} {exc.reason}"
            if exc.code in (401, 403, 405, 429):
                return url, {
                    "reachable": True,
                    "status": exc.code,
                    "finalUrl": url,
                    "body": "",
                    "error": None,
                }
            if exc.code in (404, 410):
                return url, {
                    "reachable": False,
                    "status": exc.code,
                    "finalUrl": url,
                    "body": "",
                    "error": last_error,
                }
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"

        if attempt == 0:
            time.sleep(0.25)

    return url, {
        "reachable": False if last_status in (404, 410) or last_status is None else True,
        "status": last_status,
        "finalUrl": final_url,
        "body": "",
        "error": (last_error or "Unknown dependency error")[:300],
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

    endpoint_dependencies: dict[str, list[str]] = {}
    dependency_urls: set[str] = set()
    endpoint_markers: dict[str, list[str]] = {}
    for url, sample_text in samples.items():
        if not sample_text or not results[url].get("sourceOnline"):
            continue
        deps = direct_request_urls(sample_text, url)
        endpoint_dependencies[url] = deps
        dependency_urls.update(deps)
        endpoint_markers[url] = html_markers(sample_text)
        module_matches = sorted(set(re.findall(r"\bimportModule\s*\(\s*['\"]([^'\"]+)['\"]", sample_text)))
        if module_matches:
            results[url]["moduleDependencies"] = module_matches[:8]
            results[url]["contentWarning"] = "Requires additional importModule file(s): " + ", ".join(module_matches[:3])

    dependency_results: dict[str, dict[str, object]] = {}
    if dependency_urls:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = [pool.submit(probe_dependency, url) for url in sorted(dependency_urls)]
            for future in as_completed(futures):
                url, status = future.result()
                dependency_results[url] = status

    for install_url, deps in endpoint_dependencies.items():
        broken: list[str] = []
        checked: list[dict[str, object]] = []
        markers = endpoint_markers.get(install_url, [])
        for dep in deps:
            state = dependency_results.get(dep, {})
            reachable = state.get("reachable") is True
            final_url = str(state.get("finalUrl") or dep)
            reason = None
            if not reachable:
                reason = str(state.get("error") or f"HTTP {state.get('status')}")
            elif dependency_is_homepage_redirect(dep, final_url):
                reachable = False
                reason = f"Redirected to homepage: {final_url}"
            elif markers and state.get("body"):
                body = str(state.get("body") or "")
                if not any(marker in body for marker in markers):
                    reachable = False
                    reason = "Expected page marker missing: " + ", ".join(markers[:2])

            checked.append({
                "url": dep,
                "reachable": reachable,
                "httpStatus": state.get("status"),
                "finalUrl": final_url if final_url != dep else None,
                "error": reason,
            })
            if not reachable:
                broken.append(f"{dep} ({reason or 'unreachable'})")

        if checked:
            results[install_url]["runtimeDependencies"] = checked
        if broken and results[install_url].get("sourceOnline") is True:
            results[install_url]["online"] = False
            results[install_url]["error"] = ("Runtime dependency failed: " + " | ".join(broken))[:600]

    project_online = 0
    for project in projects:
        statuses = [results.get(url, {}) for url in project["files"]]
        if any(status.get("online") is True for status in statuses):
            project_online += 1
    project_offline = len(projects) - project_online

    endpoint_online = sum(1 for item in results.values() if item.get("online") is True)
    endpoint_offline = len(results) - endpoint_online
    payload = {
        "generatedAt": now_iso(),
        "total": len(projects),
        "online": project_online,
        "offline": project_offline,
        "endpointsTotal": len(results),
        "endpointsOnline": endpoint_online,
        "endpointsOffline": endpoint_offline,
        "runtimeDependenciesChecked": len(dependency_results),
        "items": dict(sorted(results.items())),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Checked {len(projects)} community projects / {len(results)} download endpoints / "
        f"{len(dependency_results)} direct runtime dependencies: "
        f"{project_online} projects online, {project_offline} offline"
    )


if __name__ == "__main__":
    main()
