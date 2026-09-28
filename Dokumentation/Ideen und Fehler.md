David:
die mine als gebaeude + Forschung dass Reaktoren kohle für höhere Produktionsraten benutzen können + Forschung dass mine alle 10 ticks oder seltener 1 eisen produziert

Julian:

 Gebäude für Bildung um vielleicht die gesamte Produktion um ca. 1- 5% steigert was sich dann im weiteren spielverlauf sehr gut auszahlt weil die wenigen Prozente dann mehr ausmachen

Richtige anordnung:

Labor zur Universitaet umgewandelt: Je mehr Studenten desto schneller wird geforscht aber kostet mehr, spaeter wenn leute studiert haben steigern sie die produktion wo sie arbeiten (update), und das Gebaude soll grosser als eine Kachel sein sondern 2x3

Ausserdem Strassen


## Umsetzungsstand der Ideen

Die Bildungs-Idee wurde als Universität umgesetzt. Die Universität verwendet das angehängte Schulbild, ist 2 Kacheln breit und 3 Kacheln hoch, benötigt zwei Arbeitskräfte und erzeugt Forschungspunkte. Forschungen laufen nur weiter, wenn mindestens eine Universität tatsächlich arbeitet.

Die Mine erzeugt Kohle und regelmäßig Eisen. Das Stahlwerk verarbeitet Eisen und Kohle zu Stahl. Straßen sind als eigenes Gebäude vorhanden. Zusätzliche Ideen wie Gewächshaus, Lagerhaus, Wohnblock, Handelsposten und Koloniezentrum sind ebenfalls als Gebäude mit eigenen Bildern, Wirtschaftsdaten und Forschungsfreischaltungen eingebaut.

Die frühere feste Tastaturbelegung wurde durch Kategorien ersetzt. So können neue Schülerideen ergänzt werden, ohne jedes Gebäude auf eine neue feste Ziffer legen zu müssen. Die genauen Regeln stehen in `STUNDE11_DESIGN.md`.

## Umsetzungsstand Phase 4: Gegner und Verteidigung

Die Schülerwunschliste „Gegner/Verteidigung“ ist als Modul `gegner.py` eingebaut:

- Ein Zustandsautomat fährt jede Kolonie durch **Frieden (150 Ticks Start,
  danach 100–160) → Warnung (25 Ticks) → Gefecht**. Die Warnung spielt die
  Sirene und zeigt im Verteidigungs-Panel rechts Angriffsstärke und Countdown;
  nach dem Gefecht steht 6 Sekunden das Ergebnis-Banner mittig.
- **Abwehr** zahlt 40 + 20 × Welle Gold und 10 × Welle Forschung, kostet aber
  20 % der Verteidiger und Raumschiffe (auch wenn nichts passiert ist).
- **Niederlage** nimmt 30 % von acht Rohstoffen mit (Gold, Energie, Holz,
  Stein, Nahrung, Kohle, Eisen, Stahl). Bevölkerung, Forschung, Roboter,
  Zufriedenheit, Verteidiger und Raumschiffe sind ausdrücklich geschützt —
  Plünderung allein führt nie zu Game Over.
- Neue Gebäude: **Kaserne (21)** bildet Verteidiger aus (max. 30 % der
  Bevölkerung), **Raumschiffwerft (22)** baut Schiffe (je 6 Stärke),
  **Laserturm (23)** verteidigt mit 10 Stärke, solange er arbeitet.
- Neue Forschungen: Militärtraining, Raumschiffbau, Laserverteidigung,
  Schutzschilde (+25 % Verteidigung). Kategorie 9 heißt jetzt
  „Spezial / Verteidigung“.
- Die Regelwerke tragen die Felder `gegner_aktiv`/`gegner_faktor`:
  Entspannt und Freies Spiel sind ohne Angriffe, Überleben rechnet mit 1.3.
- Drei Achievements („Erste Abwehr“, „Festung“, „Flotte“) und die Mission
  „Kaserne bauen“ belohnen den Einstieg. Alte Spielstände laden weiterhin.

## Bekannte Fehlerquellen aus dieser Phase (zum Nachschlagen)

1. **`UnboundLocalError` in Modulvariablen**: Wer in einer Funktion eine
   Modulvariable nur liest, braucht kein `global`; wer sie *schreibt*, braucht
   es — auch wenn nur bedingt geschrieben wird (`_banner` in `gegner.py`).
2. **Neues Achievement vergessen**: In `achievements.pruefen()` gibt es ein
   festes `bedingungen`-Dict. Ein neuer Eintrag in `ACHIEVEMENTS` wird ohne
   passende Zeile dort nie erreicht — der Test bricht mit „nicht in neue“.
3. **`main.py` und gemischte Zeilenenden**: Mehrzeilige Ersetzungen schlagen
   fehl, wenn eine Zeile CRLF und die andere LF hat. Workaround: einzeilige
   Anker nehmen oder ein Python-Patchskript mit `\\r?\\n` schreiben.
4. **Werte im Test raten**: Die Kaserne produziert 0.5 Verteidiger pro Tick —
   Wer im Test 0.05 erwartet, bekommt einen sonderbaren Fehler. Immer in
   `ressourcen.GEBAEUDE_WIRTSCHAFT` nachschauen statt aus dem Gedächtnis.

## Umsetzungsstand: Oberfläche aufgeräumt (schwebende Fenster)

Die Überlappungen aus dem Screenshot sind behoben:

- **`panel.py` (neu):** Alle Info-Kästen sind schwebende Fenster — an der
  Titelzeile verschiebbar, mit **–** minimierbar, mit **X** ausblendbar,
  immer im Bild geklemmt. Tasten: **S** Verteidigung, **C** Bauinfo,
  **I** Übersicht, **O** Ziel, **L** Layout zurücksetzen.
- **Ressourcenleiste:** berechnet Spalten und Schriftgröße selbst
  (`hud.ressourcen_leiste_layout`). Vorher: feste 162-Pixel-Spalten, dadurch
  lief „Bevoelkerung: 24/100“ in „Nahrung“ hinein und „Zufriedenheit“ wurde
  am Rand abgeschnitten.
- **Ziel-Fenster:** lag früher fest im HUD-Balken (y=54) und verdeckte die
  Ressourcen; jetzt ein Panel unterhalb des HUD (Standardposition 762/248).
- **Übersicht:** Kamera-, Karten-, Boden- und Personal-Texte sind aus dem
  Kartenbild in ein Fenster gewandert (links oben).
- **Klicks:** Ein Klick in ein Fenster wird verbraucht — man baut nie
  versehentlich ein Gebäude unter einem Panel.
- **Test:** `tests/test_fortgeschritten_panels.py` prüft Anordnung, Ziehen,
  Klemmen, Minimieren, Schließen, Klicken und das Leisten-Layout.
  Zusätzlich `unnoetig/vorschau.py` rendert ein PNG zur Sichtprüfung.

**Offene Idee für euch:** Fenster-Transparenz einstellbar machen oder
Fensterinhalte per Rechtsklick umschalten (z. B. Übersicht → nur Personal).

## Offene Ideen zum Gegnersystem (noch nicht umgesetzt)

- David/Julian: Hier kommt eure nächste Idee hin (z. B. unterschiedliche
  Gegnerflotten, Reparatur geplünderter Lager, eigene Gegner-Skripte).
  Beschreibt zuerst die Regel, dann die Formel, dann den Testfall.

