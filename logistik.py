"""
===============================================================================
MODUL: logistik.py  —  Strassen, Netz und Versorgung (Fortgeschrittener Kurs)
===============================================================================

Die Spielidee (Wunsch der Schuelerinnen und Schueler)
    Die Basis ist das Zentrum der Kolonie. Strassen verbinden die Gebaeude mit
    der Basis. Nur Gebaeude, die an diesem Strassennetz haengen, koennen
    arbeiten: Sie produzieren, verbrauchen Rohstoffe und belegen Personal.
    Ohne Strasse steht ein Gebaeude still - es zeigt ein gelbes Warndreieck.

Wie funktioniert das Netz?
    1. Alle Strassenkacheln werden eingesammelt (Gebaeudetyp ``STRASSE_TYP``).
    2. Eine Breitensuche (BFS) startet bei allen Strassen, die direkt
       (Nachbarschaft in vier Richtungen) an die Basis grenzen.
    3. Von dort laeuft die Suche ueber benachbarte Strassen weiter: Genau
       diese Strassen bilden das Netz.
    4. Ein Gebaeude ist angebunden, wenn eine Kachel seines Grundrisses direkt
       an die Basis oder an eine Netz-Strasse grenzt. Mehrkachel-Gebaeude wie
       die Universitaet (2x3) werden dabei ueber ihre ganze Flaeche geprueft.

Effizienz
    Das Netz wird nur dann neu berechnet, wenn sich etwas aendern KANN:
    beim Bauen, beim Abreissen, beim Laden und beim neuen Spiel. Nicht in
    jedem Frame - deshalb bleibt das Spiel fluessig.

Tasten und Einstellungen
    V  — Logistik-Ansicht ein-/ausschalten (Netz gruen, stillstehende
         Gebaeude rot markiert).
    LOGISTIK_AKTIV — Schalter fuer Tests oder fuer ein Spiel ohne Strassen.
    BRAUCHT_STRASSENANBINDUNG — Ausnahmeliste: Typ-Index → True/False.

Nicht umgesetzt (Ideen fuer Schueler, siehe auch das Schuelerhandbuch):
    Wegstrecken-Malus, Strassenkapazitaet und sichtbare Transportfahrzeuge.
===============================================================================
"""

import pygame

import gebaeude


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 1: KONSTANTEN (hier kannst du alles einstellen)
# ═════════════════════════════════════════════════════════════════════════════

# Hauptschalter: False = Strassen sind reine Deko (wie in alten Versionen).
# Bestehende Tests, die Gebaeude ohne Strassen bauen, setzen ihn auf False.
LOGISTIK_AKTIV = True

# Die beiden wichtigsten Gebaeudetypen fuer dieses Modul.
BASIS_TYP = 0
STRASSE_TYP = 9

# Grund, der in einem stillstehenden Gebaeude gespeichert wird. Die Anzeige
# (HUD, Warndreieck) liest genau diesen Text.
STILLSTAND_GRUND = "Keine Straßenanbindung"

# Farben der Logistik-Ansicht
FARBE_NETZ = (90, 235, 140)          # Netzstrassen: kraeftiges Gruen
FARBE_NETZ_ALPHA = 90                # Transparenz der gruenen Markierung
FARBE_WARNUNG = (255, 90, 90)        # Nicht angebundene Gebaeude: rot
FARBE_TEXT = (235, 245, 255)

# ── Braucht dieses Gebaeude eine Strassenanbindung? ────────────────────────
# Aufbau: {Typ-Index: True/False}. Standard: alle Gebaeude brauchen eine
# Strasse. Ausnahmen sind Basis (0), Strasse (9) und Park (19).
# Schuelerinnen und Schueler koennen hier einfach Werte aendern, z. B.
# BRAUCHT_STRASSENANBINDUNG[2] = False, damit Farmen ohne Strasse arbeiten.
BRAUCHT_STRASSENANBINDUNG = {
    typ_index: True for typ_index in range(len(gebaeude.GEBAEUDE_TYPEN))
}
BRAUCHT_STRASSENANBINDUNG[BASIS_TYP] = False     # Die Basis ist das Zentrum
BRAUCHT_STRASSENANBINDUNG[STRASSE_TYP] = False   # Strassen sind das Netz selbst
BRAUCHT_STRASSENANBINDUNG[19] = False            # Der Park braucht keine Strasse


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 2: MODUL-VARIABLEN
# ═════════════════════════════════════════════════════════════════════════════

_fenster = None            # Pygame-Fenster fuer die Logistik-Ansicht
_netz_kacheln = set()      # alle Strassenkacheln, die am Netz haengen
_aktualisierungen = 0      # Zaehler: wie oft wurde das Netz neu berechnet?
_ansicht_aktiv = False     # Ist die Logistik-Ansicht (Taste V) eingeschaltet?


def initialisieren(fenster_obj):
    """Merkt sich das Pygame-Fenster (einmal beim Spielstart aufrufen)."""
    global _fenster
    _fenster = fenster_obj


def zustand_zuruecksetzen():
    """Loescht Netz und Ansicht — zum Beispiel fuer ein neues Spiel."""
    global _netz_kacheln, _ansicht_aktiv, _aktualisierungen
    _netz_kacheln = set()
    _ansicht_aktiv = False
    _aktualisierungen = 0


def zustand_exportieren():
    """Gibt die Logistik-Einstellungen fuer einen Spielstand zurueck.

    Das Netz selbst wird NICHT gespeichert: Es laesst sich aus den Gebaeuden
    jederzeit wieder berechnen. Nur die Ansicht ist eine Spielereinstellung.
    """
    return {
        "ansicht_aktiv": bool(_ansicht_aktiv),
        "logistik_aktiv": bool(LOGISTIK_AKTIV),
    }


def zustand_importieren(daten):
    """Stellt die Logistik-Einstellungen aus einem Spielstand wieder her."""
    global _ansicht_aktiv, _netz_kacheln
    daten = daten if isinstance(daten, dict) else {}
    _ansicht_aktiv = bool(daten.get("ansicht_aktiv", False))
    # Nach dem Laden ist das Netz unbekannt und wird neu berechnet.
    _netz_kacheln = set()


def braucht_anbindung(typ_index):
    """True, wenn dieser Gebaeudetyp eine Strasse zur Basis braucht."""
    return bool(BRAUCHT_STRASSENANBINDUNG.get(typ_index, True))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 3: DAS STRASSENNETZ BERECHNEN
# ═════════════════════════════════════════════════════════════════════════════

def _kacheln_von(gebaeude_daten):
    """Liefert alle Kacheln, die ein Gebaeude belegt (Grundriss)."""
    return gebaeude.gebaeude_flaeche(
        gebaeude_daten.get("typ", 0),
        gebaeude_daten.get("kachel_x", 0),
        gebaeude_daten.get("kachel_y", 0))


def _grenzt_an(kachel, kachel_menge):
    """Prueft, ob eine Kachel in vier Richtungen an eine Kachelmenge grenzt.

    Die Nachbarschaft in vier Richtungen (oben, unten, links, rechts) ist
    einfach zu verstehen und leicht zu zeichnen. Diagonal zaehlt NICHT.
    """
    x, y = kachel
    return ((x + 1, y) in kachel_menge or (x - 1, y) in kachel_menge or
            (x, y + 1) in kachel_menge or (x, y - 1) in kachel_menge)


def basis_kacheln(liste_gebaeude):
    """Sammelt alle Kacheln der Basis (normalerweise genau eine)."""
    kacheln = set()
    for ein_gebaeude in liste_gebaeude:
        if ein_gebaeude.get("typ") == BASIS_TYP:
            kacheln.update(_kacheln_von(ein_gebaeude))
    return kacheln


def netz_berechnen(liste_gebaeude):
    """Berechnet alle Strassenkacheln, die mit der Basis verbunden sind.

    Rueckgabe: ein ``set`` mit (kachel_x, kachel_y)-Tupeln.
    """
    basis = basis_kacheln(liste_gebaeude)

    # Alle Strassenkacheln sammeln (ohne Basis gibt es kein Netz).
    alle_strassen = set()
    for ein_gebaeude in liste_gebaeude:
        if ein_gebaeude.get("typ") == STRASSE_TYP:
            alle_strassen.update(_kacheln_von(ein_gebaeude))

    # ── Breitensuche (BFS) ────────────────────────────────────────────────
    # Wir starten bei allen Strassen, die direkt an die Basis grenzen, und
    # laufen dann Schritt fuer Schritt ueber benachbarte Strassen weiter.
    netz = set()
    warteschlange = []
    for kachel in alle_strassen:
        if _grenzt_an(kachel, basis):
            netz.add(kachel)
            warteschlange.append(kachel)

    while warteschlange:
        x, y = warteschlange.pop()
        for nachbar in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nachbar in alle_strassen and nachbar not in netz:
                netz.add(nachbar)
                warteschlange.append(nachbar)
    return netz


def netz_aktualisieren(liste_gebaeude):
    """Berechnet das Netz neu und markiert nicht angebundene Gebaeude.

    Rueckgabe: ein Dictionary mit Zahlen fuer HUD, Tests und Achievements:
        {"netz_kacheln": ..., "ohne_anbindung": ...}

    Diese Funktion darf NICHT in jedem Frame aufgerufen werden. Sie wird nur
    nach Bauen, Abriss, Laden und neuem Spiel aufgerufen.
    """
    global _netz_kacheln, _aktualisierungen
    _aktualisierungen += 1

    if not LOGISTIK_AKTIV:
        # Logistik abgeschaltet: Alle Gebaeude arbeiten wie frueher. Deshalb
        # loeschen wir alle Stillstands-Gruende wieder.
        for ein_gebaeude in liste_gebaeude:
            ein_gebaeude.pop("stillstand_grund", None)
        _netz_kacheln = set()
        return {"netz_kacheln": 0, "ohne_anbindung": 0}

    netz = netz_berechnen(liste_gebaeude)
    basis = basis_kacheln(liste_gebaeude)
    _netz_kacheln = netz

    ohne_anbindung = 0
    for ein_gebaeude in liste_gebaeude:
        # Ausnahmen (Basis, Strasse, Park): kein Stillstand, keine Warnung.
        if not braucht_anbindung(ein_gebaeude.get("typ", -1)):
            ein_gebaeude.pop("stillstand_grund", None)
            continue

        angebunden = False
        for kachel in _kacheln_von(ein_gebaeude):
            # Zwei Faelle zaehlen als angebunden:
            #   1. Die Kachel liegt selbst im Netz (kompakte Bauweise).
            #   2. Die Kachel grenzt an eine Netzstrasse oder an die Basis.
            if (kachel in netz or kachel in basis or
                    _grenzt_an(kachel, netz) or _grenzt_an(kachel, basis)):
                angebunden = True
                break

        if angebunden:
            # Sobald die Strasse da ist, verschwindet die Warnung wieder.
            ein_gebaeude.pop("stillstand_grund", None)
        else:
            ein_gebaeude["stillstand_grund"] = STILLSTAND_GRUND
            ein_gebaeude["arbeitet"] = False
            ohne_anbindung += 1

    return {"netz_kacheln": len(netz), "ohne_anbindung": ohne_anbindung}


def netz_kacheln():
    """Kopie der aktuellen Netzstrassen (fuer Ansicht und Tests)."""
    return set(_netz_kacheln)


def ist_angebunden(ein_gebaeude):
    """Einfache Abfrage fuer andere Module: arbeitet dieses Gebaeude frei?"""
    return not ein_gebaeude.get("stillstand_grund")


def anzahl_ohne_anbindung(liste_gebaeude):
    """Zaehlt Gebaeude, die laut letzter Berechnung keine Strasse haben."""
    return sum(1 for ein_gebaeude in liste_gebaeude
               if ein_gebaeude.get("stillstand_grund"))


def aktualisierungen():
    """Wie oft wurde das Netz insgesamt neu berechnet? (fuer Tests und Doku)"""
    return _aktualisierungen


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 4: LOGISTIK-ANSICHT (Taste V)
# ═════════════════════════════════════════════════════════════════════════════

def ansicht_umschalten():
    """Schaltet die Logistik-Ansicht ein oder aus. Rueckgabe: neuer Zustand."""
    global _ansicht_aktiv
    _ansicht_aktiv = not _ansicht_aktiv
    return _ansicht_aktiv


def ansicht_aktiv():
    """Ist die Logistik-Ansicht gerade sichtbar?"""
    return _ansicht_aktiv


def _kachel_rechteck(kacheln, kamera_x, kamera_y, kachel_groesse):
    """Baut ein Rechteck um einen ganzen Gebaeude-Grundriss."""
    xs = [kachel[0] for kachel in kacheln]
    ys = [kachel[1] for kachel in kacheln]
    return pygame.Rect(min(xs) * kachel_groesse - kamera_x,
                       min(ys) * kachel_groesse - kamera_y,
                       (max(xs) - min(xs) + 1) * kachel_groesse,
                       (max(ys) - min(ys) + 1) * kachel_groesse)


def _ist_sichtbar(rect):
    """Schnelle Pruefung, ob ein Rechteck im Fenster liegt."""
    if _fenster is None:
        return False
    return not (rect.right < 0 or rect.bottom < 0 or
                rect.left > _fenster.get_width() or
                rect.top > _fenster.get_height())


def zeichnen(liste_gebaeude, kamera_x, kamera_y, kachel_groesse):
    """Zeichnet die Logistik-Ansicht ueber die Welt.

    Gruene Kacheln = Strassennetz an der Basis
    Rote Rahmen    = Gebaeude ohne Strassenanbindung
    """
    if _fenster is None or not _ansicht_aktiv:
        return

    # ── Schritt 1: Netzstrassen gruen hinterlegen ────────────────────────
    # Eine halbtransparente Flaeche liegt ueber der Welt, damit man die
    # Strassen und Gebaeude trotzdem noch erkennt.
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    for (kachel_x, kachel_y) in _netz_kacheln:
        rect = pygame.Rect(kachel_x * kachel_groesse - kamera_x,
                           kachel_y * kachel_groesse - kamera_y,
                           kachel_groesse, kachel_groesse)
        if _ist_sichtbar(rect):
            overlay.fill((FARBE_NETZ[0], FARBE_NETZ[1], FARBE_NETZ[2],
                          FARBE_NETZ_ALPHA), rect)
    _fenster.blit(overlay, (0, 0))

    # ── Schritt 2: Nicht angebundene Gebaeude rot umranden ──────────────
    schrift = pygame.font.Font(None, 17)
    stillstehende = []
    for ein_gebaeude in liste_gebaeude:
        if not ein_gebaeude.get("stillstand_grund"):
            continue
        rect = _kachel_rechteck(_kacheln_von(ein_gebaeude),
                                kamera_x, kamera_y, kachel_groesse)
        if _ist_sichtbar(rect):
            pygame.draw.rect(_fenster, FARBE_WARNUNG, rect, 3)
        stillstehende.append(ein_gebaeude)

    # ── Schritt 3: Legende und Liste der stillstehenden Gebaeude ─────────
    zeilen = ["LOGISTIK-ANSICHT (V schliesst die Ansicht)",
              "Gruen = Strassennetz an der Basis"]
    if stillstehende:
        zeilen.append("Rot markiert - " + STILLSTAND_GRUND + ":")
        for ein_gebaeude in stillstehende[:6]:
            name = gebaeude.GEBAEUDE_TYPEN[ein_gebaeude.get("typ", 0)]["name"]
            zeilen.append(f"   {name} bei ({ein_gebaeude.get('kachel_x')}, "
                          f"{ein_gebaeude.get('kachel_y')})")
        if len(stillstehende) > 6:
            zeilen.append(f"   ... und {len(stillstehende) - 6} weitere")
    else:
        zeilen.append("Alle Gebaeude sind angebunden.")

    y = 200
    for zeile in zeilen:
        text = schrift.render(zeile, True, FARBE_TEXT)
        hintergrund = pygame.Surface((text.get_width() + 12, 20),
                                     pygame.SRCALPHA)
        hintergrund.fill((8, 14, 28, 200))
        _fenster.blit(hintergrund, (12, y - 2))
        _fenster.blit(text, (18, y))
        y += 20

