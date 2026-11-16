# Changelog — Terra_Nova

Alle Änderungen am Projekt, sortiert nach Version (neueste zuerst).

Jeder Eintrag trägt ein **Datum** (Format: TT.MM.JJJJ), wann die Änderung vorgenommen wurde.

## [Unreleased] — 16.11.2026 — Schüler-Hausaufgaben eingearbeitet

### 📄 Schüler-Hausaufgaben aus `Hausaufgaben/Neue/` eingearbeitet (16.11.2026)

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 1 | 16.11.2026 | Straßenbilder von Schülern in `bilder/strasse/` kopiert (11 PNGs: gerade, Kurven, T-Kreuzungen, X-Kreuzung) | `bilder/strasse/` |
| 2 | 16.11.2026 | Straßenbilder werden dynamisch nach Nachbar-Verbindungen gewählt (Geraden ↔ Kurven ↔ T-Kreuzungen ↔ X-Kreuzung) | `gebaeude.py`, `logistik.py` |
| 3 | 16.11.2026 | Straßenbilder von Quadrat (Top-Down) in isometrische Raute konvertiert (128x64 px) für korrekte Iso-Ansicht | `bilder/strasse/` |
| 3 | 16.11.2026 | `bilder_erzeugen.py` und `sounds_erzeugen.py` nach `werkzeuge/` verschoben (Schüler: Tools gehören getrennt) | `werkzeuge/` |
| 4 | 16.11.2026 | Gebäude-Bilder nach `bilder/gebaeude/` verschoben (Schüler: Bilder nach Typ getrennt) | `bilder/gebaeude/` |
| 5 | 16.11.2026 | Sound-Dateien von `sounds/` nach `audio/` verschoben (Schüler: Töne getrennt von anderen Medien) | `audio/` |
| 6 | 16.11.2026 | `terra_nova_24_gebaeude_pngs/` nach `unnoetig/` verschoben (Schüler: doppelte Bilder) | `unnoetig/` |
| 7 | 16.11.2026 | Code-Kommentare als `#` ergänzt (gebaeude.py, ton.py, logistik.py, CHANGELOG.md, README.md) | alle |

### 📄 Neue Hausaufgabe — 10.11.2026

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 1 | 10.11.2026 | Neue Hausaufgabe "Projektstruktur aufräumen & Straßenbilder erstellen" erstellt | `Hausaufgaben/10112026.md` |
| 2 | 10.11.2026 | Ordner `bilder/strasse/` angelegt (leer, für Schüler-Straßenbilder) | `bilder/strasse/` |

### 🔴 Fehler behoben

| # | Datum | Fehler | Ursache | Fix | Datei |
|---|-------|--------|---------|-----|-------|
| 1 | 09.11.2026 | `S` öffnete Verteidigungspanel **und** scrollte Kamera gleichzeitig | `pygame.K_s` belegt für Kamera-Scroll **und** Verteidigungspanel-Toggle | `S` ist wieder nur Kamera-Scroll nach unten; Verteidigungspanel auf `V` gelegt | `main.py` |
| 2 | 09.11.2026 | Leertaste setzt Spielgeschwindigkeit auf 0/1 zurück (vorherige 2×/4× geht verloren) | Inline-Toggle überschrieb `spiel_geschwindigkeit` ohne `_geschwindigkeit_vor_pause` zu nutzen | Leertaste ruft nun `pause_umschalten()` auf, das die Geschwindigkeit vor der Pause merkt und wiederherstellt | `main.py` |
| 3 | 09.11.2026 | README sagt „Leertaste baut Gebäude“, Spiel pausiert stattdessen | Dokumentation nicht mit Code abgeglichen | README-Tabelle korrigiert: Leertaste = Pause/Start, Linksklick = Bauen | `README.md` |

### 🟡 Überflüssigkeiten entfernt — 09.11.2026

| # | Datum | Was | Wo | Datei |
|---|-------|-----|-----|-------|
| 4 | 09.11.2026 | 9 doppelte Funktionsdefinitionen entfernt (`kamera_zeichnen_y`, `karte_generieren`, `karte_zeichnen`, `_hintergrund_aus_sternen_aufbauen`, `sterne_generieren`, `_farbe_dunkler`, `_karte_2d_zeichnen`, `_kartenrand_links`, `items_generieren`) | `main.py` — 3415 → 2881 Zeilen | `main.py` |
| 5 | 09.11.2026 | `__pycache__/` Ordner gelöscht (Projektstamm, `unnoetig/`, `tests/`) | Repository | — |
| 6 | 09.11.2026 | Temporäre Debug-Skripte und Backups gelöscht (`_check_*.py`, `_remove_dupes*.py`, `*.backup_*`) | Projektstamm | — |

### 📄 Dokumentation — 09.11.2026

- `CHANGELOG.md` neu erstellt (diese Datei)
- `README.md`: Steuerungstabelle korrigiert (S = Kamera-Scroll, V = Verteidigung, Leertaste, Linksklick)
- `.clinerules`: Regel #7 — Tastenbelegung entzerrt (S für Kamera-Scroll, V für Verteidigung); Regel #9 — Changelog-Einträge benötigen Timestamp

### 🚀 Weitere Verbesserungen — 09.11.2026

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 7 | 09.11.2026 | Items werden beim Bauen auf derselben Kachel eingesammelt (entfernt + Ressource gutgeschrieben) statt einfach überdeckt | `main.py` |
| 8 | 09.11.2026 | Einstellungen: "Auf Standard zurücksetzen" + "Fertig (Esc)" zu einem Button "Zurücksetzen & Fertig" zusammengeführt, der nach dem Klick das Menü schließt | `einstellungen.py` |
| 9 | 09.11.2026 | Straße: Bild passt besser auf die Kachel (2D: fast volle Kachelbreite, Iso: flache Höhe statt Gebäude-Höhe) | `gebaeude.py` |

---

### 🔴 Fehler behoben

| # | Datum | Fehler | Ursache | Fix | Datei |
|---|-------|--------|---------|-----|-------|
| 1 | 09.11.2026 | `S` öffnete Verteidigungspanel **und** scrollte Kamera gleichzeitig | `pygame.K_s` belegt für Kamera-Scroll **und** Verteidigungspanel-Toggle | `S` ist wieder nur Kamera-Scroll nach unten; Verteidigungspanel auf `V` gelegt | `main.py` |
| 2 | 09.11.2026 | Leertaste setzt Spielgeschwindigkeit auf 0/1 zurück (vorherige 2×/4× geht verloren) | Inline-Toggle überschrieb `spiel_geschwindigkeit` ohne `_geschwindigkeit_vor_pause` zu nutzen | Leertaste ruft nun `pause_umschalten()` auf, das die Geschwindigkeit vor der Pause merkt und wiederherstellt | `main.py` |
| 3 | 09.11.2026 | README sagt „Leertaste baut Gebäude“, Spiel pausiert stattdessen | Dokumentation nicht mit Code abgeglichen | README-Tabelle korrigiert: Leertaste = Pause/Start, Linksklick = Bauen | `README.md` |

### 🟡 Überflüssigkeiten entfernt — 09.11.2026

| # | Datum | Was | Wo | Datei |
|---|-------|-----|-----|-------|
| 4 | 09.11.2026 | 9 doppelte Funktionsdefinitionen entfernt (`kamera_zeichnen_y`, `karte_generieren`, `karte_zeichnen`, `_hintergrund_aus_sternen_aufbauen`, `sterne_generieren`, `_farbe_dunkler`, `_karte_2d_zeichnen`, `_kartenrand_links`, `items_generieren`) | `main.py` — 3415 → 2881 Zeilen | `main.py` |
| 5 | 09.11.2026 | `__pycache__/` Ordner gelöscht (Projektstamm, `unnoetig/`, `tests/`) | Repository | — |
| 6 | 09.11.2026 | Temporäre Debug-Skripte und Backups gelöscht (`_check_*.py`, `_remove_dupes*.py`, `*.backup_*`) | Projektstamm | — |

### 📄 Dokumentation — 09.11.2026

- `CHANGELOG.md` neu erstellt (diese Datei)
- `README.md`: Steuerungstabelle korrigiert (S = Kamera-Scroll, V = Verteidigung, Leertaste, Linksklick)
- `.clinerules`: Regel #7 — Tastenbelegung entzerrt (S für Kamera-Scroll, V für Verteidigung); Regel #9 — Changelog-Einträge benötigen Timestamp

### 🚀 Weitere Verbesserungen — 09.11.2026

| # | Datum | Was | Datei |
|---|-------|-----|-------|
| 7 | 09.11.2026 | Items werden beim Bauen auf derselben Kachel eingesammelt (entfernt + Ressource gutgeschrieben) statt einfach überdeckt | `main.py` |
| 8 | 09.11.2026 | Einstellungen: "Auf Standard zurücksetzen" + "Fertig (Esc)" zu einem Button "Zurücksetzen & Fertig" zusammengeführt, der nach dem Klick das Menü schließt | `einstellungen.py` |
| 9 | 09.11.2026 | Straße: Bild passt besser auf die Kachel (2D: fast volle Kachelbreite, Iso: flache Höhe statt Gebäude-Höhe) | `gebaeude.py` |

---

## Legende

- `main.py` — Hauptspiel (Steuerung, Spielschleife, Pause/Tick-System)
- `README.md` — Projekt-Dokumentation und Steuerungsübersicht
- `.clinerules` — Konventionen für die Arbeit am Projekt

---