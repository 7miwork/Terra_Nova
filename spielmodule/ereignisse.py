"""Zufällige Ereignisse für die Kolonie (Wünsche der Schülerinnen und Schüler).

Drei Ereignisse, die von selbst passieren können:

* **Systemausfall** — die Energieproduktion fällt 30 Prozent (3 Minuten lang).
  Wer 100 Gold zahlt, repariert sofort.
* **Unbekanntes Raumschiff** — die Kolonie kann Ressourcen einsetzen und
  würfeln: zu 50 Prozent kommt das Doppelte zurück, zu 50 Prozent ist die
  Einlage verloren. Höchstens 75 Einheiten je Ressource.
* **Meteoritenschauer** — 10 zufällige Gebäude werden getroffen und
  produzieren 3 Minuten lang nur noch 20 Prozent.

Ein Wirtschaftstick dauert eine Sekunde Spielzeit. Drei Minuten sind
deshalb 180 Ticks. Die Zeitmessung liegt bewusst im Modul: `main.py`
muss nur `ereignisse_tick()` aufrufen und die Rückgabe als Meldung zeigen.
"""

import random

import pygame

import hud
import ton
import ressourcen
import statistik

DAUER_TICKS = 180          # 3 Minuten Spielzeit
REPARATUR_KOSTEN = 100     # Gold fuer die sofortige Reparatur
MAX_EINSATZ = 75           # Deckel je Ressource beim Raumschiff
METEOR_GEBAEUDE = 10       # wie viele Gebäude der Schauer trifft
ERSTE_EREIGNIS = (90, 180)  # erst ab Tick 90 bis 180 passiert etwas
ABSTAND_EREIGNIS = (60, 150)
ANGEBOT_DAUER = 240        # so lange bleibt das Raumschiff-Angebot offen

EREIGNISSE = ("systemausfall", "meteoritenschauer", "raumschiff")

_RESSOURCEN = ("gold", "energie", "holz", "stein", "nahrung", "kohle", "eisen")
_TASTEN = {pygame.K_q: "gold", pygame.K_w: "energie", pygame.K_e: "holz",
           pygame.K_r: "stein", pygame.K_t: "nahrung", pygame.K_z: "kohle",
           pygame.K_x: "eisen"}
# Pfeiltasten und Plus/Minus aendern die Menge. Achtung: pygame nennt die
# Taste auf der Hauptzeile "K_EQUALS", nicht "K_EQUAL".
_MEHR_TASTEN = (pygame.K_UP, pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS)
_WENIGER_TASTEN = (pygame.K_DOWN, pygame.K_MINUS, pygame.K_KP_EQUALS)

_fenster = None
_tick = 0
_naechster_termin = 0
_angebot = None          # {"auswahl": {...}, "rest": int}
_auswahl = "gold"       # welche Ressource gerade veraendert wird


def ereignisse_initialisieren(fenster_obj):
    global _fenster
    _fenster = fenster_obj


def ereignisse_zuruecksetzen():
    """Setzt alle Ereignisse zurueck (neues Spiel)."""
    global _tick, _naechster_termin, _angebot, _auswahl
    _tick = 0
    _naechster_termin = random.randint(*ERSTE_EREIGNIS)
    _angebot = None
    _auswahl = "gold"
    ressourcen.energie_stoerung_setzen(0)


def zustand_exportieren():
    """Ereigniszustand fuer den Spielstand."""
    return {
        "tick": _tick,
        "naechster_termin": _naechster_termin,
        "energie_stoerung": ressourcen.energie_stoerung_rest(),
        "angebot": ({"auswahl": dict(_angebot["auswahl"]),
                     "rest": _angebot["rest"]} if _angebot else None),
    }


def zustand_importieren(daten):
    """Stellt den Ereigniszustand wieder her (alte Staende: alles ruhig)."""
    global _tick, _naechster_termin, _angebot, _auswahl
    daten = daten if isinstance(daten, dict) else {}
    try:
        _tick = max(0, int(daten.get("tick", 0)))
    except (TypeError, ValueError):
        _tick = 0
    try:
        _naechster_termin = int(daten.get("naechster_termin", 0))
    except (TypeError, ValueError):
        _naechster_termin = 0
    if _naechster_termin <= _tick:
        _naechster_termin = _tick + random.randint(*ABSTAND_EREIGNIS)
    ressourcen.energie_stoerung_setzen(daten.get("energie_stoerung", 0))
    angebot = daten.get("angebot")
    auswahl = angebot.get("auswahl") if isinstance(angebot, dict) else None
    if isinstance(auswahl, dict):
        _angebot = {"auswahl": {name: max(0, min(MAX_EINSATZ, int(auswahl.get(name, 0) or 0)))
                                for name in _RESSOURCEN},
                    "rest": max(1, int(angebot.get("rest", ANGEBOT_DAUER) or 0))}
    else:
        _angebot = None
    _auswahl = "gold"


def systemausfall_aktiv():
    """Läuft gerade ein Systemausfall?"""
    return ressourcen.energie_stoerung_aktiv()


def systemausfall_rest():
    """Wie viele Ticks der Systemausfall noch dauert."""
    return ressourcen.energie_stoerung_rest()


def systemausfall_reparieren(ressourcen_dict):
    """Bezahlt die Reparatur und behebt den Systemausfall sofort."""
    if not systemausfall_aktiv():
        hud.meldung_anzeigen("Es gibt aktuell keinen Systemausfall.")
        return False
    if ressourcen_dict.get("gold", 0) < REPARATUR_KOSTEN:
        hud.meldung_anzeigen(
            f"Die Reparatur kostet {REPARATUR_KOSTEN} Gold.")
        return False
    ressourcen_dict["gold"] -= REPARATUR_KOSTEN
    ressourcen.energie_stoerung_setzen(0)
    hud.meldung_anzeigen("Repariert! Die Energieproduktion läuft wieder normal.")
    ton.sound_abspielen("handel")
    return True


def beschaedigte_anzahl(liste_gebaeude):
    """Wie viele Gebäude sind gerade vom Meteoritenschauer getroffen?"""
    return sum(1 for gebaeude in liste_gebaeude
               if ressourcen.gebaeude_beschaedigt(gebaeude))


def _systemausfall_starten():
    ressourcen.energie_stoerung_setzen(DAUER_TICKS)
    statistik.ereignis("systemausfall")
    ton.sound_abspielen("fehler")
    return {"ereignis": "systemausfall",
            "text": f"Systemausfall! 30 Prozent weniger Energie für "
                    f"{DAUER_TICKS // 60} Minuten "
                    f"(R repariert für {REPARATUR_KOSTEN} Gold)."}


def _meteoritenschauer_starten(liste_gebaeude):
    if not liste_gebaeude:
        return None
    treffer = random.sample(liste_gebaeude,
                            min(METEOR_GEBAEUDE, len(liste_gebaeude)))
    for gebaeude in treffer:
        ressourcen.gebaeude_beschaedigen(gebaeude, DAUER_TICKS)
    statistik.ereignis("meteoritenschauer")
    ton.sound_abspielen("fehler")
    return {"ereignis": "meteoritenschauer", "anzahl": len(treffer),
            "text": f"Meteoritenschauer! {len(treffer)} Gebäude produzieren "
                    f"{DAUER_TICKS // 60} Minuten lang nur noch 20 Prozent."}


def _raumschiff_starten():
    global _angebot
    _angebot = {"auswahl": {name: 0 for name in _RESSOURCEN},
                "rest": ANGEBOT_DAUER}
    statistik.ereignis("raumschiff")
    ton.sound_abspielen("angriff_warnung")
    return {"ereignis": "raumschiff",
            "text": "Ein unbekanntes Raumschiff funkt an! Es tauscht "
                    "Ressourcen - 50 zu 50 gewinnen oder verlieren."}


def ereignisse_tick(ressourcen_dict, liste_gebaeude):
    """Läuft pro Wirtschaftstick: Effekte altern, neue Ereignisse planen.

    Die Rückgabe ist eine Meldung (Dictionary) oder None. `main.py` zeigt
    den Text im HUD an - die Logik bleibt hier im Modul.
    """
    global _tick, _naechster_termin, _angebot
    _tick += 1
    if _angebot is not None:
        _angebot["rest"] -= 1
        if _angebot["rest"] <= 0:
            _angebot = None
            return {"ereignis": "angebot_verfallen",
                    "text": "Das unbekannte Raumschiff ist wieder weitergeflogen."}
    if _tick < _naechster_termin or _angebot is not None:
        return None
    ereignis_id = random.choice(EREIGNISSE)
    # Ein laufender Systemausfall wird nicht noch einmal ausgeloest.
    if ereignis_id == "systemausfall" and systemausfall_aktiv():
        ereignis_id = "meteoritenschauer"
    _naechster_termin = _tick + random.randint(*ABSTAND_EREIGNIS)
    if ereignis_id == "systemausfall":
        return _systemausfall_starten()
    if ereignis_id == "meteoritenschauer":
        return _meteoritenschauer_starten(liste_gebaeude)
    return _raumschiff_starten()


def ereignis_ausloesen(ereignis_id, ressourcen_dict, liste_gebaeude):
    """Loest ein Ereignis direkt aus - fuer Tests und spaetere Bonusereignisse."""
    if ereignis_id == "systemausfall":
        return _systemausfall_starten()
    if ereignis_id == "meteoritenschauer":
        return _meteoritenschauer_starten(liste_gebaeude)
    if ereignis_id == "raumschiff":
        return _raumschiff_starten()
    return None


def angebot_ist_offen():
    """Ist gerade das Raumschiff-Angebot offen? (Dann läuft das Spiel nicht)"""
    return _angebot is not None


def angebot_uebersicht():
    """Die Liste (Ressourcenname, eingesetzte Menge) für die Anzeige."""
    if _angebot is None:
        return []
    return [(name, _angebot["auswahl"][name]) for name in _RESSOURCEN]


def angebot_summe():
    """Wie viele Einheiten werden insgesamt eingesetzt?"""
    if _angebot is None:
        return 0
    return sum(_angebot["auswahl"].values())


def _setze_auswahl(delta):
    aktuell = _angebot["auswahl"][_auswahl]
    _angebot["auswahl"][_auswahl] = max(0, min(MAX_EINSATZ, aktuell + delta))


def angebot_ablehnen():
    global _angebot
    if _angebot is None:
        return False
    _angebot = None
    hud.meldung_anzeigen("Das Raumschiff-Angebot wurde abgelehnt.")
    return True


def angebot_abschicken(ressourcen_dict):
    """Setzt die gewaehlten Ressourcen ein: 50 zu 50 das Doppelte oder nichts."""
    global _angebot
    if _angebot is None:
        return False
    einsatz = {name: menge for name, menge in _angebot["auswahl"].items() if menge > 0}
    if not einsatz:
        hud.meldung_anzeigen("Wähle zuerst Ressourcen aus (Q bis X, dann Pfeil hoch/runter).")
        return False
    for name, menge in einsatz.items():
        if ressourcen_dict.get(name, 0) < menge:
            hud.meldung_anzeigen(
                f"Zu wenig {ressourcen.RESSOURCEN_NAMEN.get(name, name)} im Lager.")
            return False
    for name, menge in einsatz.items():
        ressourcen_dict[name] -= menge
    if random.random() < 0.5:
        gewonnen = []
        for name, menge in einsatz.items():
            vorher = ressourcen_dict.get(name, 0)
            ziel = min(vorher + menge * 2, ressourcen.maximaler_speicher(name))
            ressourcen_dict[name] = ziel
            gewonnen.append(f"{ziel - vorher:.0f} "
                            f"{ressourcen.RESSOURCEN_NAMEN.get(name, name)}")
        ton.sound_abspielen("achievement")
        hud.meldung_anzeigen("Das Raumschiff zahlt doppelt: " + ", ".join(gewonnen))
    else:
        ton.sound_abspielen("fehler")
        hud.meldung_anzeigen("Das Raumschiff ist weitergeflogen. Die Einlage ist weg.")
    _angebot = None
    return True


def taste(key, ressourcen_dict):
    """Verarbeitet eine Taste. True heißt: das Modul hat sie benutzt."""
    global _auswahl
    if _angebot is not None:
        if key in _TASTEN:
            _auswahl = _TASTEN[key]
            return True
        if key in _MEHR_TASTEN:
            _setze_auswahl(5)
            return True
        if key in _WENIGER_TASTEN:
            _setze_auswahl(-5)
            return True
        if key in (pygame.K_RETURN, pygame.K_SPACE):
            return angebot_abschicken(ressourcen_dict)
        if key == pygame.K_ESCAPE:
            return angebot_ablehnen()
        return False
    if key == pygame.K_r:
        return systemausfall_reparieren(ressourcen_dict)
    return False


def _naechste_auswahl_tasten():
    """Reihenfolge der Auswahltasten für die Anzeige."""
    return sorted(_TASTEN.items(), key=lambda paar: paar[1])


def menu_zeichnen(ressourcen_dict):
    """Zeichnet das Raumschiff-Fenster, solange ein Angebot offen ist."""
    if _fenster is None or _angebot is None:
        return
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((6, 8, 16, 228))
    _fenster.blit(overlay, (0, 0))
    gross = pygame.font.Font(None, 34)
    mittel = pygame.font.Font(None, 24)
    klein = pygame.font.Font(None, 19)

    titel = gross.render("UNBEKANNTES RAUMSCHIFF", True, (255, 220, 120))
    _fenster.blit(titel, (30, 22))
    text = klein.render("Setze Ressourcen ein: zu 50 Prozent kommt das Doppelte "
                        "zurueck, zu 50 Prozent ist die Einlage weg.",
                        True, (200, 210, 225))
    _fenster.blit(text, (30, 62))

    y = 110
    tasten = {name: pygame.key.name(taste)[-1]
              for taste, name in _naechste_auswahl_tasten()}
    for name, menge in angebot_uebersicht():
        markiert = name == _auswahl
        hintergrund = (48, 44, 22) if markiert else (22, 26, 40)
        pygame.draw.rect(_fenster, hintergrund, (28, y - 4, 470, 30), border_radius=5)
        if markiert:
            pygame.draw.rect(_fenster, (220, 190, 90), (28, y - 4, 470, 30),
                             width=1, border_radius=5)
        beschriftung = f"[{tasten.get(name, ' ')}] {ressourcen.RESSOURCEN_NAMEN.get(name, name)}"
        farbe = (255, 235, 170) if markiert else (205, 212, 225)
        _fenster.blit(mittel.render(f"{beschriftung:<22}", True, farbe), (40, y))
        _fenster.blit(mittel.render(f"{menge:>4} / {MAX_EINSATZ}", True, farbe),
                      (300, y))
        y += 34

    y += 8
    summe = angebot_summe()
    _fenster.blit(klein.render(f"Einsatz gesamt: {summe} Einheiten", True, (255, 220, 140)), (30, y))
    _fenster.blit(klein.render(
        f"Q W E R T Z X waehlen | Pfeil hoch/runter = 5 mehr/weniger | "
        f"Enter senden | Esc ablehnen", True, (170, 210, 230)), (30, y + 26))
    _fenster.blit(klein.render(f"Das Angebot bleibt {_angebot['rest']} Ticks offen.",
                               True, (150, 160, 180)), (30, y + 52))
