"""Kleiner Selbsttest für die Stunde-11-Mechaniken.

Aufruf im Projektordner: python3 test_stunde11.py
"""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
import forschung
import ressourcen
import gebaeude
import handel

forschung.forschung_zuruecksetzen()
werte = {"gold": 200, "energie": 200, "holz": 100, "stein": 100,
         "bevoelkerung": 20, "nahrung": 100, "forschung": 500,
         "kohle": 100, "eisen": 100, "roboter": 0, "stahl": 100}

benoetigte_forschungen = {
    "effiziente_bautechnik", "kompakte_maschinen", "anpassende_architektur",
    "energieoptimierung", "verbesserte_generatoren", "energiespeicher",
    "fusionsreaktor", "mini_reaktor", "verbesserte_laborausruestung",
    "neue_instrumente", "quantencomputer", "einfache_robotik",
    "autonome_fabriken", "effizienter_aufbau", "tiefenbohrung",
    "verbesserte_aexte", "forstwirtschaft", "effizientere_holzverwendung",
    "verbesserte_marktstaende", "ressourcenhandel", "handel_mit_kolonien",
    "verbesserte_landwirtschaft", "hoeher_saettigende_nahrung", "terraforming",
    "stahlverarbeitung", "stahlverarbeitung_plus", "gewaechshausbau", "gewaechshaus_effizienz",
    "logistik_lager", "lagerhaus_ausbau", "wohnblockbau", "interkolonialhandel",
    "handelsrouten", "koloniezentrum",
}
assert benoetigte_forschungen.issubset({t["id"] for t in forschung.TECHNOLOGIEN})
assert len(gebaeude.GEBAEUDE_TYPEN) == len(ressourcen.GEBAEUDE_WIRTSCHAFT)
assert len(gebaeude.GEBAEUDE_TYPEN) >= 19
assert all(daten.get("bild") and os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bilder", daten["bild"]))
           for daten in gebaeude.GEBAEUDE_TYPEN)
assert all(index in range(len(gebaeude.GEBAEUDE_TYPEN))
           for kat in gebaeude.GEBAEUDE_KATEGORIEN.values()
           for index in kat["typen"])
assert gebaeude.kategorie_auswahl("5", 0) == 7
assert gebaeude.kategorie_weiter("4", 0, 1)[1] == 11

assert forschung.technologie_erforschen("effiziente_bautechnik", werte)
for _ in range(8):
    forschung.forschung_tick(werte)
assert forschung.ist_technologie_erforscht("effiziente_bautechnik")
assert ressourcen.baukosten_berechnen(1)["gold"] == 19

gebaeude_liste = []
gebaeude.gebaeude_platzieren(gebaeude_liste, 1, 2, 2)
gebaeude.gebaeude_platzieren(gebaeude_liste, 1, 3, 2)
werte["bevoelkerung"] = 1
ressourcen.ressourcen_produzieren(werte, gebaeude_liste)
assert sum(bool(g.get("arbeitet")) for g in gebaeude_liste) == 1

forschung._erforschte_technologien.update({"energiespeicher", "kompakte_maschinen"})
werte["energie"] = 999
ressourcen.ressourcen_begrenzen(werte)
assert werte["energie"] == ressourcen.maximaler_speicher("energie")
werte_vorher = werte["gold"]
ressourcen.ressourcen_produzieren(werte, [{"typ": 0}])
assert werte["gold"] > werte_vorher and werte["stahl"] <= ressourcen.maximaler_speicher("stahl")
assert gebaeude.kann_platzieren(gebaeude_liste, 1, 2, 2)
gebaeude.gebaeude_platzieren(gebaeude_liste, 1, 2, 2)
assert not gebaeude.kann_platzieren(gebaeude_liste, 1, 2, 2)

# Universität: 2 Kacheln breit und 3 Kacheln hoch.
uni_flaeche = set(gebaeude.gebaeude_flaeche(7, 10, 10))
assert uni_flaeche == {(10, 10), (11, 10), (10, 11), (11, 11), (10, 12), (11, 12)}
assert gebaeude.kann_platzieren(gebaeude_liste, 7, 10, 10, 60, 40)
gebaeude.gebaeude_platzieren(gebaeude_liste, 7, 10, 10, 60, 40)
assert not gebaeude.kann_platzieren(gebaeude_liste, 1, 11, 11, 60, 40)
assert not gebaeude.kann_platzieren(gebaeude_liste, 7, 59, 38, 60, 40)
assert gebaeude.gebaeude_abreissen(gebaeude_liste, 11, 12) == 7
assert all(g["typ"] != 7 for g in gebaeude_liste)

# Neue Forschungsfreischaltungen und Produktionsgebäude.
forschung._erforschte_technologien.update({
    "stahlverarbeitung", "gewaechshausbau", "logistik_lager", "wohnblockbau",
    "interkolonialhandel", "koloniezentrum", "lagerhaus_ausbau"
})
assert ressourcen.ist_freigeschaltet(werte, 12)
assert ressourcen.ist_freigeschaltet(werte, 13)
assert ressourcen.ist_freigeschaltet(werte, 14)
assert ressourcen.ist_freigeschaltet(werte, 15)
assert ressourcen.ist_freigeschaltet(werte, 16)
assert ressourcen.ist_freigeschaltet(werte, 17)
ressourcen.ressourcen_produzieren(werte, [{"typ": 14}])
assert ressourcen.maximaler_speicher("stahl") >= 225

forschung._erforschte_technologien.add("terraforming")
karte = [[0, 2], [3, 0]]
ok, _ = ressourcen.terraformieren(werte, karte, 1, 0)
assert ok and karte[0][1] == 1

forschung._erforschte_technologien.add("ressourcenhandel")
handel.handel_tick(werte, [{"typ": 5}])
werte["holz"], werte["stein"] = 10, 50
assert handel.ressourcen_tauschen(werte, "holz", "stein")
assert werte["holz"] == 8 and werte["stein"] == 51

pygame.quit()
print("STUNDE11_TESTS_OK")
