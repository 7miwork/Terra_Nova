"""Kleine Selbsttests fuer das ausgelagerte Bodeneichen-Modul."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

projekt_ordner = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spielmodule_ordner = os.path.join(projekt_ordner, "spielmodule")
if projekt_ordner not in sys.path:
    sys.path.insert(0, projekt_ordner)
if spielmodule_ordner not in sys.path:
    sys.path.insert(0, spielmodule_ordner)

import pygame
import boden
import iso

pygame.init()
fenster = pygame.display.set_mode((320, 200))

boden.initialisieren(fenster, 48)
assert boden.BODEN_FARBEN[0] == (160, 140, 110)
assert boden.BODEN_FARBEN[1] == (100, 160, 80)
assert boden.ISO_UEBERLAPPUNG == 2
assert boden._uebergangs_farbe(1) == (127, 177, 111)

karte = [
    [0, 1, 2, 3],
    [1, 0, 3, 2],
]
boden.karte_zeichnen(
    karte, True, False, 4, 2, 0, 82, 320, 200)

boden.karte_zeichnen(
    karte, False, False, 4, 2, 0, 82, 320, 200)

print("BODEN_TESTS_OK")
