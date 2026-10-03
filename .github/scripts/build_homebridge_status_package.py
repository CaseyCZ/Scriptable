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

entry = (
    "      {name:'Homebridge Status',version:'" + version + "',icon:'🏠',"
    "file:'./apps/Homebridge-Status/Homebridge%20Status.js',"
    "install:'./apps/Homebridge-Status/Homebridge%20Status.scriptable',"
    "preview:'https://raw.githubusercontent.com/homebridge/branding/latest/logos/homebridge-silhouette-round-white.png',"
    "tags:['Homebridge','Monitoring','LAN / VPN','Widgets'],"
    "description:{cs:'Homebridge monitoring s automatickým LAN → VPN fallbackem, stavem aktualizací a vlastním vzhledem.',"
    "en:'Homebridge monitoring with automatic LAN → VPN fallback, update status and customizable appearance.'},"
    "features:{cs:['LAN → VPN fallback bez ruční změny adresy','Homebridge, pluginy a Node.js update stav','CPU, RAM, teplota, uptime a grafy','Small / Medium / Large + Lock Screen'],"
    "en:['LAN → VPN fallback without changing the address manually','Homebridge, plugins and Node.js update status','CPU, RAM, temperature, uptime and charts','Small / Medium / Large + Lock Screen']}}"
)

site = SITE.read_text(encoding="utf-8")
block_match = re.search(r"(const ourApps=\[\n)(.*?)(\n    \];)", site, re.S)
assert block_match, "ourApps block missing in index.html"
body = block_match.group(2)

if "{name:'Homebridge Status'" in body:
    body, count = re.subn(
        r"\s*\{name:'Homebridge Status'[^\n]*\}",
        "\n" + entry,
        body,
        count=1,
    )
    assert count == 1, "Homebridge Status card update failed"
else:
    body = body.rstrip()
    if body and not body.endswith(","):
        body += ","
    body += "\n" + entry

site = site[:block_match.start()] + block_match.group(1) + body + block_match.group(3) + site[block_match.end():]
SITE.write_text(site, encoding="utf-8")

print(f"Homebridge Status v{version} synchronized:")
print(f"- {SRC}")
print(f"- {PACKAGE}")
print(f"- {SITE}")
