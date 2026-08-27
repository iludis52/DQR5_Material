#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pfad-Rechner -- Lehrwerkzeug für absolute und relative Pfade
=============================================================

Startet einen lokalen Webserver und öffnet die Oberfläche im Browser.
Der Ordner-Dialog wird plattformnativ geöffnet:

    macOS    osascript / Finder-Dialog   (umgeht Tk vollständig)
    Windows  PowerShell FolderBrowserDialog
    Linux    zenity, ersatzweise kdialog
    Notfall  tkinter (nur falls nichts davon vorhanden ist)

Start:  python3 pfadrechner.py
Ende:   Button "Beenden" in der Oberfläche oder Strg+C im Terminal

Nur Standardbibliothek -- keine Installation nötig.
"""

import http.server
import json
import os
import pathlib
import socket
import subprocess
import sys
import threading
import urllib.parse
import webbrowser

# ---------------------------------------------------------------------------
# Ordner-Dialoge -- plattformnativ
# ---------------------------------------------------------------------------

# Nur ein Dialog gleichzeitig, sonst kämpfen zwei Fenster um den Fokus.
DIALOG_SPERRE = threading.Lock()


def _ohne_schlusstrenner(pfad: str) -> str:
    """Entfernt einen abschließenden Trenner, lässt die Wurzel aber intakt."""
    pfad = pfad.strip()
    if len(pfad) > 1 and pfad.endswith(("/", "\\")) and not pfad.endswith(":\\"):
        return pfad[:-1]
    return pfad


def _dialog_macos(titel: str) -> str:
    """Finder-Dialog über AppleScript. Kein Tk, keine Abhängigkeit."""
    skript = 'POSIX path of (choose folder with prompt "%s")' % titel.replace('"', "'")
    ergebnis = subprocess.run(
        ["osascript", "-e", skript], capture_output=True, text=True
    )
    if ergebnis.returncode != 0:  # Abbruch durch die Nutzerin
        return ""
    return _ohne_schlusstrenner(ergebnis.stdout)


def _dialog_windows(titel: str) -> str:
    """FolderBrowserDialog über PowerShell, im STA-Modus und im Vordergrund."""
    befehl = (
        "Add-Type -AssemblyName System.Windows.Forms;"
        "$vorne = New-Object System.Windows.Forms.Form;"
        "$vorne.TopMost = $true;"
        "$d = New-Object System.Windows.Forms.FolderBrowserDialog;"
        "$d.Description = '%s';"
        "$d.ShowNewFolderButton = $true;"
        "if ($d.ShowDialog($vorne) -eq [System.Windows.Forms.DialogResult]::OK)"
        "{ Write-Output $d.SelectedPath };"
        "$vorne.Dispose()"
    ) % titel.replace("'", " ")
    ergebnis = subprocess.run(
        ["powershell", "-NoProfile", "-STA", "-Command", befehl],
        capture_output=True,
        text=True,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    return _ohne_schlusstrenner(ergebnis.stdout)


def _dialog_linux(titel: str) -> str:
    """zenity, ersatzweise kdialog."""
    versuche = [
        ["zenity", "--file-selection", "--directory", "--title=" + titel],
        ["kdialog", "--getexistingdirectory", os.path.expanduser("~")],
    ]
    for befehl in versuche:
        try:
            ergebnis = subprocess.run(befehl, capture_output=True, text=True)
        except FileNotFoundError:
            continue
        if ergebnis.returncode != 0:
            return ""
        return _ohne_schlusstrenner(ergebnis.stdout)
    raise FileNotFoundError("zenity/kdialog")


def _dialog_tkinter(titel: str) -> str:
    """Notnagel: Tk in einem eigenen Prozess, damit nichts einfriert."""
    skript = (
        "import tkinter as tk\n"
        "from tkinter import filedialog\n"
        "wurzel = tk.Tk()\n"
        "wurzel.attributes('-topmost', True)\n"
        "wurzel.withdraw()\n"
        "print(filedialog.askdirectory(title=%r))\n" % titel
    )
    ergebnis = subprocess.run(
        [sys.executable, "-c", skript], capture_output=True, text=True
    )
    if ergebnis.returncode != 0:
        # Kein Tk vorhanden oder keine Anzeige -- weiterreichen, nicht verschlucken
        zeilen = ergebnis.stderr.strip().splitlines()
        raise RuntimeError(zeilen[-1] if zeilen else "Tk ist nicht nutzbar")
    return _ohne_schlusstrenner(ergebnis.stdout)


def ordner_waehlen(titel: str) -> dict:
    """Oeffnet den passenden Dialog. Gibt {'pfad': ...} oder {'fehler': ...} zurück."""
    if sys.platform == "darwin":
        reihenfolge = [_dialog_macos, _dialog_tkinter]
    elif os.name == "nt":
        reihenfolge = [_dialog_windows, _dialog_tkinter]
    else:
        reihenfolge = [_dialog_linux, _dialog_tkinter]

    letzter_fehler = None
    for dialog in reihenfolge:
        try:
            return {"pfad": dialog(titel)}
        except Exception as fehler:  # nächste Variante versuchen
            letzter_fehler = fehler
    return {
        "pfad": "",
        "fehler": "Auf diesem System lässt sich kein Ordner-Dialog öffnen (%s)."
        % letzter_fehler,
    }


# ---------------------------------------------------------------------------
# Pfad-Analyse
# ---------------------------------------------------------------------------

TRENNER = os.sep


def _teile_gleich(a: str, b: str) -> bool:
    """Windows unterscheidet keine Groß- und Kleinschreibung, POSIX schon."""
    return a.lower() == b.lower() if os.name == "nt" else a == b


def pfade_analysieren(ordner1: str, ordner2: str) -> dict:
    """Normalisiert beide Pfade, bestimmt gemeinsamen Teil und relativen Pfad."""
    if not ordner1 or not ordner2:
        return {"ok": False, "meldung": "Wähle beide Ordner aus."}

    pfad1 = pathlib.Path(ordner1).resolve()
    pfad2 = pathlib.Path(ordner2).resolve()
    abs1, abs2 = str(pfad1), str(pfad2)

    # Gemeinsamer Anfang, Bestandteil für Bestandteil
    teile1, teile2 = pfad1.parts, pfad2.parts
    anzahl = 0
    while anzahl < min(len(teile1), len(teile2)) and _teile_gleich(
        teile1[anzahl], teile2[anzahl]
    ):
        anzahl += 1

    gemeinsam = os.path.join(*teile1[:anzahl]) if anzahl else ""
    rest1 = abs1[len(gemeinsam):]
    rest2 = abs2[len(gemeinsam):]

    try:
        relativ = os.path.relpath(abs2, abs1)
    except ValueError:
        return {
            "ok": False,
            "abs1": abs1,
            "abs2": abs2,
            "gemeinsam": "",
            "rest1": abs1,
            "rest2": abs2,
            "meldung": "Kein relativer Pfad möglich: die Ordner liegen auf "
            "verschiedenen Laufwerken.",
        }

    # Jeder Bestandteil des relativen Pfads bekommt eine Rolle:
    # 'hoch' für .. (aus Ordner 1 heraus), 'runter' für den Weg nach Ordner 2.
    segmente = []
    for stueck in relativ.split(TRENNER):
        if stueck == "..":
            segmente.append({"text": "..", "rolle": "hoch"})
        elif stueck == ".":
            segmente.append({"text": ".", "rolle": "gleich"})
        else:
            segmente.append({"text": stueck, "rolle": "runter"})

    schritte_hoch = sum(1 for s in segmente if s["rolle"] == "hoch")
    schritte_runter = sum(1 for s in segmente if s["rolle"] == "runter")

    if relativ == ".":
        meldung = "Beide Ordner sind derselbe Ordner."
    else:
        stuecke = []
        if schritte_hoch:
            stuecke.append(
                "%d Ebene%s nach oben"
                % (schritte_hoch, "" if schritte_hoch == 1 else "n")
            )
        if schritte_runter:
            stuecke.append(
                "%d Ebene%s nach unten"
                % (schritte_runter, "" if schritte_runter == 1 else "n")
            )
        meldung = ", dann ".join(stuecke)

    return {
        "ok": True,
        "abs1": abs1,
        "abs2": abs2,
        "gemeinsam": gemeinsam,
        "rest1": rest1,
        "rest2": rest2,
        "relativ": relativ,
        "segmente": segmente,
        "trenner": TRENNER,
        "meldung": meldung,
    }


# ---------------------------------------------------------------------------
# Oberfläche
# ---------------------------------------------------------------------------

SEITE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pfad-Rechner</title>
<style>
  :root {
    --papier:      #f4f6f9;
    --karte:       #ffffff;
    --tinte:       #17202b;
    --gedaempft:   #64748b;
    --linie:       #dbe2ec;

    --gemeinsam-farbe: #0969da;
    --gemeinsam-flaeche: #e2edfc;

    --hoch-farbe:    #b45309;
    --hoch-flaeche:  #fdf0d5;

    --runter-farbe:   #0f766e;
    --runter-flaeche: #d3f4ee;

    --mono: "JetBrains Mono", "SF Mono", "Cascadia Mono", Consolas,
            "DejaVu Sans Mono", monospace;
    --text: "Helvetica Neue", Arial, "Segoe UI", sans-serif;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    padding: 40px 20px 64px;
    background: var(--papier);
    color: var(--tinte);
    font-family: var(--text);
    font-size: 15px;
    line-height: 1.55;
  }

  .huelle { max-width: 880px; margin: 0 auto; }

  /* --- Kopf ------------------------------------------------------------ */

  .augenbraue {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gedaempft);
    margin-bottom: 10px;
  }

  h1 {
    font-family: var(--mono);
    font-size: 30px;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin: 0 0 10px;
  }

  h1 .trenner { color: var(--gemeinsam-farbe); }

  .vorspann {
    margin: 0 0 32px;
    max-width: 60ch;
    color: var(--gedaempft);
  }

  /* --- Auswahl --------------------------------------------------------- */

  .wahl {
    background: var(--karte);
    border: 1px solid var(--linie);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 12px;
    display: flex;
    gap: 18px;
    align-items: center;
    flex-wrap: wrap;
  }

  .wahl-marke {
    font-family: var(--mono);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    width: 108px;
    flex-shrink: 0;
  }
  .wahl-marke small {
    display: block;
    font-weight: 400;
    letter-spacing: 0;
    text-transform: none;
    color: var(--gedaempft);
  }
  .wahl.eins .wahl-marke { color: var(--hoch-farbe); }
  .wahl.zwei .wahl-marke { color: var(--runter-farbe); }

  .wahl-pfad {
    flex: 1 1 320px;
    min-width: 0;
    font-family: var(--mono);
    font-size: 13px;
    color: var(--tinte);
    word-break: break-all;
  }
  .wahl-pfad.leer { color: #94a3b8; font-style: italic; }

  button {
    font-family: var(--text);
    font-size: 14px;
    border-radius: 7px;
    border: 1px solid var(--linie);
    background: #fff;
    color: var(--tinte);
    padding: 9px 16px;
    cursor: pointer;
    transition: background 0.12s, border-color 0.12s;
  }
  button:hover { background: #f1f5f9; border-color: #b9c4d4; }
  button:focus-visible {
    outline: 2px solid var(--gemeinsam-farbe);
    outline-offset: 2px;
  }
  button[disabled] { opacity: 0.5; cursor: default; }

  button.stark {
    background: var(--gemeinsam-farbe);
    border-color: var(--gemeinsam-farbe);
    color: #fff;
    font-weight: 600;
  }
  button.stark:hover { background: #0a5cb8; border-color: #0a5cb8; }

  button.leise {
    border: none;
    background: none;
    color: var(--gemeinsam-farbe);
    padding: 4px 6px;
    font-size: 13px;
  }
  button.leise:hover { background: #e8effa; }

  .leiste {
    display: flex;
    gap: 10px;
    align-items: center;
    margin: 18px 0 30px;
  }

  /* --- Ergebnis -------------------------------------------------------- */

  #ergebnis[hidden] { display: none; }

  .vergleich {
    background: var(--karte);
    border: 1px solid var(--linie);
    border-radius: 10px;
    padding: 22px;
    margin-bottom: 14px;
  }

  .zeile { margin-bottom: 18px; }
  .zeile:last-child { margin-bottom: 0; }

  .zeile-kopf {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 6px;
  }

  .etikett {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--gedaempft);
  }

  .pfadzeile {
    font-family: var(--mono);
    font-size: 14px;
    line-height: 1.9;
    word-break: break-all;
  }

  .stueck-gemeinsam {
    background: var(--gemeinsam-flaeche);
    color: var(--gemeinsam-farbe);
    padding: 3px 1px;
    border-radius: 3px;
  }
  .stueck-eins {
    background: var(--hoch-flaeche);
    color: var(--hoch-farbe);
    padding: 3px 1px;
    border-radius: 3px;
    font-weight: 600;
  }
  .stueck-zwei {
    background: var(--runter-flaeche);
    color: var(--runter-farbe);
    padding: 3px 1px;
    border-radius: 3px;
    font-weight: 600;
  }

  /* --- Relativer Pfad -------------------------------------------------- */

  .antwort {
    background: var(--karte);
    border: 1px solid var(--linie);
    border-left: 4px solid var(--gemeinsam-farbe);
    border-radius: 10px;
    padding: 22px;
  }

  .antwort-pfad {
    font-family: var(--mono);
    font-size: 22px;
    font-weight: 700;
    line-height: 1.7;
    word-break: break-all;
    margin: 4px 0 10px;
  }

  .seg-hoch   { color: var(--hoch-farbe);   background: var(--hoch-flaeche);
                padding: 2px 4px; border-radius: 4px; }
  .seg-runter { color: var(--runter-farbe); background: var(--runter-flaeche);
                padding: 2px 4px; border-radius: 4px; }
  .seg-gleich { color: var(--gedaempft); }
  .seg-trenner { color: #94a3b8; padding: 0 1px; }

  .erklaerung { color: var(--gedaempft); font-size: 14px; }

  .warnung {
    background: #fdf0d5;
    border: 1px solid #f0c98a;
    border-radius: 10px;
    padding: 16px 18px;
    color: var(--hoch-farbe);
  }

  /* --- Legende --------------------------------------------------------- */

  .legende {
    margin-top: 30px;
    padding-top: 18px;
    border-top: 1px solid var(--linie);
    font-size: 13px;
    color: var(--gedaempft);
    display: flex;
    gap: 22px;
    flex-wrap: wrap;
  }
  .legende span b { font-weight: 600; }
  .punkt {
    display: inline-block;
    width: 9px; height: 9px;
    border-radius: 2px;
    margin-right: 6px;
    vertical-align: baseline;
  }
  .punkt.g { background: var(--gemeinsam-farbe); }
  .punkt.h { background: var(--hoch-farbe); }
  .punkt.r { background: var(--runter-farbe); }

  .fuss {
    margin-top: 26px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    font-size: 13px;
    color: var(--gedaempft);
  }

  @media (prefers-reduced-motion: no-preference) {
    #ergebnis { animation: auftauchen 0.22s ease-out; }
    @keyframes auftauchen {
      from { opacity: 0; transform: translateY(5px); }
      to   { opacity: 1; transform: none; }
    }
  }
</style>
</head>
<body>
<div class="huelle">

  <p class="augenbraue">Absolut <span style="color:#0969da">/</span> Relativ</p>
  <h1>Pfad<span class="trenner">/</span>Rechner</h1>
  <p class="vorspann">
    Lege dir im Explorer bzw. Finder zwei Ordner an und wähle sie hier aus.
    Du siehst dann, wie ihre absoluten Pfade aussehen, wo sie sich trennen und
    wie der Weg vom einen zum anderen lautet.
  </p>

  <div class="wahl eins">
    <div class="wahl-marke">Ordner 1<small>Startpunkt</small></div>
    <button id="knopf1">Ordner 1 wählen</button>
    <div class="wahl-pfad leer" id="anzeige1">noch nichts gewählt</div>
  </div>

  <div class="wahl zwei">
    <div class="wahl-marke">Ordner 2<small>Zielpunkt</small></div>
    <button id="knopf2">Ordner 2 wählen</button>
    <div class="wahl-pfad leer" id="anzeige2">noch nichts gewählt</div>
  </div>

  <div class="leiste">
    <button class="stark" id="knopfRechnen" disabled>Pfade berechnen</button>
    <button class="leise" id="knopfTauschen" disabled>Richtung umkehren</button>
    <button class="leise" id="knopfLeeren">Zurücksetzen</button>
  </div>

  <div id="ergebnis" hidden></div>

  <div class="legende">
    <span><i class="punkt g"></i><b>gemeinsamer Teil</b> beider Pfade</span>
    <span><i class="punkt h"></i>aus Ordner 1 heraus (<b>..</b>)</span>
    <span><i class="punkt r"></i>nach Ordner 2 hinein</span>
  </div>

  <div class="fuss">
    <span>Läuft lokal auf deinem Rechner. Nichts wird gesendet oder gespeichert.</span>
    <button class="leise" id="knopfEnde">Beenden</button>
  </div>

</div>

<script>
  const zustand = { pfad1: "", pfad2: "" };

  const anzeige1 = document.getElementById("anzeige1");
  const anzeige2 = document.getElementById("anzeige2");
  const ergebnis = document.getElementById("ergebnis");
  const knopfRechnen  = document.getElementById("knopfRechnen");
  const knopfTauschen = document.getElementById("knopfTauschen");

  function schuetzen(text) {
    const hilf = document.createElement("div");
    hilf.textContent = text;
    return hilf.innerHTML;
  }

  function anzeigenAktualisieren() {
    for (const [feld, knoten] of [[1, anzeige1], [2, anzeige2]]) {
      const wert = zustand["pfad" + feld];
      knoten.textContent = wert || "noch nichts gewählt";
      knoten.classList.toggle("leer", !wert);
    }
    const beide = Boolean(zustand.pfad1 && zustand.pfad2);
    knopfRechnen.disabled = !beide;
    knopfTauschen.disabled = !beide;
  }

  async function ordnerWaehlen(feld) {
    const knopf = document.getElementById("knopf" + feld);
    const vorher = knopf.textContent;
    knopf.textContent = "Dialog läuft ...";
    knopf.disabled = true;
    try {
      const antwort = await fetch("/waehle?feld=" + feld);
      const daten = await antwort.json();
      if (daten.fehler) { alert(daten.fehler); }
      if (daten.pfad) { zustand["pfad" + feld] = daten.pfad; }
    } catch (fehler) {
      alert("Der Dialog konnte nicht geöffnet werden: " + fehler);
    } finally {
      knopf.textContent = vorher;
      knopf.disabled = false;
      anzeigenAktualisieren();
      if (zustand.pfad1 && zustand.pfad2) { berechnen(); }
    }
  }

  function pfadZeichnen(gemeinsam, rest, klasseRest) {
    let html = "";
    if (gemeinsam) {
      html += '<span class="stueck-gemeinsam">' + schuetzen(gemeinsam) + "</span>";
    }
    if (rest) {
      html += '<span class="' + klasseRest + '">' + schuetzen(rest) + "</span>";
    }
    return html;
  }

  function segmenteZeichnen(segmente, trenner) {
    return segmente.map(function (segment) {
      const klasse = { hoch: "seg-hoch", runter: "seg-runter", gleich: "seg-gleich" }[segment.rolle];
      return '<span class="' + klasse + '">' + schuetzen(segment.text) + "</span>";
    }).join('<span class="seg-trenner">' + schuetzen(trenner) + "</span>");
  }

  function ergebnisZeichnen(daten) {
    if (!daten.ok) {
      let html = "";
      if (daten.abs1) {
        html += '<div class="vergleich">'
             +  '<div class="zeile"><div class="etikett">Absoluter Pfad, Ordner 1</div>'
             +  '<div class="pfadzeile"><span class="stueck-eins">' + schuetzen(daten.abs1) + "</span></div></div>"
             +  '<div class="zeile"><div class="etikett">Absoluter Pfad, Ordner 2</div>'
             +  '<div class="pfadzeile"><span class="stueck-zwei">' + schuetzen(daten.abs2) + "</span></div></div>"
             +  "</div>";
      }
      html += '<div class="warnung">' + schuetzen(daten.meldung) + "</div>";
      ergebnis.innerHTML = html;
      ergebnis.hidden = false;
      return;
    }

    ergebnis.innerHTML =
        '<div class="vergleich">'
      +   '<div class="zeile">'
      +     '<div class="zeile-kopf"><span class="etikett">Absoluter Pfad, Ordner 1</span>'
      +       '<button class="leise" data-kopieren="' + schuetzen(daten.abs1) + '">kopieren</button></div>'
      +     '<div class="pfadzeile">' + pfadZeichnen(daten.gemeinsam, daten.rest1, "stueck-eins") + "</div>"
      +   "</div>"
      +   '<div class="zeile">'
      +     '<div class="zeile-kopf"><span class="etikett">Absoluter Pfad, Ordner 2</span>'
      +       '<button class="leise" data-kopieren="' + schuetzen(daten.abs2) + '">kopieren</button></div>'
      +     '<div class="pfadzeile">' + pfadZeichnen(daten.gemeinsam, daten.rest2, "stueck-zwei") + "</div>"
      +   "</div>"
      + "</div>"
      + '<div class="antwort">'
      +   '<div class="zeile-kopf"><span class="etikett">Relativer Pfad, von Ordner 1 nach Ordner 2</span>'
      +     '<button class="leise" data-kopieren="' + schuetzen(daten.relativ) + '">kopieren</button></div>'
      +   '<div class="antwort-pfad">' + segmenteZeichnen(daten.segmente, daten.trenner) + "</div>"
      +   '<div class="erklaerung">' + schuetzen(daten.meldung) + "</div>"
      + "</div>";
    ergebnis.hidden = false;
  }

  async function berechnen() {
    const abfrage = new URLSearchParams({ eins: zustand.pfad1, zwei: zustand.pfad2 });
    const antwort = await fetch("/berechne?" + abfrage.toString());
    ergebnisZeichnen(await antwort.json());
  }

  document.getElementById("knopf1").addEventListener("click", () => ordnerWaehlen(1));
  document.getElementById("knopf2").addEventListener("click", () => ordnerWaehlen(2));
  knopfRechnen.addEventListener("click", berechnen);

  knopfTauschen.addEventListener("click", function () {
    [zustand.pfad1, zustand.pfad2] = [zustand.pfad2, zustand.pfad1];
    anzeigenAktualisieren();
    berechnen();
  });

  document.getElementById("knopfLeeren").addEventListener("click", function () {
    zustand.pfad1 = "";
    zustand.pfad2 = "";
    ergebnis.hidden = true;
    anzeigenAktualisieren();
  });

  document.getElementById("knopfEnde").addEventListener("click", async function () {
    await fetch("/beenden");
    document.body.innerHTML =
      '<div class="huelle"><h1>Beendet</h1>'
      + '<p class="vorspann">Der Pfad-Rechner wurde geschlossen. '
      + "Du kannst dieses Fenster jetzt schließen.</p></div>";
  });

  // Kopier-Knöpfe: ein Zuhörer für alle, auch für später erzeugte.
  document.addEventListener("click", async function (ereignis) {
    const knopf = ereignis.target.closest("[data-kopieren]");
    if (!knopf) { return; }
    try {
      await navigator.clipboard.writeText(knopf.dataset.kopieren);
    } catch (fehler) {
      const hilf = document.createElement("textarea");
      hilf.value = knopf.dataset.kopieren;
      document.body.appendChild(hilf);
      hilf.select();
      document.execCommand("copy");
      hilf.remove();
    }
    const vorher = knopf.textContent;
    knopf.textContent = "kopiert";
    setTimeout(() => { knopf.textContent = vorher; }, 1200);
  });

  anzeigenAktualisieren();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Webserver
# ---------------------------------------------------------------------------


class Anfragebehandlung(http.server.BaseHTTPRequestHandler):
    server_version = "Pfadrechner"

    def log_message(self, *args):
        pass  # Konsole bleibt sauber

    def _senden(self, inhalt: bytes, typ: str):
        self.send_response(200)
        self.send_header("Content-Type", typ)
        self.send_header("Content-Length", str(len(inhalt)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(inhalt)

    def _json(self, daten: dict):
        self._senden(
            json.dumps(daten, ensure_ascii=False).encode("utf-8"),
            "application/json; charset=utf-8",
        )

    def do_GET(self):
        zerlegt = urllib.parse.urlparse(self.path)
        route = zerlegt.path
        werte = urllib.parse.parse_qs(zerlegt.query)

        if route in ("/", "/index.html"):
            self._senden(SEITE.encode("utf-8"), "text/html; charset=utf-8")

        elif route == "/waehle":
            feld = werte.get("feld", ["1"])[0]
            titel = "Ordner %s auswählen" % ("2" if feld == "2" else "1")
            with DIALOG_SPERRE:
                self._json(ordner_waehlen(titel))

        elif route == "/berechne":
            self._json(
                pfade_analysieren(
                    werte.get("eins", [""])[0], werte.get("zwei", [""])[0]
                )
            )

        elif route == "/beenden":
            self._json({"ok": True})
            threading.Thread(target=self.server.shutdown, daemon=True).start()

        else:
            self.send_error(404, "Unbekannte Adresse")


def freier_port() -> int:
    with socket.socket() as verbindung:
        verbindung.bind(("127.0.0.1", 0))
        return verbindung.getsockname()[1]


def main():
    port = freier_port()
    adresse = "http://127.0.0.1:%d/" % port
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Anfragebehandlung)

    print("Pfad-Rechner läuft:", adresse)
    print("Beenden: Button in der Oberfläche oder Strg+C\n")
    threading.Timer(0.6, lambda: webbrowser.open(adresse)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Beendet.")


if __name__ == "__main__":
    main()
