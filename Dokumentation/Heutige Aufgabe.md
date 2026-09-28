# Heutige Aufgabe — Stunde 10

Heute haben wir das Forschungssystem eingebaut! Jetzt kannst du das Spiel
weiter anpassen und verbessern.

## Aufgaben für heute

### 1. Bilder für die Kacheln erstellen (Quadrat-Form)

Bisher werden die Gebäude nur als farbige Quadrate gezeichnet. Jetzt sollst
du eigene **Bilder** für die Kacheln erstellen:

- Suche oder zeichne kleine Bilder (am besten im Format **Quadrat**, z.B.
  32×32 Pixel) für jedes Gebäude:
  - Basis, Reaktor, Farm, Holzfäller, Steinmetz, Marktplatz, Wohnhaus, Labor
- Speichere die Bilder im Ordner `bilder/` (erstelle ihn falls er nicht existiert).
- Passe den Code in `gebaeude.py` an, sodass die Bilder anstelle der einfachen
  Quadrate gezeichnet werden.
  - Tipp: `pygame.image.load("bilder/basis.png")` lädt ein Bild.
  - Mit `pygame.transform.scale(bild, (groesse, groesse))` kannst du es auf
    die passende Kachel-Größe bringen.
- Achte darauf, dass die Bilder **transparente Hintergründe** haben (PNG-Format).

### 2. Gebäude-Werte anpassen

Die aktuellen Werte (Baukosten, Produktion, Verbrauch) sind noch nicht
perfekt abgestimmt. Probiere aus und finde bessere Werte:

- Öffne `ressourcen.py` und schaue dir `GEBAEUDE_WIRTSCHAFT` an.
- Ändere einzelne Werte und beobachte, wie sich das Spiel verändert.
  - Beispiel: Den Holzfäller von `+6 Holz` auf `+8 Holz` erhöhen.
  - Beispiel: Den Reaktor von `−2 Holz` auf `−1 Holz` verringern.
- Teste im Spiel: Laufen die Ressourcen aus? Wird die Kolonie zu schnell zu reich?
- Schreibe deine Lieblingswerte auf und begründe, warum du sie gewählt hast.

### 3. Forschungen anpassen / Namen ändern

Das Forschungsmenü (Taste F) ist noch sehr einfach. Erweitere es:

- Öffne `forschung.py` und schaue dir `TECHNOLOGIEN` an.
- Ändere die **Namen** oder **Beschreibungen** der Technologien.
- Passe die **Kosten** an (z.B. Wohnbau von 30 auf 20 Punkte senken).
- Füge eine **neue Technologie** hinzu:
  - Lege eine neues Dictionary in `TECHNOLOGIEN` an.
  - Lasse es ein neues Gebäude freischalten oder einen Bonus geben.
  - Überlege dir eine sinnvolle `voraussetzung` (z.B. muss erst
    "stein_effizienz" erforscht sein, bevor man "produktion" erforschen kann).
- Teste im Spiel: Kann man die neue Technologie erforschen? Wird das Gebäude
  wirklich freigeschaltet?

### 4. Weitere Fehler suchen

Das Spiel hat absichtlich ein paar kleine Fehler eingebaut, damit ihr
üben könnt, sie zu finden. Schau dir folgende Stellen genau an:

- **In `ressourcen.py`:** Die Liste `gebaeude_namen` in der Funktion
  `ressourcen_produzieren()` — ist der Marktplatz (Index 5) enthalten?
  Was passiert, wenn er fehlt?
- **In `hud.py`:** Die Ressourcen-Leiste zeigt jetzt 6 Icons. Sind alle
  richtig positioniert? Überlappen sie?
- **In `main.py`:** Die Taste `8` wählt das Labor aus. Wird das Labor auch
  im HUD unten angezeigt (mit Produktion und Verbrauch)?
- **In `forschung.py`:** Was passiert, wenn man eine Technologie erforscht,
  deren `voraussetzung` nicht erfüllt ist?

Findest du alle Fehler? Behebe sie und teste, ob das Spiel weiterhin läuft!

### 5. Verbesserungsvorschläge

Du hast jetzt einen guten Überblick über das Spiel. Was könnte man noch
verbessern? Notiere deine Ideen:

- Welche **neuen Gebäude** könnte man noch hinzufügen?
J: Parks, Baeume, Luftreiniger
D: Minen (Kohle)
- Welche **neuen Technologien** wären spannend?
J: Luftreiniger (kann verbessert werden)
D: Verbesserter Reaktor (Kohle), verbesserungen der produktion und verbauch
- Sollte man Gebäude auch **upgraden** können (z.B. Reaktor Stufe 2)?
J: Ja Luftreiniger, 
D: Minen (Kohle, unregelmaessig Eisen/Diamanten), Verbesserter Reaktor (Kohle, unregelmaessig Diamanten)
- Braucht das Spiel eine **Speichern/Laden**-Funktion?
J: 
D: Ja
- Was fehlt dir noch im **Baumenü** oder **Forschungsmenü**?
J: Forschungsmenu: Baum oder Mindmap system
D: Baumenue: Verbrauch und Produktion, 
- Sonstige Aenderungen:
J: den Ressourcen verbrauch und generierung die ticks aendern, Luftverschmutzung
D: 

Schreibe deine Ideen auf — die besten Vorschläge werden vielleicht in der
nächsten Stunde umgesetzt!

## Tipp

- Nutze die Konsolenausgabe (`print`), um zu verstehen, was passiert.
- Ändere immer nur EINE Sache auf einmal — dann siehst du, was die Änderung bewirkt.
- Wenn etwas nicht klappt, frage deinen Sitznachbarn oder den Lehrer!



# Aktualisierte Projektaufgabe: Kategorien und vollständige Gebäude

Die ältere Einzelbelegung der Zifferntasten wird in der aktuellen Version ersetzt. `1` bis `9` wählen Kategorien, links/rechts wechseln innerhalb der Kategorie, `0` wählt das zuletzt gebaute Gebäude und `+/-` steuern die Geschwindigkeit. Damit können mehrere Schülerinnen und Schüler parallel eigene Gebäudekategorien erweitern.

## Pflichtaufgabe A: Kategorien verstehen

Öffnet `gebaeude.py` und untersucht `GEBAEUDE_KATEGORIEN`. Ergänzt ein neues Gebäude in mindestens einer sinnvollen Kategorie. Verwendet den vorhandenen Index und legt keine zweite Kopie der Wirtschaftsdaten an. Testet danach Zifferntaste, Pfeil links/rechts und die Bildvorschau im HUD.

## Pflichtaufgabe B: Neue Gebäude vollständig einbauen

Die aktuelle Liste umfasst 18 Gebäude. Ergänzt bei einer eigenen Idee immer alle vier Bereiche: Gebäudedaten in `gebaeude.py`, Wirtschaftsdaten an derselben Position in `ressourcen.py`, Bilddatei in `bilder/` und Forschung/Freischaltung in `forschung.py`. Ein Gebäude ist erst fertig, wenn es im Baumenü auftaucht, eine Kategorie besitzt, gebaut werden kann, produziert oder verbraucht und im Selbsttest vorkommt.

## Pflichtaufgabe C: Produktionsketten

Untersucht die Kette Mine → Eisen und Kohle → Stahlwerk → Stahl. Ergänzt bei Bedarf eine eigene Weiterverarbeitung. Achtet auf die parallelen Ressourcenlisten und darauf, dass jede Ressource ein Speicherlimit besitzt. Testet auch, ob ein Lagerhaus zusammen mit `lagerhaus_ausbau` die Speichergrenze tatsächlich verändert.

## Pflichtaufgabe D: Bilder

Erstellt ein eigenes 64×64-PNG für ein 1×1-Gebäude oder ein 64×96-PNG für ein 2×3-Gebäude. Speichert es mit transparentem Hintergrund in `bilder/`, tragt den Dateinamen in `gebaeude.py` ein und startet das Spiel neu. Die genaue Anleitung steht in `BILDER_ANLEITUNG.md`. `labor.png` wird nicht mehr verwendet, weil die Universität das Labor ersetzt.

## Pflichtaufgabe E: Testen und dokumentieren

Führt nach jeder größeren Änderung `python3 test_stunde11.py` aus. Dokumentiert anschließend: Welche Datei wurde geändert? Welche Spielregel ist neu? Welche Taste oder Forschung aktiviert sie? Was ist der Testfall? Ein Test ist erst vollständig, wenn nicht nur das Menü, sondern die echte Wirtschaftswirkung überprüft wurde.
