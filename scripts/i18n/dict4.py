# UI dictionary, part 4: committees, regions, assets, search, about, follow, misc.
from dict1 import E

# ---- dates in context ({d} = a date the translator formats itself)
E("Záverečné hlasovanie {d}:", "Final vote {d}:", "Schlussabstimmung {d}:", "Zárószavazás {d}:", "Głosowanie końcowe {d}:")
E("Posledné hlasovanie, {d}", "Latest vote, {d}", "Letzte Abstimmung, {d}", "Legutóbbi szavazás, {d}", "Ostatnie głosowanie, {d}")
E("Rozprava {d}", "Debate {d}", "Debatte {d}", "Vita {d}", "Debata {d}")
E(["Posledná aktualizácia {n}. {n}. {n} {n}:{n}"], "Last updated {n}. {n}. {n} {n}:{n}", "Zuletzt aktualisiert {n}. {n}. {n} {n}:{n}", "Utolsó frissítés: {n}. {n}. {n} {n}:{n}", "Ostatnia aktualizacja {n}. {n}. {n} {n}:{n}")

# ---- committees
E("Výbory – faktická poznámka", "Committees – faktická poznámka", "Ausschüsse – faktická poznámka", "Bizottságok – faktická poznámka", "Komisje – faktická poznámka")
E("Výbory pripravujú návrhy zákonov pred hlasovaním v pléne. Zloženie podľa nrsr.sk.", "Committees prepare bills before the plenary vote. Membership according to nrsr.sk.", "Ausschüsse bereiten Gesetzentwürfe vor der Plenarabstimmung vor. Zusammensetzung laut nrsr.sk.", "A bizottságok a plenáris szavazás előtt készítik elő a javaslatokat. Összetétel az nrsr.sk szerint.", "Komisje przygotowują projekty przed głosowaniem plenarnym. Skład według nrsr.sk.")
E("Výbory Národnej rady SR: predsedovia, členovia a zloženie podľa poslaneckých klubov.", "Committees of the National Council: chairs, members and composition by caucus.", "Ausschüsse des Nationalrats: Vorsitzende, Mitglieder und Zusammensetzung nach Fraktionen.", "A Nemzeti Tanács bizottságai: elnökök, tagok és összetétel frakciók szerint.", "Komisje Rady Narodowej: przewodniczący, członkowie i skład według klubów.")
E("Údaje o výboroch sa práve načítavajú.", "Committee data is loading.", "Ausschussdaten werden geladen.", "A bizottsági adatok betöltése folyamatban.", "Dane komisji są wczytywane.")
E("Gestorský výbor pre", "Lead committee for", "Federführend für", "Illetékes bizottság a következőkhöz:", "Komisja wiodąca dla")
E("Výbor na nrsr.sk", "Committee on nrsr.sk", "Ausschuss auf nrsr.sk", "Bizottság az nrsr.sk-n", "Komisja na nrsr.sk")
for sk, en, de, hu, pl in [
  ("Mandátový a imunitný výbor NR SR", "Mandate and Immunity Committee", "Mandats- und Immunitätsausschuss", "Mandátum- és mentelmi bizottság", "Komisja Mandatowo-Immunitetowa"),
  ("Mandátový a imunitný výbor", "Mandate and Immunity Committee", "Mandats- und Immunitätsausschuss", "Mandátum- és mentelmi bizottság", "Komisja Mandatowo-Immunitetowa"),
  ("Nezlučiteľnosť funkcií", "Incompatibility of Functions", "Unvereinbarkeit von Ämtern", "Összeférhetetlenség", "Niepołączalność funkcji"),
  ("Európske záležitosti", "European Affairs", "Europäische Angelegenheiten", "Európai ügyek", "Sprawy europejskie"),
  ("Ústavnoprávny výbor NR SR", "Constitutional and Legal Affairs Committee", "Verfassungs- und Rechtsausschuss", "Alkotmányjogi bizottság", "Komisja Konstytucyjno-Prawna"),
  ("Ústavnoprávny výbor", "Constitutional and Legal Affairs Committee", "Verfassungs- und Rechtsausschuss", "Alkotmányjogi bizottság", "Komisja Konstytucyjno-Prawna"),
  ("Financie a rozpočet", "Finance and Budget", "Finanzen und Haushalt", "Pénzügyek és költségvetés", "Finanse i budżet"),
  ("Hospodárske záležitosti", "Economic Affairs", "Wirtschaftliche Angelegenheiten", "Gazdasági ügyek", "Sprawy gospodarcze"),
  ("Pôdohospodárstvo a životné prostredie", "Agriculture and Environment", "Landwirtschaft und Umwelt", "Mezőgazdaság és környezetvédelem", "Rolnictwo i środowisko"),
  ("Verejnú správu a regionálny rozvoj", "Public Administration and Regional Development", "Öffentliche Verwaltung und regionale Entwicklung", "Közigazgatás és regionális fejlesztés", "Administracja publiczna i rozwój regionalny"),
  ("Sociálne veci", "Social Affairs", "Soziales", "Szociális ügyek", "Sprawy społeczne"),
  ("Zdravotníctvo", "Health", "Gesundheitswesen", "Egészségügy", "Zdrowie"),
  ("Obranu a bezpečnosť", "Defence and Security", "Verteidigung und Sicherheit", "Védelem és biztonság", "Obrona i bezpieczeństwo"),
  ("Zahraničný výbor NR SR", "Foreign Affairs Committee", "Auswärtiger Ausschuss", "Külügyi bizottság", "Komisja Spraw Zagranicznych"),
  ("Zahraničný výbor", "Foreign Affairs Committee", "Auswärtiger Ausschuss", "Külügyi bizottság", "Komisja Spraw Zagranicznych"),
  ("Vzdelávanie, vedu, mládež, šport a cestovný ruch", "Education, Science, Youth, Sport and Tourism", "Bildung, Wissenschaft, Jugend, Sport und Tourismus", "Oktatás, tudomány, ifjúság, sport és idegenforgalom", "Edukacja, nauka, młodzież, sport i turystyka"),
  ("Kultúru a médiá", "Culture and Media", "Kultur und Medien", "Kultúra és média", "Kultura i media"),
  ("Ľudské práva a národnostné menšiny", "Human Rights and National Minorities", "Menschenrechte und nationale Minderheiten", "Emberi jogok és nemzeti kisebbségek", "Prawa człowieka i mniejszości narodowe"),
  ("Sociálne veci a bývanie", "Social Affairs and Housing", "Soziales und Wohnen", "Szociális ügyek és lakhatás", "Sprawy społeczne i mieszkalnictwo"),
  ("Výbor NR SR na kontrolu činnosti SIS", "Committee for Oversight of the SIS", "Ausschuss zur Kontrolle des SIS", "Az SIS tevékenységét ellenőrző bizottság", "Komisja ds. kontroli SIS"),
  ("Výbor NR SR na kontrolu činnosti VS", "Committee for Oversight of Military Intelligence", "Ausschuss zur Kontrolle des Militärgeheimdienstes", "A katonai hírszerzést ellenőrző bizottság", "Komisja ds. kontroli wywiadu wojskowego"),
  ("Výbor NR SR na kontrolu činnosti NBÚ", "Committee for Oversight of the National Security Authority", "Ausschuss zur Kontrolle der Nationalen Sicherheitsbehörde", "A Nemzeti Biztonsági Hivatalt ellenőrző bizottság", "Komisja ds. kontroli NBÚ"),
]:
    E(sk, en, de, hu, pl)
    E(sk + " ({n})", en + " ({n})", de + " ({n})", hu + " ({n})", pl + " ({n})")

# ---- regions
for sk, en, de, hu, pl in [("Bratislavský","Bratislava","Bratislava","Pozsonyi","Bratysławski"),("Trnavský","Trnava","Trnava","Nagyszombati","Trnawski"),("Trenčiansky","Trenčín","Trenčín","Trencséni","Trenczyński"),
  ("Nitriansky","Nitra","Nitra","Nyitrai","Nitrzański"),("Žilinský","Žilina","Žilina","Zsolnai","Żyliński"),("Banskobystrický","Banská Bystrica","Banská Bystrica","Besztercebányai","Bańskobystrzycki"),
  ("Prešovský","Prešov","Prešov","Eperjesi","Preszowski"),("Košický","Košice","Košice","Kassai","Koszycki")]:
    E(sk, en, de, hu, pl)
    E(sk + " kraj", en + " Region", "Region " + de, hu + " kerület", "Kraj " + pl.lower())
E("Poslanci podľa krajov – faktická poznámka", "MPs by region – faktická poznámka", "Abgeordnete nach Regionen – faktická poznámka", "Képviselők kerületenként – faktická poznámka", "Posłowie według krajów – faktická poznámka")
E("Podľa bydliska uvedeného na nrsr.sk. Slovensko je jeden volebný obvod, takže poslanci nezastupujú kraje formálne.", "By residence as listed on nrsr.sk. Slovakia is a single constituency, so MPs do not formally represent regions.", "Nach dem auf nrsr.sk angegebenen Wohnort. Die Slowakei ist ein einziger Wahlkreis, Abgeordnete vertreten Regionen also nicht formell.", "Az nrsr.sk-n feltüntetett lakhely szerint. Szlovákia egyetlen választókerület, így a képviselők formálisan nem képviselnek kerületeket.", "Według miejsca zamieszkania podanego na nrsr.sk. Słowacja to jeden okręg wyborczy, więc posłowie formalnie nie reprezentują krajów.")
E("Odkiaľ pochádzajú poslanci NR SR: počet poslancov s bydliskom v každom kraji a ich kluby.", "Where MPs come from: number of MPs living in each region and their caucuses.", "Woher die Abgeordneten kommen: Zahl der Abgeordneten mit Wohnsitz in jeder Region und ihre Fraktionen.", "Honnan származnak a képviselők: az egyes kerületekben élő képviselők száma és frakciójuk.", "Skąd pochodzą posłowie: liczba posłów mieszkających w każdym kraju i ich kluby.")
E("Bez uvedeného kraja", "No region given", "Ohne Regionsangabe", "Kerület megadása nélkül", "Bez podanego kraju")

# ---- assets
E("Majetkové priznania poslancov – faktická poznámka", "MPs' asset declarations – faktická poznámka", "Vermögenserklärungen der Abgeordneten – faktická poznámka", "Képviselői vagyonnyilatkozatok – faktická poznámka", "Oświadczenia majątkowe posłów – faktická poznámka")
E("Príjmy, nehnuteľnosti, hnuteľné veci a záväzky poslancov NR SR podľa oznámení verejných funkcionárov.", "Income, real estate, movable property and liabilities of MPs according to public officials' declarations.", "Einkünfte, Immobilien, bewegliche Sachen und Verbindlichkeiten der Abgeordneten laut Erklärungen öffentlicher Amtsträger.", "A képviselők jövedelme, ingatlanai, ingóságai és kötelezettségei a közfunkcionáriusi nyilatkozatok szerint.", "Dochody, nieruchomości, ruchomości i zobowiązania posłów według oświadczeń funkcjonariuszy publicznych.")
E(["Oznámenia verejných funkcionárov za rok {n}, ako ich zverejňuje nrsr.sk. Presné polohy nehnuteľností neuvádzame."], "Public officials' declarations for {n}, as published by nrsr.sk. We do not show exact property locations.", "Erklärungen öffentlicher Amtsträger für {n}, wie von nrsr.sk veröffentlicht. Genaue Lagen von Immobilien zeigen wir nicht.", "Közfunkcionáriusi nyilatkozatok ({n}), ahogy az nrsr.sk közzéteszi. Az ingatlanok pontos helyét nem közöljük.", "Oświadczenia funkcjonariuszy publicznych za {n} r., jak publikuje je nrsr.sk. Nie podajemy dokładnych lokalizacji nieruchomości.")
E("Medián príjmu z funkcie", "Median income from office", "Medianeinkommen aus dem Amt", "Közfunkcióból származó jövedelem mediánja", "Mediana dochodu z funkcji")
E("Poslanci s inými príjmami", "MPs with other income", "Abgeordnete mit sonstigen Einkünften", "Egyéb jövedelemmel rendelkező képviselők", "Posłowie z innymi dochodami")
E("Medián nehnuteľností", "Median real estate", "Median Immobilien", "Ingatlanok mediánja", "Mediana nieruchomości")
E("Poslanci so záväzkami", "MPs with liabilities", "Abgeordnete mit Verbindlichkeiten", "Kötelezettséggel rendelkező képviselők", "Posłowie ze zobowiązaniami")
E("Poslanec", "MP", "Abgeordnete(r)", "Képviselő", "Poseł")
E("Z funkcie", "From office", "Aus dem Amt", "Közfunkcióból", "Z funkcji")
E("Nehnut.", "Real est.", "Immob.", "Ingatl.", "Nieruch.")
E("Hnut.", "Movable", "Bewegl.", "Ingóság", "Ruchom.")
E("podľa iných príjmov", "by other income", "nach sonstigen Einkünften", "egyéb jövedelem szerint", "wg innych dochodów")
E("podľa príjmu z funkcie", "by income from office", "nach Einkünften aus dem Amt", "közfunkciós jövedelem szerint", "wg dochodu z funkcji")
E("podľa počtu nehnuteľností", "by number of properties", "nach Anzahl der Immobilien", "ingatlanok száma szerint", "wg liczby nieruchomości")
E("podľa hnuteľných vecí", "by movable property", "nach beweglichen Sachen", "ingóságok szerint", "wg ruchomości")
E("podľa záväzkov", "by liabilities", "nach Verbindlichkeiten", "kötelezettségek szerint", "wg zobowiązań")
E("podľa mena", "by name", "nach Name", "név szerint", "wg nazwiska")
E("Zoradiť", "Sort", "Sortieren", "Rendezés", "Sortuj")
E("Počty sú počty položiek v oznámení (napríklad jeden list vlastníctva môže zahŕňať viac parciel). Iné príjmy zahŕňajú všetky príjmy mimo výkonu verejnej funkcie. Kliknutím otvoríte detail poslanca s odkazom na celé oznámenie.", "Counts are numbers of items in the declaration (one title deed can cover several plots). Other income covers everything outside the public office. Click to open the MP's detail with a link to the full declaration.", "Die Zahlen sind Einträge in der Erklärung (ein Grundbuchblatt kann mehrere Parzellen umfassen). Sonstige Einkünfte umfassen alles außerhalb des Amtes. Klicken öffnet die Details mit Link zur vollständigen Erklärung.", "A számok a nyilatkozat tételeinek száma (egy tulajdoni lap több parcellát is tartalmazhat). Az egyéb jövedelem a közfunkción kívüli összes jövedelem. Kattintásra megnyílik a képviselő adatlapja a teljes nyilatkozat linkjével.", "Liczby to pozycje w oświadczeniu (jedna księga wieczysta może obejmować kilka działek). Inne dochody to wszystko poza funkcją publiczną. Kliknij, aby otworzyć szczegóły posła z odnośnikiem do pełnego oświadczenia.")
E("Údaje sa práve načítavajú.", "Data is loading.", "Daten werden geladen.", "Az adatok betöltése folyamatban.", "Dane są wczytywane.")

# ---- search page
E("Hľadať – faktická poznámka", "Search – faktická poznámka", "Suche – faktická poznámka", "Keresés – faktická poznámka", "Szukaj – faktická poznámka")
E("Hľadať v parlamente", "Search parliament", "Im Parlament suchen", "Keresés a parlamentben", "Szukaj w parlamencie")
E("Prepisy rozpravy, zákony, poslanci, schôdze a výbory na jednom mieste.", "Debate transcripts, bills, MPs, sessions and committees in one place.", "Debattenprotokolle, Gesetze, Abgeordnete, Sitzungen und Ausschüsse an einem Ort.", "Vitajegyzőkönyvek, törvények, képviselők, ülésszakok és bizottságok egy helyen.", "Stenogramy debat, ustawy, posłowie, posiedzenia i komisje w jednym miejscu.")
E("Vyhľadávanie v prepisoch rozpravy, zákonoch, poslancoch, schôdzach a výboroch NR SR.", "Search debate transcripts, bills, MPs, sessions and committees of the National Council.", "Suche in Debattenprotokollen, Gesetzen, Abgeordneten, Sitzungen und Ausschüssen.", "Keresés vitajegyzőkönyvekben, törvényekben, képviselők, ülésszakok és bizottságok között.", "Wyszukiwanie w stenogramach, ustawach, posłach, posiedzeniach i komisjach.")
E("Slovo, meno poslanca alebo číslo tlače", "Word, MP name or print number", "Wort, Name oder Drucksachennummer", "Szó, képviselő neve vagy nyomtatványszám", "Słowo, nazwisko posła lub numer druku")
E("Naposledy", "Recent", "Zuletzt", "Legutóbb", "Ostatnio")
E("Skúste", "Try", "Versuchen Sie", "Próbáld", "Spróbuj")
E("Prehliadať", "Browse", "Durchsuchen", "Böngészés", "Przeglądaj")
E("Tlače, čítania a stav", "Prints, readings and status", "Drucksachen, Lesungen und Status", "Nyomtatványok, olvasatok és állapot", "Druki, czytania i stan")
E("Všetky hlasovania s filtrom", "All votes, filterable", "Alle Abstimmungen mit Filter", "Minden szavazás szűrővel", "Wszystkie głosowania z filtrem")
E("Kalendár a program", "Calendar and agenda", "Kalender und Programm", "Naptár és program", "Kalendarz i program")
E("Zloženie a predsedovia", "Membership and chairs", "Zusammensetzung und Vorsitzende", "Összetétel és elnökök", "Skład i przewodniczący")
E("Príjmy a priznania", "Income and declarations", "Einkünfte und Erklärungen", "Jövedelmek és nyilatkozatok", "Dochody i oświadczenia")
E("Rýchle výsledky", "Quick results", "Schnelle Ergebnisse", "Gyors találatok", "Szybkie wyniki")
E("Druh výsledkov", "Result type", "Ergebnisart", "Találat típusa", "Rodzaj wyników")
E("Všetko", "Everything", "Alles", "Minden", "Wszystko")
E("Tlač", "Print", "Drucksache", "Nyomtatvány", "Druk")
E("výbor", "committee", "Ausschuss", "bizottság", "komisja")
E("Zobraziť ďalšie", "Show more", "Mehr anzeigen", "Továbbiak", "Pokaż więcej")
E("Hľadám…", "Searching…", "Suche läuft…", "Keresés…", "Szukam…")
E("hľadať aj v hlasovaniach", "also search votes", "auch in Abstimmungen suchen", "keresés a szavazásokban is", "szukaj też w głosowaniach")
E("hľadať v hlasovaniach", "search votes", "in Abstimmungen suchen", "keresés a szavazásokban", "szukaj w głosowaniach")
E("Stránka", "Page", "Seite", "Oldal", "Strona")
E("Fulltextové vyhľadávanie je dostupné na zverejnenej stránke.", "Full-text search is available on the published site.", "Die Volltextsuche ist auf der veröffentlichten Seite verfügbar.", "A teljes szöveges keresés a közzétett oldalon érhető el.", "Wyszukiwanie pełnotekstowe jest dostępne na opublikowanej stronie.")
for sk, en, de, hu, pl in [("rozpočet","budget","Haushalt","költségvetés","budżet"),("zdravotníctvo","healthcare","Gesundheitswesen","egészségügy","ochrona zdrowia"),("konsolidácia","consolidation","Konsolidierung","konszolidáció","konsolidacja"),("Trestný zákon","Criminal Code","Strafgesetzbuch","Büntető törvénykönyv","Kodeks karny"),("dane","taxes","Steuern","adók","podatki"),("školstvo","education","Bildung","oktatásügy","szkolnictwo"),("energie","energy","Energie","energia","energia")]:
    E(sk, en, de, hu, pl)

# ---- follow, changes, 404
E("Sledujem – faktická poznámka", "Following – faktická poznámka", "Folge ich – faktická poznámka", "Követem – faktická poznámka", "Obserwuję – faktická poznámka")
E("Poslanci, ktorých sledujete: ich posledné vystúpenia a hlasovania proti klubu.", "MPs you follow: their latest speeches and votes against their caucus.", "Abgeordnete, denen Sie folgen: ihre letzten Reden und Abstimmungen gegen die Fraktion.", "Az általad követett képviselők: legutóbbi felszólalásaik és frakcióellenes szavazásaik.", "Obserwowani posłowie: ich ostatnie wystąpienia i głosowania przeciw klubowi.")
E("Zoznam je uložený iba v tomto prehliadači.", "The list is stored only in this browser.", "Die Liste ist nur in diesem Browser gespeichert.", "A lista csak ebben a böngészőben tárolódik.", "Lista jest zapisana tylko w tej przeglądarce.")
E("Zatiaľ nikoho nesledujete", "You are not following anyone yet", "Sie folgen noch niemandem", "Még senkit sem követsz", "Jeszcze nikogo nie obserwujesz")
E("V sále otvorte kartu poslanca a ťuknite na Sledovať. Jeho vystúpenia a hlasovania proti klubu sa potom zobrazia tu.", "Open an MP's card in the chamber and tap Follow. Their speeches and votes against their caucus will then appear here.", "Öffnen Sie im Saal die Karte eines Abgeordneten und tippen Sie auf Folgen. Reden und Abstimmungen gegen die Fraktion erscheinen dann hier.", "Nyisd meg egy képviselő kártyáját az ülésteremben, és koppints a Követés gombra. Felszólalásai és frakcióellenes szavazásai itt jelennek meg.", "Otwórz kartę posła na sali i stuknij Obserwuj. Jego wystąpienia i głosowania przeciw klubowi pojawią się tutaj.")
E("Zmeny v zložení parlamentu – faktická poznámka", "Membership changes – faktická poznámka", "Änderungen in der Zusammensetzung – faktická poznámka", "A parlament összetételének változásai – faktická poznámka", "Zmiany w składzie parlamentu – faktická poznámka")
E("Kto nastúpil ako náhradník, komu mandát zanikol alebo sa neuplatňuje (napríklad pri vstupe do vlády). Zdroj: nrsr.sk.", "Who took a seat as a substitute and whose mandate ended or is suspended (for example on joining the government). Source: nrsr.sk.", "Wer als Nachrücker eintrat und wessen Mandat erlosch oder ruht (z. B. bei Eintritt in die Regierung). Quelle: nrsr.sk.", "Ki lépett be pótképviselőként, kinek szűnt meg vagy szünetel a mandátuma (például kormánytaggá válás miatt). Forrás: nrsr.sk.", "Kto objął mandat jako zastępca, komu mandat wygasł lub jest zawieszony (np. po wejściu do rządu). Źródło: nrsr.sk.")
E("Náhradníci, zánik a uplatnenie mandátov poslancov NR SR v IX. volebnom období.", "Substitutes, ended and suspended mandates of MPs in the 9th term.", "Nachrücker, erloschene und ruhende Mandate in der IX. Wahlperiode.", "Pótképviselők, megszűnt és szünetelő mandátumok a IX. ciklusban.", "Zastępcy, wygasłe i zawieszone mandaty posłów w IX kadencji.")
for sk, en, de, hu, pl in [("mandát náhradníka vykonávaný","substitute mandate exercised","Nachrückermandat ausgeübt","pótképviselői mandátum gyakorolva","mandat zastępcy wykonywany"),
  ("mandát náhradníka zaniknutý","substitute mandate ended","Nachrückermandat erloschen","pótképviselői mandátum megszűnt","mandat zastępcy wygasł"),
  ("mandát náhradníka získaný","substitute mandate obtained","Nachrückermandat erhalten","pótképviselői mandátum megszerezve","mandat zastępcy uzyskany"),
  ("mandát sa neuplatňuje","mandate suspended","Mandat ruht","a mandátum szünetel","mandat zawieszony"),
  ("mandát vykonávaný","mandate exercised","Mandat ausgeübt","mandátum gyakorolva","mandat wykonywany"),
  ("mandát zaniknutý","mandate ended","Mandat erloschen","mandátum megszűnt","mandat wygasł")]:
    E(sk, en, de, hu, pl); E(", " + sk, ", " + en, ", " + de, ", " + hu, ", " + pl)
E(["Zložil sľub poslanca", "Zložil sľub poslanca."], "Took the MP's oath", "Legte den Abgeordneteneid ab", "Letette a képviselői esküt", "Złożył ślubowanie poselskie")
E(["Zložila sľub poslanca", "Zložila sľub poslanca."], "Took the MP's oath", "Legte den Abgeordneteneid ab", "Letette a képviselői esküt", "Złożyła ślubowanie poselskie")
E("Stránka neexistuje – faktická poznámka", "Page not found – faktická poznámka", "Seite nicht gefunden – faktická poznámka", "Az oldal nem található – faktická poznámka", "Strona nie istnieje – faktická poznámka")
E("Táto stránka neexistuje", "This page does not exist", "Diese Seite existiert nicht", "Ez az oldal nem létezik", "Ta strona nie istnieje")
E("Adresa je možno preklepnutá alebo hlasovanie ešte nemáme v dátach. Skúste", "The address may be mistyped, or we do not have the vote yet. Try", "Die Adresse ist vielleicht falsch oder die Abstimmung liegt noch nicht vor. Versuchen Sie", "Lehet, hogy elírták a címet, vagy a szavazás még nincs az adataink között. Próbáld", "Adres może zawierać literówkę albo nie mamy jeszcze tego głosowania. Spróbuj")
E("alebo", "or", "oder", "vagy", "lub")
E("zoznam hlasovaní", "the list of votes", "die Liste der Abstimmungen", "a szavazások listáját", "listę głosowań")

# ---- about page
E("O projekte – faktická poznámka", "About – faktická poznámka", "Über das Projekt – faktická poznámka", "A projektről – faktická poznámka", "O projekcie – faktická poznámka")
E("Čo je faktická poznámka, odkiaľ berie dáta, ako počíta štatistiky a ako nás kontaktovať.", "What faktická poznámka is, where its data comes from, how it calculates statistics and how to contact us.", "Was faktická poznámka ist, woher die Daten stammen, wie Statistiken berechnet werden und wie man uns kontaktiert.", "Mi a faktická poznámka, honnan származnak az adatai, hogyan számolja a statisztikákat és hogyan érhetsz el minket.", "Czym jest faktická poznámka, skąd bierze dane, jak liczy statystyki i jak się z nami skontaktować.")
E("Parlament, ktorému sa dá rozumieť", "A parliament you can understand", "Ein Parlament, das man verstehen kann", "Egy parlament, amely érthető", "Parlament, który da się zrozumieć")
E("Faktická poznámka prehľadne ukazuje, ako hlasujú a čo hovoria poslanci Národnej rady SR. Nezávisle, bez reklám, s otvoreným kódom a dátami.", "Faktická poznámka clearly shows how members of the Slovak National Council vote and what they say. Independent, ad-free, with open code and data.", "Faktická poznámka zeigt übersichtlich, wie die Abgeordneten des slowakischen Nationalrats abstimmen und was sie sagen. Unabhängig, werbefrei, mit offenem Code und offenen Daten.", "A Faktická poznámka áttekinthetően mutatja, hogyan szavaznak és mit mondanak a Szlovák Nemzeti Tanács képviselői. Függetlenül, reklámok nélkül, nyílt kóddal és adatokkal.", "Faktická poznámka przejrzyście pokazuje, jak głosują i co mówią posłowie Słowackiej Rady Narodowej. Niezależnie, bez reklam, z otwartym kodem i danymi.")
E("hlasovaní", "votes", "Abstimmungen", "szavazás", "głosowań")
E("vystúpení v rozprave", "speeches in debate", "Reden in der Debatte", "felszólalás a vitában", "wystąpień w debacie")
E("tlačí a zákonov", "prints and bills", "Drucksachen und Gesetze", "nyomtatvány és törvény", "druków i ustaw")
E("poslancov", "MPs", "Abgeordnete", "képviselő", "posłów")
E("Ako to funguje", "How it works", "So funktioniert es", "Hogyan működik", "Jak to działa")
E("Verejné stránky parlamentu: hlasovania, prepisy, tlače, výbory, oznámenia funkcionárov.", "Parliament's public pages: votes, transcripts, prints, committees, officials' declarations.", "Öffentliche Seiten des Parlaments: Abstimmungen, Protokolle, Drucksachen, Ausschüsse, Erklärungen.", "A parlament nyilvános oldalai: szavazások, jegyzőkönyvek, nyomtatványok, bizottságok, nyilatkozatok.", "Publiczne strony parlamentu: głosowania, stenogramy, druki, komisje, oświadczenia.")
E("Automatický zber", "Automatic collection", "Automatische Erfassung", "Automatikus gyűjtés", "Automatyczne pobieranie")
E("Každú hodinu počas pracovných dní skript stiahne nové údaje a skontroluje ich.", "Every hour on working days a script downloads new data and checks it.", "Jede Stunde an Werktagen lädt ein Skript neue Daten herunter und prüft sie.", "Munkanapokon óránként egy szkript letölti és ellenőrzi az új adatokat.", "Co godzinę w dni robocze skrypt pobiera nowe dane i je sprawdza.")
E("Výpočty", "Calculations", "Berechnungen", "Számítások", "Obliczenia")
E("Účasť, súlad s klubom, stav zákonov a ďalšie ukazovatele podľa metodiky nižšie.", "Attendance, caucus loyalty, bill status and other measures according to the methodology below.", "Teilnahme, Fraktionstreue, Gesetzesstatus und weitere Kennzahlen nach der Methodik unten.", "Részvétel, frakcióhűség, törvények állapota és más mutatók az alábbi módszertan szerint.", "Obecność, zgodność z klubem, stan ustaw i inne wskaźniki według poniższej metodologii.")
E("Nová verzia sa zverejní do pár minút. Pri každom údaji je odkaz na pôvodný zdroj.", "A new version is published within minutes. Every figure links to its original source.", "Eine neue Version erscheint innerhalb weniger Minuten. Jede Angabe verlinkt auf die Originalquelle.", "Az új verzió percek alatt megjelenik. Minden adatnál link vezet az eredeti forráshoz.", "Nowa wersja publikowana jest w ciągu kilku minut. Każda dana ma odnośnik do źródła.")
E("Metodika", "Methodology", "Methodik", "Módszertan", "Metodologia")
E("Ako počítame jednotlivé čísla. Kliknutím rozbalíte.", "How we calculate each figure. Click to expand.", "Wie wir die einzelnen Zahlen berechnen. Zum Aufklappen klicken.", "Hogyan számoljuk az egyes számokat. Kattints a kibontáshoz.", "Jak liczymy poszczególne wartości. Kliknij, aby rozwinąć.")
E("Stav zákona", "Bill status", "Gesetzesstatus", "A törvény állapota", "Stan ustawy")
E("Tesné hlasovania a súdržnosť", "Close votes and cohesion", "Knappe Abstimmungen und Geschlossenheit", "Szoros szavazások és kohézió", "Wyrównane głosowania i spójność")
E("Charakteristické slová", "Characteristic words", "Charakteristische Wörter", "Jellemző szavak", "Charakterystyczne słowa")
E("Aktivita poslancov", "MP activity", "Aktivität der Abgeordneten", "Képviselői aktivitás", "Aktywność posłów")
E("AI zhrnutia vystúpení", "AI summaries of speeches", "KI-Zusammenfassungen der Reden", "MI-összefoglalók a felszólalásokról", "Podsumowania AI wystąpień")
E("Čo nepočítame", "What we do not count", "Was wir nicht zählen", "Amit nem számolunk", "Czego nie liczymy")
E("Časté otázky", "FAQ", "Häufige Fragen", "Gyakori kérdések", "Częste pytania")
E("Je to oficiálna stránka parlamentu?", "Is this the official parliament website?", "Ist das die offizielle Seite des Parlaments?", "Ez a parlament hivatalos oldala?", "Czy to oficjalna strona parlamentu?")
E("Ako často sa údaje obnovujú?", "How often is the data updated?", "Wie oft werden die Daten aktualisiert?", "Milyen gyakran frissülnek az adatok?", "Jak często dane są aktualizowane?")
E("Môžem dáta použiť?", "Can I use the data?", "Darf ich die Daten verwenden?", "Felhasználhatom az adatokat?", "Czy mogę używać danych?")
E("Odkiaľ sú fotografie?", "Where are the photos from?", "Woher stammen die Fotos?", "Honnan származnak a fényképek?", "Skąd pochodzą zdjęcia?")
E("Ako sledovať konkrétneho poslanca?", "How do I follow a particular MP?", "Wie folge ich einem bestimmten Abgeordneten?", "Hogyan követhetek egy adott képviselőt?", "Jak obserwować konkretnego posła?")
E("Napíšte nám", "Write to us", "Schreiben Sie uns", "Írj nekünk", "Napisz do nas")
E("Našli ste chybu alebo máte nápad? kontakt@faktickapoznamka.sk", "Found a mistake or have an idea? kontakt@faktickapoznamka.sk", "Fehler gefunden oder eine Idee? kontakt@faktickapoznamka.sk", "Hibát találtál vagy ötleted van? kontakt@faktickapoznamka.sk", "Znalazłeś błąd lub masz pomysł? kontakt@faktickapoznamka.sk")
E("Otvorený kód a dáta", "Open code and data", "Offener Code und Daten", "Nyílt kód és adatok", "Otwarty kod i dane")
E("Všetko je verejné na GitHube, môžete to voľne použiť.", "Everything is public on GitHub; feel free to use it.", "Alles ist öffentlich auf GitHub und frei verwendbar.", "Minden nyilvános a GitHubon, szabadon felhasználható.", "Wszystko jest publiczne na GitHubie, możesz z tego swobodnie korzystać.")
E("RSS kanál", "RSS feed", "RSS-Feed", "RSS-csatorna", "Kanał RSS")
E("Nové hlasovania priamo vo vašej čítačke. Každý poslanec má aj vlastný kanál.", "New votes straight into your reader. Every MP also has their own feed.", "Neue Abstimmungen direkt in Ihrem Reader. Jeder Abgeordnete hat auch einen eigenen Feed.", "Új szavazások közvetlenül az olvasódba. Minden képviselőnek saját csatornája is van.", "Nowe głosowania prosto w czytniku. Każdy poseł ma też własny kanał.")
