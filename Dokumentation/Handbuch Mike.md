# Handbuch Mike — Terra_Nova (Fortgeschrittener Kurs)

> **Stand:** Schritt 5 (Items / passive Gegenstände + Abbau)  
> **Projektordner:** `Terra_Nova/`  
> **Start:** `python main.py` (Python 3.10+, pygame 2.x)

---

## 1. Projektüberblick

Terra_Nova ist ein Koloniespiel im Stil von *Final Earth 2*: Auf einem fremden Planeten
baust du eine Kolonie auf — Wohnraum, Energie, Nahrung, Forschung, Handel, Verteidigung.
Seit dem Fortgeschrittenen Kurs kommen Straßennetz/Logistik, Sound, feindliche Angriffe
und eine isometrische (Iso) Ansicht dazu.

Der Spielname wird zentral über `SPIELNAME` in `main.py` gesetzt — Fenstertitel und
Hauptmenü lesen den Namen von dort.

### Ordnerstruktur

| Ort | Inhalt |
|---|---|
| `main.py` + Module | Spielcode — direkt hier starten mit `python main.py` |
| `bilder/`, `sounds/` | Grafiken und Töne, die das Spiel lädt |
| `tests/` | Selbsttests: `test_*.py` und `check.py` |
| `Dokumentation/` | Handbücher, PDFs (`PDF/`), Erklärbilder (`Erklaer Bilder/`) |
| `unnoetig/` | Ablage für Altlasten/Einmal-Skripte (nicht ins Repository) |

---

## 2. Steuerung

| Taste / Eingabe | Funktion |
|---|---|
| 1–9 | Baumenü-Kategorie wählen (9 = Spezial / Verteidigung) |
| ← / →, Leertaste | Gebäude in der Kategorie wählen und bauen |
| TAB | Baumenü (alle Gebäudetypen) |
| F | Forschungsmenü |
| E / T | Handelsmenü |
| + / − | Spielgeschwindigkeit |
| ESC | Pause (S = speichern, I = Missionen, A = Achievements) |
| L | Spielstand laden (im Hauptmenü) |
| R | Spielregeln wählen (im Hauptmenü) |
| V | Logistik-Ansicht ein-/ausblenden |
| S / C / I / O | Fenster: Verteidigung / Bauinfo / Übersicht / Ziel |
| L | Fenster-Layout zurücksetzen |
| Maus | Fenster an Titelzeile ziehen; – minimiert, X blendet aus |
| Linksklick | bauen / terraformen |
| Rechtsklick | Gebäude abreißen **oder** Items (Ressourcen) abbauen |

### Schwebende Info-Fenster
Die vier Fenster **Übersicht**, **Verteidigung**, **Ziel** und **Bauinfo** sind frei
verschiebbar (an Titelzeile ziehen, – minimiert, X blendet aus). Ein Klick in
ein Fenster wird nicht an die Karte weitergegeben.

---

## 3. Spielregeln (Hauptmenü → Spielregeln)

| Regel | Sieg | Niederlage | Gegner |
|---|---|---|---|
| Standard | 30 Bewohner + Koloniezentrum | 12 Ticks ohne Versorgung | an, Faktor 1.0 |
| Entspannt | 30 Bewohner + Koloniezentrum | keine | aus |
| Freies Spiel | keine | keine | aus |
| Überleben | 40 Bewohner + Koloniezentrum | 6 Ticks ohne Versorgung | an, Faktor 1.3 |

---

## 4. Gebäude (Auswahl)

Alle Gebäudetypen liegen in `gebaeude.GEBAEUDE_TYPEN`. Jedes hat ein Bild
(`bilder/`), eine Farbe, ein Kürzel, Masse (breite × höhe) und eine
Wirtschaftsdefinition in `ressourcen.GEBAEUDE_WIRTSCHAFT`.

Besondere Typen:
- **0 Basis** — nur 1× baubar, Zentrum der Kolonie
- **7 Universität** — 2×3 Kacheln (großes Gebäude)
- **9 Strasse** — Bestandteil des Straßennetzes
- **19 Park** — senkt den Nahrungsverbrauch (max. 30 %)
- **20 Solarreaktor** — produziert Energie ohne Kohle
- **22 Raumschiffwerft** — 2×2 Kacheln

---

## 5. Fortgeschrittener Kurs — Phasen

| Phase | Thema | Zentrale Dateien |
|---|---|---|
| 0 | Ordner-Umzug und Ist-Analyse | alle |
| 1/2 | Sound und Musik | `ton.py`, `sounds_erzeugen.py`, `sounds/` |
| 3 | Straßennetz und Logistik | `logistik.py` |
| 4 | Gegner und Verteidigung | `gegner.py`, Gebäude 21–23 |
| 5 | Dokumentation, Iso-Ansicht, Items | `iso.py`, `items.py`, `gebaeude.py`, `tests/` |

---

## 6. Welt und Bau-Feld

Die Spielwelt ist groß (wirkt endlos beim Scrollen), aber das **bebaubare Feld ist begrenzt**.

| Konstante | Wert | Bedeutung |
|---|---|---|
| `WELT_BREITE` | 200 | Die Welt ist groß — man kann überall hin scrollen |
| `WELT_HOEHE` | 150 | |
| `BAU_BREITE` | 60 | Nur hier darf gebaut und abgerissen werden |
| `BAU_HOEHE` | 40 | |
| `BAU_FELD_START_X/Y` | 70 / 55 | Obere linke Ecke des Bau-Felds (zentriert) |
| `BAU_FELD_ENDE_X/Y` | 130 / 95 | Untere rechte Ecke des Bau-Felds |

- Die Kamera kann über die **ganze Welt** schwenken (keine harte Kante).
- **Bauen und Abreißen** funktionieren nur innerhalb des Bau-Felds. Klicks außerhalb werden ignoriert.
- Items werden nur innerhalb des Bau-Felds generiert.
- Der Startbildschirm zeigt direkt auf die Mitte des Bau-Felds.

## 7. Isometrische Ansicht (Iso)

**Modul:** `iso.py` — Umrechnung Raster ↔ Rauten.

- Raute: 96 × 48 Pixel (Verhältnis 2:1).
- `raster_zu_welt(spalte, zeile)` → Welt-Pixel (obere Ecke der Raute)
- `welt_zu_raster(welt_x, welt_y)` → Kachel (mit `floor` für negative Werte)
- `kachel_unten_mitte(...)` — Ankerpunkt für Gebäude-Bilder
- `zeichen_reihenfolge(liste, fussabdruck_fn)` — sortiert hinten → vorne

**Ansicht-Schalter:** `ISO_ANSICHT = True` in `main.py`. Die Module `gebaeude`,
`logistik` und `items` übernehmen den Schalter über `ansicht_setzen(ISO_ANSICHT)`
(kein Kreis-Import).

**Bild-Rendering (`gebaeude.py`):**
- Bilder skalieren auf die Kachel (1×1 = 88×88 px, Multi-Kachel proportional).
- Verankerung: untere Mitte des Bildes am `fuss_x/fuss_y`-Punkt.
- Der weiße 2-px-Rahmen wurde entfernt; Quader-Platzhalter vergrößert.
- **Kartenrand:** Die Welt hat keine feste Kante mehr (sie wirkt endlos). An den
  Rück- und Linkskanten der Welt läuft eine dünne Kontur entlang, damit der
  Übergang zum Sternenhimmel sauber ist. Die Erdwand (3D-Effekt) entfällt an
  der Welt-Kante, da die Welt ja weitergeht.
---

## 8. Items (passive Gegenstände) — Schritt 5

**Modul:** `items.py` — Ressourcen und Deko auf der Karte.

### Item-Typen

| Index | Name | Größe | Ressource | Menge |
|---|---|---|---|---|
| 0 | Goldvorkommen | 1×1 | gold | 50 |
| 1 | Holzhaufen | 1×1 | holz | 30 |
| 2 | Steinhaufen | 1×1 | stein | 25 |
| 3 | Kristall | 1×1 | forschung | 10 |
| 4 | Grosser Fels | 2×2 | stein | 60 |

### Funktionen
- `ansicht_setzen(iso_an)` — Iso/2D-Schalter (von `main.py` aufgerufen)
- `item_initialisieren(fenster, kachel_groesse)` — Fenster merken, Bilder laden
- `item_flaeche(typ_index, kachel_x, kachel_y)` — alle belegten Kacheln (Fussabdruck)
- `item_am_punkt(kachel_x, kachel_y, liste_items)` — Item an einer Kachel finden
- `item_abbauen(item)` — Ressourcen-Dict, das beim Abbau gutgeschrieben wird
- `zeichnen(liste_items, kamera_x, kamera_y)` — Iso: sortiert hinten→vorne; 2D: einfache Rechtecke

### Verdrahtung in `main.py`
- `import items` (neben `import iso`)
- `liste_items = []` — globale Liste aller Items
- `items_generieren()` — verteilt ~14 Items auf freien Kacheln (vermeidet
  Gebäude-Fussabdrücke; der 2×2-Fels braucht 4 freie Kacheln)
- Aufruf in `neues_spiel_starten()`, `zustand_laden()`, `kolonie_wechseln()`
- Zeichnen im Render-Loop: nach `karte_zeichnen()`, vor `gebaeude.gebaeude_zeichnen()`
- Init in `spiel_starten()`: `items.item_initialisieren(...)` + `items.ansicht_setzen(ISO_ANSICHT)`

### Abbau (Ernten)
- **Rechtsklick** auf ein Item: Ressource wird gutgeschrieben, Item entfernt,
  HUD-Meldung + Sound. Items haben Vorrang vor Gebäude-Demolition.
- Items sind reine Optik/Passiv-Objekte (produzieren nichts automatisch).

### Bekannte Einschränkungen
- Items werden **nicht gespeichert** — beim Laden/Koloniewechsel neu verteilt.
- Items blockieren keinen Bauplatz (ein Gebäude kann auf einem Item-Tile gebaut
  werden — das Item wird dann vom Gebäude überdeckt).
- Items und Gebäude werden in getrennten Sortier-Pässen gemalt (kleiner
  visueller Artefakt bei Items direkt vor Gebäuden).

---

## 9. Verteidigung (Phase 4)

- Ablauf: 150 Ticks Frieden → Warnung (25 Ticks) → Gefecht → 100–160 Ticks Frieden
- Angriff = (6 + 4 × Welle + 0.3 × Gebäudeanzahl) × Regelwerk-Faktor
- Verteidigung = 1 × Verteidiger + 6 × Raumschiff + 10 × Laserturm
  („Schutzschilde“ +25 %)
- Bei Niederlage: 30 % Verlust von Gold, Energie, Holz, Stein, Nahrung, Kohle,
  Eisen, Stahl. Bevölkerung/Forschung/Roboter/Zufriedenheit/Verteidiger/
  Raumschiffe geschützt; kein Game Over durch Angriff.
- Einstieg: Forschung „Militärtraining“ → Kaserne (Typ 21). Max. 30 % der
  Bevölkerung dürfen Verteidiger sein.

---

## 9. Schwebende Info-Fenster

Vier Fenster — **Übersicht**, **Verteidigung**, **Ziel**, **Bauinfo** — frei
verschiebbar (an Titelzeile ziehen, – minimiert, X blendet aus).

Tasten: **S** Verteidigung, **C** Bauinfo, **I** Übersicht, **O** Ziel,
**L** Layout zurücksetzen. Klicks in Fenster werden nicht an die Karte
weitergegeben.

Die Ressourcenleiste berechnet Spaltenbreite und Schriftgröße selbst
(`hud.ressourcen_leiste_layout`).

---

## 10. Selbsttesten

```powershell
python tests/check.py                        # Konsistenz aller Listen und Dateien
python tests/test_spielname.py               # Spielname in Konstante und Fenstertitel
python tests/test_fortgeschritten_gegner.py  # Phase 4: Ablauf, Formeln, Beute
python tests/test_fortgeschritten_logistik.py
python tests/test_fortgeschritten_sound.py
python tests/test_iso.py                     # Iso-Umrechnung
python tests/test_items.py                   # Items: Fussabdruck, Ansicht, Abbau
python tests/test_stunde11.py … test_stunde18.py
```

Alle am Stück (PowerShell im Spielordner):
```powershell
Get-ChildItem 'tests' -Filter 'test_*.py' | ForEach-Object { python $_.FullName }
```

---

## 11. Spielstände

- Speichern: Pause öffnen und **S** (oder Knopf „Speichern“).
- Laden: im Hauptmenü **L**. Ergebnis ist die lesbare Datei `spielstand.json`.
- Alte Spielstände bleiben ladbar (neue Felder bekommen Startwerte).
- Items werden (noch) nicht gespeichert — sie werden beim Laden neu verteilt.

---

## 12. Dateien neu erzeugen

```powershell
python bilder_erzeugen.py   # Platzhalter-PNGs für Gebäude 21–23
python sounds_erzeugen.py   # Standard-Sounds und Hintergrundmusik
```

Anleitungen: `Dokumentation/BILDER_ANLEITUNG.md`.

---

## 13. Repository

Quellcode auf GitHub: <https://github.com/7miwork/Terra_Nova>
(privates Repository — Zugriff nur für eingeladene Personen.)

---

## 14. Hinweis für die Pflege von main.py

`main.py` enthält historisch gemischte Zeilenenden (CRLF und LF). Beim
Editieren von mehrzeiligen Blöcken kann das dazu führen, dass die alte
Zeichenkette nicht gefunden wird. Hilft meistens: einzeiligen Anker verwenden
oder den Block über ein kleines Python-Skript mit `\\r?\\n`-Mustern ersetzen.

---

## 15. Was noch zu tun ist (offene Punkte)

- [ ] Items in den Spielstand speichern (`spielstand.speichern` + `kolonien.FELDER`
      um `liste_items` erweitern), damit Abbau-Fortschritt erhalten bleibt.
- [ ] Items blockieren Bauplätze (Gebäude auf Item-Tiles verhindern oder Item
      entfernen beim Bauen).
- [ ] Gemeinsame Sortierung von Gebäuden + Items (ein `iso.zeichen_reihenfolge`-
      Durchlauf) für perfekte Überdeckung.
- [ ] Visuelles Feedback beim Abbau (Partikel/Animation, HP-basierter Abbau).
- [ ] Items als Ressourcenquelle in der Wirtschaft (z. B. Mine auf
      Goldvorkommen bauen, um Gold zu produzieren).
- [ ] Optional: Schritt 6 (weitere Features laut Schülerwünschen).