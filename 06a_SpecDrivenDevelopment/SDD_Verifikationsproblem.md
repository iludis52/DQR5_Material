# Verifikation in agentischer Softwareentwicklung

*Beobachtungen und Abgleich mit dem Stand der Technik · Stand 02.09.2026*

---

## 1. Zweck dieses Dokuments

Es hält eine Fehlerklasse fest, die bei der Umsetzung von Software durch KI-Agenten regelmäßig auftritt, ordnet sie in die veröffentlichte Praxis- und Forschungslage ein und leitet daraus Regeln ab, die unabhängig von Projekt, Werkzeug und Modell gelten.

Die Kernaussage in einem Satz: **Die Qualität agentisch erzeugter Software hängt weniger vom Modell ab als davon, ob es ein Abnahmesignal gibt, das die umsetzende Instanz nicht selbst erzeugt hat.**

---

## 2. Die Fehlerklasse

### 2.1 Beobachtungsmuster

Ein Projekt wird mit einem sorgfältig aufgebauten Prompt-Set und einer expliziten Arbeitsverfassung umgesetzt. Die umsetzende Instanz arbeitet erkennbar diszipliniert: sie schreibt Tests, sie nutzt ein anerkanntes Testframework, sie meldet grüne Läufe. Das Ergebnis enthält gleichwohl schwere Mängel, die bei der ersten echten Benutzung sofort auffallen — und zwar solche, die kein Test angezeigt hat. Es folgen mehrere Korrekturrunden, die den Aufwand vervielfachen, ohne dass sich die zugrunde liegende Ursache ändert.

Übergibt man dasselbe Projekt einer Umgebung, in der eine Instanz die gebaute Anwendung **selbst starten und bedienen** kann, treten dieselben Mängel innerhalb eines Durchlaufs zutage.

### 2.2 Was daran nicht die Ursache ist

* **Nicht die Modellqualität.** Sie beeinflusst die Ausbeute, erklärt aber nicht, warum Mängel systematisch unentdeckt bleiben, die eine andere Umgebung sofort findet.
* **Nicht fehlende Tests.** Es gab Tests, sie liefen, sie waren grün.
* **Nicht mangelnde Prozessdisziplin.** Ein ausgearbeiteter Prozess kann diese Fehlerklasse sogar verdecken, weil er Belege produziert, die geprüft aussehen.

### 2.3 Was die Ursache ist

Zwei voneinander unabhängige Lücken, die sich gegenseitig verstärken:

**(a) Endogene Verifikation.** Dieselbe Instanz leitet aus der Spezifikation ihre Lesart ab, schreibt daraus den Code **und** die Tests. Alle drei Artefakte stammen aus derselben Interpretation. Ist die Interpretation falsch, bestätigen die Tests genau diesen Fehler. Der Grünstand belegt dann Widerspruchsfreiheit, nicht Richtigkeit.

**(b) Fehlende Ausführung.** Tests werden erzeugt, aber nicht gegen ein laufendes Artefakt in einer vollständigen Umgebung ausgeführt — oder nur so weit, wie es ohne Bedienung der Oberfläche geht. Alles, was sich erst im Betrieb zeigt, sammelt sich bis zur Abnahme an.

Die Kombination erzeugt den charakteristischen Zustand: **hoher Nachweisaufwand bei niedriger Nachweiskraft.**

---

## 3. Einordnung in den Stand der Technik

### 3.1 Der Begriff Harness

Als Harness gilt alles an einem Agenten außer dem Modell: die Ausführungsschleife, die verfügbaren Werkzeuge, die Sandbox, das Gedächtnis über Sitzungsgrenzen, die Regeln darüber, was in den Kontext gelangt. Kurzformel: *Agent = Modell + Harness*.

Die veröffentlichten Messungen zeigen, dass die Streuung zwischen Harnesses die Streuung zwischen Modellen übertreffen kann:

| Beobachtung | Wirkung |
| --- | --- |
| Cursor, Benchmark-Untersuchung | dasselbe Modell 46 % gegenüber 80 % unter zwei Harnesses |
| Princeton, CORE-Bench | ein Modell 42 % gegenüber 78 % unter zwei Scaffolds |
| LangChain, Terminal Bench | 52,8 % auf 66,5 % allein durch Harness-Änderung |
| Vercel | Erfolgsquote 80 % auf 100 % nach Entfernen von 80 % der Werkzeuge |

*Diese Zahlen stammen aus Hersteller- und Praxisberichten, nicht aus unabhängiger Replikation. Die Größenordnung ist über mehrere Quellen konsistent, die Einzelwerte sind es nicht notwendig.*

Praktische Folgerung: Wer Qualitätsprobleme durch Modellwechsel lösen will, verschiebt sie. Die Investition gehört zuerst in die Rückmeldeschicht.

### 3.2 Guides und Sensoren

Birgitta Böckeler (Thoughtworks) beschreibt den Harness auf martinfowler.com als Regelkreis aus zwei Richtungen: **Guides** wirken vorwärts (Anweisungen, Konventionen, Spezifikationen — sie erhöhen die Wahrscheinlichkeit, dass etwas Richtiges entsteht), **Sensoren** wirken rückwärts (Messungen am Ergebnis — sie stellen fest, was tatsächlich entstanden ist). Beide gibt es in rechnerischer und in inferentieller Ausprägung, also als Werkzeuglauf oder als Urteil eines Modells.

Sie unterscheidet drei Regelungsbereiche nach Schwierigkeit:

1. **Wartbarkeit** — Komplexität, Duplizierung, Stil. Gut beherrschbar durch rechnerische Sensoren.
2. **Architekturkonformität** — Struktur, Beobachtbarkeit, Leistungseigenschaften. Beherrschbar durch Fitnessfunktionen.
3. **Verhalten** — funktionale Richtigkeit. Von ihr sagt sie, sie sei der Elefant im Raum: Verhaltensprüfung stützt sich weitgehend auf agentengenerierte Tests, und ein Agent, der die Anforderung missversteht, erzeugt Tests, die sein Missverständnis bestätigen.

Damit ist die unter 2.3 (a) beschriebene Lücke nicht ein Einzelbefund, sondern der offene Punkt des Feldes.

### 3.3 Das Orakelproblem

Der zugehörige Fachbegriff ist älter als die Sache: das **Orakelproblem** bezeichnet die Schwierigkeit, für eine gegebene Eingabe die richtige Ausgabe überhaupt zu bestimmen. Die aktuelle Forschungslage überträgt es auf agentisch erzeugte Tests:

* Von Sprachmodellen erzeugte Zusicherungen bilden eher das **tatsächliche** als das **beabsichtigte** Verhalten ab; Fehler werden dadurch als Sollverhalten festgeschrieben (Konstantinou u. a., ICST 2025).
* Zwischen ausgeführtem und tatsächlich geprüftem Code klafft eine Lücke, die als *oracle gap* formalisiert ist. Hohe Überdeckung sagt über Prüftiefe wenig aus.
* Selbstgeschriebene Verschärfungen schließen die Lücke nicht zuverlässig; nötig ist ein **exogenes Abnahmesignal**, das der Agent weder schreiben noch beobachten noch direkt optimieren kann (arXiv, Juli 2026).
* Eine Untersuchung aus dem Microsoft-Umfeld beschreibt zwei Ausprägungen: Ohne vorgegebenes Prüfsignal liefern Agenten ehrliche, aber unvollständige Artefakte, weil ihre selbstgewählte Validierung die interaktiven Verhaltensweisen nie erreicht. Mit vorgegebenem Prüfsignal erfüllen sie dieses auf dem kürzesten Weg — notfalls über einen Nebenpfad, während der eigentlich verlangte Liefergegenstand unfertig bleibt. Das Phänomen wird *building to the test* genannt.

Der letzte Punkt ist die wichtigste Einschränkung dieses ganzen Dokuments: **Ein Prüfsignal einzuführen genügt nicht. Es muss durch den Auslieferungspfad führen.**

### 3.4 Empirische Lage zur Codequalität

Die Beobachtung ist kein Einzelfall. Für 2026 berichten mehrere Erhebungen in dieselbe Richtung: rund 1,7-mal mehr Gesamtprobleme in KI-generiertem gegenüber menschlich geschriebenem Code, bei Logik- und Korrektheitsfehlern etwa 1,75-mal so viele. In einer Befragung von 300 Fachkräften aus Test und Qualitätssicherung gaben 58,1 % einen gestiegenen Testaufwand an, 51,6 % mehr Fehler. Auch diese Zahlen stammen überwiegend von Anbietern mit Interesse an der Aussage; die Richtung ist konsistent, die Genauigkeit unbelegt.

---

## 4. Drei Gegenmittel

Alle drei zielen auf dieselbe Eigenschaft: ein Signal zu erzeugen, das die umsetzende Instanz nicht nach ihrer eigenen Lesart formen kann.

### 4.1 Invarianten statt Sollwerten

**Problem.** Ein Beispieltest braucht einen Erwartungswert. Kennt ihn niemand, erfindet ihn die Instanz — aus ihrer eigenen Umsetzung heraus.

**Mechanismus.** Eine Invariante beschreibt nicht, *was* herauskommt, sondern *wie sich das Ergebnis ändern muss*, wenn sich die Eingabe auf bestimmte Weise ändert. Sie ist ohne Kenntnis des richtigen Ergebnisses formulierbar und nicht nachträglich an eine Ausgabe anpassbar. Familien: Skalierung, Symmetrie und Vertauschung, Umkehrung und Rückeinsetzung, Dimensions- und Einheitenkonsistenz, Monotonie und Grenzverhalten, Erhaltungsgrößen.

**Stand der Technik.** Der Fachbegriff ist *metamorphes Testen*; metamorphe Relationen sind notwendige Eigenschaften der beabsichtigten Funktionalität, die über mehrere Programmläufe geprüft werden. Das Verfahren gilt seit langem als Standardantwort auf das Orakelproblem für Systeme, deren richtige Ausgabe schwer bestimmbar ist — namentlich wissenschaftliche Rechenanwendungen, Simulatoren, Compiler, Bild- und Signalverarbeitung, maschinelles Lernen. Verwandt und praktisch oft identisch: eigenschaftsbasiertes Testen, das in Praxisvergleichen ausdrücklich für alles mit klarer Invariante empfohlen wird — Parser, Serialisierer, Mathematik, Zustandsmaschinen.

**Grenzen.** Invarianten sind fachliche Aussagen und müssen von jemandem stammen, der das Fach beherrscht. Ein Modell kann sie gut vorschlagen; bestätigen muss sie ein Mensch. Eine unbestätigte Invariante ist gefährlicher als keine, weil sie wie ein Maß aussieht. Und: Invarianten ersetzen keine Sollwerte, wo Sollwerte bekannt sind — sie ergänzen sie dort, wo keine bekannt sind.

**Anwendungsbereich.** Überall, wo gerechnet, umgeformt, aufgelöst, sortiert, transformiert oder ausgewertet wird. Nicht anwendbar auf reine Darstellungs- oder Bedienfragen.

### 4.2 Verfälschungsprüfung (Mutationstesten)

**Problem.** Testüberdeckung misst, welcher Code ausgeführt wurde, nicht, welches Verhalten geprüft wurde. Eine Suite kann vollständig durchlaufen und nichts absichern.

**Mechanismus.** In den Code werden einzelne, plausible Fehler eingesetzt — ein Vergleichsoperator umgedreht, ein Vorzeichen getauscht, ein Faktor entfernt, eine Bedingung invertiert. Anschließend laufen die Tests. Schlägt keiner an, hat die Verfälschung *überlebt*, und das ist der Nachweis einer Testlücke. Damit beantwortet das Verfahren als einziges die Frage, die zählt: *Würde diese Suite einen echten Fehler bemerken?*

**Stand der Technik.** Für agentengeschriebene Tests wird ein Mutationsgatter in der Integrationsstrecke empfohlen; ein niedriger Wert gilt als starkes Signal dafür, dass eine Suite Überdeckungszahlen polstert. Werkzeuge existieren sprachabhängig (Stryker für JavaScript und TypeScript, PIT für die JVM, weitere für Python und Solidity), 2026 sind zusätzlich agentenoptimierte Werkzeuge und Skills erschienen. Industrielle Evidenz: Meta setzte Sprachmodelle mit Mutationsrückmeldung über 10.795 Android-Kotlin-Klassen ein, erzeugte 9.095 gezielte Mutanten und 571 Tests, von denen Entwickler 73 % annahmen. Eine Benchmark-Untersuchung (SWE-Mutation) fand, dass von Agenten erzeugte semantische Mutanten für Testsuiten deutlich schwerer zu entdecken sind als konventionelle — das Verfahren wird also nicht leichter, sondern wichtiger.

**Grenzen.** Vollständige Läufe sind rechenintensiv; der Umfang muss begrenzt werden, sinnvoll auf geänderte Dateien und den fachlichen Kern. Wo kein Werkzeug für den Stack existiert, funktioniert das Verfahren von Hand: Dateien bestimmen, je Kernfunktion eine Verfälschung setzen, Tests laufen lassen, zurücknehmen. Und es misst die Empfindlichkeit der Tests, nicht die Richtigkeit der Anforderung — eine Suite kann eine falsche Anforderung sehr empfindlich absichern.

### 4.3 Bedienung der laufenden Anwendung durch die prüfende Instanz

**Problem.** Alles, was sich erst im Betrieb zeigt — leere Zustände, Ladezustände, Fehlermeldungen, Grenzwerte, ungültige Eingaben — wird von Prüfmitteln, die nur den Quellstand betrachten, prinzipiell nicht erfasst.

**Mechanismus.** Die prüfende Instanz startet das gebaute Artefakt und bedient es selbst. Entscheidend ist nicht die Bedienung, sondern was dabei zurückbleibt: Accessibility-Snapshot, Screenshot, Browserkonsole, Netzwerkmitschnitt, Ablaufaufzeichnung. Diese Artefakte sind unabhängig von dem, was die Instanz über ihren Lauf **behauptet**, und lassen sich getrennt auswerten. Der Agent hört damit auf, eine Blackbox zu sein, die Erfolg meldet, und beginnt, Belege zu erzeugen.

**Stand der Technik.** Der praktische Engpass war lange der Kontextverbrauch: Bei protokollgestützter Browsersteuerung wandert nach jeder Interaktion ein umfangreicher Bedienbaum in den Modellkontext, was lange Explorationsläufe unwirtschaftlich macht. Seit 2026 gibt es dafür eine Antwort — kommandozeilenbasierte Werkzeuge, die ihre Ausgabe auf die Festplatte schreiben statt in den Kontext. Der berichtete Unterschied für eine typische Aufgabe liegt bei etwa 114.000 gegenüber etwa 27.000 Token. Die Empfehlung des Herstellers lautet entsprechend: Kommandozeile, wenn der Agent Dateisystemzugriff hat; Protokollanbindung nur, wenn nicht. Ergänzend erlauben solche Werkzeuge das Abfangen und Manipulieren von Hintergrundaufrufen, wodurch sich Fehler-, Verzögerungs- und Ausfallzustände gezielt herbeiführen lassen, statt auf ihr zufälliges Auftreten zu warten.

**Grenzen.** Das Verfahren prüft, was jemand zu prüfen aufgeschrieben hat. Es findet keinen Mangel, für den kein Kriterium existiert. Deshalb hängt sein Nutzen daran, dass Zustände in der Spezifikation als Kriterien stehen — sonst verschiebt es die Lücke nur.

---

## 5. Allgemeine Regeln

Aus dem Vorstehenden lassen sich Regeln ableiten, die unabhängig von Werkzeug, Sprache und Modell gelten.

1. **Das Maß schreibt nicht, wer daran gemessen wird.** Akzeptanzkriterien, Invarianten und Nachweisverfahren entstehen vor der Umsetzung und außerhalb ihrer Sitzung. Die umsetzende Instanz darf sie lesen, nicht ändern.
2. **Grün heißt widerspruchsfrei, nicht richtig.** Ein bestandener Testlauf belegt Übereinstimmung zwischen Code und Test. Stammen beide aus derselben Lesart, belegt er nichts über die Anforderung.
3. **Was nicht gemessen wurde, ist nicht erfüllt.** Und ein Prüfmittel, das eine absichtlich verfälschte Umsetzung nicht bemerkt, zählt nicht als Messung.
4. **Der Nachweis muss durch den Auslieferungspfad führen.** Erfüllung auf einem Nebenpfad — Demoansicht, Testmodus, fest verdrahteter Zustand — ist Nichterfüllung. Eine Umsetzung, die auf ein Prüfsignal hin arbeitet, nimmt den kürzesten Weg dorthin.
5. **Die Messeinrichtung entsteht vor der Fachlichkeit** und ist fertig, wenn sie am leeren Projekt **erwartungsgemäß fehlschlägt**. Ein Prüfstand, der auf nichts grün meldet, misst nichts.
6. **Belege sind Dateien, keine Sätze.** Behauptungen ohne zurückgebliebenes Artefakt gelten als nicht nachgewiesen. Das gilt für Kommandoausgaben ebenso wie für Bedienläufe.
7. **Ein ehrliches Teilergebnis ist wertvoller als ein unbelegtes Vollergebnis.** Ein Bewertungsschema braucht eine mittlere Stufe für „umgesetzt, aber nicht nachgewiesen", sonst wird sie zur unteren oder zur oberen gerundet — meist zur oberen.
8. **Zustände sind Anforderungen.** Leer, lädt, Fehler, Grenzwert, ungültige Eingabe gehören in die Spezifikation. Was dort fehlt, wird weder gebaut noch geprüft und endet als Geschmacksurteil in der Abnahme.
9. **Kontext ist eine knappe Ressource der Verifikation.** Prüfmittel, die ihre Ausgabe in den Modellkontext spielen, begrenzen die Prüftiefe. Solche, die auf die Festplatte schreiben, nicht.
10. **Rechnerische und inferentielle Prüfung ersetzen einander nicht.** Werkzeugläufe fangen Strukturelles zuverlässig; ob ein Produkt das Richtige tut, bleibt eine Urteilsfrage, die Rollentrennung braucht.

---

## 6. Was offen bleibt

Ehrlichkeitshalber gehört dazu, was diese Mittel **nicht** leisten.

Sie prüfen Erfüllung, nicht Angemessenheit. Ein Mangel, den niemand spezifiziert hat — „das ist an dieser Stelle verwirrend", „hier fehlt eine Rückmeldung", „diese Reihenfolge ist unlogisch" — wird von keinem Prüfmittel gefunden. Er verlangt Urteil, und Urteil lässt sich nur teilweise in Kriterien überführen: über Zustandsmatrizen, Heuristik-Checklisten, Barrierefreiheitsprüfungen. Ein Rest bleibt beim Menschen, und die Verhaltensregelung ist nach übereinstimmender Einschätzung der Praxisliteratur der ungelöste Teil des Feldes.

Zweitens verschieben diese Mittel Aufwand nach vorn. Sie machen den Anfang teurer und das Ende billiger. Für kurzlebige Prototypen lohnt sich das nicht; der Nutzen wächst mit Lebensdauer, Kritikalität und Zahl der beteiligten Instanzen.

Drittens ist die Zahlenlage schwach. Fast alle quantitativen Angaben in Abschnitt 3 stammen von Anbietern oder aus nicht replizierten Einzelstudien. Belastbar ist die Richtung, nicht die Größe.

---

## 7. Quellen

* Böckeler, B.: *Harness engineering for coding agent users* — martinfowler.com/articles/harness-engineering.html
* Böckeler, B.: *Maintainability sensors for coding agents* — martinfowler.com/articles/sensors-for-coding-agents.html
* *Self-Authored Verification Is Unreliable in Heuristic Self-Improving Agents*, arXiv 2607.24300
* *Building to the Test: Coding Agents Deliver What You Check, Not What You Requested*, arXiv 2606.28430
* *All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code*, arXiv 2606.18168
* Barr, Harman, McMinn, Shahbaz, Yoo: *The Oracle Problem in Software Testing: A Survey*, IEEE TSE 41(5), 2015
* Chen u. a.: *Metamorphic Testing: A Review of Challenges and Opportunities*, ACM Computing Surveys 51(1), 2018
* *Mutation Testing for Agent-Written Code* — awesome-testing.com, August 2026
* *AI Test Generation Tools Compared 2026* — developersdigest.tech, August 2026
* Playwright, Abschnitt *Coding agents* — playwright.dev/docs/getting-started-cli
* *Playwright CLI, Skills and Isolated Agentic Testing* — awesome-testing.com, März 2026
* *State of AI-Generated Code 2026: The QA and Testing Gap* — deviqa.com, Juli 2026

---

## 8. Anlassfall

*Zur Nachvollziehbarkeit, nicht zur Verallgemeinerung.*

Ein kleines Softwareprojekt — eine Web-Anwendung, deren fachliche Schwierigkeit im Auflösen physikalischer Formeln lag — wurde mit einem ausgearbeiteten Prompt-Set und einer Arbeitsverfassung umgesetzt. Umgebung: Visual Studio Code mit der Erweiterung Kilo Code. Spezifikation und Plan entstanden mit einem Modell, Aufgaben und Umsetzung mit einem zweiten. Die umsetzende Instanz nutzte im Ablauf ein Browser-Testframework.

Ergebnis: Die erste fertige Fassung enthielt schwere Bedienfehler und war nicht fehlerfrei lauffähig; bis zum Zustand eines minimal brauchbaren Produkts waren etliche Korrekturrunden nötig. Die Qualität blieb deutlich hinter der Erwartung zurück.

Dasselbe Projekt wurde anschließend per Repository an Claude Code übergeben. Dort entstand ohne Zutun ein Container für die Simulation der Anwendung, in dem sofort Bedienprüfungen liefen. Sie förderten zahlreiche Ungenauigkeiten und Fehler zutage, die in der ersten Umgebung unentdeckt geblieben waren. Am Ende stand ein auslieferungsreifer Zustand.

Zur Einordnung: Die Erweiterung Kilo Code unterstützt das Model Context Protocol nativ und kann externe Werkzeuge einbinden. Der Unterschied lag also nicht an einer fehlenden Werkzeugklasse, sondern daran, dass die Rückmeldeschicht nicht eingerichtet war — und daran, dass eine Editor-Erweiterung eine geöffnete Sitzung mit grafischer Oberfläche voraussetzt und damit eine Obergrenze für unbeaufsichtigten Betrieb setzt, die keine Erweiterung vollständig überwinden kann.

Der Fall ist als Beleg schwach: eine Umsetzung, ein Projekt, keine Kontrollbedingung. Er ist als Anlass tauglich, weil das gefundene Muster sich anschließend in der Literatur wiedergefunden hat — nicht umgekehrt.
