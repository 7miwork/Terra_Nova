"""Mehrere Kolonien auf verschiedenen Planeten (Wunschliste der Schueler).

Architektur-Beweis mit zwei Kolonien (z.B. Mond und Mars):

 * Die AKTIVE Kolonie steckt wie bisher in den globalen Variablen von
   main.py und in den Modulzustaenden (ressourcen, forschung, logistik).
 * Jede Kolonie besitzt eine Kopie davon ("stand") in _kolonien.
 * Wechseln = aktuellen Stand sichern, Zielstand zurueck in die globalen
   Variablen schreiben. Danach laeuft die Wirtschaft der anderen Kolonie
   weiter, als waere nie gewechselt worden.

WICHTIG beim Gruenden: Der Aufrufer sichert ZUERST die alte Kolonie
(kolonien.stand_merken()), baut DANN die frische Welt auf und ruft am
Ende kolonien.gruenden(). Sonst ginge der Zustand der alten Kolonie verloren.

Die Feldliste ist absichtlich explizit: Wer eine neue globale
Kolonie-Variable einfuegt, traegt sie hier ein - sonst ueberlebt der
Koloniewechsel sie nicht.
"""

import copy

import forschung
import logistik
import planeten
import ressourcen

# Alle main.py-Variablen, die EINER Kolonie gehoeren.
KOLONIE_FELDER = (
    "kamera_x", "kamera_y",          # Blickpunkt auf der Karte
    "karten_daten", "sterne_liste",  # eigene Oberflaeche und eigener Sternenhimmel
    "ressourcen_dict", "liste_gebaeude",
    "gebaeude_auswahl", "_auswahl_kategorie", "_auswahl_position",
    "_letztes_gebaeude",
    "tick_zaehler",                  # Wirtschaftsticker der Kolonie
    "_null_nahrung_ticks", "_null_energie_ticks",  # Niederlage-Zaehler
)

# Modulzustaende, die ebenfalls pro Kolonie mitreisen.
KOLONIE_MODULS = (("wirtschaft", ressourcen),
                  ("forschung", forschung),
                  ("logistik", logistik))

_hauptmodul = None      # main.py, nach init per hauptmodul_setzen()
_kolonien = {}          # id -> {"planet": str, "stand": dict oder None}
_aktuell = None         # id der aktiven Kolonie
_zaehler = 0            # erzeugt die IDs kolonie_1, kolonie_2, ...
_karte_breite = 0       # nur zur Plausibilitaetspruefung geladener Stands
_karte_hoehe = 0


def hauptmodul_setzen(modul, karte_breite=0, karte_hoehe=0):
    """Merkt sich main.py als Ziel der globalen Variablen."""
    global _hauptmodul, _karte_breite, _karte_hoehe
    _hauptmodul = modul
    _karte_breite = int(karte_breite)
    _karte_hoehe = int(karte_hoehe)


def zuruecksetzen(startplanet="erde"):
    """Leeres Kolonie-Verzeichnis mit EINER Startkolonie anlegen."""
    global _kolonien, _aktuell, _zaehler
    _zaehler = 1
    _kolonien = {"kolonie_1": {"planet": startplanet, "stand": None}}
    _aktuell = "kolonie_1"
    return _aktuell


def aktuelle_id():
    return _aktuell


def aktueller_planet():
    eintrag = _kolonien.get(_aktuell)
    return eintrag["planet"] if eintrag else None


def alle_ids():
    """Alle Kolonie-IDs, sortiert nach ihrer Nummer."""
    return sorted(_kolonien, key=lambda kid: kid.rsplit("_", 1)[-1])


def anzahl():
    return len(_kolonien)


def position(kolonie_id=None):
    """1-basierte Position der Kolonie in der Reihenfolge."""
    ids = alle_ids()
    ziel = kolonie_id or _aktuell
    return ids.index(ziel) + 1 if ziel in ids else 0


def planet_von(kolonie_id):
    eintrag = _kolonien.get(kolonie_id)
    return eintrag["planet"] if eintrag else None


def ist_besiedelt(planet_id):
    return any(eintrag["planet"] == planet_id for eintrag in _kolonien.values())


def besetzte_planeten():
    return [eintrag["planet"] for eintrag in _kolonien.values()]


def naechster_freier_planet():
    """Naechster spielbarer Planet ohne Kolonie (None = alle voll)."""
    return planeten.naechster_freier_planet(besetzte_planeten())


def aktuelle_beschreibung():
    """Kurzer Text fuer Menues: 'Mond (Kolonie 1 von 2)'."""
    planet_id = aktueller_planet()
    if planet_id is None:
        return "keine Kolonie"
    return f"{planeten.name(planet_id)} (Kolonie {position()} von {anzahl()})"


# ═════════════════════════════════════════════════════════════════════════════
# STAND SICHERN UND ZURUECKLADEN
# ═════════════════════════════════════════════════════════════════════════════

def _stand_auslesen():
    """Kopie aller kolonie-spezifischen Zustände aus main.py und Modulen."""
    if _hauptmodul is None:
        raise RuntimeError("kolonien.hauptmodul_setzen() wurde noch nicht aufgerufen.")
    stand = {}
    for feld in KOLONIE_FELDER:
        stand[feld] = copy.deepcopy(getattr(_hauptmodul, feld))
    for schluessel, modul in KOLONIE_MODULS:
        stand[schluessel] = copy.deepcopy(modul.zustand_exportieren())
    return stand


def _stand_schreiben(stand):
    """Schreibt einen gesicherten Stand in main.py und die Module."""
    if _hauptmodul is None:
        raise RuntimeError("kolonien.hauptmodul_setzen() wurde noch nicht aufgerufen.")
    for feld in KOLONIE_FELDER:
        if feld in stand:
            setattr(_hauptmodul, feld, copy.deepcopy(stand[feld]))
    for schluessel, modul in KOLONIE_MODULS:
        if schluessel in stand and isinstance(stand[schluessel], dict):
            modul.zustand_importieren(stand[schluessel])


def _stand_pruefen(stand):
    """Prüft geladene Daten, bevor sie in die Spielwelt geschrieben werden."""
    if not isinstance(stand, dict):
        return False
    karte = stand.get("karten_daten")
    if not isinstance(karte, list) or not karte:
        return False
    if any(not isinstance(zeile, list) or not zeile for zeile in karte):
        return False
    if _karte_hoehe and len(karte) != _karte_hoehe:
        return False
    if _karte_breite and any(len(zeile) != _karte_breite for zeile in karte):
        return False
    if not isinstance(stand.get("liste_gebaeude"), list):
        return False
    if not isinstance(stand.get("ressourcen_dict"), dict):
        return False
    return True


def stand_merken(kolonie_id=None):
    """Sichert den aktuell laufenden Zustand als Stand dieser Kolonie."""
    ziel = kolonie_id or _aktuell
    if ziel not in _kolonien:
        return False
    _kolonien[ziel]["stand"] = _stand_auslesen()
    return True


def stand_uebernehmen(kolonie_id):
    """Schreibt den gesicherten Stand in main.py und die Module."""
    eintrag = _kolonien.get(kolonie_id)
    if not eintrag or eintrag.get("stand") is None:
        return False
    _stand_schreiben(eintrag["stand"])
    return True


def wechseln(ziel_id):
    """Aktuelle Kolonie sichern, Ziel-Kolonie laden und aktivieren."""
    global _aktuell
    if ziel_id not in _kolonien:
        return False
    if ziel_id == _aktuell:
        return False
    if _aktuell is not None and not stand_merken(_aktuell):
        return False
    if not stand_uebernehmen(ziel_id):
        return False
    _aktuell = ziel_id
    return True


def gruenden(planet_id, stand=None):
    """Neue Kolonie auf einem Planeten anlegen und aktivieren.

    Vor dem Aufruf muss die alte Kolonie per stand_merken() gesichert
    sein und die frische Welt des Zielplaneten in main.py stehen.
    """
    global _aktuell, _zaehler
    if not planeten.ist_spielbar(planet_id):
        return None
    if ist_besiedelt(planet_id):
        return None
    _zaehler += 1
    kolonie_id = f"kolonie_{_zaehler}"
    _kolonien[kolonie_id] = {"planet": planet_id, "stand": stand}
    _aktuell = kolonie_id
    return kolonie_id


# ═════════════════════════════════════════════════════════════════════════════
# SPEICHERSTAND (SPIELSTAND VERSION 2)
# ═════════════════════════════════════════════════════════════════════════════

def zustand_fuer_spielstand():
    """JSON-faehiges Abbild aller Kolonien fuer spielstand.speichern().

    Die AKTIVE Kolonie steckt wie bisher in den flachen Feldern des
    Spielstands - ihr Stand steht deshalb nicht noch einmal hier drin.
    """
    liste = {}
    for kolonie_id, eintrag in _kolonien.items():
        if kolonie_id == _aktuell:
            continue
        liste[kolonie_id] = {"planet": eintrag["planet"],
                             "stand": eintrag["stand"]}
    return {"zaehler": _zaehler,
            "aktuell": _aktuell,
            "planeten": {kolonie_id: eintrag["planet"]
                         for kolonie_id, eintrag in _kolonien.items()},
            "liste": liste}


def zustand_uebernehmen(daten):
    """Kolonie-Liste aus einem Spielstand uebernehmen (Version 2).

    Der Stand der aktiven Kolonie fehlt hier absichtlich - er steckt in
    den flachen Feldern, die main.py vorher schon geladen hat.
    """
    global _kolonien, _aktuell, _zaehler
    daten = daten if isinstance(daten, dict) else {}
    planeten_map = daten.get("planeten")
    if not isinstance(planeten_map, dict) or not planeten_map:
        # Alter Spielstand (Version 1) oder Fremddaten: eine Kolonie.
        planeten_map = {"kolonie_1": "erde"}
    liste = daten.get("liste")
    liste = liste if isinstance(liste, dict) else {}

    neu = {}
    for kolonie_id, planet_id in planeten_map.items():
        if not isinstance(kolonie_id, str) or not isinstance(planet_id, str):
            continue
        eintrag = liste.get(kolonie_id)
        eintrag = eintrag if isinstance(eintrag, dict) else {}
        stand = eintrag.get("stand")
        # None ist erlaubt = die aktive Kolonie (steckt in den Feldern).
        if stand is not None and not _stand_pruefen(stand):
            continue  # defekter Stand: diese Kolonie wird nicht geladen
        planet = eintrag.get("planet") or planet_id
        neu[kolonie_id] = {"planet": planet, "stand": stand}
    if not neu:
        return False

    _kolonien = neu
    aktuell = daten.get("aktuell")
    _aktuell = aktuell if aktuell in _kolonien else alle_ids()[0]
    nummern = [int(kid.rsplit("_", 1)[-1]) for kid in _kolonien
               if kid.rsplit("_", 1)[-1].isdigit()]
    hoechste_nr = max(nummern) if nummern else 0
    try:
        _zaehler = max(int(daten.get("zaehler", 0)), hoechste_nr)
    except (TypeError, ValueError):
        _zaehler = hoechste_nr
    return True


