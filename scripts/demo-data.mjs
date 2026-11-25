// Generates clearly FICTIONAL demo data so the site can be built before the
// first real scrape. Names are invented on purpose — never fake votes for real people.
import { mkdirSync, writeFileSync, rmSync } from "node:fs";

let seed = 42;
const rnd = () => ((seed = (seed * 1664525 + 1013904223) % 2 ** 32) / 2 ** 32);
const pick = (a) => a[Math.floor(rnd() * a.length)];

const first = ["Anna","Ján","Mária","Peter","Eva","Martin","Zuzana","Tomáš","Katarína","Michal","Lucia","Juraj","Jana","Marek","Veronika"];
const last = [["Vzorový","Vzorová"],["Ukážkový","Ukážková"],["Pokusný","Pokusná"],["Šablónsky","Šablónska"],["Fiktívny","Fiktívna"],["Makétový","Maketová"],["Skúšobný","Skúšobná"],["Náhradný","Náhradná"],["Modelový","Modelová"],["Testovský","Testovská"],["Prototypný","Prototypná"],["Náčrtový","Náčrtová"]];
const fem = new Set(["Anna","Mária","Eva","Zuzana","Katarína","Lucia","Jana","Veronika"]);
const clubs = [["Klub A",42],["Klub B",30],["Klub C",25],["Klub D",20],["Klub E",15],["Klub F",10],["Nezaradení",8]];

const combos = [];
for (const f of first) for (const l of last) combos.push([f, fem.has(f) ? l[1] : l[0]]);
combos.sort(() => rnd() - 0.5);

const mps = [];
let i = 0;
for (const [club, n] of clubs) for (let k = 0; k < n; k++) {
  const [f, l] = combos[i++];
  mps.push({ id: String(1000 + i), name: `${f} ${l}`, sortName: `${l} ${f}`, club });
}

rmSync("data/votes", { recursive: true, force: true });
mkdirSync("data/votes", { recursive: true });
const kinds = ["návrh zákona ako celok","pozmeňujúci návrh z rozpravy","prerokovanie v druhom čítaní","návrh uznesenia","pridelenie výborom"];
const start = Date.parse("2026-11-03T11:00:00+01:00");
for (let v = 1; v <= 40; v++) {
  const id = 50000 + v;
  const leaning = Object.fromEntries(clubs.map(([c]) => [c, pick(["Z","Z","P","?"])]));
  const votes = {}; const counts = { Z: 0, P: 0, "?": 0, N: 0, "0": 0 };
  for (const mp of mps) {
    const r = rnd();
    const code = r < 0.07 ? "0" : r < 0.09 ? "N" : r < 0.93 ? leaning[mp.club] : pick(["Z","P","?"]);
    votes[mp.id] = code; counts[code]++;
  }
  const present = 150 - counts["0"];
  writeFileSync(`data/votes/${id}.json`, JSON.stringify({
    id: String(id), session: 60 + Math.floor((v - 1) / 14), number: v,
    datetime: new Date(start + v * 37 * 60 * 1000 + Math.floor(v / 8) * 86400000).toISOString(),
    title: `Ukážkové hlasovanie č. ${v}: ${pick(kinds)} (tlač ${1400 + v})`,
    tlac: String(1400 + v), passed: counts.Z > present / 2, counts, votes,
  }, null, 1));
}
writeFileSync("data/mps.json", JSON.stringify(mps, null, 1));
writeFileSync("data/meta.json", JSON.stringify({ demo: true, term: 9, updatedAt: new Date().toISOString(), lastVoteId: null }, null, 1));
console.log(`demo: ${mps.length} MPs, 40 votes`);
