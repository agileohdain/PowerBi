#!/usr/bin/env node
/**
 * Smoke test d'une maquette Power BI générée par le skill `powerbi-prototype`.
 *
 * Exécute le JavaScript inline de la maquette dans Node, avec un DOM et
 * ECharts simulés, puis :
 *   - appelle `renderPage()` (si défini) et vérifie qu'il ne lève pas d'exception ;
 *   - vérifie que la rangée de KPI et la zone de visuels ne sont pas vides ;
 *   - parcourt toutes les sous-pages via `go(page, sub)` (si `NAV`/`go` existent) ;
 *   - exécute chaque vue de `VIEWS` avec `aggregates()` (si présents).
 *
 * Usage :  node smoke-test.js <chemin/vers/index.html>
 * Sortie : exit code 0 = OK, 1 = au moins un échec, 2 = mauvaise invocation.
 *
 * Pourquoi ce test existe : une seule erreur JS fatale (ReferenceError,
 * réassignation d'une `const`, identifiant mal orthographié) rend la page
 * vide dans le navigateur — la navigation s'affiche mais ni les KPI ni les
 * visuels. Ce test le détecte mécaniquement avant livraison.
 */
const fs = require('fs');

const target = process.argv[2];
if (!target) {
  console.error('usage: node smoke-test.js <chemin/vers/index.html>');
  process.exit(2);
}
if (!fs.existsSync(target)) {
  console.error('FAIL: fichier introuvable: ' + target);
  process.exit(1);
}

const html = fs.readFileSync(target, 'utf8');
// Ne capture que les <script> inline (sans attribut src=...).
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .map(m => m[1])
  .filter(s => s.trim());
if (!scripts.length) {
  console.error('FAIL: aucun <script> inline trouvé dans ' + target);
  process.exit(1);
}
const js = scripts[scripts.length - 1];

/* ---------- DOM / ECharts stubs ---------- */
const dummyParent = {
  querySelector() { return null; },
  appendChild() {},
};
function makeEl(id) {
  return {
    id,
    innerHTML: '',
    className: '',
    value: '0',
    textContent: '',
    style: {},
    dataset: {},
    parentElement: dummyParent,
    children: [],
    appendChild(c) { this.children.push(c); return c; },
    querySelector() { return null; },
    querySelectorAll() { return []; },
    addEventListener() {},
    removeEventListener() {},
    setAttribute() {},
    getBoundingClientRect() { return { width: 400, height: 300, left: 0, top: 0 }; },
  };
}
const els = {};
global.__els = els;
global.document = {
  getElementById: (id) => (els[id] = els[id] || makeEl(id)),
  createElement: (tag) => makeEl(tag),
  querySelector() { return null; },
  querySelectorAll() { return []; },
  addEventListener() {},
  documentElement: { style: { setProperty() {} } },
  body: makeEl('body'),
};
global.window = {
  addEventListener() {},
  removeEventListener() {},
  innerWidth: 1920,
  innerHeight: 1080,
};
global.getComputedStyle = () => ({
  getPropertyValue: () => '#B69E7F',
});
global.echarts = {
  init: () => ({ setOption() {}, dispose() {}, resize() {}, on() {} }),
};
global.requestAnimationFrame = (fn) => fn();

/* ---------- Exécution + vérifications ---------- */
const testHarness = `
;let __failures = 0;
function __check(name, fn) {
  try { fn(); console.log('PASS  ' + name); }
  catch (e) { __failures++; console.log('FAIL  ' + name + '  →  ' + e.message); }
}
__check('renderPage() ne lève pas d\\'exception', () => {
  if (typeof renderPage !== 'function') throw new Error('renderPage() non défini');
  renderPage();
});
__check('contenu principal rendu (KPI + visuels non vides)', () => {
  // Tolérant aux IDs : chaque génération nomme ses conteneurs différemment.
  // Une maquette vide n'écrit que la navigation (quelques centaines de
  // caractères) ; une maquette complète écrit KPI + visuels (> 2000).
  const total = Object.keys(__els).reduce((s, k) => s + ((__els[k].innerHTML) || '').length, 0);
  if (total < 2000) throw new Error('seulement ' + total + ' caractères rendus — la maquette s\\'afficherait sans KPI ni visuels');
});
if (typeof NAV !== 'undefined' && typeof go === 'function') {
  for (let pi = 0; pi < NAV.length; pi++) {
    const subs = NAV[pi].subs || [];
    for (let si = 0; si < subs.length; si++) {
      __check('navigation go(' + pi + ',' + si + ') → ' + (NAV[pi].name || pi), () => go(pi, si));
    }
  }
}
if (typeof VIEWS !== 'undefined' && typeof aggregates === 'function') {
  const __agg = aggregates();
  for (const k of Object.keys(VIEWS)) {
    __check('VIEWS[' + k + '] s\\'exécute sans exception', () => VIEWS[k](__agg));
  }
}
if (__failures > 0) {
  console.log('\\nSMOKE TEST FAILED : ' + __failures + ' échec(s). NE PAS LIVRER la maquette en l\\'état.');
  process.exit(1);
}
console.log('\\nSMOKE TEST OK — la maquette peut être livrée.');
process.exit(0);
`;

try {
  eval(js + testHarness);
} catch (e) {
  console.log('FAIL  exécution du script de la maquette  →  ' + e.message);
  console.log('\nSMOKE TEST FAILED : le script ne s\'exécute même pas jusqu\'au bout.');
  process.exit(1);
}
