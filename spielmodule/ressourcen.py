"""Wirtschaft, Personal, Speicher und Produktionsboni für Stunde 11."""

import math
import random
import forschung

_wirtschafts_tick = 0
_lager_bonus_aktiv = False
_prestige_bonus_aktiv = False
# Zufallsereignisse (ereignisse.py) koennen die Produktion stoeren. Die
# Stoerung ist ein reiner Zahlenwert in Ticks, damit Speichern/Laden und
# Tests ohne pygame funktionieren.
SYSTEMAUSFALL_FAKTOR = 0.70    # Systemausfall: 30 Prozent weniger Energie
BESCHAEDIGT_FAKTOR = 0.20      # Meteoritenschauer: 80 Prozent weniger Produktion
_energie_stoerung = 0
# Fortgeschrittener Kurs (Planeten): Produktionsfaktoren des Planeten,
# auf dem die AKTIVE Kolonie steht. {"eisen": 2.5} auf dem Mars z.B.
# Wird pro Kolonie mitgespeichert (zustand_exportieren).
_planeten_faktoren = {}


def planeten_faktoren_setzen(faktoren):
    """Produktionsfaktoren des aktuellen Planeten setzen.

    Nur Zahlen groesser 0 werden uebernommen, alles andere stammt aus
    einem kaputten Spielstand und wird ignoriert.
    """
    global _planeten_faktoren
    neue = {}
    if isinstance(faktoren, dict):
        for rohstoff, wert in faktoren.items():
            try:
                wert = float(wert)
            except (TypeError, ValueError):
                continue
            if wert > 0:
                neue[str(rohstoff)] = wert
    _planeten_faktoren = neue


def planeten_faktor(rohstoff):
    """Faktor fuer eine Ressource auf dem aktuellen Planeten (1.0 = normal)."""
    return _planeten_faktoren.get(rohstoff, 1.0)


def zustand_exportieren():
    """Gibt interne Wirtschaftswerte für einen Spielstand zurück."""
    return {
        "wirtschafts_tick": _wirtschafts_tick,
        "lager_bonus_aktiv": _lager_bonus_aktiv,
        "prestige_bonus_aktiv": _prestige_bonus_aktiv,
        "energie_stoerung": _energie_stoerung,
        "planeten": dict(_planeten_faktoren),
    }


def zustand_importieren(daten):
    """Stellt interne Wirtschaftswerte aus einem JSON-Dictionary wieder her."""
    global _wirtschafts_tick, _lager_bonus_aktiv, _prestige_bonus_aktiv
    global _energie_stoerung
    daten = daten if isinstance(daten, dict) else {}
    try:
        _wirtschafts_tick = max(0, int(daten.get("wirtschafts_tick", 0)))
    except (TypeError, ValueError):
        _wirtschafts_tick = 0
    _lager_bonus_aktiv = bool(daten.get("lager_bonus_aktiv", False))
    _prestige_bonus_aktiv = bool(daten.get("prestige_bonus_aktiv", False))
    energie_stoerung_setzen(daten.get("energie_stoerung", 0))
    # Alter Spielstand ohne Planeten: Faktor 1.0 auf alles.
    planeten_faktoren_setzen(daten.get("planeten", {}))


def energie_stoerung_setzen(ticks):
    """Setzt die Energiestoerung in Ticks (0 hebt sie auf).

    Wird vom Ereignismodul benutzt: Systemausfall = viele Ticks, Reparatur = 0.
    """
    global _energie_stoerung
    try:
        _energie_stoerung = max(0, int(ticks))
    except (TypeError, ValueError):
        _energie_stoerung = 0


def energie_stoerung_rest():
    """Wie viele Ticks die Energiestoerung noch laeuft (0 = keine)."""
    return _energie_stoerung


def energie_stoerung_aktiv():
    return _energie_stoerung > 0


def gebaeude_beschaedigen(gebaeude, ticks):
    """Markiert ein Gebaeude als beschaedigt (Meteoritenschauer)."""
    try:
        gebaeude["beschaedigt_rest"] = max(0, int(ticks))
    except (TypeError, ValueError):
        gebaeude["beschaedigt_rest"] = 0


def gebaeude_beschaedigt(gebaeude):
    return gebaeude.get("beschaedigt_rest", 0) > 0


def _schaden_ticken(liste_gebaeude):
    """Zaehlt die Beschaedigung aller Gebaeude um einen Tick herunter."""
    for gebaeude in liste_gebaeude:
        rest = gebaeude.get("beschaedigt_rest", 0)
        if isinstance(rest, (int, float)) and rest > 0:
            rest = rest - 1
            if rest <= 0:
                gebaeude.pop("beschaedigt_rest", None)
            else:
                gebaeude["beschaedigt_rest"] = rest


RESSOURCEN_NAMEN = {
    "gold": "Gold", "energie": "Energie", "holz": "Holz", "stein": "Stein",
    "bevoelkerung": "Bevoelkerung", "nahrung": "Nahrung", "forschung": "Forschung",
    "kohle": "Kohle", "eisen": "Eisen", "roboter": "Roboter", "stahl": "Stahl",
    "verteidiger": "Verteidiger", "raumschiffe": "Raumschiffe",
    "zufriedenheit": "Zufriedenheit",
}

# Fortgeschrittener Kurs (Gegner): Buerger duerfen zu Verteidigern werden,
# aber hoechstens dieser Anteil der Bevoelkerung darf gleichzeitig
# Verteidiger sein. Sonst bleibt niemand uebrig, der wirklich arbeitet.
MAX_VERTEIDIGER_ANTEIL = 0.30

ZUFRIEDENHEIT_MIN = -50.0
ZUFRIEDENHEIT_MAX = 50.0

# Positiver Wert = Gebäude verbessert die Stimmung, negativer Wert = Belastung.
# Der Wert ist ein Grundbeitrag pro Wirtschaftstick; in der Funktion weiter
# unten wird er mit 0.25 abgeschwächt, damit Zufriedenheit nicht zu schnell
# von -50 auf +50 springt.
GEBAEUDE_ZUFRIEDENHEIT = {
    0: 0,    # Basis
    1: -3,   # Reaktor: Lärm und Kohleverbrauch
    2: 2,    # Farm: Nahrung und Versorgung
    3: -1,   # Holzfäller: Eingriff in die Umwelt
    4: -1,   # Steinmetz: Lärm
    5: 1,    # Marktplatz: Handel und Begegnung
    6: 3,    # Wohnhaus
    7: 2,    # Universität
    8: -2,   # Mine
    9: 1,    # Straße
    10: -4,  # Fusionsreaktor: sehr leistungsstark, aber belastend
    11: -1,  # Roboterfabrik
    12: -2,  # Stahlwerk
    13: 2,   # Gewächshaus
    14: 1,   # Lagerhaus
    15: 4,   # Wohnblock
    16: 1,   # Handelsposten
    17: 5,   # Koloniezentrum
    18: -2,  # Eisenmine
    19: 6,   # Park: Erholung und Natur
    20: 4,   # Solarreaktor: saubere Energie
    21: -2,  # Kaserne: Militaer wirkt bedrohlich
    22: -1,  # Raumschiffwerft: lauter Fabrikbetrieb
    23: 1,   # Laserturm: Sicherheit und Vertrauen
}

SPEICHER_BASIS = {
    "gold": 500.0, "energie": 100.0, "holz": 250.0, "stein": 250.0,
    "bevoelkerung": 100.0, "nahrung": 250.0, "forschung": 500.0,
    "kohle": 200.0, "eisen": 200.0, "roboter": 100.0, "stahl": 150.0,
    "verteidiger": 100.0, "raumschiffe": 50.0,
}

# Die Liste bleibt parallel zu GEBAEUDE_TYPEN. Die ersten zwölf Einträge
# behalten ihre alten Indizes, damit bestehende Tests und Spielstände lesbar bleiben.
GEBAEUDE_WIRTSCHAFT = [
    # 0 Basis: kleine Startproduktion ohne Personal und Verbrauch.
    {"baukosten": {}, "produktion": {"gold": 1, "energie": 1, "holz": 1, "stein": 1},
     "verbrauch": {}, "personalbedarf": 0, "max_anzahl": 1, "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 20}, "produktion": {"energie": 5}, "verbrauch": {"holz": 2},
     "personalbedarf": 1, "max_anzahl": None, "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 15, "energie": 10}, "produktion": {"nahrung": 5},
     "verbrauch": {"energie": 2}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 10, "energie": 5}, "produktion": {"holz": 6},
     "verbrauch": {"energie": 2}, "personalbedarf": 1, "max_anzahl": None,
     "freischaltung": None, "grosse_anlage": False},
    {"baukosten": {"gold": 15, "energie": 10}, "produktion": {"stein": 5},
     "verbrauch": {"energie": 3}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": None, "grosse_anlage": False},
    # Balancing: Marktplatz 12 -> 10 Gold (Gold war sehr stark).
    {"baukosten": {"gold": 30, "energie": 15}, "produktion": {"gold": 10},
     "verbrauch": {"stein": 5}, "personalbedarf": 1, "max_anzahl": None,
     "freischaltung": {"typ": "ressource", "ressource": "bevoelkerung", "menge": 5}, "grosse_anlage": False},
    {"baukosten": {"gold": 20, "holz": 15, "stein": 10}, "produktion": {"bevoelkerung": 1},
     "verbrauch": {"energie": 3}, "personalbedarf": 0, "max_anzahl": 10,
     "freischaltung": {"typ": "ressource", "ressource": "bevoelkerung", "menge": 5}, "grosse_anlage": True},
    {"baukosten": {"gold": 40, "energie": 20}, "produktion": {"forschung": 5},
     "verbrauch": {"gold": 2, "energie": 3}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": [{"typ": "ressource", "ressource": "bevoelkerung", "menge": 5},
                        {"typ": "ressource", "ressource": "gold", "menge": 40}], "grosse_anlage": True},
    {"baukosten": {"gold": 35, "energie": 10, "stein": 15}, "produktion": {"kohle": 2},
     "verbrauch": {"energie": 2}, "personalbedarf": 3, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "minenbau"}, "grosse_anlage": True},
    {"baukosten": {"stein": 2}, "produktion": {}, "verbrauch": {}, "personalbedarf": 0,
     "max_anzahl": None, "freischaltung": None, "grosse_anlage": False},
    # Balancing: Der Fusionsreaktor war sehr stark (+25 Energie). 20 Energie
    # bleiben stark, kosten aber spuerbar Kohle und Personal.
    {"baukosten": {"gold": 100, "energie": 20, "stein": 40, "eisen": 20},
     "produktion": {"energie": 20}, "verbrauch": {"kohle": 5}, "personalbedarf": 4,
     "max_anzahl": None, "freischaltung": {"typ": "forschung", "technologie": "fusionsreaktor"}, "grosse_anlage": True},
    {"baukosten": {"gold": 60, "energie": 20, "eisen": 10}, "produktion": {"roboter": 1},
     "verbrauch": {"energie": 2, "kohle": 1}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "einfache_robotik"}, "grosse_anlage": True},
    # 12 Stahlwerk / Eisenschmelze
    {"baukosten": {"gold": 70, "energie": 20, "eisen": 8, "kohle": 6}, "produktion": {"stahl": 2},
     "verbrauch": {"energie": 3, "eisen": 2, "kohle": 2}, "personalbedarf": 3, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "stahlverarbeitung"}, "grosse_anlage": True},
    # 13 Gewächshaus als zweite Nahrungsquelle
    # Balancing: Gewaechshaus 8 -> 6 Nahrung, weil Nahrung im spaeten
    # Spielverlauf ohnehin im Ueberfluss vorhanden ist.
    {"baukosten": {"gold": 45, "energie": 20, "eisen": 5}, "produktion": {"nahrung": 6},
     "verbrauch": {"energie": 3}, "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "gewaechshausbau"}, "grosse_anlage": False},
    # 14 Lagerhaus erhöht mit der Forschung die Speichergrenzen.
    {"baukosten": {"gold": 60, "holz": 20, "stein": 20}, "produktion": {}, "verbrauch": {},
     "personalbedarf": 0, "max_anzahl": 4,
     "freischaltung": {"typ": "forschung", "technologie": "logistik_lager"}, "grosse_anlage": False},
    # 15 Wohnblock bietet eine höhere Bevölkerungskapazität als ein Wohnhaus.
    {"baukosten": {"gold": 80, "holz": 30, "stein": 30}, "produktion": {"bevoelkerung": 3},
     "verbrauch": {"energie": 5, "nahrung": 1}, "personalbedarf": 0, "max_anzahl": 6,
     "freischaltung": {"typ": "forschung", "technologie": "wohnblockbau"}, "grosse_anlage": True},
    # 16 Handelsposten ergänzt den Marktplatz um interkolonialen Handel.
    {"baukosten": {"gold": 100, "energie": 25, "eisen": 15}, "produktion": {"gold": 4},
     "verbrauch": {"energie": 2}, "personalbedarf": 2, "max_anzahl": 3,
     "freischaltung": {"typ": "forschung", "technologie": "interkolonialhandel"}, "grosse_anlage": False},
        # 17 Koloniezentrum ist ein Prestigegebäude mit kleinem globalem Produktionsbonus.
    {"baukosten": {"gold": 200, "stein": 50, "stahl": 10},
     "produktion": {},
     "verbrauch": {"energie": 2},
     "personalbedarf": 0, "max_anzahl": 1,
     "freischaltung": {"typ": "forschung", "technologie": "koloniezentrum"}, "grosse_anlage": True},
    # 18 Eisenmine: teures Spezialgebäude aus der späten Metallurgie.
    # Sie liefert planbar Eisen; die normale Mine bleibt als frühe, zufällige
    # Möglichkeit erhalten.
    {"baukosten": {"gold": 160, "energie": 40, "stein": 60},
     "produktion": {"eisen": 3}, "verbrauch": {"energie": 4},
     "personalbedarf": 3, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "eisenminenbau"}, "grosse_anlage": True},
    # 19 Park: Ein Park verbessert das Wohlbefinden. In dieser Spielversion
    # wird das einfach und sichtbar als geringerer Nahrungsverbrauch umgesetzt.
    {"baukosten": {"gold": 35, "holz": 20, "stein": 15},
     "produktion": {}, "verbrauch": {}, "personalbedarf": 0, "max_anzahl": 8,
     "freischaltung": None, "grosse_anlage": False},
    # 20 Solarreaktor: erneuerbare Energiequelle ohne Kohleverbrauch.
    {"baukosten": {"gold": 90, "energie": 10, "stein": 25},
     "produktion": {"energie": 10}, "verbrauch": {}, "personalbedarf": 1, "max_anzahl": 6,
     "freischaltung": None, "grosse_anlage": True},
    # ── Fortgeschrittener Kurs (Gegner): Verteidigung — Indizes 21 bis 23 ────
    # Diese drei Typen MUESSEN hinten angehaengt bleiben: Spielstaende
    # speichern den Typ-Index, kein Umsortieren erlaubt!
    # 21 Kaserne: bildet Buerger zu Verteidigern aus (Deckel siehe oben).
    {"baukosten": {"gold": 80, "holz": 30, "stein": 30},
     "produktion": {"verteidiger": 0.5}, "verbrauch": {"nahrung": 1, "energie": 2},
     "personalbedarf": 2, "max_anzahl": None,
     "freischaltung": {"typ": "forschung", "technologie": "militaertraining"},
     "grosse_anlage": False},
    # 22 Raumschiffwerft: baut kampfbereite Raumschiffe (je 6 Staerke).
    {"baukosten": {"gold": 250, "stahl": 30, "energie": 40, "stein": 40},
     "produktion": {"raumschiffe": 0.2}, "verbrauch": {"energie": 5, "stahl": 1},
     "personalbedarf": 3, "max_anzahl": 3,
     "freischaltung": {"typ": "forschung", "technologie": "raumschiffbau"},
     "grosse_anlage": False},
    # 23 Laserturm: feste Verteidigung, solange er arbeitet.
    {"baukosten": {"gold": 120, "stahl": 15, "energie": 20},
     "produktion": {}, "verbrauch": {"energie": 3},
     "personalbedarf": 1, "max_anzahl": 10,
     "freischaltung": {"typ": "forschung", "technologie": "laserverteidigung"},
     "grosse_anlage": False},
]


_GEBAEUDE_NAMEN = [
    "Basis", "Reaktor", "Farm", "Holzfaeller", "Steinmetz", "Marktplatz", "Wohnhaus",
    "Universitaet", "Mine", "Strasse", "Fusionsreaktor", "Roboterfabrik", "Stahlwerk",
    "Gewaechshaus", "Lagerhaus", "Wohnblock", "Handelsposten", "Koloniezentrum", "Eisenmine",
    "Park", "Solarreaktor", "Kaserne", "Raumschiffwerft", "Laserturm",
]


def _hat_genug(ressourcen_dict, ressourcen_name, benoetigte_menge):
    return ressourcen_dict.get(ressourcen_name, 0) >= benoetigte_menge


def _gebaeude_name_fuer_index(typ_index):
    return _GEBAEUDE_NAMEN[typ_index] if 0 <= typ_index < len(_GEBAEUDE_NAMEN) else "Unbekannt"


def _ressourcen_name(ress_name):
    return RESSOURCEN_NAMEN.get(ress_name, ress_name)


def maximaler_speicher(ressourcen_name):
    limit = SPEICHER_BASIS.get(ressourcen_name, 9999.0)
    if ressourcen_name == "energie" and forschung.ist_technologie_erforscht("energiespeicher"):
        limit *= 1.25
    if _lager_bonus_aktiv and forschung.ist_technologie_erforscht("lagerhaus_ausbau"):
        limit *= 1.50
    return limit


def zufriedenheit_begrenzen(ressourcen_dict):
    """Hält Zufriedenheit sicher im Bereich -50 bis +50."""
    wert = float(ressourcen_dict.get("zufriedenheit", 0.0))
    ressourcen_dict["zufriedenheit"] = round(
        max(ZUFRIEDENHEIT_MIN, min(ZUFRIEDENHEIT_MAX, wert)), 2)


def ressourcen_begrenzen(ressourcen_dict):
    for name in SPEICHER_BASIS:
        wert = ressourcen_dict.get(name, 0)
        ressourcen_dict[name] = max(0.0, min(float(wert), maximaler_speicher(name)))
    zufriedenheit_begrenzen(ressourcen_dict)


def zufriedenheit_aktualisieren(ressourcen_dict, liste_gebaeude):
    """Aktualisiert Zufriedenheit anhand der gebauten Gebäude.

    Gebäude geben nicht sofort den gesamten Grundbeitrag, sondern ein Viertel
    davon pro Wirtschaftstick. Dadurch entsteht ein langsam veränderlicher,
    gut beobachtbarer Wert. Ohne Gebäude nähert sich Zufriedenheit wieder 0.
    """
    zufriedenheit_begrenzen(ressourcen_dict)
    grundbeitrag = sum(
        GEBAEUDE_ZUFRIEDENHEIT.get(gebaeude.get("typ"), 0)
        for gebaeude in liste_gebaeude
    )
    if grundbeitrag:
        veraenderung = grundbeitrag * 0.25
    else:
        # Ein neutraler Grundzustand verhindert, dass eine verlassene Kolonie
        # für immer bei einem alten Extremwert stehen bleibt.
        veraenderung = -ressourcen_dict["zufriedenheit"] * 0.10
    ressourcen_dict["zufriedenheit"] += veraenderung
    zufriedenheit_begrenzen(ressourcen_dict)


def baukosten_berechnen(typ_index):
    rohkosten = GEBAEUDE_WIRTSCHAFT[typ_index].get("baukosten", {})
    kosten = dict(rohkosten)
    for ress_name, wert in list(kosten.items()):
        faktor = 1.0
        if forschung.ist_technologie_erforscht("effiziente_bautechnik"):
            faktor *= 0.95
        if ress_name == "holz" and forschung.ist_technologie_erforscht("effizientere_holzverwendung"):
            faktor *= 0.95
        kosten[ress_name] = max(1, int(math.ceil(wert * faktor)))
    return kosten


def ist_freigeschaltet(ressourcen_dict, typ_index):
    freischaltung = GEBAEUDE_WIRTSCHAFT[typ_index].get("freischaltung")
    if freischaltung is None:
        return True
    def pruefen(bedingung):
        if bedingung.get("typ", "ressource") == "forschung":
            return forschung.ist_technologie_erforscht(bedingung["technologie"])
        return _hat_genug(ressourcen_dict, bedingung["ressource"], bedingung["menge"])
    if isinstance(freischaltung, list):
        return all(pruefen(bedingung) for bedingung in freischaltung)
    return pruefen(freischaltung)


def freischaltung_hinweis(ressourcen_dict, typ_index):
    freischaltung = GEBAEUDE_WIRTSCHAFT[typ_index].get("freischaltung")
    if freischaltung is None or ist_freigeschaltet(ressourcen_dict, typ_index):
        return ""
    bedingungen = freischaltung if isinstance(freischaltung, list) else [freischaltung]
    texte = []
    for bedingung in bedingungen:
        if bedingung.get("typ", "ressource") == "forschung":
            texte.append("Forschung fehlt: " + forschung.technologie_name(bedingung["technologie"]))
        else:
            texte.append(f"{bedingung['menge']} {_ressourcen_name(bedingung['ressource'])}")
    if any(bedingung.get("typ", "ressource") == "forschung"
           for bedingung in bedingungen):
        return " und ".join(texte)
    return "Benötigt " + " und ".join(texte)


def fehlende_baukosten(ressourcen_dict, typ_index):
    """Gibt die tatsächlich fehlenden Rohstoffe für ein Gebäude zurück.

    Die Rückgabe ist ein lesbarer Text, damit main.py nicht nur pauschal
    „fehlende Rohstoffe“ melden muss. So sehen Spielerinnen und Spieler zum
    Beispiel: „Energie: 10 (benötigt 20)“.
    """
    fehlend = []
    for name, benoetigt in baukosten_berechnen(typ_index).items():
        vorhanden = ressourcen_dict.get(name, 0)
        if vorhanden < benoetigt:
            fehlend.append(
                f"{_ressourcen_name(name)}: {benoetigt - vorhanden:.0f} fehlen")
    return ", ".join(fehlend)


def kann_bauen(ressourcen_dict, liste_gebaeude, typ_index, boden_typ=None):
    if typ_index < 0 or typ_index >= len(GEBAEUDE_WIRTSCHAFT) or not ist_freigeschaltet(ressourcen_dict, typ_index):
        return False
    wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
    max_anzahl = wirtschaft.get("max_anzahl")
    if max_anzahl is not None and sum(g["typ"] == typ_index for g in liste_gebaeude) >= max_anzahl:
        return False
    if boden_typ is not None:
        boden_anforderung = {2: 1, 3: 1, 4: 2, 13: 1}
        if typ_index in boden_anforderung and boden_typ != boden_anforderung[typ_index]:
            return False
    return all(_hat_genug(ressourcen_dict, name, menge)
               for name, menge in baukosten_berechnen(typ_index).items())


def baukosten_abziehen(ressourcen_dict, typ_index):
    for ress_name, kosten in baukosten_berechnen(typ_index).items():
        ressourcen_dict[ress_name] = max(0.0, ressourcen_dict.get(ress_name, 0) - kosten)


def ressourcen_zurueckerstatten(ressourcen_dict, typ_index):
    rueckerstattung = {}
    for ress_name, kosten in baukosten_berechnen(typ_index).items():
        betrag = kosten // 2
        if betrag:
            ressourcen_dict[ress_name] = ressourcen_dict.get(ress_name, 0) + betrag
            rueckerstattung[ress_name] = betrag
    ressourcen_begrenzen(ressourcen_dict)
    return rueckerstattung


def personalbedarf(typ_index):
    bedarf = GEBAEUDE_WIRTSCHAFT[typ_index].get("personalbedarf", 0)
    if forschung.ist_technologie_erforscht("autonome_fabriken") and bedarf:
        return max(1, int(round(bedarf * 0.70)))
    return bedarf


def verteidiger_kontingent(ressourcen_dict):
    """Höchste erlaubte Anzahl Verteidiger (MAX_VERTEIDIGER_ANTEIL × Bevölkerung).

    Verteidiger bleiben Bewohner — aber nur ein Teil der Kolonie darf
    gleichzeitig zum Militär gehen, sonst fehlen Arbeitskräfte überall.
    """
    return int(ressourcen_dict.get("bevoelkerung", 0) * MAX_VERTEIDIGER_ANTEIL)


def personal_info(ressourcen_dict, liste_gebaeude):
    verfuegbar = int(ressourcen_dict.get("bevoelkerung", 0) + ressourcen_dict.get("roboter", 0))
    # Fortgeschrittener Kurs (Gegner): Verteidiger sind Bewohner, die
    # nicht mehr als Arbeitskraefte zur Verfuegung stehen. Fuer die
    # Anzeige im HUD gilt derselbe Abzug wie im Wirtschaftstick.
    verfuegbar = max(0, verfuegbar - int(ressourcen_dict.get("verteidiger", 0)))
    # Fortgeschrittener Kurs (Logistik): Gebaeude ohne Strassenanbindung
    # stehen still und brauchen deshalb kein Personal.
    bedarf = sum(personalbedarf(g["typ"]) for g in liste_gebaeude
                 if not g.get("stillstand_grund"))
    return verfuegbar, bedarf


def park_nahrungsfaktor(liste_gebaeude):
    """Berechnet den Nahrungsverbrauchsbonus durch Parks.

    Jeder Park senkt den Verbrauch um 5 Prozentpunkte. Der Bonus ist bei
    30 Prozent gedeckelt, damit viele Parks die Nahrung nicht komplett
    kostenlos machen.
    """
    anzahl_parks = sum(g.get("typ") == 19 for g in liste_gebaeude)
    return max(0.70, 1.0 - anzahl_parks * 0.05)


def eisen_fund_chance():
    """Gibt die aktuelle Eisen-Fundchance der normalen Mine zurück.

    Die normale Mine bleibt eine frühe Möglichkeit: Sie findet standardmäßig
    gelegentlich Eisen. `Eisenerkundung` erhöht die Chance deutlich und
    `Tiefenbohrung` verbessert sie zusätzlich. Die spätere Eisenmine braucht
    diese Zufallschance nicht, sondern produziert planbar Eisen.
    """
    chance = 0.10
    if forschung.ist_technologie_erforscht("eisenerkundung"):
        chance += 0.25
    if forschung.ist_technologie_erforscht("tiefenbohrung"):
        chance += 0.10
    return min(1.0, chance)


def _produktion_multiplikator(typ_index, ress_name):
    faktor = 1.0
    # Fortgeschrittener Kurs (Planeten): Rohstoff-Boni des Planeten
    # wirken auf JEDES produzierende Gebaeude. Mars z.B. liefert 2,5 x
    # Eisen, der Mond 1,5 x Forschung. Faktor 1.0 aendert nichts.
    if ress_name in _planeten_faktoren:
        faktor *= _planeten_faktoren[ress_name]
    if forschung.ist_technologie_erforscht("produktion"):
        faktor *= 1.25
    if _prestige_bonus_aktiv:
        faktor *= 1.05
    if ress_name == "energie" and forschung.ist_technologie_erforscht("verbesserte_generatoren"):
        faktor *= 1.10
    if typ_index in (2, 13) and forschung.ist_technologie_erforscht("verbesserte_landwirtschaft"):
        faktor *= 1.10
    if typ_index == 3 and forschung.ist_technologie_erforscht("verbesserte_aexte"):
        faktor *= 1.10
    if typ_index == 4 and forschung.ist_technologie_erforscht("effizienter_aufbau"):
        faktor *= 1.10
    if typ_index == 5 and forschung.ist_technologie_erforscht("verbesserte_marktstaende"):
        faktor *= 1.10
    if typ_index == 7 and ress_name == "forschung" and forschung.ist_technologie_erforscht("neue_instrumente"):
        faktor *= 1.05
    if typ_index == 8 and forschung.ist_technologie_erforscht("tiefenbohrung"):
        faktor *= 1.50
    if typ_index == 13 and forschung.ist_technologie_erforscht("gewaechshaus_effizienz"):
        faktor *= 1.15
    if typ_index == 12 and forschung.ist_technologie_erforscht("stahlverarbeitung_plus"):
        faktor *= 1.20
    # Zufallsereignis Systemausfall: waehrend der Stoerung liefern alle
    # Energiegebaeude nur noch 70 Prozent ihrer normalen Leistung.
    if ress_name == "energie" and _energie_stoerung > 0:
        faktor *= SYSTEMAUSFALL_FAKTOR
    return faktor


def _waldbetrieb_moeglich(gebaeude):
    if not forschung.ist_technologie_erforscht("forstwirtschaft"):
        return True
    if "wald_vorrat" not in gebaeude:
        gebaeude["wald_vorrat"] = 30
        gebaeude["wald_nachwuchs"] = 0
    if gebaeude["wald_vorrat"] > 0:
        return True
    gebaeude["wald_nachwuchs"] += 1.5
    if gebaeude["wald_nachwuchs"] >= 6:
        gebaeude["wald_vorrat"] = 30
        gebaeude["wald_nachwuchs"] = 0
        return True
    return False


def ressourcen_produzieren(ressourcen_dict, liste_gebaeude, karten_daten=None):
    global _wirtschafts_tick, _lager_bonus_aktiv, _prestige_bonus_aktiv
    _wirtschafts_tick += 1
    _lager_bonus_aktiv = any(g["typ"] == 14 for g in liste_gebaeude)
    zufriedenheit_aktualisieren(ressourcen_dict, liste_gebaeude)
    _prestige_bonus_aktiv = any(g["typ"] == 17 for g in liste_gebaeude)
    # Zufallsereignisse: Meteoritenschauer und Systemausfall laufen ab.
    _schaden_ticken(liste_gebaeude)
    if _energie_stoerung > 0:
        energie_stoerung_setzen(_energie_stoerung - 1)

    nahrungsverbrauch = ressourcen_dict.get("bevoelkerung", 0) * 0.05
    if forschung.ist_technologie_erforscht("hoeher_saettigende_nahrung"):
        nahrungsverbrauch *= 0.95
    # Parks wirken global auf die Kolonie und brauchen keinen eigenen
    # Personalbedarf. Der Faktor wird vor dem eigentlichen Verbrauch genutzt.
    nahrungsverbrauch *= park_nahrungsfaktor(liste_gebaeude)
    ressourcen_dict["nahrung"] = max(0.0, ressourcen_dict.get("nahrung", 0) - nahrungsverbrauch)

    verfuegbares_personal = int(ressourcen_dict.get("bevoelkerung", 0) + ressourcen_dict.get("roboter", 0))
    # Fortgeschrittener Kurs (Gegner): Verteidiger sind weiterhin Bewohner
    # (sie essen mit, sie zaehlen zur Bevoelkerung), aber sie dienen dem
    # Militaer und stehen als Arbeitskraefte nicht mehr zur Verfuegung.
    # Deshalb werden sie hier vom verfuegbaren Personal abgezogen —
    # mindestens 0, damit ein negatives Personal nicht moeglich ist.
    # Das ist der Zielkonflikt: Jede Kaserne schwaecht die Wirtschaft.
    verfuegbares_personal = max(
        0, verfuegbares_personal - int(ressourcen_dict.get("verteidiger", 0)))
    aktive_labore = 0
    for gebaeude in liste_gebaeude:
        typ_index = gebaeude["typ"]
        # Fortgeschrittener Kurs (Logistik): Ein Gebaeude ohne Strassen-
        # anbindung steht still. Es verbraucht nichts, produziert nichts
        # und belegt auch kein Personal. Das Merkmal setzt logistik.py
        # beim Bauen, Abreissen, Laden und bei einem neuen Spiel.
        if gebaeude.get("stillstand_grund"):
            gebaeude["arbeitet"] = False
            continue
        wirtschaft = GEBAEUDE_WIRTSCHAFT[typ_index]
        personal = personalbedarf(typ_index)
        if personal > verfuegbares_personal:
            gebaeude["arbeitet"] = False
            continue
        if typ_index == 3 and not _waldbetrieb_moeglich(gebaeude):
            gebaeude["arbeitet"] = False
            continue

        verbrauch = dict(wirtschaft.get("verbrauch", {}))
        produktion = dict(wirtschaft.get("produktion", {}))
        if forschung.ist_technologie_erforscht("energieoptimierung") and "energie" in verbrauch:
            verbrauch["energie"] *= 0.95
        if typ_index == 1 and forschung.ist_technologie_erforscht("reaktor_upgrade"):
            verbrauch["kohle"] = verbrauch.get("kohle", 0) + 1
            produktion["energie"] = produktion.get("energie", 0) + 3

        if typ_index == 8:
            # Die normale Mine findet Eisen zufällig. Die Funktion liefert
            # bewusst eine Zahl zwischen 0 und 1, die direkt mit random()
            # verglichen werden kann.
            if random.random() < eisen_fund_chance():
                produktion["eisen"] = produktion.get("eisen", 0) + 1
        if forschung.ist_technologie_erforscht("stein_effizienz") and typ_index == 4:
            verbrauch["energie"] = max(0, verbrauch.get("energie", 0) - 1)
        if forschung.ist_technologie_erforscht("mini_reaktor") and wirtschaft.get("grosse_anlage") and typ_index != 1:
            produktion["energie"] = produktion.get("energie", 0) + 1
        # Fortgeschrittener Kurs (Gegner): Die Kaserne bildet Verteidiger
        # aus, aber es duerfen nie mehr als MAX_VERTEIDIGER_ANTEIL der
        # Bevoelkerung gleichzeitig Verteidiger sein. Hat die Kolonie das
        # Kontingent erreicht, produziert die Kaserne bis auf Weiteres
        # nichts mehr (sie verbraucht aber weiter Nahrung und Energie).
        if typ_index == 21 and ressourcen_dict.get("verteidiger", 0) >= verteidiger_kontingent(ressourcen_dict):
            produktion.pop("verteidiger", None)

        if any(not _hat_genug(ressourcen_dict, name, menge) for name, menge in verbrauch.items()):
            gebaeude["arbeitet"] = False
            continue
        for ress_name, menge in verbrauch.items():
            ressourcen_dict[ress_name] = max(0.0, ressourcen_dict.get(ress_name, 0) - menge)
        verfuegbares_personal -= personal
        gebaeude["arbeitet"] = True
        if typ_index == 7:
            aktive_labore += 1

        effizient_bonus = 1.15 if forschung.ist_technologie_erforscht("anpassende_architektur") else 1.0
        # Meteoritenschauer: Ein getroffenes Gebaeude produziert nur noch
        # 20 Prozent (also 80 Prozent weniger) bis der Schaden abgelaufen ist.
        schaden_faktor = (BESCHAEDIGT_FAKTOR
                          if gebaeude.get("beschaedigt_rest", 0) > 0 else 1.0)
        for ress_name, menge in produktion.items():
            faktor = (effizient_bonus
                      * _produktion_multiplikator(typ_index, ress_name)
                      * schaden_faktor)
            ressourcen_dict[ress_name] = ressourcen_dict.get(ress_name, 0) + menge * faktor
        if typ_index == 3 and forschung.ist_technologie_erforscht("forstwirtschaft"):
            gebaeude["wald_vorrat"] = max(0, gebaeude.get("wald_vorrat", 30) - 1)

    forschung.forschung_tick(ressourcen_dict, aktive_labore)
    ressourcen_begrenzen(ressourcen_dict)
    ressourcen_dict["personal_verfuegbar"] = int(ressourcen_dict.get("bevoelkerung", 0) + ressourcen_dict.get("roboter", 0))
    # Fortgeschrittener Kurs (Logistik): Stillstehende Gebaeude belegen kein
    # Personal — derselbe Filter wie in personal_info(), damit HUD und
    # Wirtschaftstick immer dieselbe Zahl anzeigen.
    ressourcen_dict["personal_bedarf"] = sum(personalbedarf(g["typ"]) for g in liste_gebaeude
                                             if not g.get("stillstand_grund"))
    ressourcen_dict["wirtschafts_tick"] = _wirtschafts_tick


def energie_status(ressourcen_dict):
    return f"Energie {ressourcen_dict.get('energie', 0):.0f}/{maximaler_speicher('energie'):.0f}"


def ressourcen_limit_text(ressourcen_dict, name):
    return f"{ressourcen_dict.get(name, 0):.1f}/{maximaler_speicher(name):.0f}"


def terraformieren(ressourcen_dict, karten_daten, kachel_x, kachel_y):
    if not forschung.ist_technologie_erforscht("terraforming"):
        return False, "Terraforming ist noch nicht erforscht."
    if not (0 <= kachel_y < len(karten_daten) and 0 <= kachel_x < len(karten_daten[0])):
        return False, "Diese Kachel liegt außerhalb der Karte."
    if karten_daten[kachel_y][kachel_x] == 1:
        return False, "Diese Kachel ist bereits fruchtbarer Boden."
    kosten = {"energie": 5, "stein": 3}
    if any(ressourcen_dict.get(name, 0) < wert for name, wert in kosten.items()):
        return False, "Terraforming benötigt 5 Energie und 3 Stein."
    for name, wert in kosten.items():
        ressourcen_dict[name] -= wert
    karten_daten[kachel_y][kachel_x] = 1
    return True, "Kachel wurde in fruchtbaren Boden umgewandelt."
