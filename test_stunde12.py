"""Selbsttest für Sieg/Niederlage, Pause und Speichern/Laden."""
import os
import sys
import tempfile

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(__file__))

import pygame
pygame.init()
import main
import forschung
import handel
import spielstand
import achievements
import missionen

assert len(achievements.ACHIEVEMENTS) >= 20
assert len(missionen.MISSIONEN) >= 10
assert sum(eintrag["punkte"] for eintrag in achievements.ACHIEVEMENTS) >= 500

main.spiel_menue.menue_initialisieren(main.fenster)
main.menu.menu_initialisieren(main.fenster)
main.hud.hud_initialisieren(main.fenster)
main.achievements.initialisieren(main.fenster)
main.missionen.initialisieren(main.fenster)

# Hauptmenü -> Regelmenü -> freies Spiel auswählen und wieder zurück.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r))
assert main.hauptmenue_verarbeiten()
assert main.spiel_status == "regelmenue"
main.spielwelt_zeichnen()
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_3))
assert main.regelmenue_verarbeiten()
assert main._regel_auswahl == "freies_spiel"
assert main.aktives_regelwerk()["sieg_aktiv"] is False
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
assert main.regelmenue_verarbeiten()
assert main.spiel_status == "hauptmenue"

# Die Missionszentrale ist ebenfalls vom Hauptmenü aus erreichbar.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_m))
assert main.hauptmenue_verarbeiten()
assert main.spiel_status == "missionen"
main.spielwelt_zeichnen()
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
assert main.missionenmenue_verarbeiten()
assert main.spiel_status == "hauptmenue"

# Alle vier sichtbaren Zustände müssen ohne Zeichenfehler rendern.
main.spielwelt_zeichnen()

# Die Achievement-Ansicht ist vom Hauptmenü aus erreichbar.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
assert main.hauptmenue_verarbeiten()
assert main.spiel_status == "achievements"
main.spielwelt_zeichnen()
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
assert main.achievementsmenue_verarbeiten()
assert main.spiel_status == "hauptmenue"

# Für die restlichen Tests das Standardregelwerk starten.
main._regel_auswahl = "standard"
# Der Start über Enter im Hauptmenü erzeugt die erste Kolonie.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
assert main.hauptmenue_verarbeiten()
assert main.spiel_status == "spiel"

# Neues Spiel setzt alle Welt- und Modulzustände zurück.
main.neues_spiel_starten()
assert main.spiel_status == "spiel"
assert main.liste_gebaeude == []
main.spielwelt_zeichnen()
assert main.ressourcen_dict["bevoelkerung"] == 10

# Missionen prüfen eine einfache Bedingung und zahlen eine Belohnung aus.
missionen.zustand_zuruecksetzen()
main.ressourcen_dict["gold"] = 100
main.liste_gebaeude = [{"typ": 0}]
main.missionen_pruefen()
assert missionen.ist_erledigt("erste_kolonie")
assert main.ressourcen_dict["gold"] == 150

# Achievement-Fortschritt und freies Spiel.
achievements.zustand_zuruecksetzen()
achievements.gebaeude_gebaut(0)
main.achievements_pruefen()
assert "erste_schritte" in achievements.zustand_exportieren()["erreicht"]
main._regel_auswahl = "freies_spiel"
main.ressourcen_dict["nahrung"] = 0
for _ in range(30):
    main.spielstatus_pruefen()
assert main.spiel_status == "spiel"
main._regel_auswahl = "standard"

# ESC öffnet Pause und ein weiteres ESC setzt das Spiel fort.
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
assert main.ereignisse_verarbeiten()
assert main.spiel_status == "pause"
main.spielwelt_zeichnen()
assert main.pausemenue_verarbeiten()
pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
assert main.pausemenue_verarbeiten()
assert main.spiel_status == "spiel"
assert main.spiel_geschwindigkeit == 1

# Siegbedingung: Koloniezentrum plus 30 Bewohner.
main.liste_gebaeude = [{"typ": main.SIEG_GEBAEUDE_TYP}]
main.ressourcen_dict["bevoelkerung"] = main.SIEG_BEVOELKERUNG
main.spielstatus_pruefen()
assert main.spiel_status == "sieg"
main.spielwelt_zeichnen()
assert "zielmeister" in achievements.zustand_exportieren()["erreicht"]

# Niederlagebedingung: zwölf Wirtschaftsticks ohne Nahrung.
main.neues_spiel_starten()
main.ressourcen_dict["nahrung"] = 0
for _ in range(main.NIEDERLAGE_NULLRESSOURCE_TICKS):
    main.spielstatus_pruefen()
assert main.spiel_status == "niederlage"
main.spielwelt_zeichnen()

# Save/Load erhält Welt, Gebäude, laufende Forschung und Handelsangebot.
main.neues_spiel_starten()
main.karten_daten[4][5] = 2
main.sterne_liste = [{"x": 12, "y": 34, "groesse": 2, "helligkeit": 180}]
main.ressourcen_dict["gold"] = 321
main.liste_gebaeude = [{"typ": 0, "kachel_x": 2, "kachel_y": 2, "arbeitet": True}]
forschung.zustand_importieren({
    "erforschte_technologien": ["effiziente_bautechnik"],
    "forschungsauftrag": {"id": "produktion", "fortschritt": 3, "ziel": 10},
})
handel.zustand_importieren({
    "tick": 7,
    "angebot": {"geben": {"holz": 20}, "nehmen": {"stein": 10}, "text": "Holz gegen Stein"},
})
achievements.zustand_importieren({"erreicht": ["erste_schritte"], "zaehler": {"gesamt_gebaeude": 1}})
spielstand.DATEI = os.path.join(tempfile.gettempdir(), "mike_version_test_spielstand.json")
if os.path.exists(spielstand.DATEI):
    os.remove(spielstand.DATEI)
erfolg, _ = spielstand.speichern(
    main.karten_daten, main.sterne_liste, main.ressourcen_dict,
    main.liste_gebaeude, 25, 35, 4, 2, "2", 1, 1, 0, "spiel")
assert erfolg
main.ressourcen_dict["gold"] = 1
main.liste_gebaeude = []
daten, _ = spielstand.laden()
assert daten is not None
assert daten["ressourcen"]["gold"] == 321
assert daten["gebaeude"][0]["typ"] == 0
assert daten["karten_daten"][4][5] == 2
assert forschung.ist_technologie_erforscht("effiziente_bautechnik")
assert forschung.forschung_laeuft()
assert handel.aktuelles_angebot()["text"] == "Holz gegen Stein"
assert daten["regel_auswahl"] == "standard"
assert "achievements" in daten
assert "erste_schritte" in daten["achievements"]["erreicht"]
assert "missionen" in daten
assert "erste_kolonie" in daten["missionen"]["erledigt"]
os.remove(spielstand.DATEI)
pygame.quit()
print("STUNDE12_TESTS_OK")
