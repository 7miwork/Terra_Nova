"""Planeten der Spielwelt und ihre Eigenschaften.

Wunschliste der Schuelerinnen und Schueler:

    Erde   - Startplanet
    Mond   - wenig Ressourcen, aber gute Forschung
    Mars   - viel Eisen, schwierige Bedingungen
    Alien  - unbekannte Lebensformen
    Vulkan - sehr viel Energie, aber gefaehrlich
    Eis    - Wasser im Ueberfluss

Nur "freigeschaltete" Planeten koennen besiedelt werden: Erde, Mond und
Mars (Phase 1 = Beweis der Kolonie-Architektur mit dem Duo Mond + Mars).
Die anderen drei folgen in Phase 2, sobald Wasser, Biomasse und Gefahr
ihre Rechnung haben.

Das Modul ist reine Datenlogik ohne pygame, damit die Tests ohne Fenster
laufen. Die Rohstoff-Faktoren wirken ueber
ressourcen.planeten_faktoren_setzen() direkt im Produktionsrechner, die
Karten-Parameter steuern main.karte_generieren().
"""

# Anzahl der Flaechen je Bodentyp, wenn ein Planet nichts Eigenes angibt.
# Die Werte sind die Originalwerte der ersten Version - kein Planet
# veraendert also ohne eigenen Eintrag das alte Kartenbild.
KARTEN_STANDARD = {
    "gras_flaechen": 8,      # fruchtbar - gut fuer Farmen
    "gestein_flaechen": 5,   # Felsen - viel Stein, Mining
    "sand_flaechen": 6,      # Wueste - wenig guter Boden
}

# Kosten jeder Koloniegruendung. Phase 2 darf das pro Planet
# unterschiedlich machen (Vulkanplanet teurer, etc.).
GRUENDUNGS_KOSTEN = {
    "gold": 120,
    "energie": 60,
    "holz": 40,
    "stein": 40,
}

# Pflichtfelder jedes Planeten - die Tests pruefen sie.
PFLICHTFELDER = ("id", "name", "untertitel", "beschreibung",
                 "freigeschaltet", "rohstoffe", "start", "karte",
                 "gefahr", "farbe")

PLANETEN = [
    {
        "id": "erde",
        "name": "Erde",
        "untertitel": "Startplanet",
        "beschreibung": "Gruener Heimatplanet mit ausgewogenem Boden.",
        "freigeschaltet": True,
        # Kein Eintrag = 1.0 auf alle Rohstoffe.
        "rohstoffe": {},
        # Kein Eintrag = die Grundwerte aus _neue_ressourcen().
        "start": {},
        "karte": {},                  # 8 Gras, 5 Gestein, 6 Sand (Original)
        "gefahr": 0,
        "farbe": (95, 195, 115),
    },
    {
        "id": "mond",
        "name": "Mond",
        "untertitel": "Forschungsstation",
        "beschreibung": "Wenig Ressourcen, aber dafuer gute Forschung.",
        "freigeschaltet": True,
        "rohstoffe": {"forschung": 1.5, "holz": 0.6, "stein": 0.7},
        "start": {"gold": 80, "energie": 40, "holz": 20,
                  "stein": 15, "nahrung": 40},
        "karte": {"gras_flaechen": 4, "gestein_flaechen": 9, "sand_flaechen": 3},
        "gefahr": 0,
        "farbe": (205, 205, 210),
    },
    {
        "id": "mars",
        "name": "Mars",
        "untertitel": "Eisenplanet",
        "beschreibung": "Viel Eisen, aber schwierige Bedingungen.",
        "freigeschaltet": True,
        # 2,5 x Eisen aus der Mine, dafuer knapp Energie.
        "rohstoffe": {"eisen": 2.5, "kohle": 1.5, "energie": 0.85},
        "start": {"gold": 90, "energie": 30, "holz": 20,
                  "stein": 25, "nahrung": 40},
        "karte": {"gras_flaechen": 3, "gestein_flaechen": 10, "sand_flaechen": 8},
        "gefahr": 1,
        "farbe": (215, 120, 80),
    },
    {
        "id": "alien",
        "name": "Alienplanet",
        "untertitel": "Unbekannte Lebensformen",
        "beschreibung": "Fremdes Leben - reich an Nahrung, rätselhaft.",
        "freigeschaltet": False,      # Phase 2: Biomasse und Leben
        "rohstoffe": {"nahrung": 1.4, "forschung": 1.2},
        "start": {"nahrung": 70},
        "karte": {"gras_flaechen": 12, "gestein_flaechen": 4, "sand_flaechen": 4},
        "gefahr": 1,
        "farbe": (175, 105, 220),
    },
    {
        "id": "vulkan",
        "name": "Vulkanplanet",
        "untertitel": "Energie, aber gefaehrlich",
        "beschreibung": "Sehr viel Energie - und sehr viel Gefahr.",
        "freigeschaltet": False,      # Phase 2: Gefahr- und Hitze-Rechnung
        "rohstoffe": {"energie": 1.6, "stein": 1.2},
        "start": {"energie": 90, "gold": 90},
        "karte": {"gras_flaechen": 2, "gestein_flaechen": 10, "sand_flaechen": 6},
        "gefahr": 2,
        "farbe": (240, 95, 70),
    },
    {
        "id": "eis",
        "name": "Eisplanet",
        "untertitel": "Wasser im Ueberfluss",
        "beschreibung": "Wasser im Ueberfluss, aber eisige Kaelt.",
        "freigeschaltet": False,      # Phase 2: Wasser und Energie-Rechnung
        "rohstoffe": {"nahrung": 1.3, "energie": 1.1},
        "start": {"nahrung": 90, "energie": 50},
        "karte": {"gras_flaechen": 6, "gestein_flaechen": 6, "sand_flaechen": 6},
        "gefahr": 1,
        "farbe": (140, 210, 245),
    },
]


def planet(planet_id):
    """Gibt das Daten-Dictionary des Planeten zurueck oder None."""
    for eintrag in PLANETEN:
        if eintrag["id"] == planet_id:
            return eintrag
    return None


def alle_ids():
    """Alle Planeten-IDs in der festgelegten Reihenfolge."""
    return [eintrag["id"] for eintrag in PLANETEN]


def spielbare_ids():
    """Nur die Planeten, die besiedelt werden duerfen."""
    return [eintrag["id"] for eintrag in PLANETEN
            if eintrag["freigeschaltet"]]


def ist_spielbar(planet_id):
    return planet_id in spielbare_ids()


def name(planet_id):
    """Anzeigename des Planeten (fremde IDs werden unveraendert gezeigt)."""
    eintrag = planet(planet_id)
    return eintrag["name"] if eintrag else str(planet_id)


def farbe(planet_id):
    """Akzentfarbe des Planeten fuer Menues und Anzeigen."""
    eintrag = planet(planet_id)
    return tuple(eintrag["farbe"]) if eintrag else (200, 200, 200)


def rohstoffe(planet_id):
    """Kopie der Produktionsfaktoren dieses Planeten."""
    eintrag = planet(planet_id)
    return dict(eintrag["rohstoffe"]) if eintrag else {}


def rohstoff_faktor(planet_id, rohstoff):
    """Faktor fuer EINE Ressource (1.0 = keine Aenderung)."""
    try:
        return float(rohstoffe(planet_id).get(rohstoff, 1.0))
    except (TypeError, ValueError):
        return 1.0


def startressourcen(planet_id):
    """Kopie der Startvorräte - werden ueber die Grundwerte gelegt."""
    eintrag = planet(planet_id)
    return dict(eintrag["start"]) if eintrag else {}


def karten_parameter(planet_id):
    """Flaechen-Zahlen fuer main.karte_generieren()."""
    parameter = dict(KARTEN_STANDARD)
    eintrag = planet(planet_id)
    if eintrag:
        for schluessel, wert in eintrag["karte"].items():
            if schluessel in parameter:
                parameter[schluessel] = int(wert)
    return parameter


def gruendungskosten(planet_id=None):
    """Kosten einer neuen Kolonie auf diesem Planeten."""
    # Phase 2: hier pro Planet unterscheiden (Vulkan z.B. teurer).
    del planet_id
    return dict(GRUENDUNGS_KOSTEN)


def naechster_freier_planet(besetzte_planeten):
    """Erster spielbarer Planet, der noch nicht besiedelt ist."""
    for planet_id in spielbare_ids():
        if planet_id not in besetzte_planeten:
            return planet_id
    return None
