"""Regressionstest fuer Groesse und Ueberlagerungen der Iso-Strassenbilder."""
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
import iso

fenster = pygame.display.set_mode((160, 120))
gebaeude.gebaeude_initialisieren(fenster, 48)

assert set(gebaeude.STRASSE_VERBINDUNGEN_ZU_BILD.values()).issubset(
    gebaeude._STRASSE_BILDER), "Alle Straßenmodule müssen geladen werden"

geraden_und_kurven = {
    frozenset(("N", "S")): "strasse_gerade_ne_sw.png",
    frozenset(("E", "W")): "strasse_gerade_nw_se.png",
    frozenset(("N", "E")): "strasse_kurve_ne_se.png",
    frozenset(("E", "S")): "strasse_kurve_se_sw.png",
    frozenset(("S", "W")): "strasse_kurve_sw_nw.png",
    frozenset(("W", "N")): "strasse_kurve_nw_ne.png",
}
for verbindungen, bildname in geraden_und_kurven.items():
    assert gebaeude.STRASSE_VERBINDUNGEN_ZU_BILD[verbindungen] == bildname

strassen_3x3 = [
    {"typ": 9, "kachel_x": x, "kachel_y": y}
    for y in range(3)
    for x in range(3)
]
erwartete_bilder_3x3 = {
    (0, 0): "strasse_kurve_se_sw.png",
    (1, 0): "strasse_t_ohne_ne.png",
    (2, 0): "strasse_kurve_sw_nw.png",
    (0, 1): "strasse_t_ohne_nw.png",
    (1, 1): "strasse_kreuz.png",
    (2, 1): "strasse_t_ohne_se.png",
    (0, 2): "strasse_kurve_ne_se.png",
    (1, 2): "strasse_t_ohne_sw.png",
    (2, 2): "strasse_kurve_nw_ne.png",
}
for strassenkachel in strassen_3x3:
    verbindungen = gebaeude.strasse_verbindungen_berechnen(
        strassenkachel, strassen_3x3)
    position = (strassenkachel["kachel_x"], strassenkachel["kachel_y"])
    assert gebaeude.STRASSE_VERBINDUNGEN_ZU_BILD[verbindungen] == \
        erwartete_bilder_3x3[position]

for kacheln, bildname in (
    ([(0, 0), (1, 0), (2, 0)], "strasse_gerade_nw_se.png"),
    ([(0, 0), (0, 1), (0, 2)], "strasse_gerade_ne_sw.png"),
):
    strassenkette = [
        {"typ": 9, "kachel_x": x, "kachel_y": y}
        for x, y in kacheln
    ]
    erwartet = pygame.transform.smoothscale(
        gebaeude._STRASSE_BILDER[bildname], (96, 48))
    for strassenkachel in strassenkette:
        verbindungen = gebaeude.strasse_verbindungen_berechnen(
            strassenkachel, strassenkette)
        bild = gebaeude.strasse_bild_fuer_verbindungen(
            verbindungen, (96, 48))
        assert pygame.image.tostring(bild, "RGBA") == \
            pygame.image.tostring(erwartet, "RGBA"), \
            "Ein Straßenende muss sich an seinem Nachbarn ausrichten"

bildname = "strasse_gerade_nw_se.png"
strassenbild = gebaeude._STRASSE_BILDER[bildname]
kreuzbild = gebaeude._STRASSE_BILDER["strasse_kreuz.png"]

fuss_x, fuss_y = 80, 70
strasse = {
    "typ": 9, "kachel_x": 2, "kachel_y": 2,
    "verbindungen": frozenset(("E", "W")),
}
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
bild = pygame.transform.smoothscale(strassenbild, rect.size)
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
bild = pygame.transform.smoothscale(kreuzbild, rect.size)
erwartet.blit(bild, rect)
gebaeude._gebauede_zeichen_einmal(
    strasse, 9, gebaeude.GEBAEUDE_TYPEN[9], 1, 1,
    fuss_x, fuss_y, 0, pygame.font.Font(None, 23))
assert pygame.image.tostring(gebaeude._fenster, "RGBA") == \
    pygame.image.tostring(erwartet, "RGBA"), \
    "Die fertig gedrehte X-Kreuzung muss passend zur Kachel gezeichnet werden"

pygame.quit()
print("STRASSEN_DARSTELLUNG_TESTS_OK")
