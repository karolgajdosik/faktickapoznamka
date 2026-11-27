// Parliament week by week: every ISO week with at least one vote gets a summary.
import { votes, speeches, mpById, dayKey, isFinal, lawTitle, CHAIR, NEZ, type Vote, type Mp } from "./data";

export interface Week {
  key: string;              // "2026-W48"
  year: number; week: number;
  from: string; to: string; // first and last day with a vote (YYYY-MM-DD)
  days: string[];
  sessions: number[];
  votes: Vote[];            // newest first
  passed: number; failed: number;
  attendance: number | null;
  finals: Vote[];           // final votes on bills (passed or not)
  close: Vote[];            // narrowest results
  absent: { m: Mp; n: number; of: number }[];
  rebels: { m: Mp; n: number }[];
  talkers: { m: Mp; sec: number; n: number }[];
}

function isoWeek(day: string) {
  const d = new Date(day + "T12:00:00Z");
  const dow = (d.getUTCDay() + 6) % 7;            // Monday = 0
  d.setUTCDate(d.getUTCDate() - dow + 3);         // Thursday decides the year
  const y = d.getUTCFullYear();
  const jan4 = new Date(Date.UTC(y, 0, 4));
  const w = 1 + Math.round(((d.getTime() - jan4.getTime()) / 86400000 - 3 + ((jan4.getUTCDay() + 6) % 7)) / 7);
  return { y, w, key: `${y}-W${String(w).padStart(2, "0")}` };
}

/** How many MPs would have had to vote differently to flip the result (a bill needs a majority of those present). */
export const margin = (v: Vote) => {
  const present = 150 - v.counts["0"], needed = Math.floor(present / 2) + 1;
  return v.passed ? v.counts.Z - needed + 1 : needed - v.counts.Z;
};

const clubMajority = (v: Vote) => {
  const tally = new Map<string, Record<string, number>>();
  for (const [id, c] of Object.entries(v.votes)) {
    if (c !== "Z" && c !== "P" && c !== "?") continue;
    const cl = v.clubs?.[id] ?? mpById.get(id)?.club; if (!cl || cl === NEZ) continue;
    const t = tally.get(cl) ?? {}; t[c] = (t[c] ?? 0) + 1; tally.set(cl, t);
  }
  const out = new Map<string, string>();
  for (const [cl, t] of tally) { const s = Object.entries(t).sort((a, b) => b[1] - a[1]); if (s[0] && (!s[1] || s[0][1] > s[1][1])) out.set(cl, s[0][0]); }
  return out;
};

export const weeks: Week[] = (() => {
  const by = new Map<string, Vote[]>();
  for (const v of votes) { const k = isoWeek(dayKey(v.datetime)).key; (by.get(k) ?? by.set(k, []).get(k)!).push(v); }
  const talkBy = new Map<string, Map<string, { sec: number; n: number }>>();
  for (const s of speeches) {
    if (s.kind === CHAIR || !s.mpId) continue;
    const k = isoWeek(dayKey(s.start)).key;
    const m = talkBy.get(k) ?? talkBy.set(k, new Map()).get(k)!;
    const t = m.get(s.mpId) ?? { sec: 0, n: 0 }; t.sec += s.dur; t.n++; m.set(s.mpId, t);
  }
  return [...by.entries()].map(([key, vs]) => {
    const { y, w } = isoWeek(dayKey(vs[0].datetime));
    const days = [...new Set(vs.map((v) => dayKey(v.datetime)))].sort();
    let seats = 0, here = 0;
    const abs = new Map<string, [number, number]>(), reb = new Map<string, number>();
    for (const v of vs) {
      const mj = clubMajority(v);
      for (const [id, c] of Object.entries(v.votes)) {
        seats++; if (c !== "0") here++;
        const a = abs.get(id) ?? [0, 0]; a[1]++; if (c === "0") a[0]++; abs.set(id, a);
        const cl = v.clubs?.[id] ?? mpById.get(id)?.club; const m = cl ? mj.get(cl) : undefined;
        if (m && (c === "Z" || c === "P" || c === "?") && c !== m) reb.set(id, (reb.get(id) ?? 0) + 1);
      }
    }
    const withVotes = vs.filter((v) => v.passed !== null);
    return {
      key, year: y, week: w, from: days[0], to: days[days.length - 1], days,
      sessions: [...new Set(vs.map((v) => v.session).filter((s): s is number => s != null))].sort((a, b) => a - b),
      votes: vs, passed: vs.filter((v) => v.passed).length, failed: vs.filter((v) => v.passed === false).length,
      attendance: seats ? here / seats : null,
      finals: vs.filter(isFinal),
      close: withVotes.filter((v) => margin(v) > 0).sort((a, b) => margin(a) - margin(b)).slice(0, 3),
      absent: [...abs.entries()].filter(([id, [n]]) => n > 0 && mpById.has(id)).map(([id, [n, of]]) => ({ m: mpById.get(id)!, n, of })).sort((a, b) => b.n - a.n || a.m.sortName.localeCompare(b.m.sortName, "sk")).slice(0, 8),
      rebels: [...reb.entries()].filter(([id]) => mpById.has(id)).map(([id, n]) => ({ m: mpById.get(id)!, n })).sort((a, b) => b.n - a.n).slice(0, 8),
      talkers: [...(talkBy.get(key) ?? new Map()).entries()].filter(([id]) => mpById.has(id)).map(([id, t]) => ({ m: mpById.get(id)!, ...t })).sort((a, b) => b.sec - a.sec).slice(0, 5),
    };
  }).sort((a, b) => b.key.localeCompare(a.key));
})();

export const weekByKey = new Map(weeks.map((w) => [w.key, w]));
export const latestWeek = weeks[0];
export const weekLabel = (w: Week) => {
  const f = new Date(w.from + "T12:00:00Z"), t = new Date(w.to + "T12:00:00Z");
  const d = (x: Date, o: Intl.DateTimeFormatOptions) => x.toLocaleDateString("sk-SK", { timeZone: "UTC", ...o });
  if (w.from === w.to) return d(f, { day: "numeric", month: "long", year: "numeric" });
  return f.getUTCMonth() === t.getUTCMonth()
    ? `${f.getUTCDate()}. – ${d(t, { day: "numeric", month: "long", year: "numeric" })}`
    : `${d(f, { day: "numeric", month: "long" })} – ${d(t, { day: "numeric", month: "long", year: "numeric" })}`;
};
export { lawTitle };
