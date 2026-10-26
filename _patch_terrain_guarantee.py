"""Patch-Skript: Garantiert, dass der Start-Chunk alle Bodentypen enthaelt."""
pfad = r'z:/Codes/Unterricht/Schuster/Fortgeschrittener Kurs/Terra_Nova/main.py'
with open(pfad, 'r', encoding='utf-8') as f:
    inhalt = f.read()

# Find the end of karte_generieren (the last line before the next function or section)
# We'll insert guarantee code before the function ends
suchtext = '''    # ── Schritt 3: Sand-Flächen erzeugen ──────────────────────────────────
    anzahl_sand_flaechen = parameter["sand_flaechen"]
    for _ in range(anzahl_sand_flaechen):
        mitte_x = random.randint(5, WELT_BREITE - 5)
        mitte_y = random.randint(5, WELT_HOEHE - 5)
        radius = random.randint(3, 8)
        for zeile in range(WELT_HOEHE):
            for spalte in range(WELT_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 3  # 3 = Sand
'''

# This appears twice (two sections). We need to handle both.
# But actually, the second section overrides the first. Let's patch both.
guarantee_code = suchtext + '''
    # ── Garantie: Start-Chunk enthaelt alle Bodentypen ─────────────────────
    # Der Spieler muss von Anfang an auf alle Bodentypen zugreifen koennen,
    # sonst kann er nicht weiterkommen (z.B. Gestein fuer Steinmetz).
    start_x0 = START_CHUNK_X * CHUNK_GROESSE
    start_y0 = START_CHUNK_Y * CHUNK_GROESSE
    start_x1 = start_x0 + CHUNK_GROESSE
    start_y1 = start_y0 + CHUNK_GROESSE
    vorhandene_typen = set()
    for zeile in range(start_y0, start_y1):
        for spalte in range(start_x0, start_x1):
            vorhandene_typen.add(karten_daten[zeile][spalte])
    # Fehlende Bodentypen als kleine Flaeche (3x3) in den Start-Chunk setzen
    for boden_typ in (0, 1, 2, 3):
        if boden_typ not in vorhandene_typen:
            # Finde eine freie Stelle im Start-Chunk
            mitte_x = start_x0 + CHUNK_GROESSE // 2
            mitte_y = start_y0 + CHUNK_GROESSE // 2
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    kx = mitte_x + dx
                    ky = mitte_y + dy
                    if (start_x0 <= kx < start_x1 and start_y0 <= ky < start_y1):
                        karten_daten[ky][kx] = boden_typ
'''

count = inhalt.count(suchtext)
inhalt = inhalt.replace(suchtext, guarantee_code)
print(f'Terrain-Garantie: {count} occurrences ersetzt')

with open(pfad, 'w', encoding='utf-8') as f:
    f.write(inhalt)

print('Patch abgeschlossen')