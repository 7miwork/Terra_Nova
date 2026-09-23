"""Forschungsbaum und Forschungsfortschritt für Stunde 11."""

import pygame
import hud
import ton


TECHNOLOGIEN = [
    # Gebäude
    {"id": "effiziente_bautechnik", "name": "Effiziente Bautechnik", "kategorie": "Gebäude",
     "beschreibung": "Alle Baukosten sind 5 Prozent günstiger.", "kosten": 30, "zeit": 8,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "kompakte_maschinen", "name": "Kompakte Maschinen", "kategorie": "Gebäude",
     "beschreibung": "Bis zu zwei Gebäude können eine Kachel nutzen.", "kosten": 45, "zeit": 12,
     "voraussetzung": "effiziente_bautechnik", "schaltet_gebaeude_frei": None},
    {"id": "anpassende_architektur", "name": "Anpassende Architektur", "kategorie": "Gebäude",
     "beschreibung": "Gut versorgte Betriebe erhalten automatisch bis zu 15 Prozent Effizienz.",
     "kosten": 140, "zeit": 35, "voraussetzung": "kompakte_maschinen", "schaltet_gebaeude_frei": None},
    # Energie
    {"id": "energieoptimierung", "name": "Energieoptimierung", "kategorie": "Energie",
     "beschreibung": "Der Energieverbrauch aller Gebäude sinkt um 5 Prozent.", "kosten": 35, "zeit": 9,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "verbesserte_generatoren", "name": "Verbesserte Generatoren", "kategorie": "Energie",
     "beschreibung": "Energieproduktion steigt um 10 Prozent.", "kosten": 55, "zeit": 14,
     "voraussetzung": "energieoptimierung", "schaltet_gebaeude_frei": None},
    {"id": "energiespeicher", "name": "Energiespeicher", "kategorie": "Energie",
     "beschreibung": "Die maximale Energiespeicherkapazität steigt um 25 Prozent.", "kosten": 50, "zeit": 12,
     "voraussetzung": "energieoptimierung", "schaltet_gebaeude_frei": None},
    {"id": "fusionsreaktor", "name": "Fusionsreaktor", "kategorie": "Energie",
     "beschreibung": "Schaltet einen sehr leistungsstarken Energieerzeuger frei.", "kosten": 160, "zeit": 40,
     "voraussetzung": "verbesserte_generatoren", "schaltet_gebaeude_frei": 10},
    {"id": "mini_reaktor", "name": "Mini-Reaktor", "kategorie": "Energie",
     "beschreibung": "Große Gebäude erzeugen zusätzlich 1 Energie pro Tick.", "kosten": 95, "zeit": 24,
     "voraussetzung": "verbesserte_generatoren", "schaltet_gebaeude_frei": None},
    # Forschung
    {"id": "verbesserte_laborausruestung", "name": "Verbesserte Laborausrüstung", "kategorie": "Forschung",
     "beschreibung": "Die Forschungsgeschwindigkeit steigt um 10 Prozent.", "kosten": 40, "zeit": 10,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "neue_instrumente", "name": "Neue Geräte und Instrumente", "kategorie": "Forschung",
     "beschreibung": "Labore erzeugen 5 Prozent mehr Forschungspunkte.", "kosten": 60, "zeit": 15,
     "voraussetzung": "verbesserte_laborausruestung", "schaltet_gebaeude_frei": None},
    {"id": "quantencomputer", "name": "Quantencomputer", "kategorie": "Forschung",
     "beschreibung": "Endgame: Forschungsgeschwindigkeit steigt um weitere 40 Prozent.", "kosten": 180, "zeit": 45,
     "voraussetzung": "neue_instrumente", "schaltet_gebaeude_frei": None},
    # Automatisierung
    {"id": "einfache_robotik", "name": "Einfache Robotik", "kategorie": "Automatisierung",
     "beschreibung": "Schaltet die Roboterfabrik frei; Roboter können arbeiten.", "kosten": 75, "zeit": 18,
     "voraussetzung": None, "schaltet_gebaeude_frei": 11},
    {"id": "autonome_fabriken", "name": "Autonome Fabriken", "kategorie": "Automatisierung",
     "beschreibung": "Produktionsgebäude benötigen 30 Prozent weniger Personal.", "kosten": 170, "zeit": 42,
     "voraussetzung": "einfache_robotik", "schaltet_gebaeude_frei": None},
    # Steinmetz
    {"id": "effizienter_aufbau", "name": "Effizienter Aufbau", "kategorie": "Steinmetz",
     "beschreibung": "Steinmetze produzieren 10 Prozent mehr Stein.", "kosten": 35, "zeit": 9,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "tiefenbohrung", "name": "Tiefenbohrung", "kategorie": "Steinmetz",
     "beschreibung": "Neue tiefe Vorkommen erhöhen die Ausbeute von Minen.", "kosten": 70, "zeit": 18,
     "voraussetzung": "effizienter_aufbau", "schaltet_gebaeude_frei": None},
    # Holzfäller
    {"id": "verbesserte_aexte", "name": "Verbesserte Äxte", "kategorie": "Holzfäller",
     "beschreibung": "Holzfäller produzieren 10 Prozent mehr Holz.", "kosten": 35, "zeit": 9,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "forstwirtschaft", "name": "Forstwirtschaft", "kategorie": "Holzfäller",
     "beschreibung": "Wälder wachsen schneller nach, wenn sie abgeholzt sind.", "kosten": 70, "zeit": 18,
     "voraussetzung": "verbesserte_aexte", "schaltet_gebaeude_frei": None},
    {"id": "effizientere_holzverwendung", "name": "Effizientere Holzverwendung", "kategorie": "Holzfäller",
     "beschreibung": "Der Holzanteil aller Baukosten sinkt um 5 Prozent.", "kosten": 65, "zeit": 16,
     "voraussetzung": "forstwirtschaft", "schaltet_gebaeude_frei": None},
    # Marktplatz
    {"id": "verbesserte_marktstaende", "name": "Verbesserte Marktstände", "kategorie": "Marktplatz",
     "beschreibung": "Marktplätze erzeugen 10 Prozent mehr Gold.", "kosten": 40, "zeit": 10,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "ressourcenhandel", "name": "Ressourcenhandel", "kategorie": "Marktplatz",
     "beschreibung": "Ressourcen können am Marktplatz im Kurs 2:1 getauscht werden.", "kosten": 65, "zeit": 16,
     "voraussetzung": "verbesserte_marktstaende", "schaltet_gebaeude_frei": None},
    {"id": "handel_mit_kolonien", "name": "Handel mit anderen Kolonien", "kategorie": "Marktplatz",
     "beschreibung": "Andere Kolonien schicken zeitweise Angebote.", "kosten": 100, "zeit": 25,
     "voraussetzung": "ressourcenhandel", "schaltet_gebaeude_frei": None},
    # Farm
    {"id": "verbesserte_landwirtschaft", "name": "Verbesserte Landwirtschaft", "kategorie": "Farm",
     "beschreibung": "Farmen erzeugen 10 Prozent mehr Nahrung.", "kosten": 40, "zeit": 10,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "hoeher_saettigende_nahrung", "name": "Höher sättigende Nahrung", "kategorie": "Farm",
     "beschreibung": "Der Nahrungsverbrauch pro Bewohner sinkt um 5 Prozent.", "kosten": 55, "zeit": 14,
     "voraussetzung": "verbesserte_landwirtschaft", "schaltet_gebaeude_frei": None},
    {"id": "terraforming", "name": "Terraforming für Farmbau", "kategorie": "Farm",
     "beschreibung": "Freie Kacheln können in fruchtbaren Boden umgewandelt werden.", "kosten": 85, "zeit": 22,
     "voraussetzung": "verbesserte_landwirtschaft", "schaltet_gebaeude_frei": None},
    # Früherer Stunde-10-Baum bleibt als Einstieg erhalten.
    {"id": "wohnbau", "name": "Wohnbau", "kategorie": "Grundlagen",
     "beschreibung": "Schaltet das Wohnhaus frei.", "kosten": 30, "zeit": 8,
     "voraussetzung": None, "schaltet_gebaeude_frei": 6},
    {"id": "produktion", "name": "Produktions-Boost", "kategorie": "Grundlagen",
     "beschreibung": "Alle Produktionsgebäude erzeugen 25 Prozent mehr.", "kosten": 50, "zeit": 12,
     "voraussetzung": "wohnbau", "schaltet_gebaeude_frei": None},
    {"id": "stein_effizienz", "name": "Stein-Effizienz", "kategorie": "Grundlagen",
     "beschreibung": "Steinmetze verbrauchen 1 Energie weniger.", "kosten": 25, "zeit": 7,
     "voraussetzung": None, "schaltet_gebaeude_frei": None},
    {"id": "minenbau", "name": "Minenbau", "kategorie": "Grundlagen",
     "beschreibung": "Schaltet die Mine für Kohle und erste Eisenfunde frei.", "kosten": 40, "zeit": 10,
     "voraussetzung": "stein_effizienz", "schaltet_gebaeude_frei": 8},
    # Diese Forschung verbessert die Suche der normalen Mine. Eisen bleibt
    # absichtlich unregelmäßig, wird aber deutlich wahrscheinlicher.
    {"id": "eisenerkundung", "name": "Eisenerkundung", "kategorie": "Metallurgie",
     "beschreibung": "Minen finden deutlich häufiger Eisen.", "kosten": 70, "zeit": 16,
     "voraussetzung": "minenbau", "schaltet_gebaeude_frei": None},
    {"id": "reaktor_upgrade", "name": "Verbesserter Reaktor", "kategorie": "Grundlagen",
     "beschreibung": "Reaktoren erzeugen mehr Energie und verbrauchen Kohle.", "kosten": 60, "zeit": 15,
     "voraussetzung": "minenbau", "schaltet_gebaeude_frei": None},
    # Neue Kategorie: Metallurgie
    {"id": "stahlverarbeitung", "name": "Stahlverarbeitung", "kategorie": "Metallurgie",
     "beschreibung": "Schaltet das Stahlwerk frei, das Eisen und Kohle zu Stahl verarbeitet.", "kosten": 90, "zeit": 22,
     "voraussetzung": "minenbau", "schaltet_gebaeude_frei": 12},
    {"id": "eisenminenbau", "name": "Eisenminenbau", "kategorie": "Metallurgie",
     "beschreibung": "Teure Spezialforschung: Schaltet eine echte Eisenmine frei.", "kosten": 240, "zeit": 48,
     "voraussetzungen": ["eisenerkundung", "stahlverarbeitung"], "schaltet_gebaeude_frei": 18},
    {"id": "stahlverarbeitung_plus", "name": "Hochöfen", "kategorie": "Metallurgie",
     "beschreibung": "Stahlwerke erzeugen 20 Prozent mehr Stahl.", "kosten": 120, "zeit": 28,
     "voraussetzung": "stahlverarbeitung", "schaltet_gebaeude_frei": None},
    # Neue Kategorie: Nahrung
    {"id": "gewaechshausbau", "name": "Gewächshausbau", "kategorie": "Nahrung",
     "beschreibung": "Schaltet Gewächshäuser als zweite Nahrungsquelle frei.", "kosten": 75, "zeit": 18,
     "voraussetzung": None, "schaltet_gebaeude_frei": 13},
    {"id": "gewaechshaus_effizienz", "name": "Hydroponik", "kategorie": "Nahrung",
     "beschreibung": "Gewächshäuser erzeugen 15 Prozent mehr Nahrung.", "kosten": 110, "zeit": 25,
     "voraussetzung": "gewaechshausbau", "schaltet_gebaeude_frei": None},
    # Neue Kategorie: Logistik
    {"id": "logistik_lager", "name": "Logistik-Grundlagen", "kategorie": "Logistik",
     "beschreibung": "Schaltet ein Lagerhaus für die Kolonie frei.", "kosten": 70, "zeit": 16,
     "voraussetzung": None, "schaltet_gebaeude_frei": 14},
    {"id": "lagerhaus_ausbau", "name": "Großlager", "kategorie": "Logistik",
     "beschreibung": "Lagerhäuser erhöhen die Speichergrenzen aller Ressourcen um 50 Prozent.", "kosten": 130, "zeit": 30,
     "voraussetzung": "logistik_lager", "schaltet_gebaeude_frei": None},
    # Neue Kategorie: Kolonie und Wohnen
    {"id": "wohnblockbau", "name": "Wohnblockbau", "kategorie": "Kolonie",
     "beschreibung": "Schaltet Wohnblöcke mit höherer Bevölkerungskapazität frei.", "kosten": 85, "zeit": 20,
     "voraussetzung": "wohnbau", "schaltet_gebaeude_frei": 15},
    # Neue Kategorie: Handel
    {"id": "interkolonialhandel", "name": "Interkolonialer Handel", "kategorie": "Handel",
     "beschreibung": "Schaltet einen Handelsposten für Angebote anderer Kolonien frei.", "kosten": 115, "zeit": 27,
     "voraussetzung": "handel_mit_kolonien", "schaltet_gebaeude_frei": 16},
    {"id": "handelsrouten", "name": "Handelsrouten", "kategorie": "Handel",
     "beschreibung": "NPC-Angebote erscheinen häufiger und geben bessere Mengen.", "kosten": 150, "zeit": 34,
     "voraussetzung": "interkolonialhandel", "schaltet_gebaeude_frei": None},
    # Neue Kategorie: Prestige
    {"id": "koloniezentrum", "name": "Koloniezentrum", "kategorie": "Prestige",
     "beschreibung": "Schaltet ein Koloniezentrum frei, das die gesamte Produktion leicht stärkt.", "kosten": 220, "zeit": 50,
     "voraussetzung": "wohnblockbau", "schaltet_gebaeude_frei": 17},
    # ── Fortgeschrittener Kurs (Gegner): Militär und Verteidigung ────────────
    # Die neue Kategorie baut auf bestehenden Technologien auf: Militär-
    # training als Einstieg, danach Schiffbau und Laser. Schutzschilde sind
    # eine reine Verteidigungsverbesserung ohne eigenes Gebäude.
    {"id": "militaertraining", "name": "Militärtraining", "kategorie": "Verteidigung",
     "beschreibung": "Schaltet die Kaserne frei, in der Bürger zu Verteidigern ausgebildet werden.", "kosten": 90, "zeit": 20,
     "voraussetzung": None, "schaltet_gebaeude_frei": 21},
    {"id": "raumschiffbau", "name": "Raumschiffbau", "kategorie": "Verteidigung",
     "beschreibung": "Schaltet die Raumschiffwerft frei, die kampfbereite Schiffe baut.", "kosten": 170, "zeit": 36,
     "voraussetzungen": ["militaertraining", "stahlverarbeitung"], "schaltet_gebaeude_frei": 22},
    {"id": "laserverteidigung", "name": "Laserverteidigung", "kategorie": "Verteidigung",
     "beschreibung": "Schaltet den Laserturm als feste Verteidigungsanlage frei.", "kosten": 130, "zeit": 28,
     "voraussetzung": "militaertraining", "schaltet_gebaeude_frei": 23},
    {"id": "schutzschilde", "name": "Schutzschilde", "kategorie": "Verteidigung",
     "beschreibung": "Energiefelder erhöhen die Verteidigungsstärke der Kolonie um 25 Prozent.", "kosten": 150, "zeit": 32,
     "voraussetzung": "laserverteidigung", "schaltet_gebaeude_frei": None},
]

_fenster = None
_menu_offen = False
_scroll = 0
_erforschte_technologien = set()
_forschungsauftrag = None


def forschung_initialisieren(fenster_obj):
    global _fenster
    _fenster = fenster_obj


def forschung_zuruecksetzen():
    global _erforschte_technologien, _forschungsauftrag, _scroll, _menu_offen
    _erforschte_technologien = set()
    _forschungsauftrag = None
    _scroll = 0
    _menu_offen = False


def zustand_exportieren():
    """Gibt den dauerhaften Forschungszustand für einen Spielstand zurück."""
    return {
        "erforschte_technologien": sorted(_erforschte_technologien),
        "forschungsauftrag": dict(_forschungsauftrag) if _forschungsauftrag else None,
    }


def zustand_importieren(daten):
    """Stellt Forschungsfortschritt aus einem geprüften JSON-Dictionary wieder her."""
    global _erforschte_technologien, _forschungsauftrag, _scroll, _menu_offen
    daten = daten if isinstance(daten, dict) else {}
    gueltige_ids = {technologie["id"] for technologie in TECHNOLOGIEN}
    erforscht = daten.get("erforschte_technologien", [])
    if not isinstance(erforscht, list):
        erforscht = []
    _erforschte_technologien = {str(technologie_id) for technologie_id in erforscht
                                if str(technologie_id) in gueltige_ids}
    auftrag = daten.get("forschungsauftrag")
    if isinstance(auftrag, dict) and auftrag.get("id") in gueltige_ids:
        try:
            fortschritt = max(0.0, float(auftrag.get("fortschritt", 0.0)))
            ziel = max(1.0, float(auftrag.get("ziel", 1.0)))
            _forschungsauftrag = {"id": auftrag["id"],
                                  "fortschritt": fortschritt,
                                  "ziel": ziel}
        except (TypeError, ValueError):
            _forschungsauftrag = None
    else:
        _forschungsauftrag = None
    _scroll = 0
    _menu_offen = False


def forschung_menu_umschalten():
    global _menu_offen
    _menu_offen = not _menu_offen


def forschung_menu_ist_offen():
    return _menu_offen


def _technologie_finden(technologie_id):
    return next((t for t in TECHNOLOGIEN if t["id"] == technologie_id), None)


def technologie_name(technologie_id):
    technologie = _technologie_finden(technologie_id)
    return technologie["name"] if technologie else technologie_id


def ist_technologie_erforscht(technologie_id):
    return technologie_id in _erforschte_technologien


def anzahl_erforscht():
    return len(_erforschte_technologien)


def forschung_laeuft():
    return _forschungsauftrag is not None


def forschung_status(technologie_id):
    if technologie_id in _erforschte_technologien:
        return "erforscht"
    if _forschungsauftrag and _forschungsauftrag["id"] == technologie_id:
        return "in_forschung"
    technologie = _technologie_finden(technologie_id)
    if technologie is None:
        return "unbekannt"
    voraussetzung = technologie.get("voraussetzungen")
    if voraussetzung is None:
        voraussetzung = technologie.get("voraussetzung")
    if voraussetzung is None:
        return "bereit"
    if isinstance(voraussetzung, str):
        voraussetzung = [voraussetzung]
    return "bereit" if all(ist_technologie_erforscht(x) for x in voraussetzung) else "gesperrt"


def _voraussetzungen(technologie):
    voraussetzungen = technologie.get("voraussetzungen")
    if voraussetzungen is None:
        voraussetzungen = technologie.get("voraussetzung")
    if voraussetzungen is None:
        return []
    return [voraussetzungen] if isinstance(voraussetzungen, str) else list(voraussetzungen)


def technologie_erforschen(technologie_id, ressourcen_dict):
    global _forschungsauftrag
    technologie = _technologie_finden(technologie_id)
    if technologie is None:
        return False
    if ist_technologie_erforscht(technologie_id):
        hud.meldung_anzeigen("Diese Technologie ist bereits erforscht.")
        return False
    if _forschungsauftrag is not None:
        hud.meldung_anzeigen("Es läuft bereits eine Forschung.")
        return False
    fehlend = [technologie_name(x) for x in _voraussetzungen(technologie)
               if not ist_technologie_erforscht(x)]
    if fehlend:
        hud.meldung_anzeigen("Voraussetzung fehlt: " + ", ".join(fehlend))
        return False
    kosten = technologie["kosten"]
    if ressourcen_dict.get("forschung", 0) < kosten:
        hud.meldung_anzeigen(f"Nicht genug Forschungspunkte ({kosten} benötigt).")
        return False
    ressourcen_dict["forschung"] -= kosten
    _forschungsauftrag = {"id": technologie_id, "fortschritt": 0.0,
                          "ziel": float(technologie["zeit"])}
    hud.meldung_anzeigen(f"Forschung gestartet: {technologie['name']}")
    return True


def forschung_tick(ressourcen_dict, aktive_labore=1):
    global _forschungsauftrag
    if _forschungsauftrag is None:
        return None
    if aktive_labore <= 0:
        return None
    tempo = float(aktive_labore)
    if ist_technologie_erforscht("verbesserte_laborausruestung"):
        tempo += 0.10
    if ist_technologie_erforscht("quantencomputer"):
        tempo += 0.40
    _forschungsauftrag["fortschritt"] += tempo
    if _forschungsauftrag["fortschritt"] >= _forschungsauftrag["ziel"]:
        technologie_id = _forschungsauftrag["id"]
        technologie = _technologie_finden(technologie_id)
        _erforschte_technologien.add(technologie_id)
        _forschungsauftrag = None
        hud.meldung_anzeigen(f"Forschung abgeschlossen: {technologie['name']}")
        # Fortgeschrittener Kurs: kleine Hoer-Bestaetigung fuer die Forschung.
        ton.sound_abspielen("forschung_fertig")
        return technologie_id
    return None


def forschung_fortschritt_text():
    if _forschungsauftrag is None:
        return "Keine Forschung aktiv"
    technologie = technologie_name(_forschungsauftrag["id"])
    return f"{technologie}: {int(_forschungsauftrag['fortschritt'])}/{int(_forschungsauftrag['ziel'])}"


def _taste_fuer_index(index):
    return f"F{index + 1}" if index < 12 else "klicken"


def forschung_menu_scroll(delta):
    global _scroll
    max_scroll = max(0, len(TECHNOLOGIEN) - 12)
    _scroll = max(0, min(max_scroll, _scroll + delta))


def forschung_menu_mausevent(pos, ressourcen_dict):
    if not _menu_offen:
        return False
    x, y = pos
    if not (35 <= x <= _fenster.get_width() - 35 and 82 <= y <= 650):
        return False
    index = _scroll + (y - 82) // 44
    if 0 <= index < len(TECHNOLOGIEN):
        technologie_erforschen(TECHNOLOGIEN[index]["id"], ressourcen_dict)
        return True
    return False


def forschung_menu_taste(key, ressourcen_dict):
    if not _menu_offen:
        return False
    if key == pygame.K_PAGEUP:
        forschung_menu_scroll(-6)
        return True
    if key == pygame.K_PAGEDOWN:
        forschung_menu_scroll(6)
        return True
    tasten = [pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5,
              pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10,
              pygame.K_F11, pygame.K_F12]
    if key in tasten:
        index = _scroll + tasten.index(key)
        if index < len(TECHNOLOGIEN):
            technologie_erforschen(TECHNOLOGIEN[index]["id"], ressourcen_dict)
        return True
    return False


def _status_farbe(status):
    return {"erforscht": (120, 230, 130), "in_forschung": (255, 220, 90),
            "bereit": (235, 235, 235), "gesperrt": (130, 130, 140)}.get(status, (180, 180, 180))


def forschung_menu_zeichnen(ressourcen_dict, gebaeude_typen):
    if _fenster is None or not _menu_offen:
        return
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((5, 8, 18, 220))
    _fenster.blit(overlay, (0, 0))
    gross = pygame.font.Font(None, 32)
    klein = pygame.font.Font(None, 18)
    titel = gross.render("FORSCHUNG  (F schließt)", True, (255, 255, 255))
    _fenster.blit(titel, (30, 18))
    punkte = klein.render(f"Punkte: {ressourcen_dict.get('forschung', 0):.1f}    |    {forschung_fortschritt_text()}", True, (120, 220, 255))
    _fenster.blit(punkte, (30, 47))
    hinweis = klein.render("F1–F12 starten sichtbare Forschung | Mausrad/Bild auf-ab scrollen", True, (170, 180, 200))
    _fenster.blit(hinweis, (30, 66))
    for sichtbar in range(12):
        index = _scroll + sichtbar
        if index >= len(TECHNOLOGIEN):
            break
        technologie = TECHNOLOGIEN[index]
        y = 82 + sichtbar * 44
        status = forschung_status(technologie["id"])
        farbe = _status_farbe(status)
        pygame.draw.rect(_fenster, (25, 30, 45), (28, y - 2, 944, 39))
        pygame.draw.rect(_fenster, farbe, (28, y - 2, 5, 39))
        status_text = {"erforscht": "ERFORSCHT", "in_forschung": "IN FORSCHUNG",
                       "bereit": "BEREIT", "gesperrt": "GESPERRT"}.get(status, status)
        zeile1 = f"{_taste_fuer_index(sichtbar)}  {technologie['name']} [{technologie['kategorie']}]  –  {status_text}"
        zeile2 = f"    {technologie['beschreibung']}  |  Kosten: {technologie['kosten']}  |  Zeit: {technologie['zeit']} Ticks"
        _fenster.blit(klein.render(zeile1, True, farbe), (42, y + 2))
        _fenster.blit(klein.render(zeile2, True, (185, 190, 205)), (42, y + 20))
    if _scroll > 0:
        _fenster.blit(klein.render("↑ weitere Forschungen oberhalb", True, (160, 180, 200)), (760, 18))
    if _scroll + 12 < len(TECHNOLOGIEN):
        _fenster.blit(klein.render("↓ weitere Forschungen unterhalb", True, (160, 180, 200)), (760, 47))
