export type Code = "Z" | "P" | "?" | "N" | "0";
export interface Mp {
  id: string; name: string; sortName: string; club: string;
  title?: string | null; party?: string | null; born?: string | null; city?: string | null; region?: string | null;
}
export interface Vote {
  id: string; session: number | null; number: number | null; datetime: string;
  title: string; tlac: string | null; passed: boolean | null;
  counts: Record<Code, number>; votes: Record<string, Code>; clubs?: Record<string, string>;
}
export interface Meta { demo: boolean; term: number; updatedAt: string }

import mpsJson from "../../data/mps.json";
import metaJson from "../../data/meta.json";
import liveJson from "../../data/live.json";
const voteFiles = import.meta.glob<{ default: Vote }>("../../data/votes/*.json", { eager: true });

export const meta = metaJson as Meta;
export const live = liveJson as { item: string | null; since: string | null };
export const CODES: Code[] = ["Z", "P", "?", "N", "0"];
export const LABEL: Record<Code, string> = { Z: "Za", P: "Proti", "?": "Zdržal sa", N: "Nehlasoval", "0": "Neprítomný" };
export const cls = (c: Code) => (c === "?" ? "Q" : c === "0" ? "O" : c);

/** "Prezentácia" = attendance check, not a decision on anything: excluded from lists and stats. */
export const isPresence = (v: Vote) => /^prezentácia\.?$/i.test(v.title.trim());
const allVotes = Object.values(voteFiles).map((m) => m.default);
export const votes = allVotes.filter((v) => !isPresence(v))
  .sort((a, b) => b.datetime.localeCompare(a.datetime) || Number(b.id) - Number(a.id));
export const voteById = new Map(votes.map((v) => [v.id, v]));

const mpList = mpsJson as Mp[];
export const mpById = new Map(mpList.map((m) => [m.id, m]));
/** Current members = those listed in the most recent vote. */
export const currentIds = new Set(Object.keys(votes[0]?.votes ?? {}));
export const mps = mpList.filter((m) => currentIds.has(m.id)).sort((a, b) => a.sortName.localeCompare(b.sortName, "sk"));
export const formerMps = mpList.filter((m) => !currentIds.has(m.id)).sort((a, b) => a.sortName.localeCompare(b.sortName, "sk"));
export const NEZ = "Nezaradení";

/** Clubs ordered by current size. Size ordering is deliberately neutral — no left/right placement. */
export const clubs = (() => {
  const n = new Map<string, number>();
  for (const m of mps) n.set(m.club, (n.get(m.club) ?? 0) + 1);
  return [...n.entries()].sort((a, b) => (a[0] === NEZ ? 1 : b[0] === NEZ ? -1 : b[1] - a[1]))
    .map(([name, size]) => ({ name, size }));
})();
// Neutral categorical palette assigned by club size (not party branding).
const PALETTE = ["#6ea8fe", "#f4a261", "#5fd3b0", "#c3a6ff", "#f6d06f", "#ef8fb3", "#7fd4f5", "#b9c98a", "#e48f8f"];
export const clubColor = (name: string) => {
  if (name === NEZ) return "#9aa4b6";
  const i = clubs.findIndex((c) => c.name === name);
  return PALETTE[(i < 0 ? clubs.length : i) % PALETTE.length];
};

const clubOf = (v: Vote, id: string) => v.clubs?.[id] ?? mpById.get(id)?.club ?? "";

/* ---------- precomputed statistics (once per build) ---------- */
export interface MpStats {
  total: number; present: number; attendance: number | null; loyalty: number | null;
  rebels: string[]; monthly: { month: string; total: number; present: number }[]; rankAttendance: number;
}
export const stats = new Map<string, MpStats>();
(() => {
  const acc = new Map<string, { total: number; present: number; comp: number; withClub: number; rebels: string[]; months: Map<string, [number, number]> }>();
  for (const v of votes) {
    // majority position of each club in this vote
    const tally = new Map<string, Record<string, number>>();
    for (const [id, c] of Object.entries(v.votes)) {
      if (c !== "Z" && c !== "P" && c !== "?") continue;
      const cl = clubOf(v, id); if (!cl || cl === NEZ) continue;
      const t = tally.get(cl) ?? {}; t[c] = (t[c] ?? 0) + 1; tally.set(cl, t);
    }
    const major = new Map<string, string>();
    for (const [cl, t] of tally) {
      const s = Object.entries(t).sort((a, b) => b[1] - a[1]);
      if (s[0] && (!s[1] || s[0][1] > s[1][1])) major.set(cl, s[0][0]);
    }
    const month = v.datetime.slice(0, 7);
    for (const [id, c] of Object.entries(v.votes)) {
      const a = acc.get(id) ?? { total: 0, present: 0, comp: 0, withClub: 0, rebels: [], months: new Map() };
      a.total++; if (c !== "0") a.present++;
      const mo = a.months.get(month) ?? [0, 0]; mo[0]++; if (c !== "0") mo[1]++; a.months.set(month, mo);
      const mj = major.get(clubOf(v, id));
      if (mj && (c === "Z" || c === "P" || c === "?")) { a.comp++; if (c === mj) a.withClub++; else a.rebels.push(v.id); }
      acc.set(id, a);
    }
  }
  for (const [id, a] of acc) stats.set(id, {
    total: a.total, present: a.present,
    attendance: a.total ? a.present / a.total : null,
    loyalty: a.comp ? a.withClub / a.comp : null,
    rebels: a.rebels, rankAttendance: 0,
    monthly: [...a.months.entries()].sort().map(([month, [total, present]]) => ({ month, total, present })),
  });
  const ranked = mps.map((m) => m.id).sort((x, y) => (stats.get(y)?.attendance ?? 0) - (stats.get(x)?.attendance ?? 0));
  ranked.forEach((id, i) => { const s = stats.get(id); if (s) s.rankAttendance = i + 1; });
})();
export const mpStats = (id: string) => stats.get(id) ?? { total: 0, present: 0, attendance: null, loyalty: null, rebels: [], monthly: [], rankAttendance: 0 };

/* ---------- sessions ---------- */
export interface Session { n: number; votes: Vote[]; days: string[]; from: string; to: string; passed: number; failed: number; attendance: number }
export const sessions: Session[] = (() => {
  const by = new Map<number, Vote[]>();
  for (const v of votes) if (v.session != null) by.set(v.session, [...(by.get(v.session) ?? []), v]);
  return [...by.entries()].map(([n, vs]) => {
    const asc = vs.slice().sort((a, b) => a.datetime.localeCompare(b.datetime));
    const days = [...new Set(asc.map((v) => dayKey(v.datetime)))];
    const att = asc.reduce((s, v) => s + (150 - v.counts["0"]) / 150, 0) / asc.length;
    return { n, votes: asc, days, from: asc[0].datetime, to: asc[asc.length - 1].datetime,
      passed: asc.filter((v) => v.passed).length, failed: asc.filter((v) => v.passed === false).length, attendance: att };
  }).sort((a, b) => b.to.localeCompare(a.to));
})();

/* ---------- formatting ---------- */
const TZ = "Europe/Bratislava";
export function dayKey(iso: string) { return new Date(iso).toLocaleDateString("sv-SE", { timeZone: TZ }); }
export const fmtDate = (iso: string) => new Date(iso).toLocaleDateString("sk-SK", { day: "numeric", month: "long", year: "numeric", timeZone: TZ });
export const fmtShort = (iso: string) => new Date(iso).toLocaleDateString("sk-SK", { day: "numeric", month: "numeric", year: "numeric", timeZone: TZ });
export const fmtDay = (iso: string) => new Date(iso).toLocaleDateString("sk-SK", { weekday: "long", day: "numeric", month: "long", timeZone: TZ });
export const fmtTime = (iso: string) => new Date(iso).toLocaleTimeString("sk-SK", { hour: "2-digit", minute: "2-digit", timeZone: TZ });
/** Percent; keeps one decimal near the ends so 99.6 % is not shown as 100 %. */
export const pct = (x: number | null) => {
  if (x === null) return "–";
  const v = x * 100;
  return (v > 99 && v < 100) || (v > 0 && v < 1) ? `${v.toFixed(1).replace(".", ",")} %` : `${Math.round(v)} %`;
};
/** Slovak plural: plural(5, "hlasovanie", "hlasovania", "hlasovaní") */
export const plural = (n: number, one: string, few: string, many: string) => (n === 1 ? one : n >= 2 && n <= 4 ? few : many);
export const resultText = (v: Vote) => (v.passed === null ? "Bez výsledku" : v.passed ? "Schválené" : "Neschválené");
export const resultCls = (v: Vote) => (v.passed ? "yes" : v.passed === false ? "no" : "");
export const initials = (m: Mp) => {
  const [last, first] = [m.sortName.split(" ")[0], m.name.split(" ")[0]];
  return (first[0] + last[0]).toUpperCase();
};
export const age = (born?: string | null) => {
  if (!born) return null;
  const b = new Date(born), n = new Date();
  return n.getFullYear() - b.getFullYear() - (n < new Date(n.getFullYear(), b.getMonth(), b.getDate()) ? 1 : 0);
};
/** "Vládny návrh zákona, ktorým … (tlač 29) - tretie čítanie." → short label for dense lists */
export const shortTitle = (t: string, max = 140) => (t.length > max ? t.slice(0, max - 1).replace(/\s+\S*$/, "") + "…" : t);
