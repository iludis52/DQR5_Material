# Zeitreihenanalyse

Der Datensatz enthält Datumsspalten, die auf zeitliche Muster hindeuten.

## Analyseaufgaben

- **Zeitlichen Index erstellen**: Konvertiere die Datumsspalte mit 
  `pd.to_datetime()` und setze sie ggf. als Index.
- **Trends**: Liniendiagramme über die Zeit. Gibt es einen Aufwärts-/
  Abwärtstrend? Nutze ggf. Rolling Averages zur Glättung.
- **Saisonale Muster**: Aggregiere nach Monat, Wochentag oder Quartal. 
  Gibt es wiederkehrende Muster?
- **Vergleich über Zeiträume**: Gibt es signifikante Unterschiede 
  zwischen Perioden (z.B. Q1 vs. Q2)?

## Qualitätsanspruch

Zeitliche Analysen brauchen Kontext: "Der Umsatz stieg von Januar 
(Ø 1.200€) auf März (Ø 1.850€) um 54%" ist besser als "Der Umsatz 
zeigt einen Aufwärtstrend".
