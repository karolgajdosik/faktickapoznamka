# UI dictionary, part 5: About page methodology and FAQ answers.
from dict1 import E

E("Podiel hlasovaní, pri ktorých poslanec nebol vedený ako neprítomný. Neprítomnosť považujeme za ospravedlnenú, ak má poslanec v daný deň zapísané ospravedlnenie na nrsr.sk; neospravedlnená môže byť aj krátka neprítomnosť počas rokovacieho dňa.",
  "Share of votes at which the MP was not recorded as absent. An absence counts as excused if the MP has an excuse recorded for that day on nrsr.sk; an unexcused absence can also be a short absence during a sitting day.",
  "Anteil der Abstimmungen, bei denen die/der Abgeordnete nicht als abwesend geführt wurde. Eine Abwesenheit gilt als entschuldigt, wenn für den Tag auf nrsr.sk eine Entschuldigung eingetragen ist; unentschuldigt kann auch eine kurze Abwesenheit während eines Sitzungstags sein.",
  "Azon szavazások aránya, amelyeken a képviselőt nem jegyezték távollévőként. A távollétet igazoltnak tekintjük, ha az adott napra az nrsr.sk-n igazolás szerepel; igazolatlan lehet egy ülésnapon belüli rövid távollét is.",
  "Odsetek głosowań, na których poseł nie był odnotowany jako nieobecny. Nieobecność uznajemy za usprawiedliwioną, jeśli na dany dzień na nrsr.sk zapisano usprawiedliwienie; nieusprawiedliwiona może być też krótka nieobecność w dniu obrad.")
E("Podiel hlasovaní, v ktorých poslanec hlasoval rovnako ako väčšina jeho klubu (počítajú sa len hlasy za, proti a zdržal sa). Klub berieme podľa stavu v čase hlasovania. Ak klub nemal jasnú väčšinu, hlasovanie sa nepočíta. Pri nezaradených poslancoch sa súlad nepočíta.",
  "Share of votes in which the MP voted with the caucus majority (only for, against and abstain count). The caucus is taken as it was at the time of the vote. If the caucus had no clear majority, the vote is not counted. Loyalty is not calculated for independent MPs.",
  "Anteil der Abstimmungen, in denen die/der Abgeordnete wie die Fraktionsmehrheit stimmte (gezählt werden nur dafür, dagegen und Enthaltung). Maßgeblich ist die Fraktion zum Zeitpunkt der Abstimmung. Ohne klare Fraktionsmehrheit wird die Abstimmung nicht gezählt. Für fraktionslose Abgeordnete wird keine Treue berechnet.",
  "Azon szavazások aránya, amelyekben a képviselő a frakciótöbbséggel együtt szavazott (csak az igen, nem és tartózkodás számít). A frakciót a szavazás időpontja szerint vesszük. Ha a frakciónak nem volt egyértelmű többsége, a szavazás nem számít. A független képviselőknél frakcióhűséget nem számolunk.",
  "Odsetek głosowań, w których poseł głosował jak większość jego klubu (liczą się tylko głosy za, przeciw i wstrzymujące się). Klub ustalamy według stanu w chwili głosowania. Jeśli klub nie miał wyraźnej większości, głosowanie nie jest liczone. Dla posłów niezrzeszonych zgodności nie liczymy.")
E(["Podiel hlasovaní, v ktorých dvaja poslanci hlasovali rovnako, spomedzi tých, kde obaja hlasovali za, proti alebo sa zdržali (aspoň {n} spoločných hlasovaní)."],
  "Share of votes in which two MPs voted the same way, among those where both voted for, against or abstained (at least {n} shared votes).",
  "Anteil der Abstimmungen, in denen zwei Abgeordnete gleich stimmten, unter denen, bei denen beide dafür, dagegen oder mit Enthaltung stimmten (mindestens {n} gemeinsame Abstimmungen).",
  "Azon szavazások aránya, amelyekben két képviselő ugyanúgy szavazott, azok közül, ahol mindketten igennel, nemmel szavaztak vagy tartózkodtak (legalább {n} közös szavazás).",
  "Odsetek głosowań, w których dwóch posłów głosowało tak samo, spośród tych, w których obaj głosowali za, przeciw lub się wstrzymali (co najmniej {n} wspólnych głosowań).")
E(["„Schválený“ alebo „neschválený“ podľa záverečného hlasovania v treťom čítaní (pri uzneseniach, voľbách a správach podľa posledného hlasovania). „V procese“ pri aktivite za posledné {n} mesiace, inak „bez záverečného hlasovania“. Oficiálny priebeh vrátane čísla v Zbierke zákonov preberáme z nrsr.sk."],
  "“Passed” or “rejected” according to the final third-reading vote (for resolutions, elections and reports, the last vote). “In progress” with activity in the last {n} months, otherwise “no final vote”. The official progress, including the Collection of Laws number, comes from nrsr.sk.",
  "„Angenommen“ oder „abgelehnt“ nach der Schlussabstimmung in dritter Lesung (bei Beschlüssen, Wahlen und Berichten nach der letzten Abstimmung). „In Bearbeitung“ bei Aktivität in den letzten {n} Monaten, sonst „ohne Schlussabstimmung“. Den offiziellen Verlauf einschließlich der Nummer in der Gesetzessammlung übernehmen wir von nrsr.sk.",
  "„Elfogadva” vagy „elutasítva” a harmadik olvasat zárószavazása szerint (határozatoknál, választásoknál és jelentéseknél az utolsó szavazás szerint). „Folyamatban”, ha az elmúlt {n} hónapban volt aktivitás, egyébként „zárószavazás nélkül”. A hivatalos menetet a Törvénytár-számmal együtt az nrsr.sk-ról vesszük át.",
  "„Przyjęta” lub „odrzucona” według głosowania końcowego w trzecim czytaniu (przy uchwałach, wyborach i sprawozdaniach według ostatniego głosowania). „W toku” przy aktywności w ostatnich {n} miesiącach, w przeciwnym razie „bez głosowania końcowego”. Oficjalny przebieg wraz z numerem w Zbiorze ustaw pobieramy z nrsr.sk.")
E(["Tesné hlasovanie je také, o ktorom rozhodlo najviac {n} hlasov. Súdržnosť klubu je Riceov/Hixov index zhody: {n} % znamená, že všetci členovia hlasovali rovnako."],
  "A close vote is one decided by at most {n} votes. Caucus cohesion is the Rice/Hix agreement index: {n} % means all members voted the same way.",
  "Eine knappe Abstimmung wird mit höchstens {n} Stimmen entschieden. Die Geschlossenheit ist der Rice/Hix-Übereinstimmungsindex: {n} % bedeutet, dass alle Mitglieder gleich stimmten.",
  "Szoros szavazás az, amelyről legfeljebb {n} szavazat döntött. A frakciókohézió a Rice/Hix-egyezési index: {n} % azt jelenti, hogy minden tag ugyanúgy szavazott.",
  "Wyrównane głosowanie to takie, o którym zdecydowało najwyżej {n} głosów. Spójność klubu to indeks zgodności Rice'a/Hixa: {n} % oznacza, że wszyscy członkowie głosowali tak samo.")
E("Slová, ktoré poslanec v rozprave používa výrazne častejšie ako ostatní, počítané metódou TF-IDF zo stenografických prepisov, bez vlastných mien, rokovacích fráz a vystúpení predsedajúceho.",
  "Words an MP uses in debate much more often than others, computed with TF-IDF from the stenographic transcripts, excluding proper names, procedural phrases and the chair's remarks.",
  "Wörter, die eine Abgeordnete oder ein Abgeordneter in Debatten deutlich häufiger verwendet als andere, berechnet per TF-IDF aus den stenografischen Protokollen, ohne Eigennamen, Verfahrensfloskeln und Beiträge des Vorsitzes.",
  "Szavak, amelyeket a képviselő a vitákban jóval gyakrabban használ, mint mások, TF-IDF módszerrel számolva a gyorsírásos jegyzőkönyvekből, tulajdonnevek, eljárási fordulatok és a levezető elnök felszólalásai nélkül.",
  "Słowa, których poseł używa w debacie znacznie częściej niż inni, liczone metodą TF-IDF ze stenogramów, bez nazw własnych, zwrotów proceduralnych i wypowiedzi przewodniczącego.")
E("Ospravedlnenia, návrhy zákonov, pozmeňujúce návrhy, interpelácie, zahraničné cesty, kancelárie, výbory a zmeny v zložení parlamentu preberáme z nrsr.sk a obnovujeme približne raz týždenne.",
  "Excuses, bills, amendments, interpellations, trips abroad, offices, committees and membership changes come from nrsr.sk and are refreshed about once a week.",
  "Entschuldigungen, Gesetzentwürfe, Änderungsanträge, Interpellationen, Auslandsreisen, Büros, Ausschüsse und Änderungen der Zusammensetzung übernehmen wir von nrsr.sk und aktualisieren sie etwa einmal pro Woche.",
  "Az igazolásokat, törvényjavaslatokat, módosító javaslatokat, interpellációkat, külföldi utakat, irodákat, bizottságokat és összetételi változásokat az nrsr.sk-ról vesszük át, és nagyjából hetente frissítjük.",
  "Usprawiedliwienia, projekty ustaw, poprawki, interpelacje, podróże zagraniczne, biura, komisje i zmiany w składzie parlamentu pobieramy z nrsr.sk i odświeżamy mniej więcej raz w tygodniu.")
E("Z oznámení verejných funkcionárov uvádzame príjmy, funkcie, zamestnanie, podnikanie a druhy a počty majetku. Presné polohy nehnuteľností (katastrálne územia, listy vlastníctva) zámerne neuvádzame; celé oznámenie je dostupné cez odkaz na nrsr.sk.",
  "From public officials' declarations we show income, positions, employment, business activity and the types and numbers of assets. We deliberately do not show exact property locations (cadastral areas, title deeds); the full declaration is available via the link to nrsr.sk.",
  "Aus den Erklärungen öffentlicher Amtsträger zeigen wir Einkünfte, Funktionen, Beschäftigung, unternehmerische Tätigkeit sowie Arten und Anzahl der Vermögenswerte. Genaue Lagen von Immobilien (Katastergebiete, Grundbuchblätter) zeigen wir bewusst nicht; die vollständige Erklärung ist über den Link zu nrsr.sk abrufbar.",
  "A közfunkcionáriusi nyilatkozatokból a jövedelmet, tisztségeket, munkaviszonyt, vállalkozást, valamint a vagyon típusát és mennyiségét közöljük. Az ingatlanok pontos helyét (kataszteri terület, tulajdoni lap) szándékosan nem közöljük; a teljes nyilatkozat az nrsr.sk linkjén érhető el.",
  "Z oświadczeń funkcjonariuszy publicznych podajemy dochody, funkcje, zatrudnienie, działalność gospodarczą oraz rodzaje i liczbę składników majątku. Celowo nie podajemy dokładnych lokalizacji nieruchomości (obręby katastralne, księgi wieczyste); pełne oświadczenie jest dostępne przez odnośnik do nrsr.sk.")
E("Pri dlhších vystúpeniach zobrazujeme krátke zhrnutie označené „AI zhrnutie“. Vytvára ho jazykový model (GitHub Models) výlučne z oficiálneho prepisu, s pokynom zachovať nestrannosť a nič nepridávať. Zhrnutie môže byť nepresné, rozhoduje celý prepis.",
  "For longer speeches we show a short summary marked “AI summary”. It is written by a language model (GitHub Models) solely from the official transcript, instructed to stay impartial and add nothing. A summary may be inaccurate; the full transcript is authoritative. Summaries are in Slovak.",
  "Bei längeren Reden zeigen wir eine kurze, als „KI-Zusammenfassung“ gekennzeichnete Zusammenfassung. Sie wird von einem Sprachmodell (GitHub Models) ausschließlich aus dem offiziellen Protokoll erstellt, mit der Vorgabe, unparteiisch zu bleiben und nichts hinzuzufügen. Sie kann ungenau sein; maßgeblich ist das vollständige Protokoll. Zusammenfassungen sind auf Slowakisch.",
  "Hosszabb felszólalásoknál rövid, „MI-összefoglaló” jelölésű összefoglalót mutatunk. Ezt egy nyelvi modell (GitHub Models) kizárólag a hivatalos jegyzőkönyvből készíti, azzal az utasítással, hogy maradjon pártatlan és ne tegyen hozzá semmit. Az összefoglaló pontatlan lehet, a teljes jegyzőkönyv a mérvadó. Az összefoglalók szlovák nyelvűek.",
  "Przy dłuższych wystąpieniach pokazujemy krótkie podsumowanie oznaczone „Podsumowanie AI”. Tworzy je model językowy (GitHub Models) wyłącznie na podstawie oficjalnego stenogramu, z poleceniem zachowania bezstronności i niedodawania niczego. Podsumowanie może być niedokładne; rozstrzyga pełny stenogram. Podsumowania są po słowacku.")
E("Prezentácie (kontroly prítomnosti) neuvádzame v štatistikách, lebo sa pri nich o ničom nerozhoduje. Kluby sú v sále zoradené podľa veľkosti a ich farby sú neutrálne, nie stranícke.",
  "Attendance checks are left out of the statistics because nothing is decided in them. Caucuses in the chamber are ordered by size, and their colours are neutral, not party colours.",
  "Anwesenheitsfeststellungen fließen nicht in die Statistiken ein, da dabei nichts entschieden wird. Die Fraktionen sind im Saal nach Größe geordnet, ihre Farben sind neutral, nicht die der Parteien.",
  "A jelenléti ellenőrzéseket nem számoljuk a statisztikákba, mert azokon nem döntenek semmiről. A frakciók az ülésteremben méret szerint vannak sorba rendezve, színeik semlegesek, nem pártszínek.",
  "Sprawdzeń obecności nie uwzględniamy w statystykach, bo nic się w nich nie rozstrzyga. Kluby na sali są ułożone według wielkości, a ich kolory są neutralne, nie partyjne.")
E("Nie. Faktická poznámka je nezávislý projekt bez väzby na Národnú radu SR, vládu či politické strany. Ak sa údaj líši od nrsr.sk, platí nrsr.sk.",
  "No. Faktická poznámka is an independent project with no ties to the National Council, the government or political parties. If a figure differs from nrsr.sk, nrsr.sk prevails.",
  "Nein. Faktická poznámka ist ein unabhängiges Projekt ohne Verbindung zum Nationalrat, zur Regierung oder zu Parteien. Weicht eine Angabe von nrsr.sk ab, gilt nrsr.sk.",
  "Nem. A Faktická poznámka független projekt, nincs kapcsolata a Nemzeti Tanáccsal, a kormánnyal vagy pártokkal. Ha egy adat eltér az nrsr.sk-tól, az nrsr.sk a mérvadó.",
  "Nie. Faktická poznámka to niezależny projekt bez powiązań z Radą Narodową, rządem czy partiami. Jeśli dana różni się od nrsr.sk, obowiązuje nrsr.sk.")
E("Hlasovania a rozprava sa kontrolujú každú hodinu počas pracovných dní. Aktivita poslancov, výbory a majetkové priznania približne raz týždenne.",
  "Votes and debate are checked every hour on working days. MP activity, committees and asset declarations about once a week.",
  "Abstimmungen und Debatte werden an Werktagen stündlich geprüft. Aktivität der Abgeordneten, Ausschüsse und Vermögenserklärungen etwa einmal pro Woche.",
  "A szavazásokat és a vitát munkanapokon óránként ellenőrizzük. A képviselői aktivitást, a bizottságokat és a vagyonnyilatkozatokat nagyjából hetente.",
  "Głosowania i debatę sprawdzamy co godzinę w dni robocze. Aktywność posłów, komisje i oświadczenia majątkowe mniej więcej raz w tygodniu.")
E("Áno. Kód aj dáta sú verejné na GitHube a môžete ich voľne použiť, uvítame uvedenie zdroja.",
  "Yes. Code and data are public on GitHub and you may use them freely; crediting the source is appreciated.",
  "Ja. Code und Daten sind öffentlich auf GitHub und frei nutzbar; über eine Quellenangabe freuen wir uns.",
  "Igen. A kód és az adatok nyilvánosak a GitHubon, szabadon felhasználhatók; örülünk a forrás megjelölésének.",
  "Tak. Kod i dane są publiczne na GitHubie i można z nich swobodnie korzystać; prosimy o podanie źródła.")
E("Väčšina zo stránky politicheck.sk (pôvodne oficiálne portréty poslancov NR SR). Fotografie J. Ferenčáka, Ľ. Galka, T. Tarabu a R. Vašečku sú z Wikimedia Commons pod licenciami Creative Commons (autor a licencia sú na stránke každého súboru: CoR_Members_portraits_-_Jan_FERENCAK.jpg, Lubomir_Galko.jpg, Tomáš_Taraba_in_May_2026.jpg, Vasecka.jpg), fotografia M. Kováča zo stránky sns.sk. Fotografie sú orezané a zmenšené. Kde fotografia chýba, zobrazujeme iniciály.",
  "Most come from politicheck.sk (originally official portraits of MPs). Photos of J. Ferenčák, Ľ. Galko, T. Taraba and R. Vašečka are from Wikimedia Commons under Creative Commons licences (author and licence are on each file's page: CoR_Members_portraits_-_Jan_FERENCAK.jpg, Lubomir_Galko.jpg, Tomáš_Taraba_in_May_2026.jpg, Vasecka.jpg); the photo of M. Kováč is from sns.sk. Photos are cropped and resized. Where a photo is missing, we show initials.",
  "Die meisten stammen von politicheck.sk (ursprünglich offizielle Porträts der Abgeordneten). Fotos von J. Ferenčák, Ľ. Galko, T. Taraba und R. Vašečka stammen von Wikimedia Commons unter Creative-Commons-Lizenzen (Urheber und Lizenz auf der Seite jeder Datei: CoR_Members_portraits_-_Jan_FERENCAK.jpg, Lubomir_Galko.jpg, Tomáš_Taraba_in_May_2026.jpg, Vasecka.jpg), das Foto von M. Kováč von sns.sk. Die Fotos sind zugeschnitten und verkleinert. Fehlt ein Foto, zeigen wir Initialen.",
  "A legtöbb a politicheck.sk oldalról származik (eredetileg a képviselők hivatalos portréi). J. Ferenčák, Ľ. Galko, T. Taraba és R. Vašečka fotói a Wikimedia Commonsról származnak Creative Commons licenccel (a szerző és a licenc minden fájl oldalán: CoR_Members_portraits_-_Jan_FERENCAK.jpg, Lubomir_Galko.jpg, Tomáš_Taraba_in_May_2026.jpg, Vasecka.jpg), M. Kováč fotója a sns.sk oldalról. A fotókat körbevágtuk és kicsinyítettük. Ahol hiányzik a fotó, monogramot mutatunk.",
  "Większość pochodzi z politicheck.sk (pierwotnie oficjalne portrety posłów). Zdjęcia J. Ferenčáka, Ľ. Galka, T. Taraby i R. Vašečki pochodzą z Wikimedia Commons na licencjach Creative Commons (autor i licencja na stronie każdego pliku: CoR_Members_portraits_-_Jan_FERENCAK.jpg, Lubomir_Galko.jpg, Tomáš_Taraba_in_May_2026.jpg, Vasecka.jpg), zdjęcie M. Kováča z sns.sk. Zdjęcia są przycięte i pomniejszone. Gdy brak zdjęcia, pokazujemy inicjały.")
E("Na profile poslanca kliknite na Sledovať, alebo si pridajte jeho RSS kanál. Novinky zo všetkých hlasovaní sú v RSS kanáli hlasovaní.",
  "Click Follow on the MP's profile, or add their RSS feed. News from all votes is in the votes RSS feed.",
  "Klicken Sie im Profil auf Folgen oder abonnieren Sie den RSS-Feed. Neues aus allen Abstimmungen steht im RSS-Feed der Abstimmungen.",
  "A képviselő profilján kattints a Követés gombra, vagy add hozzá az RSS-csatornáját. Az összes szavazás újdonságai a szavazások RSS-csatornájában vannak.",
  "Na profilu posła kliknij Obserwuj albo dodaj jego kanał RSS. Nowości ze wszystkich głosowań są w kanale RSS głosowań.")
E("Kontakt", "Contact", "Kontakt", "Kapcsolat", "Kontakt")
E("Zdroj dát:", "Data source:", "Datenquelle:", "Adatforrás:", "Źródło danych:")
E("Fotografie:", "Photos:", "Fotos:", "Fotók:", "Zdjęcia:")
E("Preložené je ovládanie stránky. Názvy zákonov, prepisy rozpravy a mená ostávajú po slovensky, tak ako ich zverejňuje NR SR.",
  "The site's interface is translated. Bill titles, debate transcripts and names stay in Slovak, as published by parliament.",
  "Übersetzt ist die Bedienoberfläche. Gesetzestitel, Debattenprotokolle und Namen bleiben auf Slowakisch, wie sie das Parlament veröffentlicht.",
  "Az oldal kezelőfelülete van lefordítva. A törvények címe, a vitajegyzőkönyvek és a nevek szlovákul maradnak, ahogy a parlament közzéteszi őket.",
  "Przetłumaczony jest interfejs strony. Tytuły ustaw, stenogramy debat i nazwiska pozostają po słowacku, tak jak publikuje je parlament.")
E("↺ Obnoviť pôvodné nastavenia", "↺ Restore default settings", "↺ Standardeinstellungen wiederherstellen", "↺ Eredeti beállítások visszaállítása", "↺ Przywróć ustawienia domyślne")
E("Slovenčina, pôvodná veľkosť písma, bežný kontrast, animácie a farebný režim podľa systému.",
  "Slovak, default text size, normal contrast, animations on and colour theme from the system.",
  "Slowakisch, Standardschriftgröße, normaler Kontrast, Animationen an und Farbmodus nach System.",
  "Szlovák nyelv, eredeti betűméret, normál kontraszt, animációk és a rendszer szerinti színmód.",
  "Słowacki, domyślny rozmiar tekstu, zwykły kontrast, animacje i tryb kolorów według systemu.")
E("Hľadať v prepisoch", "Search transcripts", "In Protokollen suchen", "Keresés a jegyzőkönyvekben", "Szukaj w stenogramach")
E("Nezaradení", "Non-attached", "Fraktionslos", "Független", "Niezrzeszeni")
E(["Nezaradení {n}"], "Non-attached {n}", "Fraktionslos {n}", "Független {n}", "Niezrzeszeni {n}")
E(["Nezaradení: {n}"], "Non-attached: {n}", "Fraktionslos: {n}", "Független: {n}", "Niezrzeszeni: {n}")
E("poslanci NR SR", "MPs", "Abgeordnete", "képviselők", "posłowie")
E(["{n} za, {n} proti, {n} zdržal"], "{n} for, {n} against, {n} abstained", "{n} dafür, {n} dagegen, {n} Enthaltung", "{n} igen, {n} nem, {n} tartózkodott", "{n} za, {n} przeciw, {n} wstrzym.")
for sk, en, de, hu, pl in [
  ("NZ postúpil do redakcie", "Bill moved to editing", "Entwurf an die Redaktion übergeben", "A javaslat szerkesztésre került", "Projekt skierowany do redakcji"),
  ("NZ postúpil do II. čítania.", "Bill moved to second reading.", "Entwurf in die zweite Lesung überwiesen.", "A javaslat második olvasatba került.", "Projekt skierowany do drugiego czytania."),
  ("NZ postúpil do III. čítania.", "Bill moved to third reading.", "Entwurf in die dritte Lesung überwiesen.", "A javaslat harmadik olvasatba került.", "Projekt skierowany do trzeciego czytania."),
  ("NZ postupuje do redakcie.", "Bill moves to editing.", "Entwurf geht in die Redaktion.", "A javaslat szerkesztésre kerül.", "Projekt przechodzi do redakcji."),
  ("Príprava informácie k NZ.", "Preparing information on the bill.", "Vorbereitung der Information zum Entwurf.", "Tájékoztatás előkészítése a javaslatról.", "Przygotowanie informacji o projekcie."),
  ("NZ vzatý späť", "Bill withdrawn", "Entwurf zurückgezogen", "A javaslatot visszavonták", "Projekt wycofany"),
  ("NZ nebol schválený", "Bill not passed", "Entwurf nicht angenommen", "A javaslatot nem fogadták el", "Projekt nie został przyjęty"),
  ("NR SR nepokračuje v rokovaní o NZ", "Parliament will not continue debating the bill", "Der Nationalrat setzt die Beratung des Entwurfs nicht fort", "A parlament nem folytatja a javaslat tárgyalását", "Parlament nie kontynuuje prac nad projektem"),
  ("Zákon vyšiel v Zbierke zákonov", "Law published in the Collection of Laws", "Gesetz in der Gesetzessammlung veröffentlicht", "A törvény megjelent a Törvénytárban", "Ustawa opublikowana w Zbiorze ustaw"),
]:
    E(sk, en, de, hu, pl)
E(["NZ bol prerokovaný na {n}. schôdzi NR SR, uznesenie číslo {n} zo dňa {n}. {n}. {n}", "NZ bol prerokovaný na {n}. schôdzi NR SR, uznesenie číslo {n} zo dňa {n}. {n}. {n}."],
  "Bill debated at session {n}, resolution no. {n} of {n}. {n}. {n}", "Entwurf in der {n}. Sitzung beraten, Beschluss Nr. {n} vom {n}. {n}. {n}", "A javaslatot a(z) {n}. ülésszakon tárgyalták, {n}. számú határozat, {n}. {n}. {n}.", "Projekt rozpatrzony na {n}. posiedzeniu, uchwała nr {n} z dnia {n}. {n}. {n}")
E(["NZ bol prerokovaný na {n}. schôdzi NR SR dňa {n}. {n}. {n}."], "Bill debated at session {n} on {n}. {n}. {n}.", "Entwurf in der {n}. Sitzung am {n}. {n}. {n} beraten.", "A javaslatot a(z) {n}. ülésszakon tárgyalták, {n}. {n}. {n}.", "Projekt rozpatrzony na {n}. posiedzeniu dnia {n}. {n}. {n}.")
