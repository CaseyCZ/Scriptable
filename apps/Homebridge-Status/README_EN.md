# Homebridge Status

A Scriptable widget for monitoring Homebridge. It keeps the proven Homebridge API logic from the original `homebridgeStatusWidget`, while using the settings, visual style and update flow of the CaseyCZ Scriptable Apps collection.

## Features

- Homebridge running state, Homebridge version, plugins and Node.js status
- CPU load, CPU temperature, RAM usage and uptime
- CPU and RAM charts
- Small, Medium and Large widgets
- Lock Screen Inline, Circular and Rectangular widgets
- customizable appearance, themes and colors
- configurable refresh interval and request timeout
- notifications for outages and available updates
- password stored in Scriptable Keychain
- automatic migration of basic settings from the old `homebridgeStatus/black.json`
- built-in script updater

## LAN → VPN fallback

Two Homebridge addresses can be configured:

1. **Primary address (LAN)** – for example `http://192.168.1.50:8581`
2. **Fallback address (VPN)** – for example a Tailscale/VPN address such as `http://100.x.x.x:8581`

On every run or widget refresh the script always tries the LAN address first. Only when the LAN address is unavailable does it automatically try the VPN address. You therefore do not need to change the Homebridge URL when you leave your home network.

Medium and Large widgets can show whether the current connection is using `LAN` or `VPN`.

## Settings

Run the script directly in Scriptable to open its settings:

- **Connection** – LAN/VPN URL, username, password and HTTPS behavior
- **Widget preview** – previews of all supported widget families
- **Appearance** – theme, colors and visible information
- **Behavior** – refresh interval, timeout and ignored update checks
- **Notifications** – outages, updates and recovery notifications
- **Update** – check for and install a newer script version

## Ignoring updates

The `Ignored updates` field accepts exact npm plugin names separated by commas. It also supports these special values:

- `HOMEBRIDGE_UTD`
- `NODEJS_UTD`

## Origin

The Homebridge API portions are based on the `homebridgeStatusWidget` project by lwitzani. The settings UI, fallback logic, widget layouts and updater are adapted for CaseyCZ Scriptable Apps.
