from pathlib import Path
import json
import re

APP_DIR = Path("apps/Homebridge-Status")
SRC = APP_DIR / "Homebridge Status.js"
PACKAGE = APP_DIR / "Homebridge Status.scriptable"
SITE = Path("index.html")

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

# Keep the app in the repository while it is being tested, but do not expose it
# in the public website catalog yet.
site = SITE.read_text(encoding="utf-8")
block_match = re.search(r"(const ourApps=\[\n)(.*?)(\n    \];)", site, re.S)
assert block_match, "ourApps block missing in index.html"
body = block_match.group(2)
body, _ = re.subn(
    r"\n?\s*\{name:'Homebridge Status'[^\n]*\},?",
    "",
    body,
    count=1,
)
body = re.sub(r",\s*$", "", body.rstrip())
site = site[:block_match.start()] + block_match.group(1) + body + block_match.group(3) + site[block_match.end():]
SITE.write_text(site, encoding="utf-8")

print(f"Homebridge Status v{version} synchronized (private testing):")
print(f"- {SRC}")
print(f"- {PACKAGE}")
print("- public website card hidden")
