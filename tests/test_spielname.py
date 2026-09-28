"""Selbsttest fuer den Spielnamen (Abnahme im Fortgeschrittenen Kurs).

Headless (SDL- Treiber "dummy"): prueft
    1. die Konstante main.SPIELNAME,
    2. den Fenstertitel ueber pygame.display.get_caption(),
    3. den Hauptmenue-Titel (Grossschreibung nur, wenn sie nichts veraendert),
    4. das Rendern von Hauptmenue und Spielwelt ohne Fehler,
    5. 60 Frames Spielbetrieb ohne Exception.
"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
import main

# ── 1. Der Name ist gesetzt und brauchbar ──────────────────────────────────
assert isinstance(main.SPIELNAME, str), "SPIELNAME muss ein Text sein"
assert main.SPIELNAME.strip() != "", "SPIELNAME darf nicht leer sein"
print("SPIELNAME:", main.SPIELNAME)

# ── 2. Fenstertitel kommt aus SPIELNAME (ohne Zusatz "wie Final Earth 2") ──
assert main.BILD_TITEL == main.SPIELNAME, "BILD_TITEL muss SPIELNAME sein"
titel = pygame.display.get_caption()[0]
assert titel == main.SPIELNAME, \
    f"Fenstertitel ist '{titel}', erwartet '{main.SPIELNAME}'"
print("Fenstertitel:", titel)

# ── 3. Hauptmenue-Titel: Versalien nur ohne Zeichenveraenderung (ß -> SS) ──
erwartet = (main.SPIELNAME.upper()
            if main.SPIELNAME.upper().lower() == main.SPIELNAME.lower()
            else main.SPIELNAME)
assert main.menue_titel() == erwartet, main.menue_titel()
assert main.menue_titel().lower() == main.SPIELNAME.lower()
print("Hauptmenue-Titel:", main.menue_titel())

# ── 4. Menues und Welt aufsetzen ───────────────────────────────────────────
main.spiel_menue.menue_initialisieren(main.fenster)
main.menu.menu_initialisieren(main.fenster)
main.hud.hud_initialisieren(main.fenster)
main.achievements.initialisieren(main.fenster)
main.missionen.initialisieren(main.fenster)
main.forschung.forschung_initialisieren(main.fenster)
main.handel.handel_initialisieren(main.fenster)
main.logistik.initialisieren(main.fenster)
main.gegner.initialisieren(main.fenster)
main.neues_spiel_starten()

# Alle Menues rendern, in denen der Titel vorkommen koennte.
for status in ("hauptmenue", "regelmenue", "achievements", "missionen"):
    main.spiel_status = status
    main.spielwelt_zeichnen()
    pygame.display.flip()

# ── 5. 60 Frames Spielbetrieb (headless) ohne Exception ────────────────────
main.neues_spiel_starten()
main.spiel_status = "spiel"
for _frame in range(60):
    main.tick_zaehler += 1
    if main.tick_zaehler >= 60 // main.spiel_geschwindigkeit:
        main.tick_zaehler = 0
        main.ressourcen.ressourcen_produzieren(main.ressourcen_dict,
                                               main.liste_gebaeude,
                                               main.karten_daten)
        main.handel.handel_tick(main.ressourcen_dict, main.liste_gebaeude)
        main.gegner_ereignis_verarbeiten(
            main.gegner.gegner_tick(main.ressourcen_dict, main.liste_gebaeude,
                                    main.aktives_regelwerk()))
    main.spielwelt_zeichnen()
    pygame.display.flip()

# ── 6. Titel bleibt waehrend des Spiels unveraendert ───────────────────────
assert pygame.display.get_caption()[0] == main.SPIELNAME

print("SPIELNAME_TESTS_OK")
