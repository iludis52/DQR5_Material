# Analyse fehlender Werte

Der Datensatz enthält fehlende Werte: {fehlende_werte}

## Analyseaufgaben

- **Muster erkennen**: Fehlen Werte zufällig (MCAR), systematisch 
  abhängig von beobachteten Variablen (MAR), oder abhängig von den 
  fehlenden Werten selbst (MNAR)?
- **Visualisierung**: Erstelle eine Heatmap oder ein Balkendiagramm 
  der fehlenden Werte pro Spalte.
- **Zusammenhänge**: Korrelieren fehlende Werte in einer Spalte mit 
  bestimmten Kategorien oder Zeiträumen? (z.B. fehlen Umsatzdaten 
  häufiger in einer bestimmten Region?)
- **Empfehlung**: Basierend auf dem Muster — was ist der empfohlene 
  Umgang? (Löschen, Imputation mit Median/Modus, Interpolation, etc.)

## Qualitätsanspruch

Nenne immer die konkreten Anzahlen und Anteile: "In Spalte 'umsatz' 
fehlen 2 von 30 Werten (6.7%), beide in der Kategorie 'Widget Pro'."
