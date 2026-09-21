# Eigene Gebäude-Bilder einfügen

## Ziel

Jedes Gebäude kann ein eigenes PNG-Bild erhalten. Das Spiel lädt die Bilder automatisch aus dem Ordner `bilder/` und skaliert sie auf die Gebäudekachel.

## Dateinamen-Tabelle

| Gebäude | Eintrag in `gebaeude.py` | Datei im Ordner `bilder/` |
|---|---|---|
| Basis | `"bild": "basis.png"` | `bilder/basis.png` |
| Reaktor | `"bild": "reaktor.png"` | `bilder/reaktor.png` |
| Farm | `"bild": "farm.png"` | `bilder/farm.png` |
| Holzfäller | `"bild": "holzfaeller.png"` | `bilder/holzfaeller.png` |
| Steinmetz | `"bild": "steinmetz.png"` | `bilder/steinmetz.png` |
| Marktplatz | `"bild": "marktplatz.png"` | `bilder/marktplatz.png` |
| Wohnhaus | `"bild": "wohnhaus.png"` | `bilder/wohnhaus.png` |
| Universität / Schulgebäude | `"bild": "schule_2x3_kacheln_64x96.png"` | `bilder/schule_2x3_kacheln_64x96.png` (64×96 Pixel, Seitenverhältnis 2:3) |
| Mine | `"bild": None` | optional eigenes Bild |
| Straße | `"bild": None` | optional eigenes Bild |
| Fusionsreaktor | `"bild": None` | optional `fusionsreaktor.png` |
| Roboterfabrik | `"bild": None` | optional `roboterfabrik.png` |

## Schritt-für-Schritt-Anleitung

### 1. Bild erstellen

Erstellt eine quadratische Grafik, zum Beispiel mit 64 × 64 Pixeln. Zeichnet das Gebäude möglichst groß, aber lasst am Rand etwas Abstand. Ein transparentes PNG sieht im Spiel am besten aus, weil die Bodenfarbe um das Gebäude sichtbar bleibt.

### 2. Bild als PNG exportieren

Verwendet beim Export das Format PNG. Wenn das Zeichenprogramm nach einem Alpha-Kanal oder Transparenz fragt, muss diese Option aktiviert werden. Ein Bild mit weißem Hintergrund wird im Spiel als weißes Rechteck erscheinen.

### 3. Datei kopieren

Kopiert die Datei in den Ordner `bilder/`, der neben `main.py` und `gebaeude.py` liegt. Der Dateiname muss genau mit dem Wert im Dictionary übereinstimmen.

Beispiel:

```python
{
    "name": "Fusionsreaktor",
    "bild": "fusionsreaktor.png",
    "farbe": (255, 110, 210),
    "kuerzel": "F",
    "taste": "G",
},
```

Dazu muss die Datei exakt hier liegen:

```text
Stunde 11/bilder/fusionsreaktor.png
```

### 4. Spiel neu starten

Die Bilder werden beim Start in `gebaeude_initialisieren()` geladen. Nach dem Kopieren muss das Spiel neu gestartet werden. Ein bloßes Zurückkehren zum Menü lädt die Datei nicht erneut.

### 5. Fallback prüfen

Wenn eine Datei nicht gefunden wird, stürzt das Spiel nicht ab. Es zeichnet stattdessen ein farbiges Rechteck mit dem Wert aus `"farbe"`. Das ist hilfreich beim Programmieren, weil ihr zuerst die Spiellogik testen könnt und das Bild später ergänzt.

## Technischer Ablauf

In `gebaeude.py` wird zunächst der Ordner gesucht:

```python
bilder_ordner = os.path.join(os.path.dirname(__file__), "bilder")
```

Danach wird für jeden Gebäudetyp der Dateiname gelesen:

```python
dateiname = typ_daten.get("bild")
if not dateiname:
    continue
```

Anschließend wird geprüft, ob die Datei existiert und mit Transparenz geladen:

```python
bild_pfad = os.path.join(bilder_ordner, dateiname)
if os.path.exists(bild_pfad):
    _bilder[typ_daten["name"]] = pygame.image.load(
        bild_pfad).convert_alpha()
```

Beim Zeichnen wird das Bild auf die Zielgröße skaliert:

```python
bild = _bilder.get(typ_daten["name"])
if bild is not None:
    bild = pygame.transform.smoothscale(bild, rect.size)
    _fenster.blit(bild, rect)
else:
    pygame.draw.rect(_fenster, typ_daten["farbe"], rect)
```

## Fehlerkontrolle

Wenn ein Bild nicht angezeigt wird, kontrolliert ihr zuerst den Ordnernamen `bilder`, danach Groß- und Kleinschreibung, Dateiendung und Schreibweise im Dictionary. Anschließend startet ihr das Spiel aus dem richtigen Projektordner neu. Der Selbsttest prüft die Bilddateien nicht, weil fehlende Bilder bewusst durch die Fallback-Farbe ersetzt werden.

## Erweiterungsaufgabe

Erstellt ein eigenes Bild für die Roboterfabrik, ergänzt in `gebaeude.py` den Wert `"bild": "roboterfabrik.png"` und überprüft im Spiel, ob das Bild auch dann korrekt angezeigt wird, wenn zwei kompakte Gebäude dieselbe Kachel teilen.

## Das Universitätsbild als 2×3-Gebäude

Das angehängte Bild `schule_2x3_kacheln_64x96.png` ist bereits passend vorbereitet: 64 Pixel breit und 96 Pixel hoch, also im Verhältnis 2:3. Bei einer Spielkachel von 48×48 Pixeln wird es automatisch auf ungefähr 96×144 Pixel skaliert. Es bedeckt deshalb zwei Kacheln nebeneinander und drei Kacheln untereinander.

In `gebaeude.py` stehen dafür die zusätzlichen Werte:

```python
{
    "name": "Universitaet",
    "bild": "schule_2x3_kacheln_64x96.png",
    "breite": 2,
    "hoehe": 3,
    "kuerzel": "L",
    "taste": "8",
}
```

Die angeklickte Kachel ist die **linke obere Ecke** des Gebäudes. Das Spiel reserviert anschließend automatisch alle sechs Kacheln in diesem Rechteck. Die Universität darf nicht gebaut werden, wenn eine dieser sechs Kacheln bereits belegt ist oder wenn das Rechteck über den Kartenrand hinausgeht.

Beim Rechtsklick genügt es, auf eine beliebige der sechs Universitätskacheln zu klicken. Das Spiel findet das zugehörige Gebäude über seine gesamte Fläche und gibt anschließend die Rückerstattung nur einmal zurück. Dadurch wird ein großes Gebäude nicht versehentlich sechsmal abgerissen.

Für eigene 2×3-Gebäude könnt ihr dieselbe Struktur wiederverwenden. Ändert nur Bilddatei, Name, Farbe und die Werte `breite` und `hoehe`. Für ein Gebäude mit drei Kacheln Breite und zwei Kacheln Höhe wären die Werte `"breite": 3` und `"hoehe": 2`.


# Aktualisierung: vollständige Bildpflicht und neue Gebäude

Diese Ergänzung ersetzt die ältere Tabelle, in der für Mine, Straße, Fusionsreaktor und Roboterfabrik noch `bild: None` stand. In der aktuellen Version besitzt jedes Gebäude einen konkreten PNG-Dateinamen.

## Aktuelle Dateinamen

| Gebäude | PNG-Datei | Größe |
|---|---|---:|
| Basis | `basis.png` | 64×64 |
| Reaktor | `reaktor.png` | 64×64 |
| Farm | `farm.png` | 64×64 |
| Holzfäller | `holzfaeller.png` | 64×64 |
| Steinmetz | `steinmetz.png` | 64×64 |
| Marktplatz | `marktplatz.png` | 64×64 |
| Wohnhaus | `wohnhaus.png` | 64×64 |
| Universität | `schule_2x3_kacheln_64x96.png` | 64×96 |
| Mine | `mine.png` | 64×64 |
| Straße | `strasse.png` | 64×64 |
| Fusionsreaktor | `fusionsreaktor.png` | 64×64 |
| Roboterfabrik | `roboterfabrik.png` | 64×64 |
| Stahlwerk | `stahlwerk.png` | 64×64 |
| Gewächshaus | `gewaechshaus.png` | 64×64 |
| Lagerhaus | `lagerhaus.png` | 64×64 |
| Wohnblock | `wohnblock.png` | 64×64 |
| Handelsposten | `handelsposten.png` | 64×64 |
| Koloniezentrum | `koloniezentrum.png` | 64×64 |

`labor.png` ist kein aktives Spielasset mehr. Die Universität ist das Bildungs- und Laborgebäude und verwendet das angehängte Schulbild.

## Eigenes Bild für ein neues 1×1-Gebäude

Erstellt eine quadratische PNG-Datei, zum Beispiel 64×64 Pixel. Zeichnet das Gebäude mittig und lasst einen kleinen transparenten Rand. Exportiert mit Alpha-Kanal, kopiert die Datei nach `bilder/` und tragt denselben Namen in `gebaeude.py` ein:

```python
{"name": "Luftreiniger", "bild": "luftreiniger.png",
 "farbe": (120, 220, 180), "kuerzel": "L",
 "taste": "", "breite": 1, "hoehe": 1},
```

Startet das Spiel vollständig neu, weil die Bilder in `gebaeude_initialisieren()` geladen werden. Danach führt ihr `python3 test_stunde11.py` aus. Der Test verlangt, dass jedes Gebäude einen vorhandenen Dateinamen besitzt.

## Eigenes Mehrkachelbild

Für ein Gebäude mit zwei Kacheln Breite und drei Kacheln Höhe verwendet ihr ein Seitenverhältnis von 2:3. Bei 48×48 Pixel pro Kachel ist 96×144 ein passendes Zielmaß; die Universität verwendet 64×96 und wird beim Zeichnen automatisch auf die Spielfläche skaliert.

```python
{"name": "Forschungszentrum", "bild": "forschungszentrum_2x3.png",
 "farbe": (150, 200, 255), "kuerzel": "Z",
 "taste": "", "breite": 2, "hoehe": 3},
```

`gebaeude_flaeche()` erzeugt daraus sechs Kachelkoordinaten. Die angeklickte Kachel ist die linke obere Ecke. Das Gebäude darf nur gebaut werden, wenn alle sechs Kacheln innerhalb der Karte und frei sind. Beim Rechtsklick auf irgendeine Teilkachel wird das ganze Gebäude entfernt.

## Typische Fehler

| Problem | Kontrolle |
|---|---|
| Bild fehlt | Ordner heißt genau `bilder`, Dateiname stimmt einschließlich Endung und Groß-/Kleinschreibung |
| Weißes Rechteck erscheint | Bild besitzt keinen Alpha-Kanal oder der Hintergrund wurde nicht entfernt |
| Bild erscheint zu klein | Das Gebäude ist als 1×1 eingetragen; für die Universität müssen `breite: 2` und `hoehe: 3` gesetzt sein |
| Altes Bild bleibt sichtbar | Spiel vollständig schließen und aus demselben Projektordner neu starten |
| Neues Gebäude ist im Menü, aber nicht baubar | Index in `GEBAEUDE_TYPEN`, `GEBAEUDE_WIRTSCHAFT`, Kategorie und Forschung prüfen |
| Verwaiste Datei | Jede Datei muss in `gebaeude.py` verwendet werden; `labor.png` nicht wieder hinzufügen |
