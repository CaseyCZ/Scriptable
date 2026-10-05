# Homebridge Status

> **Testing build:** the app is intentionally hidden from the public website catalog for now. The install package remains in the repository for private testing.

Homebridge Status is a Scriptable widget for monitoring Homebridge in the shared CaseyCZ Scriptable Apps style.

## Main features

- keeps the proven Homebridge UI API logic from the original `homebridgeStatusWidget`,
- primary LAN address with automatic fallback to a second VPN address,
- LAN is preferred again on every new refresh,
- Homebridge, Plugins and Node.js update status,
- CPU load, RAM usage, CPU temperature, uptime and charts,
- Small / Medium / Large widgets,
- Lock Screen Inline / Circular / Rectangular,
- settings appearance and navigation aligned with Home Dashboard,
- customizable widget colors and themes,
- status notifications,
- self-update from `Master`,
- password stored in Scriptable Keychain.

## Connection

Open **Connection** in the app and configure:

1. **Primary address (LAN)** – for example `http://192.168.1.50:8581`
2. **Fallback address (VPN)** – for example a Tailscale IP / hostname with port `8581`
3. Homebridge username and password

Each refresh tries LAN first. If it cannot connect, the VPN address is tried automatically.

## Legacy settings

On first launch the script attempts to migrate the main settings from the old `homebridgeStatus/black.json`, if it exists. The migrated password is stored in Keychain.

## Version

Current testing version: **v0.1.13**
