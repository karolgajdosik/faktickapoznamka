// Data beyond votes and debates (scraper/extra.py): MP activity, committees, changes,
// session programme, official law process, debate keywords. Every source is optional:
// pages render without it until the scraper has filled data/extra/.
import { votes, mps, mpById, clubColor, NEZ, lawByTlac, type Mp, type Vote } from "./data";

export interface Excuse { from: string; to: string; days: string[]; reason: string }
export interface Bill { title: string; tlac: string | null; state: string; delivered: string | null; approved: string | null; sponsors: string; category: string }
export interface Amendment { date: string; by: string; tlac: string | null; title: string; session: number | null; voteId: string | null; id: string | null }
export interface Interpellation { id: string; title: string; state: string; date: string | null; to: string }
export interface Trip { from: string; to: string; desc: string }
export interface Declaration {
  year: number | null; filed: string | null; function: string | null; incomePublic: number | null; incomeOther: number | null;
  employment: string | null; business: string | null; roles: string[]; realEstateCount: number; realEstateKinds: Record<string, number>;
  movablesCount: number; movables: string[]; rights: string[]; obligations: string[]; userId: string;
}
export interface MpExtra { id: string; excuses: Excuse[]; bills: Bill[]; amendments: Amendment[]; interpellations: Interpellation[]; trips: Trip[]; offices: string[]; declaration: Declaration | null; at: string }
export interface Committee { id: number; name: string; members: { mpId: string; role: string }[] }
export interface Change { date: string; mp: string; mpId: string | null; status: string | null; reason: string }
export interface LawProcess { state: string; stateNote: string | null; delivered: string | null; submitter: string | null; gestor: string | null;
  returnedByPresident: boolean; zbierka: string | null; stages: { stage: string; text: string; result: string | null }[]; at: string }

const one = import.meta.glob<{ default: unknown }>("../../data/extra/*.json", { eager: true });
const file = <T,>(name: string, d: T): T => (one[`../../data/extra/${name}.json`]?.default as T) ?? d;
const byStem = <T,>(g: Record<string, { default: unknown }>) => new Map(Object.entries(g).map(([p, m]) => [p.split("/").pop()!.replace(/\.json$/, ""), m.default as T]));

export const mpExtra = byStem<MpExtra>(import.meta.glob("../../data/extra/mp/*.json", { eager: true }));
export const lawProcess = byStem<LawProcess>(import.meta.glob("../../data/extra/law/*.json", { eager: true }));
const roleKey = (r: string) => (/^predsed/.test(r) ? "predseda" : /^podpredsed/.test(r) ? "podpredseda" : /^overovate/.test(r) ? "overovateľ" : /^náhrad/.test(r) ? "náhradník" : "člen");
export const committees = file<Committee[]>("committees", []).map((c) => ({ ...c, members: c.members.map((x) => ({ ...x, label: x.role, role: roleKey(x.role) })), short: c.name.replace(/^Výbor NR SR pre /, "").replace(/^(\p{Ll})/u, (x) => x.toUpperCase()) }));
export const changes = file<Change[]>("changes", []);
export const program = file<{ n: number; when: string }[]>("program", []);
export const topics = file<Record<string, string[]>>("topics", {});
export const hasExtra = mpExtra.size > 0;

export const committeesOf = (id: string) => committees.flatMap((c) => c.members.filter((x) => x.mpId === id).map((x) => ({ ...c, role: x.role, label: x.label })));

/* ---------- absences: excused vs unexcused ---------- */
const TZ = "Europe/Bratislava";
const day = (iso: string) => new Date(iso).toLocaleDateString("sv-SE", { timeZone: TZ });
export interface Absence { absent: number; excused: number; unexcused: number; excusedDays: number }
export const absence = new Map<string, Absence>();
for (const m of mps) {
  const ex = mpExtra.get(m.id); if (!ex) continue;
  const days = new Set(ex.excuses.flatMap((e) => e.days));
  const a: Absence = { absent: 0, excused: 0, unexcused: 0, excusedDays: days.size };
  for (const v of votes) if (v.votes[m.id] === "0") { a.absent++; if (days.has(day(v.datetime))) a.excused++; else a.unexcused++; }
  absence.set(m.id, a);
}

/* ---------- legislative activity ---------- */
export const isApproved = (b: Bill) => !!b.approved || (!!b.tlac && lawByTlac.get(b.tlac)?.status === "schválený");
const voteById = new Map(votes.map((v) => [v.id, v]));
export const amendmentPassed = (a: Amendment) => (a.voteId ? voteById.get(a.voteId)?.passed ?? null : null);
export const legis = (id: string) => {
  const ex = mpExtra.get(id);
  const bills = ex?.bills ?? []; const am = ex?.amendments ?? [];
  const voted = am.filter((a) => amendmentPassed(a) !== null);
  return { bills, approved: bills.filter(isApproved).length, amendments: am, amendmentsVoted: voted.length, amendmentsPassed: voted.filter((a) => amendmentPassed(a)).length,
    interpellations: ex?.interpellations ?? [], trips: ex?.trips ?? [], offices: ex?.offices ?? [], declaration: ex?.declaration ?? null };
};

/* ---------- voting similarity ---------- */
// Agreement on votes where both MPs voted for, against or abstained.
const ids = mps.map((m) => m.id); const N = ids.length; const pos = new Map(ids.map((id, i) => [id, i]));
const same = new Uint16Array(N * N), both = new Uint16Array(N * N);
const enc: Record<string, number> = { Z: 1, P: 2, "?": 3 };
for (const v of votes) {
  const row: [number, number][] = [];
  for (const [id, c] of Object.entries(v.votes)) { const i = pos.get(id); const e = enc[c]; if (i !== undefined && e) row.push([i, e]); }
  for (let a = 0; a < row.length; a++) for (let b = a + 1; b < row.length; b++) {
    const [i, ei] = row[a], [j, ej] = row[b]; const k = i * N + j, k2 = j * N + i;
    both[k]++; both[k2]++; if (ei === ej) { same[k]++; same[k2]++; }
  }
}
export const similar = (id: string, n = 5) => {
  const i = pos.get(id); if (i === undefined) return { closest: [], otherClubs: [], farthest: [] };
  const me = mpById.get(id)!;
  const all = ids.map((oid, j) => ({ m: mpById.get(oid)!, r: both[i * N + j] >= 50 ? same[i * N + j] / both[i * N + j] : -1, n: both[i * N + j] }))
    .filter((x) => x.m.id !== id && x.r >= 0).sort((a, b) => b.r - a.r);
  return { closest: all.slice(0, n), otherClubs: all.filter((x) => x.m.club !== me.club).slice(0, 3), farthest: all.slice(-3).reverse() };
};

/* ---------- regions ---------- */
export const REGIONS = ["Bratislavský", "Trnavský", "Trenčiansky", "Nitriansky", "Žilinský", "Banskobystrický", "Prešovský", "Košický"] as const;
export const regionMps = (r: string) => mps.filter((m) => m.region === r);
export const outsideSk = mps.filter((m) => !m.region || !REGIONS.includes(m.region as any));

/* ---------- leaderboards ---------- */
const rank = <T,>(f: (m: Mp) => T | undefined, key: (x: T) => number, n = 10) =>
  mps.map((m) => ({ m, x: f(m) })).filter((e): e is { m: Mp; x: T } => e.x !== undefined && key(e.x) > 0).sort((a, b) => key(b.x) - key(a.x)).slice(0, n);
export const topBills = () => rank((m) => mpExtra.get(m.id)?.bills.length, (x) => x);
export const topAmendments = () => rank((m) => mpExtra.get(m.id)?.amendments.length, (x) => x);
export const topInterpellations = () => rank((m) => mpExtra.get(m.id)?.interpellations.length, (x) => x);
export const topTrips = () => rank((m) => mpExtra.get(m.id)?.trips.length, (x) => x);
export const topUnexcused = () => rank((m) => absence.get(m.id)?.unexcused, (x) => x);

export const eur = (n: number | null) => (n == null ? "–" : `${n.toLocaleString("sk-SK")} €`);
export const clubOrNez = (m: Mp) => (m.club === NEZ ? "nezaradený" : m.club);
export { clubColor };
export type { Vote };
