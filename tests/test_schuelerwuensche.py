"""Tests fuer Balancing, Zufallsereignisse, Statistik und Langzeit-Achievements."""

import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
pygame.init()
pygame.display.set_mode((1000, 720))

import achievements
import ereignisse
import forschung
import handel
import hud
import main
import ressourcen
import statistik

# Statistik nie in die echte Datei schreiben.
statistik.DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "test_statistik.json")


# ── 1. Balancing: die drei Produktionswerte ───────────────────────────────
assert ressourcen.GEBAEUDE_WIRTSCHAFT[10]["produktion"]["energie"] == 20
assert ressourcen.GEBAEUDE_WIRTSCHAFT[13]["produktion"]["nahrung"] == 6
assert ressourcen.GEBAEUDE_WIRTSCHAFT[5]["produktion"]["gold"] == 10
print("Balancing: Fusionsreaktor 20, Gewächshaus 6, Marktplatz 10")


# ── 2. Balancing: Handel zahlt 3:1 ────────────────────────────────────────
assert handel.TAUSCH_VERHALTNIS == 3
werte = {"gold": 500, "energie": 500, "holz": 30, "stein": 30,
         "nahrung": 100, "kohle": 30, "eisen": 30}
forschung._erforschte_technologien.add("ressourcenhandel")
handel.handel_tick(werte, [{"typ": 5}])
assert handel.ressourcen_tauschen(werte, "holz", "stein")
assert werte["holz"] == 27 and werte["stein"] == 31
# Bei genau 3 Einheiten darf getauscht werden, bei 2 nicht.
werte["holz"] = 2
assert not handel.ressourcen_tauschen(werte, "holz", "stein")
werte["holz"] = 3
assert handel.ressourcen_tauschen(werte, "holz", "stein")
print("Handel: 3 Einheiten gegen 1, Deckel und Mindestmenge stimmen")


# ── 3. Systemausfall: -30 % Energie, 3 Minuten, Reparatur für 100 Gold ───
gebaeude = [{"typ": 1, "arbeitet": True}]          # Reaktor: 5 Energie
energie_normal = {"gold": 400, "energie": 0, "holz": 40, "stein": 40,
                  "bevoelkerung": 20, "nahrung": 100, "kohle": 40,
                  "eisen": 0, "roboter": 0, "stahl": 0, "forschung": 0}
ressourcen.zustand_importieren({})
messung_ohne = dict(energie_normal)
ressourcen.ressourcen_produzieren(messung_ohne, gebaeude)
ohne_stoerung = messung_ohne["energie"]
assert ohne_stoerung > 0, "Ohne Stoerung muss der Reaktor Energie liefern"

ereignisse.ereignisse_zuruecksetzen()
meldung = ereignisse.ereignis_ausloesen("systemausfall", energie_normal, gebaeude)
assert meldung["ereignis"] == "systemausfall"
assert ressourcen.energie_stoerung_rest() == ereignisse.DAUER_TICKS == 180
mit_stoerung = dict(energie_normal)
mit_stoerung["energie"] = 0
ressourcen.ressourcen_produzieren(mit_stoerung, gebaeude)
erwartet = ohne_stoerung * ressourcen.SYSTEMAUSFALL_FAKTOR
assert abs(mit_stoerung["energie"] - erwartet) < 0.01, (mit_stoerung, erwartet)

# Reparatur kostet Gold und behebt die Stoerung sofort.
assert not ereignisse.systemausfall_reparieren({"gold": 99})
assert ressourcen.energie_stoerung_aktiv()
gold = {"gold": 100, "energie": 0}
assert ereignisse.systemausfall_reparieren(gold)
assert gold["gold"] == 0
assert not ressourcen.energie_stoerung_aktiv()
print("Systemausfall: -30 % für 180 Ticks, Reparatur für 100 Gold")


# ── 4. Meteoritenschauer: 10 Gebäude mit -80 % Produktion ────────────────
ereignisse.ereignisse_zuruecksetzen()
kolonie = [{"typ": 1, "arbeitet": True} for _ in range(15)]
meldung = ereignisse.ereignis_ausloesen("meteoritenschauer", werte, kolonie)
assert meldung["ereignis"] == "meteoritenschauer"
assert meldung["anzahl"] == ereignisse.METEOR_GEBAEUDE == 10
assert ereignisse.beschaedigte_anzahl(kolonie) == 10
# 5 unbeschaedigte gegen 5 beschaedigte Reaktoren: die beschaedigten
# produzieren nur noch 20 Prozent. Welche Gebaeude getroffen wurden, entscheidet
# der Zufall - deshalb hier nach echtem Zustand sortieren.
heil_liste = [g for g in kolonie if not ressourcen.gebaeude_beschaedigt(g)][:5]
kaputt_liste = [g for g in kolonie if ressourcen.gebaeude_beschaedigt(g)][:5]
assert len(heil_liste) == 5 and len(kaputt_liste) == 5
basis = {"gold": 0, "energie": 0, "holz": 400, "stein": 400,
         "bevoelkerung": 60, "nahrung": 100, "kohle": 400,
         "eisen": 0, "roboter": 0, "stahl": 0, "forschung": 0}
ressourcen.zustand_importieren({})
heil = dict(basis)
ressourcen.ressourcen_produzieren(heil, heil_liste)
ressourcen.zustand_importieren({})
kaputt = dict(basis)
ressourcen.ressourcen_produzieren(kaputt, kaputt_liste)
assert heil["energie"] > 0
erwartet = heil["energie"] * ressourcen.BESCHAEDIGT_FAKTOR
assert abs(kaputt["energie"] - erwartet) < 0.01, (kaputt, erwartet)
# Der Schaden laeuft nach der eingestellten Zeit ab.
for _ in range(ereignisse.DAUER_TICKS):
    ressourcen._schaden_ticken(kolonie)
assert ereignisse.beschaedigte_anzahl(kolonie) == 0
print("Meteoritenschauer: 10 Gebäude, 80 % weniger, Schaden läuft ab")


# ── 5. Raumschiff: 50/50, Deckel 75 je Ressource, Rückgabe ──────────────
import random
ereignisse.ereignisse_zuruecksetzen()
lager = {"gold": 100, "energie": 100, "holz": 200, "stein": 100,
         "nahrung": 100, "kohle": 0, "eisen": 0, "stahl": 0,
         "bevoelkerung": 10, "forschung": 0, "zufriedenheit": 0.0}
meldung = ereignisse.ereignis_ausloesen("raumschiff", lager, [])
assert meldung["ereignis"] == "raumschiff"
assert ereignisse.angebot_ist_offen()

# Ohne Auswahl passiert beim Enter nichts.
assert not ereignisse.angebot_abschicken(lager)
assert lager["gold"] == 100

# Obergrenze: mehr als 75 Einheiten einer Ressource gehen nicht.
for _ in range(40):
    ereignisse.taste(pygame.K_UP, lager)
auswahl = dict(ereignisse.angebot_uebersicht())
assert auswahl["gold"] == ereignisse.MAX_EINSATZ == 75
# Andere Ressourcen bleiben unberührt.
assert auswahl["energie"] == 0

# 60 Versuche: es muessen beide Ausgaenge vorkommen.
gewinne, verluste = [], []
for versuch in range(60):
    random.seed(versuch)
    lager["holz"] = 100
    ereignisse.ereignisse_zuruecksetzen()
    ereignisse.ereignis_ausloesen("raumschiff", lager, [])
    ereignisse.taste(pygame.K_e, lager)      # Holz waehlen
    for _ in range(12):
        ereignisse.taste(pygame.K_UP, lager)  # Holz = 60
    assert ereignisse.angebot_summe() == 60
    assert ereignisse.angebot_abschicken(lager)
    (gewinne if lager["holz"] > 100 else verluste).append(lager["holz"])
assert gewinne and verluste, "Es muss beide Ausgaenge geben"
assert set(gewinne) == {160}, gewinne     # 100 - 60 Einsatz + 120 zurueck
assert set(verluste) == {40}, verluste    # 100 - 60 Einsatz, sonst nichts
assert not ereignisse.angebot_ist_offen()
print("Raumschiff: Deckel 75, 50/50 gefunden und verloren")


# ── 6. Raumschiff: zu wenig Ressourcen wird nicht eingesetzt ─────────────
ereignisse.ereignisse_zuruecksetzen()
lager["holz"] = 5
ereignisse.ereignis_ausloesen("raumschiff", lager, [])
ereignisse.taste(pygame.K_e, lager)
for _ in range(5):
    ereignisse.taste(pygame.K_UP, lager)   # Holz = 25, aber nur 5 da
assert not ereignisse.angebot_abschicken(lager)
assert lager["holz"] == 5
assert ereignisse.angebot_ist_offen()
assert ereignisse.taste(pygame.K_ESCAPE, lager)
assert not ereignisse.angebot_ist_offen()
print("Raumschiff: zu wenig Lager und Ablehnen funktionieren")

# ── 7. Ereignisse: Tick, Ablauf und Speichern/Laden ─────────────────────
ereignisse.ereignisse_zuruecksetzen()
lager = {"gold": 500, "energie": 100, "holz": 100, "stein": 100,
         "nahrung": 100, "kohle": 100, "eisen": 100, "stahl": 0,
         "bevoelkerung": 10, "forschung": 0, "zufriedenheit": 0.0}
assert ereignisse.ereignisse_tick(lager, kolonie) is None   # noch zu frueh
# Wichtig: erst den Modulzustand leeren, DANN den Systemausfall ausloesen -
# ressourcen.zustand_importieren({}) setzt auch die Energiestoerung auf 0.
ressourcen.zustand_importieren({})
ereignisse.ereignis_ausloesen("systemausfall", lager, kolonie)
# Ein echter Spieltick: erst produzieren (das zaehlt die Stoerung herunter),
# danach die Ereignisse.
messung = dict(lager)
ressourcen.ressourcen_produzieren(messung, heil_liste)
assert ressourcen.energie_stoerung_rest() == 179
assert ereignisse.ereignisse_tick(messung, kolonie) is None
assert ressourcen.energie_stoerung_rest() == 179   # der Tick zaehlt nicht weiter
zustand = ereignisse.zustand_exportieren()
ereignisse.ereignisse_zuruecksetzen()
assert not ressourcen.energie_stoerung_aktiv()
ereignisse.zustand_importieren(zustand)
assert ressourcen.energie_stoerung_rest() == 179
# Kaputter Spielstand darf nichts abstuerzen.
ereignisse.zustand_importieren({"angebot": "quatsch", "tick": "x"})
assert not ressourcen.energie_stoerung_aktiv()
print("Ereignisse: Tick zählt, Spielstand speichert, kaputte Daten sind sicher")


# ── 8. Statistik: zählt, merkt und überlebt das Neustarten ───────────────
if os.path.isfile(statistik.DATEI):
    os.remove(statistik.DATEI)
# Klarer Start: die Ereignistests oben haben schon gezaehlt.
statistik.zustand_zuruecksetzen()
statistik.neue_partie()
statistik.gebaeude_gebaut(3)
statistik.forschung_erzeugt(120)
statistik.handelsaktion()
statistik.technologie_erforscht()
statistik.ereignis("systemausfall")
for _ in range(5):
    statistik.tick({"bevoelkerung": 42}, [])
profil = statistik.profil_werte()
assert profil["gebaeude"] == 3
assert profil["forschung"] == 120
assert profil["zeit"] == 5
assert profil["max_bevoelkerung"] == 42
assert profil["ereignisse"] == 1
assert statistik.ereignisse_uebersicht() == {"systemausfall": 1}
assert statistik.zeit_text(3725) == "1 Std 2 Min 5 Sek"
assert statistik.zeit_text(95) == "1 Min 35 Sek"
assert statistik.speichern()
# Neu laden: die Werte stehen noch da.
statistik.zustand_zuruecksetzen()
assert statistik.laden()
assert statistik.profil_werte()["gebaeude"] == 3
# Das Profil bleibt, die laufende Partie beginnt nach dem Laden neu.
assert statistik.partei_werte()["gebaeude"] == 0
statistik.neue_partie()
statistik.gebaeude_gebaut(1)
assert statistik.partei_werte()["gebaeude"] == 1
assert statistik.profil_werte()["gebaeude"] == 4
# Kaputte Datei: leere Statistik statt Absturz.
with open(statistik.DATEI, "w", encoding="utf-8") as datei:
    datei.write("{ kaputt")
assert not statistik.laden()
assert statistik.profil_werte()["gebaeude"] == 0
assert len(statistik.uebersicht_zeilen()) == len(statistik.FELDER)
print("Statistik: zählt, speichert, kaputte Datei ist sicher")


# ── 9. Neue Achievements ─────────────────────────────────────────────────
assert len(achievements.ACHIEVEMENTS) == 37      # passt in 3 Spalten mit 13
for ziel in ("architekt", "forschungslegende", "stahlzeitalter"):
    assert achievements.eintrag(ziel) is not None, ziel
assert achievements.eintrag("architekt")["fortschritt"] == "profil_gebaeude"

achievements.zustand_zuruecksetzen()
neu = achievements.pruefen({}, [], [[0]], profil={"gebaeude": 100,
                                                  "forschung": 1000})
assert "architekt" in neu and "forschungslegende" in neu, neu
assert "stahlzeitalter" not in neu
assert "architekt" not in achievements.pruefen({}, [], [[0]],
                                               profil={"gebaeude": 100})
achievements.zustand_zuruecksetzen()
assert "stahlzeitalter" not in achievements.pruefen({}, [], [[0]])
achievements.stahl_erzeugt(1)
assert "stahlzeitalter" in achievements.pruefen({}, [], [[0]])
# Ohne Profil zaehlen die Langzeitziele nicht.
achievements.zustand_zuruecksetzen()
assert "architekt" not in achievements.pruefen({}, [], [[0]])
print("Achievements: 100 Gebäude, 1000 Forschung, erste Stahlproduktion")

if os.path.isfile(statistik.DATEI):
    os.remove(statistik.DATEI)
pygame.quit()
print("SCHUELERWUENSCHE_TESTS_OK")
