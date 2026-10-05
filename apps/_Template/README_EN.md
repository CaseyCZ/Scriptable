# CaseyCZ Scriptable Template

Shared starter template for new Scriptable apps in `CaseyCZ/Scriptable`.

The template is not intended as a standalone end-user product. It is the baseline for new apps so settings, appearance, updates, backups and behavior stay consistent across the CaseyCZ Scriptable collection.

## Included

- shared CaseyCZ WebView visual system based on Home Dashboard / Sports Info / Sports Live
- hero with app name, version and update check
- Small / Medium / Large preview
- common screens: `App`, `Widget appearance`, `Behavior`, `APIs & sources`, `Diagnostics`, `Backup & maintenance`, `Help`
- automatic settings saving
- separate `APP_VERSION` and `SETTINGS_VERSION`
- settings migration framework
- feature flags through `FEATURES`
- selectable `local` / `icloud` storage
- CS / EN / DE / ES translations with first-run language choice
- custom colors with color picker + HEX
- Scriptable Keychain support for secrets through `SECRET_KEYS`
- JSON file backup/import with secrets excluded
- shared diagnostic states: `checking / ok / warning / error / off`
- updater using `version.json`, cache busting and downloaded-source validation
- automatic backup of the previous JS before an update
- build workflow for the `.scriptable` package

## Creating a new app

1. Copy `apps/_Template` into a new app folder.
2. Rename `CaseyCZ Template.js` and change `APP_NAME`, `APP_SLUG`, icon metadata and update URLs.
3. Configure `FEATURES` for the app.
4. Adjust `DEFAULTS` and replace the sample `App` screen with app-specific settings.
5. Never place sensitive values directly in settings. Add their keys to `SECRET_KEYS` and store them in Scriptable Keychain.
6. Increase `SETTINGS_VERSION` when the settings schema changes and add a migration. Normal releases use `APP_VERSION`.
7. Copy/adapt the template build workflow for the new app.

## Recommended settings order

1. Hero + Update
2. Widget preview
3. app-specific settings
4. Widget appearance
5. Behavior
6. APIs & sources when needed
7. Diagnostics
8. Backup & maintenance
9. Help

## Shared colors

| Element | Color |
| --- | --- |
| root | `#070B14` |
| background | `#0B1020` |
| panel | `#111827` |
| secondary panel | `#172033` |
| border | `#2A3850` |
| text | `#F8FAFC` |
| muted | `#94A3B8` |
| accent | `#38BDF8` |
| OK | `#34C759` |
| warning | `#FF9F0A` |
| error | `#FF453A` |

## Backup format

```json
{
  "format": "CaseyCZ.Scriptable.Backup",
  "schema": 1,
  "app": "App Name",
  "appVersion": "1.0.0",
  "settingsVersion": 1,
  "exportedAt": "2026-10-05T12:00:00.000Z",
  "settings": {}
}
```

Secrets stored in Keychain are never included in the backup.

## Build

`.github/workflows/build-caseycz-template-package.yml` validates JavaScript syntax, synchronizes `version.json`, builds the `.scriptable` package and verifies package/source parity.

The workflow only commits files under `apps/_Template`; it does not modify existing apps.
