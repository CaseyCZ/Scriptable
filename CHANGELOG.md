# Changelog

All notable public changes to Scriptable Apps are documented here.

## October 2026 updates — 2026-10-23

### New games for Scriptable

- Added **Piškvorky Deluxe v1.1.0**: local two-player tic-tac-toe, AI difficulty levels, player profiles, statistics and in-app update checks.
- Added **Breakout Deluxe v1.2.0**: touch-controlled brick breaker with scores, levels, lives, themes and update checks.
- Added **Pong Fotbal v1.1.0**: portrait football Pong, AI and local two-player modes, match settings and updates.
- Standardized the three games' Scriptable install packages and Czech/English READMEs.

### Catalog and release documentation

- Added the new games to the Scriptable Apps catalog and root README tables.
- Matched the project-link badges and game preview style across the catalog.
- Repaired release metadata synchronization to use the actual `assets/js/index-page.js` catalog data, including the three games and existing apps.
- Updated the Sideload Watch catalog version to **v0.2.26**.
- Added an attribution to [CodeGuppy](https://codeguppy.com/games/) for inspiration behind Breakout Deluxe.

## 1.0.0 — 2026-10-08

### Public catalog

- Launched the Scriptable Apps web catalog with CaseyCZ apps and a large curated third-party Scriptable library.
- Added responsive grid/list layouts, dark/light appearance, language switching and mobile-friendly navigation.
- Added iOS-Hub-style filters for availability, category, sorting and search.
- Added direct Scriptable installation flow while keeping third-party source code hosted by the original authors.
- Added original project links and attribution for community entries.

### Community quality controls

- Added scheduled Online/Offline checks for community install endpoints.
- Added deployment-blocking duplicate checks for install URLs and `author + name` identities.
- Added variant detection for projects that expose multiple related script files.
- Merged duplicate/variant listings such as F1 Scriptable Widget, Countdown Widget, Quote Widget and Blend into clearer single-project cards with variants where appropriate.
- Removed or repaired dead community install links during the 1.0 release audit.

### CaseyCZ apps

- LockScreen Generator
- Sports Info
- Sideload Watch
- Home Dashboard
- Homebridge Status
- Sports Live

Each app keeps its own version, README and project-specific release history where applicable.

### Documentation and governance

- Added Czech and English project documentation.
- Added `SECURITY.md`, `CONTRIBUTING.md`, MIT `LICENSE` and this changelog.
- Added `COMPLIANCE.md` describing third-party catalog handling, attribution, availability checks and non-rehosting policy.
- Added a public Getting Started guide for new Scriptable users.
- Added explicit cookie consent before Google Analytics is loaded.

### Credits

Projects derived from or inspired by existing public Scriptable work credit the relevant original authors in their app README files and in the root README.
