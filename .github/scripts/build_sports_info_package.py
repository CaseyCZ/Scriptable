from pathlib import Path
import json
import re

app = Path("apps/Sports-Info")
src = app / "Sports Info.js"
out = app / "Sports Info.scriptable"
script = src.read_text(encoding="utf-8")
assert re.search(r'const APP_VERSION\s*=\s*"[^"]+"', script)
assert 'const APP_NAME = "Sports Info";' in script
package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "trophy"},
    "name": "Sports Info",
    "script": script,
    "share_sheet_inputs": [],
}
out.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Built {out} from {src} ({len(script)} chars)")
