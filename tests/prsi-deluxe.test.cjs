const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '../apps/Prsi-Deluxe/Prsi Deluxe.js'), 'utf8');
const opening = source.indexOf('const engine = (() => {');
const closing = source.indexOf('// ENGINE END', opening);
if (opening < 0 || closing < 0) throw new Error('Nelze najít samostatná pravidla Prší');
const engineSource = source.slice(opening, closing);
const engine = vm.runInNewContext(engineSource + '\nengine;', {});

test('balíček .scriptable obsahuje totožný samostatný skript', () => {
  const bundle = JSON.parse(fs.readFileSync(path.join(__dirname, '../apps/Prsi-Deluxe/Prsi Deluxe.scriptable'), 'utf8'));
  const version = JSON.parse(fs.readFileSync(path.join(__dirname, '../apps/Prsi-Deluxe/version.json'), 'utf8'));
  assert.equal(bundle.script, source);
  assert.equal(bundle.name, 'Prší Deluxe');
  assert.equal(source.match(/const APP_VERSION = "(.*?)"/)[1], version.version);
});

test('Scriptable obsahuje syntakticky platný HTML herní skript', () => {
  const scriptStart = source.indexOf('<script>');
  const scriptEnd = source.indexOf('</script>', scriptStart);
  assert.ok(scriptStart > 0 && scriptEnd > scriptStart);
  const browserScript = source.slice(scriptStart + '<script>'.length, scriptEnd)
    .replace('__INITIAL_STATE__', '{}');
  assert.doesNotThrow(() => new vm.Script(browserScript));
  assert.ok(source.includes('new WebView()'));
  assert.ok(source.includes('await view.present(true)'));
});

function fixture({ hand0 = ['hearts-7'], hand1 = ['bells-7'], top = 'hearts-8', current = 0, pending = null } = {}) {
  const cards = engine.deck();
  const get = id => cards.find(card => card.id === id);
  const excluded = new Set([...hand0, ...hand1, top]);
  return {
    stock: cards.filter(card => !excluded.has(card.id)),
    discard: [get(top)],
    hands: [hand0.map(get), hand1.map(get)],
    current,
    activeSuit: get(top).suit,
    pending,
    winner: null,
    history: [],
  };
}

test('32 různých karet a rozdání po čtyřech', () => {
  assert.equal(new Set(engine.deck().map(c => c.id)).size, 32);
  for (let n = 0; n < 80; n++) {
    const game = engine.start();
    assert.equal(game.hands[0].length, 4);
    assert.equal(game.hands[1].length, 4);
    assert.equal(game.stock.length, 23);
    assert.equal(game.discard.length, 1);
    assert.ok(!['7', 'A', 'O'].includes(engine.top(game).rank));
  }
});

test('lze položit stejnou hodnotu nebo barvu, nikoliv jinou', () => {
  const game = fixture({ hand0: ['hearts-9', 'bells-8', 'acorns-K'] });
  assert.equal(engine.canPlay(game, game.hands[0][0]), true);
  assert.equal(engine.canPlay(game, game.hands[0][1]), true);
  assert.equal(engine.canPlay(game, game.hands[0][2]), false);
});

test('sedmička načte +2, další sedmička navýší +4', () => {
  const game = fixture({ hand0: ['hearts-7', 'hearts-K'], hand1: ['bells-7', 'acorns-9'] });
  assert.equal(engine.play(game, 0, 'hearts-7'), true);
  assert.equal(game.pending.count, 2);
  assert.equal(engine.canPlay(game, game.hands[1][1]), false);
  assert.equal(engine.play(game, 1, 'bells-7'), true);
  assert.equal(game.pending.count, 4);
  assert.equal(engine.draw(game, 0).count, 4);
  assert.equal(game.pending, null);
  assert.equal(game.current, 1);
});

test('eso přeskočí tah a lze ho přebít dalším esem', () => {
  const game = fixture({ hand0: ['hearts-A','hearts-K'], hand1: ['bells-A','bells-8'] });
  assert.equal(engine.play(game, 0, 'hearts-A'), true);
  assert.equal(game.pending.type, 'ace');
  assert.equal(engine.play(game, 1, 'bells-8'), false);
  assert.equal(engine.play(game, 1, 'bells-A'), true);
  assert.equal(game.pending.type, 'ace');
  assert.equal(engine.draw(game, 0).type, 'skip');
  assert.equal(game.current, 1);
});

test('svršek jde na libovolnou běžnou kartu, vybírá barvu', () => {
  const game = fixture({ hand0: ['acorns-O', 'hearts-K'], hand1: ['leaves-7', 'bells-9'] });
  assert.equal(engine.play(game, 0, 'acorns-O'), false, 'bez výběru barvy se karta nesmí odehrát');
  assert.equal(engine.play(game, 0, 'acorns-O', 'leaves'), true);
  assert.equal(game.activeSuit, 'leaves');
  assert.equal(engine.canPlay(game, game.hands[1][0]), true);
  assert.equal(engine.canPlay(game, game.hands[1][1]), false);
});

test('svršek nemůže přebít nevyřešenou sedmičku nebo eso', () => {
  for (const pending of [{ type: 'seven', count: 2 }, { type: 'ace' }]) {
    const game = fixture({ hand0: ['acorns-O'], pending });
    assert.equal(engine.play(game, 0, 'acorns-O', 'hearts'), false);
  }
});

test('běžné dobírání je povoleno jen bez hratelné karty a končí tah', () => {
  const game = fixture({ hand0: ['acorns-K', 'acorns-A'] });
  assert.equal(engine.draw(game, 0).count, 1);
  assert.equal(game.current, 1);
  const canPlay = fixture({ hand0: ['hearts-9'] });
  assert.equal(engine.draw(canPlay, 0), null);
});

test('dobírací balíček se doplní z odhazovacího, vrchní karta zůstane', () => {
  const game = fixture({ hand0: ['acorns-K'], hand1: ['bells-7'], top: 'hearts-8' });
  game.discard = [game.stock.pop(), game.stock.pop(), game.discard[0]];
  game.stock = [];
  const last = engine.top(game).id;
  assert.equal(engine.draw(game, 0).count, 1);
  assert.equal(engine.top(game).id, last);
  assert.equal(game.discard.length, 1);
  assert.equal(game.stock.length, 1);
});

test('poslední zahranou kartou hráč vyhrává', () => {
  const game = fixture();
  assert.equal(engine.play(game, 0, 'hearts-7'), true);
  assert.equal(game.winner, 0);
  assert.equal(engine.draw(game, 1), null);
});

test('AI volí pouze legální tahy a reaguje na dobírání i eso', () => {
  for (const difficulty of ['easy', 'normal', 'hard']) {
    for (let i = 0; i < 80; i++) {
      const game = engine.start(Math.random, 1);
      const move = engine.aiMove(game, difficulty);
      if (move.type === 'play') {
        assert.ok(engine.legal(game, 1).some(card => card.id === move.id));
        assert.equal(engine.play(game, 1, move.id, move.chosenSuit), true);
      } else {
        assert.ok(['skip', 'draw'].includes(move.type));
        assert.ok(engine.draw(game, 1));
      }
    }
  }
});

test('desítky celých partií skončí a během tahů se žádná karta neztratí', () => {
  for (let round = 0; round < 60; round++) {
    const game = engine.start(Math.random, round % 2);
    for (let turn = 0; game.winner === null && turn < 2000; turn++) {
      const player = game.current;
      const playable = engine.legal(game, player);
      if (player === 1) {
        const move = engine.aiMove(game, 'hard');
        if (move.type === 'play') assert.equal(engine.play(game, 1, move.id, move.chosenSuit), true);
        else assert.ok(engine.draw(game, 1));
      } else if (playable.length) {
        const card = playable[0];
        const rest = game.hands[0].filter(other => other.id !== card.id);
        assert.equal(engine.play(game, 0, card.id, card.rank === 'O' ? engine.bestSuit(rest) : null), true);
      } else {
        assert.ok(engine.draw(game, 0));
      }
      const all = [...game.stock, ...game.discard, ...game.hands[0], ...game.hands[1]];
      assert.equal(all.length, 32);
      assert.equal(new Set(all.map(card => card.id)).size, 32);
    }
    assert.ok(game.winner === 0 || game.winner === 1, 'Partie má skončit vítězem');
  }
});
