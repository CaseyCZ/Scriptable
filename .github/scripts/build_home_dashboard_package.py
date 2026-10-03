from pathlib import Path
import json
import re

APP_DIR = Path("apps/Home-Dashboard")
SRC = APP_DIR / "Home Dashboard.js"
PACKAGE = APP_DIR / "Home Dashboard.scriptable"
SITE = Path("index.html")

script = SRC.read_text(encoding="utf-8")
assert 'const APP_NAME = "Home Dashboard";' in script
version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script)
assert version_match, "APP_VERSION missing from Home Dashboard.js"
version = version_match.group(1)

package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "house"},
    "name": "Home Dashboard",
    "script": script,
    "share_sheet_inputs": [],
}
PACKAGE.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")

site = SITE.read_text(encoding="utf-8")
site, count = re.subn(
    r"(\{name:'Home Dashboard',version:')[^']+(')",
    lambda m: f"{m.group(1)}{version}{m.group(2)}",
    site,
    count=1,
)
assert count == 1, "Home Dashboard card missing in index.html"
site, count = re.subn(
    r"(\{name:'Home Dashboard'[^\n]*?install:')[^']+(')",
    lambda m: f"{m.group(1)}./apps/Home-Dashboard/Home%20Dashboard.scriptable{m.group(2)}",
    site,
    count=1,
)
assert count == 1, "Home Dashboard install path missing in index.html"
SITE.write_text(site, encoding="utf-8")

print(f"Home Dashboard v{version} synchronized:")
print(f"- {SRC}")
print(f"- {PACKAGE}")
print(f"- {SITE}")
