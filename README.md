# Terra_Nova

Terra_Nova ist ein Koloniespiel, inspiriert von Final Earth 2, entstanden im
Informatikunterricht. Baue auf einem fremden Planeten eine Kolonie: Wohnraum,
Energie, Nahrung, Forschung, Handel — und seit dem Fortgeschrittenen Kurs auch
Straßennetz, Sound und feindliche Angriffe.

Der Spielname wird zentral über `SPIELNAME` in `main.py` gesetzt: Fenstertitel
und Hauptmenü lesen den Namen von dort. Umbenennen heißt also, genau diese eine
Zeile zu ändern.

## Starten

    python main.py

Voraussetzungen: Python 3.10+, pygame 2.x. Ohne Audiogerät läuft das Spiel
ohne Ton weiter (alle Tonfunktionen sind try/except-gesichert).

## Steuerung (Auszug, vollständig mit Taste H im Spiel)

| Taste | Funktion |
|---|---|
| 1–9 | Baumenü-Kategorie (9 = Spezial / Verteidigung) |
| ←/→, Leertaste | Gebäude wählen und bauen |
| TAB / F / E | Baumenü, Forschung, Handel |
| +/− | Spielgeschwindigkeit |
| ESC | Pause (**S** = speichern, **I** = Missionen, **A** = Achievements) |
| Maus | Fenster an der Titelzeile ziehen; **–** minimiert, **X** blendet aus |
| S / C / I / L | Fenster: Verteidigung / Bauinfo / Übersicht / Layout zurücksetzen |
| L | Spielstand laden (im Hauptmenü) |
| R | Spielregeln wählen (im Hauptmenü) |

## Spielregeln (Hauptmenü → Spielregeln)

| Regel | Sieg | Niederlage | Gegner |
|---|---|---|---|
| Standard | 30 Bewohner + Koloniezentrum | 12 Ticks ohne Versorgung | an, Faktor 1.0 |
| Entspannt | 30 Bewohner + Koloniezentrum | keine | aus |
| Freies Spiel | keine | keine | aus |
| Überleben | 40 Bewohner + Koloniezentrum | 6 Ticks ohne Versorgung | an, Faktor 1.3 |

## Fortgeschrittener Kurs — die Phasen

| Phase | Thema | Zentrale Dateien |
|---|---|---|
| 0 | Ordner-Umzug und Ist-Analyse | alle |
| 1/2 | Sound und Musik | `ton.py`, `sounds_erzeugen.py`, `sounds/` |
| 3 | Straßennetz und Logistik | `logistik.py` |
| 4 | Gegner und Verteidigung | `gegner.py`, neue Gebäude 21–23 |
| 5 | Dokumentation und Abnahme | README, Handbücher, `check.py` |

Details für Schülerinnen und Schüler: **FORTGESCHRITTEN_SCHUELERHANDBUCH.md**.

## Verteidigung (Phase 4) — die Regeln in Kürze

- Ablauf: 150 Ticks Frieden → Warnung (25 Ticks, Sirene und rotes Panel) →
  Gefecht. Danach 100–160 Ticks Frieden, dann kommt die nächste Welle.
- Angriff = (6 + 4 × Welle + 0.3 × Gebäudeanzahl) × Regelwerk-Faktor.
- Verteidigung = 1 × Verteidiger + 6 × Raumschiff + 10 × arbeitender
  Laserturm; Technologie „Schutzschilde“ bringt +25 % auf alles.
- Abwehr bringt 40 + 20 × Welle Gold und 10 × Welle Forschung — kostet aber
  20 % der Verteidiger und Raumschiffe (Gefallene zählen als Bevölkerungs­verlust).
- Bei Niederlage geht genau 30 % von Gold, Energie, Holz, Stein, Nahrung,
  Kohle, Eisen und Stahl verloren. Bevölkerung, Forschung, Roboter,
  Zufriedenheit, Verteidiger und Raumschiffe sind davor geschützt; ein
  Angriff löst nie selbst ein Game Over aus.
- Der Einstieg: Forschung „Militärtraining“ → Kaserne (Typ 21). Höchstens
  30 % der Bevölkerung dürfen gleichzeitig Verteidiger sein.

## Schwebende Info-Fenster

Die vier Info-Fenster — **Übersicht** (Kamera, Personal), **Verteidigung**,
**Ziel** und **Bauinfo** — sind frei verschiebbar:

- an der **Titelzeile** mit der linken Maustaste ziehen,
- **–** minimiert auf die Titelzeile (Knopf wird zu **+**),
- **X** blendet das Fenster aus.

Tasten: **S** Verteidigung, **C** Bauinfo, **I** Übersicht, **O** Ziel,
**L** setzt die ganze Anordnung wieder auf die Standardpositionen zurück.
Ein Klick in ein Fenster wird nicht an die Karte weitergegeben — man baut
also nie versehentlich unter einem Fenster.

Die Ressourcenleiste berechnet Spaltenbreite und Schriftgröße selbst
(`hud.ressourcen_leiste_layout`), damit sich Werte wie „Bevoelkerung:
24/100“ nie mehr überlappen oder am Rand abgeschnitten werden.

## Selbsttesten

    python check.py                        # Konsistenz aller Listen und Dateien
    python test_spielname.py               # Spielname in Konstante und Fenstertitel
    python test_fortgeschritten_gegner.py  # Phase 4: Ablauf, Formeln, Beute
    python test_fortgeschritten_logistik.py
    python test_fortgeschritten_sound.py
    python test_stunde11.py … test_stunde18.py

Alle am Stück (PowerShell im Spielordner):

    Get-ChildItem -Filter 'test_*.py' | ForEach-Object { python $_.Name }

## Spielstände

Speichern: Pause öffnen und **S** drücken (oder Knopf „Speichern“).
Laden: im Hauptmenü **L**. Ergebnis ist die lesbare Datei `spielstand.json`.
Alte Spielstände bleiben ladbar: Neue Felder (`gegner`, `verteidiger`,
`raumschiffe`) bekommen beim Laden ihre Startwerte.

## Dateien neu erzeugen

    python bilder_erzeugen.py   # Platzhalter-PNGs für Gebäude 21–23
    python sounds_erzeugen.py   # Standard-Sounds und Hintergrundmusik

Die erzeugten Dateien liegen bei — die Skripte braucht man nur zum
Neuerzeugen oder zum eigenen Anpassen (Anleitungen: `BILDER_ANLEITUNG.md`).

## Repository

Der Quellcode liegt auf GitHub: <https://github.com/7miwork/Terra_Nova>
(privates Repository – Zugriff nur für eingeladene Personen.)

## Hinweis für die Pflege von main.py

`main.py` enthält historisch gemischte Zeilenenden (CRLF und LF). Beim
Editieren von mehrzeiligen Blöcken kann das dazu führen, dass die alte
Zeichenkette nicht gefunden wird. Hilft meistens: einzeiligen Anker verwenden
oder den Block über ein kleines Python-Skript mit `\\r?\\n`-Mustern ersetzen.
