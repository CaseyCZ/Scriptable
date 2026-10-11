from pathlib import Path
import json
import re

APP_DIR = Path("apps/LockScreenGenerator")
SRC = APP_DIR / "LockScreenGenerator.js"
PACKAGE = APP_DIR / "LockScreenGenerator.scriptable"

script = SRC.read_text(encoding="utf-8")
version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script)
assert version_match, "APP_VERSION missing from LockScreenGenerator.js"
version = version_match.group(1)

package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "magic"},
    "name": "LockScreen Generator",
    "script": script,
    "share_sheet_inputs": [],
}
PACKAGE.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"LockScreen Generator v{version} package synchronized")
