"""Regressionstest: Die Basis darf pro Kolonie nur einmal gebaut werden."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(__file__))

import pygame

pygame.init()
import forschung
import gebaeude

fenster = pygame.display.set_mode((1000, 700))
forschung.forschung_initialisieren(fenster)
gebaeude.gebaeude_initialisieren(fenster, 48)

# Auf einem leeren Bauplatz darf die erste Basis gebaut werden.
liste = []
assert gebaeude.kann_platzieren(liste, 0, 2, 2, 60, 40)
assert gebaeude.gebaeude_platzieren(liste, 0, 2, 2, 60, 40)
assert sum(g.get("typ") == 0 for g in liste) == 1

# Auch ein freier zweiter Bauplatz darf keine weitere Basis erlauben.
assert not gebaeude.kann_platzieren(liste, 0, 10, 10, 60, 40)
assert not gebaeude.gebaeude_platzieren(liste, 0, 10, 10, 60, 40)
assert sum(g.get("typ") == 0 for g in liste) == 1

# Die Prüfung gilt ebenfalls für einen belegten Bauplatz.
assert not gebaeude.kann_platzieren(liste, 0, 2, 2, 60, 40)

pygame.quit()
print("STUNDE17_TESTS_OK")
