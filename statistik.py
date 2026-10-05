"""Dauerhafte Spielstatistik für Terra_Nova.

Die Statistik steht in einer eigenen Datei (statistik.json) und überlebt
Spielstände, Neustarts und neue Partien — anders als der Spielstand zählt
sie über alle Partien hinweg. Angezeigt wird sie im Hauptmenü.

Wichtig: Diese Datei wird wie ein Spielstand behandelt und steht deshalb
nicht im Git-Repository (siehe .gitignore).
"""

import json
import os

import pygame

import achievements

DATEI = os.path.join(os.path.dirname(__file__), "statistik.json")

# Diese Felder gibt es im Profil und in der laufenden Partie.
FELDER = ("spiele", "siege", "niederlagen", "zeit", "gebaeude", "forschung",
          "handelsaktionen", "technologien", "ereignisse",
          "max_bevoelkerung", "achievements")

# Anzeigetext und Einheit je Feld.
BESCHRIEBUNG = {
    "spiele": "Gespielte Partien",
    "siege": "Gewonnene Partien",
    "niederlagen": "Verlorene Partien",
    "zeit": "Spielzeit",
    "gebaeude": "Gebaute Gebäude",
    "forschung": "Forschungspunkte",
    "handelsaktionen": "Handelsaktionen",
    "technologien": "Technologien",
    "ereignisse": "Erlebte Ereignisse",
    "max_bevoelkerung": "Größte Kolonie",
    "achievements": "Achievements",
}

_fenster = None
_profil = {name: 0 for name in FELDER}
_ereignisse_art = {}
_partie = {name: 0 for name in FELDER}
_ereignisse_partie = {}


def initialisieren(fenster_obj):
    global _fenster
    _fenster = fenster_obj


def _zahl(name):
    """Liest ein Profilfeld als Zahl und verträgt kaputte Dateien."""
    try:
        return max(0.0, float(_profil.get(name, 0)))
    except (TypeError, ValueError):
        return 0.0


def _erhoehen(name, wert=1):
    """Erhöht ein Feld im Profil und in der laufenden Partie."""
    if name not in _profil:
        return
    _profil[name] = _zahl(name) + wert
    _partie[name] = _partie.get(name, 0) + wert


def laden():
    """Liest die Statistikdatei. Fehler oder fehlende Datei bedeuten: leer."""
    global _profil, _ereignisse_art
    _profil = {name: 0 for name in FELDER}
    _ereignisse_art = {}
    try:
        with open(DATEI, "r", encoding="utf-8") as datei:
            daten = json.load(datei)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return False
    if not isinstance(daten, dict):
        return False
    # Wichtig: Die Werte kommen aus den geladenen Daten, nicht aus _profil -
    # _profil wurde oben bewusst schon auf Null gesetzt.
    for name in FELDER:
        try:
            _profil[name] = max(0.0, float(daten.get(name, 0) or 0))
        except (TypeError, ValueError):
            _profil[name] = 0.0
    art = daten.get("ereignisse_art")
    if isinstance(art, dict):
        _ereignisse_art = {}
        for schluessel, wert in art.items():
            try:
                _ereignisse_art[str(schluessel)] = max(0, int(wert))
            except (TypeError, ValueError):
                continue
    return True


def speichern():
    """Schreibt das Profil als JSON. Fehler sind nicht fatal."""
    daten = dict(_profil)
    daten["ereignisse_art"] = dict(_ereignisse_art)
    try:
        temporaer = DATEI + ".tmp"
        with open(temporaer, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, ensure_ascii=False, indent=2)
        os.replace(temporaer, DATEI)
    except (OSError, TypeError, ValueError):
        try:
            if os.path.exists(DATEI + ".tmp"):
                os.remove(DATEI + ".tmp")
        except OSError:
            pass
        return False
    return True


def zustand_zuruecksetzen():
    """Loescht das komplette Profil (Tests, neues Profil, Profil zuruecksetzen).

    Anders als `neue_partie()` werden auch die Werte aller Partien geloescht.
    """
    global _profil, _partie, _ereignisse_art, _ereignisse_partie
    _profil = {name: 0 for name in FELDER}
    _partie = {name: 0 for name in FELDER}
    _ereignisse_art = {}
    _ereignisse_partie = {}


def neue_partie():
    """Beginnt eine neue Partie; alte Werte stehen weiter im Profil."""
    global _partie, _ereignisse_partie
    _partie = {name: 0 for name in FELDER}
    _ereignisse_partie = {}
    _erhoehen("spiele")


def tick(ressourcen_dict, liste_gebaeude):
    """Wird pro Wirtschaftstick aufgerufen: Spielzeit und Bestwerte."""
    _erhoehen("zeit")
    try:
        bevoelkerung = float(ressourcen_dict.get("bevoelkerung", 0))
    except (TypeError, ValueError):
        bevoelkerung = 0.0
    if bevoelkerung > _profil.get("max_bevoelkerung", 0):
        _erhoehen("max_bevoelkerung", bevoelkerung - _profil["max_bevoelkerung"])
    erreicht = achievements.anzahl_erreicht()
    if erreicht > _profil.get("achievements", 0):
        _erhoehen("achievements", erreicht - _profil["achievements"])


def gebaeude_gebaut(anzahl=1):
    _erhoehen("gebaeude", anzahl)


def forschung_erzeugt(menge):
    """Zählt erzeugte Forschungspunkte (nicht den Lagerbestand)."""
    if menge > 0:
        _erhoehen("forschung", menge)


def handelsaktion():
    _erhoehen("handelsaktionen")


def technologie_erforscht():
    _erhoehen("technologien")


def ereignis(ereignis_id):
    """Ein Zufallsereignis ist aufgetreten (für Statistik und Profil)."""
    _erhoehen("ereignisse")
    _ereignisse_art[ereignis_id] = _ereignisse_art.get(ereignis_id, 0) + 1
    _ereignisse_partie[ereignis_id] = _ereignisse_partie.get(ereignis_id, 0) + 1


def partie_beendet(status):
    """Zählt Sieg oder Niederlage und speichert das Profil sofort."""
    if status == "sieg":
        _erhoehen("siege")
    elif status == "niederlage":
        _erhoehen("niederlagen")
    return speichern()


def profil():
    """Die Werte, die achievements.pruefen() für Langzeitziele braucht."""
    return {"gebaeude": _zahl("gebaeude"), "forschung": _zahl("forschung"),
            "zeit": _zahl("zeit"), "siege": _zahl("siege")}


def profil_werte():
    """Alle Profilwerte (für Anzeige und Tests)."""
    return dict(_profil)


def partei_werte():
    """Alle Werte der laufenden Partie (für Anzeige und Tests)."""
    return dict(_partie)


def ereignisse_uebersicht():
    """Wie oft wurde jedes Ereignis bisher gesehen?"""
    return dict(_ereignisse_art)


def zeit_text(ticks):
    """Formatiert eine Tickzahl als „2 Std 15 Min 30 Sek“."""
    try:
        sekunden = int(max(0, ticks))
    except (TypeError, ValueError):
        sekunden = 0
    stunden, rest = divmod(sekunden, 3600)
    minuten, sek = divmod(rest, 60)
    if stunden:
        return f"{stunden} Std {minuten} Min {sek} Sek"
    if minuten:
        return f"{minuten} Min {sek} Sek"
    return f"{sek} Sek"


def _anzeige_wert(name, wert):
    if name == "zeit":
        return zeit_text(wert)
    if name == "max_bevoelkerung":
        return f"{int(wert)} Bewohner"
    return f"{int(wert)}"


def uebersicht_zeilen():
    """Die Zeilen für die Anzeige: (Beschreibung, Profilwert, Partiewert)."""
    return [(BESCHRIEBUNG[name], _anzeige_wert(name, _profil.get(name, 0)),
             _anzeige_wert(name, _partie.get(name, 0))) for name in FELDER]


EREIGNIS_NAMEN = {
    "systemausfall": "Systemausfall",
    "raumschiff": "Unbekanntes Raumschiff",
    "meteoritenschauer": "Meteoritenschauer",
}


def zurueck_rect():
    return pygame.Rect(390, 648, 220, 30)


def menu_zeichnen():
    """Zeichnet die Statistik als Vollbild-Overlay (Aufruf aus main.py)."""
    if _fenster is None:
        return
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((4, 8, 20, 242))
    _fenster.blit(overlay, (0, 0))
    gross = pygame.font.Font(None, 38)
    mittel = pygame.font.Font(None, 22)
    klein = pygame.font.Font(None, 17)

    titel = gross.render("STATISTIK", True, (255, 240, 145))
    _fenster.blit(titel, (500 - titel.get_width() // 2, 18))
    kopf = klein.render("Insgesamt über alle Partien", True, (190, 225, 255))
    _fenster.blit(kopf, (400 - kopf.get_width() // 2, 58))
    kopf2 = klein.render("Diese Partie", True, (255, 200, 140))
    _fenster.blit(kopf2, (720 - kopf2.get_width() // 2, 58))

    y = 80
    for beschreibung, wert, partei_wert in uebersicht_zeilen():
        _fenster.blit(klein.render(beschreibung, True, (200, 210, 225)), (150, y))
        text = mittel.render(wert, True, (240, 245, 255))
        _fenster.blit(text, (560 - text.get_width(), y - 3))
        text2 = mittel.render(partei_wert, True, (255, 205, 150))
        _fenster.blit(text2, (860 - text2.get_width(), y - 3))
        y += 30

    y += 8
    _fenster.blit(klein.render("Erlebte Ereignisse:", True, (150, 200, 240)), (150, y))
    y += 24
    if not _ereignisse_art:
        _fenster.blit(klein.render("Noch keine Zufallsereignisse.",
                                   True, (150, 158, 175)), (170, y))
    else:
        for ereignis_id, anzahl in sorted(_ereignisse_art.items()):
            text = f"{EREIGNIS_NAMEN.get(ereignis_id, ereignis_id)}: {anzahl}x"
            _fenster.blit(klein.render(text, True, (185, 200, 220)), (170, y))
            y += 22

    rect = zurueck_rect()
    pygame.draw.rect(_fenster, (39, 52, 76), rect, border_radius=6)
    pygame.draw.rect(_fenster, (105, 170, 220), rect, width=1, border_radius=6)
    text = mittel.render("Zurück  [ESC / T]", True, (235, 240, 255))
    _fenster.blit(text, (rect.centerx - text.get_width() // 2,
                         rect.centery - text.get_height() // 2))
