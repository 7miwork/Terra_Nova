# Changelog — Terra_Nova

Alle Änderungen sind nach Datum geordnet.

## 23.11.2026 — Projektstruktur aufgeräumt

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 1 | 23.11.2026 | Die 22 Spielmodule nach `spielmodule/` verschoben und flache Importe über `sys.path` verdrahtet | `main.py`, `spielmodule/*.py`, `tests/*.py` |
| 2 | 23.11.2026 | Zentrale Projektpfade in `pfade.py` ergänzt | `spielmodule/pfade.py` |
| 3 | 23.11.2026 | JSON-Dateien nach `saves/` verschoben und `.gitignore` angepasst | `saves/*.json`, `.gitignore` |
| 4 | 23.11.2026 | Gebäude-, Straßen-, Terrain- und Item-Pfade sowie Audio-Pfade zentralisiert | `spielmodule/gebaeude.py`, `spielmodule/items.py`, `spielmodule/ton.py`, `main.py` |
| 5 | 23.11.2026 | Werkzeug-Skripte auf Bilder und Audio umgestellt | `werkzeuge/bilder_erzeugen.py`, `werkzeuge/sounds_erzeugen.py` |
| 6 | 23.11.2026 | Temporäre Dateien und `__pycache__/` entfernt | mehrere Dateien |
| 7 | 23.11.2026 | Veraltete Tests für Verteidigungstaste, Kartenwerte und alte Kartengrößen aktualisiert | `tests/test_fortgeschritten_panels.py`, `tests/test_planeten_kolonien.py` |
| 8 | 23.11.2026 | README, Cline-Regeln, Handbuch, Hausaufgabe und Ordner-READMEs aktualisiert | `.clinerules`, `README.md`, `Dokumentation/Handbuch Mike.md`, `Hausaufgaben/17112026.md` |
| 9 | 23.11.2026 | Isometrische Bodenrauten bekommen minimale Überlappung und Gitterlinien sind standardmäßig aus | `main.py`, `spielmodule/einstellungen.py`, `saves/einstellungen.json` |
| 10 | 23.11.2026 | Hausaufgabe um ideale Lösung und hilfreiche Code-Hinweise ergänzt | `Hausaufgaben/17112026.md`, `main.py`, `spielmodule/*.py`, `werkzeuge/*.py` |
| 11 | 23.11.2026 | Zentrales Saves-Verzeichnis wird automatisch angelegt und Tests erhalten Pfadkommentare | `spielmodule/pfade.py`, `tests/*.py` |
| 12 | 23.11.2026 | Veraltete Pfadzusammenstellungen entfernt und zentrale Pfad-/Import-Hinweise in den Code übernommen | `main.py`, `spielmodule/*.py`, `werkzeuge/*.py`, `tests/*.py` |
| 13 | 23.11.2026 | Bodentexturen und Kartenzeichnung in `spielmodule/boden.py` ausgelagert | `main.py`, `spielmodule/boden.py`, `tests/test_boden.py` |
| 14 | 23.11.2026 | Sanfte Bodentypübergänge, geschlossene Kartenkante und dezente Gebäude-Schatten ergänzt | `spielmodule/boden.py`, `spielmodule/gebaeude.py` |
| 15 | 23.11.2026 | Punkt 5 vollständig verdrahtet: Karten-/Terrainzeichnen aus `main.py` in `spielmodule/boden.py` ausgelagert | `main.py`, `spielmodule/boden.py`, `tests/test_boden.py` |
| 16 | 24.11.2026 | Würfel-Seiten aus Terrain-PNGs bei der Iso-Darstellung entfernt und Bodentexturen als echte Rautenmasken gerendert | `spielmodule/boden.py`, `tests/test_boden.py` |
| 17 | 24.11.2026 | Einstellungs-Knopf in getrennte Befehle `Zurücksetzen` und `Fertig` aufgeteilt | `spielmodule/einstellungen.py`, `tests/test_einstellungen.py` |
| 18 | 24.11.2026 | Neue Optimierungs-Hausaufgabe mit Leistung, Grafik und Verbesserungsplan erstellt | `Hausaufgaben/24112026.md` |

## 17.11.2026 — Musik und große Gebäudedarstellung

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 1 | 17.11.2026 | Hintergrundmusik und Sound-Funktionen erweitert | `spielmodule/ton.py` |
| 2 | 17.11.2026 | Darstellung großer Gebäude getestet | `tests/test_grosse_gebaeude_darstellung.py` |
| 3 | 17.11.2026 | Große Gebäudedarstellung in der Lade- und Zeichenlogik verbessert | `spielmodule/gebaeude.py` |

## 16.11.2026 — Schüler-Arbeiten eingearbeitet

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 1 | 16.11.2026 | Straßenbilder von Schülern in `bilder/strasse/` zusammengeführt | `bilder/strasse/` |
| 2 | 16.11.2026 | Straßenbilder werden nach Nachbar-Verbindungen gewählt | `spielmodule/gebaeude.py`, `spielmodule/logistik.py` |
| 3 | 16.11.2026 | Werkzeugskripte nach `werkzeuge/` verschoben | `werkzeuge/bilder_erzeugen.py`, `werkzeuge/sounds_erzeugen.py` |
| 4 | 16.11.2026 | Gebäude-Bilder nach `bilder/gebaeude/` verschoben | `bilder/gebaeude/` |
| 5 | 16.11.2026 | Sound-Dateien nach `audio/` verschoben | `audio/` |
| 6 | 16.11.2026 | Doppelte Gebäude-Bilder nach `unnoetig/` verschoben | `unnoetig/` |

## 10.11.2026 — Neue Hausaufgabe

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 1 | 10.11.2026 | Hausaufgabe zur Projektstruktur angelegt | `Hausaufgaben/10112026.md` |
| 2 | 10.11.2026 | Leeren Ordner `bilder/strasse/` angelegt | `bilder/strasse/` |

## 09.11.2026 — Tasten, Pause und Codebereinigung

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 1 | 09.11.2026 | S-Konflikt aufgelöst: S scrollt nur nach unten | `main.py` |
| 2 | 09.11.2026 | Verteidigungspanel auf Taste V gelegt | `main.py` |
| 3 | 09.11.2026 | Leertaste merkt und stellt die Geschwindigkeit vor der Pause wieder her | `main.py` |
| 4 | 09.11.2026 | README-Tabelle an die tatsächliche Steuerung angeglichen | `README.md` |
| 5 | 09.11.2026 | Neun doppelte Funktionsdefinitionen entfernt | `main.py` |
| 6 | 09.11.2026 | `__pycache__/` und temporäre Debug-Skripte entfernt | Projektstamm, `tests/`, `unnoetig/` |
| 7 | 09.11.2026 | Items werden beim Bauen eingesammelt | `main.py` |
| 8 | 09.11.2026 | Einstellungs-Buttons zusammengeführt | `spielmodule/einstellungen.py` |
| 9 | 09.11.2026 | Straßenbildgröße in Iso- und 2D-Ansicht verbessert | `spielmodule/gebaeude.py` |
