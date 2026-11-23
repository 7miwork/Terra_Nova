"""Stellt sicher, dass grosse Gebaeudebilder kein loses Kuerzel erhalten."""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
# Projektstamm und Spielmodule: main.py und flache Modulimporte sind erreichbar.
projekt_ordner = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spielmodule_ordner = os.path.join(projekt_ordner, "spielmodule")
if projekt_ordner not in sys.path:
    sys.path.insert(0, projekt_ordner)

if spielmodule_ordner not in sys.path:
    sys.path.insert(0, spielmodule_ordner)

import pygame

pygame.init()

import gebaeude

fenster = pygame.display.set_mode((400, 300))
gebaeude.gebaeude_initialisieren(fenster, 48)
universitaet = {
    "typ": 7,
    "kachel_x": 2,
    "kachel_y": 2,
    "arbeitet": True,
}

gebaeude.ansicht_setzen(True)
gebaeude._fenster = pygame.Surface((400, 300), pygame.SRCALPHA)
erwartet = pygame.Surface((400, 300), pygame.SRCALPHA)
rect = gebaeude._gebauede_bild_rechteck(
    universitaet, 7, gebaeude.GEBAEUDE_TYPEN[7], 2, 3, 200, 220, 0)
erwartet.blit(gebaeude.bild_fuer_typ(7, rect.size), rect)
gebaeude._gebauede_zeichen_einmal(
    universitaet, 7, gebaeude.GEBAEUDE_TYPEN[7], 2, 3,
    200, 220, 0, pygame.font.Font(None, 23))
assert pygame.image.tostring(gebaeude._fenster, "RGBA") == \
    pygame.image.tostring(erwartet, "RGBA"), \
    "Im Iso-Bild darf kein Kuerzel neben der Universitaet erscheinen"

gebaeude.ansicht_setzen(False)
gebaeude._fenster = pygame.Surface((400, 300), pygame.SRCALPHA)
erwartet = pygame.Surface((400, 300), pygame.SRCALPHA)
rect = pygame.Rect(2 * 48 + 4, 2 * 48 + 4, 2 * 48 - 8, 3 * 48 - 8)
erwartet.blit(gebaeude.bild_fuer_typ(7, rect.size), rect)
pygame.draw.rect(erwartet, (255, 255, 255), rect, 2)
gebaeude.gebaeude_zeichnen([universitaet], 0, 0)
assert pygame.image.tostring(gebaeude._fenster, "RGBA") == \
    pygame.image.tostring(erwartet, "RGBA"), \
    "Auch in der alten Ansicht darf kein Kuerzel neben dem Bild erscheinen"

pygame.quit()
print("GROSSE_GEBAEUDE_DARSTELLUNG_TESTS_OK")
