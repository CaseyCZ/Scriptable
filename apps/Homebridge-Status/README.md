# Homebridge Status

Homebridge Status je Scriptable widget pro přehled stavu Homebridge v jednotném stylu CaseyCZ Scriptable Apps.

![Homebridge Status preview](./Homebridge%20Status.jpg)

## Co aplikace umí

**Homebridge Status** ti ukáže, jak se daří tvému Homebridge. Z iPhonu můžeš rychle zkontrolovat, zda běží, jak je vytížený a jestli jsou dostupné aktualizace.

## Co uvidíš

- 🟢 Stav připojení a dostupnost Homebridge.
- 🔄 Dostupné aktualizace Homebridge, pluginů a Node.js.
- 📊 Využití procesoru a paměti, teplotu, dobu provozu a grafy.
- 📱 Widgety na plochu i zamykací obrazovku.
- 🎨 Nastavitelné barvy a vzhled.
- 🔔 Upozornění na změny stavu.
- 🔄 Aktualizace aplikace přímo ze Scriptable.

## Jak začít

1. Nainstaluj **Homebridge Status** do Scriptable a spusť jej.
2. Otevři **Připojení** a zadej adresu svého Homebridge, například `http://192.168.1.50:8581`.
3. Vyplň přihlašovací údaje k Homebridge.
4. Pokud používáš vzdálený přístup, můžeš zadat také záložní adresu, například přes Tailscale.
5. Vyber vzhled a přidej widget Scriptable na plochu iPhonu.

## Jak funguje připojení

Aplikace se nejprve pokusí spojit s Homebridge přes domácí síť. Pokud to nejde a máš nastavenou záložní adresu, zkusí ji automaticky. Při dalším obnovení opět nejprve vyzkouší domácí připojení.

## Dobré vědět

K používání potřebuješ funkční Homebridge a přístup k jeho webovému rozhraní. Heslo se ukládá do zabezpečeného úložiště Scriptable. Pokud jsi používal starší verzi widgetu, aplikace se při prvním spuštění pokusí převzít její základní nastavení.

## Původ a poděkování

Projekt vychází z [homebridgeStatusWidget](https://github.com/lwitzani/homebridgeStatusWidget) od [lwitzani](https://github.com/lwitzani). Původní řešení posloužilo jako základ; současná aplikace má přepracované rozhraní a rozšířené funkce.

## Verze

Aktuální verze: **v0.1.13**


