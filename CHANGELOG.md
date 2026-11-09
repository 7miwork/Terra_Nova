# Changelog — Terra_Nova

Alle Änderungen am Projekt, sortiert nach Version (neueste zuerst).

## [Unreleased] — Fehlerbehebungen (Schüler-QA)

### 🔴 Fehler behoben

| # | Fehler | Ursache | Fix | Datei |
|---|--------|---------|-----|-------|
| 1 | `S` öffnet Verteidigungspanel **und** scrollt Kamera gleichzeitig | `pygame.K_s` belegt für Kamera-Scroll (gedrückt halten) **und** Verteidigungspanel-Toggle | `S` aus Kamera-Scroll entfernt; Kamera nach unten nur noch per Maus-Rand-Scrolling | `main.py` |
| 2 | Leertaste setzt Spielgeschwindigkeit auf 0/1 zurück (vorherige 2×/4× geht verloren) | Inline-Toggle überschrieb `spiel_geschwindigkeit` ohne `_geschwindigkeit_vor_pause` zu nutzen | Leertaste ruft nun `pause_umschalten()` auf, das die Geschwindigkeit vor der Pause merkt und wiederherstellt | `main.py` |
| 3 | README sagt „Leertaste baut Gebäude“, Spiel pausiert stattdessen | Dokumentation nicht mit Code abgeglichen | README-Tabelle korrigiert: Leertaste = Pause/Start, Linksklick = Bauen | `README.md` |

### 🟡 Überflüssigkeiten entfernt

| # | Was | Wo | Datei |
|---|-----|-----|-------|
| 4 | 9 doppelte Funktionsdefinitionen entfernt (`kamera_zeichnen_y`, `karte_generieren`, `karte_zeichnen`, `_hintergrund_aus_sternen_aufbauen`, `sterne_generieren`, `_farbe_dunkler`, `_karte_2d_zeichnen`, `_kartenrand_links`, `items_generieren`) | `main.py` — 3415 → 2881 Zeilen | `main.py` |
| 5 | `__pycache__/` Ordner gelöscht (Projektstamm, `unnoetig/`, `tests/`) | Repository | — |
| 6 | Temporäre Debug-Skripte und Backups gelöscht (`_check_*.py`, `_remove_dupes*.py`, `*.backup_*`) | Projektstamm | — |

### 📄 Dokumentation

- `CHANGELOG.md` neu erstellt (diese Datei)
- `README.md`: Steuerungstabelle korrigiert (Leertaste, Linksklick)
- `.clinerules`: Regel #7 ergänzt — keine Tasten-Doppelbelegung vor Einführung neuer Tasten prüfen

---

## Legende

- `main.py` — Hauptspiel (Steuerung, Spielschleife, Pause/Tick-System)
- `README.md` — Projekt-Dokumentation und Steuerungsübersicht
- `.clinerules` — Konventionen für die Arbeit am Projekt

---