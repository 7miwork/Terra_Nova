"""Schnelle Konsistenzkontrolle für die aktuelle Stunde-11-Version."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import gebaeude
import ressourcen
import forschung

print('=== GEBAEUDE_TYPEN ===')
for i, daten in enumerate(gebaeude.GEBAEUDE_TYPEN):
    bild = daten.get('bild', '')
    bild_pfad = os.path.join(os.path.dirname(__file__), 'bilder', bild)
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
assert all(os.path.exists(os.path.join(os.path.dirname(__file__), 'bilder', daten['bild']))
           for daten in gebaeude.GEBAEUDE_TYPEN)
print('\nCHECK_OK')
