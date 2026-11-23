"""Zeichnen der Planetenoberflaeche in 2D und isometrischer Ansicht."""

import os

import pygame

import pfade
import iso


BODEN_FARBEN = {
    0: (160, 140, 110),
    1: (100, 160, 80),
    2: (90, 90, 95),
    3: (195, 185, 150),
}
FARBE_GITTER = (60, 55, 50)
FARBE_KARTENRAND = (90, 110, 140)
KARTENRAND_DICKE = 2
ISO_UEBERLAPPUNG = 2

_fenster = None
_kachel_groesse = 48
_bilder = {}
_bilder_geladen = False
_iso_cache = {}


def initialisieren(fenster_obj, kachel_groesse=48):
    """Merkt sich das Fenster und die Kachelgroesse fuer alle Zeichenfunktionen."""
    global _fenster, _kachel_groesse
    _fenster = fenster_obj
    _kachel_groesse = kachel_groesse


def bilder_laden():
    """Laedt Bodenbilder einmalig aus dem zentralen Terrainordner."""
    global _bilder_geladen
    if _bilder_geladen:
        return
    dateinamen = {
        0: "erde.png",
        1: "gras.png",
        2: "stein.png",
        3: "sand.png",
    }
    for typ_index, dateiname in dateinamen.items():
        bild_pfad = os.path.join(pfade.BILDER_TERRAIN, dateiname)
        if os.path.exists(bild_pfad):
            _bilder[typ_index] = pygame.image.load(bild_pfad).convert_alpha()
    _bilder_geladen = True


def _farbe_mischen(farbe, anteil=0.0):
    """Mischt eine Farbe mit Weiss fuer hellere Kanten."""
    anteil = max(0.0, min(1.0, anteil))
    return tuple(int(wert + (255 - wert) * anteil) for wert in farbe)


def _uebergangs_farbe(typ_index):
    """Liefert eine helle Mischfarbe fuer einen Bodentyp."""
    farbe = BODEN_FARBEN.get(typ_index)
    if farbe is None:
        return None
    return _farbe_mischen(farbe, 0.18)


def _iso_bild(typ_index, nachbarn=None):
    """Erzeugt eine gecachte rautenfoermige Bodenoberflaeche."""
    del nachbarn
    cache_schluessel = typ_index
    if cache_schluessel in _iso_cache:
        return _iso_cache[cache_schluessel]
    bild = _bilder.get(typ_index)
    if bild is None:
        _iso_cache[cache_schluessel] = None
        return None

    breite = iso.ISO_KACHEL_BREITE
    hoehe = iso.ISO_KACHEL_HOEHE
    surface_breite = breite + ISO_UEBERLAPPUNG
    surface_hoehe = hoehe + ISO_UEBERLAPPUNG

    # Die PNG-Dateien enthalten einen kompletten kleinen Wuerfel.
    # Hier wird nur die obere Diamantfloche aus dem PNG ausgeschnitten.
    # Damit keine Seitenwaende als neue Wuerfel in die Karte ragen.
    quelle_breite = bild.get_width()
    quelle_hoehe = bild.get_height()
    quelle_punkte = [
        (quelle_breite // 2, quelle_hoehe // 16),
        (quelle_breite * 15 // 16, quelle_hoehe // 2),
        (quelle_breite // 2, quelle_hoehe * 15 // 16),
        (quelle_breite // 16, quelle_hoehe // 2),
    ]
    quelle_maske = pygame.Surface(
        (quelle_breite, quelle_hoehe), pygame.SRCALPHA)
    pygame.draw.polygon(
        quelle_maske, (255, 255, 255, 255), quelle_punkte)
    ausschnitt = pygame.Surface(
        (quelle_breite, quelle_hoehe), pygame.SRCALPHA)
    ausschnitt.blit(bild, (0, 0))
    for x in range(quelle_breite):
        for y in range(quelle_hoehe):
            if quelle_maske.get_at((x, y))[3] == 0:
                ausschnitt.set_at((x, y), (0, 0, 0, 0))
    bild_klein = pygame.transform.scale(
        ausschnitt, (surface_breite, surface_hoehe))
    oberflaeche = pygame.Surface(
        (surface_breite, surface_hoehe), pygame.SRCALPHA)
    oberflaeche.blit(bild_klein, (0, 0))

    punkte = [
        (surface_breite // 2, 0),
        (surface_breite, surface_hoehe // 2),
        (surface_breite // 2, surface_hoehe),
        (0, surface_hoehe // 2),
    ]
    maske = pygame.Surface(
        (surface_breite, surface_hoehe), pygame.SRCALPHA)
    pygame.draw.polygon(maske, (255, 255, 255, 255), punkte)
    for x in range(surface_breite):
        for y in range(surface_hoehe):
            if maske.get_at((x, y))[3] == 0:
                oberflaeche.set_at((x, y), (0, 0, 0, 0))
    _iso_cache[cache_schluessel] = oberflaeche
    return oberflaeche


def _2d_zeichnen(karten_daten, gitter_an, erste_spalte, letzte_spalte,
                 erste_zeile, letzte_zeile, kamera_x, kamera_y,
                 bild_breite, bild_hoehe):
    global _fenster
    if _fenster is None:
        _fenster = pygame.display.get_surface()
    del bild_breite, bild_hoehe
    bilder_laden()
    for zeile in range(erste_zeile, letzte_zeile):
        pixel_y = zeile * _kachel_groesse - kamera_y
        for spalte in range(erste_spalte, letzte_spalte):
            pixel_x = spalte * _kachel_groesse - kamera_x
            rect = pygame.Rect(
                pixel_x, pixel_y, _kachel_groesse, _kachel_groesse)
            bild = _bilder.get(karten_daten[zeile][spalte])
            if bild is not None:
                bild_klein = pygame.transform.scale(
                    bild, (_kachel_groesse + 2, _kachel_groesse + 2))
                _fenster.blit(bild_klein, (pixel_x - 1, pixel_y - 1))
            else:
                pygame.draw.rect(
                    _fenster,
                    BODEN_FARBEN[karten_daten[zeile][spalte]],
                    rect)
            if gitter_an:
                pygame.draw.rect(_fenster, FARBE_GITTER, rect, 1)


def _iso_zeichnen(karten_daten, gitter_an, welt_breite, welt_hoehe,
                  kamera_x, kamera_y, bild_breite, bild_hoehe):
    global _fenster
    if _fenster is None:
        _fenster = pygame.display.get_surface()
    bilder_laden()
    kacheln = []
    for zeile in range(welt_hoehe):
        for spalte in range(welt_breite):
            ecke_x, ecke_y = iso.raster_zu_welt(spalte, zeile)
            bild_x = ecke_x - kamera_x
            bild_y = ecke_y - kamera_y
            if (bild_x + iso.ISO_HALB_BREITE < 0
                    or bild_x - iso.ISO_HALB_BREITE > bild_breite
                    or bild_y + iso.ISO_KACHEL_HOEHE < 0
                    or bild_y > bild_hoehe):
                continue
            kacheln.append((spalte, zeile))

    kacheln.sort(key=lambda kachel: (kachel[0] + kachel[1], kachel[1]))
    for spalte, zeile in kacheln:
        punkte = iso.kachel_polygon(spalte, zeile, kamera_x, kamera_y)
        typ_index = karten_daten[zeile][spalte]
        nachbarn = {}
        if zeile > 0 and karten_daten[zeile - 1][spalte] != typ_index:
            nachbarn["oben"] = karten_daten[zeile - 1][spalte]
        if zeile + 1 < welt_hoehe and karten_daten[zeile + 1][spalte] != typ_index:
            nachbarn["unten"] = karten_daten[zeile + 1][spalte]
        if spalte > 0 and karten_daten[zeile][spalte - 1] != typ_index:
            nachbarn["links"] = karten_daten[zeile][spalte - 1]
        if spalte + 1 < welt_breite and karten_daten[zeile][spalte + 1] != typ_index:
            nachbarn["rechts"] = karten_daten[zeile][spalte + 1]
        bodenbild = _iso_bild(typ_index, nachbarn)
        if bodenbild is not None:
            _fenster.blit(
                bodenbild,
                (punkte[0][0] - iso.ISO_HALB_BREITE - 1,
                 punkte[0][1] - 1))
        else:
            pygame.draw.polygon(
                _fenster,
                BODEN_FARBEN[karten_daten[zeile][spalte]],
                punkte)
        if gitter_an:
            pygame.draw.polygon(_fenster, FARBE_GITTER, punkte, 1)

    # Geschlossene Kartenränder ohne Würfelwirkung.
    oben_links = iso.raster_zu_welt(0, 0)
    oben_rechts = iso.raster_zu_welt(welt_breite - 1, 0)
    unten_links = iso.raster_zu_welt(0, welt_hoehe - 1)
    unten_rechts = iso.raster_zu_welt(welt_breite - 1, welt_hoehe - 1)
    randpunkte = [
        (oben_links[0] - kamera_x,
         oben_links[1] - kamera_y),
        (oben_rechts[0] + iso.ISO_HALB_BREITE - kamera_x,
         oben_rechts[1] + iso.ISO_HALB_HOEHE - kamera_y),
        (unten_rechts[0] - kamera_x,
         unten_rechts[1] + iso.ISO_KACHEL_HOEHE - kamera_y),
        (unten_links[0] - iso.ISO_HALB_BREITE - kamera_x,
         unten_links[1] + iso.ISO_HALB_HOEHE - kamera_y),
    ]
    pygame.draw.lines(
        _fenster, FARBE_KARTENRAND, True, randpunkte,
        KARTENRAND_DICKE)


def karte_zeichnen(karten_daten, iso_an, gitter_an,
                   welt_breite, welt_hoehe, kamera_x, kamera_y,
                   bild_breite, bild_hoehe):
    """Zeichnet eine Karte in 2D oder Iso ohne Spiellogik zu enthalten."""
    if iso_an:
        _iso_zeichnen(
            karten_daten, gitter_an, welt_breite, welt_hoehe,
            kamera_x, kamera_y, bild_breite, bild_hoehe)
        return

    erste_spalte = max(0, kamera_x // _kachel_groesse)
    letzte_spalte = min(
        welt_breite,
        (kamera_x + bild_breite) // _kachel_groesse + 2)
    erste_zeile = max(0, kamera_y // _kachel_groesse)
    letzte_zeile = min(
        welt_hoehe,
        (kamera_y + bild_hoehe) // _kachel_groesse + 2)
    _2d_zeichnen(
        karten_daten, gitter_an, erste_spalte, letzte_spalte,
        erste_zeile, letzte_zeile, kamera_x, kamera_y,
        bild_breite, bild_hoehe)
