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


def js_strings(text: str) -> list[str]:
    out: list[str] = []
    pattern = re.compile(r"'((?:\\.|[^'\\])*)'|\"((?:\\.|[^\"\\])*)\"")
    for match in pattern.finditer(text):
        raw = match.group(1) if match.group(1) is not None else match.group(2)
        raw = raw.replace("\\/", "/").replace("\\'", "'").replace('\\"', '"').replace("\\\\", "\\")
        out.append(raw)
    return out


def collect_items() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []

    index_text = INDEX.read_text(encoding="utf-8")
    try:
        community_block = index_text.split("const communityApps=[", 1)[1].split("];\n    communityApps.push", 1)[0]
    except IndexError as exc:
        raise RuntimeError("Unable to locate communityApps in index.html") from exc

    object_pattern = re.compile(r"\{name:(['\"])(.*?)\1.*?file:(['\"])(.*?)\3.*?\}", re.S)
    for match in object_pattern.finditer(community_block):
        items.append({"name": match.group(2), "file": match.group(4)})

    extra_text = EXTRA.read_text(encoding="utf-8")
    for line in extra_text.splitlines():
        if "communityItem(" not in line:
            continue
        chunk = line.split("communityItem(", 1)[1]
        values = js_strings(chunk)
        if len(values) >= 5:
            items.append({"name": values[0], "file": values[4]})

    dedup: dict[str, dict[str, str]] = {}
    for item in items:
        url = item["file"].strip()
        if not url.startswith(("https://", "http://")):
            continue
        dedup.setdefault(url, item)

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
    items = collect_items()
    if not items:
        raise SystemExit("No community download URLs found")

    results: dict[str, dict[str, object]] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(probe, item) for item in items]
        for future in as_completed(futures):
            url, status = future.result()
            results[url] = status

    online = sum(1 for item in results.values() if item.get("online") is True)
    offline = len(results) - online
    payload = {
        "generatedAt": now_iso(),
        "total": len(results),
        "online": online,
        "offline": offline,
        "items": dict(sorted(results.items())),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Checked {len(results)} community projects: {online} online, {offline} offline")


if __name__ == "__main__":
    main()
