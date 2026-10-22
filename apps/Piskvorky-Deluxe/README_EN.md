# 🎮 Tic-Tac-Toe Deluxe

An offline 3 × 3 tic-tac-toe game for iPhone, designed for **Scriptable**.

![Version](https://img.shields.io/badge/version-1.1.0-38BDF8)

**[Čeština](README.md)**

## Installation

1. Download **[Piskvorky Deluxe.js](./Piskvorky%20Deluxe.js)**.
2. Save it to **iCloud Drive → Scriptable**, or paste its contents into a new Scriptable script.
3. Run **Piškvorky Deluxe**.

A [.scriptable package](./Piskvorky%20Deluxe.scriptable) is also available. If it opens as JSON code instead of importing as a script, use the **.js** file.

## Features

- 👥 Two-player mode and computer opponent (easy, medium, hard).
- 🦁 Custom player names, emoji and colors.
- 🎨 Three color themes and adjustable board size.
- 🔁 Alternating first player or a fixed starting player.
- 🏆 Separate results per game mode and an option to reset scores.
- 🎉 Winning-line highlight, victory banner and confetti.
- 🔊 Optional game sounds.
- 🔒 Offline gameplay, without accounts or game APIs. Internet is used only for optional update checks; results remain local.

Open **⚙️ Settings** to find the difficulty, sound, appearance and player profiles. When iOS Reduce Motion is enabled, moving celebrations are suppressed but the win banner remains visible.

## Updates

Since **v1.1.0**, the game checks GitHub `version.json` on launch. When a newer version is available, it asks before installing. It downloads and validates the script, creates a backup of the existing `.js` file, then replaces it. Relaunch the game after updating.

The **⚙️ Settings** page shows the app icon, installed version and latest update-check result. Offline gameplay remains available when the version check cannot connect.

Users on v1.0.0 must install v1.1.0 manually once to enable future update checks.

## Notes

- This is an app-like Scriptable script, not a Home Screen widget.
- No dependencies or internet connection required.
- Game logic passed automated tests; behavior should still be checked on a real iPhone.
