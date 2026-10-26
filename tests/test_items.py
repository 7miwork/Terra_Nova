"""Tests fuer die Items (passive Gegenstaende auf der Karte) — Schritt 5.

Die Spiellogik denkt weiter im normalen Raster. Diese Tests pruefen den
Fussabdruck, die Ansicht-Umschaltung und dass das Zeichnen in beiden
Ansichten (Iso und 2D) ohne Absturz laeuft.
"""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
import items
import iso

fenster = pygame.display.set_mode((1000, 700))


# ── 1. Fussabdruck (item_flaeche) ──────────────────────────────────────────
# 1x1-Items belegen genau eine Kachel.
assert items.item_flaeche(0, 3, 5) == [(3, 5)], items.item_flaeche(0, 3, 5)
assert items.item_flaeche(1, 0, 0) == [(0, 0)]
# Der 2x2 "Grosse Fels" (Index 4) belegt vier Kacheln.
assert items.item_flaeche(4, 0, 0) == [(0, 0), (1, 0), (0, 1), (1, 1)], \
    items.item_flaeche(4, 0, 0)
assert items.item_flaeche(4, 5, 7) == [(5, 7), (6, 7), (5, 8), (6, 8)]
# Alle ITEM_TYPEN haben breite/hoehe.
for typ in items.ITEM_TYPEN:
    assert typ.get("breite", 0) >= 1 and typ.get("hoehe", 0) >= 1
print("Items: Fussabdruck fuer 1x1 und 2x2 korrekt")


# ── 2. Ansicht umschalten ───────────────────────────────────────────────────
items.ansicht_setzen(False)
assert items._iso_ansicht is False
items.ansicht_setzen(True)
assert items._iso_ansicht is True
items.ansicht_setzen(0)  # Falsey
assert items._iso_ansicht is False
items.ansicht_setzen(1)  # Truthy
assert items._iso_ansicht is True
print("Items: Ansicht-Umschaltung (Iso <-> 2D) funktioniert")


# ── 3. Initialisieren + Zeichnen (Smoke-Test, dummy-Fenster) ────────────────
items.item_initialisieren(fenster, 48)
assert items._fenster is fenster
assert items._kachel_groesse == 48

# Leere Liste: nichts crashen lassen.
items.zeichnen([], 0, 0)

# Einige Items im sichtbaren Bereich und ausserhalb — culling muss robust sein.
liste = [
    {"typ": 0, "kachel_x": 5, "kachel_y": 5},   # sichtbar
    {"typ": 4, "kachel_x": 10, "kachel_y": 10},  # 2x2
    {"typ": 3, "kachel_x": -100, "kachel_y": -100},  # ausserhalb
    {"typ": 2, "kachel_x": 1000, "kachel_y": 1000},  # ausserhalb
]
# Iso-Pfad
items.ansicht_setzen(True)
items.zeichnen(liste, 0, 0)
# 2D-Pfad
items.ansicht_setzen(False)
items.zeichnen(liste, 0, 0)
print("Items: Zeichnen in Iso und 2D ohne Absturz (inkl. Culling)")


# ── 4. Sortierung (hinten zuerst) ───────────────────────────────────────────
# iso.zeichen_reihenfolge mit dem Item-Fussabdruck sortiert von hinten nach
# vorne — die sortierte Liste veraendert die Original-Liste nicht.
items.ansicht_setzen(True)
sortiert = iso.zeichen_reihenfolge(liste, items._item_flaeche)
assert isinstance(sortiert, list) and len(sortiert) == len(liste)
# Original bleibt unveraendert.
assert liste == [{"typ": 0, "kachel_x": 5, "kachel_y": 5},
                 {"typ": 4, "kachel_x": 10, "kachel_y": 10},
                 {"typ": 3, "kachel_x": -100, "kachel_y": -100},
                 {"typ": 2, "kachel_x": 1000, "kachel_y": 1000}]
print("Items: Sortierung (hinten zuerst) arbeitet auf einer Kopie")


# ── 5. main.py-Verdrahtung (Quelltext-Check) ────────────────────────────────
main_pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
with open(main_pfad, encoding="utf-8") as _f:
    _main_quelle = _f.read()
for _muss in ("import items", "items.item_initialisieren(", "items.ansicht_setzen(",
              "items.zeichnen(", "items_generieren()"):
    assert _muss in _main_quelle, f"main.py: {_muss} fehlt"
print("Items: main.py importiert und verdrahtet das Modul korrekt")


# ── 6. Abbau-Mechanik (Ressourcen aus Items gewinnen) ───────────────────────
# item_abbauen liefert die Ressourcen eines Items.
ertrag = items.item_abbauen({"typ": 0, "kachel_x": 1, "kachel_y": 2})
assert ertrag == {"gold": 50}, ertrag
ertrag = items.item_abbauen({"typ": 4, "kachel_x": 0, "kachel_y": 0})
assert ertrag == {"stein": 60}, ertrag
ertrag = items.item_abbauen({"typ": 3, "kachel_x": 0, "kachel_y": 0})
assert ertrag == {"forschung": 10}, ertrag
# Unbekannter Typ liefert {}.
assert items.item_abbauen({"typ": 99, "kachel_x": 0, "kachel_y": 0}) == {}
# item_am_punkt findet ein Item an einer seiner Kacheln.
liste_test = [{"typ": 4, "kachel_x": 5, "kachel_y": 5}]
assert items.item_am_punkt(5, 5, liste_test) is liste_test[0]
assert items.item_am_punkt(6, 6, liste_test) is liste_test[0]
assert items.item_am_punkt(0, 0, liste_test) is None
print("Items: Abbau-Mechanik (item_abbauen / item_am_punkt) korrekt")

pygame.quit()
print("ITEMS_TESTS_OK")