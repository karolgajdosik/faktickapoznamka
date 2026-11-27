// Open data tables, built once per deploy: the same rows feed CSV files and the Excel workbook.
import { mps, formerMps, votes, laws, speeches, mpStats, talk, mpById, CHAIR, type Mp } from "./data";
import { mpExtra, absence, isApproved, lawProcess } from "./extra";
import { temaOfVote } from "./temy";

export interface Table { file: string; title: string; desc: string; cols: [string, string][]; rows: (string | number | null)[][] }

const club = (m: Mp) => m.club;
const r3 = (x: number | null) => (x == null ? null : Math.round(x * 1000) / 1000);

export const tables = (): Table[] => {
  const all = [...mps, ...formerMps];
  const poslanci: Table = {
    file: "poslanci", title: "Poslanci", desc: "Všetci poslanci IX. volebného obdobia s hlavnými ukazovateľmi.",
    cols: [["id", "ID poslanca na nrsr.sk"], ["meno", "meno"], ["klub", "klub (aktuálny)"], ["kraj", "kraj"], ["aktualne", "1 = aktuálne poslanec"],
      ["ucast", "účasť na hlasovaniach (0–1)"], ["sulad_s_klubom", "súlad s väčšinou klubu (0–1)"], ["proti_klubu", "počet hlasovaní proti väčšine klubu"],
      ["neospravedlnene_dni", "dni neospravedlnenej neúčasti"], ["rozprava_sekundy", "čas v rozprave (s)"], ["vystupenia", "počet vystúpení"], ["fakticke", "faktické poznámky"],
      ["navrhy_zakonov", "predložené návrhy zákonov"], ["schvalene_navrhy", "z toho schválené"], ["pozmenujuce", "pozmeňujúce návrhy"], ["interpelacie", "interpelácie"], ["cesty", "zahraničné pracovné cesty"]],
    rows: all.map((m) => { const s = mpStats(m.id), t = talk.get(m.id), x = mpExtra.get(m.id), a = absence.get(m.id);
      return [m.id, m.name, club(m), m.region ?? null, mps.includes(m) ? 1 : 0, r3(s.attendance), r3(s.loyalty), s.rebels.length, a?.unexcused ?? null,
        t?.seconds ?? 0, t?.count ?? 0, t?.factual ?? 0, x?.bills.length ?? null, x ? x.bills.filter(isApproved).length : null, x?.amendments.length ?? null, x?.interpellations.length ?? null, x?.trips.length ?? null]; }),
  };
  const hlasovania: Table = {
    file: "hlasovania", title: "Hlasovania", desc: "Každé hlasovanie s výsledkom, počtami hlasov a témou.",
    cols: [["id", "ID hlasovania na nrsr.sk"], ["datum_cas", "dátum a čas (ISO 8601)"], ["schodza", "číslo schôdze"], ["cislo", "číslo hlasovania na schôdzi"], ["nazov", "názov"], ["upresnenie", "čo sa hlasovalo"],
      ["tlac", "parlamentná tlač"], ["vysledok", "schválené / neschválené / bez výsledku"], ["za", "za"], ["proti", "proti"], ["zdrzal_sa", "zdržal sa"], ["nehlasoval", "nehlasoval"], ["nepritomni", "neprítomní"], ["temy", "témy (oddelené |)"]],
    rows: votes.map((v) => [v.id, v.datetime, v.session, v.number, v.title, v.detail ?? null, v.tlac, v.passed === null ? "bez výsledku" : v.passed ? "schválené" : "neschválené",
      v.counts.Z, v.counts.P, v.counts["?"], v.counts.N, v.counts["0"], (temaOfVote.get(v.id) ?? []).join("|")]),
  };
  // one file per year keeps every file far below the 25 MB hosting limit for the whole term
  const years = [...new Set(votes.map((v) => v.datetime.slice(0, 4)))].sort();
  const hlasy: Table[] = years.map((y) => ({
    file: `hlasy-${y}`, title: `Hlasy poslancov ${y}`, desc: `Ako hlasoval každý poslanec v každom hlasovaní v roku ${y} (jeden riadok = jeden hlas).`,
    cols: [["hlasovanie_id", "ID hlasovania"], ["poslanec_id", "ID poslanca"], ["hlas", "Z = za, P = proti, ? = zdržal sa, N = nehlasoval, 0 = neprítomný"], ["klub", "klub v čase hlasovania"]],
    rows: votes.filter((v) => v.datetime.startsWith(y)).flatMap((v) => Object.entries(v.votes).map(([id, c]) => [v.id, id, c, v.clubs?.[id] ?? mpById.get(id)?.club ?? null])),
  }));
  const zakony: Table = {
    file: "zakony", title: "Zákony", desc: "Parlamentné tlače, o ktorých sa hlasovalo, so stavom legislatívneho procesu.",
    cols: [["tlac", "parlamentná tlač"], ["nazov", "názov"], ["druh", "druh návrhu"], ["stav", "stav podľa hlasovaní"], ["stav_nrsr", "stav podľa nrsr.sk"], ["navrhovatel", "navrhovateľ"],
      ["dorucene", "dátum doručenia"], ["prve", "prvá aktivita"], ["posledne", "posledná aktivita"], ["zbierka", "číslo v Zbierke zákonov"], ["hlasovani", "počet hlasovaní"]],
    rows: laws.map((l) => { const p = lawProcess.get(l.tlac);
      return [l.tlac, l.title, l.kind, l.status, p?.state ?? null, p?.submitter ?? null, p?.delivered ?? null, l.first, l.last, p?.zbierka ?? null, l.votes.length]; }),
  };
  const majetok: Table = {
    file: "majetok", title: "Majetkové priznania", desc: "Verejná časť oznámení funkcionárov (bez polohy nehnuteľností).",
    cols: [["poslanec_id", "ID poslanca"], ["meno", "meno"], ["rok", "rok oznámenia"], ["prijem_z_funkcie", "príjem z verejnej funkcie (€)"], ["ine_prijmy", "iné príjmy (€)"],
      ["nehnutelnosti", "počet nehnuteľností"], ["druhy_nehnutelnosti", "druhy nehnuteľností"], ["hnutelne_veci", "počet hnuteľných vecí"], ["majetkove_prava", "majetkové práva"], ["zavazky", "záväzky"]],
    rows: all.flatMap((m) => { const d = mpExtra.get(m.id)?.declaration; if (!d) return [];
      return [[m.id, m.name, d.year ?? null, d.incomePublic ?? null, d.incomeOther ?? null, d.realEstateCount, Object.entries(d.realEstateKinds).map(([k, n]) => `${k} (${n})`).join("; "),
        d.movablesCount, d.rights.join("; "), d.obligations.join("; ")]]; }),
  };
  const vystupenia: Table = {
    file: "vystupenia", title: "Vystúpenia v rozprave", desc: "Metadáta vystúpení (bez textu prepisu; ten je na stránkach rozpravy).",
    cols: [["id", "ID vystúpenia"], ["zaciatok", "začiatok (ISO 8601)"], ["trvanie_s", "trvanie (s)"], ["schodza", "schôdza"], ["recnik", "rečník"], ["poslanec_id", "ID poslanca"], ["druh", "druh vystúpenia"], ["tlac", "tlač"]],
    rows: speeches.filter((x) => x.kind !== CHAIR).map((x) => [x.id, x.start, x.dur, x.session, x.speaker, x.mpId ?? null, x.kind, x.tlac]),
  };
  return [poslanci, hlasovania, ...hlasy, zakony, majetok, vystupenia];
};

const cell = (v: string | number | null) => { if (v == null) return ""; const s = String(v); return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
export const toCsv = (t: Table) => "﻿" + [t.cols.map((c) => c[0]).join(","), ...t.rows.map((r) => r.map(cell).join(","))].join("\r\n") + "\r\n";
