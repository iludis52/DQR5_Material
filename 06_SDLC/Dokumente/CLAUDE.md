# Projektregeln — Predictive-Maintenance-Prototyp

> Diese Datei ist das „Grundgesetz“ des Projekts (Constitution).
> **Claude Code** liest sie zu Beginn jeder Sitzung automatisch.
> Für die **Continue-Extension**: denselben Inhalt als `CONVENTIONS.md` ablegen und
> im Chat per `@CONVENTIONS.md` anhängen (oder als Continue-Regel hinterlegen).

## Worum es geht

Prototyp / Proof of Concept für Predictive Maintenance:
Sensordaten → Anomalie-Erkennung → Ampel-Status → einfache Web-Oberfläche für den Industriemeister.

## Wichtigste Regel (Spec-Driven Development)

- **`spec.md` ist die Source of Truth.** Verhalten, Constraints und Akzeptanzkriterien stehen dort.
- **Neue Anforderungen oder Fehler kommen ZUERST in `spec.md`**, danach in den Code — niemals umgekehrt. Keine stillen Änderungen am Verhalten.

## Tech-Stack & Constraints (aus spec.md, Abschnitt 5)

- Sprache: **Python**.
- ML: **scikit-learn** (`IsolationForest`) — **kein** Deep Learning.
- Backend: **FastAPI**. Datenhaltung: **SQLite** (eine Datei, kein DB-Server).
- Frontend: eine einfache HTML-Seite, die das Backend per `fetch` abfragt.
- Lokal lauffähig, keine Cloud-Abhängigkeit.
- **Keine zusätzlichen Bibliotheken** einführen, die nicht in `spec.md` genannt sind, ohne vorher zu fragen.

## Arbeitsweise, die ich erwarte

- Bei größeren Schritten zuerst kurz den **Plan** erläutern, dann umsetzen.
- **Tests zuerst:** zu den Akzeptanzkriterien (`spec.md`, Abschnitt 6) `pytest`-Tests schreiben, die zunächst fehlschlagen — danach den Code, bis sie grün sind.
- In **kleinen, einzeln testbaren Schritten** entlang `tasks.md` arbeiten.
- Tests selbst ausführen und das Ergebnis zeigen. Änderungen als nachvollziehbare Diffs halten.

## Code-Stil

- Einfach und gut lesbar; Kommentare auf Deutsch sind willkommen.
- Type Hints verwenden; kleine, fokussierte Funktionen und Module.

## Nicht im Prototyp (siehe spec.md, Abschnitt 8)

- Keine Authentifizierung, kein Mehrmaschinen-Betrieb, keine Restlebensdauer-Vorhersage, kein Modell-Monitoring.
- Das übernehmen später externe Fachleute. Im Zweifel: lieber einfach halten und in `spec.md` vermerken.

## Nützliche Befehle

```bash
# Umgebung aktivieren
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Server starten
uvicorn main:app --reload          # http://127.0.0.1:8000

# Tests ausführen
pytest

# Sensor-Simulator (Test ohne echte Hardware)
python simulate_sensor.py              # Normalbetrieb  -> Ampel bleibt grün
python simulate_sensor.py --anomalie   # Störung        -> Ampel wird gelb/rot
```
