#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
EXTRA = ROOT / "community-extra.js"
OUTPUT = ROOT / "data" / "community-status.json"
USER_AGENT = "CaseyCZ-Scriptable-Catalog (+https://caseycz.github.io/Scriptable/)"
MAX_WORKERS = 12
TIMEOUT = 15


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

    index_text = INDEX.read_text(encoding="utf-8")
    try:
        community_block = index_text.split("const communityApps=[", 1)[1].split("];\n    communityApps.push", 1)[0]
    except IndexError as exc:
        raise RuntimeError("Unable to locate communityApps in index.html") from exc

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


def probe(item: dict[str, str]) -> tuple[str, dict[str, object]]:
    url = item["file"]
    checked_at = now_iso()
    last_error = None
    last_status = None

    for attempt in range(2):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "text/plain,*/*",
                    "Range": "bytes=0-1023",
                    "Cache-Control": "no-cache",
                },
            )
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                status = getattr(response, "status", 200)
                sample = response.read(1024)
            if 200 <= status < 400 and sample.strip():
                return url, {
                    "name": item["name"],
                    "online": True,
                    "checkedAt": checked_at,
                    "httpStatus": status,
                    "error": None,
                }
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
        "checkedAt": checked_at,
        "httpStatus": last_status,
        "error": (last_error or "Unknown error")[:300],
    }


def main() -> None:
    projects = collect_projects()
    if not projects:
        raise SystemExit("No community download URLs found")

    endpoints: dict[str, dict[str, str]] = {}
    for project in projects:
        for url in project["files"]:
            endpoints.setdefault(url, {"name": str(project["name"]), "file": url})

    results: dict[str, dict[str, object]] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(probe, item) for item in endpoints.values()]
        for future in as_completed(futures):
            url, status = future.result()
            results[url] = status

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
        "items": dict(sorted(results.items())),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Checked {len(projects)} community projects / {len(results)} download endpoints: "
        f"{project_online} projects online, {project_offline} offline"
    )


if __name__ == "__main__":
    main()
