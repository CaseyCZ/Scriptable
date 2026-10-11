from pathlib import Path
import json
import re

APP_DIR = Path("apps/Sports-Live")
SRC = APP_DIR / "Sports Live.js"
PACKAGE = APP_DIR / "Sports Live.scriptable"
VERSION_JSON = APP_DIR / "version.json"

script = SRC.read_text(encoding="utf-8")
assert 'const APP_NAME = "Sports Live";' in script
version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script)
assert version_match, "APP_VERSION missing from Sports Live.js"
version = version_match.group(1)

package = {
    "always_run_in_app": False,
    "icon": {"color": "orange", "glyph": "trophy"},
    "name": "Sports Live",
    "script": script,
    "share_sheet_inputs": [],
}
PACKAGE.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
VERSION_JSON.write_text(json.dumps({"version": version}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"Sports Live v{version} package synchronized")
