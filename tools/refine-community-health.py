#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "community-status.json"
USER_AGENT = "CaseyCZ-Scriptable-Catalog (+https://caseycz.github.io/Scriptable/)"
TIMEOUT = 12
SAMPLE = 131072

SCRIPTABLE_MARKERS = (
    "ListWidget", "Script.setWidget", "Script.complete", "FileManager.", "Notification(",
    "CalendarEvent.", "Reminder.", "Location.", "Photos.", "Safari.open", "WebView(",
    "Alert(", "DrawContext(", "SFSymbol.", "Pasteboard.", "QuickLook.",
)


def fetch(url: str, accept: str = "text/plain,*/*") -> tuple[int, str, str, str]:
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept,
        "Range": f"bytes=0-{SAMPLE-1}",
        "Cache-Control": "no-cache",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        status = getattr(response, "status", 200)
        final_url = response.geturl()
        content_type = str(response.headers.get("Content-Type", ""))
        body = response.read(SAMPLE).decode("utf-8", errors="replace")
    return status, final_url, content_type, body


def looks_html(text: str, content_type: str = "") -> bool:
    prefix = text.lstrip()[:1000].lower()
    return "text/html" in content_type.lower() or prefix.startswith("<!doctype html") or "<html" in prefix


def looks_executable_scriptable(text: str) -> bool:
    if not text.strip() or looks_html(text):
        return False
    marker_count = sum(1 for marker in SCRIPTABLE_MARKERS if marker in text)
    has_runtime = bool(re.search(r"\b(?:new\s+)?(?:ListWidget|Request|Alert|WebView|Notification|DrawContext)\s*\(", text))
    has_script_entry = "Variables used by Scriptable" in text or "Script.setWidget" in text or "Script.complete" in text
    obvious_tooling = bool(re.search(r"\b(?:module\.exports\s*=\s*\{|eslint|webpack|rollup|vite|prettier)\b", text, re.I)) and marker_count == 0
    return not obvious_tooling and marker_count >= 1 and (has_runtime or has_script_entry)


def literal_requests(text: str) -> list[dict[str, object]]:
    pattern = re.compile(
        r"(?:(?:let|const|var)\s+([A-Za-z_$][\w$]*)\s*=\s*)?"
        r"(?:new\s+)?Request\s*\(\s*(?:'([^']+)'|\"([^\"]+)\"|`([^`$]+)`)\s*\)",
        re.I,
    )
    out: list[dict[str, object]] = []
    seen: set[str] = set()
    for match in pattern.finditer(text):
        url = next((v for v in match.groups()[1:] if v), "").strip()
        if not url.startswith(("https://", "http://")) or url in seen:
            continue
        variable = match.group(1)
        tail = text[match.end():match.end()+2600]
        load_string = False
        load_json = False
        if variable:
            load_string = bool(re.search(rf"\b{re.escape(variable)}\.loadString\s*\(", tail))
            load_json = bool(re.search(rf"\b{re.escape(variable)}\.loadJSON\s*\(", tail))
        if not load_string and not load_json:
            load_string = bool(re.search(r"\.loadString\s*\(", tail[:900]))
            load_json = bool(re.search(r"\.loadJSON\s*\(", tail[:900]))
        if not (load_string or load_json):
            continue
        seen.add(url)
        out.append({"url": url, "html": load_string, "json": load_json})
        if len(out) >= 6:
            break
    return out


def expected_html_markers(text: str) -> list[str]:
    normalized = text.replace("\\", "")
    markers: list[str] = []
    patterns = (
        r"(?:class|id)\s*=\s*[\"']([A-Za-z][A-Za-z0-9_-]{3,})",
        r"(?:class|id)\s*=\s*\"?([A-Za-z][A-Za-z0-9_-]{3,})",
        r"querySelector(?:All)?\s*\(\s*[\"'][.#]([A-Za-z][A-Za-z0-9_-]{3,})",
        r"getElementById\s*\(\s*[\"']([A-Za-z][A-Za-z0-9_-]{3,})",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, normalized, re.I):
            marker = match.group(1)
            if marker not in markers:
                markers.append(marker)
            if len(markers) >= 8:
                return markers
    return markers


def marker_present(body: str, marker: str) -> bool:
    return bool(re.search(rf"(?:class\s*=\s*[\"'][^\"']*\b{re.escape(marker)}\b|id\s*=\s*[\"']{re.escape(marker)}[\"'])", body, re.I))


def auth_or_setup_likely(text: str) -> bool:
    return bool(re.search(r"\b(?:Authorization|Bearer|api[_-]?key|token|client[_-]?secret|username|password)\b", text, re.I))


def append_reason(item: dict[str, object], reason: str) -> None:
    old = str(item.get("verificationReason") or "").strip()
    if old and reason not in old:
        item["verificationReason"] = (old + "; " + reason)[:700]
    elif not old:
        item["verificationReason"] = reason[:700]


def set_limited(item: dict[str, object], reason: str) -> None:
    if item.get("health") != "offline":
        item["health"] = "limited"
        item["online"] = True
    append_reason(item, reason)


def set_offline(item: dict[str, object], reason: str) -> None:
    item["health"] = "offline"
    item["online"] = False
    item["error"] = reason[:700]
    item["verificationReason"] = reason[:700]


def refine(url: str, item: dict[str, object]) -> None:
    if item.get("sourceOnline") is not True:
        return
    try:
        status, _, content_type, source = fetch(url)
    except Exception as exc:
        set_limited(item, f"Source content could not be re-verified: {type(exc).__name__}")
        return

    if not (200 <= status < 400) or not source.strip():
        set_offline(item, f"Install source is not readable (HTTP {status})")
        return
    if looks_html(source, content_type):
        set_offline(item, "Install URL returned HTML instead of a Scriptable script")
        return
    if not looks_executable_scriptable(source):
        set_limited(item, "Source is reachable but does not clearly look like an executable Scriptable script")

    markers = expected_html_markers(source)
    setup = auth_or_setup_likely(source)
    checked_deps: list[dict[str, object]] = []

    for dep in literal_requests(source):
        dep_url = str(dep["url"])
        parsed = urllib.parse.urlparse(dep_url)
        if parsed.hostname in {"raw.githubusercontent.com", "github.com", "api.github.com", "gist.githubusercontent.com"}:
            continue
        try:
            dstatus, final_url, dctype, body = fetch(dep_url, "text/html,application/json,text/plain,*/*")
            state: dict[str, object] = {"url": dep_url, "httpStatus": dstatus, "finalUrl": final_url if final_url != dep_url else None}
            checked_deps.append(state)

            if dstatus in (404, 410):
                set_offline(item, f"Runtime dependency is gone: {dep_url} (HTTP {dstatus})")
                continue

            if dep.get("html"):
                if dstatus in (401, 403, 429) and not body.strip():
                    set_limited(item, f"HTML source cannot be verified (HTTP {dstatus}): {dep_url}")
                    continue
                if not (200 <= dstatus < 400):
                    set_limited(item, f"HTML source returned HTTP {dstatus}: {dep_url}")
                    continue
                if not looks_html(body, dctype):
                    set_offline(item, f"Expected HTML source no longer returns HTML: {dep_url}")
                    continue
                if markers and not any(marker_present(body, marker) for marker in markers):
                    set_offline(item, "HTML scraper target changed; expected selector is missing: " + ", ".join(markers[:3]))
                    continue
                if not markers:
                    set_limited(item, "HTML scraper is reachable, but its page structure cannot be verified automatically")

            elif dep.get("json"):
                if dstatus in (401, 403, 429):
                    if setup:
                        # Expected for private/account-bound APIs. This is configuration, not downtime.
                        continue
                    set_limited(item, f"API could not be fully verified (HTTP {dstatus}): {dep_url}")
                elif not (200 <= dstatus < 400):
                    set_limited(item, f"API returned HTTP {dstatus}: {dep_url}")
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 410):
                set_offline(item, f"Runtime dependency is gone: {dep_url} (HTTP {exc.code})")
            elif dep.get("html"):
                set_limited(item, f"HTML source cannot be verified (HTTP {exc.code}): {dep_url}")
            elif setup and exc.code in (401, 403, 405, 429):
                continue
            else:
                set_limited(item, f"Runtime dependency could not be verified (HTTP {exc.code})")
        except Exception as exc:
            set_limited(item, f"Runtime dependency could not be verified safely: {type(exc).__name__}")
        time.sleep(0.03)

    if checked_deps:
        item["deepRuntimeChecks"] = checked_deps


def main() -> None:
    payload = json.loads(STATUS.read_text(encoding="utf-8"))
    items = payload.get("items") or {}
    for url, item in items.items():
        if isinstance(item, dict):
            refine(str(url), item)

    endpoint_healths = [str(item.get("health") or ("online" if item.get("online") else "offline")) for item in items.values() if isinstance(item, dict)]
    payload["endpointsOnline"] = endpoint_healths.count("online")
    payload["endpointsLimited"] = endpoint_healths.count("limited")
    payload["endpointsOffline"] = endpoint_healths.count("offline")

    limited_delta = max(0, payload["endpointsLimited"] - int(payload.get("endpointsLimited") or 0))
    offline_delta = max(0, payload["endpointsOffline"] - int(payload.get("endpointsOffline") or 0))
    if limited_delta or offline_delta:
        payload["deepCheckWarnings"] = limited_delta + offline_delta

    STATUS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Deep community health check: online={payload['endpointsOnline']} limited={payload['endpointsLimited']} offline={payload['endpointsOffline']}")


if __name__ == "__main__":
    main()
