"""Chunk-System fuer endliche und endlose Welt.

Haltet hier alle Variablen und Funktionen zum Chunk-Besitz, damit main.py,
forschung.py und spielstand.py denselben Zustand nutzen, ohne dass main.py
ein zweites Mal geladen werden muss (kein __import__("main") mehr noetig).
"""

# ═══════════════════════════════════════════════════════════════════════════════════════
# CHUNK-SYSTEM FÜR ENDLOSE WELT
# Die Welt wird in Chunks unterteilt. Jeder Chunk muss einzeln gekauft werden,
# bevor darauf gebaut werden darf. Der mittlere Chunk ist kostenlos.
# Forschung schaltet neue Chunks zum Kauf frei. Kosten steigen mit jedem Kauf.
# ═══════════════════════════════════════════════════════════════════════════════════════
CHUNK_GROESSE = 25                      # Kacheln pro Chunk (Quadratisch)
WELT_CHUNK_BREITE = 8                   # Chunks in X-Richtung (WELT_BREITE / CHUNK_GROESSE)
WELT_CHUNK_HOEHE = 6                    # Chunks in Y-Richtung (WELT_HOEHE / CHUNK_GROESSE)
CHUNK_BASISKOSTEN = {"gold": 150, "stein": 60, "holz": 40}  # Kosten für 1. Chunk
CHUNK_KOSTEN_MULTIPLIKATOR = 1.6        # Jeder weitere Chunk ist teurer
CHUNK_NACHBARN = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

# Zustand — Chunk-Besitz
besitzte_chunks = set()       # Gekaufte Chunks: {(chunk_x, chunk_y), ...}
freigeschaltete_chunks = set()  # Durch Forschung zum Kauf freigegebene Chunks
chunks_gekauft = 0            # Anzahl gekaufter Chunks (für Kostensteigerung)

# Start-Chunk (Mitte der Welt) gehört automatisch zum Besitz
START_CHUNK_X = WELT_CHUNK_BREITE // 2   # 4
START_CHUNK_Y = WELT_CHUNK_HOEHE // 2    # 3
besitzte_chunks.add((START_CHUNK_X, START_CHUNK_Y))


def chunk_fuer_kachel(kachel_x, kachel_y):
    """Berechnet den Chunk für eine Kachelkoordinate."""
    return kachel_x // CHUNK_GROESSE, kachel_y // CHUNK_GROESSE


def kachel_in_besitztem_chunk(kachel_x, kachel_y):
    """Prüft, ob die Kachel in einem bereits besitzten Chunk liegt."""
    cx, cy = chunk_fuer_kachel(kachel_x, kachel_y)
    return (cx, cy) in besitzte_chunks


def chunk_kann_gekauft_werden(chunk_x, chunk_y):
    """Prüft, ob ein Chunk gekauft werden kann.

    Bedingungen:
    1. Noch nicht im Besitz
    2. Durch Forschung freigeschaltet
    3. Benachbart zu einem bereits besitzten Chunk (8-Nachbarschaft)
    """
    if (chunk_x, chunk_y) in besitzte_chunks:
        return False, "Dieser Chunk gehört bereits dir."
    if (chunk_x, chunk_y) not in freigeschaltete_chunks:
        return False, "Dieser Chunk ist noch nicht freigeschaltet."
    for dx, dy in CHUNK_NACHBARN:
        if (chunk_x + dx, chunk_y + dy) in besitzte_chunks:
            return True, ""
    return False, "Dieser Chunk liegt nicht neben deinem Gebiet."


def chunk_kosten_berechnen(chunks_gekauft_anzahl):
    """Berechnet die Kosten für den nächsten Chunk-Kauf.

    Jeder weitere Chunk ist teurer (Multiplikator potenziert mit Kaufanzahl).
    """
    faktor = CHUNK_KOSTEN_MULTIPLIKATOR ** chunks_gekauft_anzahl
    kosten = {}
    for name, basis in CHUNK_BASISKOSTEN.items():
        kosten[name] = max(1, int(basis * faktor))
    return kosten


def chunk_kaufen(chunk_x, chunk_y, ressourcen_dict):
    """Kauft einen Chunk, wenn möglich.

    Gibt (erfolg, meldung) zurück.
    """
    global chunks_gekauft
    kann, grund = chunk_kann_gekauft_werden(chunk_x, chunk_y)
    if not kann:
        return False, grund
    kosten = chunk_kosten_berechnen(chunks_gekauft)
    fehlende = [f"{name}: {menge}" for name, menge in kosten.items()
                if ressourcen_dict.get(name, 0) < menge]
    if fehlende:
        return False, "Rohstoffe fehlen: " + ", ".join(fehlende)
    for name, menge in kosten.items():
        ressourcen_dict[name] -= menge
    besitzte_chunks.add((chunk_x, chunk_y))
    chunks_gekauft += 1
    return True, f"Chunk ({chunk_x}, {chunk_y}) gekauft!"