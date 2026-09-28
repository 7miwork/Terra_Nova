"""Schnelle Konsistenzkontrolle für die aktuelle Stunde-11-Version."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gebaeude
import ressourcen
import forschung
import gegner
import ton
import achievements
import missionen

print('=== GEBAEUDE_TYPEN ===')
for i, daten in enumerate(gebaeude.GEBAEUDE_TYPEN):
    bild = daten.get('bild', '')
    bild_pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bilder', bild)
    print(f"  [{i}] {daten['name']} | {daten['breite']}x{daten['hoehe']} | "
          f"Bild: {bild} ({'vorhanden' if os.path.exists(bild_pfad) else 'FEHLT'})")

print('\n=== GEBAEUDE_WIRTSCHAFT ===')
for i, wirtschaft in enumerate(ressourcen.GEBAEUDE_WIRTSCHAFT):
    print(f"  [{i}] {ressourcen._gebaeude_name_fuer_index(i)} | {wirtschaft}")

print('\n=== KATEGORIEN ===')
for taste, kategorie in gebaeude.GEBAEUDE_KATEGORIEN.items():
    namen = [gebaeude.GEBAEUDE_TYPEN[i]['name'] for i in kategorie['typen']]
    print(f"  [{taste}] {kategorie['name']}: {', '.join(namen)}")

print('\n=== TECHNOLOGIEN ===')
for i, technologie in enumerate(forschung.TECHNOLOGIEN):
    print(f"  [{i}] {technologie['id']} | {technologie['name']} | "
          f"{technologie['kategorie']} | {technologie['kosten']} Punkte | {technologie['zeit']} Ticks")

assert len(gebaeude.GEBAEUDE_TYPEN) == len(ressourcen.GEBAEUDE_WIRTSCHAFT)
assert all(os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bilder', daten['bild']))
           for daten in gebaeude.GEBAEUDE_TYPEN)

print('\n=== GEGNER UND VERTEIDIGUNG (Phase 4) ===')
# Automat: Feste Werte aus der Aufgabe.
assert gegner.FRIEDENSZEIT_TICKS == 150
assert gegner.ANGRIFFS_INTERVALL == (100, 160)
assert gegner.WARNZEIT_TICKS == 25
assert gegner.BANNER_TICKS == 6
assert gegner.PLUENDERUNG_ANTEIL == 0.30
assert gegner.VERLUST_ANTEIL == 0.2
assert gegner.angriffsstaerke(10, 3) == 21.0          # 6 + 12 + 3
assert gegner.verteidigungsstaerke({}, []) == 0.0
# Die sechs geschuetzten Werte duerfen NIE in der Pluenderungsliste stehen.
_geschuetzt = {"bevoelkerung", "forschung", "roboter",
               "zufriedenheit", "verteidiger", "raumschiffe"}
assert not (_geschuetzt & set(gegner.PLUENDERUNG_RESSOURCEN))
assert gegner.regelwerk_gegner_aktiv(None) is True
assert gegner.regelwerk_gegner_aktiv({"gegner_aktiv": False}) is False

print('\n=== MILITAER-RESSOURCEN UND -GEBaeude ===')
for _name in ("verteidiger", "raumschiffe"):
    assert _name in ressourcen.RESSOURCEN_NAMEN, _name
    assert _name in ressourcen.SPEICHER_BASIS, _name
assert len(ressourcen.GEBAEUDE_ZUFRIEDENHEIT) == len(ressourcen.GEBAEUDE_WIRTSCHAFT)
assert ressourcen.MAX_VERTEIDIGER_ANTEIL == 0.30
# Kategorie 9 "Spezial / Verteidigung" enthaelt alle sechs Militaergebaeude.
_kat9 = gebaeude.GEBAEUDE_KATEGORIEN['9']
assert set(_kat9['typen']) >= {17, 19, 20, 21, 22, 23}, _kat9
print(f"  [9] {_kat9['name']}: {_kat9['typen']}")

print('\n=== MILITAER-TECHNOLOGIEN ===')
_ids = {t['id'] for t in forschung.TECHNOLOGIEN}
for _tid in ("militaertraining", "raumschiffbau", "laserverteidigung", "schutzschilde"):
    assert _tid in _ids, _tid
    print(f"  OK {_tid}")
for _typ in (21, 22, 23):
    _frei = ressourcen.GEBAEUDE_WIRTSCHAFT[_typ].get("freischaltung", {})
    if _frei.get("typ") == "forschung":
        assert _frei.get("technologie") in _ids, (_typ, _frei)

print('\n=== SOUNDS UND BILDER (Phase 4) ===')
for _ereignis in ("angriff_warnung", "abwehr_erfolg", "ausgeraubt"):
    _pfad = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sounds", ton.SOUNDS[_ereignis])
    assert os.path.exists(_pfad), _pfad
    print(f"  OK {_ereignis} -> {ton.SOUNDS[_ereignis]}")
for _bild in ("kaserne.png", "raumschiffwerft.png", "laserturm.png"):
    assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bilder", _bild)), _bild
    print(f"  OK bilder/{_bild}")

print('\n=== ACHIEVEMENTS UND MISSION (Phase 4) ===')
_ach_ids = {e['id'] for e in achievements.ACHIEVEMENTS}
assert {"erste_abwehr", "festung", "flotte"} <= _ach_ids
assert len(achievements.ACHIEVEMENTS) <= 39   # Anzeige: 3 Spalten a 13 Zeilen
assert any(m['id'] == "kaserne_bauen" for m in missionen.MISSIONEN)
assert len(missionen.MISSIONEN) <= 24         # Anzeige: 3 Spalten a 8 Zeilen
print(f"  {len(achievements.ACHIEVEMENTS)} Achievements, "
      f"{len(missionen.MISSIONEN)} Missionen — passen ins Menü")

print('\n=== SCHWEBENDE FENSTER UND HUD ===')
import hud
import panel
for _name in ("frame_start", "zeichnen", "maus_ereignis", "panel_rect",
              "titel_rect", "knopf_rechtecke", "umschalten", "verschieben",
              "minimieren_setzen", "zustand_zuruecksetzen"):
    assert hasattr(panel, _name), f"panel.{_name} fehlt"
assert panel.TITEL_HOEHE == 22 and panel.RAND_FENSTER == 4
assert hud.HUD_HOEHE == 82 and hud._RESSOURCEN_SPALTEN == 6
assert hasattr(hud, "ressourcen_leiste_layout") and hasattr(hud, "_letztes_layout")
# Verdrahtung: jedes Fenster zeichnet genau ein Modul, alle Mauspfade sind da
_quellen = {}
for _datei in ("main.py", "hud.py", "gegner.py"):
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), _datei), encoding="utf-8") as _f:
        _quellen[_datei] = _f.read()
for _datei, _muss in (("hud.py", 'panel.zeichnen("uebersicht"'),
                      ("hud.py", 'panel.zeichnen("bauinfo"'),
                      ("gegner.py", 'panel.zeichnen("verteidigung"'),
                      ("main.py", 'panel.zeichnen("ziel"'),
                      ("main.py", "panel.frame_start()"),
                      ("main.py", "panel.maus_ereignis(ereignis)"),
                      ("main.py", "panels_anordnen()")):
    assert _muss in _quellen[_datei], f"{_datei}: {_muss}"
print("  OK 4 Fenster, Maus-/Klick-Pfad und Leisten-Layout verdrahtet")

print('\nCHECK_OK')
