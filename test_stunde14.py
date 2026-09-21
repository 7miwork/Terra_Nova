"""Tests für Forschungshinweise und den neuen Eisen-Forschungspfad."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(__file__))

import pygame

pygame.init()
import forschung
import ressourcen
import gebaeude
import hud

fenster = pygame.display.set_mode((1000, 700))
forschung.forschung_initialisieren(fenster)
hud.hud_initialisieren(fenster)
gebaeude.gebaeude_initialisieren(fenster, 48)

forschung.forschung_zuruecksetzen()
werte = {
    "gold": 500, "energie": 500, "holz": 500, "stein": 500,
    "bevoelkerung": 20, "nahrung": 500, "forschung": 1000,
    "kohle": 0, "eisen": 0, "roboter": 0, "stahl": 0,
}

# Der lange Pfad ist absichtlich gestuft:
# Minenbau -> Eisenerkundung + Stahlverarbeitung -> Eisenminenbau.
assert forschung.forschung_status("eisenminenbau") == "gesperrt"
assert "Eisenerkundung" in forschung.technologie_name("eisenerkundung")
assert "Eisenmine" in ressourcen.freischaltung_hinweis(werte, 18)

# Vor dem Start der Forschung meldet der Baupfad nicht pauschal Rohstoffe,
# sondern die fehlende Forschung.
assert ressourcen.freischaltung_hinweis(werte, 18).startswith("Forschung fehlt:")

assert ressourcen.eisen_fund_chance() == 0.10
forschung._erforschte_technologien.update({"minenbau", "eisenerkundung"})
assert forschung.forschung_status("eisenminenbau") == "gesperrt"
assert ressourcen.eisen_fund_chance() == 0.35

# Erst mit beiden Vorforschungen ist Eisenminenbau startbereit.
forschung._erforschte_technologien.add("stahlverarbeitung")
assert forschung.forschung_status("eisenminenbau") == "bereit"
assert forschung.technologie_erforschen("eisenminenbau", werte)
assert not ressourcen.ist_freigeschaltet(werte, 18)
for _ in range(48):
    forschung.forschung_tick(werte)
assert forschung.ist_technologie_erforscht("eisenminenbau")
assert ressourcen.ist_freigeschaltet(werte, 18)

# Die echte Eisenmine produziert unabhängig von der Zufallschance planbar.
werte["energie"] = 500
liste = [{"typ": 18, "kachel_x": 4, "kachel_y": 4, "arbeitet": False}]
eisen_vorher = werte["eisen"]
ressourcen.ressourcen_produzieren(werte, liste)
assert werte["eisen"] > eisen_vorher

# Ein alter Spielstand ohne die neue Technologie bleibt gültig und meldet
# weiterhin die Forschung statt einen Rohstoffmangel.
forschung.forschung_zuruecksetzen()
assert ressourcen.freischaltung_hinweis(werte, 18).startswith("Forschung fehlt:")

pygame.quit()
print("STUNDE14_TESTS_OK")
