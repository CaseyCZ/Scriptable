# Homebridge Status

Homebridge Status is a Scriptable widget for monitoring Homebridge in the shared CaseyCZ Scriptable Apps style.

## What it does

**Homebridge Status** gives you a quick view of your Homebridge from your iPhone. See whether it is running, how busy it is and whether updates are available.

## What you can see

- 🟢 Homebridge availability and connection status.
- 🔄 Available Homebridge, plugin and Node.js updates.
- 📊 Processor and memory usage, temperature, uptime and charts.
- 📱 Home Screen and Lock Screen widgets.
- 🎨 Custom colors and appearance.
- 🔔 Notifications when the status changes.
- 🔄 In-app updates through Scriptable.

## Getting started

1. Install **Homebridge Status** in Scriptable and open it.
2. Open **Connection** and enter your Homebridge address, for example `http://192.168.1.50:8581`.
3. Enter your Homebridge sign-in details.
4. Optionally add a second address for remote access, such as Tailscale.
5. Choose your appearance and add a Scriptable widget to your iPhone.

## How the connection works

The app tries your home network first. If that connection fails and you configured a backup address, it automatically tries the second one. On the next refresh, it checks the home connection first again.

## Good to know

You need a working Homebridge installation and access to its web interface. Your password is kept in Scriptable's secure storage. On first launch, the app also attempts to carry over basic settings from an older version of the widget.

## Origin and credits

Based on [homebridgeStatusWidget](https://github.com/lwitzani/homebridgeStatusWidget) by [lwitzani](https://github.com/lwitzani). The original project provided the foundation; this version has a redesigned interface and additional features.

## Version

Current version: **v0.1.13**


