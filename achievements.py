"""Achievement-System für Terra_Nova.

Die Achievements sind bewusst unabhängig von Pygame-Spielmechanik gehalten:
Das Spiel meldet Gebäude- und Handelsereignisse, während dieses Modul nur
Fortschritt sammelt, Ziele prüft und die Übersicht zeichnet.
"""

import pygame


ACHIEVEMENTS = [
    {"id": "erste_schritte", "titel": "Erste Schritte", "beschreibung": "Baue dein erstes Gebäude.", "punkte": 10, "fortschritt": "gesamt_gebaeude", "ziel": 1},
    {"id": "grundstein", "titel": "Grundstein gelegt", "beschreibung": "Errichte die Basis.", "punkte": 10, "fortschritt": "typ_0", "ziel": 1},
    {"id": "bauer", "titel": "Fleißiger Bauer", "beschreibung": "Baue insgesamt 5 Gebäude in dieser Kolonie.", "punkte": 15, "fortschritt": "gesamt_gebaeude", "ziel": 5},
    {"id": "stadtplaner", "titel": "Stadtplaner", "beschreibung": "Baue insgesamt 15 Gebäude in dieser Kolonie.", "punkte": 25, "fortschritt": "gesamt_gebaeude", "ziel": 15},
    {"id": "bauherr", "titel": "Großer Bauherr", "beschreibung": "Baue insgesamt 30 Gebäude in dieser Kolonie.", "punkte": 50, "fortschritt": "gesamt_gebaeude", "ziel": 30},
    {"id": "wohnraum", "titel": "Wohnraum schaffen", "beschreibung": "Baue mindestens 3 Wohnhäuser.", "punkte": 20, "fortschritt": "typ_6", "ziel": 3},
    {"id": "wohnblock", "titel": "Hoch hinaus", "beschreibung": "Baue mindestens 2 Wohnblöcke.", "punkte": 30, "fortschritt": "typ_15", "ziel": 2},
    {"id": "metropole", "titel": "Kleine Metropole", "beschreibung": "Erreiche 25 Bewohner.", "punkte": 40, "fortschritt": "max_bevoelkerung", "ziel": 25},
    {"id": "megastadt", "titel": "Megastadt", "beschreibung": "Erreiche 50 Bewohner.", "punkte": 80, "fortschritt": "max_bevoelkerung", "ziel": 50},
    {"id": "maschinenpark", "titel": "Maschinenpark", "beschreibung": "Baue eine Roboterfabrik.", "punkte": 25, "fortschritt": "typ_11", "ziel": 1},
    {"id": "stahlzeit", "titel": "Stahlzeit", "beschreibung": "Lagere mindestens 10 Stahl ein.", "punkte": 25, "fortschritt": "stahl", "ziel": 10},
    {"id": "energiereserve", "titel": "Energiereserve", "beschreibung": "Halte mindestens 90 Energie bereit.", "punkte": 20, "fortschritt": "energie", "ziel": 90},
    {"id": "wohlstand", "titel": "Wohlstand", "beschreibung": "Sammle mindestens 400 Gold.", "punkte": 25, "fortschritt": "gold", "ziel": 400},
    {"id": "voll_lager", "titel": "Gut vorbereitet", "beschreibung": "Fülle mindestens einen Ressourcenspeicher zu 95 Prozent.", "punkte": 25, "fortschritt": "speicher", "ziel": 1},
    {"id": "wissenschaftler", "titel": "Wissenschaftler", "beschreibung": "Erforsche deine erste Technologie.", "punkte": 20, "fortschritt": "forschungen", "ziel": 1},
    {"id": "forschungsprofi", "titel": "Forschungsprofi", "beschreibung": "Erforsche 5 Technologien.", "punkte": 45, "fortschritt": "forschungen", "ziel": 5},
    {"id": "genie", "titel": "Kolonie-Genie", "beschreibung": "Erforsche 10 Technologien.", "punkte": 80, "fortschritt": "forschungen", "ziel": 10},
    {"id": "haendler", "titel": "Erster Handel", "beschreibung": "Führe einen Handel durch.", "punkte": 20, "fortschritt": "handelsaktionen", "ziel": 1},
    {"id": "handelsmeister", "titel": "Handelsmeister", "beschreibung": "Führe 10 Handelsaktionen durch.", "punkte": 50, "fortschritt": "handelsaktionen", "ziel": 10},
    {"id": "terraformer", "titel": "Terraformer", "beschreibung": "Schaffe 20 fruchtbare Kacheln.", "punkte": 30, "fortschritt": "fruchtbare_kacheln", "ziel": 20},
    {"id": "ueberlebender", "titel": "Überlebender", "beschreibung": "Erreiche 30 Wirtschaftsticks.", "punkte": 30, "fortschritt": "wirtschafts_ticks", "ziel": 30},
    {"id": "nachhaltig", "titel": "Nachhaltige Kolonie", "beschreibung": "Halte 100 Nahrung und 100 Energie gleichzeitig bereit.", "punkte": 35, "fortschritt": "nachhaltigkeit", "ziel": 1},
    {"id": "roboter_army", "titel": "Roboter-Armee", "beschreibung": "Besitze mindestens 10 Roboter.", "punkte": 35, "fortschritt": "roboter", "ziel": 10},
    {"id": "koloniezentrum", "titel": "Zentrum der Kolonie", "beschreibung": "Baue das Koloniezentrum.", "punkte": 50, "fortschritt": "typ_17", "ziel": 1},
    {"id": "zielmeister", "titel": "Zielmeister", "beschreibung": "Erfülle die gewählten Siegbedingungen.", "punkte": 100, "fortschritt": "sieg", "ziel": 1},
    {"id": "perfekte_runde", "titel": "Perfekte Runde", "beschreibung": "Gewinne eine Partie und schalte mindestens 10 Achievements frei.", "punkte": 150, "fortschritt": "erreichte", "ziel": 10},
    {"id": "gruene_oase", "titel": "Grüne Oase", "beschreibung": "Baue einen Park.", "punkte": 20, "fortschritt": "typ_19", "ziel": 1},
    {"id": "solarpionier", "titel": "Solarpionier", "beschreibung": "Baue einen Solarreaktor.", "punkte": 30, "fortschritt": "typ_20", "ziel": 1},
    {"id": "zufriedene_kolonie", "titel": "Zufriedene Kolonie", "beschreibung": "Erreiche mindestens +30 Zufriedenheit.", "punkte": 45, "fortschritt": "zufriedenheit", "ziel": 30},
    # Fortgeschrittener Kurs (Logistik): Strassen bauen und alles anbinden.
    {"id": "strassenbauer", "titel": "Strassenbauer", "beschreibung": "Baue insgesamt 10 Strassen.", "punkte": 25, "fortschritt": "strassen", "ziel": 10},
    {"id": "gut_vernetzt", "titel": "Gut vernetzt", "beschreibung": "Stehe mit mindestens 10 Gebaeuden und ohne offene Anbindung da.", "punkte": 40, "fortschritt": "vernetzt", "ziel": 1},
    # Fortgeschrittener Kurs (Gegner): Militär-Erfolge.
    {"id": "erste_abwehr", "titel": "Erste Abwehr", "beschreibung": "Wehre den ersten Angriff ab.", "punkte": 30, "fortschritt": "abgewehrt", "ziel": 1},
    {"id": "festung", "titel": "Festung", "beschreibung": "Halte vier Lasertürme gleichzeitig.", "punkte": 50, "fortschritt": "typ_23", "ziel": 4},
    {"id": "flotte", "titel": "Flotte", "beschreibung": "Stelle 5 Raumschiffe gleichzeitig.", "punkte": 60, "fortschritt": "raumschiffe", "ziel": 5},
]

_fenster = None
_erreicht = set()
_zaehler = {}


def initialisieren(fenster_obj):
    global _fenster
    _fenster = fenster_obj


def neue_kolonie():
    """Setzt den Fortschritt der aktuellen Kolonie zurück.

    Bereits freigeschaltete Achievements bleiben erhalten, damit mehrere
    Partien nacheinander sinnvoll gespielt werden können.
    """
    global _zaehler
    _zaehler = {}


def zustand_zuruecksetzen():
    """Setzt Profil und aktuelle Achievement-Werte vollständig zurück."""
    global _erreicht, _zaehler
    _erreicht = set()
    _zaehler = {}


def zustand_exportieren():
    return {"erreicht": sorted(_erreicht), "zaehler": dict(_zaehler)}


def zustand_importieren(daten):
    global _erreicht, _zaehler
    daten = daten if isinstance(daten, dict) else {}
    ids = {eintrag["id"] for eintrag in ACHIEVEMENTS}
    erreicht = daten.get("erreicht", [])
    _erreicht = {str(wert) for wert in erreicht if str(wert) in ids}
    zaehler = daten.get("zaehler", {})
    _zaehler = {}
    if isinstance(zaehler, dict):
        for schluessel, wert in zaehler.items():
            try:
                _zaehler[str(schluessel)] = max(0.0, float(wert))
            except (TypeError, ValueError):
                continue


def gebaeude_gebaut(typ_index):
    _zaehler["gesamt_gebaeude"] = _zaehler.get("gesamt_gebaeude", 0) + 1
    schluessel = f"typ_{typ_index}"
    _zaehler[schluessel] = _zaehler.get(schluessel, 0) + 1


def handel_aktion():
    _zaehler["handelsaktionen"] = _zaehler.get("handelsaktionen", 0) + 1


def terraformierung():
    _zaehler["fruchtbare_kacheln"] = _zaehler.get("fruchtbare_kacheln", 0) + 1


def angriff_abgewehrt():
    """Ein feindlicher Angriff wurde abgewehrt (Zähler „Erste Abwehr“)."""
    _zaehler["abgewehrt"] = _zaehler.get("abgewehrt", 0) + 1


def _kontext(ressourcen_dict, liste_gebaeude, karten_daten,
             forschungen=0, wirtschafts_ticks=0, spielstatus="spiel",
             speicher_max=None):
    zaehler = dict(_zaehler)
    bevoelkerung = float(ressourcen_dict.get("bevoelkerung", 0))
    zaehler["max_bevoelkerung"] = max(zaehler.get("max_bevoelkerung", 0), bevoelkerung)
    zaehler["wirtschafts_ticks"] = max(zaehler.get("wirtschafts_ticks", 0), wirtschafts_ticks)
    zaehler["forschungen"] = max(zaehler.get("forschungen", 0), forschungen)
    zaehler["fruchtbare_kacheln"] = _zaehler.get("fruchtbare_kacheln", 0)
    zaehler["stahl"] = float(ressourcen_dict.get("stahl", 0))
    zaehler["gold"] = float(ressourcen_dict.get("gold", 0))
    zaehler["energie"] = float(ressourcen_dict.get("energie", 0))
    zaehler["roboter"] = float(ressourcen_dict.get("roboter", 0))
    # Fortgeschrittener Kurs (Gegner): Raumschiffe für das „Flotte“-Achievement.
    zaehler["raumschiffe"] = float(ressourcen_dict.get("raumschiffe", 0))
    zaehler["zufriedenheit"] = float(ressourcen_dict.get("zufriedenheit", 0))
    zaehler["nachhaltigkeit"] = int(ressourcen_dict.get("nahrung", 0) >= 100 and
                                      ressourcen_dict.get("energie", 0) >= 100)
    # Fortgeschrittener Kurs (Logistik): Strassen zaehlen und pruefen,
    # ob alle stehenden Gebaeude eine Anbindung haben.
    zaehler["strassen"] = sum(1 for g in liste_gebaeude
                               if g.get("typ") == 9)
    zaehler["ohne_anbindung"] = sum(1 for g in liste_gebaeude
                                    if g.get("stillstand_grund"))
    zaehler["vernetzt"] = int(len(liste_gebaeude) >= 10 and
                              zaehler["ohne_anbindung"] == 0)
    zaehler["sieg"] = int(spielstatus == "sieg")
    zaehler["erreichte"] = len(_erreicht)
    if speicher_max:
        zaehler["speicher"] = int(any(
            max_wert > 0 and ressourcen_dict.get(name, 0) >= max_wert * 0.95
            for name, max_wert in speicher_max.items()))
    else:
        zaehler["speicher"] = 0
    return zaehler


def pruefen(ressourcen_dict, liste_gebaeude, karten_daten,
            forschungen=0, wirtschafts_ticks=0, spielstatus="spiel",
            speicher_max=None):
    """Prüft alle Ziele und gibt die in diesem Aufruf neuen IDs zurück."""
    global _zaehler
    _zaehler.update(_kontext(ressourcen_dict, liste_gebaeude, karten_daten,
                             forschungen, wirtschafts_ticks, spielstatus,
                             speicher_max))
    aktuelle_typen = {f"typ_{index}": sum(
        g.get("typ") == index for g in liste_gebaeude)
        for index in (0, 6, 11, 15, 17, 19, 20)}
    for schluessel, wert in aktuelle_typen.items():
        _zaehler[schluessel] = max(_zaehler.get(schluessel, 0), wert)

    bedingungen = {
        "erste_schritte": _zaehler.get("gesamt_gebaeude", 0) >= 1,
        "grundstein": _zaehler.get("typ_0", 0) >= 1,
        "bauer": _zaehler.get("gesamt_gebaeude", 0) >= 5,
        "stadtplaner": _zaehler.get("gesamt_gebaeude", 0) >= 15,
        "bauherr": _zaehler.get("gesamt_gebaeude", 0) >= 30,
        "wohnraum": _zaehler.get("typ_6", 0) >= 3,
        "wohnblock": _zaehler.get("typ_15", 0) >= 2,
        "metropole": _zaehler.get("max_bevoelkerung", 0) >= 25,
        "megastadt": _zaehler.get("max_bevoelkerung", 0) >= 50,
        "maschinenpark": _zaehler.get("typ_11", 0) >= 1,
        "stahlzeit": _zaehler.get("stahl", 0) >= 10,
        "energiereserve": _zaehler.get("energie", 0) >= 90,
        "wohlstand": _zaehler.get("gold", 0) >= 400,
        "voll_lager": _zaehler.get("speicher", 0) >= 1,
        "wissenschaftler": _zaehler.get("forschungen", 0) >= 1,
        "forschungsprofi": _zaehler.get("forschungen", 0) >= 5,
        "genie": _zaehler.get("forschungen", 0) >= 10,
        "haendler": _zaehler.get("handelsaktionen", 0) >= 1,
        "handelsmeister": _zaehler.get("handelsaktionen", 0) >= 10,
        "terraformer": _zaehler.get("fruchtbare_kacheln", 0) >= 20,
        "ueberlebender": _zaehler.get("wirtschafts_ticks", 0) >= 30,
        "nachhaltig": _zaehler.get("nachhaltigkeit", 0) >= 1,
        "roboter_army": _zaehler.get("roboter", 0) >= 10,
        "koloniezentrum": _zaehler.get("typ_17", 0) >= 1,
        "gruene_oase": _zaehler.get("typ_19", 0) >= 1,
        "solarpionier": _zaehler.get("typ_20", 0) >= 1,
        "zufriedene_kolonie": _zaehler.get("zufriedenheit", 0) >= 30,
        "strassenbauer": _zaehler.get("strassen", 0) >= 10,
        "gut_vernetzt": _zaehler.get("vernetzt", 0) >= 1,
        # Fortgeschrittener Kurs (Gegner): Militärziele.
        "erste_abwehr": _zaehler.get("abgewehrt", 0) >= 1,
        "festung": _zaehler.get("typ_23", 0) >= 4,
        "flotte": _zaehler.get("raumschiffe", 0) >= 5,
        "zielmeister": _zaehler.get("sieg", 0) >= 1,
        "perfekte_runde": (_zaehler.get("sieg", 0) >= 1 and
                            len(_erreicht) >= 10),
    }
    neue = []
    for eintrag in ACHIEVEMENTS:
        achievement_id = eintrag["id"]
        if bedingungen.get(achievement_id, False) and achievement_id not in _erreicht:
            _erreicht.add(achievement_id)
            neue.append(achievement_id)
    if (spielstatus == "sieg" and len(_erreicht) >= 10 and
            "perfekte_runde" not in _erreicht):
        _erreicht.add("perfekte_runde")
        neue.append("perfekte_runde")
    return neue


def eintrag(achievement_id):
    return next((wert for wert in ACHIEVEMENTS if wert["id"] == achievement_id), None)


def titel(achievement_id):
    wert = eintrag(achievement_id)
    return wert["titel"] if wert else achievement_id


def punkte():
    return sum(wert["punkte"] for wert in ACHIEVEMENTS if wert["id"] in _erreicht)


def anzahl_erreicht():
    return len(_erreicht)


def _fortschritt_text(wert):
    schluessel = wert.get("fortschritt")
    aktuell = _zaehler.get(schluessel, 0)
    if schluessel in ("sieg", "nachhaltigkeit", "speicher"):
        return "erfüllt" if aktuell else "offen"
    ziel = wert.get("ziel", 1)
    if isinstance(aktuell, float) and not aktuell.is_integer():
        return f"{aktuell:.1f}/{ziel}"
    return f"{int(aktuell)}/{ziel}"


def zurueck_rect():
    return pygame.Rect(390, 660, 220, 30)


def menu_zeichnen():
    if _fenster is None:
        return
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((4, 8, 20, 242))
    _fenster.blit(overlay, (0, 0))
    gross = pygame.font.Font(None, 38)
    mittel = pygame.font.Font(None, 23)
    klein = pygame.font.Font(None, 16)
    titel_surface = gross.render("ACHIEVEMENTS", True, (255, 240, 145))
    _fenster.blit(titel_surface, (500 - titel_surface.get_width() // 2, 16))
    kopf = mittel.render(
        f"{anzahl_erreicht()}/{len(ACHIEVEMENTS)} erreicht   |   {punkte()} Punkte",
        True, (190, 225, 255))
    _fenster.blit(kopf, (500 - kopf.get_width() // 2, 52))

    # Fortgeschrittener Kurs: drei Spalten mit je 13 Eintraegen. So bleiben
    # auch die neu hinzugefuegten Achievements vollstaendig im Bild.
    for index, wert in enumerate(ACHIEVEMENTS):
        spalte = index // 13
        zeile = index % 13
        x = 18 + spalte * 326
        y = 92 + zeile * 43
        ist_erreicht = wert["id"] in _erreicht
        hintergrund = (28, 58, 52) if ist_erreicht else (25, 29, 43)
        rahmen = (110, 225, 145) if ist_erreicht else (70, 78, 100)
        pygame.draw.rect(_fenster, hintergrund, (x, y, 310, 38), border_radius=5)
        pygame.draw.rect(_fenster, rahmen, (x, y, 310, 38), width=1, border_radius=5)
        status = "✓" if ist_erreicht else "?"
        farbe = (145, 245, 165) if ist_erreicht else (150, 158, 175)
        zeile1 = f"{status} {wert['titel']}  +{wert['punkte']} P"
        zeile2 = wert["beschreibung"]
        if len(zeile2) > 42:
            zeile2 = zeile2[:39] + "..."
        _fenster.blit(klein.render(zeile1, True, farbe), (x + 9, y + 4))
        _fenster.blit(klein.render(zeile2, True, (185, 194, 210)), (x + 9, y + 21))
        if not ist_erreicht:
            fortschritt = klein.render(_fortschritt_text(wert), True, (125, 195, 220))
            _fenster.blit(fortschritt,
                           (x + 306 - fortschritt.get_width(), y + 4))

    rect = zurueck_rect()
    pygame.draw.rect(_fenster, (39, 52, 76), rect, border_radius=6)
    pygame.draw.rect(_fenster, (105, 170, 220), rect, width=1, border_radius=6)
    text = mittel.render("Zurück  [ESC / A]", True, (235, 240, 255))
    _fenster.blit(text, (rect.centerx - text.get_width() // 2,
                         rect.centery - text.get_height() // 2))
