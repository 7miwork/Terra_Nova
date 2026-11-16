"""Regressionstest fuer Groesse und Ueberlagerungen der Iso-Strassenbilder."""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

pygame.init()

import gebaeude
import iso

fenster = pygame.display.set_mode((160, 120))
gebaeude.gebaeude_initialisieren(fenster, 48)

bildname = "strasse_gerade_nw_se.png"
strassenbild = pygame.Surface((128, 64), pygame.SRCALPHA)
pygame.draw.line(strassenbild, (120, 130, 140, 255), (64, 8), (64, 56), 9)
kreuzbild = pygame.Surface((128, 64), pygame.SRCALPHA)
pygame.draw.line(kreuzbild, (120, 130, 140, 255), (34, 32), (94, 32), 9)
pygame.draw.line(kreuzbild, (120, 130, 140, 255), (64, 16), (64, 48), 9)
gebaeude._STRASSE_BILDER = {
    bildname: strassenbild,
    "strasse_kreuz.png": kreuzbild,
}
gebaeude._STRASSE_BILD_CACHE = {}

fuss_x, fuss_y = 80, 70
strasse = {"typ": 9, "kachel_x": 2, "kachel_y": 2, "verbindungen": frozenset()}
rect = gebaeude._gebauede_bild_rechteck(
    strasse, 9, gebaeude.GEBAEUDE_TYPEN[9], 1, 1, fuss_x, fuss_y, 0)
assert rect == pygame.Rect(
    fuss_x - iso.ISO_HALB_BREITE,
    fuss_y - iso.ISO_KACHEL_HOEHE,
    iso.ISO_KACHEL_BREITE,
    iso.ISO_KACHEL_HOEHE,
)

gebaeude._fenster = pygame.Surface((160, 120), pygame.SRCALPHA)
erwartet = pygame.Surface((160, 120), pygame.SRCALPHA)
bild = gebaeude.strasse_bild_fuer_verbindungen(
    strasse["verbindungen"], rect.size)
erwartet.blit(bild, rect)
gebaeude._gebauede_zeichen_einmal(
    strasse, 9, gebaeude.GEBAEUDE_TYPEN[9], 1, 1,
    fuss_x, fuss_y, 0, pygame.font.Font(None, 23))
assert pygame.image.tostring(gebaeude._fenster, "RGBA") == \
    pygame.image.tostring(erwartet, "RGBA"), \
    "Das Strassenbild darf nicht mit dem Kuerzel ueberdruckt werden"

strasse["verbindungen"] = frozenset(("N", "E", "S", "W"))
gebaeude._fenster.fill((0, 0, 0, 0))
erwartet.fill((0, 0, 0, 0))
bild = pygame.transform.smoothscale(
    pygame.transform.rotate(kreuzbild, 45), rect.size)
erwartet.blit(bild, rect)
gebaeude._gebauede_zeichen_einmal(
    strasse, 9, gebaeude.GEBAEUDE_TYPEN[9], 1, 1,
    fuss_x, fuss_y, 0, pygame.font.Font(None, 23))
assert pygame.image.tostring(gebaeude._fenster, "RGBA") == \
    pygame.image.tostring(erwartet, "RGBA"), \
    "Die Strassenkreuzung muss gedreht und passend zur Kachel gezeichnet werden"

pygame.quit()
print("STRASSEN_DARSTELLUNG_TESTS_OK")
