import type { APIRoute } from "astro";
import { votes, voteHeadline, voteContext, resultText } from "../lib/data";
import { rss } from "../lib/feed";
export const GET: APIRoute = () => new Response(rss("faktická poznámka – hlasovania NR SR", "/", "Najnovšie hlasovania Národnej rady SR",
  votes.slice(0, 100).map((v) => ({ type: "vote", date: v.datetime, url: `/hlasovania/${v.id}/`,
    title: `${resultText(v)}: ${voteHeadline(v)}`.slice(0, 200),
    text: `${voteContext(v) ?? ""} Za ${v.counts.Z}, proti ${v.counts.P}, zdržalo sa ${v.counts["?"]}, neprítomní ${v.counts["0"]}.`.trim() }))),
  { headers: { "content-type": "application/rss+xml; charset=utf-8" } });
