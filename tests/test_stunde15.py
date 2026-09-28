"""Integrationstest für die beiden von Schülern erstellten Gebäude."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

pygame.init()
import achievements
import forschung
import gebaeude
import handel
import hud
import missionen
import ressourcen

fenster = pygame.display.set_mode((1000, 700))
forschung.forschung_initialisieren(fenster)
gebaeude.gebaeude_initialisieren(fenster, 48)
hud.hud_initialisieren(fenster)
achievements.initialisieren(fenster)
missionen.initialisieren(fenster)
handel.handel_initialisieren(fenster)

# Die beiden Grafiken liegen im Projekt und sind den neuen Typnummern
# zugeordnet. Die bisherigen Gebäudetypen bleiben davor unverändert.
bilder_ordner = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bilder")
assert len(gebaeude.GEBAEUDE_TYPEN) == len(ressourcen.GEBAEUDE_WIRTSCHAFT)
assert gebaeude.GEBAEUDE_TYPEN[19]["name"] == "Park"
assert gebaeude.GEBAEUDE_TYPEN[20]["name"] == "Solarreaktor"
assert os.path.exists(os.path.join(bilder_ordner, "park_32x32.png"))
assert os.path.exists(os.path.join(bilder_ordner, "solareaktor_32x32.png"))
assert 19 in gebaeude.GEBAEUDE_KATEGORIEN["9"]["typen"]
assert 20 in gebaeude.GEBAEUDE_KATEGORIEN["6"]["typen"]

# Parks senken den Nahrungsverbrauch, ohne Personal zu benötigen. Der Effekt
# ist pro Park 5 Prozentpunkte und wird bei 30 Prozent gedeckelt.
assert ressourcen.park_nahrungsfaktor([]) == 1.0
assert ressourcen.park_nahrungsfaktor([{"typ": 19}]) == 0.95
assert ressourcen.park_nahrungsfaktor([{"typ": 19}] * 10) == 0.70

werte = {
    "gold": 500, "energie": 100, "holz": 100, "stein": 100,
    "bevoelkerung": 20, "nahrung": 100, "forschung": 0,
    "kohle": 0, "eisen": 0, "roboter": 0, "stahl": 0,
}
ressourcen.ressourcen_produzieren(werte, [{"typ": 19}])
assert abs(werte["nahrung"] - 99.05) < 0.001

# Der Solarreaktor produziert Energie, verbraucht aber keine Kohle.
werte["energie"] = 0
werte["nahrung"] = 100
werte["kohle"] = 0
ressourcen.ressourcen_produzieren(
    werte, [{"typ": 20, "arbeitet": False}])
assert werte["energie"] == 10
assert werte["kohle"] == 0

# Beide Gebäude erzeugen eigene Missions- und Achievement-Fortschritte.
missionen.zustand_zuruecksetzen()
neu = missionen.pruefen({"gebaeude_typ_19": 1, "gebaeude_typ_20": 1})
assert "gruene_oase" in neu
assert "sonnenkraft" in neu

achievements.zustand_zuruecksetzen()
neu = achievements.pruefen(
    werte,
    [{"typ": 19}, {"typ": 20}],
    [[0]],
)
assert "gruene_oase" in neu
assert "solarpionier" in neu

pygame.quit()
print("STUNDE15_TESTS_OK")
