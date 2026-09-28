"""Selbsttest für das Einstellungs-Modul (Einstellungsmenü mit JSON-Datei).

Der Test läuft headless (dummy Video- und Audio-Treiber) und prüft:
  1. Laden/Speichern als eigene JSON-Datei (getrennt vom Spielstand)
  2. Wertebereiche: alles außerhalb wird begrenzt, Unbekanntes ignoriert
  3. Kaputte Datei = Standardwerte, kein Absturz
  4. Ton-Verkabelung: Lautstärke und Musik an/aus wirken sofort
  5. Menü: Zeichnen, Tastatur, Mausklicks, Slider und Rückkehr zum Ursprung

Aufruf im Projektordner: python tests/test_einstellungen.py
"""

import json
import os
import sys
import tempfile

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

pygame.init()
import einstellungen
import ton

# Die echte Datei bleibt unberührt — der Test nutzt ein Temporärverzeichnis.
with tempfile.TemporaryDirectory() as ordner:
    einstellungen.DATEI = os.path.join(ordner, "einstellungen.json")

    # ── 1. Ohne Datei gelten die Standards ────────────────────────────────
    assert einstellungen.laden() is False
    assert einstellungen.wert("fps") == 60
    assert einstellungen.wert("musik_an") is True
    assert einstellungen.wert("unbekannt") is None

    # ── 2. Werte werden begrenzt, Unbekanntes ignoriert ───────────────────
    assert einstellungen.setzen("fps", 500) == 120
    assert einstellungen.setzen("fps", 10) == 30
    assert einstellungen.setzen("musik_lautstaerke", -1) == 0.0
    assert einstellungen.setzen("musik_lautstaerke", 2.5) == 1.0
    assert einstellungen.setzen("kamera_tempo", 999) == 16
    assert einstellungen.setzen("gitter_an", 0) is False
    assert einstellungen.setzen("quatsch", 1) is None

    # ── 1b. Roundtrip: schreiben, neu laden, Werte stimmen ────────────────
    einstellungen.setzen("fps", 120)
    einstellungen.setzen("musik_an", False)
    assert einstellungen.laden() is True
    assert einstellungen.wert("fps") == 120
    assert einstellungen.wert("musik_an") is False
    assert einstellungen.wert("gitter_an") is False  # zuvor gesetzt → überlebt den Roundtrip

    # ── 3. Kaputte Datei: Standard statt Absturz ──────────────────────────
    with open(einstellungen.DATEI, "w", encoding="utf-8") as datei:
        datei.write("{ kaputt")
    assert einstellungen.laden() is False
    assert einstellungen.wert("fps") == 60

    # Fehlerhafte Typen in einer intakten Datei werden bereinigt.
    with open(einstellungen.DATEI, "w", encoding="utf-8") as datei:
        json.dump({"fps": "120", "musik_lautstaerke": "nein",
                   "gitter_an": 1, "quatsch": 5}, datei)
    assert einstellungen.laden() is True
    assert einstellungen.wert("fps") == 120          # "120" → 120
    assert einstellungen.wert("musik_lautstaerke") == 0.45  # nicht lesbar → Standard
    assert einstellungen.wert("gitter_an") is True   # 1 → True
    assert einstellungen.wert("quatsch") is None     # unbekannter Schlüssel

    # ── 4. Ton-Verkabelung ────────────────────────────────────────────────
    einstellungen.zuruecksetzen()
    ton.initialisieren()          # ohne Gerät alles No-Op — darf nicht stürzen
    einstellungen.setzen("musik_lautstaerke", 0.25)
    assert ton.MUSIK_LAUTSTAERKE == 0.25
    einstellungen.setzen("effekt_lautstaerke", 0.5)
    assert ton.EFFEKT_LAUTSTAERKE == 0.5
    ton.musik_an_setzen(False)
    assert ton.musik_ist_an() is False
    einstellungen.setzen("musik_an", ton.musik_ist_an())
    assert einstellungen.wert("musik_an") is False

    # Zurück auf Standard — auch im Ton-Modul wieder hörbar.
    einstellungen.zuruecksetzen()
    einstellungen.alle_anwenden()
    assert ton.MUSIK_LAUTSTAERKE == 0.45
    assert ton.EFFEKT_LAUTSTAERKE == 0.70
    assert ton.musik_ist_an() is True

    # ── 5. Menü ───────────────────────────────────────────────────────────
    einstellungen.menue_initialisieren(pygame.Surface((1000, 700)))
    einstellungen.menue_oeffnen()
    einstellungen.menu_zeichnen()           # darf nicht abstürzen

    assert einstellungen.ziel() == "hauptmenue"
    einstellungen.ziel_setzen("pause")
    assert einstellungen.ziel() == "pause"
    einstellungen.ziel_setzen("quatsch")    # ungültiges Ziel wird ignoriert
    assert einstellungen.ziel() == "pause"

    # Esc schließt das Menü.
    assert einstellungen.taste(pygame.K_ESCAPE) == "zurueck"

    # Pfeil rechts/links am Slider (Zeile 0) ändert die Lautstärke sofort.
    einstellungen.menue_oeffnen()
    assert ton.MUSIK_LAUTSTAERKE == 0.45
    assert einstellungen.taste(pygame.K_RIGHT) is None
    assert einstellungen.wert("musik_lautstaerke") == 0.50
    assert ton.MUSIK_LAUTSTAERKE == 0.50
    assert einstellungen.taste(pygame.K_LEFT) is None
    assert einstellungen.wert("musik_lautstaerke") == 0.45

    # Zur letzten Zeile (Fertig) und Enter führt zurück.
    for _ in range(len(einstellungen.ZEILEN) - 1):
        einstellungen.taste(pygame.K_DOWN)
    assert einstellungen.taste(pygame.K_RETURN) == "zurueck"

    # Klick auf die Gitterlinien-Zeile schaltet um und speichert.
    einstellungen.menue_oeffnen()
    vorher = einstellungen.wert("gitter_an")
    einstellungen.mausklick(einstellungen._zeile_rect(3).center)
    assert einstellungen.wert("gitter_an") != vorher
    assert einstellungen.laden() is True    # Änderung steht in der Datei
    assert einstellungen.wert("gitter_an") == (not vorher)

    # Klick auf "Fertig" (letzte Zeile) führt zurück.
    letzte = len(einstellungen.ZEILEN) - 1
    assert einstellungen.mausklick(einstellungen._zeile_rect(letzte).center) == "zurueck"

    # Slider per Klick in die Mitte ≈ 50 %.
    einstellungen.menue_oeffnen()
    balken = einstellungen._balken_rect(0)
    einstellungen.mausklick((balken.x + balken.w // 2, balken.centery))
    einstellungen.maus_loslassen()
    assert 0.45 <= einstellungen.wert("musik_lautstaerke") <= 0.55

print("EINSTELLUNGEN_TESTS_OK")
