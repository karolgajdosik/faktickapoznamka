// Term-wide statistics for /statistiky/ (computed once per build).
import { votes, clubs, mpById, mps, NEZ, talk, speeches, CHAIR, type Vote } from "./data";

const clubOf = (v: Vote, id: string) => v.clubs?.[id] ?? mpById.get(id)?.club ?? "";
const current = clubs.filter((c) => c.name !== NEZ).map((c) => c.name);

/** Hix agreement index per club: 1 = everyone votes the same, 0 = evenly split. */
export const cohesion = current.map((club) => {
  let sum = 0, n = 0;
  for (const v of votes) {
    const t = { Z: 0, P: 0, Q: 0 };
    for (const [id, c] of Object.entries(v.votes)) if (clubOf(v, id) === club) { if (c === "Z") t.Z++; else if (c === "P") t.P++; else if (c === "?") t.Q++; }
    const tot = t.Z + t.P + t.Q; if (tot < 2) continue;
    const mx = Math.max(t.Z, t.P, t.Q);
    sum += (mx - 0.5 * (tot - mx)) / tot; n++;
  }
  return { club, value: n ? sum / n : null, n };
}).sort((a, b) => (b.value ?? 0) - (a.value ?? 0));

/** Share of votes in which two clubs' majorities took the same position. */
export const agreement = (() => {
  const major = votes.map((v) => {
    const t = new Map<string, Record<string, number>>();
    for (const [id, c] of Object.entries(v.votes)) {
      if (c !== "Z" && c !== "P" && c !== "?") continue;
      const cl = clubOf(v, id); const r = t.get(cl) ?? {}; r[c] = (r[c] ?? 0) + 1; t.set(cl, r);
    }
    const m = new Map<string, string>();
    for (const [cl, r] of t) { const s = Object.entries(r).sort((a, b) => b[1] - a[1]); if (s[0] && (!s[1] || s[0][1] > s[1][1])) m.set(cl, s[0][0]); }
    return m;
  });
  return current.map((a) => current.map((b) => {
    if (a === b) return 1;
    let same = 0, n = 0;
    for (const m of major) { const x = m.get(a), y = m.get(b); if (x && y) { n++; if (x === y) same++; } }
    return n ? same / n : null;
  }));
})();
export const agreementClubs = current;

/** Per month: votes, share passed, average attendance. */
export const monthly = (() => {
  const by = new Map<string, Vote[]>();
  for (const v of votes) { const k = v.datetime.slice(0, 7); by.set(k, [...(by.get(k) ?? []), v]); }
  return [...by.entries()].sort().map(([month, vs]) => ({
    month, n: vs.length,
    passed: vs.filter((v) => v.passed).length / vs.length,
    attendance: vs.reduce((s, v) => s + (150 - v.counts["0"]) / 150, 0) / vs.length,
  }));
})();

export const topTalkers = [...talk.entries()].filter(([id]) => mpById.has(id)).sort((a, b) => b[1].seconds - a[1].seconds).slice(0, 15)
  .map(([id, t]) => ({ m: mpById.get(id)!, t }));
export const topFactual = [...talk.entries()].filter(([id]) => mpById.has(id)).sort((a, b) => b[1].factual - a[1].factual).slice(0, 10)
  .map(([id, t]) => ({ m: mpById.get(id)!, t }));
export const speechTotals = { count: speeches.filter((x) => x.kind !== CHAIR).length, seconds: speeches.filter((x) => x.kind !== CHAIR).reduce((a, x) => a + x.dur, 0) };
export const closeVotes = votes.filter((v) => v.passed !== null && Math.abs(v.counts.Z - (150 - v.counts["0"]) / 2) <= 3).slice(0, 10);
export const failed = votes.filter((v) => v.passed === false).length;
export { mps };
