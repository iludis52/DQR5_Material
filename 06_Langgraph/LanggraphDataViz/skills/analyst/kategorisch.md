# Kategorische Analyse

Der Datensatz enthält kategorische Spalten: {kategorische_spalten}

## Analyseaufgaben

- **Häufigkeitsverteilung**: Balkendiagramme für die Kategorien. 
  Wie gleichmäßig sind die Gruppen verteilt?
- **Gruppierte Analyse**: Numerische Kennzahlen aufgeschlüsselt nach 
  Kategorien (z.B. Umsatz pro Region, Zufriedenheit pro Produkt). 
  Nutze `groupby()` und visualisiere die Unterschiede.
- **Kreuztabellen**: Gibt es interessante Kombinationen zwischen 
  kategorischen Spalten? (z.B. `pd.crosstab()`)

## Qualitätsanspruch

Identifiziere die Top- und Bottom-Performer in jeder Kategorie 
mit konkreten Zahlen. "Region Nord hat 23% höheren Durchschnittsumsatz 
als Region Ost" ist besser als "Es gibt Unterschiede zwischen Regionen".
