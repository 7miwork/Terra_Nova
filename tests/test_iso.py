"""Tests fuer die isometrische Ansicht (iso.py).

Die Spiellogik denkt weiter im normalen Raster. Diese Tests pruefen nur
die Umrechnung: Jede Kachel muss sich exakt hin- und zurueckrechnen
lassen, und ein Klick in eine Raute muss genau diese Kachel treffen.
"""

import math
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import iso

KARTE_BREITE = 60
KARTE_HOEHE = 40


# ── 1. Konstanten: Raute im Verhaeltnis 2 zu 1 ──────────────────────────────
assert iso.ISO_KACHEL_BREITE == 96
assert iso.ISO_KACHEL_HOEHE == 48
assert iso.ISO_KACHEL_BREITE == 2 * iso.ISO_KACHEL_HOEHE
assert iso.ISO_HALB_BREITE == 48
assert iso.ISO_HALB_HOEHE == 24
print("Iso: Raute 96x48, Verhaeltnis 2 zu 1")


# ── 2. Formel mit Zahlenbeispiel: Kachel (3, 1) ─────────────────────────────
# welt_x = (3 - 1) * 48 = 96, welt_y = (3 + 1) * 24 = 96 (obere Ecke).
welt_x, welt_y = iso.raster_zu_welt(3, 1)
assert (welt_x, welt_y) == (96, 96), (welt_x, welt_y)
# Nullpunkt der Karte: Kachel (0, 0) liegt bei Welt (0, 0).
assert iso.raster_zu_welt(0, 0) == (0, 0)
print("Iso: Kachel (3, 1) liegt bei Welt (96, 96)")


# ── 3. Hin- und Rueckrechnung fuer alle 2400 Kacheln ────────────────────────
for zeile in range(KARTE_HOEHE):
    for spalte in range(KARTE_BREITE):
        welt = iso.raster_zu_welt(spalte, zeile)
        zurueck = iso.welt_zu_raster(*welt)
        assert zurueck == (spalte, zeile), (spalte, zeile, welt, zurueck)
        # Die Rautenmitte gehoert immer zur eigenen Kachel.
        mitte = iso.kachel_mitte(spalte, zeile, 0, 0)
        assert iso.welt_zu_raster(*mitte) == (spalte, zeile), (spalte, zeile)
print("Iso: alle 60x40 Kacheln rechnen exakt hin und zurueck")


# ── 4. Wie Test 3, aber mit verschobener Kamera ────────────────────────────
# Die Kamera wird in Bildschirm- UND Welt-Koordinaten addiert, darum muss
# die Mitte plus Kamera wieder dieselbe Kachel liefern.
for kamera_x, kamera_y in [(0, 0), (377, 123), (-900, 50), (2500, 1800)]:
    for spalte, zeile in [(0, 0), (59, 39), (3, 1), (30, 20), (0, 39)]:
        mitte = iso.kachel_mitte(spalte, zeile, kamera_x, kamera_y)
        kachel = iso.welt_zu_raster(mitte[0] + kamera_x,
                                    mitte[1] + kamera_y)
        assert kachel == (spalte, zeile), (spalte, zeile, kamera_x, kamera_y)
print("Iso: Rueckrechnung stimmt auch mit Kamera-Versatz")


# ── 5. Negative Welt-Pixel: floor statt int ────────────────────────────────
# Links und oben neben der Karte ist die Welt negativ. int() wuerde dort
# Richtung null abschneiden und falsche Kacheln liefern.
assert iso.welt_zu_raster(-1, -1) == (-1, -1)
assert iso.welt_zu_raster(-48, 0) == (-1, 0)
assert iso.welt_zu_raster(-96, 24) == (-1, 1)     # Mitte von Kachel (-1, 1)
assert iso.welt_zu_raster(-100, 24) == (-1, 1)    # knapp links daneben
print("Iso: negative Werte runden mit floor richtig ab")


# ── 6. Raute-Ecken: innen trifft, aussen nicht ─────────────────────────────
# Die obere Ecke von Kachel (5, 7) gehoert noch zu ihr, einen Pixel
# darueber beginnt die Nachbarkachel links oben — die beiden Rauten
# teilen sich genau diese Kante. So trennt die Ecke sauber.
ecke_x, ecke_y = iso.raster_zu_welt(5, 7)

assert iso.welt_zu_raster(ecke_x, ecke_y) == (5, 7)
assert iso.welt_zu_raster(ecke_x, ecke_y - 1) == (4, 6)  # Kante zu (4, 6)
assert iso.welt_zu_raster(ecke_x, ecke_y + 1) == (5, 7)
# Linke und rechte Ecke teilen sich zwei Nachbarn: knapp innerhalb der
# Ecke liegt die eigene Kachel, knapp ausserhalb der Nachbar.
mitte_x, mitte_y = iso.kachel_mitte(5, 7, 0, 0)
assert iso.welt_zu_raster(mitte_x - 47, mitte_y) == (5, 7)
assert iso.welt_zu_raster(mitte_x + 47, mitte_y) == (5, 7)
print("Iso: Ecken trennen sauber zwischen Nachbarkacheln")


# ── 7. Polygon: vier Ecken, oben-rechts-unten-links ────────────────────────
punkte = iso.kachel_polygon(3, 1, 0, 0)
assert punkte == [(96, 96), (144, 120), (96, 144), (48, 120)], punkte
# Mit Kamera verschiebt sich alles um denselben Versatz.
punkte_kam = iso.kachel_polygon(3, 1, 10, 20)
assert punkte_kam == [(86, 76), (134, 100), (86, 124), (38, 100)]
# Ankerpunkte fuer Gebaeude-Bilder:
assert iso.kachel_unten_mitte(3, 1, 0, 0) == (96, 144)
print("Iso: Polygon und Anker stimmen mit und ohne Kamera")


# ── 8. Weltgrenzen des Rautenfelds ─────────────────────────────────────────
# x reicht von -40*48 = -1920 bis 60*48 = 2880,
# y reicht von 0 bis (60+40)*24 = 2400.
assert iso.welt_grenzen(60, 40) == (-1920, 0, 2880, 2400)
print("Iso: Weltgrenzen -1920/0 bis 2880/2400")


# ── 9. Sichtbarer Bereich enthaelt die Bildschirmmitte ─────────────────────
# Bei Kamera (0, 0) muss die Kachel unter der Bildschirmmitte von
# sichtbarer_bereich() abgedeckt sein (Culling darf nichts weglassen).
erste_sp, letzte_sp, erste_zei, letzte_zei = iso.sichtbarer_bereich(
    0, 0, 1000, 700, KARTE_BREITE, KARTE_HOEHE)
mitte_kachel = iso.welt_zu_raster(500, 350)
assert erste_sp <= mitte_kachel[0] < letzte_sp
assert erste_zei <= mitte_kachel[1] < letzte_zei
assert erste_sp >= 0 and erste_zei >= 0
assert letzte_sp <= KARTE_BREITE and letzte_zei <= KARTE_HOEHE
# Mitten auf der Karte ist der sichtbare Bereich deutlich kleiner als
# die ganze Karte (sonst waere das Culling nutzlos).
erste_sp, letzte_sp, erste_zei, letzte_zei = iso.sichtbarer_bereich(
    500, 800, 1000, 700, KARTE_BREITE, KARTE_HOEHE)
assert (letzte_sp - erste_sp) < KARTE_BREITE
assert (letzte_zei - erste_zei) < KARTE_HOEHE
print("Iso: sichtbarer Bereich deckt die Mitte ab und spart Kacheln")


# ── 10. Zeichenreihenfolge: hinten zuerst ──────────────────────────────────
assert iso.sortier_schluessel(0, 0) < iso.sortier_schluessel(1, 0)
assert iso.sortier_schluessel(1, 0) < iso.sortier_schluessel(0, 1)
assert iso.sortier_schluessel(0, 1) < iso.sortier_schluessel(1, 1)
gebaeude = [{"typ": 1, "kachel_x": 5, "kachel_y": 7},
            {"typ": 1, "kachel_x": 0, "kachel_y": 0},
            {"typ": 1, "kachel_x": 4, "kachel_y": 8}]
sortiert = iso.zeichen_reihenfolge(gebaeude)
assert [(g["kachel_x"], g["kachel_y"]) for g in sortiert] == [
    (0, 0), (5, 7), (4, 8)]
assert [g["kachel_x"] for g in gebaeude] == [5, 0, 4]  # Original heil
print("Iso: hinten zuerst, Original-Liste unveraendert")
print("ISO_TESTS_OK")
