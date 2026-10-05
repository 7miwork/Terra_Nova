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

## Umsetzungsstand Phase 5: Balancing, Zufallsereignisse, Statistik

Die Wunschliste der Schülerinnen und Schüler ist als zwei neue Module
eingebaut — `ereignisse.py` und `statistik.py`.

### Balancing

| Gebäude | vorher | nachher | Grund |
|---|---|---|---|
| Fusionsreaktor (10) | 25 Energie | **20** | war zu stark |
| Gewächshaus (13) | 8 Nahrung | **6** | Nahrung wird später Überschuss |
| Marktplatz (5) | 12 Gold | **10** | Gold war zu stark |

Der Ressourcenhandel kostet jetzt **3 Einheiten für 1** statt 2:1
(`handel.TAUSCH_VERHALTNIS`). Der alte Kurs erlaubte es, den kompletten
Überschuss billig in knappe Ressourcen umzurechnen — das war eine zweite
Produktionskette. Menütext, Hilfe-Overlay und Handelsfenster benutzen alle
dieselbe Konstante, damit nichts auseinanderläuft.

### Zufallsereignisse (`ereignisse.py`)

Ein Wirtschaftstick dauert eine Sekunde Spielzeit, deshalb sind „3 Minuten“
konstant `DAUER_TICKS = 180`. Die Effekte liegen bewusst in `ressourcen.py`,
damit sie ohne pygame testbar sind:

- **Systemausfall** setzt `energie_stoerung_setzen(180)`. In
  `_produktion_multiplikator()` bekommen alle Energiegebäude den Faktor
  `SYSTEMAUSFALL_FAKTOR` (0,70). `systemausfall_reparieren()` kostet 100 Gold
  und setzt den Zähler auf 0. Taste **R** im Spiel.
- **Meteoritenschauer** markiert bis zu 10 zufällige Gebäude mit
  `beschaedigt_rest`. In `ressourcen_produzieren()` bekommen sie den Faktor
  `BESCHAEDIGT_FAKTOR` (0,20); `_schaden_ticken()` zählt jeden Tick herunter.
- **Unbekanntes Raumschiff** öffnet ein modales Fenster: **Q W E R T Z X**
  wählen die Ressource, Pfeiltasten ändern die Menge in 5er-Schritten
  (Deckel 75), **Enter** setzt ein, **Esc** lehnt ab. Gewonnen heißt
  +2 × Einsatz, verloren heißt −Einsatz (jeweils 50 %). Solange das Fenster
  offen ist, hält `main.py` die Wirtschaft an — sonst wäre die Fracht weg,
  während man wählt.

Ereignisse starten frühestens nach 90 bis 180 Ticks und danach alle 60 bis
150 Ticks. Ein laufender Systemausfall wird nicht doppelt ausgelöst.

### Gesamtstatistik (`statistik.py`)

Eine eigene Datei `statistik.json` (in `.gitignore`), die **alle Partien**
zählt: gespielte/gewonnene/verlorene Partien, Spielzeit, Gebäude,
Forschungspunkte, Handelsaktionen, Technologien, größte Kolonie, Achievements
und die Häufigkeit der Ereignisse. Angezeigt im Hauptmenü über **T**, jeweils
neben dem Wert der laufenden Partie. Die beiden Langzeit-Achievements
(100 Gebäude, 1000 Forschungspunkte) lesen genau diese Werte.

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

## Fallstricke aus Phase 5 (zum Nachschlagen)

5. **`laden()` liest aus dem falschen Wörterbuch**: Wer in einer Ladefunktion
   erst das Profil leert und danach `_profil[name] = _zahl(name)` schreibt,
   bekommt immer 0 — `_zahl()` liest das gerade geleerte Profil. Die Werte
   müssen aus den geladenen Daten (`daten[name]`) kommen. Der Test
   „speichern, zurücksetzen, laden“ deckt das sofort auf.
6. **`pygame.K_EQUAL` gibt es nicht**: Die Taste heißt `K_EQUALS` (ebenso
   `K_KP_EQUALS` für den Zahlenblock). Ein Tippfehler fällt erst zur Laufzeit
   auf, wenn der Spieler die Taste drückt.
7. **Zufällige Treffer im Test nicht per Index annehmen**: Der
   Meteoritenschauer wählt seine Gebäude mit `random.sample()`. Ein Test, der
   „die Indizes 5–14 sind beschädigt“ annimmt, schlägt fehl. Die Testliste
   nach `gebaeude_beschaedigt()` filtern, wie in
   `tests/test_schuelerwuensche.py`.
8. **Rücksetzfunktionen zuerst aufrufen**: `ressourcen.zustand_importieren({})`
   leert auch die Energiestörung. Wer erst zurücksetzt und dann ein Ereignis
   auslöst, testet eine andere Reihenfolge als das Spiel (dort produziert
   `ressourcen_produzieren()` zuerst, `ereignisse.ereignisse_tick()` danach).
9. **Achievement-Ziele brauchen drei Stellen**: Eintrag in `ACHIEVEMENTS`,
   Zeile im `bedingungen`-Dict von `pruefen()` und ein Zähler, der gefüllt
   wird. Die Langzeit-Achievements lesen ihre Zahl zusätzlich aus dem
   Statistikprofil (`pruefen(..., profil=statistik.profil())`).
   Bei 3 × 13 Plätzen passt höchstens bis 37 Zielen in die Übersicht.

## Offene Ideen zum Gegnersystem (noch nicht umgesetzt)

- David/Julian: Hier kommt eure nächste Idee hin (z. B. unterschiedliche
  Gegnerflotten, Reparatur geplünderter Lager, eigene Gegner-Skripte).
  Beschreibt zuerst die Regel, dann die Formel, dann den Testfall.

