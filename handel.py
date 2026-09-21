"""Marktplatz-Handel und NPC-Angebote für Stunde 11."""

import pygame
import forschung
import hud
import ton


_ROHSTOFFE = ["gold", "energie", "holz", "stein", "nahrung", "kohle", "eisen"]
_ROHSTOFF_NAMEN = {"gold": "Gold", "energie": "Energie", "holz": "Holz", "stein": "Stein",
                  "nahrung": "Nahrung", "kohle": "Kohle", "eisen": "Eisen"}
_ANGEBOTE = [
    {"geben": {"holz": 20}, "nehmen": {"stein": 10}, "text": "Holz gegen Stein"},
    {"geben": {"nahrung": 25}, "nehmen": {"energie": 12}, "text": "Nahrung gegen Energie"},
    {"geben": {"eisen": 8}, "nehmen": {"gold": 20}, "text": "Eisen gegen Gold"},
    {"geben": {"kohle": 15}, "nehmen": {"holz": 20}, "text": "Kohle gegen Holz"},
]

_fenster = None
_menu_offen = False
_tick = 0
_angebot = None
_marktplatz_aktiv = False
_handelsaktionen = 0


def handel_initialisieren(fenster_obj):
    global _fenster
    _fenster = fenster_obj


def handel_zuruecksetzen():
    global _menu_offen, _tick, _angebot, _marktplatz_aktiv, _handelsaktionen
    _menu_offen = False
    _tick = 0
    _angebot = None
    _marktplatz_aktiv = False
    _handelsaktionen = 0


def zustand_exportieren():
    """Gibt den dauerhaften Handelszustand für einen Spielstand zurück."""
    return {
        "tick": _tick,
        "angebot": dict(_angebot) if _angebot else None,
        "marktplatz_aktiv": _marktplatz_aktiv,
        "handelsaktionen": _handelsaktionen,
    }


def zustand_importieren(daten):
    """Stellt Handels-Tick und ein gültiges offenes Angebot wieder her."""
    global _menu_offen, _tick, _angebot, _marktplatz_aktiv, _handelsaktionen
    daten = daten if isinstance(daten, dict) else {}
    try:
        _tick = max(0, int(daten.get("tick", 0)))
    except (TypeError, ValueError):
        _tick = 0
    angebot = daten.get("angebot")
    if (isinstance(angebot, dict) and
            isinstance(angebot.get("geben"), dict) and
            isinstance(angebot.get("nehmen"), dict) and
            isinstance(angebot.get("text"), str)):
        _angebot = {"geben": dict(angebot["geben"]),
                    "nehmen": dict(angebot["nehmen"]),
                    "text": angebot["text"]}
    else:
        _angebot = None
    _marktplatz_aktiv = bool(daten.get("marktplatz_aktiv", False))
    try:
        _handelsaktionen = max(0, int(daten.get("handelsaktionen", 0)))
    except (TypeError, ValueError):
        _handelsaktionen = 0
    _menu_offen = False


def handelsmenue_umschalten():
    global _menu_offen
    _menu_offen = not _menu_offen


def handelsmenue_ist_offen():
    return _menu_offen


def _hat_marktplatz(liste_gebaeude):
    """Marktplatz oder Handelsposten können Handelsfunktionen bedienen."""
    return any(g["typ"] in (5, 16) for g in liste_gebaeude)


def handel_tick(ressourcen_dict, liste_gebaeude):
    global _tick, _angebot, _marktplatz_aktiv
    _tick += 1
    _marktplatz_aktiv = _hat_marktplatz(liste_gebaeude)
    intervall = 12 if forschung.ist_technologie_erforscht("handelsrouten") else 20
    if (forschung.ist_technologie_erforscht("handel_mit_kolonien") and
            _hat_marktplatz(liste_gebaeude) and _angebot is None and _tick % intervall == 0):
        _angebot = dict(_ANGEBOTE[(_tick // 20) % len(_ANGEBOTE)])
        hud.meldung_anzeigen("Eine andere Kolonie hat ein Handelsangebot geschickt.")


def aktuelles_angebot():
    return _angebot


def angebot_annahmen(ressourcen_dict):
    global _angebot
    if _angebot is None:
        hud.meldung_anzeigen("Es gibt aktuell kein Handelsangebot.")
        return False
    for name, menge in _angebot["geben"].items():
        if ressourcen_dict.get(name, 0) < menge:
            hud.meldung_anzeigen("Für dieses Angebot fehlen Ressourcen.")
            return False
    for name, menge in _angebot["geben"].items():
        ressourcen_dict[name] -= menge
    for name, menge in _angebot["nehmen"].items():
        ressourcen_dict[name] = ressourcen_dict.get(name, 0) + menge
    text = _angebot["text"]
    _angebot = None
    handel_aktion()
    hud.meldung_anzeigen("Handel angenommen: " + text)
    ton.sound_abspielen("handel")
    return True


def handel_aktionszahl():
    return _handelsaktionen


def handel_aktion():
    global _handelsaktionen
    _handelsaktionen += 1


def angebot_ablehnen():
    global _angebot
    if _angebot is not None:
        _angebot = None
        hud.meldung_anzeigen("Handelsangebot abgelehnt.")
        return True
    return False


def ressourcen_tauschen(ressourcen_dict, von, zu):
    if not _marktplatz_aktiv:
        hud.meldung_anzeigen("Für Handel wird ein Marktplatz oder Handelsposten benötigt.")
        return False
    if not forschung.ist_technologie_erforscht("ressourcenhandel"):
        hud.meldung_anzeigen("Ressourcenhandel ist noch nicht erforscht.")
        return False
    if von == zu or ressourcen_dict.get(von, 0) < 2:
        hud.meldung_anzeigen("Für einen Tausch werden 2 Einheiten der Ausgangsressource benötigt.")
        return False
    ressourcen_dict[von] -= 2
    ressourcen_dict[zu] = ressourcen_dict.get(zu, 0) + 1
    handel_aktion()
    hud.meldung_anzeigen(f"Tausch durchgeführt: 2 {_ROHSTOFF_NAMEN[von]} gegen 1 {_ROHSTOFF_NAMEN[zu]}.")
    ton.sound_abspielen("handel")
    return True


def handelsmenue_taste(key, ressourcen_dict):
    if not _menu_offen:
        return False
    if key == pygame.K_j:
        return angebot_annahmen(ressourcen_dict)
    if key == pygame.K_k:
        return angebot_ablehnen()
    paare = {
        pygame.K_q: ("holz", "stein"), pygame.K_w: ("stein", "holz"),
        pygame.K_r: ("nahrung", "energie"), pygame.K_t: ("energie", "nahrung"),
        pygame.K_y: ("kohle", "eisen"), pygame.K_u: ("eisen", "gold"),
    }
    if key in paare:
        return ressourcen_tauschen(ressourcen_dict, *paare[key])
    return False


def _format_dict(d):
    return ", ".join(f"{m} {_ROHSTOFF_NAMEN.get(n, n)}" for n, m in d.items())


def handelsmenue_zeichnen(ressourcen_dict):
    if _fenster is None or not _menu_offen:
        return
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((8, 18, 22, 220))
    _fenster.blit(overlay, (0, 0))
    gross = pygame.font.Font(None, 34)
    klein = pygame.font.Font(None, 22)
    _fenster.blit(gross.render("HANDEL  (E schließt)", True, (255, 255, 255)), (30, 24))
    _fenster.blit(klein.render("Kurs: 2 Einheiten gegen 1 Einheit | Marktplatz oder Handelsposten nötig", True, (160, 220, 220)), (30, 65))
    zeilen = [
        "Q: 2 Holz → 1 Stein       W: 2 Stein → 1 Holz",
        "R: 2 Nahrung → 1 Energie  T: 2 Energie → 1 Nahrung",
        "Y: 2 Kohle → 1 Eisen       U: 2 Eisen → 1 Gold",
        "",
    ]
    y = 105
    for zeile in zeilen:
        _fenster.blit(klein.render(zeile, True, (225, 230, 235)), (45, y))
        y += 30
    _fenster.blit(klein.render("NPC-Angebote", True, (255, 220, 100)), (45, y + 5))
    y += 38
    if _angebot is None:
        _fenster.blit(klein.render("Kein Angebot aktiv. Neue Angebote kommen regelmäßig.", True, (170, 180, 190)), (45, y))
    else:
        _fenster.blit(klein.render(f"Angebot: Du gibst {_format_dict(_angebot['geben'])}", True, (255, 180, 150)), (45, y))
        _fenster.blit(klein.render(f"und erhältst {_format_dict(_angebot['nehmen'])}", True, (150, 240, 160)), (45, y + 30))
        _fenster.blit(klein.render("J: annehmen    K: ablehnen", True, (255, 255, 255)), (45, y + 65))
