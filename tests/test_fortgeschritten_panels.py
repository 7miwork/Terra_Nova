"""Selbsttest fuer die schwebenden Info-Fenster (panel.py) und das HUD-Layout.

Geprueft wird genau das, was auf dem Screenshot schiefging:
    1. Neue Fenster werden angeordnet, liegen unter dem HUD und ueberlappen nicht.
    2. Ziehen an der Titelzeile verschiebt das Fenster.
    3. Fenster lassen sich nicht aus dem Bild schieben (Klemmen).
    4. "-" minimiert, "+" klappt wieder auf.
    5. "X" blendet aus, Taste O holt das Zielfenster zurueck.
    6. Ein Klick IN ein Fenster wird verbraucht (man baut nicht darunter).
    7. V/C/I blenden Fenster ein/aus, L stellt die Anordnung zurueck.
    8. Die Ressourcenleiste schreibt keinen Text in die Nachbarspalte.
"""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
import main
import hud
import panel
import gegner

main.spiel_menue.menue_initialisieren(main.fenster)
main.menu.menu_initialisieren(main.fenster)
main.hud.hud_initialisieren(main.fenster)
main.achievements.initialisieren(main.fenster)
main.missionen.initialisieren(main.fenster)
main.forschung.forschung_initialisieren(main.fenster)
main.handel.handel_initialisieren(main.fenster)
main.logistik.initialisieren(main.fenster)
gegner.initialisieren(main.fenster)

FENSTER = ("uebersicht", "verteidigung", "ziel", "bauinfo")


def klick(pos, button=1):
    """Erzeugt ein Mausklick-Ereignis (ohne echtes Mausgerät)."""
    return pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=button, pos=pos)


def bewegung(pos):
    return pygame.event.Event(pygame.MOUSEMOTION, pos=pos)


def loslassen(pos):
    return pygame.event.Event(pygame.MOUSEBUTTONUP, button=1, pos=pos)


def taste(key):
    return pygame.event.Event(pygame.KEYDOWN, key=key)


# ── 1. Neues Spiel ordnet alle Fenster an ──────────────────────────────────
main.neues_spiel_starten()
assert main.spiel_status == "spiel"
main.gebaeude_auswahl = 0
main.spielwelt_zeichnen()
for name in FENSTER:
    assert panel.ist_sichtbar(name), f"{name} muss sichtbar sein"
    assert not panel.ist_minimiert(name), f"{name} startet ausgeklappt"
    assert panel.panel_rect(name) is not None, name

# ── 2. Fenster liegen unter dem HUD und ueberlappen sich nicht ─────────────
rechtecke = {name: panel.panel_rect(name) for name in FENSTER}
for name, rect in rechtecke.items():
    assert rect.y >= hud.HUD_HOEHE, f"{name} liegt im HUD-Balken"
    assert rect.x >= 0 and rect.right <= main.fenster.get_width(), name
    assert rect.bottom <= main.fenster.get_height(), name
for index, links in enumerate(FENSTER):
    for rechts in FENSTER[index + 1:]:
        assert not rechtecke[links].colliderect(rechtecke[rechts]), \
            f"{links} und {rechts} ueberlappen sich"

# ── 3. Ziehen an der Titelzeile verschiebt das Fenster ─────────────────────
titel = panel.titel_rect("ziel")
griff = (titel.x + 40, titel.y + 10)
vorher = panel.position("ziel")
assert panel.maus_ereignis(klick(griff)), "Klick auf die Titelzeile muss ziehen"
assert panel.zieht_gerade()
panel.maus_ereignis(bewegung((griff[0] - 120, griff[1] + 60)))
assert panel.position("ziel") == (vorher[0] - 120, vorher[1] + 60), \
    (vorher, panel.position("ziel"))
panel.maus_ereignis(loslassen((griff[0] - 120, griff[1] + 60)))
assert not panel.zieht_gerade(), "Nach dem Loslassen endet das Ziehen"

# ── 4. Fenster bleiben im Bild (Klemmen an den Raendern) ───────────────────
panel.verschieben("ziel", -500, -500)
assert panel.position("ziel") == (panel.RAND_FENSTER, panel.RAND_FENSTER)
panel.verschieben("ziel", 99999, 99999)
x, y = panel.position("ziel")
main.spielwelt_zeichnen()
rect = panel.panel_rect("ziel")
assert x + rect.width <= main.fenster.get_width()
assert y + rect.height <= main.fenster.get_height()

# ── 5. Minimieren ("-") und wieder aufklappen ("+") ────────────────────────
main.spielwelt_zeichnen()
hoehe_offen = panel.panel_rect("ziel").height
knopf = panel.knopf_rechtecke("ziel")["minimieren"]
assert panel.maus_ereignis(klick(knopf.center)), "Klick auf '-' muss wirken"
assert panel.ist_minimiert("ziel")
main.spielwelt_zeichnen()
assert panel.panel_rect("ziel").height == panel.TITEL_HOEHE < hoehe_offen
knopf = panel.knopf_rechtecke("ziel")["minimieren"]
assert panel.maus_ereignis(klick(knopf.center))
assert not panel.ist_minimiert("ziel")
main.spielwelt_zeichnen()
assert panel.panel_rect("ziel").height == hoehe_offen

# ── 6. Schliessen ("X") und mit Taste O zurueckholen ───────────────────────
schliessen = panel.knopf_rechtecke("ziel")["schliessen"]
assert panel.maus_ereignis(klick(schliessen.center))
assert not panel.ist_sichtbar("ziel")
main.spielwelt_zeichnen()
assert panel.panel_rect("ziel") is None, "Ausgeblendet = kein Fenster"
assert not main._ziel_anzeige_sichtbar, "Alter Merker bleibt synchron"
main.ziel_anzeige_umschalten()
assert panel.ist_sichtbar("ziel") and main._ziel_anzeige_sichtbar
main.spielwelt_zeichnen()

# ── 7. Klick in ein Fenster wird verbraucht (kein Bauen darunter) ──────────
innen = panel.panel_rect("verteidigung").center
assert panel.maus_ereignis(klick(innen)), "Klick im Fenster wird verbraucht"
assert not panel.maus_ereignis(klick((5, 690))), \
    "Klick neben den Fenstern gehoert der Karte"

# ── 8. Tasten S/C/I und Layout zuruecksetzen mit L ─────────────────────────
for key, name in ((pygame.K_s, "verteidigung"), (pygame.K_c, "bauinfo"),
                  (pygame.K_i, "uebersicht")):
    assert panel.ist_sichtbar(name)
    pygame.event.post(taste(key))
    assert main.ereignisse_verarbeiten()
    assert not panel.ist_sichtbar(name), f"{name} muss mit Taste aus sein"
    pygame.event.post(taste(key))
    assert main.ereignisse_verarbeiten()
    assert panel.ist_sichtbar(name), f"{name} muss wieder sichtbar sein"
panel.verschieben("uebersicht", 300, 400)
panel.minimieren_setzen("bauinfo", True)
pygame.event.post(taste(pygame.K_l))
assert main.ereignisse_verarbeiten()
assert panel.position("uebersicht") == (14, hud.HUD_HOEHE + 8)
assert not panel.ist_minimiert("bauinfo"), "L klappt alle Fenster auf"

# ── 9. Ressourcenleiste: kein Text in der Nachbarspalte, nichts am Rand ────
main.ressourcen_dict.update({
    "gold": 480, "energie": 92, "holz": 173, "stein": 210, "bevoelkerung": 24,
    "nahrung": 190, "forschung": 35, "kohle": 60, "eisen": 40, "roboter": 3,
    "stahl": 12, "zufriedenheit": 12})
main.spielwelt_zeichnen()
layout = hud._letztes_layout
assert layout is not None, "Layout muss beim Zeichnen berechnet werden"
schrift = hud._font(layout["schriftgroesse"])
for index, eintrag in enumerate(layout["eintraege"]):
    rechts = eintrag["text_pos"][0] + schrift.size(eintrag["text"])[0]
    spalte = index % hud._RESSOURCEN_SPALTEN
    grenze = (spalte + 1) * layout["spaltenbreite"] + 14
    assert rechts <= grenze - 4, (eintrag["text"], rechts, grenze)
    assert rechts <= main.fenster.get_width(), eintrag["text"]
assert layout["balkenhoehe"] >= hud.HUD_HOEHE

# Die reine Layoutfunktion laesst sich auch fuer ein schmales Fenster nutzen.
schmal = hud.ressourcen_leiste_layout(
    [{"name": "Bevoelkerung", "schluessel": "bevoelkerung"}],
    {"bevoelkerung": 100}, {"bevoelkerung": 100.0}, fenster_breite=800)
assert schmal["eintraege"][0]["text"] == "Bevoelkerung: 100/100"
assert schmal["schriftgroesse"] <= 24

# ── 10. Ganzes Bild rendert weiterhin ohne Fehler ──────────────────────────
main.spielwelt_zeichnen()
pygame.display.flip()

print("PANEL_TESTS_OK")

