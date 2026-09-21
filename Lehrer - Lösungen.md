# Lehrer — Lösungen zu den 10 Fehlern (Stunde 7)

Diese Datei ist **nur für die Lehrkraft** gedacht.
Sie enthält alle 10 Fehler mit genauer Beschreibung und der korrekten Lösung.

---

## Fehler 1 — `gebaeude.py` — Wohnhaus-Farbe

**Datei:** `gebaeude.py`  
**Funktion/Stelle:** `GEBAEUDE_TYPEN` — Eintrag Index 6 (Wohnhaus)  
**Zeile (ca.):** Zeile mit `"farbe":`

**Fehler:**
```python
"farbe":   (180, 180, 200),   # Fast Violett — Wohnungen für die Leute
```

**Richtig:**
```python
"farbe":   (180, 120, 200),   # Violett — Wohnungen für die Leute
```

**Warum ist das didaktisch sinnvoll?**  
Schüler müssen die Farbe im Code mit der Beschreibung abgleichen. Der Kommentar sagt "Violett", der Code enthält aber einen geänderten RGB-Wert. Das fördert die Aufmerksamkeit für konsistente Dokumentation.

---

## Fehler 2 — `gebaeude.py` — Wohnhaus-Kürzel

**Datei:** `gebaeude.py`  
**Funktion/Stelle:** `GEBAEUDE_TYPEN` — Eintrag Index 6 (Wohnhaus)  
**Zeile (ca.):** Zeile mit `"kuerzel":`

**Fehler:**
```python
"kuerzel": "V",
```

**Richtig:**
```python
"kuerzel": "W",
```

**Warum ist das didaktisch sinnvoll?**  
Das Kürzel "W" für Wohnhaus ist naheliegend, steht aber nicht im Code. Schüler müssen das HUD und die Tastenbelegung prüfen, um zu sehen, dass Taste 7 ein "W" anzeigen sollte.

---

## Fehler 3 — `ressourcen.py` — Wohnhaus-Produktionsmenge

**Datei:** `ressourcen.py`  
**Funktion/Stelle:** `GEBAEUDE_WIRTSCHAFT` — Eintrag Index 6 (Wohnhaus)  
**Zeile (ca.):** Zeile mit `"produktion":`

**Fehler:**
```python
"produktion": {"bevoelkerung": 1},   # Produziert Bevölkerung
```

**Richtig:**
```python
"produktion": {"bevoelkerung": 2},   # Produziert Bevölkerung
```

**Warum ist das didaktisch sinnvoll?**  
Schüler sehen, dass ein Wohnhaus nur +1 Bevölkerung gibt statt +2. Sie müssen den Wert mit der Dokumentation in README.md und main.py abgleichen und verstehen, dass Produktionswerte in der Wirtschafts-Tabelle gespeichert sind.

---

## Fehler 4 — `main.py` — Bevölkerungs-Startwert

**Datei:** `main.py`  
**Funktion/Stelle:** Initialisierung von `ressourcen_dict`  
**Zeile (ca.):** Die Zeile mit `"bevoelkerung":`

**Fehler:**
```python
ressourcen_dict = {"gold": 100, "energie": 50, "holz": 30, "stein": 20, "bevoelkerung": 5}
```

**Richtig:**
```python
ressourcen_dict = {"gold": 100, "energie": 50, "holz": 30, "stein": 20, "bevoelkerung": 0}
```

**Warum ist das didaktisch sinnvoll?**  
Der Startwert 5 ist inkonsistent zur Kommentierung ("Startwert = 0"). Schüler müssen prüfen, woher der erste Wert im Spiel kommt und ob er mit der Dokumentation übereinstimmt.

---

## Fehler 5 — `hud.py` — Bevölkerung-Icon-Position

**Datei:** `hud.py`  
**Funktion/Stelle:** `_ressourcen_leiste_zeichnen()` — Ressourcen-Typen  
**Zeile (ca.):** `"icon_pos"` bei Bevölkerung

**Fehler:**
```python
"icon_pos": (500, 15),
```

**Richtig:**
```python
"icon_pos": (480, 15),
```

**Warum ist das didaktisch sinnvoll?**  
Das Icon ist um 20 Pixel zu weit rechts. Schüler sehen visuell, dass das Bevölkerungs-Icon überlappt oder zu weit außen liegt. Sie müssen die Position im Code anpassen, bis die Anzeige sauber aussieht.

---

## Fehler 6 — `hud.py` — Bevölkerung-Text-Position

**Datei:** `hud.py`  
**Funktion/Stelle:** `_ressourcen_leiste_zeichnen()` — Ressourcen-Typen  
**Zeile (ca.):** `"text_pos"` bei Bevölkerung

**Fehler:**
```python
"text_pos": (515, 12),
```

**Richtig:**
```python
"text_pos": (495, 12),
```

**Warum ist das didaktisch sinnvoll?**  
Der Text beginnt zu weit rechts — neben dem Icon soll nicht der Text stehen. Schüler müssen bemerken, dass Icon-Position und Text-Position zusammengehören und beim Anpassen des Icons auch den Text anpassen müssen.

---

## Fehler 7 — `hud.py` — Dictionary-Key mit Leerzeichen

**Datei:** `hud.py`  
**Funktion/Stelle:** `_ressourcen_leiste_zeichnen()` — Ressourcen-Typen  
**Zeile (ca.):** `"schluessel"` bei Bevölkerung

**Fehler:**
```python
"schluessel": "bevoelkerung ",
```

**Richtig:**
```python
"schluessel": "bevoelkerung",
```

**Warum ist das didaktisch sinnvoll?**  
Das Leerzeichen am Ende führt dazu, dass `ressourcen.get("bevoelkerung ", 0)` immer 0 zurückgibt — im echten Ressourcen-Dictionary steht der Key aber ohne Leerzeichen. Schüler müssen den Tippfehler finden und verstehen, dass Dictionary-Keys **exakt** stimmen müssen.

---

## Fehler 8 — `main.py` — Falscher Index-Bereich im Kommentar

**Datei:** `main.py`  
**Funktion/Stelle:** Definition von `gebaeude_auswahl`  
**Zeile (ca.):** Die Zeile mit `gebaeude_auswahl = 0`

**Fehler:**
```python
gebaeude_auswahl = 0      # Welches Gebäude ist ausgewählt? (0-5)
```

**Richtig:**
```python
gebaeude_auswahl = 0      # Welches Gebäude ist ausgewählt? (0-6)
```

**Warum ist das didaktisch sinnvoll?**  
Der Kommentar sagt 0-5, also 6 Gebäude. Tatsächlich gibt es 7 (0-6). Schüler prüfen die Tastenbelegung: Taste 7 wählt Index 6 aus. Der Widerspruch führt sie zum Fehler.

---

## Fehler 9 — `main.py` — Falscher Wert in der Stunde-7-Zusammenfassung

**Datei:** `main.py`  
**Funktion/Stelle:** Footer-Block — Wiederholung Stunde 7  
**Zeile (ca.):** Zeile mit "produziert +1 Bevölkerung"

**Fehler:**
```python
#   ✓ Neues Gebäude: Wohnhaus (Index 6, produziert +1 Bevölkerung, kostet 20 Gold + 15 Holz + 10 Stein)
```

**Richtig:**
```python
#   ✓ Neues Gebäude: Wohnhaus (Index 6, produziert +2 Bevölkerung, kostet 20 Gold + 15 Holz + 10 Stein)
```

**Warum ist das didaktisch sinnvoll?**  
Der Kommentar im Footer widerspricht der README und der Wirtschafts-Tabelle in ressourcen.py. Schüler müssen die Konsistenz zwischen Hauptcode, Modulen und Dokumentation prüfen.

---

## Fehler 10 — `ressourcen.py` — Fehlender Eintrag in Namensliste

**Datei:** `ressourcen.py`  
**Funktion/Stelle:** `baukosten_abziehen()` — Liste `gebaeude_namen`  
**Zeile (ca.):** Die Liste mit den 6 Gebäude-Namen

**Fehler:**
```python
gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                  "Steinmetz", "Wohnhaus"]
```
(6 Einträge: Index 0–5; Index 6 = Wohnhaus fehlt)

**Richtig:**
```python
gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                  "Steinmetz", "Marktplatz", "Wohnhaus"]
```
(7 Einträge: Index 0–6)

**Warum ist das didaktisch sinnvoll?**  
Wenn ein Schüler das Wohnhaus baut, wird der Name als "Unbekannt" ausgegeben — weil Index 6 nicht in der Liste steht. Das zeigt, was passiert, wenn parallele Listen nicht synchronisiert werden.

---


# Stunde 9 — Lösungen zu den neuen Features

Diese Datei ist **nur für die Lehrkraft** gedacht.
Die sechs Verbesserungsvorschläge sind bereits **fertig umgesetzt**.
Hier findest du die wichtigsten Stellen als Übersicht für die Besprechung.

## 1. Gebäude abreißen (Rechtsklick)

- **`gebaeude.py`** → neue Funktion `gebaeude_abreissen(liste_gebaeude, kachel_x, kachel_y)`:
  - durchsucht die Liste nach passender Kachel, entfernt das Gebäude mit `remove()`
  - gibt `typ_index` zurück (oder `None`, wenn nichts steht)
  - Sicherheitsprüfung: `gebaeude["typ"] == 0` (Basis) → `print` + `return None`
- **`ressourcen.py`** → neue Funktion `ressourcen_zurueckerstatten(ressourcen_dict, typ_index)`:
  - `betrag = kosten // 2` (50 % abgerundet), fügt Werte wieder hinzu, gibt `rueckerstattung`-Dict zurück
- **`main.py`** → `elif ereignis.button == 3:` (rechte Maustaste) → Abriss + Ausgabe.

## 2. Mehr Infos bei der Gebäude-Auswahl

- **`hud.py`** → `_gebaeude_auswahl_zeichnen()` zeigt jetzt zusätzlich `Produktion` und `Verbrauch`.
  - Kästchen-Höhe auf `118` erhöht (von `70`), `hintergrund_y = get_height() - 108`.
  - Neue Hilfsfunktion `_ressourcen_name()` für deutsche Anzeige-Namen.

## 3. Baumenü mit TAB

- **Neues Modul `menu.py`**: `menu_initialisieren()`, `menu_umschalten()`, `menu_ist_offen()`, `menu_zeichnen(gebaeude_typen, gebaeude_wirtschaft, ressourcen_dict)`.
  - Halbtransparenter Hintergrund (Surface mit `SRCALPHA`).
  - Gesperrte Gebäude ausgegraut + 🔒 + Hinweistext (was zum Freischalten fehlt).
- **`main.py`**: `import menu`, `menu.menu_initialisieren(fenster)` in `spiel_starten()`, `if ereignis.key == pygame.K_TAB: menu.menu_umschalten()`, Aufruf `menu.menu_zeichnen(...)` **ganz am Ende** der Zeichenreihenfolge.

## 4. Tooltip beim Ressourcen-Icon

- **`hud.py`** → `_ressourcen_leiste_zeichnen(ressourcen, maus_pos, gebaeude_wirtschaft)`.
  - Abstand Maus↔Icon mit Satz des Pythagoras, bei `<= 12` → `_ressourcen_tooltip_zeichnen()`.
  - `hud_zeichnen()` hat neuen Parameter `maus_pos`, `main.py` übergibt `pygame.mouse.get_pos()`.

## 5. Rote Meldung bei zu wenig Rohstoffen

- **`hud.py`** → Modul-Variablen `_meldung_text`, `_meldung_timer`; Funktion `meldung_anzeigen(text)` setzt Timer auf 120.
  - `hud_zeichnen()` zeichnet Banner und macht `_meldung_timer -= 1`.
- **`main.py`** → im `else`-Zweig von `kann_bauen()`: `hud.meldung_anzeigen(f"Nicht genug Rohstoffe fuer {name}!")`.

## 6. Stufenweise Freischaltung

- **`ressourcen.py`** → neues Feld `freischaltung` in allen 7 Einträgen von `GEBAEUDE_WIRTSCHAFT`:
  - Marktplatz (5): `{"ressource": "bevoelkerung", "menge": 5}`
  - Wohnhaus (6): `{"ressource": "holz", "menge": 20}`
  - alle anderen: `None`
- **Neue Funktion** `ist_freigeschaltet(ressourcen_dict, typ_index)`.
- **`kann_bauen()`** prüft zuerst die Freischaltung (Prüfung 0) → `False` + Konsolenmeldung.

## Wichtige Stolperfallen (zum Besprechen)

- Rückerstattung **nur** nach erfolgreicher Abriss-Prüfung (sonst Gold geschenkt).
- `GEBAEUDE_TYPEN` und `GEBAEUDE_WIRTSCHAFT` müssen **gleiche Länge** haben (beide 7).
- `gebaeude_namen`-Listen in `ressourcen.py`/`hud.py` müssen alle 7 Einträge enthalten.
- `menu.py` muss **zuerst** `menu_initialisieren()` bekommen, sonst bleibt `_fenster = None`.
- Das Baumenü blockiert den Mausklick bewusst nicht.


# Aktuelle Lösungsskizze: Gebäudeaufgabe

Die älteren Lösungen beziehen sich auf sieben Gebäude und feste Einzelnummern. Für die aktuelle Fassung gelten folgende Prüfpunkte.

## 1. Parallele Gebäudelisten

`gebaeude.GEBAEUDE_TYPEN` und `ressourcen.GEBAEUDE_WIRTSCHAFT` müssen beide 18 Einträge besitzen. Die gemeinsame Reihenfolge endet mit Stahlwerk (12), Gewächshaus (13), Lagerhaus (14), Wohnblock (15), Handelsposten (16) und Koloniezentrum (17). Der Selbsttest prüft diese Länge automatisch.

## 2. Kategorienavigation

Die Definition steht in `gebaeude.GEBAEUDE_KATEGORIEN`. `main.py` speichert `_auswahl_kategorie`, `_auswahl_position` und `_letztes_gebaeude`. Zifferntasten rufen `kategorie_waehlen()` auf, Pfeile rufen `kategorie_weiter()` auf, und eine erfolgreiche Platzierung aktualisiert `_letztes_gebaeude`. Die Geschwindigkeitskonflikte der alten `1/2`-Belegung sind durch `+/-` beseitigt.

## 3. Vollständige Bildzuordnung

Jeder Eintrag in `GEBAEUDE_TYPEN` besitzt einen konkreten Wert `bild`. Die Datei muss in `bilder/` existieren. `labor.png` ist zu entfernen, weil die Universität das Labor ersetzt. Die Universität verwendet die einzige nichtquadratische Datei `schule_2x3_kacheln_64x96.png` und die Werte `breite: 2`, `hoehe: 3`.

## 4. Neue Wirtschaft

Die Basis produziert nun pro Tick je eine Einheit Gold, Energie, Holz und Stein. Das Stahlwerk verbraucht Eisen und Kohle und erzeugt Stahl. Ein Lagerhaus aktiviert nach `lagerhaus_ausbau` die Speichererweiterung, ein Handelsposten zählt in `handel.py` als Handelsgebäude und das Koloniezentrum aktiviert den globalen Produktionsbonus.

## 5. Tests

Der korrekte Abschluss lautet:

```text
STUNDE11_TESTS_OK
```

Zusätzlich sollte die Lehrkraft im Spiel die Kategorien, die HUD-Bildvorschau, Taste `0`, `+/-`, die 2×3-Universität und mindestens eine neue Forschungsfreischaltung demonstrieren.
