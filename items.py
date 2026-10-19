"""
items.py - Passive Gegenstande auf der Karte (Ressourcen, Deko, etc.)
Schritt 5: Isometrische Ansicht mit Fussabdruck und Sortierung.

Die Spiellogik denkt weiter im normalen Raster. Nur das ZEICHNEN nutzt
die Iso-Umrechnung aus iso.py. Items werden wie Gebaeude von hinten nach
vorne sortiert, damit vordere Objekte hintere ueberdecken.
"""

import os
import pygame
import iso

# Jeder Gegenstandstyp hat ein Bild, eine Farbe und eine Fussabdruck-Groesse.
ITEM_TYPEN = [
    {"name": "Goldvorkommen", "bild": None, "farbe": (255, 215, 0), "kuerzel": "G",
     "breite": 1, "hoehe": 1},
    {"name": "Holzhaufen", "bild": None, "farbe": (139, 69, 19), "kuerzel": "H",
     "breite": 1, "hoehe": 1},
    {"name": "Steinhaufen", "bild": None, "farbe": (128, 128, 128), "kuerzel": "S",
     "breite": 1, "hoehe": 1},
    {"name": "Kristall", "bild": None, "farbe": (200, 100, 255), "kuerzel": "K",
     "breite": 1, "hoehe": 1},
    {"name": "Grosser Fels", "bild": None, "farbe": (100, 100, 110), "kuerzel": "F",
     "breite": 2, "hoehe": 2},
]

_fenster = None
_kachel_groesse = 48
_iso_ansicht = True
_bilder = {}
_schrift = None


def ansicht_setzen(iso_an):
    """Schaltet die Item-Ansicht um (Iso <-> 2D).

    main.py gibt hier ISO_ANSICHT weiter, damit Items, Gebaeude und
    Logistik dieselbe Ansicht zeigen. Ohne diese Funktion muesste
    items.py die Konstante aus main.py importieren — das gaebe einen
    Kreis-Import.
    """
    global _iso_ansicht
    _iso_ansicht = bool(iso_an)


def item_initialisieren(fenster_obj, kachel_groesse):
    """Merkt sich Fenster, Kachel-Groesse und laedt Item-Bilder."""
    global _fenster, _kachel_groesse, _bilder, _schrift
    _fenster = fenster_obj
    _kachel_groesse = kachel_groesse
    _schrift = pygame.font.Font(None, 23)
    bilder_ordner = os.path.join(os.path.dirname(__file__), "bilder")
    _bilder = {}
    for typ_daten in ITEM_TYPEN:
        dateiname = typ_daten.get("bild")
        if not dateiname:
            continue
        bild_pfad = os.path.join(bilder_ordner, dateiname)
        if os.path.exists(bild_pfad):
            _bilder[typ_daten["name"]] = pygame.image.load(bild_pfad).convert_alpha()


def _masse_fuer_typ(typ_index):
    typ_daten = ITEM_TYPEN[typ_index]
    return typ_daten.get("breite", 1), typ_daten.get("hoehe", 1)


def item_flaeche(typ_index, kachel_x, kachel_y):
    """Liefert alle Kacheln, die ein Item belegt (Fussabdruck)."""
    breite, hoehe = _masse_fuer_typ(typ_index)
    return [(kachel_x + dx, kachel_y + dy)
            for dy in range(hoehe) for dx in range(breite)]


def _item_flaeche(item):
    return item_flaeche(item["typ"], item["kachel_x"], item["kachel_y"])


def zeichnen(liste_items, kamera_x, kamera_y):
    """Zeichnet alle Items — in Iso hinten zuerst, sonst wie frueher.

    Der Iso-Pfad sortiert die Items mit iso.zeichen_reihenfolge (nach
    der vordersten Fussabdruck-Kachel) und malt jedes als Bild oder
    Farbkreis. Der 2D-Pfad darunter ist der unveraenderte alte Code zum
    Vergleichen im Unterricht.
    """
    if _fenster is None:
        return
    schrift = _schrift or pygame.font.Font(None, 23)
    if _iso_ansicht:
        _zeichnen_iso(liste_items, kamera_x, kamera_y, schrift)
        return
    # 2D-Pfad: einfache Rechtecke pro Item.
    for item in liste_items:
        typ_index = item["typ"]
        typ_daten = ITEM_TYPEN[typ_index]
        breite, hoehe = _masse_fuer_typ(typ_index)
        pixel_x = item["kachel_x"] * _kachel_groesse - kamera_x
        pixel_y = item["kachel_y"] * _kachel_groesse - kamera_y
        voll_breite = breite * _kachel_groesse
        voll_hoehe = hoehe * _kachel_groesse
        if pixel_x + voll_breite < 0 or pixel_y + voll_hoehe < 0:
            continue
        if pixel_x > _fenster.get_width() or pixel_y > _fenster.get_height():
            continue
        rect = pygame.Rect(pixel_x + 4, pixel_y + 4,
                           voll_breite - 8, voll_hoehe - 8)
        bild = _bilder.get(typ_daten["name"])
        if bild is not None:
            _fenster.blit(pygame.transform.scale(bild, rect.size), rect)
        else:
            pygame.draw.rect(_fenster, typ_daten["farbe"], rect)
        pygame.draw.rect(_fenster, (255, 255, 255), rect, 1)
        text = schrift.render(typ_daten.get("kuerzel", "?"), True, (20, 20, 20))
        _fenster.blit(text, text.get_rect(center=rect.center))


def _zeichnen_iso(liste_items, kamera_x, kamera_y, schrift):
    """Zeichnet alle Items in der Iso-Ansicht (hinten zuerst).

    Die Sortierung kommt aus iso.py und benutzt die vorderste Kachel des
    Fussabdrucks — so ueberdeckt zum Beispiel ein grosses Item alles
    hinter ihm und nichts vor ihm.
    """
    stapel_zaehler = {}
    sortiert = iso.zeichen_reihenfolge(liste_items, _item_flaeche)
    for item in sortiert:
        typ_index = item["typ"]
        typ_daten = ITEM_TYPEN[typ_index]
        breite, hoehe = _masse_fuer_typ(typ_index)
        stapel_index = 0
        if breite == 1 and hoehe == 1:
            stapel_schluessel = (item["kachel_x"], item["kachel_y"])
            stapel_index = stapel_zaehler.get(stapel_schluessel, 0)
            stapel_zaehler[stapel_schluessel] = stapel_index + 1
        fuss_spalte, fuss_zeile = iso._fuss_vorne(item, _item_flaeche)
        fuss_x, fuss_y = iso.kachel_unten_mitte(fuss_spalte, fuss_zeile,
                                                kamera_x, kamera_y)
        # Ganz ausserhalb des Bildes malen wir nichts (spart Rechenzeit).
        if (fuss_x < -200 or fuss_x > _fenster.get_width() + 200
                or fuss_y < -200 or fuss_y > _fenster.get_height() + 200):
            continue
        # Bild oder Farbkreis als Platzhalter.
        bild = _bilder.get(typ_daten["name"])
        if bild is not None:
            # Groesse anpasst an Fussabdruck: 1 Kachel = eine Raute.
            bild_breite = max(breite, hoehe) * iso.ISO_KACHEL_BREITE // 2 - 8
            bild_hoehe = iso.ISO_KACHEL_HOEHE - 8
            if breite > 1 or hoehe > 1:
                bild_hoehe = max(bild_hoehe, bild_breite * 3 // 4)
            rect = pygame.Rect(fuss_x - bild_breite // 2, fuss_y - bild_hoehe,
                               bild_breite, bild_hoehe)
            _fenster.blit(pygame.transform.scale(bild, rect.size), rect)
        else:
            # Kein Bild: Farbkreis auf dem Fusspunkt (untere Rautenecke).
            radius = 8 + max(0, breite - 1) * 6
            pygame.draw.circle(_fenster, typ_daten["farbe"],
                               (fuss_x, fuss_y), radius)
            pygame.draw.circle(_fenster, (255, 255, 255),
                               (fuss_x, fuss_y), radius, 1)
        # Kuerzel am Fusspunkt.
        text = schrift.render(typ_daten.get("kuerzel", "?"), True, (20, 20, 20))
        _fenster.blit(text, text.get_rect(center=(fuss_x, fuss_y)))
