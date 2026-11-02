# Protokoll – Unterrichtsstunde am 03.11.2026

## Kurs
Fortgeschrittener Kurs – Terra_Nova

## Datum
03.11.2026 (Samstag)

## Teilnehmer
Lehrer + Schüler (Klasse)

## Zusammenfassung der Stunde

Heute wurde an dem Python-Spiel **Terra_Nova** gearbeitet. Der Schwerpunkt lag auf der Fehlerbehebung und der Vorbereitung der Hausaufgabe.

---

## Durchgeführte Arbeiten

### 1. Fehlerbehebung: Funktionsname in main.py korrigiert

**Problem:** Beim Bauen eines Gebäudes trat folgender Fehler auf:

```
AttributeError: module 'chunks' has no attribute 'kachel_in_besetztem_chunk'.
Did you mean: 'kachel_in_besitztem_chunk'?
```

**Ursache:** `main.py` rief `chunks.kachel_in_besetztem_chunk()` auf (mit "e"), aber in `chunks.py` ist die Funktion korrekt als `kachel_in_besitztem_chunk` definiert (mit "z").

**Lösung:** In `main.py` Zeile 2844 wurde der Funktionsname von `kachel_in_besetztem_chunk` auf `kachel_in_besitztem_chunk` korrigiert.

**Datei:** `Z:/Codes/Unterricht/Schuster/Fortgeschrittener Kurs/Terra_Nova/main.py`

**Validierung:**
- `python -m py_compile main.py` → `COMPILE_OK`
- `python tests/check.py` → `CHECK_OK`
- Spiel startet erfolgreich ohne `AttributeError`

---

### 2. Hausaufgabe erstellt / überarbeitet

**Datei:** `Z:/Codes/Unterricht/Schuster/Fortgeschrittener Kurs/Terra_Nova/Hausaufgaben/02112026.md`

**Inhalte:**
- Abgabedatum geändert auf **Samstag, 07.11.2026**
- **Punktesystem** eingeführt: Gesamt 300 Punkte (je 100 pro Aufgabe)
- **3 Aufgaben** für Schüler:
  1. Fehler-Auflistung (mindestens 3 Fehler finden)
  2. Überflüssigkeiten finden (mindestens 3 Überflüssigkeiten)
  3. Verbesserungen & Ideen (mindestens 3 Vorschläge)
- Jede Aufgabe hat ausfüllbare Tabellen mit leeren Feldern für direkte Eingabe
- Bewertungskriterien pro Aufgabe: Genauigkeit (40), Beweis (30), Begründung/Umsetzung (20), Vielfalt (10)
- Bonus-Punkte für zusätzliche Funde oder selbst durchgeführte Reparaturen

---

### 3. Aufräumarbeiten

Temporäre Hilfsdateien im falschen Ordner (`Z:/Codes/Untericht/Schuster/Fortgeschichtener Kurs/Terra_Nova/`) wurden gelöscht:
- `_check_kachel.py`
- `_check_names.py`
- `_diff_bloecke.py`
- `_diff_report.py`
- `_diff3.py`
- `_pathcheck.py`

---

## Offene Punkte / Nächste Schritte

- Bilddateien für Gebäude und Items prüfen (einige könnten fehlen)
- Doppelter Code in `main.py` entfernen (zweite `karte_generieren()` und zweite `karte_zeichnen()` waren bereits entfernt)
- Spielstand-Speichern/Laden mit Items ergänzen (Schritt 3 war bereits umgesetzt)
- Weitere Tests durchführen

---

## Dateien, die heute geändert wurden

| Datei | Änderung |
|-------|----------|
| `main.py` | Funktionsname `kachel_in_besetztem_chunk` → `kachel_in_besitztem_chunk` |
| `Hausaufgaben/02112026.md` | Abgabedatum, Punktesystem, ausfüllbare Tabellen |
| `Protokolle/Protokoll_2026-11-03.md` | Neu erstellt (dieses Protokoll) |

---