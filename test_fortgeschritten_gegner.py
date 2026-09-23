"""Selbsttest fuer Gegner und Verteidigung (Fortgeschrittener Kurs).

Alle Ablaeufe laufen mit festem Seed deterministisch:

    1.  Timeline: 150 Ticks Frieden, 25 Ticks Warnung, dann Gefecht.
    2.  Staerkeformeln fuer Angriff und Verteidigung inkl. Schutzschilde.
    3.  Abwehr: Belohnung 40+20*Welle Gold und 10*Welle Forschung.
    4.  Niederlage: genau 30% der acht Rohstoffe, sechs Werte geschuetzt.
    5.  Kampfverluste: 20% der Verteidiger/Schiffe, Bevoelkerung sinkt.
    6.  Regelwerk: inaktiv zaehlt nichts mit, Faktor 1.3 bei Ueberleben.
    7.  Kein Angriff ohne Basis (Typ 0).
    8.  Seed-Determinismus und Spielstand-Rundlauf (auch ohne Feld).
    9.  Banner exakt 6 Ticks, Panel und Vollbild zeichnen ohne Fehler.
    10. Achievements "Erste Abwehr/Festung/Flotte", Mission "Kaserne bauen".
    11. Kaserne stoppt beim Verteidiger-Kontingent (ressourcen.py).
"""
import json
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(__file__))

import pygame
pygame.init()
import main
import gegner
import forschung
import ressourcen
import achievements
import missionen

# Gleiches Bootstrap wie in den anderen Tests: Menues und Fenster.
main.spiel_menue.menue_initialisieren(main.fenster)
main.menu.menu_initialisieren(main.fenster)
main.hud.hud_initialisieren(main.fenster)
main.achievements.initialisieren(main.fenster)
main.missionen.initialisieren(main.fenster)
main.logistik.initialisieren(main.fenster)
gegner.initialisieren(main.fenster)
main.neues_spiel_starten()

# Registrierungen: Alles muss in den Listen stehen.
_ACH_IDS = {eintrag["id"] for eintrag in achievements.ACHIEVEMENTS}
assert {"erste_abwehr", "festung", "flotte"} <= _ACH_IDS
assert any(m["id"] == "kaserne_bauen" for m in missionen.MISSIONEN)

# Regelwerk-Felder: aktiv/inaktiv und der Faktor 1.3 beim Ueberleben.
assert main.REGELWERKE["standard"].get("gegner_aktiv") is True
assert main.REGELWERKE["standard"].get("gegner_faktor") == 1.0
assert main.REGELWERKE["entspannt"].get("gegner_aktiv") is False
assert main.REGELWERKE["freies_spiel"].get("gegner_aktiv") is False
assert main.REGELWERKE["ueberleben"].get("gegner_aktiv") is True
assert main.REGELWERKE["ueberleben"].get("gegner_faktor") == 1.3

STANDARD = {"gegner_aktiv": True, "gegner_faktor": 1.0}
PLUENDERUNG = ("gold", "energie", "holz", "stein",
               "nahrung", "kohle", "eisen", "stahl")


def neue_welt():
    """Frische Ressourcen mit allen (auch neuen) Schluesseln."""
    return {"gold": 100.0, "energie": 50.0, "holz": 30.0, "stein": 20.0,
            "bevoelkerung": 10.0, "nahrung": 50.0, "forschung": 0.0,
            "kohle": 10.0, "eisen": 10.0, "roboter": 0.0, "stahl": 5.0,
            "zufriedenheit": 5.0, "verteidiger": 0.0, "raumschiffe": 0.0}


def starten(seed=7):
    """Zustand und Technologien fuer jeden Testfall frisch aufsetzen."""
    gegner.seed_setzen(seed)
    gegner.zustand_zuruecksetzen()
    forschung.zustand_importieren({})


def bis_warnung(ressourcen_dict, gebaeude, regel=STANDARD):
    """Tickt bis zum Warnungsereignis (Tag 150) und gibt es zurueck."""
    for _ in range(gegner.FRIEDENSZEIT_TICKS - 1):
        assert gegner.gegner_tick(ressourcen_dict, gebaeude, regel) is None
    ereignis = gegner.gegner_tick(ressourcen_dict, gebaeude, regel)
    assert ereignis is not None and ereignis["ereignis"] == "warnung"
    return ereignis


def bis_gefecht(ressourcen_dict, gebaeude, regel=STANDARD):
    """Tickt durch Warnung bis zum Gefechtsergebnis."""
    bis_warnung(ressourcen_dict, gebaeude, regel)
    for _ in range(gegner.WARNZEIT_TICKS - 1):
        assert gegner.gegner_tick(ressourcen_dict, gebaeude, regel) is None
    ergebnis = gegner.gegner_tick(ressourcen_dict, gebaeude, regel)
    assert ergebnis is not None
    assert ergebnis["ereignis"] in ("abwehr_erfolg", "ausgeraubt")
    return ergebnis


BASIS = {"typ": 0, "kachel_x": 1, "kachel_y": 1}


# ── Test 1: Timeline (150 Frieden, 25 Warnung, dann Pluenderung) ─────────────
starten(7)
r = neue_welt()
geb = [BASIS]
for _ in range(149):
    assert gegner.gegner_tick(r, geb, STANDARD) is None
assert gegner.status() == "frieden"

warnung = gegner.gegner_tick(r, geb, STANDARD)   # 150. Tick
assert warnung["ereignis"] == "warnung"
assert warnung["welle"] == 1
assert warnung["warnzeit"] == gegner.WARNZEIT_TICKS == 25
assert warnung["staerke"] == 10.3                # 6 + 4*1 + 0.3*1 Gebaeude
assert gegner.status() == "warnung"
assert gegner.rest_ticks() == 25

for _ in range(24):
    assert gegner.gegner_tick(r, geb, STANDARD) is None
kampf = gegner.gegner_tick(r, geb, STANDARD)     # 25. Warn-Tick
assert kampf["ereignis"] == "ausgeraubt"          # keine Verteidigung
assert gegner.status() == "frieden"
assert gegner.banner_ist_sichtbar()
assert gegner.statistik() == {"angriffe": 1, "abgewehrt": 0, "verloren": 1}
assert 100 <= gegner.rest_ticks() <= 160
# 30 Prozent Beute, aber Bevoelkerung bleibt ueber Pluenderung unangetastet.
assert abs(r["gold"] - 70.0) < 1e-6
assert r["bevoelkerung"] == 10.0
assert r["forschung"] == 0.0

# ── Test 2: Stärkeformeln ───────────────────────────────────────────────────
assert gegner.angriffsstaerke(0, 1) == 10.0
assert gegner.angriffsstaerke(10, 3) == 21.0       # 6+12+3
assert gegner.angriffsstaerke(5, 2, 1.3) == 20.15  # 15.5 * 1.3
assert gegner.angriffsstaerke(0, 1, 1.3) == 13.0
assert gegner.regelwerk_gegner_faktor(None) == 1.0
assert gegner.regelwerk_gegner_aktiv(None) is True
assert gegner.regelwerk_gegner_aktiv({"gegner_aktiv": False}) is False

# ── Test 3: Verteidigungsstärke inkl. Schutzschilde ────────────────────────
starten(7)
r = neue_welt()
r["verteidiger"] = 10.0
r["raumschiffe"] = 3.0
turm = {"typ": 23, "kachel_x": 4, "kachel_y": 4, "arbeitet": True}
g = [BASIS, turm]
assert gegner.verteidigungsstaerke(r, g) == 38.0   # 10 + 3*6 + 10
# Turm ohne Betrieb oder ohne Strassenanbindung verteidigt nicht.
turm["arbeitet"] = False
assert gegner.verteidigungsstaerke(r, g) == 28.0
turm["arbeitet"] = True
turm["stillstand_grund"] = "Strasse fehlt"
assert gegner.verteidigungsstaerke(r, g) == 28.0
del turm["stillstand_grund"]
# Technologie "schutzschilde": +25 Prozent auf die gesamte Stärke.
forschung.zustand_importieren({"erforschte_technologien": ["schutzschilde"]})
assert gegner.verteidigungsstaerke(r, g) == 47.5
forschung.zustand_importieren({})

# ── Test 4: Abwehr bringt Belohnung, keine Beute, aber Kampfverluste ────────
starten(7)
r = neue_welt()
r["verteidiger"] = 20.0                            # 20 > 10.3 Angriff
geb = [BASIS]
sieg = bis_gefecht(r, geb)
assert sieg["ereignis"] == "abwehr_erfolg"
assert sieg["belohnung"] == {"gold": 60, "forschung": 10}   # Welle 1
assert sieg["verluste"] == {"verteidiger": 4, "raumschiffe": 0}
assert abs(r["gold"] - 160.0) < 1e-6               # 100 + 60, keine Beute
assert r["forschung"] == 10.0
assert r["nahrung"] == 50.0                        # geschuetzt
assert r["verteidiger"] == 16.0                    # 20 - 4 Gefallene
assert r["bevoelkerung"] == 6.0                    # 10 - 4 Gefallene
assert gegner.statistik()["abgewehrt"] == 1
assert gegner.banner_ist_sichtbar()

# ── Test 5: Niederlage plündert nur die acht Rohstoffe ──────────────────────
starten(7)
r = neue_welt()
geb = [BASIS]
geschuetzt_vorher = {name: r[name] for name in
                     ("bevoelkerung", "forschung", "roboter",
                      "zufriedenheit", "verteidiger", "raumschiffe")}
rohstoffe_vorher = {name: r[name] for name in PLUENDERUNG}
kampf = bis_gefecht(r, geb)
assert kampf["ereignis"] == "ausgeraubt"
for name in PLUENDERUNG:
    soll = rohstoffe_vorher[name] * (1 - gegner.PLUENDERUNG_ANTEIL)
    assert abs(r[name] - soll) < 1e-6, f"{name}: {r[name]} != {soll}"
    assert abs(kampf["pluenderung"][name]
               - rohstoffe_vorher[name] * gegner.PLUENDERUNG_ANTEIL) < 1e-6
for name, wert in geschuetzt_vorher.items():
    assert r[name] == wert, f"{name} darf nicht gepluendert werden"

# ── Test 6: Mit Verteidigern kostet die Niederlage 20 Prozent ──────────────
starten(7)
r = neue_welt()
r["verteidiger"] = 10.0
geb = [BASIS, {"typ": 9}, {"typ": 9}, {"typ": 9}]   # 4 Gebaeude → Angriff 11.2
kampf = bis_gefecht(r, geb)
assert kampf["ereignis"] == "ausgeraubt"
assert kampf["angriff"] == 11.2
assert kampf["verteidigung"] == 10.0
assert kampf["verluste"] == {"verteidiger": 2, "raumschiffe": 0}
assert r["verteidiger"] == 8.0
assert r["bevoelkerung"] == 8.0                      # Gefallene fehlen

# ── Test 7: Regelwerk ohne Gegner friert den Countdown ein ─────────────────
starten(7)
r = neue_welt()
geb = [BASIS]
for _ in range(500):
    assert gegner.gegner_tick(r, geb, {"gegner_aktiv": False}) is None
assert gegner.status() == "frieden"
assert gegner.rest_ticks() == gegner.FRIEDENSZEIT_TICKS == 150
# Auch "freies_spiel" und "entspannt" laufen ueber dieselben Felder.
for regel in ("entspannt", "freies_spiel"):
    assert gegner.regelwerk_gegner_aktiv(main.REGELWERKE[regel]) is False

# Faktor 1.3 aus dem Ueberleben-Regelwerk wirkt auf die eingefrorene Stärke.
starten(7)
r = neue_welt()
regel = main.REGELWERKE["ueberleben"]
warnung = bis_warnung(r, [BASIS], regel)
assert warnung["staerke"] == 13.39                  # 10.3 * 1.3

# ── Test 8: Ohne Basis wird nie angegriffen ────────────────────────────────
starten(7)
r = neue_welt()
for _ in range(400):
    assert gegner.gegner_tick(r, [], STANDARD) is None
assert gegner.status() == "frieden"
assert gegner.rest_ticks() == gegner.FRIEDENSZEIT_TICKS

# ── Test 9: Gleicher Seed = gleicher Ablauf ────────────────────────────────
def ablauf(seed):
    starten(seed)
    rr = neue_welt()
    gg = [BASIS]
    pfade = []
    for _ in range(500):
        ev = gegner.gegner_tick(rr, gg, STANDARD)
        if ev and ev["ereignis"] in ("abwehr_erfolg", "ausgeraubt"):
            pfade.append((ev["welle"], gegner.rest_ticks(), ev["ereignis"]))
    return pfade, gegner.statistik()

lauf_a = ablauf(7)
lauf_b = ablauf(7)
assert lauf_a == lauf_b, "gleicher Seed muss identisch ablaufen"
assert lauf_a[0], "in 500 Ticks muss mindestens ein Gefecht liegen"
for _welle, rest, _art in lauf_a[0]:
    assert 100 <= rest <= 160

# ── Test 10: Zustand exportieren/importieren (inkl. alter Spielstaende) ────
starten(7)
r = neue_welt()
geb = [BASIS]
bis_warnung(r, geb)
daten = gegner.zustand_exportieren()
json.dumps(daten, ensure_ascii=False)                # muss JSON-faehig sein
gegner.zustand_zuruecksetzen()
assert gegner.status() == "frieden" and gegner.welle() == 0
gegner.zustand_importieren(daten)
assert gegner.status() == "warnung"
assert gegner.welle() == 1 and gegner.rest_ticks() == 25
# Alter Spielstand ohne das Feld "gegner" (leeres Dictionary) und
# kaputte Werte duerfen nie abstuerzen.
gegner.zustand_importieren({})
assert gegner.status() == "frieden"
assert gegner.rest_ticks() == gegner.FRIEDENSZEIT_TICKS
assert gegner.statistik() == {"angriffe": 0, "abgewehrt": 0, "verloren": 0}
gegner.zustand_importieren({"status": "Quatsch", "rest_ticks": "x",
                            "welle": -3, "statistik": 7,
                            "banner": {"zeilen": "nein"}})
assert gegner.status() == "frieden"
assert gegner.welle() == 0
assert gegner.rest_ticks() == gegner.FRIEDENSZEIT_TICKS
assert gegner.banner_ist_sichtbar() is False

# ── Test 11: Banner exakt 6 Ticks, Panel und Vollbild zeichnen ─────────────
starten(7)
r = neue_welt()
geb = [BASIS]
bis_gefecht(r, geb)
assert gegner.banner_ist_sichtbar()
INAKTIV = {"gegner_aktiv": False}
for _ in range(gegner.BANNER_TICKS - 1):             # 5 Ticks: sichtbar
    gegner.gegner_tick(r, geb, INAKTIV)
    assert gegner.banner_ist_sichtbar()
gegner.gegner_tick(r, geb, INAKTIV)                  # 6. Tick: Ende
assert gegner.banner_ist_sichtbar() is False

gegner.initialisieren(main.fenster)
gegner.panel_zeichnen(r, geb, main.REGELWERKE["standard"])
gegner.banner_zeichnen()
# Ohne Gegner kein Panel — das darf aber nicht abstuerzen.
gegner.panel_zeichnen(r, geb, main.REGELWERKE["entspannt"])
main.liste_gebaeude = list(geb)
main.ressourcen_dict.update(r)
main.spiel_status = "spiel"
main.spielwelt_zeichnen()                            # Integration ins HUD
pygame.display.flip()

# ── Test 12: Achievements Erste Abwehr / Festung / Flotte ──────────────────
achievements.zustand_zuruecksetzen()
achievements.angriff_abgewehrt()
for _ in range(4):
    achievements.gebaeude_gebaut(23)
r = neue_welt()
r["raumschiffe"] = 5.0
g_tuerme = [BASIS] + [{"typ": 23, "arbeitet": True}] * 4
speicher = {name: ressourcen.maximaler_speicher(name)
            for name in ressourcen.SPEICHER_BASIS}
neue_ach = achievements.pruefen(r, g_tuerme, main.karten_daten,
                                0, 0, "spiel", speicher)
assert "erste_abwehr" in neue_ach
assert "festung" in neue_ach
assert "flotte" in neue_ach

# ── Test 13: Mission "Kaserne bauen" ──────────────────────────────────────
missionen.zustand_zuruecksetzen()
main.liste_gebaeude = [BASIS, {"typ": 21, "kachel_x": 3, "kachel_y": 3}]
neue_missionen = missionen.pruefen(main.missionen_kontext())
assert "kaserne_bauen" in neue_missionen

# ── Test 14: Kaserne stoppt beim Verteidiger-Kontingent ────────────────────
starten(7)
r = neue_welt()
kaserne = {"typ": 21, "kachel_x": 3, "kachel_y": 3}
kontingent = ressourcen.verteidiger_kontingent(r)
assert kontingent == 3.0                             # 30 Prozent von 10
r["verteidiger"] = kontingent
ressourcen.ressourcen_produzieren(r, [kaserne])
assert r["verteidiger"] == kontingent                # keine Produktion mehr
assert kaserne["arbeitet"] is True                   # verbraucht aber weiter
r["verteidiger"] = 0.0
ressourcen.ressourcen_produzieren(r, [kaserne])
assert abs(r["verteidiger"] - 0.5) < 1e-9            # wieder am Ausbilden

print("Alle Gegner-Tests bestanden.")

