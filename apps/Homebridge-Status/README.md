# Homebridge Status

Scriptable widget pro sledování Homebridge postavený na ověřené API logice původního `homebridgeStatusWidget`, ale s rozhraním a nastavením sjednoceným s ostatními CaseyCZ Scriptable Apps.

## Funkce

- stav Homebridge, Homebridge verze, pluginů a Node.js
- CPU load, teplota CPU, RAM a uptime
- grafy CPU a RAM
- Small, Medium a Large widget
- Lock Screen: Inline, Circular a Rectangular
- vlastní vzhled, motivy a barvy
- nastavitelný refresh a timeout
- notifikace při výpadku nebo dostupné aktualizaci
- heslo uložené v Scriptable Keychain
- automatická migrace základního nastavení ze starého `homebridgeStatus/black.json`
- vlastní updater skriptu

## LAN → VPN fallback

V nastavení lze zadat dvě adresy:

1. **Primární adresa (LAN)** – například `http://192.168.1.50:8581`
2. **Záložní adresa (VPN)** – například Tailscale/VPN adresa `http://100.x.x.x:8581`

Při každém spuštění nebo obnovení widgetu se vždy nejdříve zkusí LAN adresa. Pokud není dostupná, skript automaticky zkusí VPN adresu. Není tedy potřeba ručně měnit Homebridge URL při odchodu z domácí sítě.

Medium a Large widget mohou zobrazit, zda právě používají `LAN` nebo `VPN`.

## Nastavení

Spusť skript přímo v Scriptable. Otevře se nastavení ve stylu ostatních CaseyCZ widgetů:

- **Připojení** – LAN/VPN URL, uživatel, heslo, HTTPS
- **Náhled widgetu** – náhled všech podporovaných velikostí
- **Vzhled widgetu** – motiv, barvy a viditelné údaje
- **Chování** – refresh, timeout a ignorované update kontroly
- **Notifikace** – výpadky, aktualizace a recovery zprávy
- **Aktualizace** – kontrola a instalace nové verze skriptu

## Ignorování aktualizací

Do pole `Ignorovat aktualizace` lze zadat přesné npm názvy pluginů oddělené čárkou. Podporované jsou také speciální hodnoty:

- `HOMEBRIDGE_UTD`
- `NODEJS_UTD`

## Původ

Homebridge API části vycházejí z projektu `homebridgeStatusWidget` od lwitzani. Uživatelské rozhraní, fallback, nastavení, widget layouty a updater jsou upravené pro CaseyCZ Scriptable Apps.
