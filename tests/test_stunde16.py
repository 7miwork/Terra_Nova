"""Integrationstest für die neue Ressource Zufriedenheit."""

import os
import sys
import tempfile

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
import spielstand

fenster = pygame.display.set_mode((1000, 700))
forschung.forschung_initialisieren(fenster)
gebaeude.gebaeude_initialisieren(fenster, 48)
hud.hud_initialisieren(fenster)
achievements.initialisieren(fenster)
missionen.initialisieren(fenster)
handel.handel_initialisieren(fenster)

# Zufriedenheit startet neutral und wird immer auf -50 bis +50 begrenzt.
werte = {"zufriedenheit": 0.0, "bevoelkerung": 20, "nahrung": 100,
         "energie": 100, "gold": 100, "holz": 100, "stein": 100,
         "forschung": 0, "kohle": 0, "eisen": 0, "roboter": 0, "stahl": 0}
assert ressourcen.park_nahrungsfaktor([]) == 1.0
ressourcen.zufriedenheit_aktualisieren(werte, [{"typ": 19}] * 20)
assert 0 <= werte["zufriedenheit"] <= 50
assert werte["zufriedenheit"] == 30.0

# Belastende Gebäude senken den Wert, aber nie unter -50.
werte["zufriedenheit"] = 0
ressourcen.zufriedenheit_aktualisieren(werte, [{"typ": 10}] * 100)
assert werte["zufriedenheit"] == -50.0
werte["zufriedenheit"] = 75
ressourcen.zufriedenheit_begrenzen(werte)
assert werte["zufriedenheit"] == 50.0
werte["zufriedenheit"] = -80
ressourcen.zufriedenheit_begrenzen(werte)
assert werte["zufriedenheit"] == -50.0

# Der Park wirkt auf den Nahrungsverbrauch; der Solarreaktor liefert Energie.
werte["zufriedenheit"] = 0
werte["nahrung"] = 100
werte["energie"] = 0
ressourcen.ressourcen_produzieren(
    werte, [{"typ": 19}, {"typ": 20, "arbeitet": False}])
assert werte["zufriedenheit"] > 0
assert werte["energie"] == 10
assert werte["nahrung"] < 100

# Mission und Achievement sehen Zufriedenheit als gemeinsamen Kontextwert.
missionen.zustand_zuruecksetzen()
assert "zufriedene_kolonie" in missionen.pruefen({"zufriedenheit": 30})
achievements.zustand_zuruecksetzen()
neu = achievements.pruefen(
    {"zufriedenheit": 30, "nahrung": 100, "energie": 100},
    [], [[0]],
)
assert "zufriedene_kolonie" in neu

# Die JSON-Speicherung übernimmt den Wert automatisch. Ein alter Zustand ohne
# dieses Feld wird vom Spielstart später mit 0 ergänzt.
spielstand.DATEI = os.path.join(tempfile.gettempdir(), "kolonie_test_zufriedenheit.json")
if os.path.exists(spielstand.DATEI):
    os.remove(spielstand.DATEI)
forschung.forschung_zuruecksetzen()
handel.handel_zuruecksetzen()
missionen.zustand_zuruecksetzen()
achievements.zustand_zuruecksetzen()
erfolg, _ = spielstand.speichern(
    [[0]], [], werte, [], 0, 0, 0, 1, "1", 0, 0, 0, "spiel")
assert erfolg
daten, _ = spielstand.laden()
assert daten["ressourcen"]["zufriedenheit"] == werte["zufriedenheit"]
os.remove(spielstand.DATEI)

pygame.quit()
print("STUNDE16_TESTS_OK")
