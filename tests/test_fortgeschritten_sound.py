"""Selbsttest für das Ton-Modul (Fortgeschrittener Kurs, Stunde 1 — Phase 2).

Der Test läuft headless (dummy Video- und Audio-Treiber) und prüft:
  1. Alle Dateien aus SOUNDS existieren und sind gültige WAV-Dateien
     (22050 Hz, 16 Bit, mono) — geprüft mit dem Standardmodul ``wave``.
  2. Der Pygame-Mixer lädt alle Effekte, sofern ein Audiogerät verfügbar ist.
  3. ton.py funktioniert auch OHNE Mixer: alle Funktionen sind dann No-Ops.
  4. Gleiche Effekte werden innerhalb von SOUND_ABSTAND_MS nicht doppelt
     gestartet (Schutz vor Knistern).
  5. zustand_exportieren/zustand_importieren verhalten sich wie in den anderen
     Modulen (inkl. Default für alte Spielstände).

Aufruf im Projektordner: python test_fortgeschritten_sound.py
"""

import os
import sys
import wave

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

pygame.init()
import ton

# ── 1. Die Pflicht-Effekte müssen im Dictionary stehen ──────────────────────
pflicht_effekte = {
    "bauen", "abriss", "fehler", "achievement", "mission_erledigt",
    "forschung_fertig", "terraforming", "handel", "sieg", "niederlage",
    "angriff_warnung", "abwehr_erfolg", "ausgeraubt",
}
assert pflicht_effekte.issubset(set(ton.SOUNDS)), "Es fehlen Pflicht-Effekte"

# Der Musik-Loop und alle Effekte liegen als gültige WAV-Datei vor.
alles = list(ton.SOUNDS.items()) + [("musik", ton.MUSIK_DATEI)]
for name, dateiname in alles:
    pfad = os.path.join(ton.sounds_ordner(), dateiname)
    assert os.path.isfile(pfad), f"Sounddatei fehlt: {dateiname}"
    with wave.open(pfad, "rb") as datei:
        assert datei.getnchannels() == 1, f"{dateiname} ist nicht mono"
        assert datei.getsampwidth() == 2, f"{dateiname} ist nicht 16 Bit"
        assert datei.getframerate() == 22050, f"{dateiname} hat falsche Rate"
        assert datei.getnframes() > 0, f"{dateiname} ist leer"

# Die Hintergrundmusik ist ein echter Loop (deutlich länger als ein Effekt).
with wave.open(os.path.join(ton.sounds_ordner(), ton.MUSIK_DATEI), "rb") as datei:
    musik_sekunden = datei.getnframes() / datei.getframerate()
assert 40.0 <= musik_sekunden <= 70.0, "Musik-Loop sollte 40-70 s lang sein"

# ── 2. Mixer initialisieren und alle Effekte laden ─────────────────────────
bereit = ton.initialisieren()
assert bereit == ton.mixer_bereit()
# Zweimal initialisieren darf keinen Fehler ergeben (Spielstart + Test).
ton.initialisieren()
if bereit:
    for name in ton.SOUNDS:
        assert ton._effekt_laden(name) is not None, f"{name} nicht ladbar"

# ── 3. Ohne Mixer bleibt alles ein No-Op (kein Absturz) ─────────────────────
ton._mixer_bereit = False
assert ton.sound_abspielen("bauen") is False
assert ton.sound_abspielen("gibt_es_nicht") is False
assert ton.musik_starten() is False
ton.musik_pausieren()
ton.musik_fortsetzen()
ton.musik_stoppen()
ton.musik_umschalten()          # schaltet nur den Merker um
assert ton.musik_ist_an() is False
ton.musik_umschalten()
assert ton.musik_ist_an() is True

# ── 4. Doppelstart-Schutz (SOUND_ABSTAND_MS) ───────────────────────────────
ton._mixer_bereit = bereit
if bereit:
    ton._letzte_startzeit.clear()
    ton._abspielzaehler.clear()
    assert ton.sound_abspielen("bauen") is True
    assert ton.sound_abspielen("bauen") is False, "Effekt wurde doppelt gestartet"
    assert ton.abspielzaehler("bauen") == 1
    pygame.time.wait(ton.SOUND_ABSTAND_MS + 30)
    assert ton.sound_abspielen("bauen") is True
    assert ton.abspielzaehler("bauen") == 2
    assert ton.abspielzaehler("abriss") == 0

# ── 5. Zustand wie in den anderen Modulen ─────────────────────────────────
assert ton.zustand_exportieren()["musik_an"] is True
ton.zustand_importieren({"musik_an": False})
assert ton.musik_ist_an() is False
assert ton.musik_status_text().endswith("aus")
ton.zustand_importieren({})              # alter Spielstand ohne das Feld
assert ton.musik_ist_an() is True
ton.zustand_zuruecksetzen()
assert ton.musik_ist_an() is True

pygame.quit()
print("FORTGESCHRITTEN_SOUND_TESTS_OK")
