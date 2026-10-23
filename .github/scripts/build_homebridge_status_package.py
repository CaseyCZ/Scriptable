from pathlib import Path
import json
import re

APP_DIR = Path("apps/Homebridge-Status")
SRC = APP_DIR / "Homebridge Status.js"
PACKAGE = APP_DIR / "Homebridge Status.scriptable"
SITE = Path("assets/js/index-page.js")

script = SRC.read_text(encoding="utf-8")
assert 'const APP_NAME = "Homebridge Status";' in script
version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script)
assert version_match, "APP_VERSION missing from Homebridge Status.js"
version = version_match.group(1)

package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "house"},
    "name": "Homebridge Status",
    "script": script,
    "share_sheet_inputs": [],
}
PACKAGE.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")

# Keep the already-public Homebridge Status card in the catalog.
site = SITE.read_text(encoding="utf-8")
site, count = re.subn(
    r"(\{name:'Homebridge Status',version:')[^']+(')",
    lambda m: f"{m.group(1)}{version}{m.group(2)}",
    site,
    count=1,
)
assert count == 1, "Homebridge Status card missing in assets/js/index-page.js"
site, count = re.subn(
    r"(\{name:'Homebridge Status'[^\n]*?install:')[^']+(')",
    lambda m: f"{m.group(1)}./apps/Homebridge-Status/Homebridge%20Status.scriptable{m.group(2)}",
    site,
    count=1,
)
assert count == 1, "Homebridge Status install path missing in catalog"
SITE.write_text(site, encoding="utf-8")

print(f"Homebridge Status v{version} synchronized:")
print(f"- {SRC}")
print(f"- {PACKAGE}")
print(f"- {SITE}")
