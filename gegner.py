"""
===============================================================================
MODUL: gegner.py  —  Feindliche Angriffe und Verteidigung (Fortgeschrittener Kurs)
===============================================================================

Die Spielidee (Wunsch der Schuelerinnen und Schueler):
    Ab und zu greifen feindliche Flotten die Kolonie an. Damit das fair
    und erlernbar bleibt, laeuft jeder Angriff als Zustandsautomat ab:

        FRIEDEN ──(Zeit abgelaufen)──▶ WARNUNG ──(Countdown aus)──▶ GEFECHT
           ▲                                                               │
           └─────────────(neue Friedenszeit)◀───────────────────────────────┘

    * FRIEDENSZEIT (Start 150 Ticks, danach 100…160 Ticks):
        Nichts passiert. Der Spieler baut auf, forscht, vernetzt die Stadt.
    * WARNUNG (25 Ticks):
        Sirene + Verteidigungs-Panel zeigen Angriffsstaerke und Countdown.
        Jetzt kann man noch gegensteuern: Verteidiger ausbilden, Schiffe
        bauen, Lasertuerme mit Energie versorgen.
    * GEFECHT (ein Tick):
        Angriffsstaerke gegen Verteidigungsstaerke — hoeher oder gleich
        gewinnt der Verteidiger.

Belohnung bei Abwehr:
    Gold (40 + 20 pro Welle) und Forschung (10 pro Welle). Damit lohnt
    sich Verteidigung auch wirtschaftlich.

Pluenderung bei Niederlage:
    Der Gegner nimmt genau 30 Prozent von acht Rohstoffen mit:
    Gold, Energie, Holz, Stein, Nahrung, Kohle, Eisen, Stahl.
    NICHT angefasst werden: Bevoelkerung, Forschung, Roboter,
    Zufriedenheit, Verteidiger und Raumschiffe — Pluenderung darf nie
    selbst zum Game Over fuehren (nur das bestehende Versorgungs-Regel
    in main.py kann einen Spielstand weiter in die Niederlage treiben).

Kampfverluste (in BEIDEN Faelen, auch bei Abwehr):
    20 Prozent der Verteidiger und 20 Prozent der Raumschiffe fallen.
    Gefallene Verteidiger verringern die Bevoelkerung (sie waren ja
    vorher auch Einwohner). Verteidigung hat also immer einen Preis.

So verteidigt man sich:
    * Kaserne  (Typ 21): bildet Buerger zu Verteidigern aus (0.05/Tick).
      Hoechstens 30 Prozent der Bevoelkerung duerfen gleichzeitig
      Verteidiger sein — der Rest muss ja arbeiten (ressourcen.py).
    * Raumschiffwerft (Typ 22): baut Schiffe, je 6 Staerke.
    * Laserturm (Typ 23): feste Anlage mit 10 Staerke, NUR solange er
      arbeitet (braucht Energie und Strassenanbindung!).
    * Technologie "Schutzschilde": +25 Prozent Verteidigungsstaerke.

Regelwerk (Felder in main.REGELWERKE):
    "gegner_aktiv"  : True/False — greifen ueberhaupt Gegner an?
    "gegner_faktor" : multipliziert die Angriffsstaerke
        Standard    : aktiv, Faktor 1.0
        Entspannt   : inaktiv
        Freies Spiel: inaktiv
        Ueberleben  : aktiv, Faktor 1.3

Testbarkeit:
    Der Zufall steckt in einer eigenen random.Random-Instanz. Mit
    gegner.seed_setzen(123) ist der Ablauf exakt reproduzierbar, und
    zustand_exportieren()/zustand_importieren() erlauben Rundlaeufe
    ueber Spielstaende (auch alte ohne dieses Feld).

Nicht umgesetzt (Ideen fuer Schueler): unterschiedliche Gegnertypen,
Reparatur von Schaeden, Erfahrungspunkte fuer Verteidiger.
===============================================================================
"""

import random

import pygame

import forschung
import ressourcen
import ton


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 1: KONSTANTEN — hier kannst du alles einstellen
# ═════════════════════════════════════════════════════════════════════════════

# Start-Friedenszeit: erst einmal in Ruhe aufbauen.
FRIEDENSZEIT_TICKS = 150
# Danach greifen die Gegner in diesem Fenster (inclusive) an:
ANGRIFFS_INTERVALL = (100, 160)
# So lange toent die Sirene, bevor das Gefecht beginnt:
WARNZEIT_TICKS = 25
# Wie lange das Ergebnis-Banner mittig steht (1 Tick = ca. 1 Sekunde):
BANNER_TICKS = 6

# Angriffsstaerke = BASIS + PRO_WELLE * Welle + PRO_GEBAEUDE * Anzahl
ANGRIFFS_BASIS_STAERKE = 6.0
ANGRIFFS_STAERKE_PRO_WELLE = 4.0
ANGRIFFS_STAERKE_PRO_GEBAEUDE = 0.3

# Verteidigungsstaerke je Einheit:
STAERKE_VERTEIDIGER = 1.0     # je Verteidiger
STAERKE_RAUMSCHIFF = 6.0       # je Raumschiff
STAERKE_LASERTURM = 10.0       # je arbeitendem Laserturm
SCHILD_BONUS = 0.25            # Technologie "Schutzschilde": +25 Prozent

# Beute: dieser Anteil acht Rohstoffe geht verloren. Die restlichen
# Werte (Bevoelkerung, Forschung, Roboter, Zufriedenheit, Verteidiger,
# Raumschiffe) sind VOR Pluenderung geschuetzt.
PLUENDERUNG_ANTEIL = 0.30
PLUENDERUNG_RESSOURCEN = ("gold", "energie", "holz", "stein",
                          "nahrung", "kohle", "eisen", "stahl")

# Kampfverluste: dieser Anteil der Verteidiger und Raumschiffe faellt
# pro Gefecht (Abwehr UND Niederlage).
VERLUST_ANTEIL = 0.2

# Belohnung nach erfolgreicher Abwehr:
BELOHNUNG_GOLD_BASIS = 40
BELOHNUNG_GOLD_PRO_WELLE = 20
BELOHNUNG_FORSCHUNG_PRO_WELLE = 10

# Gebaeude-Indizes (parallel zu gebaeude.GEBAEUDE_TYPEN):
TYP_BASIS = 0
TYP_KASERNE = 21
TYP_WERFT = 22
TYP_TURM = 23

# Zustandsnamen des Automaten:
ZUSTAND_FRIEDEN = "frieden"
ZUSTAND_WARNUNG = "warnung"
ZUSTAND_GEFECHT = "gefecht"
_ZUSTAENDE = (ZUSTAND_FRIEDEN, ZUSTAND_WARNUNG, ZUSTAND_GEFECHT)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 2: MODUL-VARIABLEN (das "Gedaechtnis" des Moduls)
# ═════════════════════════════════════════════════════════════════════════════

_fenster = None
_status = ZUSTAND_FRIEDEN            # frieden | warnung | gefecht
_rest_ticks = FRIEDENSZEIT_TICKS     # Ticks bis zum naechsten Ereignis
_welle = 0                           # Anzahl bisher gestarteter Angriffe
_warnung_staerke = 0.0               # eingefrorene Angriffsstaerke der Warnung
_banner = None                       # {"erfolg": bool, "zeilen": [...], "rest": int}
_statistik = {"angriffe": 0, "abgewehrt": 0, "verloren": 0}
# Eigene Zufalls-Instanz: NIE random.* direkt benutzen, sonst ist das
# Verhalten in Tests nicht reproduzierbar.
_zufall = random.Random()


def initialisieren(fenster_obj):
    """Merkt sich das Spielfenster fuer Panel und Banner."""
    global _fenster
    _fenster = fenster_obj


def seed_setzen(seed):
    """Setzt den Startwert der eigenen Zufalls-Instanz (fuer Tests)."""
    global _zufall
    _zufall = random.Random(seed)


def zustand_zuruecksetzen():
    """Setzt den Gegner-Automaten auf frischen Spielbeginn zurueck.

    Der Zufalls-Seed bleibt erhalten: Tests rufen seed_setzen() VOR
    zustand_zuruecksetzen() auf und bekommen dann jeden Ablauf exakt
    reproduziert.
    """
    global _status, _rest_ticks, _welle, _warnung_staerke, _banner
    _status = ZUSTAND_FRIEDEN
    _rest_ticks = FRIEDENSZEIT_TICKS
    _welle = 0
    _warnung_staerke = 0.0
    _banner = None
    _statistik["angriffe"] = 0
    _statistik["abgewehrt"] = 0
    _statistik["verloren"] = 0


def zustand_exportieren():
    """Liefert den Gegner-Zustand als JSON-sicheres Dictionary."""
    return {
        "status": _status,
        "rest_ticks": _rest_ticks,
        "welle": _welle,
        "warnung_staerke": _warnung_staerke,
        "statistik": dict(_statistik),
        "banner": dict(_banner) if _banner else None,
    }


def zustand_importieren(daten):
    """Stellt den Gegner-Zustand aus einem Spielstand wieder her.

    Alte Spielstaende haben das Feld "gegner" ueberhaupt nicht — dann
    landet hier ein leeres Dictionary und alle Werte erhalten ihre
    Startwerte. Unvollstaendige oder kaputte Werte werden ebenfalls auf
    Startwerte zurueckgestuft, damit ein defekter Spielstand das Spiel
    nicht abstuerzen kann.
    """
    global _status, _rest_ticks, _welle, _warnung_staerke, _banner
    daten = daten if isinstance(daten, dict) else {}

    status = daten.get("status", ZUSTAND_FRIEDEN)
    _status = status if status in _ZUSTAENDE else ZUSTAND_FRIEDEN
    try:
        _rest_ticks = max(0, int(daten.get("rest_ticks", FRIEDENSZEIT_TICKS)))
    except (TypeError, ValueError):
        _rest_ticks = FRIEDENSZEIT_TICKS
    try:
        _welle = max(0, int(daten.get("welle", 0)))
    except (TypeError, ValueError):
        _welle = 0
    try:
        _warnung_staerke = max(0.0, float(daten.get("warnung_staerke", 0.0)))
    except (TypeError, ValueError):
        _warnung_staerke = 0.0

    roh = daten.get("statistik")
    roh = roh if isinstance(roh, dict) else {}
    for schluessel in _statistik:
        try:
            _statistik[schluessel] = max(0, int(roh.get(schluessel, 0)))
        except (TypeError, ValueError):
            _statistik[schluessel] = 0

    banner = daten.get("banner")
    if isinstance(banner, dict) and isinstance(banner.get("zeilen"), list):
        try:
            rest = max(0, int(banner.get("rest", 0)))
        except (TypeError, ValueError):
            rest = 0
        _banner = {"erfolg": bool(banner.get("erfolg")),
                   "zeilen": [str(z) for z in banner["zeilen"]],
                   "rest": rest} if rest > 0 else None
    else:
        _banner = None


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 3: REGELWERK UND STAERKEFORMELN
# ═════════════════════════════════════════════════════════════════════════════

def regelwerk_gegner_aktiv(regelwerk):
    """Sind in diesem Regelwerk feindliche Angriffe erlaubt?"""
    if not isinstance(regelwerk, dict):
        return True
    return bool(regelwerk.get("gegner_aktiv", True))


def regelwerk_gegner_faktor(regelwerk):
    """Wie stark werden Angriffe in diesem Regelwerk multipliziert?"""
    if not isinstance(regelwerk, dict):
        return 1.0
    try:
        return max(0.0, float(regelwerk.get("gegner_faktor", 1.0)))
    except (TypeError, ValueError):
        return 1.0


def angriffsstaerke(anzahl_gebaeude, welle, faktor=1.0):
    """(Basis + je Welle + je Gebäude) mal Faktor — s. Block-Kopf."""
    roh = (ANGRIFFS_BASIS_STAERKE
           + ANGRIFFS_STAERKE_PRO_WELLE * welle
           + ANGRIFFS_STAERKE_PRO_GEBAEUDE * anzahl_gebaeude)
    return round(roh * faktor, 2)


def arbeitende_lasertuerme(liste_gebaeude):
    """Anzahl Lasertuerme, die gerade WIRKEN (arbeiten und angebunden).

    Ein Turm ohne Energie oder ohne Strassenanbindung verteidigt NICHT —
    das ist der Zusammenhang zur Logistik-Erweiterung aus Phase 3.
    """
    return sum(1 for g in liste_gebaeude
               if g.get("typ") == TYP_TURM
               and not g.get("stillstand_grund")
               and g.get("arbeitet", True))


def verteidigungsstaerke(ressourcen_dict, liste_gebaeude):
    """Verteidiger + Schiffe + arbeitende Türme, plus Schutzschilde.

    Technologie "schutzschilde" bonus: +25 Prozent auf die GESAMTE
    Verteidigung (nicht nur auf einen Teil).
    """
    verteidiger = int(round(float(ressourcen_dict.get("verteidiger", 0))))
    raumschiffe = int(round(float(ressourcen_dict.get("raumschiffe", 0))))
    staerke = (verteidiger * STAERKE_VERTEIDIGER
               + raumschiffe * STAERKE_RAUMSCHIFF
               + arbeitende_lasertuerme(liste_gebaeude) * STAERKE_LASERTURM)
    if forschung.ist_technologie_erforscht("schutzschilde"):
        staerke *= (1.0 + SCHILD_BONUS)
    return round(staerke, 2)


def basis_vorhanden(liste_gebaeude):
    """Ohne Basis (Typ 0) gibt es nichts, das der Gegner angreifen kann."""
    return any(g.get("typ") == TYP_BASIS for g in liste_gebaeude)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 4: DER ZUSTANDSAUTOMAT (ein Aufruf je Wirtschaftstick)
# ═════════════════════════════════════════════════════════════════════════════

def gegner_tick(ressourcen_dict, liste_gebaeude, regelwerk=None):
    """Ein Wirtschaftstick des Gegner-Automaten.

    Rueckgabe ist None (kein Ereignis) oder ein Dictionary:

        {"ereignis": "warnung", "welle": 1, "staerke": 17.4, "warnzeit": 25}
        {"ereignis": "abwehr_erfolg", "welle": 1, "angriff": ...,
         "verteidigung": ..., "belohnung": {...}, "verluste": {...}}
        {"ereignis": "ausgeraubt", ..., "pluenderung": {...}, ...}

    main.py wertet diese Ereignisse aus (Achievements, HUD-Meldung,
    Missionen). Spiellogik passiert NUR hier — die Anzeige zeichnet
    nur, was dieser Automat als Zustand vorgibt.
    """
    global _status, _rest_ticks, _welle, _warnung_staerke, _banner

    # Das Ergebnis-Banner läuft IMMER weiter — auch wenn der Spieler
    # mitten in der Anzeige auf ein Regelwerk ohne Gegner wechselt.
    if _banner is not None:
        _banner["rest"] = max(0, int(_banner["rest"]) - 1)
        if _banner["rest"] <= 0:
            _banner = None

    if not regelwerk_gegner_aktiv(regelwerk):
        return None
    # Ohne Basis (Hauptquartier) gibt es nichts anzugreifen — der
    # Countdown friert ein, bis eine Basis existiert.
    if not basis_vorhanden(liste_gebaeude):
        return None

    if _status == ZUSTAND_FRIEDEN:
        _rest_ticks -= 1
        if _rest_ticks > 0:
            return None
        # Warnung starten: Angriffsstärke EINFRIEREN, damit die
        # Anzeige in der Warnung exakt der tatsächlichen Stärke
        # entspricht, die später aufkommt.
        _status = ZUSTAND_WARNUNG
        _rest_ticks = WARNZEIT_TICKS
        _welle += 1
        _warnung_staerke = angriffsstaerke(len(liste_gebaeude), _welle,
                                           regelwerk_gegner_faktor(regelwerk))
        ton.sound_abspielen("angriff_warnung")
        return {"ereignis": "warnung", "welle": _welle,
                "staerke": _warnung_staerke, "warnzeit": WARNZEIT_TICKS}

    if _status == ZUSTAND_WARNUNG:
        _rest_ticks -= 1
        if _rest_ticks > 0:
            return None
        return _gefecht(ressourcen_dict, liste_gebaeude)

    return None


def _gefecht(ressourcen_dict, liste_gebaeude):
    """Wertet die Warnung aus: Vergleich, Belohnung/Beute, Kampfverluste."""
    global _status, _rest_ticks, _warnung_staerke, _banner
    _status = ZUSTAND_GEFECHT
    angriff = _warnung_staerke
    verteidigung = verteidigungsstaerke(ressourcen_dict, liste_gebaeude)
    _statistik["angriffe"] += 1

    ergebnis = {"welle": _welle,
                "angriff": round(angriff, 2),
                "verteidigung": round(verteidigung, 2)}

    if verteidigung >= angriff:
        # ── Abwehr: Belohnung, kein einziger Rohstoff geht verloren ──
        _statistik["abgewehrt"] += 1
        belohnung = {
            "gold": BELOHNUNG_GOLD_BASIS + BELOHNUNG_GOLD_PRO_WELLE * _welle,
            "forschung": BELOHNUNG_FORSCHUNG_PRO_WELLE * _welle,
        }
        ressourcen_dict["gold"] = (ressourcen_dict.get("gold", 0)
                                   + belohnung["gold"])
        ressourcen_dict["forschung"] = (ressourcen_dict.get("forschung", 0)
                                        + belohnung["forschung"])
        ergebnis["ereignis"] = "abwehr_erfolg"
        ergebnis["belohnung"] = belohnung
        ton.sound_abspielen("abwehr_erfolg")
        _banner = {
            "erfolg": True,
            "zeilen": [f"ANGRIFF ABGEWEHRT — WELLE {_welle}",
                       (f"+{belohnung['gold']} Gold   "
                        f"+{belohnung['forschung']} Forschung")],
            "rest": BANNER_TICKS,
        }
    else:
        # ── Niederlage: 30 Prozent von acht Rohstoffen als Beute ──
        # Bevoelkerung, Forschung, Roboter, Zufriedenheit, Verteidiger
        # und Raumschiffe sind VOR Pluenderung geschuetzt (Aufgabe)!
        _statistik["verloren"] += 1
        pluenderung = {}
        for name in PLUENDERUNG_RESSOURCEN:
            wert = float(ressourcen_dict.get(name, 0))
            if wert <= 0:
                continue
            abzug = wert * PLUENDERUNG_ANTEIL
            ressourcen_dict[name] = wert - abzug
            pluenderung[name] = round(abzug, 2)
        ergebnis["ereignis"] = "ausgeraubt"
        ergebnis["pluenderung"] = pluenderung
        ton.sound_abspielen("ausgeraubt")
        _banner = {
            "erfolg": False,
            "zeilen": [f"KOLONIE AUSGERAUBT — WELLE {_welle}",
                       (f"Angriff {angriff:.0f} gegen "
                        f"Verteidigung {verteidigung:.0f}")],
            "rest": BANNER_TICKS,
        }

    # ── Kampfverluste in BEIDEN Faelen: 20 Prozent fallen ──
    # Auch eine Abwehr kostet Soldaten und Schiffe — Verteidigung ist
    # nie gratis (Zielkonflikt zur Wirtschaft).
    gefallene = int(round(float(ressourcen_dict.get("verteidiger", 0))
                          * VERLUST_ANTEIL))
    verlorene_schiffe = int(round(float(ressourcen_dict.get("raumschiffe", 0))
                                  * VERLUST_ANTEIL))
    ressourcen_dict["verteidiger"] = max(
        0, ressourcen_dict.get("verteidiger", 0) - gefallene)
    ressourcen_dict["raumschiffe"] = max(
        0, ressourcen_dict.get("raumschiffe", 0) - verlorene_schiffe)
    # Gefallene Verteidiger verringern die Bevoelkerung — sie waren vorher
    # auch Einwohner der Kolonie. Die Pluenderung selbst toetet niemanden.
    ressourcen_dict["bevoelkerung"] = max(
        0, ressourcen_dict.get("bevoelkerung", 0) - gefallene)
    ergebnis["verluste"] = {"verteidiger": gefallene,
                            "raumschiffe": verlorene_schiffe}

    # ── Zurueck in die Friedenszeit (Zufall aus der EIGENEN Instanz) ──
    _status = ZUSTAND_FRIEDEN
    _warnung_staerke = 0.0
    _rest_ticks = _zufall.randint(ANGRIFFS_INTERVALL[0], ANGRIFFS_INTERVALL[1])
    return ergebnis


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 5: LESEHILFEN FUER main.py UND TESTS
# ═════════════════════════════════════════════════════════════════════════════

def status():
    """Aktueller Zustand des Automaten: "frieden", "warnung" oder "gefecht"."""
    return _status


def rest_ticks():
    """Wie viele Wirtschaftsticks bis zum naechsten Ereignis fehlen."""
    return _rest_ticks


def welle():
    """Wie viele Angriffe bisher gestartet wurden."""
    return _welle


def statistik():
    """Kopie der Zaehler: Angriffe, abgewehrt, verloren."""
    return dict(_statistik)


def banner_ist_sichtbar():
    """Steht gerade ein Ergebnis-Banner auf dem Schirm?"""
    return _banner is not None


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 6: DARSTELLUNG — reine Zeichenfunktionen ohne Spiellogik
# ═════════════════════════════════════════════════════════════════════════════

# Rechte Fensterkante: Das Panel sitzt unter dem HUD (HUD-Ende y=82).
_PANEL_BREITE = 250
_PANEL_RAND = 10
_PANEL_OBERKANTE = 92


def panel_zeichnen(ressourcen_dict, liste_gebaeude, regelwerk=None):
    """Zeichnet das Verteidigungs-Panel rechts unter dem HUD.

    In den Regelwerken OHNE Gegner (Entspannt, Freies Spiel) erscheint
    ueberhaupt kein Panel — dann gibt es ja auch nichts zuverteidigen.
    Zeichnen passiert pro Frame; die Spiellogik selbst steckt
    ausschliesslich in gegner_tick().
    """
    if _fenster is None:
        return
    if not regelwerk_gegner_aktiv(regelwerk):
        return

    breite, hoehe = _fenster.get_size()
    schrift = pygame.font.Font(None, 20)
    schrift_klein = pygame.font.Font(None, 17)

    verteidiger = int(round(float(ressourcen_dict.get("verteidiger", 0))))
    kontingent = int(round(ressourcen.verteidiger_kontingent(ressourcen_dict)))
    raumschiffe = int(round(float(ressourcen_dict.get("raumschiffe", 0))))
    tuerme = arbeitende_lasertuerme(liste_gebaeude)
    staerke = verteidigungsstaerke(ressourcen_dict, liste_gebaeude)

    zeilen = [
        (f"VERTEIDIGUNG  — Welle {max(1, _welle)}", (255, 225, 130)),
        (f"Verteidiger: {verteidiger}/{kontingent}", (210, 225, 245)),
        (f"Raumschiffe: {raumschiffe}", (210, 225, 245)),
        (f"Lasertürme: {tuerme} arbeitend", (210, 225, 245)),
        (f"Stärke: {staerke:.1f}", (150, 235, 175)),
    ]
    if _status == ZUSTAND_WARNUNG:
        zeilen.append((f"⚠ ANGRIFF in {_rest_ticks} Ticks!",
                       (255, 115, 105)))
        zeilen.append((f"Gegner-Stärke: {_warnung_staerke:.1f}",
                       (255, 185, 120)))
    else:
        zeilen.append((f"Frieden: nächste Welle in {_rest_ticks}",
                       (150, 165, 190)))

    zeilen_hoehe = 19
    box_hoehe = 34 + zeilen_hoehe * len(zeilen)
    x = breite - _PANEL_BREITE - _PANEL_RAND
    y = _PANEL_OBERKANTE
    box = pygame.Rect(x, y, _PANEL_BREITE, box_hoehe)

    flaeche = pygame.Surface(box.size, pygame.SRCALPHA)
    flaeche.fill((12, 18, 40, 215))
    randfarbe = (255, 120, 110) if _status == ZUSTAND_WARNUNG else (95, 130, 190)
    pygame.draw.rect(flaeche, randfarbe, flaeche.get_rect(), width=2,
                     border_radius=7)

    for index, (text, farbe) in enumerate(zeilen):
        font = schrift if index == 0 else schrift_klein
        flaeche.blit(font.render(text, True, farbe), (10, 8 + index * zeilen_hoehe))

    _fenster.blit(flaeche, box.topleft)


def banner_zeichnen():
    """Zeichnet das 6-Sekunden-Ergebnis-Banner oben mittig.

    Erscheint NACH jedem Gefecht: gruen ("Angriff abgewehrt") oder rot
    ("Kolonie ausgeraubt"). Laufzeit: BANNER_TICKS Wirtschaftsticks.
    """
    if _fenster is None or _banner is None:
        return

    breite, hoehe = _fenster.get_size()
    flaeche = pygame.Surface((560, 84), pygame.SRCALPHA)
    flaeche.fill((10, 16, 36, 230))
    rahmen = (120, 250, 165) if _banner.get("erfolg") else (255, 120, 110)
    titelfarbe = rahmen
    pygame.draw.rect(flaeche, rahmen, flaeche.get_rect(), width=2,
                     border_radius=9)

    gross = pygame.font.Font(None, 30)
    mittel = pygame.font.Font(None, 21)
    zeilen = _banner.get("zeilen") or []
    if zeilen:
        titel = gross.render(str(zeilen[0]), True, titelfarbe)
        flaeche.blit(titel, ((560 - titel.get_width()) // 2, 14))
    if len(zeilen) > 1:
        unter = mittel.render(str(zeilen[1]), True, (225, 232, 244))
        flaeche.blit(unter, ((560 - unter.get_width()) // 2, 50))

    # Oben mittig, aber unter dem HUD — nie den Ressourcenbalken
    # verdecken. Beim naechsten Frame zeichnet das HUD wieder ueber
    # alles, was darunter liegt.
    _fenster.blit(flaeche, ((breite - 560) // 2, 100))




