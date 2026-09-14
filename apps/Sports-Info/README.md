# 🏆 Sports Info

**Sports Info v2.2.0** je univerzální sportovní widget pro Scriptable postavený na stejném nastavení/template jako LockScreen Generator.

## Sporty

- ⚽ Fotbal — Chance Liga, Premier League, LaLiga, Bundesliga, Serie A, Ligue 1, Liga mistrů a Evropská liga
- 🏒 Hokej — NHL, Tipsport Extraliga, SHL, Liiga, National League, CHL, MS a NCAA
- 🏀 Basketbal — NBA, WNBA, EuroLeague, EuroCup, NBL, ACB, BBL, LNB a NCAA
- 🥅 Florbal — česká, švédská, finská a švýcarská liga + MS IFF
- ⚾ Baseball — MLB, česká Extraliga, NPB, KBO, LMB a NCAA

## Template a funkce

- moderní tmavé nastavení ve stylu LockScreen Generatoru
- Small / Medium / Large náhled přímo z nastavení
- výběr sportu, soutěže a oblíbeného týmu
- přehledné **Nastavení widgetu** s vysvětlením každé volby a doporučeným presetem
- automatické přizpůsobení obsahu pro Small / Medium / Large
- live stav, poslední a příští zápasy, tabulka a forma
- samostatná sekce **API a zdroje**
- samostatná **Diagnostika** zdroje, týmů, tabulky a cache
- **Záloha a údržba** — export/import, vymazání cache, částečný i úplný reset
- fail-open: nastavení se otevře i bez internetu; widget používá cache, pokud je dostupná
- migrace starého `FootballInfo_settings.json` při prvním spuštění Sports Info
- CZ / EN / DE / ES
- aktualizace přímo ze Scriptable

## Datové zdroje

Sports Info používá veřejné zdroje bez osobního API klíče. Fotbal používá ESPN s FotMob fallbackem. NHL, WNBA/NBA, NCAA a MLB používají ESPN. Evropské a další vybrané hokejové, basketbalové, florbalové a baseballové soutěže používají veřejná data z Livesportu.

Livesport integrace nevyužívá oficiální veřejné API; čte veřejná data vložená do stránky soutěže. Proto zůstává zapnutá cache/fail-open logika. Pokud zdroj neposkytne tabulku ve stejném veřejném feedu, diagnostika to zobrazí informativně jako `0 rows`, nikoli jako chybu zdroje.

Ve výchozím stavu není potřeba žádný API klíč. SportsAPI Pro zůstává v pokročilém nastavení jako volitelný zdroj s vlastním klíčem.

## Instalace

- [`Sports Info.scriptable`](./Sports%20Info.scriptable)
- [`Sports Info.js`](./Sports%20Info.js)

> Runtime zůstává v jednom souboru `Sports Info.js`.