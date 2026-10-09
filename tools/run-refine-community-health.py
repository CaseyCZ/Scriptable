#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "data" / "community-status.json"
MAX_WORKERS = 16


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def needs_deep_check(item: dict[str, object]) -> bool:
    if item.get("sourceOnline") is not True:
        return False
    score = int(item.get("scriptableScore") or 0)
    # Setup requirements and helper modules are not failures by themselves.
    # Deep-check only actual runtime dependencies or suspiciously weak sources.
    return bool(item.get("runtimeDependencies") or score <= 1)


def main() -> None:
    refine_mod = load_module(ROOT / "tools" / "refine-community-health.py", "community_refine")
    updater_mod = load_module(ROOT / "tools" / "update_community_status.py", "community_updater")

    payload = json.loads(STATUS.read_text(encoding="utf-8"))
    items = payload.get("items") or {}
    candidates = [(str(url), item) for url, item in items.items() if isinstance(item, dict) and needs_deep_check(item)]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(refine_mod.refine, url, item) for url, item in candidates]
        for future in as_completed(futures):
            future.result()

    def health(item: dict[str, object]) -> str:
        return str(item.get("health") or ("online" if item.get("online") else "offline"))

    endpoint_healths = [health(item) for item in items.values() if isinstance(item, dict)]
    payload["endpointsTotal"] = len(endpoint_healths)
    payload["endpointsOnline"] = endpoint_healths.count("online")
    payload["endpointsLimited"] = endpoint_healths.count("limited")
    payload["endpointsOffline"] = endpoint_healths.count("offline")

    projects = updater_mod.collect_projects()
    project_states: list[str] = []
    for project in projects:
        states = [health(items[url]) for url in project.get("files", []) if url in items and isinstance(items[url], dict)]
        if not states:
            project_states.append("offline")
        elif "online" in states:
            project_states.append("online")
        elif "limited" in states:
            project_states.append("limited")
        else:
            project_states.append("offline")

    payload["total"] = len(project_states)
    payload["online"] = project_states.count("online")
    payload["limited"] = project_states.count("limited")
    payload["offline"] = project_states.count("offline")
    payload["deepCheckCandidates"] = len(candidates)
    payload["deepCheckWarnings"] = payload["limited"] + payload["offline"]

    STATUS.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Deep checked {len(candidates)} suspicious endpoint(s): "
        f"projects online={payload['online']} limited={payload['limited']} offline={payload['offline']}; "
        f"endpoints online={payload['endpointsOnline']} limited={payload['endpointsLimited']} offline={payload['endpointsOffline']}"
    )


if __name__ == "__main__":
    main()
