# Feature Interaction — Arbeitsblatt (Berufsspezialist, DQR 5)

Zwei Merkmale *interagieren*, wenn die Wirkung des einen von der Ausprägung
des anderen abhängt. Die Vorhersage lässt sich dann **nicht** mehr als Summe
der Einzelwirkungen schreiben. Dieses Blatt entwickelt den Begriff in vier
Schritten: Zerlegung → Stärke → Vorzeichenstruktur → direkte vs. indirekte
Wirkung.

---

## Teil 1 — Eine Vorhersage zerlegen

**Beispiel A: Immobilienpreis.** Ein Modell sagt den Preis aus zwei Merkmalen
vorher: **Lage** (gut/schlecht) und **Größe** (groß/klein). Preise in Tsd. €.

**A.1 — Der additive Fall**

| Lage | Größe | Vorhersage |
|------|-------|:---:|
| gut | groß | 300 |
| gut | klein | 200 |
| schlecht | groß | 250 |
| schlecht | klein | 150 |

Zerlege die Tabelle in: Basiswert + Effekt(Größe) + Effekt(Lage).

- Basiswert (schlecht + klein): ________
- Effekt(groß): ________   Effekt(gut): ________
- Prüfe: Ist der Aufpreis für „groß" in guter und schlechter Lage **gleich**?
  → ________

Wenn die Größenwirkung lageunabhängig ist, genügt die Summe der Einzeleffekte.
Es gibt **keinen** Interaktionsterm.

**A.2 — Der interaktive Fall**

Dieselben Merkmale, andere Vorhersagen — nur eine Zelle ändert sich:

| Lage | Größe | Vorhersage |
|------|-------|:---:|
| gut | groß | **400** |
| gut | klein | 200 |
| schlecht | groß | 250 |
| schlecht | klein | 150 |

- Aufpreis für „groß" bei **schlechter** Lage: 250 − 150 = ________
- Aufpreis für „groß" bei **guter** Lage: 400 − 200 = ________
- Die Differenz dieser beiden Aufpreise ist der **Interaktionsterm**: ________

**A.3 — Die Zerlegung als Modell**

> **Vorhersage = Basis + Effekt(Größe) + Effekt(Lage) + Interaktion(Größe, Lage)**
>
> Der Interaktionsterm ist der Anteil der Vorhersage, der **übrig bleibt**,
> nachdem Basis und Einzeleffekte abgezogen sind. Er ist genau dann null,
> wenn sich das Modell rein additiv verhält.

Setze für „gut + groß" alle vier Terme ein und rechne 400 nach.

---

## Teil 2 — Wie stark ist die Interaktion?

Nicht ob, sondern **wie viel**: Welcher Anteil der Schwankung in den
Vorhersagen geht auf den Interaktionsterm zurück — und welcher auf die
Einzeleffekte?

**A.4** In Beispiel A.2 spannen die Einzeleffekte die Werte Größe (100) und
Lage (50) auf; der Interaktionsterm beträgt (aus A.2) ________. Ordne grob
ein: Trägt die Interaktion hier viel oder wenig zur Preisspanne bei?

> **Begriff.** Die *Interaktionsstärke* misst den Anteil der Vorhersage-
> Variation, der auf Wechselwirkungen entfällt (0 = rein additiv). Die
> gängige Kennzahl dafür ist **Friedmans H-Statistik**; ihre Formel behandeln
> wir hier nicht — für uns zählt die Idee: *Anteil der Wirkung, der nur
> gemeinsam entsteht.*

**Sichtbar machen: 2D-Partial-Dependence-Plot.** Man trägt die beiden Merkmale
auf die Achsen auf und färbt die modellierte Vorhersage. **Ohne** Interaktion
sind die Profile über das eine Merkmal für jeden Wert des anderen nur parallel
verschoben; **mit** Interaktion verdrehen oder überkreuzen sie sich.

**A.5** Skizziere für A.1 und A.2 je die Größenwirkung als zwei Linien (gute
vs. schlechte Lage). In welcher Skizze verlaufen die Linien parallel, in
welcher nicht — und warum?

---

## Teil 3 — Struktur der Interaktion: Vorzeichen und Kontext

**Beispiel B: Pflanzenwachstum** aus **Dünger** und **Wasser** (Skala 0–10).

| | wenig Wasser | mittel | viel Wasser |
|------------------|:---:|:---:|:---:|
| **kein Dünger** | 2 | 3 | 4 |
| **mittel Dünger**| 2 | 5 | 7 |
| **viel Dünger** | 1 | 6 | 10 |

**B.1** Verfolge die Düngerwirkung (kein → viel) je Wasserspalte:

- viel Wasser: 4 → 10, also ________
- mittel: 3 → 6, also ________
- wenig Wasser: 2 → 1, also ________

**B.2** Beschreibe, was mit dem **Vorzeichen** der Düngerwirkung geschieht,
wenn Wasser knapp wird.

> Eine Interaktion ist kein fester „Bonus". Sie kann sich mit dem Kontext
> verstärken, abschwächen oder das **Vorzeichen wechseln** — hier kippt Dünger
> von nützlich (viel Wasser) zu schädlich (Salzstress bei Wassermangel).
> Interaktionen liegen also auf einem Kontinuum, nicht in festen Kategorien.

---

## Teil 4 — Direkte vs. indirekte Wirkung

Zwei Größen können auch zusammenhängen, **ohne** direkt zu interagieren — wenn
eine dritte Größe dazwischenliegt.

- **Direkt (Interaktionsmodifikation):** Die Wirkung von A auf die Zielgröße
  hängt unmittelbar von B ab. → *echte* Zwei-Merkmal-Interaktion
  (Beispiele A.2 und B).
- **Indirekt (Interaktionskette):** A wirkt auf die Zielgröße nur **über** eine
  dritte Größe M: A → M → Ziel. A und M erscheinen dann verknüpft, obwohl der
  Effekt vermittelt ist.

**Intuition (Ökologie).** Ein Vogel frisst Raupen, dadurch wächst die Pflanze
besser: Vogel → (weniger) Raupen → Pflanze. Der Vogel wirkt auf die Pflanze
**indirekt**, über die Raupen.

**Transfer (Kältetechnik).** Die Außentemperatur treibt sowohl die Kühllast als
auch die Verdichterlaufzeit. Eine im Modell auftauchende „Interaktion" zwischen
Kühllast und Laufzeit kann in Wahrheit über die gemeinsame Ursache Temperatur
**vermittelt** sein — keine echte Wechselwirkung der beiden Merkmale.

**B.3** Ordne zu — direkt (Modifikation) oder indirekt (vermittelt/Kette)?

1. Der Nutzen von Streusalz für die Griffigkeit hängt von der Temperatur ab
   (unter/über 0 °C). → ________
2. Mehr Werbebudget → mehr Websitebesuche → mehr Umsatz. → ________
3. Ein Betriebsdruck ist bei Kältemittel R290 optimal, bei R744 schädlich. → ________

> **Warum das für Modelle zählt.** Sind Merkmale **korreliert**, zeigen Modelle
> leicht *scheinbare* Interaktionen, die real über eine dritte Größe vermittelt
> sind. Genau darauf ist beim Random Forest zu achten — der Übergang zur
> nächsten Einheit.

---

## Teil 5 — Transfer in die eigene Domäne

Finde je **ein** Beispiel aus deinem Fachgebiet für:

- eine **echte** Interaktion (Wirkung von A hängt direkt von B ab): ________
- einen **vermittelten** Zusammenhang (A → M → Ziel): ________

Prüfe bei deiner echten Interaktion: Verändert B wirklich die *Wirkung* von A —
oder addiert B nur seinen eigenen Beitrag (dann bloßer Haupteffekt)?

---
---

## Lehrerteil — Lösungen und Hinweise

**Hinweis zu den Zahlen.** Beispiel A folgt Molnar (*Interpretable ML*,
Kap. Feature Interaction); Beispiel B nutzt didaktische Illustrationswerte.
Belegt ist die *Richtung*: Nährstoff-Wasser-Ko-Limitation (Minimumgesetz) für
die Synergie, osmotischer Salzstress für die Umkehr — nicht die konkreten
Zahlen.

**A.1** Basis 150; Effekt(groß) +100; Effekt(gut) +50. Aufpreis „groß" ist in
beiden Lagen +100 → **kein** Interaktionsterm; Modell rein additiv.

**A.2** Aufpreis „groß": schlechte Lage +100, gute Lage **+200**.
Interaktionsterm = 200 − 100 = **+100** (wirkt nur bei „gut & groß").

**A.3** 150 (Basis) + 100 (groß) + 50 (gut) + 100 (Interaktion) = **400**. ✓

**A.4** Interaktionsterm = 100 — in derselben Größenordnung wie der
Größeneffekt (100) und größer als der Lageeffekt (50): die Interaktion trägt
hier **erheblich** zur Preisspanne bei.

**A.5** A.1: zwei **parallele** Linien (konstanter Größenaufpreis, gleiche
Steigung → keine Interaktion). A.2: die Linie für „gute Lage" ist steiler →
Linien **nicht parallel** → Interaktion. Genau dieses Auseinanderlaufen macht
der 2D-PDP sichtbar.

**B.1** viel Wasser **+6**, mittel **+3**, wenig Wasser **−1**.

**B.2** Die Düngerwirkung wechselt das **Vorzeichen** — von stark positiv zu
negativ. „Mehr Dünger ist besser" gilt nur bei ausreichend Wasser und kippt bei
Wassermangel.

**B.3** (1) direkt — Temperatur modifiziert die Salzwirkung. (2) indirekt —
Kette Budget → Besuche → Umsatz. (3) direkt — Druckwirkung hängt vom Kältemittel
ab. *Diskussion:* Bei (2) lohnt der Hinweis, dass Budget und Umsatz im Modell
verknüpft *aussehen*, der Effekt aber über die Besuche läuft.

**Brücke zum Random Forest.** Ein lineares Modell erfasst Interaktionen nur mit
explizitem Produktterm; der Random Forest bildet sie über verschachtelte Splits
von selbst ab. Kehrseite: Bei korrelierten Merkmalen erzeugt er leicht
*scheinbare* Interaktionen (vgl. Teil 4). In der nächsten Einheit messen wir
Interaktionsstärke am RF und lesen 2D-PDPs — ohne die H-Statistik zu rechnen.
