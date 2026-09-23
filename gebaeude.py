"""Gebäudetypen, Bildzuordnung, Kategorien und Mehrkachel-Platzierung."""

import os
import pygame
import forschung


# Jedes Gebäude besitzt ein Bild. Die beiden Größenwerte werden für große
# Gebäude verwendet; normale Gebäude bleiben 1x1 Kachel groß.
GEBAEUDE_TYPEN = [
    {"name": "Basis", "bild": "basis.png", "farbe": (100, 180, 255), "kuerzel": "B", "taste": "1", "breite": 1, "hoehe": 1},
    {"name": "Reaktor", "bild": "reaktor.png", "farbe": (255, 200, 50), "kuerzel": "R", "taste": "2", "breite": 1, "hoehe": 1},
    {"name": "Farm", "bild": "farm.png", "farbe": (80, 200, 100), "kuerzel": "F", "taste": "3", "breite": 1, "hoehe": 1},
    {"name": "Holzfaeller", "bild": "holzfaeller.png", "farbe": (160, 120, 60), "kuerzel": "H", "taste": "4", "breite": 1, "hoehe": 1},
    {"name": "Steinmetz", "bild": "steinmetz.png", "farbe": (140, 140, 150), "kuerzel": "S", "taste": "5", "breite": 1, "hoehe": 1},
    {"name": "Marktplatz", "bild": "marktplatz.png", "farbe": (220, 180, 80), "kuerzel": "M", "taste": "6", "breite": 1, "hoehe": 1},
    {"name": "Wohnhaus", "bild": "wohnhaus.png", "farbe": (180, 120, 200), "kuerzel": "W", "taste": "7", "breite": 1, "hoehe": 1},
    {"name": "Universitaet", "bild": "schule_2x3_kacheln_64x96.png", "farbe": (150, 200, 255), "kuerzel": "L", "taste": "8", "breite": 2, "hoehe": 3},
    {"name": "Mine", "bild": "mine.png", "farbe": (110, 110, 120), "kuerzel": "M", "taste": "9", "breite": 1, "hoehe": 1},
    {"name": "Strasse", "bild": "strasse.png", "farbe": (90, 90, 95), "kuerzel": "S", "taste": "0", "breite": 1, "hoehe": 1},
    {"name": "Fusionsreaktor", "bild": "fusionsreaktor.png", "farbe": (255, 110, 210), "kuerzel": "F", "taste": "G", "breite": 1, "hoehe": 1},
    {"name": "Roboterfabrik", "bild": "roboterfabrik.png", "farbe": (100, 210, 210), "kuerzel": "R", "taste": "T", "breite": 1, "hoehe": 1},
    {"name": "Stahlwerk", "bild": "stahlwerk.png", "farbe": (230, 130, 70), "kuerzel": "S", "taste": "", "breite": 1, "hoehe": 1},
    {"name": "Gewaechshaus", "bild": "gewaechshaus.png", "farbe": (100, 220, 130), "kuerzel": "G", "taste": "", "breite": 1, "hoehe": 1},
    {"name": "Lagerhaus", "bild": "lagerhaus.png", "farbe": (100, 170, 220), "kuerzel": "L", "taste": "", "breite": 1, "hoehe": 1},
    {"name": "Wohnblock", "bild": "wohnblock.png", "farbe": (190, 140, 220), "kuerzel": "W", "taste": "", "breite": 1, "hoehe": 1},
    {"name": "Handelsposten", "bild": "handelsposten.png", "farbe": (240, 190, 80), "kuerzel": "H", "taste": "", "breite": 1, "hoehe": 1},
    {"name": "Koloniezentrum", "bild": "koloniezentrum.png", "farbe": (120, 220, 255), "kuerzel": "K", "taste": "", "breite": 1, "hoehe": 1},
    # Das Bild nutzt zunächst die vorhandene Mine als Platzhalter. So kann
    # die Klasse die Funktion sofort testen; ein eigenes Bild ist später eine
    # geeignete Schüler-Erweiterung.
    {"name": "Eisenmine", "bild": "mine.png", "farbe": (210, 130, 90), "kuerzel": "E", "taste": "", "breite": 1, "hoehe": 1},
    # Schülergebäude: Der Park verbessert die Versorgung der Bevölkerung.
    {"name": "Park", "bild": "park_32x32.png", "farbe": (80, 190, 100), "kuerzel": "P", "taste": "", "breite": 1, "hoehe": 1},
    # Schülergebäude: Der Solarreaktor liefert Energie ohne Kohleverbrauch.
    {"name": "Solarreaktor", "bild": "solareaktor_32x32.png", "farbe": (70, 170, 240), "kuerzel": "S", "taste": "", "breite": 1, "hoehe": 1},
    # ── Fortgeschrittener Kurs (Gegner): Verteidigung, Indizes 21 bis 23 ─────
    # NEUE TYPOLEN werden immer HINTEN angehaengt: Spielstaende speichern den
    # Typ-Index, therefore wuerde Umsortieren alte Spielstaende zerstoeren.
    # Die Bilder sind Platzhalter (mit bilder_erzeugen.py erzeugt) — die
    # Schuelerinnen und Schueler zeichnen spaeter eigene (wie bei Park/Solar).
    {"name": "Kaserne", "bild": "kaserne.png", "farbe": (190, 90, 90), "kuerzel": "K", "taste": "", "breite": 1, "hoehe": 1},
    {"name": "Raumschiffwerft", "bild": "raumschiffwerft.png", "farbe": (150, 160, 220), "kuerzel": "W", "taste": "", "breite": 2, "hoehe": 2},
    {"name": "Laserturm", "bild": "laserturm.png", "farbe": (255, 120, 120), "kuerzel": "T", "taste": "", "breite": 1, "hoehe": 1},
]

# Die Zifferntasten wählen Kategorien statt einzelner Gebäude. Mehrere Gebäude
# dürfen in mehreren Kategorien erscheinen; das macht die Auswahl verständlich.
GEBAEUDE_KATEGORIEN = {
    "1": {"name": "Basis / Kolonie-Zentrum", "typen": [0]},
    "2": {"name": "Erzeuger / Rohstoffe", "typen": [1, 2, 3, 4, 8, 13, 18]},
    "3": {"name": "Wohngebäude", "typen": [6, 15]},
    "4": {"name": "Veredelung / Fabriken", "typen": [5, 11, 12]},
    "5": {"name": "Forschung / Bildung", "typen": [7]},
    "6": {"name": "Energie", "typen": [1, 10, 20]},
    "7": {"name": "Infrastruktur", "typen": [9, 14]},
    "8": {"name": "Handel", "typen": [5, 16]},
    # Fortgeschrittener Kurs (Gegner): Kategorie 9 bündelt jetzt Prestige
    # UND Verteidigung, deshalb hat sie einen neuen Namen bekommen.
    "9": {"name": "Spezial / Verteidigung", "typen": [17, 19, 20, 21, 22, 23]},
}

_fenster = None
_kachel_groesse = 48
_bilder = {}
_bilder_cache = {}
_kuerzel_cache = {}
_schrift = None


def gebaeude_initialisieren(fenster_obj, kachel_groesse):
    global _fenster, _kachel_groesse, _bilder, _bilder_cache
    global _kuerzel_cache, _schrift
    _fenster = fenster_obj
    _kachel_groesse = kachel_groesse
    bilder_ordner = os.path.join(os.path.dirname(__file__), "bilder")
    _bilder = {}
    _bilder_cache = {}
    _kuerzel_cache = {}
    _schrift = pygame.font.Font(None, 23)
    for typ_daten in GEBAEUDE_TYPEN:
        dateiname = typ_daten.get("bild")
        if not dateiname:
            continue
        bild_pfad = os.path.join(bilder_ordner, dateiname)
        if os.path.exists(bild_pfad):
            _bilder[typ_daten["name"]] = pygame.image.load(bild_pfad).convert_alpha()


def bild_fuer_typ(typ_index, groesse=(30, 30)):
    """Liefert eine gecachte Bildvorschau für das Baumenü oder None.

    ``smoothscale`` ist eine vergleichsweise teure Bildoperation. Da sich die
    Vorschaugrößen selten ändern, wird jedes Ergebnis nur einmal berechnet.
    """
    if not (0 <= typ_index < len(GEBAEUDE_TYPEN)):
        return None
    name = GEBAEUDE_TYPEN[typ_index]["name"]
    bild = _bilder.get(name)
    if bild is None:
        return None
    schluessel = (name, tuple(groesse))
    if schluessel not in _bilder_cache:
        _bilder_cache[schluessel] = pygame.transform.smoothscale(bild, groesse)
    return _bilder_cache[schluessel]


def kategorie_auswahl(kategorie_taste, position=0):
    daten = GEBAEUDE_KATEGORIEN.get(str(kategorie_taste))
    if not daten or not daten["typen"]:
        return 0
    position %= len(daten["typen"])
    return daten["typen"][position]


def kategorie_name(kategorie_taste):
    daten = GEBAEUDE_KATEGORIEN.get(str(kategorie_taste))
    return daten["name"] if daten else "Schnellzugriff"


def kategorie_typen(kategorie_taste):
    daten = GEBAEUDE_KATEGORIEN.get(str(kategorie_taste))
    return list(daten["typen"]) if daten else []


def kategorie_weiter(kategorie_taste, position, delta):
    typen = kategorie_typen(kategorie_taste)
    if not typen:
        return 0, 0
    position = (position + delta) % len(typen)
    return position, typen[position]


def _masse_fuer_typ(typ_index):
    typ_daten = GEBAEUDE_TYPEN[typ_index]
    return typ_daten.get("breite", 1), typ_daten.get("hoehe", 1)


def gebaeude_flaeche(typ_index, kachel_x, kachel_y):
    breite, hoehe = _masse_fuer_typ(typ_index)
    return [(kachel_x + dx, kachel_y + dy)
            for dy in range(hoehe) for dx in range(breite)]


def _gebaeude_flaeche(gebaeude):
    return gebaeude_flaeche(gebaeude["typ"], gebaeude["kachel_x"], gebaeude["kachel_y"])


def _kompakt_erlaubt(typ_index):
    breite, hoehe = _masse_fuer_typ(typ_index)
    return (breite == 1 and hoehe == 1 and
            forschung.ist_technologie_erforscht("kompakte_maschinen") and
            typ_index not in (0, 9))


def kann_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y,
                    karten_breite=None, karten_hoehe=None):
    # Die Basis ist das zentrale Gebäude der Kolonie und darf genau einmal
    # existieren. Diese Prüfung muss vor der Flächenprüfung stehen, damit auch
    # eine zweite Basis auf einem freien Bauplatz verhindert wird.
    if typ_index == 0 and any(g.get("typ") == 0 for g in liste_gebaeude):
        return False

    neue_flaeche = set(gebaeude_flaeche(typ_index, kachel_x, kachel_y))
    if karten_breite is not None and karten_hoehe is not None:
        if any(x < 0 or y < 0 or x >= karten_breite or y >= karten_hoehe
               for x, y in neue_flaeche):
            return False
    ueberlappungen = []
    for vorhandenes in liste_gebaeude:
        if neue_flaeche.intersection(_gebaeude_flaeche(vorhandenes)):
            ueberlappungen.append(vorhandenes)
    if not ueberlappungen:
        return True
    if len(neue_flaeche) != 1 or any(len(_gebaeude_flaeche(g)) != 1 for g in ueberlappungen):
        return False
    if len(ueberlappungen) >= 2 or not _kompakt_erlaubt(typ_index):
        return False
    return _kompakt_erlaubt(ueberlappungen[0]["typ"])


def gebaeude_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y,
                        karten_breite=None, karten_hoehe=None):
    if not kann_platzieren(liste_gebaeude, typ_index, kachel_x, kachel_y,
                           karten_breite, karten_hoehe):
        print(f"Die Fläche ab ({kachel_x}, {kachel_y}) ist bereits belegt oder liegt außerhalb der Karte.")
        return False
    neues_gebaeude = {"typ": typ_index, "kachel_x": kachel_x,
                      "kachel_y": kachel_y, "arbeitet": False}
    if typ_index == 3 and forschung.ist_technologie_erforscht("forstwirtschaft"):
        neues_gebaeude["wald_vorrat"] = 30
        neues_gebaeude["wald_nachwuchs"] = 0
    liste_gebaeude.append(neues_gebaeude)
    breite, hoehe = _masse_fuer_typ(typ_index)
    print(f"{GEBAEUDE_TYPEN[typ_index]['name']} auf ({kachel_x}, {kachel_y}) platziert ({breite}x{hoehe} Kacheln).")
    return True


def gebaeude_abreissen(liste_gebaeude, kachel_x, kachel_y):
    for gebaeude in list(liste_gebaeude):
        if (kachel_x, kachel_y) in _gebaeude_flaeche(gebaeude):
            if gebaeude["typ"] == 0:
                print("Die Basis kann nicht abgerissen werden.")
                return None
            typ_index = gebaeude["typ"]
            liste_gebaeude.remove(gebaeude)
            return typ_index
    return None


def _position_fuer_stapel(liste_gebaeude, gebaeude):
    gleiche = [g for g in liste_gebaeude
               if len(_gebaeude_flaeche(g)) == 1
               and g["kachel_x"] == gebaeude["kachel_x"]
               and g["kachel_y"] == gebaeude["kachel_y"]]
    return gleiche.index(gebaeude) if gebaeude in gleiche else 0


def _warnsymbol_zeichnen(rect):
    """Zeichnet ein gelbes Warndreieck fuer ein Gebaeude ohne Strasse.

    Fortgeschrittener Kurs (Logistik): Das Dreieck sitzt unten links am
    Gebaeude. Es ist bewusst eine andere Form und eine andere Ecke als
    der rote Kreis ("arbeitet nicht"), damit beide Zeichen klar
    unterscheidbar sind.
    """
    links = rect.left + 3
    unten = rect.bottom - 3
    punkte = [(links + 7, unten - 14), (links, unten), (links + 14, unten)]
    pygame.draw.polygon(_fenster, (255, 205, 70), punkte)
    pygame.draw.polygon(_fenster, (70, 45, 0), punkte, 1)
    schrift = _schrift or pygame.font.Font(None, 23)
    zeichen = schrift.render("!", True, (70, 45, 0))
    _fenster.blit(zeichen, zeichen.get_rect(center=(links + 7, unten - 5)))


def gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y):
    if _fenster is None:
        return
    schrift = _schrift or pygame.font.Font(None, 23)
    # Der Schlüssel ist die belegte Kachel. So wird die Stapelposition in
    # einem Durchlauf ermittelt, statt für jedes Gebäude die ganze Liste zu
    # durchsuchen.
    stapel_zaehler = {}
    for gebaeude in liste_gebaeude:
        typ_index = gebaeude["typ"]
        typ_daten = GEBAEUDE_TYPEN[typ_index]
        breite, hoehe = _masse_fuer_typ(typ_index)
        pixel_x = gebaeude["kachel_x"] * _kachel_groesse - kamera_x
        pixel_y = gebaeude["kachel_y"] * _kachel_groesse - kamera_y
        voll_breite = breite * _kachel_groesse
        voll_hoehe = hoehe * _kachel_groesse
        stapel_index = 0
        if breite == 1 and hoehe == 1:
            stapel_schluessel = (gebaeude["kachel_x"], gebaeude["kachel_y"])
            stapel_index = stapel_zaehler.get(stapel_schluessel, 0)
            stapel_zaehler[stapel_schluessel] = stapel_index + 1
        if pixel_x + voll_breite < 0 or pixel_y + voll_hoehe < 0:
            continue
        if pixel_x > _fenster.get_width() or pixel_y > _fenster.get_height():
            continue
        if breite > 1 or hoehe > 1:
            rect = pygame.Rect(pixel_x + 4, pixel_y + 4,
                               voll_breite - 8, voll_hoehe - 8)
        else:
            if stapel_index:
                x_offset, y_offset = _kachel_groesse // 2, _kachel_groesse // 2
                groesse = _kachel_groesse // 2
            else:
                x_offset = y_offset = 4
                groesse = _kachel_groesse - 8
            rect = pygame.Rect(pixel_x + x_offset, pixel_y + y_offset,
                               groesse, groesse)
        bild = bild_fuer_typ(typ_index, rect.size)
        if bild is not None:
            _fenster.blit(bild, rect)
        else:
            pygame.draw.rect(_fenster, typ_daten["farbe"], rect)
        pygame.draw.rect(_fenster, (255, 255, 255), rect, 2)
        text_schluessel = (typ_index, (20, 20, 20))
        if text_schluessel not in _kuerzel_cache:
            _kuerzel_cache[text_schluessel] = schrift.render(
                typ_daten["kuerzel"], True, (20, 20, 20))
        text = _kuerzel_cache[text_schluessel]
        if breite == 1 and hoehe == 1:
            _fenster.blit(text, text.get_rect(center=rect.center))
        else:
            _fenster.blit(text, (rect.left + 6, rect.top + 4))
        if gebaeude.get("arbeitet") is False and typ_index not in (0, 9, 14, 17):
            pygame.draw.circle(_fenster, (220, 70, 70), (rect.right - 7, rect.top + 7), 4)
        # Fortgeschrittener Kurs (Logistik): Gelbes Warndreieck, wenn keine
        # Strasse zur Basis fuehrt. Der Grund steht direkt im Gebaeude.
        if gebaeude.get("stillstand_grund"):
            _warnsymbol_zeichnen(rect)
