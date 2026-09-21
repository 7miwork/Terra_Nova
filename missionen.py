"""Missionszentrale der Weltraum-Kolonie.

Dieses Modul ist absichtlich einfach aufgebaut. Jede Mission ist nur ein
Dictionary in der Liste ``MISSIONEN``. Dadurch können Schülerinnen und
Schüler später selbst neue Aufgaben ergänzen, ohne die Spielschleife neu zu
schreiben.

Wichtige Grundidee:

    Mission = Bedingung + Fortschritt + Belohnung

Das Spiel liefert in ``pruefen()`` einen Kontext mit aktuellen Zahlen. Das
Missionsmodul prüft die Bedingungen und meldet nur neue Abschlüsse zurück.
Die Auszahlung der Belohnung übernimmt anschließend ``main.py``.
"""

import pygame


# ---------------------------------------------------------------------------
# 1. MISSIONSLISTE
# ---------------------------------------------------------------------------
# Eine Mission besteht aus:
#   id           : eindeutiger Name für den Computer
#   titel        : Name im Spielmenü
#   beschreibung: Erklärung für die Spielerinnen und Spieler
#   bedingungen : eine oder mehrere Zahlenziele
#   belohnung    : Ressourcen, die einmalig ausgezahlt werden
#
# Die Bedingungen werden mit UND verknüpft. Bei "erste_kolonie" muss also
# nur ein Gebäude gebaut werden. Eine spätere Mission könnte einfach mehrere
# Bedingungen bekommen, zum Beispiel Gebäude UND Bevölkerung.
MISSIONEN = [
    {
        "id": "erste_kolonie",
        "titel": "Erste Kolonie",
        "beschreibung": "Baue dein erstes Gebäude.",
        "bedingungen": [("gebaeude_gesamt", 1)],
        "belohnung": {"gold": 50},
    },
    {
        "id": "stromversorgung",
        "titel": "Stromversorgung",
        "beschreibung": "Baue einen Reaktor.",
        "bedingungen": [("gebaeude_typ_1", 1)],
        "belohnung": {"holz": 30},
    },
    {
        "id": "gruener_daumen",
        "titel": "Grüner Daumen",
        "beschreibung": "Baue eine Farm.",
        "bedingungen": [("gebaeude_typ_2", 1)],
        "belohnung": {"stein": 30},
    },
    {
        "id": "wohnraum",
        "titel": "Wohnraum schaffen",
        "beschreibung": "Baue drei Wohnhäuser.",
        "bedingungen": [("gebaeude_typ_6", 3)],
        "belohnung": {"gold": 75},
    },
    {
        "id": "forschungslabor",
        "titel": "Forschungslabor",
        "beschreibung": "Erforsche deine erste Technologie.",
        "bedingungen": [("forschungen", 1)],
        "belohnung": {"forschung": 25},
    },
    {
        "id": "meisterbauer",
        "titel": "Meisterbauer",
        "beschreibung": "Baue insgesamt zehn Gebäude.",
        "bedingungen": [("gebaeude_gesamt", 10)],
        "belohnung": {"gold": 100},
    },
    {
        "id": "handelsabkommen",
        "titel": "Handelsabkommen",
        "beschreibung": "Führe drei Handelsaktionen durch.",
        "bedingungen": [("handelsaktionen", 3)],
        "belohnung": {"gold": 75},
    },
    {
        "id": "terraformer",
        "titel": "Terraformer",
        "beschreibung": "Wandle fünf Kacheln in fruchtbaren Boden um.",
        "bedingungen": [("terraformierungen", 5)],
        "belohnung": {"nahrung": 50},
    },
    {
        "id": "stahlzeit",
        "titel": "Stahlzeit",
        "beschreibung": "Lagere mindestens zehn Stahl ein.",
        "bedingungen": [("stahl", 10)],
        "belohnung": {"gold": 100},
    },
    {
        "id": "roboterhilfe",
        "titel": "Roboterhilfe",
        "beschreibung": "Besitze mindestens fünf Roboter.",
        "bedingungen": [("roboter", 5)],
        "belohnung": {"kohle": 25},
    },
    {
        "id": "bevoelkerungsboom",
        "titel": "Bevölkerungsboom",
        "beschreibung": "Erreiche 25 Bewohner.",
        "bedingungen": [("bevoelkerung", 25)],
        "belohnung": {"energie": 50},
    },
    {
        "id": "ueberlebender",
        "titel": "Überlebender",
        "beschreibung": "Erreiche 20 Wirtschaftsticks.",
        "bedingungen": [("wirtschafts_ticks", 20)],
        "belohnung": {"nahrung": 75},
    },
    {
        "id": "koloniezentrum",
        "titel": "Zentrum der Kolonie",
        "beschreibung": "Baue das Koloniezentrum.",
        "bedingungen": [("gebaeude_typ_17", 1)],
        "belohnung": {"forschung": 75},
    },
    {
        "id": "vollausbau",
        "titel": "Vollausbau",
        "beschreibung": "Baue insgesamt 20 Gebäude.",
        "bedingungen": [("gebaeude_gesamt", 20)],
        "belohnung": {"gold": 200},
    },
    {
        "id": "missionsmeister",
        "titel": "Missionsmeister",
        "beschreibung": "Schließe zehn andere Missionen ab.",
        "bedingungen": [("missionen_erledigt", 10)],
        "belohnung": {"forschung": 100, "gold": 100},
    },
    {
        "id": "gruene_oase",
        "titel": "Grüne Oase",
        "beschreibung": "Baue einen Park für die Kolonie.",
        "bedingungen": [("gebaeude_typ_19", 1)],
        "belohnung": {"nahrung": 50, "gold": 25},
    },
    {
        "id": "sonnenkraft",
        "titel": "Sonnenkraft",
        "beschreibung": "Baue einen Solarreaktor.",
        "bedingungen": [("gebaeude_typ_20", 1)],
        "belohnung": {"energie": 75, "forschung": 25},
    },
    {
        "id": "zufriedene_kolonie",
        "titel": "Zufriedene Kolonie",
        "beschreibung": "Erreiche mindestens +30 Zufriedenheit.",
        "bedingungen": [("zufriedenheit", 30)],
        "belohnung": {"gold": 100, "nahrung": 50},
    },
    # Fortgeschrittener Kurs (Logistik): Die erste Strasse verbindet die
    # Kolonie mit der Basis und schaltet das Strassennetz frei.
    {
        "id": "erste_strasse",
        "titel": "Erste Strasse",
        "beschreibung": "Baue eine Strasse von der Basis zu einem Gebaeude.",
        "bedingungen": [("gebaeude_typ_9", 1)],
        "belohnung": {"stein": 25},
    },
]

_fenster = None
_erledigt = set()
_zaehler = {}


# ---------------------------------------------------------------------------
# 2. ZUSTAND
# ---------------------------------------------------------------------------
def initialisieren(fenster_obj):
    """Merkt sich das Pygame-Fenster für die spätere Menüzeichnung."""
    global _fenster
    _fenster = fenster_obj


def zustand_zuruecksetzen():
    """Löscht alle Missionsabschlüsse, zum Beispiel für einen neuen Kurs."""
    global _erledigt, _zaehler
    _erledigt = set()
    _zaehler = {}


def zustand_exportieren():
    """Gibt einen einfachen, JSON-kompatiblen Dictionary-Zustand zurück."""
    return {"erledigt": sorted(_erledigt), "zaehler": dict(_zaehler)}


def zustand_importieren(daten):
    """Stellt Missionsabschlüsse und Zähler aus einem Spielstand wieder her."""
    global _erledigt, _zaehler
    daten = daten if isinstance(daten, dict) else {}
    gueltige_ids = {mission["id"] for mission in MISSIONEN}

    # Nur IDs aus unserer aktuellen Missionsliste werden übernommen. So kann
    # eine beschädigte oder von Schülerinnen und Schülern falsch geschriebene
    # JSON-Datei nicht zu einem KeyError im Menü führen.
    erledigt = daten.get("erledigt", [])
    if not isinstance(erledigt, list):
        erledigt = []
    _erledigt = {str(wert) for wert in erledigt if str(wert) in gueltige_ids}

    zaehler = daten.get("zaehler", {})
    _zaehler = {}
    if isinstance(zaehler, dict):
        for schluessel, wert in zaehler.items():
            try:
                _zaehler[str(schluessel)] = max(0.0, float(wert))
            except (TypeError, ValueError):
                # Ungültige Werte werden ignoriert. Das restliche Laden darf
                # wegen eines einzelnen falschen Zählers nicht abbrechen.
                continue


def gebaeude_gebaut(typ_index):
    """Erhöht den Gesamtzähler nach einem erfolgreichen Bauvorgang."""
    _zaehler["gebaeude_gesamt"] = _zaehler.get("gebaeude_gesamt", 0) + 1
    schluessel = f"gebaeude_typ_{typ_index}"
    _zaehler[schluessel] = _zaehler.get(schluessel, 0) + 1


def terraformiert():
    """Zählt eine erfolgreich in fruchtbaren Boden umgewandelte Kachel."""
    _zaehler["terraformierungen"] = _zaehler.get("terraformierungen", 0) + 1


def erledigte_anzahl():
    """Liefert die Zahl der abgeschlossenen Missionen für Folgeziele."""
    return len(_erledigt)


# ---------------------------------------------------------------------------
# 3. MISSIONEN PRÜFEN
# ---------------------------------------------------------------------------
def _wert(kontext, schluessel):
    """Liest einen Fortschrittswert und behandelt fehlende Werte als 0."""
    return max(_zaehler.get(schluessel, 0), kontext.get(schluessel, 0))


def pruefen(kontext):
    """Prüft alle Missionen und gibt nur neue Abschlüsse zurück.

    ``kontext`` ist ein Dictionary aus ``main.py``. Die Funktion bleibt damit
    leicht zu verstehen: Für jede Mission werden die Bedingungen durchlaufen,
    mit ``all`` verbunden und anschließend als erledigt markiert.
    """
    global _zaehler
    kontext = kontext if isinstance(kontext, dict) else {}
    for schluessel, wert in kontext.items():
        try:
            _zaehler[schluessel] = max(_zaehler.get(schluessel, 0), float(wert))
        except (TypeError, ValueError):
            continue
    _zaehler["missionen_erledigt"] = len(_erledigt)

    neue_missionen = []
    # Eine while-Schleife ist hier nicht nötig. Eine einfache for-Schleife ist
    # für den Unterricht gut lesbar und prüft jede Mission genau einmal.
    for mission in MISSIONEN:
        if mission["id"] in _erledigt:
            continue
        bedingungen_erfuellt = all(
            _wert(kontext, schluessel) >= ziel
            for schluessel, ziel in mission["bedingungen"]
        )
        if bedingungen_erfuellt:
            _erledigt.add(mission["id"])
            neue_missionen.append(mission["id"])

    # Die letzte Mission hängt von den gerade eben freigeschalteten Missionen
    # ab. Deshalb wird der aktuelle Zähler nach dem ersten Durchlauf erneut
    # gesetzt; beim nächsten Tick ist sie dann garantiert sichtbar.
    _zaehler["missionen_erledigt"] = len(_erledigt)
    if ("missionsmeister" not in _erledigt and
            len(_erledigt) >= 10):
        _erledigt.add("missionsmeister")
        neue_missionen.append("missionsmeister")
    return neue_missionen


def mission(mission_id):
    """Sucht einen Missionseintrag anhand seiner ID."""
    return next((wert for wert in MISSIONEN if wert["id"] == mission_id), None)


def titel(mission_id):
    """Liefert den sichtbaren Titel einer Mission."""
    wert = mission(mission_id)
    return wert["titel"] if wert else mission_id


def belohnung(mission_id):
    """Liefert eine Kopie der Belohnung, damit das Original unverändert bleibt."""
    wert = mission(mission_id)
    return dict(wert.get("belohnung", {})) if wert else {}


def _fortschritt_einer_bedingung(kontext, bedingung):
    schluessel, ziel = bedingung
    aktuell = _wert(kontext, schluessel)
    if isinstance(aktuell, float) and not aktuell.is_integer():
        return f"{aktuell:.1f}/{ziel}"
    return f"{int(aktuell)}/{ziel}"


def fortschritt_text(mission_id, kontext):
    """Formatiert Fortschritt; mehrere Bedingungen werden mit UND verbunden."""
    wert = mission(mission_id)
    if wert is None:
        return "unbekannt"
    return " + ".join(_fortschritt_einer_bedingung(kontext, bedingung)
                       for bedingung in wert["bedingungen"])


def ist_erledigt(mission_id):
    return mission_id in _erledigt


def zurueck_rect():
    """Position des Zurück-Knopfs für die Maussteuerung."""
    return pygame.Rect(390, 660, 220, 30)


# ---------------------------------------------------------------------------
# 4. MISSIONSMENÜ ZEICHNEN
# ---------------------------------------------------------------------------
def menu_zeichnen(kontext):
    """Zeichnet eine zweispaltige Missionsübersicht."""
    if _fenster is None:
        return

    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((5, 9, 21, 242))
    _fenster.blit(overlay, (0, 0))

    gross = pygame.font.Font(None, 38)
    mittel = pygame.font.Font(None, 23)
    klein = pygame.font.Font(None, 17)
    titel_surface = gross.render("MISSIONSZENTRALE", True, (255, 225, 130))
    _fenster.blit(titel_surface, (500 - titel_surface.get_width() // 2, 15))
    kopf = mittel.render(
        f"{erledigte_anzahl()}/{len(MISSIONEN)} Missionen erledigt",
        True, (190, 225, 255))
    _fenster.blit(kopf, (500 - kopf.get_width() // 2, 50))
    hinweis = klein.render("M öffnet dieses Menü | ESC kehrt zurück", True, (160, 175, 195))
    _fenster.blit(hinweis, (500 - hinweis.get_width() // 2, 70))

    # Fortgeschrittener Kurs: drei Spalten mit je 8 Missionen. So bleibt die
    # wachsende Missionsliste vollstaendig sichtbar.
    for index, wert in enumerate(MISSIONEN):
        spalte = index // 8
        zeile = index % 8
        x = 16 + spalte * 330
        y = 88 + zeile * 70
        geschafft = ist_erledigt(wert["id"])
        hintergrund = (28, 60, 48) if geschafft else (25, 30, 45)
        rahmen = (105, 220, 140) if geschafft else (70, 82, 108)
        pygame.draw.rect(_fenster, hintergrund, (x, y, 306, 60), border_radius=6)
        pygame.draw.rect(_fenster, rahmen, (x, y, 306, 60), width=1, border_radius=6)
        status = "✓" if geschafft else "○"
        farbe = (145, 245, 165) if geschafft else (225, 230, 240)
        zeile1 = f"{status} {wert['titel']}"
        zeile2 = wert["beschreibung"]
        if len(zeile2) > 38:
            zeile2 = zeile2[:35] + "..."
        belohnung_text = ", ".join(f"+{menge} {name}"
                                   for name, menge in wert["belohnung"].items())
        zeile3 = "Belohnung: " + belohnung_text
        _fenster.blit(klein.render(zeile1, True, farbe), (x + 9, y + 5))
        _fenster.blit(klein.render(zeile2, True, (190, 198, 212)), (x + 9, y + 23))
        if geschafft:
            zeile3 = "ERLEDIGT"
        else:
            zeile3 += " | " + fortschritt_text(wert["id"], kontext)
        _fenster.blit(klein.render(zeile3, True,
                                   (125, 205, 225) if not geschafft else (145, 245, 165)),
                      (x + 9, y + 41))

    rect = zurueck_rect()
    pygame.draw.rect(_fenster, (40, 53, 78), rect, border_radius=6)
    pygame.draw.rect(_fenster, (105, 170, 220), rect, width=1, border_radius=6)
    text = mittel.render("Zurück  [ESC]", True, (235, 240, 255))
    _fenster.blit(text, (rect.centerx - text.get_width() // 2,
                         rect.centery - text.get_height() // 2))
