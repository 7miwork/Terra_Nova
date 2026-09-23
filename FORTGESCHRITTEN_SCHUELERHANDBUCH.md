# Fortgeschrittener Kurs — Schülerhandbuch (Stunde 1)

Willkommen im Fortgeschrittenen Kurs! Du erweiterst das bestehende
Koloniespiel **Terra_Nova** um ein neues Gameplay-System — in dieser
Stunde: **Gegner und Verteidigung**. Das Handbuch erklärt, wie das Spiel
gebaut ist, was du in Phase 4 veränderst und wie du dich selbst testest.

## 1. Das Spiel in 60 Sekunden

- **Start:** `python main.py` — Hauptmenü, dann Regel wählen (Taste **R**).
- **Bauen:** Ziffern **1–9** wählen Kategorien, **←/→** wechseln das
  Gebäude, **Leertaste** baut. Kategorie **9** heißt „Spezial / Verteidigung“.
- **Tick-System:** Ein Wirtschaftstick dauert bei Geschwindigkeit 1 genau
  60 Frames (ca. 1 Sekunde). Jeden Tick laufen in `main.py` in fester
  Reihenfolge: `ressourcen.ressourcen_produzieren` → `handel.handel_tick` →
  `gegner.gegner_tick` → `spielstatus_pruefen` → `missionen.pruefen`.
- **Speichern:** Pause (**ESC**) und **S**; Laden im Hauptmenü mit **L**.
- **Selbsttests:** Nach jeder Änderung
  `python check.py` und `python test_fortgeschritten_gegner.py`.

## 2. Die Module und ihre Aufgaben

| Datei | Aufgabe |
|---|---|
| `main.py` | Spielschleife, Menüs, Regelwerke, Tick-Reihenfolge |
| `gebaeude.py` | Gebäudetypen, Kategorien, Bilder, Baupläne |
| `ressourcen.py` | Wirtschaft, Speicher, Personal, Zufriedenheit |
| `forschung.py` | Technologien und Freischaltungen |
| `gegner.py` | **NEU:** Angriffs-Automat, Stärke, Beute, Panel, Banner |
| `ton.py` | Alle Sounds und die Musik (ohne Gerät: stiller No-Op) |
| `logistik.py` | Straßennetz und Anbindung (Phase 3) |
| `achievements.py` / `missionen.py` | Zähler, Ziele, Belohnungen |
| `spielstand.py` | Speichern/Laden als lesbares JSON |

Faustregel für **jede** Erweiterung — vier Stellen prüfen:

1. **Daten:** neuer Eintrag in `gebaeude.py`/`ressourcen.py` an *derselben* Indexposition
2. **Freischaltung:** Eintrag in `forschung.py`
3. **Darstellung:** PNG in `bilder/` + `ton.SOUNDS`-Eintrag falls Ton
4. **Test:** eigene Assert-Zeile in einem `test_*.py`

Typ-Indizes werden **nie umsortiert** — Spielstände speichern die Nummern.
Neue Gebäude kommen immer **hinten** an die Listen.

## 3. Kapitel Phase 4: Wie der Gegner tickt

Alles steckt in `gegner.py`. Pro Wirtschafttick ruft `main.py` auf:

    gegner.gegner_tick(ressourcen_dict, liste_gebaeude, aktives_regelwerk())

Der Rückgabewert ist `None` oder ein Ereignis-Dict
(`warnung`, `abwehr_erfolg`, `ausgeraubt`); `main.gegner_ereignis_verarbeiten`
zeigt dann nur noch Texte an und zählt Achievements. **Spiellogik steht nie
in der Zeichenschleife** — das Panel und das Banner zeichnen nur den
gespeicherten Zustand.

### Der Zustandsautomat

    FRIEDEN ──(Countdown 0)──▶ WARNUNG ──(25 Ticks)──▶ GEFECHT ──▶ FRIEDEN ...
       │                            │                      │
       │                            │                      ├─ Verteidigung ≥ Angriff:
       │                            │                      │   Belohnung, Statistik "abgewehrt"
       │                            │                      └─ sonst: 30 % Beute, "verloren"
       └─ ohne Basis (Typ 0) läuft gar nichts ──────────────┘

Konstanten zum Nachschlagen (oben in `gegner.py`):

| Konstante | Wert | Bedeutung |
|---|---|---|
| `FRIEDENSZEIT_TICKS` | 150 | erster Angriff erst nach 150 Ticks |
| `ANGRIFFS_INTERVALL` | (100, 160) | danach zufällig im Fenster |
| `WARNZEIT_TICKS` | 25 | Reaktionszeit nach der Sirene |
| `BANNER_TICKS` | 6 | Anzeigedauer des Ergebnis-Banners |
| `PLUENDERUNG_ANTEIL` | 0.30 | Beuteanteil der acht Rohstoffe |
| `VERLUST_ANTEIL` | 0.20 | gefallene Verteidiger/Schiffe je Gefecht |

### Die beiden Formeln

    Angriff    = (6 + 4 × Welle + 0.3 × Anzahl Gebäude) × Faktor
    Verteidigung = 1 × Verteidiger + 6 × Raumschiffe
                     + 10 × arbeitende Lasertürme   (Schutzschilde: ×1,25)

„Arbeitend“ heißt: kein `stillstand_grund` (Logistik!) und `arbeitet` nicht
auf `False` gesetzt (Energie/Personal). Ein Turm ohne Strom verteidigt also
nicht — das ist die bewusste Verbindung zu Phase 3.

### Dein Verteidigungsweg (Reihenfolge für den Spieler)

1. Forschung **Militärtraining** → bau die **Kaserne** (0.5 Verteidiger/Tick,
   stoppt beim Kontingent 30 % der Bevölkerung, verbraucht aber weiter).
2. Forschung **Laserverteidigung** → **Lasertürme** an die Straße mit Strom.
3. Forschung **Raumschiffbau** (+ Stahlverarbeitung) → **Raumschiffwerft**.
4. Forschung **Schutzschilde** → +25 % auf die gesamte Verteidigung.

Belohnung der Abwehr steigt mit der Welle: Welle 3 = 100 Gold + 30 Forschung.

### Regelwerke

Die vier Einträge in `main.REGELWERKE` tragen zwei zusätzliche Felder:

    "gegner_aktiv":  True/False     # greifen überhaupt Gegner an?
    "gegner_faktor": 1.0 / 1.3      # multipliziert die Angriffsstärke

Ohne `gegner_aktiv` friert der Countdown ein und das Panel verschwindet
komplett — der Spielmodus „Entspannt“ bleibt friedlich.

### Spielstände

`gegner.zustand_exportieren()` liefert Status, Restticks, Welle, Statistik
und Banner als JSON-Dictionary; `spielstand.py` speichert es unter
`"gegner"`. Fehlt das Feld (alter Spielstand), setzt
`zustand_importieren({})` alles auf Startwerte zurück. Kaputte Werte
(`"rest_ticks": "x"` usurpierte Strings) landen ebenfalls sicher auf den
Startwerten — ein defekter Spielstand kann das Spiel nicht abstürzen.

Der Zufall steckt in einer **eigenen** `random.Random`-Instanz.
`gegner.seed_setzen(7)` macht jeden Ablauf exakt reproduzierbar — so
schreibst du Tests, die morgen noch grün sind.

## 4. Checkliste: Ich baue eine eigene Erweiterung

### Neues Gebäude (z. B. „Luftfilter“)

1. `gebaeude.py`: Eintrag **anhängen** (nie umsortieren!), Name, Größe, Bild.
2. `ressourcen.py`: `GEBAEUDE_WIRTSCHAFT`-Eintrag **auf derselben Position**
   plus `GEBAEUDE_ZUFRIEDENHEIT`-Eintrag.
3. `forschung.py`: Freischaltung als Technologie, `voraussetzung` vermerken.
4. `bilder/`: PNG ablegen (Formate siehe `BILDER_ANLEITUNG.md`).
5. `gebaeude.py`: passende Kategorie ergänzen (9 = Spezial / Verteidigung).
6. `check.py` erweitern, Tests laufen lassen.

### Neue Technologie

- Dictionary in `forschung.TECHNOLOGIEN` anhängen; `voraussetzung` (String)
  oder `voraussetzungen` (Liste) funktionieren beide.
- Bonus in `ressourcen.py` bzw. `gegner.py` per
  `forschung.ist_technologie_erforscht("id")` abfragen.

### Neues Achievement

1. Eintrag in `achievements.ACHIEVEMENTS` (max. 39 Platz = 3 × 13 im Menü).
2. **Zeile im `bedingungen`-Dict von `pruefen()`** — sonst wird es nie erreicht.
3. Zähler vorhanden? Forthole ihn über `_kontext` (aktuelle Werte) oder eine
   kleine Funktion wie `angriff_abgewehrt()` (Ereigniszähler).

### Neue Mission

- Dictionary in `missionen.MISSIONEN` (max. 24 Platz = 3 × 8).
- `bedingungen` als Liste von `(zaehler, ziel)`; `gebaeude_typ_N` zählt
  `main.missionen_kontext()` automatisch mit.

## 5. Die vier Fehler, die in dieser Phase wirklich auftraten

1. `UnboundLocalError: _banner` — Modulvariable schreiben braucht `global`,
   auch wenn nur unter Bedingung geschrieben wird.
2. Achievement „nicht erreicht“ trotz Zähler — die vergessene Zeile im
   `bedingungen`-Dict von `achievements.pruefen()`.
3. „Text not found“ beim Editieren von `main.py` — gemischte Zeilenenden
   (CRLF/LF). Einzeiliger Anker oder Patchskript mit `\\r?\\n` nutzen.
4. Test-Assert auf „0.05 Verteidiger pro Tick“ — der echte Wert steht in
   `ressourcen.GEBAEUDE_WIRTSCHAFT[21]` und lautet **0.5**.

Weitere typische Stellen: `setdefault` für neue Ressourcen beim Laden alter
Spielstände (`main.spielstand_laden`) und `.get(..., 0)` in jeder Auswertung
neuer Ressourcenschlüssel.

## 6. Abnahme — woran du erkennst, dass alles läuft

    python check.py                        # CHECK_OK am Ende
    python test_fortgeschritten_gegner.py  # "Alle Gegner-Tests bestanden."
    Get-ChildItem -Filter 'test_*.py | ... # alle PASS
    python main.py                         # manuell: Sirene hören, Banner sehen

Der 300-Frame-Lauf ohne Fenster (Headless) prüft zusätzlich, dass über ein
volles Gefecht hinweg kein Fehler auftritt und die Plünderung **keinen**
Niederlage-Status auslöst.

**Ideensammlung für die nächste Stunde** (eintragen in `Ideen und Fehler.md`):
Welche Gegner-Arten würdest du bauen? Welche Formel brauchen sie? Und welcher
Testfall beweist, dass deine Regel stimmt?


