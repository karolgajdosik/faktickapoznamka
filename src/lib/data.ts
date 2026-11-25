export type Code = "Z" | "P" | "?" | "N" | "0";
export interface Mp { id: string; name: string; sortName: string; club: string }
export interface Vote {
  id: string; session: number | null; number: number | null; datetime: string;
  title: string; tlac: string | null; passed: boolean | null;
  counts: Record<Code, number>; votes: Record<string, Code>;
}
export interface Meta { demo: boolean; term: number; updatedAt: string; lastVoteId: string | null }

import mpsJson from "../../data/mps.json";
import metaJson from "../../data/meta.json";
import liveJson from "../../data/live.json";
export const live = liveJson as { item: string | null; since: string | null };
const voteFiles = import.meta.glob<{ default: Vote }>("../../data/votes/*.json", { eager: true });

export const meta = metaJson as Meta;
export const mps = (mpsJson as Mp[]).slice().sort((a, b) => a.sortName.localeCompare(b.sortName, "sk"));
export const mpById = new Map(mps.map((m) => [m.id, m]));
/** "Prezentácia" = attendance check, not a decision on anything: excluded from lists and stats. */
export const isPresence = (v: Vote) => /^prezentácia\.?$/i.test(v.title.trim());
export const votes = Object.values(voteFiles).map((m) => m.default).filter((v) => !isPresence(v))
  .sort((a, b) => b.datetime.localeCompare(a.datetime) || Number(b.id) - Number(a.id));

export const CODES: Code[] = ["Z", "P", "?", "N", "0"];
export const LABEL: Record<Code, string> = { Z: "Za", P: "Proti", "?": "Zdržal sa", N: "Nehlasoval", "0": "Neprítomný" };

/** Clubs ordered by size (largest first). Size ordering is deliberately neutral — no left/right placement. */
export const clubs = (() => {
  const n = new Map<string, number>();
  for (const m of mps) n.set(m.club, (n.get(m.club) ?? 0) + 1);
  return [...n.entries()].sort((a, b) => (a[0] === "Nezaradení" ? 1 : b[0] === "Nezaradení" ? -1 : b[1] - a[1]))
    .map(([name, size]) => ({ name, size }));
})();

export const fmtDate = (iso: string) =>
  new Date(iso).toLocaleDateString("sk-SK", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Bratislava" });
export const fmtShort = (iso: string) =>
  new Date(iso).toLocaleDateString("sk-SK", { day: "numeric", month: "numeric", year: "numeric", timeZone: "Europe/Bratislava" });
export const fmtTime = (iso: string) =>
  new Date(iso).toLocaleTimeString("sk-SK", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Bratislava" });

export function resultText(v: Vote) {
  return v.passed === null ? "Výsledok neuvedený" : v.passed ? "Schválené" : "Neschválené";
}

export function mpStats(id: string) {
  let total = 0, present = 0, withClub = 0, clubComparable = 0;
  const mp = mpById.get(id)!;
  for (const v of votes) {
    const c = v.votes[id]; if (!c) continue;
    total++; if (c !== "0") present++;
    if (c === "Z" || c === "P" || c === "?") {
      const tally: Record<string, number> = {};
      for (const [oid, oc] of Object.entries(v.votes)) {
        if (oid === id || mpById.get(oid)?.club !== mp.club) continue;
        if (oc === "Z" || oc === "P" || oc === "?") tally[oc] = (tally[oc] ?? 0) + 1;
      }
      const top = Object.entries(tally).sort((a, b) => b[1] - a[1])[0];
      if (top && mp.club !== "Nezaradení") { clubComparable++; if (top[0] === c) withClub++; }
    }
  }
  return {
    total, present,
    attendance: total ? present / total : null,
    loyalty: clubComparable ? withClub / clubComparable : null,
  };
}

export const pct = (x: number | null) => (x === null ? "–" : `${Math.round(x * 100)} %`);
