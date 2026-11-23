# Protokoll — 23.11.2026

**Kurs:** Fortgeschrittener Kurs
**Projekt:** Terra_Nova

## Zusammenfassung

Das Projekt wurde nach der Zielstruktur aufgeräumt. Die Spielmodule liegen
nun in `spielmodule/`, JSON-Dateien in `saves/`, Grafiken in den bestehenden
Unterordnern von `bilder/` und die Töne in `audio/`.

## Durchgeführte Arbeiten

- Branch `ordnung-23112026` erstellt und Ausgangsstand als Commit gesichert.
- 22 Python-Module mit `git mv` nach `spielmodule/` verschoben.
- Zentrale Pfade in `spielmodule/pfade.py` ergänzt.
- `main.py`, Tests und Werkzeuge für die flachen Importe und Projektpfade
  angepasst.
- `einstellungen.json` und `statistik.json` nach `saves/` verschoben.
- Temporäre Dateien, Test-Hilfedatei und `__pycache__/` entfernt.
- Ordner-READMEs, README, `.clinerules`, `.gitignore`, Handbuch,
  CHANGELOG und Hausaufgabe aktualisiert.
- Zwei bekannte veraltete Tests auf die aktuelle `V`-Taste und die tatsächlichen
  Planeten-/Weltwerte aktualisiert.
- Die isometrische Bodendarstellung wurde geglättet: Nachbarkacheln
  überlappen minimal und Gitterlinien sind standardmäßig aus.
- Die Hausaufgabe `17112026.md` wurde um eine ideale Musterlösung und
  Hinweise auf die zentralen Code-Stellen ergänzt.
- `spielmodule/pfade.py` legt `saves/` bei Bedarf automatisch an.
- Alle relevanten Projektpfade liegen zentral in `spielmodule/pfade.py`;
  die Tests kennen zusätzlich den Projektstamm und `spielmodule/` für Importe.
- Die Bodentextur- und Kartenzeichnung wurde nach `spielmodule/boden.py`
  ausgelagert. 2D und Iso zeichnen Übergänge, geschlossene Kanten und
  verwenden eine gemeinsame Iso-Überlappung.
- Gebäude erhalten in der Iso-Ansicht dezente transparente Fußbodenschatten.
- Punkt 5 wurde abgeschlossen: Die Bodentextur- und Kartendarstellung liegt
  vollständig in `spielmodule/boden.py`; `main.py` ruft dieses Modul auf.

## Fehler und Lösung

- Vor dem Umbau fehlten Bildpfade in mehreren Tests, weil Grafiken bereits in
  Unterordnern lagen. Die Tests wurden auf `spielmodule/pfade.py` umgestellt.
- Das Panelskript erwartete S statt der tatsächlich implementierten Taste V.
  Der Test wurde auf V aktualisiert.
- Der Planetentest verwendete alte Kartenwerte und alte
  `KARTE_BREITE/KARTE_HOEHE`-Namen. Der Test wurde auf die aktuellen
  Planetendaten und `WELT_BREITE/WELT_HOEHE` angepasst.

## Validierung

- Ausgangsbasis: 59 Python-Dateien erfolgreich kompiliert.
- Nach dem Umbau: alle Python-Dateien erfolgreich kompiliert.
- `python tests/check.py`: `CHECK_OK`.
- Einzeltests nach Umbau: alle bekannten Baseline-Fehler wurden geprüft;
  keine neuen Umzugfehler offen.
- Pygame-Dummy-Smoke-Test: `python main.py` blieb laufend aktiv, ohne
  Startfehler oder fehlende Python-Importe.
- Es wurden keine neuen JSON-Dateien im Projektstamm erzeugt; bestehende
  Einstellungen und Statistik liegen unter `saves/`.

## Geänderte Dateien

Siehe Git-Status und CHANGELOG.

## Offene Punkte

- Die manuelle Bedienprüfung mit Hauptmenü, neuer Partie, Bauen, Pause,
  Speichern/Laden und Einstellungen konnte wegen ausgeschalteter
  Computer-Use-Freigabe nicht per Maus durchgeführt werden. Der Nutzer kann
  diese Prüfung mit `/computer on` durchführen.
