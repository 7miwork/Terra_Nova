### Verbesserungsvorschlaege (Stunde 9 — alle 6 umgesetzt ✅):

- [x] Gebaeude abreissen koennen (Kostenrueckerstattung)
- [x] Bei der Auswahl zusaetzliche Informationen
- [x] Extra Taste fuer Baumenu
- [x] Pop-Up menu beim rohstoff menu sehen koennen
- [x] wenn zu wenig rohstoffe fuers bauen sollte es eine nachricht geben
- [x] stufenweise freischaltung durch ressourcen anzahl/forschung

---

### Neue Vorschlaege fuer die naechste Stunde:

#### Balancing (Schuelerwunschliste) — alle umgesetzt ✅

- [x] Fusionsreaktor schwächer: 25 → **20 Energie**
- [x] Gewächshaus schwächer: 8 → **6 Nahrung** (wird später zur Überschussressource)
- [x] Marktplatz schwächer: 12 → **10 Gold**
- [x] Handel teurer: Tausch von **2:1 auf 3:1** (Konstante `TAUSCH_VERHALTNIS`),
      damit der Handel nicht wie eine eigene Produktionskette wirkt

#### Zufallsereignisse (Vorschläge zur Erweiterung) — alle umgesetzt ✅

- [x] **Systemausfall**: 30 % weniger Energie für 3 Minuten (180 Ticks).
      Reparatur gegen **100 Gold** behebt ihn sofort (Taste **R**).
- [x] **Unbekanntes Raumschiff**: bis zu **75 Einheiten je Ressource** einsetzen —
      50 % Chance auf das Doppelte, 50 % auf den Totalverlust.
- [x] **Meteoritenschauer**: 10 zufällige Gebäude treffen, 3 Minuten lang nur
      noch 20 % Produktion (80 % weniger).

#### Achievements — drei neue Ziele ✅

- [x] 100 Gebäude gebaut (zählt über **alle** Partien)
- [x] 1000 Forschungspunkte erzeugt (über alle Partien)
- [x] erste Stahlproduktion

#### Statistik im Anfangsmenü ✅

- [x] Hauptmenü → „Gesamtstatistik“ (Taste **T**): gespielte, gewonnene und
      verlorene Partien, Spielzeit, Gebäude, Forschungspunkte, Handelsaktionen,
      Technologien, größte Kolonie, Achievements und die Häufigkeit der
      Zufallsereignisse — jeweils „insgesamt“ und „diese Partie“.
      Liegt in `statistik.json` und steht nicht im Repository.


### Umgesetzt in der aktuellen Version

- [x] Zifferntasten 1–9 als Gebäudekategorien statt fester Einzelgebäude
- [x] Unterauswahl mit Pfeil links/rechts und Bildvorschau im HUD
- [x] Taste 0 für das zuletzt gebaute Gebäude
- [x] Spielgeschwindigkeit mit `+` und `-` ohne Konflikt mit den Kategorien
- [x] 18 Gebäude mit parallelen Wirtschafts- und Bilddaten
- [x] Basis-Grundproduktion von Gold, Energie, Holz und Stein
- [x] Stahl als Ressource und Stahlwerk als Verarbeitungskette
- [x] Gewächshaus, Lagerhaus, Wohnblock, Handelsposten und Koloniezentrum
- [x] Vollständige PNG-Dateiliste; `labor.png` entfernt, Universität übernimmt die Laborfunktion
- [x] Universität als 2×3-Gebäude mit dem Schulbild
- [x] Selbsttest für Gebäude, Kategorien, Bilder, Personal, Speicher, Handel und Mehrkachelflächen

### Noch mögliche Projektideen

- Speichern und Laden von Spielständen
- Sieg- und Niederlagebedingungen
- Ein echtes Waldobjekt pro Karte statt eines Waldvorrats direkt am Holzfäller
- Weitere Produktionsketten und individuelle Schülerbilder
