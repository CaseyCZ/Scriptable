from pathlib import Path
import json

app = Path("apps/LockScreenGenerator")
src = app / "LockScreenGenerator.js"
out = app / "LockScreenGenerator.scriptable"

script = src.read_text(encoding="utf-8")
package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "magic"},
    "name": "LockScreen Generator",
    "script": script,
    "share_sheet_inputs": [],
}

out.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Built {out} from {src} ({len(script)} chars)")
