# Stunde 11 – Forschungs- und Spielsysteme

## Ziel

Die Forschungswege der Schüler werden als vollständiger Technologiebaum umgesetzt. Jede Technologie verändert mindestens eine sichtbare Spielregel: Baukosten, Platzbedarf, Produktion, Verbrauch, Forschung, Personal, Energie, Speicher, Handel oder Kartenboden.

## Grundmodell der Wirtschaft

Ein Wirtschaftstick entspricht weiterhin einer Spielsekunde. Gebäude arbeiten nur, wenn ihr Personalbedarf gedeckt ist und alle Verbrauchsressourcen vorhanden sind. Bewohner und Roboter bilden gemeinsam das verfügbare Personal. Wohnhäuser erzeugen Bevölkerung; Roboterfabriken erzeugen nach der Robotik-Forschung Roboter.

| System | Stunde-11-Regel |
|---|---|
| Personal | Jedes Produktionsgebäude hat einen Personalbedarf. Nicht besetzte Gebäude produzieren in diesem Tick nichts. |
| Robotik | Einfache Robotik schaltet Roboterfabriken frei. Roboter zählen als zusätzliche Arbeitskräfte. |
| Autonome Fabriken | Produktionsgebäude benötigen 30 % weniger Personal. |
| Speicher | Ressourcen besitzen Obergrenzen. Energiespeicher erhöht das Energie-Limit um 25 %. |
| Nahrung | Nahrung wird global mit 0,05 pro Bewohner und Tick verbraucht. Höher sättigende Nahrung reduziert diesen Verbrauch um 5 %. |
| Forschung | Eine Forschung kostet Forschungspunkte und läuft anschließend über mehrere Ticks. Laborausrüstung (+10 %) und Quantencomputer (+40 %) beschleunigen den Fortschritt. |
| Platz | Vor Kompakte Maschinen gilt höchstens ein Gebäude pro Kachel. Danach können Produktionsgebäude eine zweite kompakte Belegung derselben Kachel nutzen. |

## Technologiebaum

| Bereich | Technologie | Wirkung |
|---|---|---|
| Gebäude | Effiziente Bautechnik | Alle Baukosten 5 % günstiger. |
| Gebäude | Kompakte Maschinen | Eine Kachel kann ein zweites Produktionsgebäude aufnehmen. |
| Gebäude | Anpassende Architektur | Automatischer Effizienzbonus, abhängig vom funktionierenden Betrieb; maximal +15 %. |
| Energie | Energieoptimierung | Energieverbrauch aller Gebäude −5 %. |
| Energie | Verbesserte Generatoren | Energieproduktion +10 %. |
| Energie | Energiespeicher | Maximale Energie +25 %. |
| Energie | Fusionsreaktor | Schaltet ein Gebäude mit hoher Energieproduktion frei. |
| Energie | Mini-Reaktor | Geeignete große Gebäude erzeugen zusätzlich 1 Energie pro Tick. |
| Forschung | Verbesserte Laborausrüstung | Forschungsgeschwindigkeit +10 %. |
| Forschung | Neue Geräte und Instrumente | Forschungspunkte aus Laboren +5 %. |
| Forschung | Quantencomputer | Forschungsgeschwindigkeit +40 %. |
| Automatisierung | Einfache Robotik | Schaltet Roboter und die Roboterfabrik frei. |
| Automatisierung | Autonome Fabriken | Produktionsgebäude benötigen 30 % weniger Personal. |
| Steinmetz | Effizienter Aufbau | Steinproduktion +10 %. |
| Steinmetz | Tiefenbohrung | Neue Kohle-/Eisenvorkommen werden nutzbar; Minen erhalten bessere Ausbeute. |
| Holzfäller | Verbesserte Äxte | Holzproduktion +10 %. |
| Holzfäller | Forstwirtschaft | Wälder können erschöpfen und wachsen anschließend wieder nach; Nachwachsen wird beschleunigt. |
| Holzfäller | Effizientere Holzverwendung | Holzanteil aller Baukosten −5 %. |
| Marktplatz | Verbesserte Marktstände | Goldproduktion von Marktplätzen +10 %. |
| Marktplatz | Ressourcenhandel | Marktplätze tauschen Ressourcen im Kurs 2:1. |
| Marktplatz | Handel mit anderen Kolonien | Zeitweise NPC-Angebote erscheinen und können angenommen oder abgelehnt werden. |
| Farm | Verbesserte Landwirtschaft | Nahrung aus Farmen +10 %. |
| Farm | Höher sättigende Nahrung | Nahrungsverbrauch der Bewohner −5 %. |
| Farm | Terraforming für Farmbau | Jede freie Kachel kann gegen Ressourcen in fruchtbaren Boden umgewandelt werden. |

## Bedienung der neuen Systeme

| Eingabe | Funktion |
|---|---|
| F | Forschungsmenü öffnen oder schließen. |
| F1–F12 | Sichtbare Forschung im Menü auswählen und starten. |
| Bild auf/Bild ab oder Mausrad | Im Forschungsmenü scrollen. |
| E | Handelsmenü öffnen oder schließen. |
| Q/W/R/T/Y/U | Vordefinierten 2:1-Ressourcentausch ausführen. |
| Z | Terraforming-Modus an- oder ausschalten, wenn erforscht. |
| G | Fusionsreaktor auswählen. |
| T | Roboterfabrik auswählen. |
| J/K | NPC-Angebot annehmen oder ablehnen, wenn ein Angebot aktiv ist. |

## Balancing-Entscheidungen

Forschungen werden in drei Stufen angeordnet. Grundtechnologien kosten wenig Forschungspunkte und benötigen kurze Forschungszeiten. Ausbau- und Produktionsverbesserungen bilden die mittlere Stufe. Anpassende Architektur, Quantencomputer und autonome Fabriken sind Endgame-Technologien mit höheren Kosten, mehreren Voraussetzungen und längerer Forschungszeit.

Die Spielwelt bleibt mit den bisherigen Gebäuden startbar. Die neuen Systeme sind additive Erweiterungen: Ohne Forschung funktionieren die bisherigen Gebäude weiter, jedoch mit Personalbedarf und begrenzten Speichern. Die Ausgangsbevölkerung ist deshalb ausreichend groß, um eine kleine Anfangswirtschaft zu betreiben, aber nicht groß genug, um unbegrenzt viele Gebäude gleichzeitig zu besetzen.


## Universität als Mehrkachel-Gebäude

Die Universität verwendet das angehängte Schulbild `schule_2x3_kacheln_64x96.png`. Sie ist zwei Kacheln breit und drei Kacheln hoch. Der Bauklick markiert die linke obere Ecke; alle sechs Kacheln werden als eine gemeinsame Gebäudefläche reserviert. Große Gebäude dürfen nicht mit anderen Gebäuden überlappen. Ein Rechtsklick auf jede beliebige belegte Universitätskachel reißt das gesamte Gebäude einmal ab und zahlt die Rückerstattung einmal aus.


# Verbindliche Aktualisierung: Gebäudekategorien und vollständige Assets

## Gebäudekategorien

Die Tasten `1` bis `9` wählen Kategorien. Die Auswahl innerhalb einer Kategorie erfolgt mit Pfeil links/rechts. Die Taste `0` wählt das zuletzt erfolgreich gebaute Gebäude aus. Die Geschwindigkeitssteuerung ist deshalb von den Zifferntasten getrennt und verwendet `+` und `-`; die Leertaste pausiert.

```python
GEBAEUDE_KATEGORIEN = {
    "1": {"name": "Basis / Kolonie-Zentrum", "typen": [0]},
    "2": {"name": "Erzeuger / Rohstoffe", "typen": [1, 2, 3, 4, 8, 13]},
    "3": {"name": "Wohngebäude", "typen": [6, 15]},
    "4": {"name": "Veredelung / Fabriken", "typen": [5, 11, 12]},
    "5": {"name": "Forschung / Bildung", "typen": [7]},
    "6": {"name": "Energie", "typen": [1, 10]},
    "7": {"name": "Infrastruktur", "typen": [9, 14]},
    "8": {"name": "Handel", "typen": [5, 16]},
    "9": {"name": "Spezial / Prestige", "typen": [17]},
}
```

Ein Gebäude darf in mehreren Kategorien vorkommen. Die Kategorien enthalten nur Indexverweise; die Gebäudedaten werden nicht dupliziert.

## 18 Gebäude und parallele Listen

`GEBAEUDE_TYPEN` in `gebaeude.py` und `GEBAEUDE_WIRTSCHAFT` in `ressourcen.py` müssen beide genau 18 Einträge besitzen. Die gemeinsame Reihenfolge lautet: Basis, Reaktor, Farm, Holzfäller, Steinmetz, Marktplatz, Wohnhaus, Universität, Mine, Straße, Fusionsreaktor, Roboterfabrik, Stahlwerk, Gewächshaus, Lagerhaus, Wohnblock, Handelsposten, Koloniezentrum.

Die neue Ressource `stahl` besitzt ein eigenes Speicherlimit. Das Stahlwerk verbraucht Eisen und Kohle und produziert Stahl. Das Gewächshaus produziert zusätzliche Nahrung. Das Lagerhaus wird erst durch `lagerhaus_ausbau` zum Speicherbonus. Der Wohnblock erzeugt mehr Bevölkerung als das Wohnhaus. Ein Handelsposten zählt für die Handelslogik wie ein Marktplatz. Das Koloniezentrum ist auf ein Gebäude begrenzt und gibt bei vorhandener Anlage einen globalen Produktionsbonus.

## Bildpflicht

Jedes der 18 Gebäude besitzt einen konkreten Wert `bild` und eine vorhandene PNG-Datei im Ordner `bilder/`. Die 1×1-Gebäude verwenden 64×64 Pixel. Die Universität verwendet das angehängte Schulbild mit 64×96 Pixeln und `breite: 2`, `hoehe: 3`. `labor.png` ist kein aktives Asset mehr.

## Neue Forschungsfreischaltungen

Die Ergänzungen im Forschungsbaum sind `stahlverarbeitung`, `stahlverarbeitung_plus`, `gewaechshausbau`, `gewaechshaus_effizienz`, `logistik_lager`, `lagerhaus_ausbau`, `wohnblockbau`, `interkolonialhandel`, `handelsrouten` und `koloniezentrum`. Jede Freischaltung verweist auf den passenden Gebäudeindex. Der Selbsttest prüft alle IDs und alle Bilddateien.
