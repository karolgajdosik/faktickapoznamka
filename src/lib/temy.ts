// Topic of each vote, from the title of the bill or motion. Rules, not AI: transparent and repeatable.
// A vote can belong to several topics; procedural votes get none.
import { votes, mps, mpById, lawTitle, isFinal, NEZ, clubs, type Vote, type Code } from "./data";

export interface Tema { slug: string; name: string; re: RegExp; desc: string }
export const TEMY: Tema[] = [
  { slug: "zdravotnictvo", name: "Zdravotníctvo", desc: "zdravotná starostlivosť, nemocnice, lieky, zdravotné poistenie", re: /zdravot|nemocn|liek|lieč|pacient|ambulan|lekár|psychiatr|hygien|verejného zdravia|záchrann/iu },
  { slug: "dane-a-rozpocet", name: "Dane a rozpočet", desc: "dane, odvody, štátny rozpočet, verejné financie", re: /\bdan[eií]|daňov|rozpočt|rozpočet|odvod|spotrebn\p{L}+ dan|\bdph\b|pridanej hodnoty|poplatk|clo\b|colný|verejných financi|účtovníc|finančn\p{L}+ správ|konsolidác/iu },
  { slug: "socialne-veci-a-rodina", name: "Sociálne veci a rodina", desc: "dôchodky, rodina, deti, sociálne služby, práca", re: /sociáln|dôchod|rodin|\bdiet|\bdeti|detí|prídav|materstv|rodičovsk|zamestnan|nezamestnan|minimáln\p{L}+ mzd|zákonník práce|pomoci v hmotnej núdzi|opatrovateľ|seniorov|ťažkým zdravotným postihnutím/iu },
  { slug: "skolstvo-a-veda", name: "Školstvo a veda", desc: "školy, vysoké školy, vzdelávanie, výskum", re: /škol|vzdeláv|výchov|univerzit|\bvede\b|vedy\b|výskum|žiak|učiteľ|pedagog|mládež/iu },
  { slug: "justicia", name: "Justícia a trestné právo", desc: "súdy, prokuratúra, trestné právo, advokácia", re: /\bsúd|súdn|súdov|sudc|trestn|prokur|justíc|advokác|exekú|notár|väzen|ochran\p{L}+ oznamovateľ|korupc|amnest|milost/iu },
  { slug: "bezpecnost-a-obrana", name: "Bezpečnosť a obrana", desc: "armáda, polícia, krízové situácie, spravodajské služby", re: /obran|ozbrojen|vojen|vojsk|polic|policaj|bezpečnost|hasič|krízov|zbra[nň]|spravodajsk|\bsis\b|\bnbú\b|nato|civiln\p{L}+ ochran|radikaliz|extrémiz/iu },
  { slug: "doprava-a-vystavba", name: "Doprava, výstavba a bývanie", desc: "cesty, železnice, letectvo, stavebné povolenia, bývanie", re: /doprav|cestn|ciest|diaľnic|železn|letec|letisk|staveb|výstavb|územn\p{L}+ plán|bývan|nájm\p{L}+ byt|byt\p{L}*|vlastníctve bytov|kataster|geodéz/iu },
  { slug: "zivotne-prostredie-a-energetika", name: "Životné prostredie a energetika", desc: "príroda, voda, odpady, energie, klíma", re: /životn\p{L}+ prostred|prírod|krajin\p{L}+ ochran|energ|klím|odpad|\bvod[ayn]|vodn|lesoch|lesn\p{L}+ |jadrov|emis|environment|ovzduš|obnoviteľn|elektrin|plyn|teplárenst/iu },
  { slug: "polnohospodarstvo", name: "Poľnohospodárstvo a potraviny", desc: "poľnohospodárstvo, potraviny, pôda, veterinárna starostlivosť", re: /poľnohospod|potravin|veterin|pôd[ay]|pozemkov|agrár|rastlinn|živočíš|vinohrad|poľovn|rybárst/iu },
  { slug: "ekonomika-a-podnikanie", name: "Ekonomika a podnikanie", desc: "podnikanie, obchod, banky, spotrebitelia, investície", re: /podnik|obchodn|živnost|hospodárs|bank|investí|spotrebite|trh\p{L}*|konkurz|reštrukturaliz|cestovn\p{L}+ ruch|kapitáln|poisťovn|regulác|hazard|úver|cenných papier|cenách|\bcien|tabak|alkohol|investičn\p{L}* pomoc|pôvodu príjmov|majetk/iu },
  { slug: "samosprava-a-volby", name: "Samospráva a voľby", desc: "obce, kraje, voľby, referendum", re: /\bobc[eíiou]|obecn|samospráv|vyšš\p{L}+ územn|samosprávn\p{L}+ kraj|voľb\p{L}+ do|volebn|referend|hlavn\p{L}+ mest|mestsk\p{L}+ čast/iu },
  { slug: "stat-a-ustava", name: "Štát a ústava", desc: "ústava, vláda, štátna správa, parlament", re: /ústav(?!n\p{L}+ súd)|ústavn\p{L}+ zákon|štátn\p{L}+ služb|verejn\p{L}+ správ|organizácii činnosti vlády|ústredn\p{L}+ štátnej správy|rokovac\p{L}+ poriad|štátn\p{L}+ symbol|štátn\p{L}+ občian|slobodn\p{L}+ prístup\p{L}* k informáci|ochran\p{L}+ osobn/iu },
  { slug: "parlament-a-vlada", name: "Parlament, vláda a dôvera", desc: "voľby do funkcií, výbory, dôvera vláde, programové vyhlásenie", re: /nedôver|dôver\p{L}* vlád|programov\p{L}* vyhlásen|voľb\p{L}* (?:overovateľ|člen|poslan|predsed|podpredsed|generáln|riaditeľ|sudc|kandidát)|výbor\p{L}* národnej rady|zložen\p{L}* výbor|podpredsedov národnej rady|odvolan\p{L}* (?:z funkcie|člen|predsed|podpredsed)|mandát/iu },
  { slug: "kultura-media-a-sport", name: "Kultúra, médiá a šport", desc: "kultúra, médiá a vysielanie, pamiatky, cirkvi, šport", re: /kultúr|médi|vysiela|televízi|rozhlas|\bstvr\b|\brtvs\b|pamiat|cirk|nábožens|šport|knižn|múze|audiovizu|autorsk/iu },
  { slug: "zahranicie-a-eu", name: "Zahraničie a EÚ", desc: "medzinárodné zmluvy, Európska únia, zahraničná politika", re: /medzinárod|zmluv\p{L}+ medzi|dohod\p{L}+ medzi|európsk|\beú\b|zahrani|ukrajin|vyslanie|diplomat|protokol\p{L}* k/iu },
];
export const temaBySlug = new Map(TEMY.map((t) => [t.slug, t]));

const SKIP = /procedur|program\p{L}* schôdze|zmen\p{L}+ programu|prezentáci|presunut|prerušen/iu;
export const temyOf = (v: Vote): string[] => {
  const text = `${lawTitle(v.title)} ${v.detail ?? ""}`;
  if (SKIP.test(v.title) && !v.tlac) return [];
  return TEMY.filter((t) => t.re.test(text)).map((t) => t.slug);
};

export const votesByTema = new Map<string, Vote[]>(TEMY.map((t) => [t.slug, []]));
export const temaOfVote = new Map<string, string[]>();
for (const v of votes) { const ts = temyOf(v); temaOfVote.set(v.id, ts); for (const s of ts) votesByTema.get(s)!.push(v); }

/** How one MP voted on a topic: shares of their votes (present + absent). */
export function mpTemy(id: string) {
  return TEMY.map((t) => {
    const c: Record<Code, number> = { Z: 0, P: 0, "?": 0, N: 0, "0": 0 };
    for (const v of votesByTema.get(t.slug)!) { const x = v.votes[id]; if (x) c[x]++; }
    const total = c.Z + c.P + c["?"] + c.N + c["0"];
    return { t, c, total };
  }).filter((x) => x.total >= 5).sort((a, b) => b.total - a.total);
}

/** Per club: share voting for, against or abstaining on the final votes of a topic. */
export function clubsOnTema(slug: string) {
  const finals = votesByTema.get(slug)!.filter(isFinal);
  return clubs.filter((c) => c.name !== NEZ).map((club) => {
    const c = { Z: 0, P: 0, "?": 0 } as Record<"Z" | "P" | "?", number>;
    for (const v of finals) for (const [id, x] of Object.entries(v.votes)) {
      if ((v.clubs?.[id] ?? mpById.get(id)?.club) !== club.name) continue;
      if (x === "Z" || x === "P" || x === "?") c[x]++;
    }
    const n = c.Z + c.P + c["?"];
    return { club: club.name, c, n };
  }).filter((x) => x.n > 0);
}
export { mps };
