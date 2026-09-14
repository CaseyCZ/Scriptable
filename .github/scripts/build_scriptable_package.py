from pathlib import Path
import json
import re

APP_DIR = Path("apps/LockScreenGenerator")
SRC = APP_DIR / "LockScreenGenerator.js"
PACKAGE = APP_DIR / "LockScreenGenerator.scriptable"
APP_README = APP_DIR / "README.md"
ROOT_README = Path("README.md")
SITE = Path("index.html")

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

app_readme = APP_README.read_text(encoding="utf-8")
app_readme, count = re.subn(
    r'version-[0-9.]+-0284c7',
    f'version-{version}-0284c7',
    app_readme,
    count=1,
)
assert count == 1, "LockScreen version badge missing in app README"
APP_README.write_text(app_readme, encoding="utf-8")

root_readme = ROOT_README.read_text(encoding="utf-8")
root_readme, count = re.subn(
    r'(\| 🪄 \*\*LockScreen Generator\*\* \| ✅ v)[^ |]+( \|)',
    lambda m: f"{m.group(1)}{version}{m.group(2)}",
    root_readme,
    count=1,
)
assert count == 1, "LockScreen row missing in root README"
ROOT_README.write_text(root_readme, encoding="utf-8")

site = SITE.read_text(encoding="utf-8")
site, count = re.subn(
    r"(\{name:'LockScreen Generator',version:')[^']+(')",
    lambda m: f"{m.group(1)}{version}{m.group(2)}",
    site,
    count=1,
)
assert count == 1, "LockScreen card missing in index.html"
SITE.write_text(site, encoding="utf-8")

print(f"LockScreen Generator v{version} synchronized:")
print(f"- {SRC}")
print(f"- {PACKAGE}")
print(f"- {APP_README}")
print(f"- {ROOT_README}")
print(f"- {SITE}")
