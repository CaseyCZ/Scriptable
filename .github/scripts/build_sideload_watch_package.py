from pathlib import Path
import json
import re

APP_DIR = Path("apps/Sideload-Watch")
SRC = APP_DIR / "Sideload Watch.js"
PACKAGE = APP_DIR / "Sideload Watch.scriptable"

script = SRC.read_text(encoding="utf-8")
assert 'const APP_NAME = "Sideload Watch";' in script
version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script)
assert version_match, "APP_VERSION missing from Sideload Watch.js"
version = version_match.group(1)

package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "download"},
    "name": "Sideload Watch",
    "script": script,
    "share_sheet_inputs": [],
}
PACKAGE.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Sideload Watch v{version} package synchronized")
