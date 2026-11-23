"""
===============================================================================
MODUL: panel.py  —  Schwebende Info-Fenster (verschiebbar + minimierbar)
===============================================================================

Warum dieses Modul?
    Im Spiel gibt es mehrere kleine Info-Kaesten: die Ziel-Anzeige, das
    Verteidigungs-Panel, die Bauinfo unten und die Uebersicht links oben.
    Frueher lagen sie an festen Positionen — dabei haben sie sich gegenseitig
    und die Ressourcenleiste verdeckt. Jetzt sind sie schwebende Fenster:
    man kann sie mit der Maus anfassen und verschieben, minimieren oder
    ganz ausblenden.

Bedienung (auch im Hilfe-Overlay mit Taste H):
    * Ziehen     — mit der linken Maustaste auf die TITELZEILE klicken und
                   die Maus bewegen. Das Fenster folgt der Maus.
    * Minimieren — Klick auf den Knopf "–" in der Titelzeile. Dann bleibt
                   nur die Titelzeile stehen (der Knopf wird zu "+").
    * Schliessen — Klick auf "×" blendet das Fenster aus; die Taste holt es zurueck.
    * Tasten     — S = Verteidigung, C = Bauinfo, I = Uebersicht, O = Ziel,
                   L = Layout zuruecksetzen (alle Fenster wieder an ihren Platz).

Wie ein Panel gezeichnet wird:
    panel.zeichnen(schluessel, titel, breite, hoehe, inhalt_funktion, ...)

Dabei ist ``inhalt_funktion(x, y, breite, hoehe)`` eine normale Funktion,
die den INHALT des Fensters malt — sie bekommt die linke obere Ecke des
Inhaltsbereichs (also unterhalb der Titelzeile) und zeichnet direkt auf das
Spielfenster. So kann jedes Modul (hud.py, gegner.py, main.py) seinen eigenen
Inhalt malen, ohne dass panel.py dessen Daten kennen muss.

Merksatz (Trennung von Logik und Anzeige):
    Panel-Zustand = Position, minimiert, sichtbar.
    Inhalt        = was drinsteht (kommt von hud, gegner oder main).
===============================================================================
"""

import pygame


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 1: KONSTANTEN UND MODUL-VARIABLEN
# ═════════════════════════════════════════════════════════════════════════════

TITEL_HOEHE = 22      # Hoehe der Titelleiste in Pixeln
KNOPF_GROESSE = 16    # Kantenlaenge der Knoepfe "–"/"+" und "×"
RAND_INNEN = 6        # Innenabstand zwischen Fensterrand und Inhalt
RAND_FENSTER = 4      # Mindestabstand zum Bildschirmrand beim Verschieben

FARBE_RAHMEN = (95, 130, 190)
FARBE_RAHMEN_AKTIV = (150, 200, 255)
FARBE_TITEL = (34, 48, 78)
FARBE_KNOPF = (58, 76, 108)
FARBE_HINTERGRUND = (15, 21, 38)
FARBE_TEXT = (235, 240, 255)

_fenster = None
_standard = {}            # schluessel -> (x, y) Standardposition
_zustand = {}             # schluessel -> {"x", "y", "minimiert", "sichtbar"}
_reihenfolge = []         # Reihenfolge der zuletzt gezeichneten Panels
_rects = {}               # schluessel -> pygame.Rect des letzten Frames
_ziehen = None            # (schluessel, versatz_x, versatz_y) beim Ziehen
_font_cache = {}


def initialisieren(fenster_obj):
    """Merkt sich das Spielfenster (wie in den anderen Modulen)."""
    global _fenster
    _fenster = fenster_obj


def _font(groesse):
    """Wiederverwendbare Schrift (nicht jeden Frame neu erzeugen)."""
    if groesse not in _font_cache:
        _font_cache[groesse] = pygame.font.Font(None, groesse)
    return _font_cache[groesse]


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 2: ZUSTAND — Position, minimiert, sichtbar
# ═════════════════════════════════════════════════════════════════════════════

def standard_setzen(schluessel, x, y):
    """Legt fest, wo ein Panel nach dem Start (oder nach Taste L) sitzt."""
    _standard[schluessel] = (int(x), int(y))
    zustand = _zustand.setdefault(
        schluessel, {"x": int(x), "y": int(y), "minimiert": False,
                     "sichtbar": True})
    zustand["x"], zustand["y"] = int(x), int(y)


def _hole(schluessel, standard_x=10, standard_y=100):
    """Liefert den Zustand eines Panels und legt ihn beim ersten Mal an."""
    if schluessel not in _zustand:
        _standard.setdefault(schluessel, (int(standard_x), int(standard_y)))
        _zustand[schluessel] = {"x": int(standard_x), "y": int(standard_y),
                                "minimiert": False, "sichtbar": True,
                                "breite": 200, "hoehe": TITEL_HOEHE}
    return _zustand[schluessel]


def zustand_zuruecksetzen():
    """Alle Panels auf Standardposition, ausgeklappt und sichtbar setzen."""
    for schluessel, (x, y) in _standard.items():
        zustand = _zustand.setdefault(
            schluessel, {"x": x, "y": y, "minimiert": False,
                         "sichtbar": True})
        zustand["x"], zustand["y"] = x, y
        zustand["minimiert"] = False
        zustand["sichtbar"] = True
    global _ziehen
    _ziehen = None


def ist_sichtbar(schluessel):
    """Ist das Panel gerade eingeblendet?"""
    return _zustand.get(schluessel, {}).get("sichtbar", True)


def ist_minimiert(schluessel):
    """Ist vom Panel nur noch die Titelzeile zu sehen?"""
    return _zustand.get(schluessel, {}).get("minimiert", False)


def position(schluessel):
    """Aktuelle Position (x, y) oder None, wenn das Panel unbekannt ist."""
    zustand = _zustand.get(schluessel)
    if not zustand:
        return None
    return (zustand["x"], zustand["y"])


def sichtbar_setzen(schluessel, an):
    _hole(schluessel)["sichtbar"] = bool(an)


def umschalten(schluessel):
    """Panel ein- oder ausblenden (Taste) — dasselbe wie der ×-Knopf."""
    zustand = _hole(schluessel)
    zustand["sichtbar"] = not zustand["sichtbar"]
    return zustand["sichtbar"]


def minimieren_setzen(schluessel, an):
    _hole(schluessel)["minimiert"] = bool(an)


def verschieben(schluessel, x, y):
    """Verschiebt ein Panel und haelt es im Fenster (es kann nicht wegfliegen)."""
    zustand = _hole(schluessel)
    breite = zustand.get("breite", 200)
    hoehe = zustand.get("hoehe", TITEL_HOEHE)
    fenster_breite = _fenster.get_width() if _fenster else 1000
    fenster_hoehe = _fenster.get_height() if _fenster else 700
    max_x = max(RAND_FENSTER, fenster_breite - breite - RAND_FENSTER)
    max_y = max(RAND_FENSTER, fenster_hoehe - hoehe - RAND_FENSTER)
    zustand["x"] = int(max(RAND_FENSTER, min(max_x, x)))
    zustand["y"] = int(max(RAND_FENSTER, min(max_y, y)))
    return (zustand["x"], zustand["y"])


def panel_rect(schluessel):
    """Rechteck des Panels im zuletzt gezeichneten Frame (oder None)."""
    return _rects.get(schluessel)


def titel_rect(schluessel):
    """Rechteck der Titelleiste (die Ziehflaeche) aus dem letzten Frame."""
    rect = _rects.get(schluessel)
    if rect is None:
        return None
    return pygame.Rect(rect.x, rect.y, rect.width, TITEL_HOEHE)


def frame_start():
    """Wird von main.py zu Beginn jedes Frames aufgerufen.

    Leert die Merkliste der Fensterrechtecke. Nur Fenster, die in DIESEM
    Frame gezeichnet werden, sind danach auffindbar — sonst wuerde ein
    ausgeblendetes Fenster (z.B. das Ziel-Fenster) weiter als Trefferzone
    fuer Mausklicks gelten.
    """
    _rects.clear()
    _reihenfolge.clear()


def schluessel_bei_position(pos):
    """Welches Panel liegt unter dieser Mausposition? Oberstes zuerst."""
    for schluessel in reversed(_reihenfolge):
        if not ist_sichtbar(schluessel):
            continue
        rect = _rects.get(schluessel)
        if rect is not None and rect.collidepoint(pos):
            return schluessel
    return None


def knopf_rechtecke(schluessel):
    """Rechtecke der Knoepfe "minimieren" und "schliessen" der Titelzeile."""
    titel = titel_rect(schluessel)
    if titel is None:
        return {}
    y = titel.y + (TITEL_HOEHE - KNOPF_GROESSE) // 2
    schliessen = pygame.Rect(titel.right - RAND_INNEN - KNOPF_GROESSE, y,
                             KNOPF_GROESSE, KNOPF_GROESSE)
    minimieren = pygame.Rect(schliessen.left - KNOPF_GROESSE - 4, y,
                             KNOPF_GROESSE, KNOPF_GROESSE)
    return {"minimieren": minimieren, "schliessen": schliessen}


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 3: ZEICHNEN — Hintergrund, Inhalt, Titelzeile mit Knoepfen
# ═════════════════════════════════════════════════════════════════════════════

def zeichnen(schluessel, titel, breite, hoehe, inhalt_funktion,
             standard_x=10, standard_y=100, akzent=None):
    """Zeichnet ein Panel und ruft fuer den Inhalt die uebergebene Funktion.

    Parameter:
        schluessel      — eindeutiger Name ("ziel", "bauinfo", ...)
        titel           — Text in der Titelzeile (auch Ziehflaeche)
        breite          — Breite in Pixeln (ganzes Fenster)
        hoehe           — Hoehe des INHALTS (die Titelzeile kommt automatisch dazu)
        inhalt_funktion — Funktion(x, y, breite, hoehe), malt den Inhalt
        standard_x/y    — Position beim ersten Aufruf / nach Taste L
        akzent          — Rahmenfarbe (z.B. Gebaeudefarbe); sonst Blau

    Rueckgabe: pygame.Rect des Fensters (oder None, wenn ausgeblendet).
    """
    if _fenster is None:
        return None
    zustand = _hole(schluessel, standard_x, standard_y)
    if not zustand["sichtbar"]:
        _rects.pop(schluessel, None)
        return None

    minimiert = bool(zustand["minimiert"])
    gesamthoehe = TITEL_HOEHE + (0 if minimiert else hoehe + 2 * RAND_INNEN)
    zustand["breite"], zustand["hoehe"] = breite, gesamthoehe
    x, y = verschieben(schluessel, zustand["x"], zustand["y"])
    rect = pygame.Rect(x, y, breite, gesamthoehe)
    _rects[schluessel] = rect

    # Zeichenreihenfolge merken: das zuletzt gezeichnete Panel liegt oben.
    if schluessel in _reihenfolge:
        _reihenfolge.remove(schluessel)
    _reihenfolge.append(schluessel)

    farbe = akzent if akzent else FARBE_RAHMEN

    # 1) Hintergrund des Fensters
    hintergrund = pygame.Surface(rect.size, pygame.SRCALPHA)
    hintergrund.fill((FARBE_HINTERGRUND[0], FARBE_HINTERGRUND[1],
                      FARBE_HINTERGRUND[2], 236))
    _fenster.blit(hintergrund, rect.topleft)

    # 2) Inhalt — er bekommt die linke obere Ecke UNTER der Titelzeile
    if not minimiert and inhalt_funktion is not None:
        inhalt_funktion(rect.x + RAND_INNEN,
                        rect.y + TITEL_HOEHE + RAND_INNEN,
                        breite - 2 * RAND_INNEN, hoehe)

    # 3) Titelzeile (Ziehflaeche) + Knoepfe
    py_titel = pygame.Rect(rect.x, rect.y, rect.width, TITEL_HOEHE)
    pygame.draw.rect(_fenster, FARBE_TITEL, py_titel)
    pygame.draw.rect(_fenster, farbe, py_titel, 1)
    schrift = _font(17)
    _fenster.blit(schrift.render(titel, True, FARBE_TEXT),
                  (py_titel.x + 7, py_titel.y + 5))

    zeichen = {"minimieren": "+" if minimiert else "-", "schliessen": "X"}
    for name, knopf in knopf_rechtecke(schluessel).items():
        pygame.draw.rect(_fenster, FARBE_KNOPF, knopf, border_radius=3)
        pygame.draw.rect(_fenster, farbe, knopf, 1, border_radius=3)
        symbol = schrift.render(zeichen[name], True, (225, 232, 245))
        _fenster.blit(symbol, symbol.get_rect(center=knopf.center))

    # 4) Rahmen zum Schluss, damit er sauber ueber allem liegt
    pygame.draw.rect(_fenster, farbe, rect, 2, border_radius=3)
    return rect


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 4: MAUSBEDIENTNG — Ziehen, Minimieren, Schliessen
# ═════════════════════════════════════════════════════════════════════════════

def maus_ereignis(ereignis):
    """Verarbeitet ein Mausereignis fuer alle Panels.

    Rueckgabe True bedeutet: Ein Panel hat das Ereignis verbraucht. main.py
    darf dann NICHT zusaetzlich ein Gebaeude bauen oder abreissen.
    """
    global _ziehen
    if _fenster is None:
        return False

    if ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1:
        schluessel = schluessel_bei_position(ereignis.pos)
        if schluessel is None:
            return False
        knoepfe = knopf_rechtecke(schluessel)
        if knoepfe["minimieren"].collidepoint(ereignis.pos):
            zustand = _zustand[schluessel]
            zustand["minimiert"] = not zustand["minimiert"]
            return True
        if knoepfe["schliessen"].collidepoint(ereignis.pos):
            _zustand[schluessel]["sichtbar"] = False
            return True
        titel = titel_rect(schluessel)
        if titel is not None and titel.collidepoint(ereignis.pos):
            # Ziehen beginnen: Abstand Maus <-> Fensterecke merken, damit
            # das Fenster beim Bewegen nicht springt.
            x, y = position(schluessel)
            _ziehen = (schluessel, ereignis.pos[0] - x, ereignis.pos[1] - y)
            return True
        # Klick in den Inhalt: verbrauchen, sonst baut man unter dem Fenster.
        return True

    if ereignis.type == pygame.MOUSEMOTION and _ziehen is not None:
        schluessel, versatz_x, versatz_y = _ziehen
        verschieben(schluessel, ereignis.pos[0] - versatz_x,
                    ereignis.pos[1] - versatz_y)
        return True

    if (ereignis.type == pygame.MOUSEBUTTONUP and ereignis.button == 1
            and _ziehen is not None):
        _ziehen = None
        return True

    return False


def zieht_gerade():
    """Wird gerade ein Panel gezogen? (für Tests und Statusanzeigen)"""
    return _ziehen is not None


