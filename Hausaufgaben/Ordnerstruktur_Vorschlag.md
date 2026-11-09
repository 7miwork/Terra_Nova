# Terra_Nova – Ordnerstruktur-Vorschlag (zum Sortieren und Diskutieren)

> **Hinweis:** Dies ist eine **Anregung** für euch als Schüler.  
> Die Struktur ist noch nicht vollständig und soll im Unterricht besprochen werden.  
> Ihr dürft Ordner hinzufügen, entfernen oder umbenennen – und dann entscheiden, welche Dateien wohin gehören.

---

## Vorschlag A: Nach Funktion sortiert (empfohlen)

```
Terra_Nova/
├── main.py                      # Spielstart + Hauptschleife
│
├── spiel/                       # Kernspiel-Logik
│   ├── gebaeude.py              # Gebäude & Strassen
│   ├── items.py                 # Items & Ressourcen
│   ├── ressourcen.py            # Wirtschaft
│   ├── logistik.py              # Strassennetz & Transport
│   ├── forschung.py             # Forschung
│   ├── gegner.py                # Gegner & Verteidigung
│   ├── planeten.py              # Planeten-Generierung
│   ├── spielstand.py            # Speichern & Laden
│   └── chunks.py                # Chunk-System
│
├── oberflaeche/                 # Alles, was der Spieler sieht
│   ├── hud.py                   # HUD / Anzeige
│   ├── menu.py                  # Menüs
│   ├── einstellungen.py         # Einstellungen
│   └── iso.py                   # Isometrische Ansicht
│
├── steuerung/                   # Eingaben & Audio
│   ├── ton.py                   # Sounds & Musik
│   └── (main.py bleibt hier, weil es die Tasten abfragt)
│
├── bilder/                      # Grafiken
│   ├── gebaeude/                # Gebäude-Bilder
│   ├── terrain/                 # Boden-Bilder (erde, gras, sand, stein)
│   ├── items/                   # Item-Icons
│   └── strasse/                 # Strassen-Bilder (zu erstellen von Schülern)
│
├── sounds/                      # Sound-Dateien
│
├── tests/                       # Automatisierte Tests
│   ├── check.py
│   └── test_*.py
│
├── Dokumentation/               # Handbücher & Protokolle
│   ├── Handbuch Mike.md
│   └── Protokolle/
│
├── Hausaufgaben/                # Hausaufgaben-Dateien
│
├── unnoetig/                    # Altlasten (zu prüfen: löschen oder behalten?)
│
├── CHANGELOG.md                 # Änderungen mit Datum
├── README.md                    # Projekt-Übersicht
└── .clinerules                  # Regeln für die Arbeit am Projekt
```

---

## Vorschlag B: Nach Dateityp sortiert (alternativ)

```
Terra_Nova/
├── code/                        # Alle Python-Dateien
│   ├── main.py
│   ├── gebaeude.py
│   ├── items.py
│   ├── hud.py
│   ├── ... (alle *.py hier rein)
│
├── assets/                      # Alle Medien-Dateien
│   ├── bilder/
│   │   ├── gebaeude/
│   │   ├── terrain/
│   │   ├── items/
│   │   └── strasse/
│   └── sounds/
│
├── daten/                       # Speicherstände, Konfiguration
│   ├── einstellungen.json
│   └── spielstaende/            # Ordner für gespeicherte Spiele
│
├── tests/
├── Dokumentation/
├── Hausaufgaben/
├── unnoetig/
│
├── CHANGELOG.md
├── README.md
└── .clinerules
```

---

## Fragen zur Diskussion im Unterricht

| Frage | Eure Meinung / Vorschlag |
|-------|--------------------------|
| Welcher Vorschlag (A oder B) gefällt euch besser? | |
| Soll `main.py` im Hauptordner bleiben oder in einen Unterordner? | |
| Sollte es einen separaten Ordner für Speicherstände geben? | |
| Soll `unnoetig/` gelöscht werden? | |
| Welche Dateien fehlen in dieser Struktur noch? | |

---

## Eure Aufgabe

1. Schaut euch beide Vorschläge an.
2. Entscheidet euch für einen – oder mischt beide.
3. Schreibt auf, welche Dateien in welchen Ordner gehören.
4. Nennen auch Ordner, die ihr zusätzlich schaffen würdet.

**Abgabe:** In eurer Hausaufgaben-Datei (`10112026.md`, Teil 1).
