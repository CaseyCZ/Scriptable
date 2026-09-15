from pathlib import Path
import json
import re

APP_DIR = Path("apps/Sports-Info")
SRC = APP_DIR / "Sports Info.js"
PACKAGE = APP_DIR / "Sports Info.scriptable"
APP_README = APP_DIR / "README.md"
ROOT_README = Path("README.md")
SITE = Path("index.html")

script = SRC.read_text(encoding="utf-8")
assert 'const APP_NAME = "Sports Info";' in script
version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script)
assert version_match, "APP_VERSION missing from Sports Info.js"
version = version_match.group(1)

# 1) Installable package always contains the exact production JS.
package = {
    "always_run_in_app": False,
    "icon": {"color": "deep-blue", "glyph": "trophy"},
    "name": "Sports Info",
    "script": script,
    "share_sheet_inputs": [],
}
PACKAGE.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")

# 2) App README version comes from APP_VERSION.
app_readme = APP_README.read_text(encoding="utf-8")
app_readme, count = re.subn(
    r'(\*\*Sports Info v)[^ ]+( — Production\*\*)',
    lambda m: f"{m.group(1)}{version}{m.group(2)}",
    app_readme,
    count=1,
)
assert count == 1, "Sports Info version marker missing in app README"
APP_README.write_text(app_readme, encoding="utf-8")

# 3) Repository README version comes from APP_VERSION.
root_readme = ROOT_README.read_text(encoding="utf-8")
root_readme, count = re.subn(
    r'(\| 🏆 \*\*Sports Info\*\* \| ✅ v)[^ |]+( \|)',
    lambda m: f"{m.group(1)}{version}{m.group(2)}",
    root_readme,
    count=1,
)
assert count == 1, "Sports Info row missing in root README"
ROOT_README.write_text(root_readme, encoding="utf-8")

# 4) GitHub Pages card version comes from APP_VERSION.
site = SITE.read_text(encoding="utf-8")
site, count = re.subn(
    r"(\{name:'Sports Info',version:')[^']+(')",
    lambda m: f"{m.group(1)}{version}{m.group(2)}",
    site,
    count=1,
)
assert count == 1, "Sports Info card missing in index.html"
SITE.write_text(site, encoding="utf-8")

print(f"Sports Info v{version} synchronized:")
print(f"- {SRC}")
print(f"- {PACKAGE}")
print(f"- {APP_README}")
print(f"- {ROOT_README}")
print(f"- {SITE}")
