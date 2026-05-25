# Clustering Skills — LLM-Anweisungen für Ordner-Clusterung

## ordnernamen_regeln

- Nur Kleinbuchstaben a-z, Ziffern 0-9 und Unterstriche
- Maximal 40 Zeichen
- Keine Umlaute, keine Sonderzeichen, kein Leerzeichen

## ausgabeformat

Antworte ausschliesslich in diesem JSON-Format:
[
  {
    "ordner": "ordnername",
    "beschreibung": "2-5 Woerter Kurzbeschreibung",
    "dateien": ["dateiname1", "dateiname2"]
  }
]

Keine Erklaerungen, kein Markdown, nur JSON.

## erstvorschlag

Du erhaeltst eine Liste von Dateien mit optionalen Stichwoertern.
Gruppiere sie in {min_cluster} bis {max_cluster} thematische Cluster.

{ordnernamen_regeln}

{ausgabeformat}

{anweisung_block}

Dateien:
{dateiliste}

## korrektur

Aktuelle Clusterung:
{aktueller_stand}

Vollstaendige Dateiliste mit Stichwoertern:
{dateiliste}

Feedback: {feedback}

Ueberarbeite die Clusterung gemaess dem Feedback.
{ordnernamen_regeln}
Antworte im selben JSON-Format. Keine Erklaerungen, nur JSON.

## persistente_anweisungen

