from pathlib import Path
import json
import re

ROOT_CZ = Path("README.md")
ROOT_EN = Path("README_EN.md")
SITE = Path("index.html")

APPS = [
    {
        "name": "LockScreen Generator",
        "source": Path("apps/LockScreenGenerator/LockScreenGenerator.js"),
        "version_json": Path("apps/LockScreenGenerator/version.json"),
        "readmes": [Path("apps/LockScreenGenerator/README.md"), Path("apps/LockScreenGenerator/README_EN.md")],
        "site": True,
    },
    {
        "name": "Sports Info",
        "source": Path("apps/Sports-Info/Sports Info.js"),
        "version_json": Path("apps/Sports-Info/version.json"),
        "readmes": [Path("apps/Sports-Info/README.md"), Path("apps/Sports-Info/README_EN.md")],
        "site": True,
    },
    {
        "name": "Sideload Watch",
        "source": Path("apps/Sideload-Watch/Sideload Watch.js"),
        "version_json": Path("apps/Sideload-Watch/version.json"),
        "readmes": [Path("apps/Sideload-Watch/README.md"), Path("apps/Sideload-Watch/README_EN.md")],
        "site": True,
    },
    {
        "name": "Home Dashboard",
        "source": Path("apps/Home-Dashboard/Home Dashboard.js"),
        "version_json": Path("apps/Home-Dashboard/version.json"),
        "readmes": [Path("apps/Home-Dashboard/README.md"), Path("apps/Home-Dashboard/README_EN.md")],
        "site": True,
    },
    {
        "name": "Homebridge Status",
        "source": Path("apps/Homebridge-Status/Homebridge Status.js"),
        "version_json": Path("apps/Homebridge-Status/version.json"),
        "readmes": [Path("apps/Homebridge-Status/README.md"), Path("apps/Homebridge-Status/README_EN.md")],
        "site": False,
    },
]


def version_from_source(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r'const APP_VERSION\s*=\s*["\']([^"\']+)["\']', text)
    if not match:
        raise SystemExit(f"APP_VERSION missing: {path}")
    return match.group(1)


def write_if_changed(path: Path, content: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old != content:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def sync_root(content: str, name: str, version: str) -> str:
    pattern = rf'(<tr><td><strong>{re.escape(name)}</strong></td><td><code>)([^<]+)(</code></td>)'
    content, count = re.subn(pattern, rf'\g<1>v{version}\g<3>', content, count=1)
    if count != 1:
        raise SystemExit(f"Root README row missing: {name}")
    return content


def sync_app_readme(content: str, version: str) -> str:
    replacements = [
        (r'(img\.shields\.io/badge/VERZE-v)[0-9A-Za-z._-]+(-38BDF8)', rf'\g<1>{version}\g<2>'),
        (r'(img\.shields\.io/badge/VERSION-v)[0-9A-Za-z._-]+(-38BDF8)', rf'\g<1>{version}\g<2>'),
        (r'(Aktuální testovací verze:\s*\*\*v)[0-9A-Za-z._-]+(\*\*)', rf'\g<1>{version}\g<2>'),
        (r'(Current testing version:\s*\*\*v)[0-9A-Za-z._-]+(\*\*)', rf'\g<1>{version}\g<2>'),
        (r'(alt="[^"]*\bverze )[0-9A-Za-z._-]+(")', rf'\g<1>{version}\g<2>'),
        (r'(alt="[^"]*\bversion )[0-9A-Za-z._-]+(")', rf'\g<1>{version}\g<2>'),
    ]
    changed = content
    hits = 0
    for pattern, replacement in replacements:
        changed, count = re.subn(pattern, replacement, changed, count=1)
        hits += count
    if hits == 0:
        raise SystemExit("No version marker found in app README")
    return changed


root_cz = ROOT_CZ.read_text(encoding="utf-8")
root_en = ROOT_EN.read_text(encoding="utf-8")
site = SITE.read_text(encoding="utf-8")

versions = {}
for app in APPS:
    version = version_from_source(app["source"])
    versions[app["name"]] = version
    write_if_changed(app["version_json"], json.dumps({"version": version}, ensure_ascii=False, indent=2) + "\n")

    root_cz = sync_root(root_cz, app["name"], version)
    root_en = sync_root(root_en, app["name"], version)

    for readme in app["readmes"]:
        text = readme.read_text(encoding="utf-8")
        write_if_changed(readme, sync_app_readme(text, version))

    if app["site"]:
        pattern = rf"(\{{name:'{re.escape(app['name'])}',version:')[^']+(')"
        site, count = re.subn(pattern, rf'\g<1>{version}\g<2>', site, count=1)
        if count != 1:
            raise SystemExit(f"Website card missing: {app['name']}")

marker = "<!-- App versions are synchronized automatically from APP_VERSION in each production script. -->"
if marker not in root_cz:
    root_cz = root_cz.replace("## Aplikace\n", "## Aplikace\n\n" + marker + "\n", 1)
if marker not in root_en:
    root_en = root_en.replace("## Apps\n", "## Apps\n\n" + marker + "\n", 1)

root_cz = root_cz.replace(
    "Homebridge monitoring s LAN → VPN fallbackem, vlastním vzhledem, notifikacemi a více velikostmi widgetu.",
    "Testovací Homebridge monitoring s LAN → VPN fallbackem, vlastním vzhledem, notifikacemi a více velikostmi widgetu.",
)
root_en = root_en.replace(
    "Homebridge monitoring with automatic LAN → VPN fallback, customizable appearance, notifications and multiple widget sizes.",
    "Testing Homebridge monitor with automatic LAN → VPN fallback, customizable appearance, notifications and multiple widget sizes.",
)

write_if_changed(ROOT_CZ, root_cz)
write_if_changed(ROOT_EN, root_en)
write_if_changed(SITE, site)

for name, version in versions.items():
    print(f"{name}: v{version}")
