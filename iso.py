"""Isometrische Ansicht: Umrechnung zwischen Raster und Bildschirm.

Die Spiellogik denkt weiter in einem normalen Raster: Jedes Gebaeude steht
auf einer Kachel (spalte, zeile), die Karte ist 60 mal 40 Kacheln gross.
Nur das ZEICHNEN dreht das Raster um 45 Grad und staucht es senkrecht auf
die halbe Hoehe. So entstehen Rauten im Verhaeltnis 2 zu 1 (wie in
OpenTTD oder Die Siedler) und das Bild wirkt dreidimensional.

Alle Umrechnungen stehen absichtlich in DIESEM einen Modul, damit man das
Prinzip an einer Stelle nachlesen kann: raster_zu_welt() malt, und
welt_zu_raster() rechnet Mausklicks zurueck. Hinweis zu den Koordinaten:
Bildschirm-Pixel plus Kamera ergibt Welt-Pixel; in y-Richtung zieht man
zusaetzlich die HUD-Hoehe ab, weil die Ressourcenleiste oben liegt.
"""

import math

# ── Kachel-Masse ─────────────────────────────────────────────────────────────
# Eine Raute ist 96 Pixel breit und 48 Pixel hoch, also genau 2 zu 1.
# Wer die Ansicht flacher oder steiler mag, aendert nur diese zwei Zahlen —
# alle Formeln darunter benutzen die Halbwerte und bleiben richtig.
ISO_KACHEL_BREITE = 96
ISO_KACHEL_HOEHE = 48
ISO_HALB_BREITE = ISO_KACHEL_BREITE // 2    # 48: halbe Rautenbreite
ISO_HALB_HOEHE = ISO_KACHEL_HOEHE // 2      # 24: halbe Rautenhoehe
SICHT_RAND = 2   # Zusatzkacheln rund ums Bild, damit nichts aufblitzt


def raster_zu_welt(spalte, zeile):
    """Rechnet eine Kachel in Welt-Pixel um (fuer das Zeichnen).

    Das Ergebnis ist die OBERE Ecke der Raute: Von dort haengen alle vier
    Ecken ab. Die Formel dreht das Raster um 45 Grad (spalte minus zeile
    fuer x) und staucht es senkrecht (spalte plus zeile, halbe Hoehe).
    """
    welt_x = (spalte - zeile) * ISO_HALB_BREITE
    welt_y = (spalte + zeile) * ISO_HALB_HOEHE
    return welt_x, welt_y


def welt_zu_raster(welt_x, welt_y):
    """Rechnet Welt-Pixel zurueck in eine Kachel (fuer Mausklicks).

    Das ist die Umkehrung von raster_zu_welt und wird gebraucht, damit ein
    Klick genau die Kachel unter dem Mauszeiger trifft. Wir runden mit
    math.floor ab: int() schneidet bei negativen Zahlen Richtung null ab
    und wuerde links und oben neben der Karte falsche Kacheln liefern.
    """
    spalte_genau = (welt_x / ISO_HALB_BREITE + welt_y / ISO_HALB_HOEHE) / 2
    zeile_genau = (welt_y / ISO_HALB_HOEHE - welt_x / ISO_HALB_BREITE) / 2
    return math.floor(spalte_genau), math.floor(zeile_genau)


def kachel_polygon(spalte, zeile, kamera_x, kamera_y):
    """Liefert die vier Ecken einer Raute in Bildschirm-Pixeln.

    Die Reihenfolge oben, rechts, unten, links passt direkt zu
    pygame.draw.polygon. Die Kamera wird hier schon abgezogen, damit der
    Aufrufer keinen Versatz mehr rechnen muss.
    """
    ecke_x, ecke_y = raster_zu_welt(spalte, zeile)
    ecke_x -= kamera_x
    ecke_y -= kamera_y
    oben = (ecke_x, ecke_y)
    rechts = (ecke_x + ISO_HALB_BREITE, ecke_y + ISO_HALB_HOEHE)
    unten = (ecke_x, ecke_y + ISO_KACHEL_HOEHE)
    links = (ecke_x - ISO_HALB_BREITE, ecke_y + ISO_HALB_HOEHE)
    return [oben, rechts, unten, links]


def kachel_mitte(spalte, zeile, kamera_x, kamera_y):
    """Liefert die Mitte einer Raute in Bildschirm-Pixeln.

    Die Mitte ist der fairste Pruefpunkt: Ein Klick genau hier muss immer
    die eigene Kachel treffen, egal wie die Raute gedreht ist. Darum
    benutzen die Tests diesen Punkt fuer jede Kachel der Karte.
    """
    ecke_x, ecke_y = raster_zu_welt(spalte, zeile)
    return ecke_x - kamera_x, ecke_y - kamera_y + ISO_HALB_HOEHE

def kachel_unten_mitte(spalte, zeile, kamera_x, kamera_y):
    """Liefert die untere Ecke einer Raute in Bildschirm-Pixeln.

    Gebaeude-Bilder stehen mit ihrer UNTEREN MITTE auf diesem Punkt: So
    wirkt es, als stuende das Haus wirklich auf der Kachel und nicht
    daneben. Bei grossen Gebaeuden nimmt man die vorderste Kachel.
    """
    ecke_x, ecke_y = raster_zu_welt(spalte, zeile)
    return ecke_x - kamera_x, ecke_y - kamera_y + ISO_KACHEL_HOEHE


def welt_grenzen(karte_breite, karte_hoehe):
    """Liefert das Rechteck um das ganze Rautenfeld in Welt-Pixeln.

    Die Raute ragt links ueber spalte 0 hinaus (bis minus Hoehe mal halbe
    Breite) und reicht unten bis zur Summe beider Seiten. Die Kamera-
    begrenzung in main.py benutzt diese vier Zahlen, damit man nicht ins
    leere Weltall neben der Karte scrollen kann.
    """
    min_x = -karte_hoehe * ISO_HALB_BREITE
    min_y = 0
    max_x = karte_breite * ISO_HALB_BREITE
    max_y = (karte_breite + karte_hoehe) * ISO_HALB_HOEHE
    return min_x, min_y, max_x, max_y


def sichtbarer_bereich(kamera_x, kamera_y, bild_breite, bild_hoehe,
                       karte_breite, karte_hoehe, rand=SICHT_RAND):
    """Berechnet, welche Kacheln gerade im Bild sind (fuer das Culling).

    Statt alle 2400 Kacheln zu pruefen, drehen wir die vier Bildschirm-
    ecken mit welt_zu_raster zurueck ins Raster und nehmen Minimum und
    Maximum. Ein kleiner Rand aussen herum faengt Rundungsfehler ab, und
    das Begrenzen auf die Karte verhindert ungueltige Indizes.
    Die Endwerte sind exklusiv, passen also direkt zu range().
    """
    ecken = [(kamera_x, kamera_y),
             (kamera_x + bild_breite, kamera_y),
             (kamera_x, kamera_y + bild_hoehe),
             (kamera_x + bild_breite, kamera_y + bild_hoehe)]
    spalten = []
    zeilen = []
    for welt_x, welt_y in ecken:
        spalte, zeile = welt_zu_raster(welt_x, welt_y)
        spalten.append(spalte)
        zeilen.append(zeile)
    erste_spalte = max(0, min(spalten) - rand)
    letzte_spalte = min(karte_breite, max(spalten) + rand + 1)
    erste_zeile = max(0, min(zeilen) - rand)
    letzte_zeile = min(karte_hoehe, max(zeilen) + rand + 1)
    return erste_spalte, letzte_spalte, erste_zeile, letzte_zeile


def sortier_schluessel(spalte, zeile):
    """Schluessel fuer die Zeichenreihenfolge: hinten zuerst.

    Weiter hinten heisst kleinere Summe aus spalte plus zeile. Bei
    Gleichstand entscheidet die Zeile: So malt zum Beispiel die Kachel
    (1, 0) vor (0, 1), und vordere Bilder ueberdecken hintere richtig.
    """
    return (spalte + zeile, zeile)


def _fuss_vorne(gebaeude, fussabdruck_funktion):
    """Sucht die vorderste Kachel eines Gebaeudes (fuer die Sortierung).

    Normale Gebaeude stehen auf genau einer Kachel — dann ist das einfach
    ihr Anker (kachel_x, kachel_y). Grosse Gebaeude wie die Universitaet
    belegen mehrere Kacheln; dort zaehlt die Kachel mit der groessten
    Summe, weil sie im Bild am weitesten vorne liegt.
    """
    if fussabdruck_funktion is None:
        return gebaeude["kachel_x"], gebaeude["kachel_y"]
    vorderste = (gebaeude["kachel_x"], gebaeude["kachel_y"])
    for kachel in fussabdruck_funktion(gebaeude):
        if sum(kachel) > sum(vorderste):
            vorderste = kachel
    return vorderste


def zeichen_reihenfolge(gebaeude_liste, fussabdruck_funktion=None):
    """Sortiert Gebaeude von hinten nach vorne (fuer das Zeichnen).

    Ohne Sortierung wuerden hintere Haeuser ploetzlich VOR vorderen
    stehen. Die Liste selbst bleibt unveraendert — es kommt eine neue,
    sortierte Liste zurueck, damit die Spiellogik nichts davon merkt.
    """
    return sorted(
        gebaeude_liste,
        key=lambda gebaeude: sortier_schluessel(
            *_fuss_vorne(gebaeude, fussabdruck_funktion)))
