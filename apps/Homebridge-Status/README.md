# Homebridge Status

> **Testing build:** aplikace je zatím záměrně skrytá z veřejného webového katalogu. Instalační soubor zůstává v repozitáři pro soukromé testování.

Homebridge Status je Scriptable widget pro přehled stavu Homebridge v jednotném stylu CaseyCZ Scriptable Apps.

## Hlavní funkce

- zachovává ověřené Homebridge UI API z původního `homebridgeStatusWidget`,
- primární LAN adresa + automatický fallback na druhou VPN adresu,
- při každém novém obnovení se znovu preferuje LAN,
- ukazuje Homebridge, Plugins a Node.js update status,
- CPU load, RAM usage, teplotu CPU, uptime a grafy,
- Small / Medium / Large widget,
- Lock Screen Inline / Circular / Rectangular,
- vzhled, navigace a nastavení sjednocené s Home Dashboardem,
- nastavitelné barvy a motiv widgetu,
- notifikace změn stavu,
- self-update z `Master`,
- heslo uložené v Scriptable Keychain.

## Připojení

V aplikaci otevři **Připojení** a nastav:

1. **Primární adresa (LAN)** – například `http://192.168.1.50:8581`
2. **Záložní adresa (VPN)** – například Tailscale IP / hostname s portem `8581`
3. Homebridge uživatelské jméno a heslo

Skript při každém načtení zkusí nejdřív LAN. Pokud se nepřipojí, automaticky zkusí VPN adresu.

## Staré nastavení

Při prvním spuštění se skript pokusí převzít základní nastavení ze starého `homebridgeStatus/black.json`, pokud soubor existuje. Heslo se po migraci uloží do Keychainu.

## Verze

Aktuální testovací verze: **v0.1.1**
