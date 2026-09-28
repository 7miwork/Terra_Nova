# Debugging-Hinweise für Stunde 9

Diesmal keine eingebauten Fehler — falls doch etwas nicht funktioniert,
hier nachfragen!

Damit du weißt, worauf du beim Testen achten kannst, hier ein paar
Hinweise zu den neuen Features:

## 1. Gebäude abreißen (Rechtsklick)

* Funktionieren Rechtsklick (Abriss) und Linksklick (Bauen) unabhängig voneinander?
* Bekommst du wirklich **50 %** der Baukosten zurück (abgerundet)?
  z.B. ein Reaktor kostet 20 Gold → beim Abriss +10 Gold.
* Kann die **Basis** nicht abgerissen werden? Es sollte eine Konsolenmeldung erscheinen.

## 2. Baumenü (Taste TAB)

* Öffnet und schließt `TAB` das Menü?
* Sind alle 7 Gebäudetypen zu sehen — mit Baukosten, Kürzel und Taste?
* Werden gesperrte Gebäude (z.B. Marktplatz) ausgegraut und mit 🔒 + Hinweistext angezeigt?

## 3. Freischaltung

* Ist der Marktplatz erst ab **5 Bevölkerung** bauen? Das Wohnhaus erst ab **20 Holz**?
* Im Baumenü solltest du genau sehen, was zum Freischalten noch fehlt.

## 4. Tooltip beim Rohstoff-Icon

* Fährst du mit der Maus über ein Icon oben, erscheint die kleine Box?
* Zeigt sie die richtigen produzierenden/verbrauchenden Gebäude?

## 5. Rote Meldung

* Erscheint oben eine rote Meldung, wenn du versuchst zu bauen, aber zu wenig
  Rohstoffe da sind? Verschwindet sie nach ~2 Sekunden wieder?


# Aktualisierte Debugging-Checkliste

Die alten Hinweise mit „7 Gebäudetypen“ gelten nicht mehr. Die aktuelle Version besitzt 18 Gebäude und kategorisierte Auswahl.

## Kategorien und Geschwindigkeit

- Drückt `1` bis `9`: Wird die passende Kategorie im HUD angezeigt?
- Drückt Pfeil links/rechts: Wechselt das Gebäude innerhalb der Kategorie und ändert sich die Bildvorschau?
- Baut ein Gebäude, drückt danach `0` und prüft den Schnellzugriff.
- Prüft, dass `+/-` die Geschwindigkeit verändern und Zifferntasten weiterhin Kategorien wählen.

## Bilder

- Existieren für alle 18 Gebäudetypen die in `gebaeude.py` genannten PNG-Dateien?
- Sind die 1×1-Dateien 64×64 Pixel groß?
- Ist das Universitätsbild 64×96 Pixel groß und transparent?
- Gibt es noch eine unbenutzte `labor.png`? Sie soll nicht mehr zum aktiven Bilderordner gehören.

## Wirtschaft und Personal

- Produziert die Basis pro Tick Gold, Energie, Holz und Stein?
- Arbeitet ein Gebäude nicht, wenn Bevölkerung plus Roboter nicht für alle Personalbedarfe reicht?
- Erzeugt die Roboterfabrik Roboter und können diese danach ein weiteres Gebäude besetzen?
- Wird Eisen von der Mine erzeugt und im Stahlwerk zu Stahl verarbeitet?
- Erhöht ein gebautes Lagerhaus zusammen mit `lagerhaus_ausbau` die Speichergrenzen?
- Erzeugt das Koloniezentrum den dokumentierten globalen Produktionsbonus?

## Große Gebäude

- Wird die Universität als 2×3-Rechteck platziert?
- Wird sie am Kartenrand oder bei Überschneidung abgelehnt?
- Entfernt ein Rechtsklick auf jede der sechs Teilkacheln genau ein Universitätsobjekt und erstattet nur einmal?

## Automatischer Test

```bash
python3 test_stunde11.py
```

Erwartet wird `STUNDE11_TESTS_OK`. Wenn der Test fehlschlägt, zuerst die angegebene Zeile lesen und dann nur eine Änderung gleichzeitig durchführen.
