"""Regressionstest für das ein- und ausblendbare Zielfenster."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(__file__))

import pygame

pygame.init()
import main

# Die normale Hauptschleife initialisiert diese Module vor dem ersten Frame.
# Der Selbsttest ruft den Renderer direkt auf und führt die Initialisierung
# deshalb hier ausdrücklich aus.
main.spiel_menue.menue_initialisieren(main.fenster)
main.menu.menu_initialisieren(main.fenster)
main.hud.hud_initialisieren(main.fenster)
main.achievements.initialisieren(main.fenster)
main.missionen.initialisieren(main.fenster)

main.neues_spiel_starten()
assert main.spiel_status == "spiel"
assert main._ziel_anzeige_sichtbar is True

# O blendet das große Zielpanel aus und wieder ein.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_o))
assert main.ereignisse_verarbeiten()
assert main._ziel_anzeige_sichtbar is False
main.spielwelt_zeichnen()

pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_o))
assert main.ereignisse_verarbeiten()
assert main._ziel_anzeige_sichtbar is True
main.spielwelt_zeichnen()

# Der X-/Öffnen-Bereich kann auch mit der Maus bedient werden.
main.ziel_anzeige_umschalten()
assert main._ziel_anzeige_sichtbar is False
pygame.event.post(pygame.event.Event(
    pygame.MOUSEBUTTONDOWN,
    button=1,
    pos=main.ziel_schalter_rect().center,
))
assert main.ereignisse_verarbeiten()
assert main._ziel_anzeige_sichtbar is True
main.spielwelt_zeichnen()

pygame.quit()
print("STUNDE18_TESTS_OK")
