"""Selbsttest fuer Strassennetz und Logistik (Fortgeschrittener Kurs).

Getestet wird das Modul logistik.py im Zusammenspiel mit der Wirtschaft:
    1. Gebaeude ohne Strasse stehen still (keine Produktion, kein Verbrauch).
    2. Mit Strasse zur Basis arbeiten sie wieder.
    3. Strasse abreiissen kappt das Netz sofort.
    4. Mehrkachel-Gebaeude (Universitaet 2x3) werden ueber die ganze
       Flaeche geprueft.
    5. Ausnahmen wie der Park brauchen keine Strasse.
    6. LOGISTIK_AKTIV = False schaltet das ganze System ab.
    7. Achievements und Mission zur Logistik werden erreicht.
"""
import os
import sys
import tempfile

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(__file__))

import pygame
pygame.init()
import main
import logistik
import ressourcen
import achievements
import missionen
import spielstand

# Gleiches Bootstrap wie in den anderen Tests: Menues und Fenster.
main.spiel_menue.menue_initialisieren(main.fenster)
main.menu.menu_initialisieren(main.fenster)
main.hud.hud_initialisieren(main.fenster)
main.achievements.initialisieren(main.fenster)
main.missionen.initialisieren(main.fenster)
logistik.initialisieren(main.fenster)

# Die Logistik-Achievements und die Mission "Erste Strasse" muessen
# registriert sein, bevor wir sie am Ende des Tests erreichen.
achievements_ids = {eintrag["id"] for eintrag in achievements.ACHIEVEMENTS}
assert "strassenbauer" in achievements_ids
assert "gut_vernetzt" in achievements_ids
assert any(m["id"] == "erste_strasse" for m in missionen.MISSIONEN)

# Neues Spiel gibt einen leeren, definierten Zustand.
main.neues_spiel_starten()
logistik.zustand_zuruecksetzen()
assert logistik.LOGISTIK_AKTIV is True

# ── Hilfsaufbau: Basis links, Gebaeude rechts ohne Verbindung ────────────
basis = {"typ": 0, "kachel_x": 2, "kachel_y": 2}
reaktor = {"typ": 1, "kachel_x": 6, "kachel_y": 4}   # produziert Energie
park = {"typ": 19, "kachel_x": 20, "kachel_y": 20}   # Ausnahme ohne Strasse
uni = {"typ": 7, "kachel_x": 10, "kachel_y": 5}      # 2x3 Mehrkachel-Gebaeude
main.liste_gebaeude = [basis, reaktor, park, uni]

# ── Test 1: Ohne Strasse steht der Reaktor still ─────────────────────────
ergebnis = logistik.netz_aktualisieren(main.liste_gebaeude)
assert ergebnis["ohne_anbindung"] == 2, "Reaktor und Uni muessen stillstehen"
assert reaktor["stillstand_grund"] == logistik.STILLSTAND_GRUND
assert uni["stillstand_grund"] == logistik.STILLSTAND_GRUND
assert logistik.braucht_anbindung(19) is False
assert "stillstand_grund" not in park, "Park braucht keine Strasse"

# Wirtschaftstick: Der stillstehende Reaktor produziert und verbraucht
# nichts — die Energie bleibt exakt gleich.
main.ressourcen_dict["energie"] = 50.0
main.ressourcen_dict["holz"] = 50.0
main.ressourcen_dict["bevoelkerung"] = 10.0
ressourcen.ressourcen_produzieren(main.ressourcen_dict, main.liste_gebaeude)
assert reaktor["arbeitet"] is False
# Die Basis produziert als Ausnahme weiter +1 Energie pro Tick — genau
# diese Aenderung ist erlaubt; der Reaktor hat nichts beigetragen.
assert main.ressourcen_dict["energie"] == 51.0

# Effizienz: Der Wirtschaftstick darf das Netz NICHT neu berechnen —
# nur Bauen, Abriss, Laden und ein neues Spiel aktualisieren es.
aktualisierungen_vorher = logistik.aktualisierungen()
ressourcen.ressourcen_produzieren(main.ressourcen_dict, main.liste_gebaeude)
assert logistik.aktualisierungen() == aktualisierungen_vorher

# ── Test 2: Strassen zur Basis bauen — alles arbeitet wieder ─────────────
# Kette: Basis (2,2) → Strassen nach rechts → Abzweigung zum Reaktor und
# weiter zur Universitaet. 11 Strassen reichen fuer beide Anschluesse.
strassen_kacheln = [(3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
                    (9, 2), (9, 3), (9, 4), (9, 5), (6, 3)]
strassen = [{"typ": 9, "kachel_x": x, "kachel_y": y}
            for (x, y) in strassen_kacheln]
main.liste_gebaeude.extend(strassen)
ergebnis = logistik.netz_aktualisieren(main.liste_gebaeude)
assert ergebnis["netz_kacheln"] == len(strassen_kacheln)
assert "stillstand_grund" not in reaktor, "Reaktor ist jetzt angebunden"
assert "stillstand_grund" not in uni, "Uni grenzt mit Kachel (10,5) an Strasse (9,5)"
assert logistik.ist_angebunden(reaktor) is True

# Wirtschaftstick: Der Reaktor arbeitet und verbraucht 2 Holz pro Tick —
# der Verbrauch zeigt, dass wirklich gerechnet wird.
holz_vorher = main.ressourcen_dict["holz"]
ressourcen.ressourcen_produzieren(main.ressourcen_dict, main.liste_gebaeude)
assert reaktor["arbeitet"] is True
assert main.ressourcen_dict["holz"] < holz_vorher

# Stillstehende Gebaeude belegen kein Personal: Bei 10 Bewohnern zählt
# nur das Personal der ANGEBUNDENEN Gebaeude als Bedarf.
verfuegbar, bedarf = ressourcen.personal_info(main.ressourcen_dict,
                                              main.liste_gebaeude)
assert verfuegbar == 10
assert bedarf == ressourcen.personalbedarf(1) + ressourcen.personalbedarf(7)

# ── Test 3: Strasse abreiissen kappt das Netz sofort ─────────────────────
# Die Strasse direkt neben der Uni (9,5) wird entfernt.
main.liste_gebaeude.remove(next(
    g for g in main.liste_gebaeude
    if g.get("typ") == 9 and g.get("kachel_x") == 9
    and g.get("kachel_y") == 5))
ergebnis = logistik.netz_aktualisieren(main.liste_gebaeude)
assert uni.get("stillstand_grund") == logistik.STILLSTAND_GRUND, \
    "Die Universitaet ist wieder abgehangen"
assert "stillstand_grund" not in reaktor, "Der Reaktor bleibt angebunden"

# ── Test 4: Auch die letzten Strassen weg → Reaktor steht still ──────────
main.liste_gebaeude = [g for g in main.liste_gebaeude if g.get("typ") != 9]
ergebnis = logistik.netz_aktualisieren(main.liste_gebaeude)
assert ergebnis["ohne_anbindung"] == 2
assert reaktor["stillstand_grund"] == logistik.STILLSTAND_GRUND

# ── Test 5: LOGISTIK_AKTIV = False (Schalter fuer alte Tests) ────────────
# Ohne Logistik arbeitet jedes Gebaeude wie frueher — der Grund
# "Keine Strassenanbindung" wird wieder entfernt.
logistik.LOGISTIK_AKTIV = False
ergebnis = logistik.netz_aktualisieren(main.liste_gebaeude)
assert ergebnis["ohne_anbindung"] == 0
assert "stillstand_grund" not in reaktor
main.ressourcen_dict["holz"] = 50.0
ressourcen.ressourcen_produzieren(main.ressourcen_dict, main.liste_gebaeude)
assert reaktor["arbeitet"] is True
logistik.LOGISTIK_AKTIV = True          # Schalter fuer weitere Tests zurueck
logistik.netz_aktualisieren(main.liste_gebaeude)

# ── Test 6: Achievements und Mission zur Logistik ────────────────────────
# Wieder alles anbinden (gleiche Strassen wie oben) und pruefen.
main.liste_gebaeude.extend(
    [{"typ": 9, "kachel_x": x, "kachel_y": y} for (x, y) in strassen_kacheln])
logistik.netz_aktualisieren(main.liste_gebaeude)
assert logistik.anzahl_ohne_anbindung(main.liste_gebaeude) == 0

achievements.zustand_zuruecksetzen()
main.achievements_pruefen()
erreicht = achievements.zustand_exportieren()["erreicht"]
assert "strassenbauer" in erreicht, "10 Strassen muessen das Achievement ausloesen"
assert "gut_vernetzt" in erreicht, "Alle Gebaeude sind angebunden"

missionen.zustand_zuruecksetzen()
main.missionen_pruefen()
assert missionen.ist_erledigt("erste_strasse")

# ── Test 7: Spielstand-Rundlauf mit Logistik-Zustand ─────────────────────
logistik.ansicht_umschalten()           # Ansicht "an" als Zustand speichern
spielstand.DATEI = os.path.join(tempfile.gettempdir(),
                                "fortgeschritten_logistik_test.json")
if os.path.exists(spielstand.DATEI):
    os.remove(spielstand.DATEI)
erfolg, _ = spielstand.speichern(
    main.karten_daten, main.sterne_liste, main.ressourcen_dict,
    main.liste_gebaeude, 25, 35, 4, 2, "2", 1, 1, 0, "spiel")
assert erfolg
daten, _ = spielstand.laden()
assert daten is not None
assert "logistik" in daten, "Der Logistik-Zustand muss gespeichert werden"
assert daten["logistik"]["ansicht_aktiv"] is True
logistik.zustand_importieren(daten["logistik"])
assert logistik.ansicht_aktiv() is True
logistik.zustand_zuruecksetzen()
os.remove(spielstand.DATEI)

pygame.quit()
print("FORTGESCHRITTEN_LOGISTIK_TESTS_OK")

