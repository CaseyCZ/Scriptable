# 🏆 Sports Info

**Sports Info v2.5.9 — Production** je univerzální sportovní widget pro Scriptable se zachovaným původním rozhraním a online sportovními daty.

## Sporty

- ⚽ Fotbal — Chance Liga, Premier League, LaLiga, Bundesliga, Serie A, Ligue 1, Liga mistrů a Evropská liga
- 🏒 Hokej — NHL, Tipsport Extraliga, SHL, Liiga, National League, CHL, MS a NCAA
- 🏀 Basketbal — NBA, WNBA, EuroLeague, EuroCup, NBL, ACB, BBL, LNB a NCAA
- 🥅 Florbal — česká, švédská, finská a švýcarská liga + MS IFF
- ⚾ Baseball — MLB, česká Extraliga, NPB, KBO, LMB a NCAA

## Online data a automatická obnova

Sports Info načítá při spuštění widgetu aktuální online data. Ruční tlačítko **Update** není určeno pro výsledky nebo tabulky — aktualizuje pouze samotný kód aplikace.

Widget požádá iOS o další obnovu podle situace:

- 🔴 **LIVE zápas:** za 2 minuty
- ⏱️ **zápas začíná do 30 minut:** za 5 minut
- 🕒 **běžný stav:** podle intervalu nastaveného uživatelem

`refreshAfterDate` určuje nejdřívější požadovaný čas obnovy; skutečný okamžik spuštění widgetu řídí iOS.

Cache slouží pouze jako nouzová záloha při výpadku internetu nebo datového zdroje.

## Template a funkce

- Small widget: loga zůstávají zachovaná a název týmu se může zalomit až na 2 řádky
- Large widget: tabulka dynamicky využívá volné místo a přitom drží bezpečný limit řádků

- původní moderní tmavé nastavení ve stylu LockScreen Generatoru
- Small / Medium / Large náhled přímo z nastavení
- výběr sportu, soutěže a oblíbeného týmu
- přehledné **Nastavení widgetu** s vysvětlením každé volby a doporučeným presetem
- automatické přizpůsobení obsahu pro Small / Medium / Large
- live stav, poslední a příští zápasy, tabulka a forma
- samostatná sekce **API a zdroje**
- samostatná **Diagnostika** zdroje, týmů, tabulky a cache
- **Záloha a údržba** — export/import, vymazání cache, částečný i úplný reset
- fail-open: nastavení se otevře i bez internetu; widget použije cache pouze při výpadku online zdroje
- migrace starého `FootballInfo_settings.json` při prvním spuštění Sports Info
- CZ / EN / DE / ES
- aktualizace kódu přímo ze Scriptable

## Datové zdroje

Sports Info používá veřejné zdroje bez osobního API klíče. Fotbal používá OneFootball s ESPN a FotMob fallbackem. NHL, WNBA/NBA, NCAA a MLB používají ESPN. Evropské a další vybrané hokejové, basketbalové, florbalové a baseballové soutěže používají veřejná data z Livesportu.

Livesport integrace nevyužívá oficiální veřejné API; čte veřejná data vložená do stránky soutěže. Proto zůstává zapnutá cache/fail-open logika. Pokud zdroj neposkytne tabulku ve stejném veřejném feedu, diagnostika to zobrazí informativně jako `0 rows`, nikoli jako chybu zdroje.

Ve výchozím stavu není potřeba žádný API klíč. SportsAPI Pro zůstává v pokročilém nastavení jako volitelný zdroj s vlastním klíčem.

## Instalace

- [`Sports Info.scriptable`](./Sports%20Info.scriptable)
- [`Sports Info.js`](./Sports%20Info.js)

> Runtime zůstává v jednom souboru `Sports Info.js`.
