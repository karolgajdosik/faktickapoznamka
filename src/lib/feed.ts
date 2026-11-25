import { mpStats, mpTalk, voteById, voteHeadline, voteContext, resultText, LABEL, speakerLabel, excerpt, type Mp } from "./data";
export const SITE = "https://faktickapoznamka.sk";
const x = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
export interface Item { title: string; url: string; date: string; text: string; type: "vote" | "speech" }
export function rss(title: string, link: string, description: string, items: Item[]) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>${x(title)}</title><link>${SITE}${link}</link><description>${x(description)}</description><language>sk</language>
<atom:link href="${SITE}${link}${link.endsWith("/") ? "" : "/"}rss.xml" rel="self" type="application/rss+xml"/>
${items.map((i) => `<item><title>${x(i.title)}</title><link>${SITE}${i.url}</link><guid isPermaLink="false">${x(i.url)}#${i.date}</guid><pubDate>${new Date(i.date).toUTCString()}</pubDate><description>${x(i.text)}</description></item>`).join("\n")}
</channel></rss>`;
}
/** Recent activity of an MP: speeches and votes against the own club. */
export function mpActivity(m: Mp, n = 30): Item[] {
  const speeches: Item[] = mpTalk(m.id).recent.map((s) => ({
    type: "speech", date: s.start, url: s.session ? `/rozprava/${s.session}/${s.start.slice(0, 10)}/#${s.id}` : `/poslanci/${m.id}/`,
    title: `${m.name}: ${s.kind || "vystúpenie"}${s.tlac ? ` (tlač ${s.tlac})` : ""}`, text: s.text ? excerpt(s.text, 400) : "Prepis zatiaľ nie je zverejnený.",
  }));
  const rebels: Item[] = mpStats(m.id).rebels.slice(-20).map((id) => voteById.get(id)!).filter(Boolean).map((v) => ({
    type: "vote", date: v.datetime, url: `/hlasovania/${v.id}/`,
    title: `${m.name} hlasoval(a) inak ako klub: ${LABEL[v.votes[m.id]].toLowerCase()}`,
    text: `${voteHeadline(v)}${voteContext(v) ? ` – ${voteContext(v)}` : ""}. Výsledok: ${resultText(v).toLowerCase()}.`,
  }));
  return [...speeches, ...rebels].sort((a, b) => b.date.localeCompare(a.date)).slice(0, n);
}
export { speakerLabel };
