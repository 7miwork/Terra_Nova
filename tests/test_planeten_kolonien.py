"""Tests fuer Planeten, Kolonien und die Spielstand-Version 2 (Wunschliste)."""

import json
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
pygame.display.set_mode((1000, 720))

import forschung
import kolonien
import main
import planeten
import ressourcen
import spielstand


# ── 1. Planeten-Datenbank ────────────────────────────────────────────────────
assert len(planeten.PLANETEN) == 6
for eintrag in planeten.PLANETEN:
    for feld in planeten.PFLICHTFELDER:
        assert feld in eintrag, (eintrag["id"], feld)
assert planeten.spielbare_ids() == ["erde", "mond", "mars"]
assert planeten.ist_spielbar("erde") and planeten.ist_spielbar("mars")
assert not planeten.ist_spielbar("vulkan") and not planeten.ist_spielbar("eis")
assert planeten.name("mond") == "Mond"
assert planeten.farbe("vulkan") == (240, 95, 70)
assert planeten.name("gibt_es_nicht") == "gibt_es_nicht"   # rohe ID zeigen
print("Planeten: 6 Eintraege, alle Pflichtfelder, Phase 1 = Erde/Mond/Mars")


# ── 2. Kartenparameter je Planet ─────────────────────────────────────────────
assert planeten.karten_parameter("erde") == planeten.KARTEN_STANDARD
assert planeten.karten_parameter("mond") == {
    "gras_flaechen": 4, "gestein_flaechen": 9, "sand_flaechen": 3}
# Unbekannter Planet behaelt die Originalwerte (8/5/6).
assert planeten.karten_parameter("gibt_es_nicht") == planeten.KARTEN_STANDARD
for planet_id in planeten.alle_ids():
    werte = planeten.karten_parameter(planet_id)
    assert set(werte) == set(planeten.KARTEN_STANDARD)
    assert all(isinstance(w, int) and w > 0 for w in werte.values())
    assert sum(werte.values()) <= 24, planet_id   # nicht mehr als ~1/5 der Karte
print("Kartenparameter: Erde 8/5/6, Mond 4/9/3, jeder Planet eigene Flaechen")


# ── 3. Startressourcen je Planet ─────────────────────────────────────────────
erde = main._neue_ressourcen("erde")
assert erde["gold"] == 100 and erde["energie"] == 50 and erde["holz"] == 30
mond = main._neue_ressourcen("mond")
assert mond["gold"] == 80 and mond["energie"] == 40 and mond["holz"] == 20
assert mond["stein"] == 15 and mond["nahrung"] == 40
assert mond["forschung"] == 0          # Grundwert bleibt erhalten
mars = main._neue_ressourcen("mars")
assert mars["gold"] == 90 and mars["energie"] == 30 and mars["stein"] == 25
print("Startressourcen: Erde 100 Gold, Mond 80, Mars 90 (Rest wie Grundwerte)")


# ── 4. Rohstoff-Faktoren und Gruendungskosten ────────────────────────────────
assert planeten.rohstoff_faktor("mars", "eisen") == 2.5
assert planeten.rohstoff_faktor("mond", "forschung") == 1.5
assert planeten.rohstoff_faktor("erde", "eisen") == 1.0     # kein Bonus
assert planeten.rohstoff_faktor("gibt_es_nicht", "gold") == 1.0
faktoren = planeten.rohstoffe("mars")
faktoren["eisen"] = 99                  # Kopie aendern ...
assert planeten.rohstoff_faktor("mars", "eisen") == 2.5     # ... Original heil
kosten = planeten.gruendungskosten()
assert kosten == {"gold": 120, "energie": 60, "holz": 40, "stein": 40}
assert planeten.gruendungskosten("vulkan") == kosten        # Phase 2 gleich
assert planeten.naechster_freier_planet([]) == "erde"
assert planeten.naechster_freier_planet(["erde"]) == "mond"
assert planeten.naechster_freier_planet(["erde", "mond"]) == "mars"
assert planeten.naechster_freier_planet(
    ["erde", "mond", "mars"]) is None                        # alles voll
assert planeten.naechster_freier_planet(["alien"]) == "erde"  # gesperrt zaehlt nicht
print("Rohstoffe: Mars 2,5 x Eisen, Mond 1,5 x Forschung, Kosten 120/60/40/40")


# ── 5. Faktoren im Produktionsrechner (ressourcen.py) ────────────────────────
ressourcen.zustand_importieren({})
forschung.forschung_zuruecksetzen()
ressourcen.planeten_faktoren_setzen(planeten.rohstoffe("mars"))
assert ressourcen.planeten_faktor("eisen") == 2.5
assert ressourcen.planeten_faktor("gold") == 1.0
assert ressourcen._produktion_multiplikator(0, "eisen") == 2.5
assert ressourcen._produktion_multiplikator(0, "energie") == 0.85
assert ressourcen._produktion_multiplikator(0, "gold") == 1.0
ressourcen.planeten_faktoren_setzen(planeten.rohstoffe("mond"))
assert ressourcen._produktion_multiplikator(7, "forschung") == 1.5
# Kaputte Werte aus einem defekten Spielstand werden ignoriert.
ressourcen.planeten_faktoren_setzen({"eisen": -1, "gold": "quatsch", "holz": "2"})
assert ressourcen.planeten_faktor("eisen") == 1.0
assert ressourcen.planeten_faktor("gold") == 1.0
assert ressourcen.planeten_faktor("holz") == 2.0
# Export/Import-Rundlauf (Spielstand traegt die Faktoren mit).
ressourcen.planeten_faktoren_setzen(planeten.rohstoffe("mars"))
stand = ressourcen.zustand_exportieren()
assert stand["planeten"] == {"eisen": 2.5, "kohle": 1.5, "energie": 0.85}
ressourcen.zustand_importieren({})
assert ressourcen.planeten_faktor("eisen") == 1.0
ressourcen.zustand_importieren(stand)
assert ressourcen.planeten_faktor("eisen") == 2.5
print("Produktion: Planetenfaktor wirkt im Multiplikator und ueberlebt Speichern")


# ── 6. Karte des Planeten wird nach Parametern gebaut ────────────────────────
main.karte_generieren("mond")
assert len(main.karten_daten) == main.KARTE_HOEHE
assert all(len(zeile) == main.KARTE_BREITE for zeile in main.karten_daten)
assert set(sum(main.karten_daten, [])) <= {0, 1, 2, 3, 4}
print("Karte: mond_kacheln in 60x40, Kacheltypen gueltig")


# ── 7. Kolonien aufbauen und wechseln (kolonien.py + main) ──────────────────
kolonien.hauptmodul_setzen(main, main.KARTE_BREITE, main.KARTE_HOEHE)
main.neues_spiel_starten()                       # frische Partie auf der Erde
assert kolonien.anzahl() == 1
assert kolonien.aktuelle_id() == "kolonie_1"
assert kolonien.aktueller_planet() == "erde"
assert kolonien.naechster_freier_planet() == "mond"

# Zustand der Erde markieren, damit wir den Wechsel erkennen.
main.ressourcen_dict["gold"] = 777
main.kamera_x = 123
main.liste_gebaeude.append({"typ": 1, "x": 2, "y": 2, "arbeitet": True})

# Mond gruenden - Ablauf wie main.kolonie_gruenden, nur ohne UI:
kolonien.stand_merken()
main.neues_spiel_starten(planet_id="mond", partei_neustart=False)
assert kolonien.gruenden("mond") == "kolonie_2"
assert kolonien.aktuelle_id() == "kolonie_2"
assert kolonien.aktueller_planet() == "mond"
assert main.ressourcen_dict["gold"] == 80              # Mond-Startvorrat
assert ressourcen.planeten_faktor("forschung") == 1.5  # Mond-Bonus aktiv
assert main.liste_gebaeude == []                       # frische Welt

# Zurueck zur Erde: alter Zustand muss wieder da sein.
assert kolonien.wechseln("kolonie_1")
assert main.ressourcen_dict["gold"] == 777
assert main.kamera_x == 123
assert len(main.liste_gebaeude) == 1
assert ressourcen.planeten_faktor("forschung") == 1.0  # ohne Mond-Bonus

# Guards: besetzte und gesperrte Planeten kann man nicht doppelt belegen.
assert kolonien.gruenden("erde") is None               # schon unsere Kolonie
assert kolonien.gruenden("vulkan") is None             # Phase 2, noch gesperrt
assert kolonien.anzahl() == 2
assert kolonien.naechster_freier_planet() == "mars"    # Mars ist noch frei
assert "Kolonie 1 von 2" in kolonien.aktuelle_beschreibung()
assert "Erde" in kolonien.aktuelle_beschreibung()

assert kolonien.wechseln("kolonie_2")      # zum Mond
assert main.ressourcen_dict["gold"] == 80
assert ressourcen.planeten_faktor("forschung") == 1.5
assert kolonien.wechseln("kolonie_1")      # zurueck zur Erde
assert main.ressourcen_dict["gold"] == 777
assert ressourcen.planeten_faktor("eisen") == 1.0
assert kolonien.wechseln("kolonie_2")      # wieder zum Mond (fuer Abschnitt 8)
assert main.ressourcen_dict["gold"] == 80
print("Kolonien: Erde+Mond belegt, Wechsel rettet Zustand, Mars noch frei")


# ── 8. UI-Funktionen aus main.py (Pause: K / G) ─────────────────────────────
# Kosten grosszuegig verfuegbar machen - sie werden von der ALTEN Kolonie
# abgezogen, bevor die neue Welt gebaut wird.
kosten = planeten.gruendungskosten()
for name, menge in kosten.items():
    main.ressourcen_dict[name] = menge + 500
alt = kolonien.aktuelle_id()                # kolonie_2 (Mond)
assert main.kolonie_gruenden()              # G: gruendet auf dem Mars
assert kolonien.anzahl() == 3
assert kolonien.aktuelle_id() == "kolonie_3"
assert kolonien.aktueller_planet() == "mars"
assert main.ressourcen_dict["gold"] == 90   # Mars-Start, nicht 500+120
assert ressourcen.planeten_faktor("eisen") == 2.5
assert "Kolonie 3 von 3" in kolonien.aktuelle_beschreibung()
# Alte Kolonie: die Gruendungskosten wurden dort abgezogen.
assert kolonien.wechseln("kolonie_2")
for name, menge in kosten.items():
    assert main.ressourcen_dict[name] == 500, name
assert kolonien.wechseln("kolonie_3")

# Alle Planeten voll: G meldet und aendert nichts.
anzahl_vorher = kolonien.anzahl()
assert not main.kolonie_gruenden()
assert kolonien.anzahl() == anzahl_vorher
assert kolonien.naechster_freier_planet() is None

# K wechselt zur naechsten Kolonie und zurueck.
weg = kolonien.aktuelle_id()
assert main.kolonie_naechste_wechseln()
assert kolonien.aktuelle_id() != weg
zurueck = kolonien.aktuelle_id()
assert main.kolonie_naechste_wechseln()
assert kolonien.aktuelle_id() != zurueck
print("UI: G gruendet Mars (Kosten von alter Kolonie), K wechselt hin-und-her")


# ── 9. Spielstand: Kolonien mitspeichern (Version 2) ────────────────────────
daten = kolonien.zustand_fuer_spielstand()
json.dumps(daten)                        # muss JSON-faehig sein
assert daten["zaehler"] == 3
assert daten["aktuell"] == "kolonie_2"
assert daten["planeten"] == {"kolonie_1": "erde",
                             "kolonie_2": "mond",
                             "kolonie_3": "mars"}
assert "kolonie_2" not in daten["liste"]   # aktive steckt in den Feldern
assert daten["liste"]["kolonie_1"]["planet"] == "erde"
assert isinstance(daten["liste"]["kolonie_1"]["stand"], dict)
assert daten["liste"]["kolonie_1"]["stand"]["ressourcen_dict"]["gold"] == 777

# Frisches Verzeichnis, dann Rueckspielung des JSON-Rundlaufs:
kolonien.zuruecksetzen("erde")
assert kolonien.anzahl() == 1
assert kolonien.zustand_uebernehmen(json.loads(json.dumps(daten)))
assert kolonien.anzahl() == 3
assert kolonien.aktuelle_id() == "kolonie_2"
assert kolonien.planet_von("kolonie_2") == "mond"
assert kolonien.planet_von("kolonie_3") == "mars"

# Defekte Daten werden verworfen (1x1-Karte passt nicht zu 60x40):
kaputt = {"planeten": {"kolonie_1": "erde"},
          "liste": {"kolonie_1": {"planet": "erde",
                                  "stand": {"karten_daten": [[1]],
                                            "liste_gebaeude": [],
                                            "ressourcen_dict": {}}}}}
assert not kolonien.zustand_uebernehmen(kaputt)
assert kolonien.anzahl() == 3               # Registry unveraendert

# Speichern/Laden mit drei Kolonien (eigene Datei, echtes Projekt bleibt heil):
original_datei = spielstand.DATEI
spielstand.DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "_spielstand_planeten_test.json")
try:
    ok, meldung = spielstand.speichern(
        main.karten_daten, main.sterne_liste, main.ressourcen_dict,
        main.liste_gebaeude, main.kamera_x, main.kamera_y, main.tick_zaehler,
        main.spiel_geschwindigkeit, main._auswahl_kategorie,
        main._auswahl_position, main.gebaeude_auswahl, main._letztes_gebaeude,
        main.spiel_status,
        {"nahrung": main._null_nahrung_ticks, "energie": main._null_energie_ticks},
        main._regel_auswahl, kolonien_daten=kolonien.zustand_fuer_spielstand())
    assert ok, meldung
    geladen, meldung = spielstand.laden()
    assert geladen is not None, meldung
    assert geladen["version"] == 2
    assert geladen["kolonien"]["zaehler"] == 3
    assert geladen["kolonien"]["aktuell"] == "kolonie_2"
    assert geladen["kolonien"]["planeten"] == {"kolonie_1": "erde",
                                               "kolonie_2": "mond",
                                               "kolonie_3": "mars"}
    assert "kolonie_2" not in geladen["kolonien"]["liste"]

    # main.spielstand_laden spielt auch die Kolonie-Liste zurueck:
    ok, meldung = main.spielstand_laden()
    assert ok, meldung
    assert kolonien.anzahl() == 3
    assert kolonien.aktuelle_id() == "kolonie_2"
    assert kolonien.planet_von("kolonie_3") == "mars"

    # Ohne kolonien_daten schreibt speichern den Einzelkolonie-Default:
    ok, meldung = spielstand.speichern(
        main.karten_daten, main.sterne_liste, main.ressourcen_dict,
        main.liste_gebaeude, 0, 0, 0, 1, "1", 0, 0, 0, "spiel",
        {"nahrung": 0, "energie": 0}, "standard")
    assert ok, meldung
    geladen, meldung = spielstand.laden()
    assert geladen is not None, meldung
    assert geladen["kolonien"] == {"zaehler": 1, "aktuell": "kolonie_1",
                                   "planeten": {"kolonie_1": "erde"},
                                   "liste": {}}

    # Version-1-Spielstand waechst beim Laden automatisch auf Version 2:
    alt = {"version": 1,
           "karten_daten": [[0] * main.KARTE_BREITE
                            for _ in range(main.KARTE_HOEHE)],
           "ressourcen": {"gold": 42, "energie": 10},
           "gebaeude": [{"typ": 1, "x": 1, "y": 1}],
           "kamera": {"x": 0, "y": 0},
           "auswahl": {"kategorie": "1", "position": 0,
                       "gebaeude": 0, "letztes_gebaeude": 0},
           "tick_zaehler": 0, "spiel_geschwindigkeit": 1,
           "spielstatus": "spiel", "regel_auswahl": "standard"}
    with open(spielstand.DATEI, "w", encoding="utf-8") as datei:
        json.dump(alt, datei)
    ok, meldung = main.spielstand_laden()
    assert ok, meldung
    assert main.ressourcen_dict["gold"] == 42
    assert kolonien.anzahl() == 1           # alte Partie = genau eine Kolonie
    assert kolonien.aktuelle_id() == "kolonie_1"
    assert kolonien.aktueller_planet() == "erde"
finally:
    if os.path.exists(spielstand.DATEI):
        os.remove(spielstand.DATEI)
    spielstand.DATEI = original_datei
print("Spielstand: v2 traegt alle Kolonien, v1 waechst automatisch nach")
print("PLANETEN_KOLONIEN_TESTS_OK")

