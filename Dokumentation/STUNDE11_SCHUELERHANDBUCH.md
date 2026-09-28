# Stunde 11 – Schülerhandbuch zum Forschungs- und Kolonieprojekt

## 1. Worum geht es in diesem Projekt?

In diesem Projekt entwickelt ihr ein eigenes kleines Kolonie-Aufbauspiel mit Python und Pygame weiter. Die Spielerin oder der Spieler baut Gebäude, sammelt Ressourcen, versorgt Bewohner, erforscht Technologien und erweitert die Kolonie. Der wichtigste Lernschritt in Stunde 11 ist, dass eine Forschung nicht nur im Menü angezeigt wird, sondern eine echte Veränderung im Spiel auslöst.

> **Merksatz:** Eine Forschungszeile besteht aus zwei Teilen. In `forschung.py` wird beschrieben, **was** die Forschung heißt und kostet. In `ressourcen.py`, `gebaeude.py`, `main.py` oder `handel.py` wird programmiert, **wie** sich die Forschung im Spiel auswirkt.

Wenn ihr nur einen Eintrag in `TECHNOLOGIEN` ergänzt, erscheint die Forschung zwar im Menü, aber sie verändert das Spiel noch nicht automatisch. Für jeden neuen Bonus braucht ihr deshalb eine passende Prüfzeile in der Wirtschaft oder im zuständigen Modul.

## 2. Die wichtigsten Dateien

| Datei | Aufgabe im Projekt | Wann wird sie geändert? |
|---|---|---|
| `main.py` | Spielschleife, Tastatur, Mausklicks, Kartenboden und Aufruf der Module | Für neue Tasten, neue Mausklick-Funktionen und neue Spielaktionen |
| `forschung.py` | Forschungsbaum, Kosten, Voraussetzungen, Forschungszeit und Forschungsmenü | Für jede neue Forschung und ihre Voraussetzungen |
| `ressourcen.py` | Baukosten, Produktion, Verbrauch, Personal, Speichergrenzen und Forschungswirkungen | Für jeden Bonus, der Ressourcen oder Gebäude verändert |
| `gebaeude.py` | Gebäudenamen, Farben, Kürzel, Bilder, Platzierung und Darstellung | Für neue Gebäude und eigene Gebäude-Bilder |
| `hud.py` | Ressourcenleiste, Auswahlfeld, Personal- und Statusanzeigen | Wenn neue Werte sichtbar werden sollen |
| `menu.py` | Baumenü mit allen Gebäuden, Kosten und Freischaltungen | Wenn neue Gebäudetypen angezeigt werden sollen |
| `handel.py` | 2:1-Tausch und Angebote anderer Kolonien | Für Handelssysteme und NPC-Angebote |
| `bilder/` | PNG-Bilder für die Gebäude | Wenn ihr eigene Grafiken einfügt |
| `test_stunde11.py` | Kleiner Selbsttest für wichtige Funktionen | Nach jeder größeren Änderung ausführen |

## 3. Wie ein Forschungs-Dictionary aufgebaut ist

Alle Forschungszeilen liegen in der Liste `TECHNOLOGIEN` in `forschung.py`. Ein Eintrag sieht zum Beispiel so aus:

```python
{
    "id": "verbesserte_aexte",
    "name": "Verbesserte Äxte",
    "kategorie": "Holzfäller",
    "beschreibung": "Holzfäller produzieren 10 Prozent mehr Holz.",
    "kosten": 35,
    "zeit": 9,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Jede Zeile im Dictionary hat eine bestimmte Aufgabe.

| Schlüssel | Bedeutung | Regel beim Ändern |
|---|---|---|
| `id` | Interner eindeutiger Name, den der Python-Code verwendet | Nur Kleinbuchstaben und Unterstriche verwenden; niemals zwei gleiche IDs anlegen |
| `name` | Name, der im Forschungsmenü angezeigt wird | Darf Leerzeichen und deutsche Umlaute enthalten |
| `kategorie` | Bereich des Forschungsbaums | Zum Beispiel `Energie`, `Farm` oder `Marktplatz` |
| `beschreibung` | Erklärung für die Spieler | Beschreibt den Bonus verständlich, verändert aber noch keine Spielregel |
| `kosten` | Benötigte Forschungspunkte | Höhere Werte machen die Forschung später und teurer |
| `zeit` | Anzahl der Forschungsfortschrittseinheiten | Die Forschung läuft nur weiter, wenn ein Labor arbeitet |
| `voraussetzung` | ID einer Forschung, die vorher abgeschlossen sein muss | `None` bedeutet, dass die Forschung sofort auswählbar ist |
| `schaltet_gebaeude_frei` | Index eines Gebäudes, das dadurch gebaut werden darf | Nur verwenden, wenn wirklich ein neues Gebäude freigeschaltet wird |

Die ID ist der wichtigste technische Wert. Im Forschungsmenü wird der `name` angezeigt, aber in den Berechnungen wird immer die `id` geprüft:

```python
if forschung.ist_technologie_erforscht("verbesserte_aexte"):
    # Hier kommt die besondere Wirkung der Äxte hin.
    pass
```

## 4. So fügt ihr eine eigene Forschung hinzu

### Schritt 1: Ein neues Dictionary ergänzen

Öffnet `forschung.py`, sucht die Liste `TECHNOLOGIEN` und fügt vor der schließenden eckigen Klammer einen neuen Eintrag ein:

```python
{
    "id": "luftreiniger",
    "name": "Luftreiniger",
    "kategorie": "Umwelt",
    "beschreibung": "Luftreiniger erhöhen die Effizienz der Kolonie.",
    "kosten": 80,
    "zeit": 20,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

### Schritt 2: Die Wirkung programmieren

Ein Eintrag in `TECHNOLOGIEN` ist zunächst nur Daten. Damit der Luftreiniger etwas tut, braucht ihr in `ressourcen.py` eine Abfrage. Angenommen, alle Produktionsgebäude sollen bei erforschter Luftreinigung fünf Prozent mehr erzeugen:

```python
if forschung.ist_technologie_erforscht("luftreiniger"):
    faktor *= 1.05
```

Die Abfrage muss an der Stelle stehen, an der der passende Produktionsfaktor berechnet wird. Für einen Bonus auf alle Ressourcen ist `_produktion_multiplikator()` geeignet. Für einen Bonus auf Baukosten gehört die Abfrage in `baukosten_berechnen()`.

### Schritt 3: Testen

Startet das Spiel und öffnet mit `F` das Forschungsmenü. Prüft zuerst, ob die neue Zeile erscheint. Danach testet ihr, ob genügend Forschungspunkte abgezogen werden, ob die Forschung mehrere Ticks dauert und ob sich die Zielressource nach dem Abschluss wirklich verändert.

## 5. Ausführliche Erklärung jeder Forschungszeile

Im folgenden Teil wird jede Forschungszeile des aktuellen Projekts erklärt. Zu jeder Forschung steht dabei:

1. Was die Spieler im Spiel sehen.
2. Welche Dictionary-Zeile den Eintrag beschreibt.
3. In welcher Funktion die Wirkung programmiert ist.
4. Wie ihr die Wirkung verändern oder erweitern könnt.
5. Was ihr testen sollt.

---

## 5.1 Gebäude-Forschungen

### 5.1.1 Effiziente Bautechnik

```python
{
    "id": "effiziente_bautechnik",
    "name": "Effiziente Bautechnik",
    "kategorie": "Gebäude",
    "beschreibung": "Alle Baukosten sind 5 Prozent günstiger.",
    "kosten": 30,
    "zeit": 8,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Diese Forschung verändert keine Produktion, sondern den Preis beim Bauen. Die eigentliche Berechnung steht in `ressourcen.py` in `baukosten_berechnen()`. Dort wird jede einzelne Baukosten-Ressource durch einen Faktor von `0.95` multipliziert. Aus 20 Gold werden dadurch 19 Gold, weil die Kosten auf eine ganze Zahl aufgerundet werden.

Wenn ihr den Rabatt ändern wollt, sucht:

```python
if forschung.ist_technologie_erforscht("effiziente_bautechnik"):
    faktor *= 0.95
```

Ein Rabatt von zehn Prozent wäre `0.90`. Achtet darauf, dass ihr den Code nicht in `baukosten_abziehen()` allein einfügt. Sonst würde die Prüfung vor dem Bauen noch mit dem alten Preis arbeiten. Die Funktion `baukosten_berechnen()` wird sowohl für die Prüfung als auch für das tatsächliche Abziehen verwendet.

**Test:** Vergleicht den Preis eines Reaktors vor und nach der Forschung. Prüft auch das Baumenü und das Auswahlfeld unten. Beide Anzeigen müssen denselben rabattierten Preis zeigen.

### 5.1.2 Kompakte Maschinen

```python
{
    "id": "kompakte_maschinen",
    "name": "Kompakte Maschinen",
    "kategorie": "Gebäude",
    "beschreibung": "Bis zu zwei Gebäude können eine Kachel nutzen.",
    "kosten": 45,
    "zeit": 12,
    "voraussetzung": "effiziente_bautechnik",
    "schaltet_gebaeude_frei": None,
},
```

Vor dieser Forschung wird in `gebaeude.py` geprüft, ob die Zielkachel schon belegt ist. Nach der Forschung darf ein zweites Produktionsgebäude dieselbe Kachel verwenden. Die Funktion `_kompakt_erlaubt()` prüft die Forschung. `kann_platzieren()` entscheidet anschließend, ob die konkrete Kachel noch Platz hat.

```python
return forschung.ist_technologie_erforscht("kompakte_maschinen") \
       and typ_index not in (0, 9)
```

Basis und Straße bleiben von dieser Sonderregel ausgeschlossen. Wenn ihr auch Straßen stapeln oder drei Gebäude zulassen wollt, müsst ihr die Bedingungen in `kann_platzieren()` ändern. Die Zeichenfunktion verschiebt das zweite Gebäude automatisch in eine kleinere Hälfte der Kachel.

**Test:** Baut ein Gebäude, erforscht Kompakte Maschinen und versucht anschließend, ein zweites Gebäude auf derselben Kachel zu bauen. Ein drittes Gebäude muss weiterhin abgelehnt werden.

### 5.1.3 Anpassende Architektur

```python
{
    "id": "anpassende_architektur",
    "name": "Anpassende Architektur",
    "kategorie": "Gebäude",
    "beschreibung": "Gut versorgte Betriebe erhalten automatisch bis zu 15 Prozent Effizienz.",
    "kosten": 140,
    "zeit": 35,
    "voraussetzung": "kompakte_maschinen",
    "schaltet_gebaeude_frei": None,
},
```

Die aktuelle Unterrichtsversion verwendet eine einfache Modellierung: Ein Gebäude, das in diesem Tick arbeiten kann, erhält einen Effizienzfaktor von `1.15`. Die Stelle befindet sich in `ressourcen_produzieren()`:

```python
effizient_bonus = 1.0
if forschung.ist_technologie_erforscht("anpassende_architektur"):
    effizient_bonus += 0.15
```

Danach wird jede Produktion mit diesem Faktor multipliziert. Für eine schwierigere Projektversion könnt ihr den Bonus von Bedingungen abhängig machen. Zum Beispiel könnte ein Gebäude nur dann den Bonus bekommen, wenn es mindestens 80 Prozent seiner benötigten Ressourcen im Speicher hat. Dafür würdet ihr die Bedingung vor `effizient_bonus += 0.15` einfügen.

**Test:** Baut eine Farm und beobachtet die Nahrungsproduktion. Vergleicht die Produktion mit und ohne Forschung. Prüft außerdem, dass ein Gebäude ohne ausreichendes Personal keinen Bonus erhält, weil es gar nicht arbeitet.

---

## 5.2 Energie-Forschungen

### 5.2.1 Energieoptimierung

```python
{
    "id": "energieoptimierung",
    "name": "Energieoptimierung",
    "kategorie": "Energie",
    "beschreibung": "Der Energieverbrauch aller Gebäude sinkt um 5 Prozent.",
    "kosten": 35,
    "zeit": 9,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Der Bonus wird in `ressourcen_produzieren()` direkt auf den Energieverbrauch angewendet:

```python
if forschung.ist_technologie_erforscht("energieoptimierung") \
        and "energie" in verbrauch:
    verbrauch["energie"] *= 0.95
```

Der wichtige Gedanke ist, dass `verbrauch` vorher als Kopie aus den Gebäudedaten erstellt wird. Dadurch werden nicht dauerhaft die Grunddaten des Gebäudes verändert. Bei jedem Wirtschaftstick wird neu berechnet, wie viel Energie dieses Gebäude verbraucht.

Wenn ihr statt fünf Prozent eine feste Einsparung von einer Energieeinheit möchtet, könnt ihr den Wert anders berechnen. Achtet aber darauf, dass der Verbrauch nicht negativ wird. Eine sichere Variante ist `max(0, verbrauch["energie"] - 1)`.

**Test:** Baut eine Farm oder ein Wohnhaus, notiert den Energieverbrauch pro Tick und vergleicht ihn nach Abschluss der Forschung.

### 5.2.2 Verbesserte Generatoren

```python
{
    "id": "verbesserte_generatoren",
    "name": "Verbesserte Generatoren",
    "kategorie": "Energie",
    "beschreibung": "Energieproduktion steigt um 10 Prozent.",
    "kosten": 55,
    "zeit": 14,
    "voraussetzung": "energieoptimierung",
    "schaltet_gebaeude_frei": None,
},
```

Die Wirkung steht in `_produktion_multiplikator()` in `ressourcen.py`. Die Funktion erhält den Gebäudetyp und den Namen der produzierten Ressource. Nur wenn die Ressource `energie` heißt, wird der Faktor um zehn Prozent erhöht:

```python
if ress_name == "energie" \
        and forschung.ist_technologie_erforscht("verbesserte_generatoren"):
    faktor *= 1.10
```

Diese Schreibweise ist besser als ein Bonus direkt beim Reaktor, weil auch der Fusionsreaktor davon profitieren kann. Wenn ihr nur normale Reaktoren verbessern wollt, ergänzt zusätzlich `and typ_index == 1`.

**Test:** Vergleicht einen normalen Reaktor und einen Fusionsreaktor vor und nach der Forschung. Beide müssen korrekt auf die Forschung reagieren, wenn ihr den allgemeinen Bonus beibehalten wollt.

### 5.2.3 Energiespeicher

```python
{
    "id": "energiespeicher",
    "name": "Energiespeicher",
    "kategorie": "Energie",
    "beschreibung": "Die maximale Energiespeicherkapazität steigt um 25 Prozent.",
    "kosten": 50,
    "zeit": 12,
    "voraussetzung": "energieoptimierung",
    "schaltet_gebaeude_frei": None,
},
```

Die Grundlimits stehen in `SPEICHER_BASIS`. Die Funktion `maximaler_speicher()` prüft, ob die Forschung abgeschlossen ist:

```python
if ressourcen_name == "energie" \
        and forschung.ist_technologie_erforscht("energiespeicher"):
    limit *= 1.25
```

`ressourcen_begrenzen()` benutzt anschließend dieses Limit. So kann Energie nicht einfach unendlich anwachsen. Wenn ihr auch Holz oder Nahrung durch einen neuen Speicher vergrößern wollt, braucht ihr eine zusätzliche Forschung-ID und eine weitere Bedingung für die jeweilige Ressource.

**Test:** Setzt testweise die Energie auf 999, ruft `ressourcen_begrenzen()` auf und prüft, ob ohne Forschung höchstens 100 und mit Forschung höchstens 125 Energie übrig bleiben.

### 5.2.4 Fusionsreaktor

```python
{
    "id": "fusionsreaktor",
    "name": "Fusionsreaktor",
    "kategorie": "Energie",
    "beschreibung": "Schaltet einen sehr leistungsstarken Energieerzeuger frei.",
    "kosten": 160,
    "zeit": 40,
    "voraussetzung": "verbesserte_generatoren",
    "schaltet_gebaeude_frei": 10,
},
```

Hier sieht man den Unterschied zwischen einem Bonus und einer Gebäudefreischaltung. Der Forschungsdatensatz sagt mit `schaltet_gebaeude_frei: 10`, dass Gebäudeindex 10 freigeschaltet wird. Der Index muss exakt zur Position in `GEBAEUDE_TYPEN` und `GEBAEUDE_WIRTSCHAFT` passen.

In `ressourcen.py` ist der Fusionsreaktor der elfte Eintrag. Er produziert 25 Energie, verbraucht fünf Kohle und benötigt vier Personal. Wenn ihr ein neues Gebäude an einer anderen Stelle einfügt, müsst ihr unbedingt beide parallelen Listen anpassen.

**Test:** Prüft, dass der Fusionsreaktor vor der Forschung im Baumenü gesperrt und danach verfügbar ist. Baut ihn anschließend und kontrolliert Personal-, Kohle- und Energieänderungen.

### 5.2.5 Mini-Reaktor

```python
{
    "id": "mini_reaktor",
    "name": "Mini-Reaktor",
    "kategorie": "Energie",
    "beschreibung": "Große Gebäude erzeugen zusätzlich 1 Energie pro Tick.",
    "kosten": 95,
    "zeit": 24,
    "voraussetzung": "verbesserte_generatoren",
    "schaltet_gebaeude_frei": None,
},
```

Große Gebäude sind in `GEBAEUDE_WIRTSCHAFT` mit `"grosse_anlage": True` gekennzeichnet. Im Wirtschaftstick wird geprüft:

```python
if forschung.ist_technologie_erforscht("mini_reaktor") \
        and wirtschaft.get("grosse_anlage") and typ_index != 1:
    produktion["energie"] = produktion.get("energie", 0) + 1
```

Der Reaktor selbst wird ausgeschlossen, weil er bereits ein Energiegebäude ist. Wenn ihr Wohnhäuser ebenfalls ausschließen wollt, ergänzt `and typ_index != 6`. Wenn ihr den Mini-Reaktor als echtes Upgrade-Gebäude bauen wollt, müsst ihr statt dieses Bonus-Codes ein eigenes Gebäude mit Baukosten und Freischaltung anlegen.

**Test:** Baut ein Labor oder eine Mine und vergleicht die Energieproduktion vor und nach der Forschung.

---

## 5.3 Forschungs- und Labor-Forschungen

### 5.3.1 Verbesserte Laborausrüstung

```python
{
    "id": "verbesserte_laborausruestung",
    "name": "Verbesserte Laborausrüstung",
    "kategorie": "Forschung",
    "beschreibung": "Die Forschungsgeschwindigkeit steigt um 10 Prozent.",
    "kosten": 40,
    "zeit": 10,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Die Forschung selbst läuft in `forschung.py` in `forschung_tick()`. Die Grundgeschwindigkeit hängt von der Anzahl der arbeitenden Labore ab. Danach wird der Zehn-Prozent-Bonus addiert:

```python
tempo = float(aktive_labore)
if ist_technologie_erforscht("verbesserte_laborausruestung"):
    tempo += 0.10
```

Wichtig ist die Variable `aktive_labore`. Ein Labor zählt nur dann, wenn es genug Personal und alle Verbrauchsressourcen hat. Dadurch übt ihr gleichzeitig die Personalmechanik und die Forschungsmechanik.

**Test:** Startet eine lange Forschung, lasst ein Labor arbeiten und beobachtet den Fortschritt. Entfernt danach das verfügbare Personal oder die nötige Ressource. Der Fortschritt muss stehen bleiben.

### 5.3.2 Neue Geräte und Instrumente

```python
{
    "id": "neue_instrumente",
    "name": "Neue Geräte und Instrumente",
    "kategorie": "Forschung",
    "beschreibung": "Labore erzeugen 5 Prozent mehr Forschungspunkte.",
    "kosten": 60,
    "zeit": 15,
    "voraussetzung": "verbesserte_laborausruestung",
    "schaltet_gebaeude_frei": None,
},
```

Dieser Bonus wird in `_produktion_multiplikator()` nur für Gebäudeindex 7, also das Universitätsgebäude, und nur für die Ressource `forschung` angewendet:

```python
if typ_index == 7 and ress_name == "forschung" \
        and forschung.ist_technologie_erforscht("neue_instrumente"):
    faktor *= 1.05
```

Die beiden Bedingungen sind wichtig. Ohne `typ_index == 7` würden auch andere Gebäude fünf Prozent mehr Forschung erzeugen. Ohne `ress_name == "forschung"` würde das Labor möglicherweise auch andere Ressourcenboni erhalten.

**Test:** Baut ein Labor, lasst es arbeiten und vergleicht seine Forschungspunkte pro Tick mit der Produktion vor und nach der Forschung.

### 5.3.3 Quantencomputer

```python
{
    "id": "quantencomputer",
    "name": "Quantencomputer",
    "kategorie": "Forschung",
    "beschreibung": "Endgame: Forschungsgeschwindigkeit steigt um weitere 40 Prozent.",
    "kosten": 180,
    "zeit": 45,
    "voraussetzung": "neue_instrumente",
    "schaltet_gebaeude_frei": None,
},
```

Der Quantencomputer wird an derselben Stelle wie die verbesserte Laborausrüstung verarbeitet:

```python
if ist_technologie_erforscht("quantencomputer"):
    tempo += 0.40
```

Der Bonus wird nicht als Multiplikation, sondern als zusätzliche Fortschrittseinheit modelliert. Das ist für Schülerinnen und Schüler leicht zu lesen. Für ein anderes Balancing könnt ihr auch `tempo *= 1.40` verwenden. Dann würde sich der Bonus stärker nach der Zahl der aktiven Labore richten.

**Test:** Startet dieselbe Forschung einmal ohne und einmal mit Quantencomputer. Vergleicht die benötigte Anzahl an Wirtschaftsticks.

---

## 5.4 Robotik und Automatisierung

### 5.4.1 Einfache Robotik

```python
{
    "id": "einfache_robotik",
    "name": "Einfache Robotik",
    "kategorie": "Automatisierung",
    "beschreibung": "Schaltet die Roboterfabrik frei; Roboter können arbeiten.",
    "kosten": 75,
    "zeit": 18,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": 11,
},
```

Die Forschung schaltet Gebäudeindex 11, also die Roboterfabrik, frei. Die Roboterfabrik produziert pro Tick einen Roboter, braucht dafür Energie und Kohle und benötigt zunächst zwei Personen. Danach zählt die Ressource `roboter` in `personal_info()` und `ressourcen_produzieren()` als zusätzliches Personal:

```python
verfuegbares_personal = int(
    ressourcen_dict.get("bevoelkerung", 0)
    + ressourcen_dict.get("roboter", 0)
)
```

Wenn ihr Roboter langsamer, teurer oder leistungsfähiger machen wollt, verändert ihr den Eintrag der Roboterfabrik in `GEBAEUDE_WIRTSCHAFT`.

**Test:** Erforscht Robotik, baut eine Roboterfabrik und prüft, ob die Roboterressource steigt. Baut anschließend mehr Produktionsgebäude als Bewohner vorhanden sind und beobachtet, ob Roboter zusätzliche Betriebe besetzen.

### 5.4.2 Autonome Fabriken

```python
{
    "id": "autonome_fabriken",
    "name": "Autonome Fabriken",
    "kategorie": "Automatisierung",
    "beschreibung": "Produktionsgebäude benötigen 30 Prozent weniger Personal.",
    "kosten": 170,
    "zeit": 42,
    "voraussetzung": "einfache_robotik",
    "schaltet_gebaeude_frei": None,
},
```

Der Personalbedarf wird zentral in `personalbedarf()` berechnet:

```python
if forschung.ist_technologie_erforscht("autonome_fabriken") and bedarf:
    return max(1, int(round(bedarf * 0.70)))
```

`max(1, ...)` verhindert, dass ein Produktionsgebäude durch Rundung gar kein Personal mehr benötigt. Wenn ihr manche Gebäude vollständig autonom machen wollt, könnt ihr für bestimmte Typen eine Sonderregel ergänzen. Überlegt vorher, ob das Spiel dadurch zu leicht wird.

**Test:** Notiert den Personalbedarf einer Mine oder eines Labors vor der Forschung. Nach Abschluss muss die Anzeige im HUD den reduzierten Bedarf zeigen.

---

## 5.5 Steinmetz-Forschungen

### 5.5.1 Effizienter Aufbau

```python
{
    "id": "effizienter_aufbau",
    "name": "Effizienter Aufbau",
    "kategorie": "Steinmetz",
    "beschreibung": "Steinmetze produzieren 10 Prozent mehr Stein.",
    "kosten": 35,
    "zeit": 9,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Der Bonus wird für Gebäudeindex 4, den Steinmetz, in `_produktion_multiplikator()` aktiviert:

```python
if typ_index == 4 and forschung.ist_technologie_erforscht("effizienter_aufbau"):
    faktor *= 1.10
```

Die ID muss exakt gleich geschrieben werden wie im Forschungsdictionary. Schon ein Tippfehler wie `effizienter_aufbau ` mit Leerzeichen würde dazu führen, dass die Forschung zwar im Menü erscheint, aber keine Wirkung hat.

**Test:** Baut einen Steinmetz auf Gestein und vergleicht seine Steinproduktion.

### 5.5.2 Tiefenbohrung

```python
{
    "id": "tiefenbohrung",
    "name": "Tiefenbohrung",
    "kategorie": "Steinmetz",
    "beschreibung": "Neue tiefe Vorkommen erhöhen die Ausbeute von Minen.",
    "kosten": 70,
    "zeit": 18,
    "voraussetzung": "effizienter_aufbau",
    "schaltet_gebaeude_frei": None,
},
```

In der aktuellen Umsetzung erhöht Tiefenbohrung den Eisenrhythmus der Mine. Ohne Forschung gibt es Eisen alle zehn Wirtschaftsticks, mit Forschung alle fünf Wirtschaftsticks. Zusätzlich erhöht `_produktion_multiplikator()` den Minenbonus.

Die Zeitprüfung sieht vereinfacht so aus:

```python
if typ_index == 8 and _wirtschafts_tick % (
        5 if forschung.ist_technologie_erforscht("tiefenbohrung") else 10
    ) == 0:
    produktion["eisen"] = 1
```

**Test:** Baut eine Mine, notiert den Wirtschafts-Tick und beobachtet, wann Eisen erscheint. Für eine anspruchsvollere Version könnt ihr statt eines festen Rhythmus eine zufällige Vorkommenswahrscheinlichkeit verwenden.

---

## 5.6 Holzfäller-Forschungen

### 5.6.1 Verbesserte Äxte

```python
{
    "id": "verbesserte_aexte",
    "name": "Verbesserte Äxte",
    "kategorie": "Holzfäller",
    "beschreibung": "Holzfäller produzieren 10 Prozent mehr Holz.",
    "kosten": 35,
    "zeit": 9,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Der Bonus gilt nur für Gebäudeindex 3. Die passende Stelle liegt in `_produktion_multiplikator()`:

```python
if typ_index == 3 and forschung.ist_technologie_erforscht("verbesserte_aexte"):
    faktor *= 1.10
```

**Test:** Baut einen Holzfäller, sorgt für ausreichend Energie und vergleicht die Holzproduktion.

### 5.6.2 Forstwirtschaft

```python
{
    "id": "forstwirtschaft",
    "name": "Forstwirtschaft",
    "kategorie": "Holzfäller",
    "beschreibung": "Wälder wachsen schneller nach, wenn sie abgeholzt sind.",
    "kosten": 70,
    "zeit": 18,
    "voraussetzung": "verbesserte_aexte",
    "schaltet_gebaeude_frei": None,
},
```

Nach dieser Forschung bekommt jeder Holzfäller einen internen Waldvorrat. Der Vorrat wird in `gebaeude.py` beim Platzieren angelegt:

```python
neues_gebaeude["wald_vorrat"] = 30
neues_gebaeude["wald_nachwuchs"] = 0
```

In `ressourcen.py` wird der Vorrat bei laufender Produktion verringert. Wenn er null erreicht, arbeitet der Holzfäller einige Ticks nicht und der Nachwuchswert steigt. Danach wird der Waldvorrat wieder aufgefüllt.

Diese Unterrichtsversion speichert den Waldvorrat am Holzfäller-Gebäude. Eine mögliche Projekt-Erweiterung wäre ein echtes Waldobjekt auf der Karte. Dafür müsstet ihr in `karten_daten` zusätzliche Informationen speichern, etwa `wald_vorrat` pro Kachel.

**Test:** Lasst einen Holzfäller lange arbeiten, bis sein Vorrat erschöpft ist. Beobachtet die Produktionspause und das spätere Nachwachsen.

### 5.6.3 Effizientere Holzverwendung

```python
{
    "id": "effizientere_holzverwendung",
    "name": "Effizientere Holzverwendung",
    "kategorie": "Holzfäller",
    "beschreibung": "Der Holzanteil aller Baukosten sinkt um 5 Prozent.",
    "kosten": 65,
    "zeit": 16,
    "voraussetzung": "forstwirtschaft",
    "schaltet_gebaeude_frei": None,
},
```

Die Wirkung wird in `baukosten_berechnen()` nur auf den Schlüssel `holz` angewendet:

```python
if ress_name == "holz" \
        and forschung.ist_technologie_erforscht("effizientere_holzverwendung"):
    faktor *= 0.95
```

Da die Funktion über alle Baukosten läuft, werden nur Gebäude mit einem Holzanteil verändert. Gebäude ohne Holz bleiben gleich teuer.

**Test:** Vergleicht die Baukosten eines Wohnhauses vor und nach der Forschung. Prüft außerdem ein Gebäude ohne Holzkosten, zum Beispiel eine Straße.

---

## 5.7 Marktplatz-Forschungen

### 5.7.1 Verbesserte Marktstände

```python
{
    "id": "verbesserte_marktstaende",
    "name": "Verbesserte Marktstände",
    "kategorie": "Marktplatz",
    "beschreibung": "Marktplätze erzeugen 10 Prozent mehr Gold.",
    "kosten": 40,
    "zeit": 10,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Der Marktplatz besitzt Gebäudeindex 5. In `_produktion_multiplikator()` wird deshalb geprüft:

```python
if typ_index == 5 and forschung.ist_technologie_erforscht("verbesserte_marktstaende"):
    faktor *= 1.10
```

**Test:** Baut einen Marktplatz, sorgt für genügend Stein und vergleicht die Goldproduktion.

### 5.7.2 Ressourcenhandel

```python
{
    "id": "ressourcenhandel",
    "name": "Ressourcenhandel",
    "kategorie": "Marktplatz",
    "beschreibung": "Ressourcen können am Marktplatz im Kurs 2:1 getauscht werden.",
    "kosten": 65,
    "zeit": 16,
    "voraussetzung": "verbesserte_marktstaende",
    "schaltet_gebaeude_frei": None,
},
```

Die eigentliche Handelslogik steht in `handel.py`. `ressourcen_tauschen()` prüft zuerst, ob ein Marktplatz vorhanden ist und ob die Forschung abgeschlossen wurde. Danach werden zwei Einheiten der Ausgangsressource abgezogen und eine Einheit der Zielressource hinzugefügt.

```python
if not _marktplatz_aktiv:
    hud.meldung_anzeigen("Für Handel wird ein Marktplatz benötigt.")
    return False
if not forschung.ist_technologie_erforscht("ressourcenhandel"):
    return False
```

Die Tastenpaare stehen in `handelsmenue_taste()`. Wenn ihr einen weiteren Tausch hinzufügen wollt, ergänzt ihr das Dictionary `paare`:

```python
pygame.K_i: ("gold", "energie"),
```

Danach müsst ihr den Tausch im Handelsmenü erklären, damit die Spieler wissen, welche Taste verwendet wird.

**Test:** Baut einen Marktplatz, öffnet mit `E` das Handelsmenü und probiert einen Tausch mit mindestens zwei Einheiten der Ausgangsressource.

### 5.7.3 Handel mit anderen Kolonien

```python
{
    "id": "handel_mit_kolonien",
    "name": "Handel mit anderen Kolonien",
    "kategorie": "Marktplatz",
    "beschreibung": "Andere Kolonien schicken zeitweise Angebote.",
    "kosten": 100,
    "zeit": 25,
    "voraussetzung": "ressourcenhandel",
    "schaltet_gebaeude_frei": None,
},
```

`handel_tick()` zählt Wirtschaftsticks. Wenn die Forschung abgeschlossen ist, ein Marktplatz existiert und gerade kein Angebot läuft, wird regelmäßig ein Angebot erzeugt. Die Angebote stehen in der Liste `_ANGEBOTE`:

```python
{"geben": {"holz": 20}, "nehmen": {"stein": 10},
 "text": "Holz gegen Stein"},
```

`geben` beschreibt die Ressourcen, die die eigene Kolonie abgibt. `nehmen` beschreibt die erhaltenen Ressourcen. Für ein eigenes Angebot fügt ihr ein weiteres Dictionary zur Liste hinzu. Danach prüft `angebot_annahmen()`, ob die Kolonie die abzugebenden Ressourcen besitzt.

**Test:** Erforscht die drei Marktplatz-Forschungen, wartet die benötigte Zeit und öffnet mit `E` das Handelsmenü. Prüft, ob ein Angebot mit `J` angenommen und mit `K` abgelehnt werden kann.

---

## 5.8 Farm-Forschungen

### 5.8.1 Verbesserte Landwirtschaft

```python
{
    "id": "verbesserte_landwirtschaft",
    "name": "Verbesserte Landwirtschaft",
    "kategorie": "Farm",
    "beschreibung": "Farmen erzeugen 10 Prozent mehr Nahrung.",
    "kosten": 40,
    "zeit": 10,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": None,
},
```

Farmen haben Gebäudeindex 2. Die Wirkung wird deshalb in `_produktion_multiplikator()` über `typ_index == 2` aktiviert. Die Grundproduktion bleibt in `GEBAEUDE_WIRTSCHAFT` stehen; der Forschungsbonus wird nur beim aktuellen Tick berechnet.

**Test:** Baut eine Farm auf Gras, versorgt sie mit Energie und vergleicht die Nahrungsproduktion.

### 5.8.2 Höher sättigende Nahrung

```python
{
    "id": "hoeher_saettigende_nahrung",
    "name": "Höher sättigende Nahrung",
    "kategorie": "Farm",
    "beschreibung": "Der Nahrungsverbrauch pro Bewohner sinkt um 5 Prozent.",
    "kosten": 55,
    "zeit": 14,
    "voraussetzung": "verbesserte_landwirtschaft",
    "schaltet_gebaeude_frei": None,
},
```

Der Bewohnerverbrauch wird am Beginn jedes Wirtschaftsticks berechnet:

```python
nahrungsverbrauch = ressourcen_dict.get("bevoelkerung", 0) * 0.05
if forschung.ist_technologie_erforscht("hoeher_saettigende_nahrung"):
    nahrungsverbrauch *= 0.95
```

Bei 20 Bewohnern beträgt der Grundverbrauch 1 Nahrung pro Tick. Nach der Forschung beträgt er 0,95 Nahrung pro Tick.

**Test:** Setzt testweise die Bevölkerung auf 20 und Nahrung auf 10. Vergleicht die Abnahme über mehrere Ticks.

### 5.8.3 Terraforming für Farmbau

```python
{
    "id": "terraforming",
    "name": "Terraforming für Farmbau",
    "kategorie": "Farm",
    "beschreibung": "Freie Kacheln können in fruchtbaren Boden umgewandelt werden.",
    "kosten": 85,
    "zeit": 22,
    "voraussetzung": "verbesserte_landwirtschaft",
    "schaltet_gebaeude_frei": None,
},
```

Nach Abschluss aktiviert `Z` den Terraforming-Modus. Ein Linksklick ruft in `main.py` die Funktion `ressourcen.terraformieren()` auf. Diese Funktion prüft Forschung, Kartengrenzen, bereits fruchtbaren Boden und die Kosten von fünf Energie und drei Stein. Danach wird der Bodentyp der Kachel auf `1`, also Gras, gesetzt.

Wenn ihr Terraforming teurer machen wollt, ändert ihr das Dictionary:

```python
kosten = {"energie": 8, "stein": 5}
```

Eine nächste Projektstufe wäre, nur freie Kacheln umzuwandeln. Dafür müsste `terraformieren()` zusätzlich die Liste `liste_gebaeude` erhalten und prüfen, ob auf der Kachel bereits ein Gebäude steht.

**Test:** Erforscht Terraforming, drückt `Z`, klickt auf eine Gesteins- oder Sandkachel und baut dort anschließend eine Farm.

---

## 5.9 Die fünf älteren Grundlagen-Forschungen

Die folgenden Forschungen stammen aus Stunde 10 und bleiben im Projekt enthalten, weil sie den Einstieg und die Verbindung zu den neuen Forschungen bilden.

| Forschung | Was passiert? | Wichtige Stelle im Code |
|---|---|---|
| `wohnbau` | Schaltet das Wohnhaus frei | `schaltet_gebaeude_frei: 6`; Gebäudeindex 6 ist das Wohnhaus |
| `produktion` | Erhöht die Produktion aller Produktionsgebäude um 25 Prozent | `_produktion_multiplikator()` mit `faktor *= 1.25` |
| `stein_effizienz` | Verringert den Energieverbrauch des Steinmetzes um eine Einheit | `ressourcen_produzieren()` beim Typindex 4 |
| `minenbau` | Schaltet die Mine frei | `schaltet_gebaeude_frei: 8`; Gebäudeindex 8 ist die Mine |
| `reaktor_upgrade` | Reaktoren benötigen Kohle und erzeugen zusätzlich Energie | Sonderbehandlung für Typindex 1 im Wirtschaftstick |

Bei diesen Forschungen könnt ihr genauso vorgehen wie bei den neuen Einträgen: Zuerst den Datensatz lesen, dann die ID in `ressourcen.py` suchen und anschließend die Wirkung anpassen.

## 6. Personal – warum Gebäude manchmal nicht produzieren

Jedes Produktionsgebäude besitzt in `GEBAEUDE_WIRTSCHAFT` den Schlüssel `personalbedarf`:

```python
{
    "baukosten": {"gold": 15, "energie": 10},
    "produktion": {"stein": 5},
    "verbrauch": {"energie": 3},
    "personalbedarf": 2,
    "max_anzahl": None,
    ...
}
```

Die Bevölkerung und die Roboter bilden das verfügbare Personal. Im Wirtschaftstick wird Gebäude für Gebäude geprüft, ob noch genug Personal vorhanden ist. Wenn nicht, erhält das Gebäude `"arbeitet": False` und produziert in diesem Tick nichts.

> **Lernaufgabe:** Baut mehr Gebäude, als eure Bevölkerung besetzen kann. Beobachtet den roten Punkt am Gebäude und die Personalzeile im HUD. Erforscht danach Robotik und baut eine Roboterfabrik.

Wenn ihr ein eigenes Gebäude erstellt, müsst ihr immer einen Personalbedarf festlegen. Ein Wohnhaus hat aktuell `0`, weil es Bewohner erzeugt und nicht von Bewohnern besetzt werden muss. Eine Straße hat ebenfalls `0`, weil sie keine Produktion besitzt.

## 7. Ein neues Gebäude vollständig hinzufügen

Ein neues Gebäude wird an mindestens vier Stellen eingetragen. Die Listen müssen parallel bleiben.

### 7.1 Gebäudebild und Anzeige in `gebaeude.py`

Fügt in `GEBAEUDE_TYPEN` einen Eintrag hinzu:

```python
{
    "name": "Luftreiniger",
    "bild": "luftreiniger.png",
    "farbe": (120, 220, 180),
    "kuerzel": "L",
    "taste": "L",
},
```

`name` wird für die Anzeige und als Schlüssel beim Bildladen verwendet. `bild` ist der exakte Dateiname im Ordner `bilder/`. `farbe` ist der Fallback, wenn das Bild fehlt. `kuerzel` wird auf dem farbigen Rechteck angezeigt. `taste` erscheint im Baumenü.

### 7.2 Wirtschaftsdaten in `ressourcen.py`

Fügt an derselben Position den passenden Eintrag ein:

```python
{
    "baukosten": {"gold": 45, "energie": 10},
    "produktion": {"gold": 3},
    "verbrauch": {"energie": 1},
    "personalbedarf": 1,
    "max_anzahl": None,
    "freischaltung": {"typ": "forschung", "technologie": "luftreiniger"},
    "grosse_anlage": False,
},
```

Der Eintrag muss dieselbe Position haben wie der Gebäudeeintrag. Wenn `GEBAEUDE_TYPEN[12]` der Luftreiniger ist, muss auch `GEBAEUDE_WIRTSCHAFT[12]` der Luftreiniger sein.

### 7.3 Forschung zur Freischaltung

In `forschung.py` wird die Forschung mit `schaltet_gebaeude_frei` auf denselben Index verknüpft:

```python
{
    "id": "luftreiniger",
    "name": "Luftreiniger",
    "kategorie": "Umwelt",
    "beschreibung": "Schaltet das Gebäude Luftreiniger frei.",
    "kosten": 80,
    "zeit": 20,
    "voraussetzung": None,
    "schaltet_gebaeude_frei": 12,
},
```

In den Wirtschaftsdaten des Gebäudes muss die Freischaltung ebenfalls auf die Technologie-ID verweisen. So prüfen Forschungsmenü und Baumenü dieselbe Regel.

### 7.4 Tastatur in `main.py`

Wenn das Gebäude eine Buchstabentaste bekommen soll, ergänzt ihr im Bereich der Gebäudeauswahl:

```python
if ereignis.key == pygame.K_l:
    gebaeude_auswahl = 12
    print("Gebäude-Auswahl: Luftreiniger")
```

Die Zahl `12` ist wieder der Gebäudeindex. Verwendet niemals einfach die Anzahl der Einträge, ohne die tatsächliche Position zu prüfen.

### 7.5 Besondere Wirkung programmieren

Wenn der Luftreiniger beispielsweise die Forschung steigert, gehört die Wirkung in die passende Funktion. Für einen allgemeinen Produktionsbonus:

```python
if forschung.ist_technologie_erforscht("luftreiniger"):
    faktor *= 1.05
```

Für eine Gebäudesonderregel ist eine Prüfung des `typ_index` besser:

```python
if typ_index == 12 and forschung.ist_technologie_erforscht("luftreiniger"):
    produktion["forschung"] = produktion.get("forschung", 0) + 1
```

## 8. Eigene Bilder für Gebäude einfügen

### 8.1 Richtige Ordnerstruktur

Die Bilddateien müssen im Unterordner `bilder` liegen:

```text
Stunde 11/
├── main.py
├── gebaeude.py
├── ressourcen.py
├── forschung.py
└── bilder/
    ├── basis.png
    ├── reaktor.png
    ├── farm.png
    ├── holzfaeller.png
    ├── steinmetz.png
    ├── marktplatz.png
    ├── wohnhaus.png
    ├── labor.png
    └── luftreiniger.png
```

Der Dateiname im Code muss exakt gleich geschrieben sein wie der Dateiname im Ordner. `Luftreiniger.png`, `luftreiniger.png` und `luftreiniger.PNG` können je nach Betriebssystem als unterschiedliche Dateien behandelt werden.

### 8.2 Empfohlene Bildgröße

Verwendet quadratische PNG-Dateien, zum Beispiel 64 × 64 Pixel oder 128 × 128 Pixel. Das Bild wird im Spiel automatisch auf die Größe der Gebäudekachel skaliert. Ein quadratisches Bild verhindert Verzerrungen.

Ein transparenter Hintergrund ist empfehlenswert. Speichert die Grafik als PNG mit Alpha-Kanal, damit die Bodenfarbe rund um das Gebäude sichtbar bleibt. Wenn ihr ein Bild mit weißem Hintergrund verwendet, erscheint im Spiel ein weißes Quadrat hinter dem Gebäude.

### 8.3 Bild mit einem Zeichenprogramm erstellen

Ihr könnt ein Bild mit einem beliebigen Zeichenprogramm erstellen. Erstellt eine quadratische Leinwand, zeichnet das Gebäude von oben oder leicht schräg und verwendet eine klare Farbe. Speichert anschließend über „Exportieren“ oder „Speichern unter“ als PNG in den Ordner `bilder`.

Achtet besonders auf drei Dinge: Der Hintergrund sollte transparent sein, das Gebäude sollte nicht bis ganz an den Rand reichen und das Bild sollte unter einem kurzen, eindeutigen Namen gespeichert werden.

### 8.4 Wie der Code das Bild lädt

In `gebaeude_initialisieren()` wird der Pfad zusammengesetzt:

```python
bilder_ordner = os.path.join(os.path.dirname(__file__), "bilder")
bild_pfad = os.path.join(bilder_ordner, dateiname)
```

`os.path.dirname(__file__)` bedeutet: Suche relativ zum Ordner, in dem `gebaeude.py` liegt. Dadurch funktioniert das Projekt auch dann, wenn es von einem anderen aktuellen Arbeitsordner aus gestartet wird.

Danach prüft der Code, ob die Datei existiert:

```python
if os.path.exists(bild_pfad):
    _bilder[typ_daten["name"]] = pygame.image.load(
        bild_pfad).convert_alpha()
```

`pygame.image.load()` liest die PNG-Datei. `convert_alpha()` sorgt dafür, dass transparente Bereiche korrekt dargestellt werden. Wenn die Datei nicht existiert, bleibt das Bild für dieses Gebäude leer und `gebaeude_zeichnen()` verwendet automatisch die Farbe aus `"farbe"`.

### 8.5 Wie der Code das Bild zeichnet

In `gebaeude_zeichnen()` wird das Bild auf die aktuelle Gebäudekachel skaliert:

```python
bild = _bilder.get(typ_daten["name"])
if bild is not None:
    _fenster.blit(
        pygame.transform.smoothscale(bild, rect.size),
        rect,
    )
else:
    pygame.draw.rect(_fenster, typ_daten["farbe"], rect)
```

`_bilder.get()` verhindert einen Absturz, wenn kein Bild geladen wurde. `smoothscale()` passt die Größe an. `blit()` kopiert das Bild auf den Bildschirm. Der `else`-Teil ist ein Sicherheitsnetz und zeichnet ein farbiges Rechteck.

### 8.6 Häufige Bildfehler

| Problem | Ursache | Lösung |
|---|---|---|
| Gebäude bleibt farbiges Rechteck | Dateiname falsch oder Datei fehlt | `bild`-Wert und Dateinamen Zeichen für Zeichen vergleichen |
| Pygame meldet einen Ladefehler | Datei ist keine gültige PNG-Datei | Bild erneut als PNG exportieren |
| Weißer Kasten hinter dem Gebäude | Hintergrund nicht transparent | PNG mit Alpha-Kanal verwenden |
| Gebäude wirkt verzerrt | Bild ist nicht quadratisch | Quadratische Arbeitsfläche verwenden |
| Falsches Bild erscheint | Zwei Einträge haben denselben `name` | Eindeutige Gebäudenamen verwenden |
| Bild erscheint sehr klein | Gebäudezeichnung verwendet eine kleinere Stapelhälfte | Prüfen, ob Kompakte Maschinen aktiv ist und die Kachel zwei Gebäude enthält |

## 9. Kommentare im Code richtig schreiben

Kommentare erklären nicht nur, **was** eine Zeile schreibt, sondern auch, **warum** sie gebraucht wird. Ein schlechter Kommentar wiederholt nur den Code:

```python
faktor *= 1.10  # Faktor mal 1.10
```

Ein guter Kommentar erklärt die Spielidee:

```python
# Verbesserte Generatoren erhöhen nur die Energieproduktion um 10 Prozent.
# Der Bonus gilt für Reaktor und Fusionsreaktor, weil beide Energie erzeugen.
faktor *= 1.10
```

Für jede neue Forschungszeile solltet ihr mindestens drei Kommentare schreiben:

```python
# Schüleridee: Die Forschung verbessert die Holzproduktion.
# Die Prüfung steht im Produktionsmultiplikator, weil dort alle Prozentboni gesammelt werden.
# Der Bonus gilt nur für Holzfäller, also für Gebäudeindex 3.
if typ_index == 3 and forschung.ist_technologie_erforscht("meine_holzforschung"):
    faktor *= 1.10
```

Schreibt Kommentare vor allem an Übergängen zwischen Modulen. Ein zukünftiges Teammitglied muss erkennen können, warum eine Forschungs-ID aus `forschung.py` in `ressourcen.py` wieder auftaucht.

## 10. Testplan für eure eigene Erweiterung

| Testschritt | Erwartetes Ergebnis |
|---|---|
| Spiel startet mit `python3 main.py` | Kein Import- oder Bildladefehler |
| Forschungsmenü mit `F` öffnen | Neue Forschung erscheint mit Name, Kosten und Zeit |
| Forschung ohne Punkte starten | Meldung über fehlende Forschungspunkte |
| Forschung mit Voraussetzung starten | Forschung bleibt gesperrt, bis die Voraussetzung erforscht wurde |
| Forschung starten | Punkte werden abgezogen und Forschung läuft über Ticks |
| Labor ohne Personal prüfen | Forschungsfortschritt bleibt stehen |
| Forschung abschließen | Bonus oder Gebäude wird tatsächlich aktiviert |
| Gebäude im Baumenü prüfen | Kosten, Freischaltung und Personal stimmen |
| Eigenes Bild testen | Bild wird angezeigt, Fallback-Farbe funktioniert weiterhin |
| Selbsttest ausführen | `STUNDE11_TESTS_OK` wird ausgegeben |

Der Selbsttest wird im Projektordner so gestartet:

```bash
python3 test_stunde11.py
```

Für die grafische Kontrolle startet ihr:

```bash
python3 main.py
```

## 11. Gute Projektaufteilung für Schülerinnen und Schüler

Wenn mehrere Personen an der Erweiterung arbeiten, kann jede Person einen Forschungsbereich übernehmen. Eine Person arbeitet an Farmen, eine an Energie, eine an Handel und eine an Bildern. Trotzdem muss am Ende eine Person prüfen, ob alle Forschungs-IDs eindeutig sind und die Gebäudeindizes noch zusammenpassen.

Ändert immer nur ein System auf einmal. Erstellt zuerst die Forschungszeile, testet das Menü, programmiert danach die Wirkung und testet erneut. Wenn ihr gleichzeitig ID, Kosten, Gebäudeindex und Produktion ändert, ist später schwer zu erkennen, welcher Schritt einen Fehler verursacht hat.

> **Abschlussaufgabe:** Erfindet eine eigene Forschung, fügt sie in den Forschungsbaum ein, programmiert eine sichtbare Wirkung, erstellt ein eigenes PNG-Bild für ein passendes Gebäude und ergänzt mindestens einen Test in `test_stunde11.py`.

## 12. Referenzen innerhalb des Projekts

Die folgenden Dateien sind die technischen Quellen für dieses Handbuch:

[1]: ./forschung.py "Forschungsbaum und Forschungsfortschritt"
[2]: ./ressourcen.py "Wirtschaft, Personal, Speicher und Produktionsboni"
[3]: ./gebaeude.py "Gebäudetypen, Platzierung und Darstellung"
[4]: ./main.py "Spielschleife und Eingabeverarbeitung"
[5]: ./hud.py "Ressourcenleiste und Statusanzeigen"
[6]: ./menu.py "Baumenü"
[7]: ./handel.py "Handel und NPC-Angebote"
[8]: ./test_stunde11.py "Portabler Selbsttest"


## 13. Mehrkachel-Gebäude: die Universität als 2×3-Schulgebäude

Die Universität verwendet jetzt das angehängte Bild `schule_2x3_kacheln_64x96.png`. Das Bild ist 64×96 Pixel groß und hat deshalb genau das Seitenverhältnis 2:3. Im Spiel wird es auf zwei Kacheln Breite und drei Kacheln Höhe skaliert.

In `GEBAEUDE_TYPEN` stehen dafür neben dem Bildnamen die beiden Größenwerte:

```python
{
    "name": "Universitaet",
    "bild": "schule_2x3_kacheln_64x96.png",
    "breite": 2,
    "hoehe": 3,
    "farbe": (150, 200, 255),
    "kuerzel": "L",
    "taste": "8",
}
```

Die Kachel, auf die beim Bauen geklickt wird, ist immer die **linke obere Ecke**. Die Funktion `gebaeude_flaeche()` erzeugt daraus die sechs belegten Positionen. Bei `breite = 2` und `hoehe = 3` entstehen diese relativen Kacheln:

```text
(0,0) (1,0)
(0,1) (1,1)
(0,2) (1,2)
```

`kann_platzieren()` prüft alle sechs Positionen. Wenn auch nur eine Position bereits von einem anderen Gebäude belegt ist, wird der Bau abgelehnt. Ebenso wird geprüft, dass keine Position außerhalb der Karte liegt. Die Forschung „Kompakte Maschinen“ gilt nur für kleine 1×1-Gebäude; ein großes Gebäude darf niemals mit einem anderen Gebäude überlappen.

Die Zeichenfunktion berechnet die Gesamtgröße mit:

```python
voll_breite = breite * _kachel_groesse
voll_hoehe = hoehe * _kachel_groesse
```

Bei einer Kachelgröße von 48 Pixeln wird die Universität also 96×144 Pixel groß gezeichnet. Das Bild erscheint als ein zusammenhängendes Gebäude und nicht als sechs einzelne Bilder.

Der Abriss funktioniert ebenfalls über die gesamte Fläche. Ein Rechtsklick auf irgendeine der sechs Kacheln sucht das Gebäude, dessen Flächenliste diese Kachel enthält. Anschließend wird das Dictionary des Gebäudes genau einmal aus `liste_gebaeude` entfernt und die Rückerstattung genau einmal ausgezahlt.

### Eigenes Mehrkachel-Gebäude als Erweiterungsaufgabe

Für ein eigenes Gebäude mit drei Kacheln Breite und zwei Kacheln Höhe ergänzt ihr beispielsweise:

```python
{
    "name": "Forschungszentrum",
    "bild": "forschungszentrum_3x2.png",
    "farbe": (180, 160, 255),
    "kuerzel": "Z",
    "taste": "V",
    "breite": 3,
    "hoehe": 2,
}
```

Das Bild sollte möglichst ebenfalls ein Seitenverhältnis von 3:2 besitzen. Ihr müsst keine neue Kollisionfunktion schreiben. Die vorhandenen Funktionen verwenden automatisch die Werte `breite` und `hoehe`.


# Aktualisierung: Kategorien, vollständige Gebäude und neue Bilder

Dieser Abschnitt beschreibt den aktuellen Spielstand nach der nächsten Aufgabenbeschreibung. Er ersetzt ältere Hinweise, in denen die Zifferntasten noch einzelne Gebäude oder gleichzeitig die Spielgeschwindigkeit gesteuert haben.

## Neue Auswahlregel

Die Tasten `1` bis `9` wählen jetzt **Gebäudekategorien**. Mit `Pfeil links` und `Pfeil rechts` wechselt ihr innerhalb der gewählten Kategorie. Die Taste `0` wählt das zuletzt erfolgreich gebaute Gebäude erneut aus. Die Spielgeschwindigkeit wird unabhängig davon mit `+` und `-` verändert; die Leertaste pausiert weiterhin.

Die Kategorien stehen in `gebaeude.py` im Dictionary `GEBAEUDE_KATEGORIEN`. Ein Eintrag hat die Form:

```python
"4": {"name": "Veredelung / Fabriken", "typen": [5, 11, 12]},
```

Die Zahlen in `typen` sind Indizes. Sie verweisen auf dieselbe Position in `GEBAEUDE_TYPEN` und `GEBAEUDE_WIRTSCHAFT`. Die Funktion `kategorie_weiter()` nimmt die aktuelle Position und eine Richtung `-1` oder `+1` entgegen. Dadurch kann eine neue Kategorie beliebig viele Gebäude aufnehmen, ohne weitere feste Tastaturblöcke in `main.py` zu benötigen.

## Vollständige Gebäudeliste

Die aktuelle Version enthält 18 Gebäude: Basis, Reaktor, Farm, Holzfäller, Steinmetz, Marktplatz, Wohnhaus, Universität, Mine, Straße, Fusionsreaktor, Roboterfabrik, Stahlwerk, Gewächshaus, Lagerhaus, Wohnblock, Handelsposten und Koloniezentrum. Für jedes Gebäude existiert ein Eintrag in `gebaeude.py`, ein Wirtschaftseintrag an derselben Indexposition in `ressourcen.py` und eine PNG-Datei im Ordner `bilder/`.

Neue Produktionsketten sind Eisen → Stahl im Stahlwerk sowie zusätzliche Nahrung im Gewächshaus. Ein Lagerhaus erhöht nach der Forschung `lagerhaus_ausbau` die Speichergrenzen, ein Wohnblock erzeugt mehr Bevölkerung, ein Handelsposten unterstützt den Handel und ein Koloniezentrum gibt bei vorhandener Anlage einen kleinen globalen Produktionsbonus.

## So fügt ihr selbst ein Gebäude hinzu

Erstens ergänzt ihr in `gebaeude.py` einen Datensatz mit `name`, `bild`, `farbe`, `kuerzel`, `breite` und `hoehe`. Zweitens fügt ihr in `ressourcen.py` an exakt derselben Position `baukosten`, `produktion`, `verbrauch`, `personalbedarf`, `max_anzahl`, `freischaltung` und `grosse_anlage` ein. Drittens legt ihr die PNG-Datei mit exakt demselben Namen in `bilder/` ab. Viertens fügt ihr die neue Indexnummer in mindestens eine Kategorie ein. Fünftens legt ihr bei einem erforschbaren Gebäude eine Forschung in `forschung.py` an.

Beispiel für ein 1×1-Gebäude:

```python
# gebaeude.py
{"name": "Luftreiniger", "bild": "luftreiniger.png",
 "farbe": (120, 220, 180), "kuerzel": "L",
 "taste": "", "breite": 1, "hoehe": 1},

# ressourcen.py — gleiche Listenposition
{"baukosten": {"gold": 45, "energie": 10},
 "produktion": {"forschung": 1}, "verbrauch": {"energie": 1},
 "personalbedarf": 1, "max_anzahl": None,
 "freischaltung": {"typ": "forschung", "technologie": "luftreiniger"},
 "grosse_anlage": False},
```

## Große Gebäude

Für ein Mehrkachelgebäude werden `breite` und `hoehe` in `gebaeude.py` gesetzt. Die Universität besitzt `breite: 2` und `hoehe: 3`. `gebaeude_flaeche()` erzeugt daraus sechs Koordinaten. `kann_platzieren()` prüft Kartenrand und Überschneidungen; `gebaeude_abreissen()` findet das Gesamtgebäude, wenn auf irgendeine Teilkachel geklickt wird.

## Bilder

1×1-Gebäude verwenden 64×64-Pixel-PNGs. Das Schulbild der Universität verwendet 64×96 Pixel. Die genauen Dateinamen stehen in `BILDER_ANLEITUNG.md`. `labor.png` wird nicht mehr benutzt, weil die Universität die Laborfunktion übernommen hat. Wenn ein eigenes Bild fehlt, erscheint weiterhin die farbige Fallback-Fläche; für die fertige Abgabe muss aber jedes Gebäude eine passende Datei besitzen.

## Testauftrag

Führt nach jeder Änderung `python3 test_stunde11.py` aus. Prüft außerdem im Spiel: Kategorie wählen, mit links/rechts blättern, Baumenü öffnen, Bildvorschau kontrollieren, ein Gebäude bauen, Taste `0` testen, Geschwindigkeit mit `+/-` verändern und die Universität als 2×3-Fläche platzieren und wieder abreißen.
