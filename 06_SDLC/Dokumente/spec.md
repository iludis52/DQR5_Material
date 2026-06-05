# Spezifikation: Predictive-Maintenance-Prototyp für eine Produktionsmaschine

> **Status:** Prototyp / Proof of Concept · **Source of Truth** für dieses Projekt.
> Änderungen am Verhalten werden zuerst hier eingetragen, dann im Code umgesetzt.

## 0. Zweck & Reifegrad

PROTOTYP / Proof of Concept. Ziel ist **nicht** der produktive Dauerbetrieb, sondern der
Nachweis, dass sich aus Sensordaten ein brauchbares Frühwarnsignal für den Wartungsbedarf
ableiten lässt. Die skalierte, produktive Umsetzung erfolgt anschließend mit externen
Fachleuten (siehe Abschnitt 8). Diese Spezifikation ist zugleich Bauplan und Übergabedokument.

## 1. Daten-Contract (Sensorik)

- **Quelle:** Sensor-Gateway sendet Messwerte als JSON per HTTP `POST /ingest`.
- **Abtastrate (Prototyp):** 1 Messung pro Sekunde je Sensor.
- **Felder je Nachricht:**
  - `machineId` (string)
  - `timestamp` (ISO 8601, UTC)
  - `vibration` (number, mm/s)
  - `temperature` (number, °C)
  - `current` (number, A)
- **Plausibilitätsgrenzen** — Werte außerhalb gelten als **Sensorfehler**, nicht als Maschinenfehler:
  - `temperature`: -20 bis 150
  - `vibration`: 0 bis 50
  - `current`: 0 bis 100

## 2. ML-Aufgabe (bewusst einfach gehalten)

- **Aufgabentyp:** Anomalie-Erkennung (unüberwacht). **Keine** Ausfallvorhersage in
  Zeiteinheiten — im Prototyp liegen i. d. R. noch keine echten Ausfälle als Trainingslabel
  vor („Cold-Start-Problem“).
- **Vorgehen:** Das Modell lernt das Normalverhalten aus einer störungsfreien Referenzphase
  und meldet Abweichungen als Anomalie-Score.
- **Ausgabe je Maschine, alle 5 Sekunden aktualisiert:**
  - `healthScore` (number, 0..1)
  - `status` (`"ok"` | `"warnung"` | `"kritisch"`)
    - Schwellen (Prototyp, später kalibrierbar): `< 0.4` = ok, `0.4–0.7` = warnung, `> 0.7` = kritisch
  - `dataStale` (boolean) — `true`, wenn seit mehr als 30 s keine gültigen Werte kamen

## 3. Web-Oberfläche (für den Industriemeister)

- Eine Seite, Auto-Refresh alle 5 Sekunden.
- Zeigt je Maschine: Ampel (grün/gelb/rot), `healthScore`, Zeitpunkt der letzten Messung
  sowie den Verlauf der letzten 30 Minuten als einfaches Liniendiagramm.
- Bei Status `kritisch` oder `dataStale`: deutlich sichtbarer Warnhinweis.
- Verständlich ohne Schulung — der Meister muss den Zustand sofort deuten können.

## 4. Verhalten in Sonderfällen

- **Datenlücke / Sensorausfall:** Status **nicht** auf `ok` setzen; `dataStale = true` und
  letzten bekannten Wert mit Zeitstempel anzeigen.
- **Sensorfehler** (Wert außerhalb der Plausibilitätsgrenzen): Messwert verwerfen, im UI als
  „Sensor prüfen“ markieren, nicht in den `healthScore` einrechnen.
- **Kaltstart** (Modell noch nicht angelernt): Status `"lernt …"` anzeigen, noch keine
  Warnungen erzeugen.

## 5. Technische Constraints (prototyp-tauglich)

- **Sprache:** Python.
- **ML:** scikit-learn, z. B. `IsolationForest` — **kein** Deep Learning im Prototyp.
- **Backend:** FastAPI. **Datenhaltung:** SQLite (eine Datei, kein DB-Server).
- **Frontend:** eine einfache HTML-Seite, die das Backend per `fetch` abfragt.
- Alles lokal auf einem Rechner lauffähig, keine Cloud-Abhängigkeit.

## 6. Akzeptanzkriterien (Prototyp gilt als erfolgreich, wenn …)

1. Bei eingespielten Normaldaten bleibt der Status stabil auf `ok`.
2. Eine künstlich erzeugte Auffälligkeit (z. B. steigende Vibration) hebt den Status
   innerhalb von 15 s auf `warnung`/`kritisch`.
3. Bei abgeschaltetem Sensor zeigt das UI binnen 30 s `dataStale` an.
4. Der Industriemeister deutet den angezeigten Zustand ohne Erklärung richtig.

## 7. Annahmen (explizit, damit sie überprüfbar bleiben)

- Genau eine Maschine; Mehrmaschinen-Betrieb erst in der Produktivversion.
- Läuft im geschützten internen Netz → keine Authentifizierung/Verschlüsselung im PoC.
- Eine ausreichend lange störungsfreie Referenzphase zum Anlernen existiert.
- Datenmengen sind klein genug für SQLite und einen einzelnen Prozess.

## 8. Bewusst NICHT im Prototyp — Übergabe an Fachleute

- Skalierung auf viele Maschinen, Hochverfügbarkeit, Zeitreihen-Datenbank.
- Echte Restlebensdauer-Vorhersage auf Basis gelabelter Ausfälle.
- Authentifizierung, Rollen, Audit, Alarmierung per E-Mail/SMS.
- Modell-Monitoring, Drift-Erkennung, regelmäßiges Re-Training.
- OT-/Sicherheitsanforderungen (Trennung vom Produktionsnetz, einschlägige Normen).
