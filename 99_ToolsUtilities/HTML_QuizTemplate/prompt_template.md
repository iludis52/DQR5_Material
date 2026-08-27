Ich benötige [ANZAHL] Multiple-Choice-Fragen zum Thema "[THEMA]" für ein JavaScript-basiertes Quiz-Template.

[X] der Fragen (z.B. Frage 1 und 3) sollen sich auf eine bestimmte SVG-Grafik beziehen. Die restlichen Fragen benötigen kein Bild.

Bitte liefere mir den Code streng nach den folgenden Vorgaben:

1. **Das JavaScript-Array (`questions`):**
   - Jedes Fragen-Objekt muss diese Struktur haben: `text` (String), `options` (Array aus 3-4 Strings), `correct` (Integer, Index der richtigen Antwort), `explanation` (String, Erklärung der Lösung).
   - Für Fragen, die ein Bild benötigen, füge dem Objekt den Key `svgId: "eine-eindeutige-id"` hinzu.
   - Fragen ohne Bild erhalten den Key `svgId` NICHT.

2. **Die SVG-Assets (am Ende des HTML-Dokuments):**
   - Liefere mir im Anschluss an das Array den HTML-Block für die SVGs.
   - Der Block muss so strukturiert sein:
     <div id="svg-assets" style="display: none;">
         <div id="eine-eindeutige-id">
             </div>
     </div>
   - Stelle sicher, dass die `id` des divs exakt mit dem String übereinstimmt, der in der Frage unter `svgId` angegeben wurde.

Erstelle mir nun den Code für [ANZAHL] Fragen zum Thema "[THEMA]". 
Frage [NUMMER] soll sich auf dieses SVG beziehen: "[BESCHREIBUNG ODER QUELLCODE DES SVGS]".