# Scriptable Apps — Community Catalog Compliance

Last reviewed: 2026-10-08

This document describes how the Scriptable Apps community catalog handles third-party projects. It is an engineering and attribution record, not legal advice.

## Policy

- The catalog stores **metadata only** for third-party projects: project name, author, category, description, tags, source link, preview link and direct install URL.
- Third-party JavaScript is **not copied into this repository, mirrored, modified, bundled or re-hosted** by the catalog.
- The **Install** action fetches the original public script URL supplied by the original author/project and prepares it for Scriptable on the user's device.
- The **Project** action links to the original repository or project page.
- Preview images remain hosted by the original project or by GitHub where possible. The catalog does not claim ownership of third-party screenshots, names, logos or source code.
- Availability checks may request public install URLs to verify that the referenced script is still reachable. The result is stored only as availability metadata (online/offline, HTTP status, check time and error text).
- The catalog contains an automated duplicate audit. Duplicate install URLs and duplicate `author + name` identities block deployment.
- Multiple files that are variants of one project may be grouped into one catalog card when they belong to the same project family.
- A listing does **not** imply affiliation, endorsement, sponsorship or ownership.

## Licenses and attribution

Each third-party project remains governed by the license, terms and documentation published by its original author. Inclusion in this catalog does not change or replace that license.

Where a project does not publish an explicit license, the catalog still links only to the original public source and does not relicense or redistribute the source code.

Projects used as a starting point for CaseyCZ's own Scriptable apps are credited separately in the corresponding app README files and in the root README.

## Installation and user responsibility

Third-party Scriptable scripts can request network access and may access data exposed to them by Scriptable or by services configured by the user. Before running a community script, users should review the original project page, setup requirements and source code when appropriate.

Some projects require API keys, accounts, local configuration, Shortcuts, companion services or other dependencies. The catalog's Online status confirms only that the referenced install endpoint is reachable; it does not guarantee that the project still works with every external service.

## Availability and removals

Dead install URLs are not considered release-ready. When a project disappears upstream, the catalog will either:

1. update the install URL if the original author has moved the script, or
2. remove the project from the active catalog if no usable original script remains.

Maintainers can request attribution corrections, link updates or removal by opening an issue in this repository.

## Automated checks

The public catalog is guarded by:

- `tools/audit-community-catalog.cjs` — duplicate and variant audit,
- `tools/update_community_status.py` — third-party install endpoint availability,
- GitHub Actions — catalog audit before Pages deployment,
- CodeQL — repository code scanning.

The generated `data/community-status.json` file is the authoritative current availability snapshot.
