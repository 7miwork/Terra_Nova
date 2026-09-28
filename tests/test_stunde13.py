"""Tests für die flüssigere Darstellung und die zusätzliche P-Pause.

Der Test verwendet den Dummy-Videotreiber und öffnet kein sichtbares Fenster.
Er prüft bewusst die Spielregeln, nicht eine bestimmte Geschwindigkeit auf
unterschiedlicher Hardware.
"""

import os
import sys
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

pygame.init()
import main

main.sterne_generieren()
main.gebaeude.gebaeude_initialisieren(main.fenster, main.KACHEL_GROESSE)
main.hud.hud_initialisieren(main.fenster)
main.menu.menu_initialisieren(main.fenster)
main.spiel_menue.menue_initialisieren(main.fenster)
main.achievements.initialisieren(main.fenster)
main.missionen.initialisieren(main.fenster)
main.neues_spiel_starten()

# P öffnet die Pause aus dem laufenden Spiel.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
assert main.ereignisse_verarbeiten()
assert main.spiel_status == "pause"
assert main.spiel_geschwindigkeit == 0

# Während der Pause darf ein Wirtschaftstick den Zustand nicht verändern.
vorher = dict(main.ressourcen_dict)
main.tick_zaehler = 59
main.spielwelt_zeichnen()
assert main.ressourcen_dict == vorher

# P setzt die vorherige Spielgeschwindigkeit fort.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p))
assert main.pausemenue_verarbeiten()
assert main.spiel_status == "spiel"
assert main.spiel_geschwindigkeit == 1

# ESC bleibt als Alternative erhalten.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
assert main.ereignisse_verarbeiten()
assert main.spiel_status == "pause"
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
assert main.pausemenue_verarbeiten()
assert main.spiel_status == "spiel"

# Render-Smoke-Test: Die optimierte sichtbare Welt muss wiederholt ohne
# Ausnahme gezeichnet werden. Die Zeit ist nur eine Vergleichsinformation und
# kein harter Testwert, da Computer unterschiedlich schnell sind.
start = time.perf_counter()
for _ in range(60):
    main.spielwelt_zeichnen()
pygame.display.flip()
dauer = time.perf_counter() - start
print(f"RENDER_60_FRAMES_SECONDS={dauer:.4f}")

pygame.quit()
print("STUNDE13_TESTS_OK")
