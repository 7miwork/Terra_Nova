"""
=============================================================================
MODUL: hud.py  —  Terra_Nova  (Stunde 4 + 5 + 6)
=============================================================================

Was ist ein HUD?
    HUD steht für "Heads-Up Display". Das ist die Anzeige am oberen Bildschirmrand,
    die wichtige Informationen zeigt — wie im Cockpit eines Raumschiffs oder in
    Final Earth 2. Informationen die du immer im Blick haben willst!

Aufgabe dieses Moduls:
    Alles was auf dem Bildschirm angezeigt wird (außer die Karte und Gebäude):
    - Ressourcen-Anzeige: Gold, Energie, Holz, Stein (NEU in St. 6)
    - Ausgewählter Gebäude-Typ (welches Gebäude wir bauen wollen)
    - Kameraposition und Steuerungshinweise
    - Baukosten des ausgewählten Gebäudes

Konzepte in dieser Datei:
    ✓ Dictionary — Ressourcen als Schlüssel-Wert-Paare
    ✓ Texte zeichnen mit pygame.font.Font und render()
    ✓ Funktionen mit mehreren Parametern
    ✓ Modul-Variablen für gemeinsamen Zustand

Stunde 4 — Was der Spieler gelernt hat:
    ✓ Ressourcen als Dictionary speichern (Gold, Energie, Holz)
    ✓ HUD am oberen Bildschirmrand zeichnen
    ✓ Mehrere Informationen auf dem Bildschirm anzeigen
    ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2)

Stunde 5 — NEU dazu:
    ✓ Baukosten-Anzeige: Zeigt was das ausgewählte Gebäude kostet
    ✓ Neuer Parameter gebaeude_wirtschaft in hud_zeichnen()

Stunde 6 — NEU dazu:
    ✓ Vierter Rohstoff: Stein (wird in der Ressourcen-Leiste angezeigt)
    ✓ Ressourcen-Leiste zeigt jetzt 4 statt 3 Werte

Stunde 7 — NEU dazu:
    ✓ Fünfter Rohstoff: Bevölkerung (wird in der Ressourcen-Leiste angezeigt)
    ✓ Ressourcen-Leiste zeigt jetzt 5 statt 4 Werte

Stunde 9 — NEU dazu:
    ✓ Bei der Gebäude-Auswahl werden jetzt auch Produktion und Verbrauch
      angezeigt (nicht nur die Baukosten) — das Kästchen ist höher
    ✓ Tooltip beim Hovern über ein Ressourcen-Icon: zeigt welche Gebäude
      diese Ressource produzieren/verbrauchen
    ✓ Meldungssystem: hud.meldung_anzeigen(text) zeigt eine auffällige rote
      Meldung am oberen Rand, z.B. "Nicht genug Rohstoffe für ..."
=============================================================================
"""

import pygame


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: MODUL-VARIABLEN
# ═════════════════════════════════════════════════════════════════════════════
# Diese Variablen gehören zum hud-Modul.
# Sie werden einmalig durch hud_initialisieren() gesetzt.
# ═════════════════════════════════════════════════════════════════════════════

_fenster = None   # Das Pygame-Fenster (wird von main.py übergeben)
_font_cache = {}


def _font(groesse):
    """Liefert eine wiederverwendbare Schrift statt sie pro Frame zu erzeugen."""
    if groesse not in _font_cache:
        _font_cache[groesse] = pygame.font.Font(None, groesse)
    return _font_cache[groesse]

# ── Meldungs-System — NEU in Stunde 9 ───────────────────────────────────────
# Die Schüler haben sich gewünscht: Wenn nicht genug Rohstoffe zum Bauen da
# sind, soll man das auch IM SPIEL sehen — nicht nur in der Konsole!
# Wir speichern den Text und einen Timer (Anzahl Frames, die er angezeigt wird).
# 120 Frames = 2 Sekunden bei 60 FPS.
_meldung_text  = ""      # Der anzuzeigende Text (leer = keine Meldung)
_meldung_timer = 0       # Wie viele Frames die Meldung noch sichtbar ist


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════

def hud_initialisieren(fenster_obj):
    """
    Übergibt die Referenz auf das Pygame-Fenster.
    Muss einmalig in main.py aufgerufen werden bevor das HUD gezeichnet wird.
    
    Parameter:
        fenster_obj — das Pygame-Surface (fenster aus main.py)
    """
    global _fenster
    _fenster = fenster_obj


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: MELDUNGEN — NEU in Stunde 9
# ═════════════════════════════════════════════════════════════════════════════
# Ein kleines Meldungssystem, damit wichtige Hinweise IM SPIEL erscheinen
# (Verbesserungsvorschlag 5). z.B. "Nicht genug Rohstoffe fuer ..."
# ═════════════════════════════════════════════════════════════════════════════

def meldung_anzeigen(text):
    """
    Zeigt eine Meldung am oberen Bildschirmrand (für 2 Sekunden).

    Diese Funktion wird von außen (main.py) aufgerufen, wenn etwas schiefgeht
    und der Spieler es sehen soll — z.B. wenn nicht genug Rohstoffe da sind.

    Wir setzen nur zwei Modul-Variablen:
        _meldung_text  = der Text
        _meldung_timer = 120  (Frames) → bei 60 FPS = 2 Sekunden

    Das eigentliche Zeichnen + Herunterzählen passiert in hud_zeichnen().
    """
    global _meldung_text, _meldung_timer

    _meldung_text  = text
    _meldung_timer = 120   # 2 Sekunden bei 60 FPS


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: RESSOURCEN-ANZEIGE
# ═════════════════════════════════════════════════════════════════════════════
# Zeichnet oben am Bildschirm die aktuellen Ressourcen.
# Jede Ressource hat einen Namen, eine Farbe (als Icon) und einen Wert.
#
    # In final Earth 2 werden alle wichtigen Ressourcen oben angezeigt.
    #
    # Neu in Stunde 6: Vierter Rohstoff "Stein" (grau) kommt dazu!
    #
    # Neu in Stunde 7: Fünfter Rohstoff "Bevölkerung" (rosa) kommt dazu!
# ═════════════════════════════════════════════════════════════════════════════

def _ressourcen_leiste_zeichnen(ressourcen, maus_pos=None, gebaeude_wirtschaft=None,
                                 ressourcen_limits=None):

    """
    Zeichnet die Ressourcen-Leiste oben am Bildschirm.
    
    Was ist eine Ressourcen-Leiste?
        In Final Earth 2 siehst du oben immer wie viel Gold, Energie, Holz und
        Stein du hast. Das ist wichtig für die Planung:
        - Hast du genug Gold für ein neues Gebäude?
        - Reicht die Energie für alle Gebäude?
        - Produzieren die Holzfäller genug Holz?
        - Liefern die Steinmetze genug Stein?
        
    Die Leiste zeigt:
        - Ein farbiges Icon (Kreis) für jede Ressource
        - Den Namen der Ressource
        - Den aktuellen Wert
    
    Neu in Stunde 6: Stein als vierte Ressource!
    Neu in Stunde 9: Wenn die Maus über einem Icon schwebt (Hover), erscheint
        ein Tooltip darunter — mit den Gebäuden, die diese Ressource
        produzieren oder verbrauchen (Verbesserungsvorschlag 4).
    
    Parameter:
        ressourcen           — Dictionary mit den aktuellen Ressourcen-Werten
        maus_pos             — aktuelle Mausposition (x, y) oder None
        gebaeude_wirtschaft  — Wirtschaftsdaten (aus ressourcen.py) für den Tooltip
    """
    if _fenster is None:
        return   # Noch nicht initialisiert
    
    # Schriftart für die Ressourcen-Anzeige (Größe 24 Pixel)
    schrift = _font(24)
    
    # ── Ressourcen definieren ─────────────────────────────────────────────
    # Jede Ressource hat:
    #   - "name": Anzeige-Name
    #   - "farbe": Farbe für das Icon (Kreis)
    #   - "schluessel": Schlüssel im ressourcen-Dictionary
    #
    # Neu in Stunde 6: Index 3 = Stein (grau)
    ressourcen_typen = [
        {
            "name":     "Gold",
            "farbe":    (255, 215, 0),      # Gold-Gelb
            "icon_pos": (20, 15),            # Position des Kreises
            "text_pos": (35, 12),            # Position des Textes
            "schluessel": "gold",
        },
        {
            "name":     "Energie",
            "farbe":    (255, 200, 50),      # Gelb-Orange
            "icon_pos": (130, 15),           # Leicht verschoben (mehr Platz)
            "text_pos": (145, 12),
            "schluessel": "energie",
        },
        {
            "name":     "Holz",
            "farbe":    (139, 90, 43),       # Braun (Holz-Farbe)
            "icon_pos": (260, 15),
            "text_pos": (275, 12),
            "schluessel": "holz",
        },
        # ── Index 3: Stein — NEU in Stunde 6 ──────────────────────────────
        {
            "name":     "Stein",
            "farbe":    (150, 150, 160),     # Hellgrau — Stein-Farbe
            "icon_pos": (370, 15),
            "text_pos": (385, 12),
            "schluessel": "stein",
        },
        # ── Index 4: Bevölkerung — NEU in Stunde 7 ──────────────────────────
        # Die vierte Ressource! Wohnhäuser produzieren Bevölkerung.
        {
            "name":     "Bevoelkerung",
            "farbe":    (255, 180, 200),     # Rosa — Menschen-Farbe
            "icon_pos": (480, 15),
            "text_pos": (495, 12),
            "schluessel": "bevoelkerung",
        },
        # ── Index 5: Nahrung — NEU in Stunde 8 ──────────────────────────────
        # Farmen produzieren Nahrung für die Bevölkerung.
        {
            "name":     "Nahrung",
            "farbe":    (255, 140, 0),       # Orange — Essen-Farbe
            "icon_pos": (620, 15),
            "text_pos": (635, 12),
            "schluessel": "nahrung",
        },
        # ── Index 6: Forschung — NEU in Stunde 10 ─────────────────────────────
        # Das Labor produziert Forschungspunkte für neue Technologien.
        {
                        "name":     "Forschung",

            "farbe":    (120, 220, 255),     # Hellblau — Wissenschaft
            "icon_pos": (740, 15),
            "text_pos": (755, 12),
            "schluessel": "forschung",
        },
        {
            "name":     "Kohle",
            "farbe":    (50, 50, 55),
            "icon_pos": (845, 15),
            "text_pos": (860, 12),
            "schluessel": "kohle",
        },
                {
            "name":     "Eisen",
            "farbe":    (190, 120, 90),
            "icon_pos": (935, 15),
            "text_pos": (950, 12),
            "schluessel": "eisen",
        },
                {
            "name":    "Roboter",
            "farbe":    (100, 220, 220),
            "icon_pos": (935, 47),
            "text_pos": (950, 44),
            "schluessel": "roboter",
        },
        {
            "name":    "Stahl",
            "farbe":    (210, 215, 225),
            "icon_pos": (935, 79),
            "text_pos": (950, 76),
            "schluessel": "stahl",
        },
        {
            "name":    "Zufriedenheit",
            "farbe":    (170, 220, 255),
            "icon_pos": (935, 111),
            "text_pos": (950, 108),
            "schluessel": "zufriedenheit",
        },

    ]

    # Elf Ressourcen werden auf sechs Spalten und zwei Reihen verteilt.
    # So bleibt auch Stahl im 1000-Pixel-Fenster lesbar.
    for index, res in enumerate(ressourcen_typen):
        if index < 6:
            spalte, zeile = index, 0
        else:
            spalte, zeile = index - 6, 1
        x = 18 + spalte * 162
        y = 15 + zeile * 32
        res["icon_pos"] = (x, y)
        res["text_pos"] = (x + 15, y - 3)
    
    # ── Hintergrund für die Leiste zeichnen ──────────────────────────────

    # Dunkler Balken oben über die volle Breite
    hintergrund_hoehe = 82

    hintergrund_rect = pygame.Rect(0, 0, _fenster.get_width(), hintergrund_hoehe)
    pygame.draw.rect(_fenster, (20, 20, 30), hintergrund_rect)   # Dunkelblau-Schwarz
    pygame.draw.rect(_fenster, (60, 60, 80), hintergrund_rect, 2)   # Hellerer Rahmen
    
    # ── Jede Ressource zeichnen ──────────────────────────────────────────
    for res in ressourcen_typen:
        # Kreis (Icon) zeichnen
        pygame.draw.circle(_fenster, res["farbe"], res["icon_pos"], 10)
        pygame.draw.circle(_fenster, (255, 255, 255), res["icon_pos"], 10, 1)   # Weißer Rahmen
        
        # Wert aus dem Dictionary lesen
        wert = ressourcen.get(res["schluessel"], 0)
        
        # Zufriedenheit ist die einzige Ressource, die auch negativ werden
        # darf. Das Pluszeichen macht positive Werte direkt erkennbar.
        if res["schluessel"] == "zufriedenheit":
            wert_anzeige = f"{float(wert):+.0f}"
        else:
            wert_anzeige = f"{wert:.0f}" if isinstance(wert, float) else str(wert)

        if ressourcen_limits and res["schluessel"] in ressourcen_limits:
            wert_anzeige += f"/{ressourcen_limits[res['schluessel']]:.0f}"
        text = schrift.render(f"{res['name']}: {wert_anzeige}", True, (255, 255, 255))

        _fenster.blit(text, res["text_pos"])

    # ── TOOLTIP beim Hovern über einem Icon — NEU in Stunde 9 ────────────────
    # Verbesserungsvorschlag 4: Wenn die Maus über einem Ressourcen-Icon
    # schwebt, zeigen wir eine kleine Box darunter. Darin steht, welche
    # Gebäude diese Ressource produzieren bzw. verbrauchen.
    if maus_pos is not None and gebaeude_wirtschaft is not None:
        maus_x, maus_y = maus_pos

        for res in ressourcen_typen:
            # Abstand zwischen Mauszeiger und Icon-Mittelpunkt
            icon_x, icon_y = res["icon_pos"]
            abstand_x = maus_x - icon_x
            abstand_y = maus_y - icon_y
            abstand = (abstand_x ** 2 + abstand_y ** 2) ** 0.5

            # Radius des Icons ist 10 — liegt die Maus darauf?
            if abstand <= 12:   # Etwas großzügiger für einfacheres Treffen
                _ressourcen_tooltip_zeichnen(
                    res, icon_x, icon_y, gebaeude_wirtschaft)
                break   # Nur EIN Tooltip gleichzeitig


def _ressourcen_tooltip_zeichnen(res, icon_x, icon_y, gebaeude_wirtschaft):
    """
    Zeichnet den kleinen Info-Tooltip unter einem Ressourcen-Icon.

    Der Tooltip zeigt welche Gebäude diese Ressource produzieren (+) und
    welche sie verbrauchen (−). Dazu brauchen wir die Wirtschaftsdaten.

    Damit wir keine Import-Zirkel erzeugen (hud → gebaeude → …) nutzen wir
    hier eine eigene kleine Namensliste — genau wie in ressourcen.py.
    """
    # Gebäude-Namen parallel zu den Indizes in GEBAEUDE_WIRTSCHAFT
    gebaeude_namen = ["Basis", "Reaktor", "Farm", "Holzfaeller",
                      "Steinmetz", "Marktplatz", "Wohnhaus", "Universitaet",
                      "Mine", "Strasse", "Fusionsreaktor", "Roboterfabrik",
                      "Stahlwerk", "Gewaechshaus", "Lagerhaus", "Wohnblock",
                      "Handelsposten", "Koloniezentrum", "Eisenmine", "Park",
                      "Solarreaktor"]

    # Sammle Gebäude, die diese Ressource PRODUZIEREN (+) bzw VERBRAUCHEN (−)
    produzenten = []
    verbraucher = []

    # Gehe alle Gebäude durch (Index = Position in der Liste)
    for i, wirtschaft in enumerate(gebaeude_wirtschaft):
        name = gebaeude_namen[i] if i < len(gebaeude_namen) else "?"
        ress_schluessel = res["schluessel"]

        # Produziert dieses Gebäude die Ressource?
        if ress_schluessel in wirtschaft.get("produktion", {}):
            produzenten.append(name)

        # Verbraucht dieses Gebäude die Ressource?
        if ress_schluessel in wirtschaft.get("verbrauch", {}):
            verbraucher.append(name)

    # Tooltip-Zeilen zusammenbauen (einfach lesbare deutsche Sätze)
    zeilen = []
    zeilen.append(f"{res['name']}:")
    if produzenten:
        zeilen.append("Produziert: " + ", ".join(produzenten))
    if verbraucher:
        zeilen.append("Verbraucht: " + ", ".join(verbraucher))
    if not produzenten and not verbraucher:
        zeilen.append("Nur Startwert (kein Gebaeude)")

    # Kleine Schrift für den Tooltip
    schrift_klein = _font(18)

    # ── Breite & Höhe der Tooltip-Box ausrechnen ───────────────────────────
    text_surfaces = []
    maximale_breite = 0
    for zeile in zeilen:
        surface = schrift_klein.render(zeile, True, (255, 255, 255))
        text_surfaces.append(surface)
        if surface.get_width() > maximale_breite:
            maximale_breite = surface.get_width()

    padding = 8
    box_breite = maximale_breite + 2 * padding
    box_hoehe  = len(zeilen) * 20 + 2 * padding

    # Box unter dem Icon platzieren (kleiner Abstand 5 Pixel)
    box_x = icon_x - box_breite // 2
    box_y = icon_y + 17

    # Damit die Box nicht über den rechten Bildschirmrand ragt
    if box_x < 0:
        box_x = 0
    if box_x + box_breite > _fenster.get_width():
        box_x = _fenster.get_width() - box_breite

    # ── Box zeichnen (dunkel, mit Rahmen) ──────────────────────────────────
    box_rect = pygame.Rect(box_x, box_y, box_breite, box_hoehe)
    pygame.draw.rect(_fenster, (10, 10, 20), box_rect)
    pygame.draw.rect(_fenster, res["farbe"], box_rect, 2)   # Rahmen in Ressourcen-Farbe

    # ── Textzeilen zeichnen ────────────────────────────────────────────────
    text_y = box_y + padding
    for surface in text_surfaces:
        _fenster.blit(surface, (box_x + padding, text_y))
        text_y += 20


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEBÄUDE-AUSWAHL ANZEIGE + BAUKOSTEN
# ═════════════════════════════════════════════════════════════════════════════
# Zeigt welches Gebäude gerade ausgewählt ist — und was es kostet.
# In Final Earth 2 siehst du bevor du baust, was das Gebäude kostet.
# ═════════════════════════════════════════════════════════════════════════════

def _gebaeude_auswahl_zeichnen(gebaeude_auswahl, gebaeude_typen,
                                gebaeude_wirtschaft, baukosten_funktion=None,
                                kategorie_name="", kategorie_position=0,
                                bild_funktion=None):

    """
    Zeigt den aktuell ausgewählten Gebäude-Typ an — mit Baukosten.
    
    Wie in Final Earth 2:
        Unten siehst du welches Gebäude du gerade baust und was es kostet.
        Mit Tasten 1/2/3/4/5 kannst du zwischen den Typen wechseln.
    
    Neu in Stunde 6: Auch Holzfäller und Steinmetz werden angezeigt.
    Die Baukosten-Liste zeigt jetzt auch Stein, falls nötig.
    
    Parameter:
        gebaeude_auswahl   — Index des aktuell ausgewählten Gebäude-Typs
        gebaeude_typen     — Liste mit allen Gebäude-Typen (aus gebaeude.py)
        gebaeude_wirtschaft — Liste mit Wirtschaftsdaten (aus ressourcen.py)
    """
    if _fenster is None:
        return   # Noch nicht initialisiert
    
    # Sicherstellen dass der Index gültig ist
    if gebaeude_auswahl < 0 or gebaeude_auswahl >= len(gebaeude_typen):
        return
    
    schrift = _font(24)
    schrift_klein = _font(18)  # Kleinere Schrift für Kosten
    
    # ── Gebäude-Daten holen ──────────────────────────────────────────────
    gebaeude_daten = gebaeude_typen[gebaeude_auswahl]
    name = gebaeude_daten["name"]
    farbe = gebaeude_daten["farbe"]
    kuerzel = gebaeude_daten["kuerzel"]
    
    # ── Baukosten-Text erstellen ─────────────────────────────────────────
    # Aus den Wirtschaftsdaten die Baukosten für dieses Gebäude holen
    # gebaeude_wirtschaft ist eine Liste parallel zu gebaeude_typen
    if gebaeude_wirtschaft is not None and gebaeude_auswahl < len(gebaeude_wirtschaft):
        wirtschaft = gebaeude_wirtschaft[gebaeude_auswahl]
        baukosten = (baukosten_funktion(gebaeude_auswahl)
                     if baukosten_funktion is not None
                     else wirtschaft["baukosten"])

    else:
        baukosten = {}
    
    # Baukosten als lesbaren String formatieren
    # z.B. "Kosten: 20 Gold" oder "Kosten: 15 Gold + 10 Energie"
    if baukosten:
        # Dictionary in lesbare Form umwandeln
        kosten_teile = []
        for ress_name, menge in baukosten.items():
            # Ressourcen-Namen schön schreiben
            if ress_name == "gold":
                kosten_teile.append(f"{menge} Gold")
            elif ress_name == "energie":
                kosten_teile.append(f"{menge} Energie")
            elif ress_name == "holz":
                kosten_teile.append(f"{menge} Holz")
            elif ress_name == "stein":
                kosten_teile.append(f"{menge} Stein")
            elif ress_name == "nahrung":
                kosten_teile.append(f"{menge} Nahrung")
            else:
                kosten_teile.append(f"{menge} {ress_name}")
        kosten_string = " + ".join(kosten_teile)
        kosten_text_string = f"Kosten: {kosten_string}"
    else:
        # Keine Baukosten (z.B. bei der Basis) → "Kostenlos!"
        kosten_text_string = "Kostenlos!"
    
    # ── Haupt-Text erstellen: "Ausgewählt: Reaktor (Taste 2)" ──────────
    taste = gebaeude_daten.get("taste", str(gebaeude_auswahl + 1))
    breite = gebaeude_daten.get("breite", 1)
    hoehe = gebaeude_daten.get("hoehe", 1)
    if kategorie_name:
        text_string = (f"{kategorie_name} [{kategorie_position + 1}] | "
                       f"Ausgewaehlt: {name} ({breite}x{hoehe} Kacheln, Taste {taste})")
    else:
        text_string = f"Ausgewaehlt: {name} ({breite}x{hoehe} Kacheln, Taste {taste})"

    text = schrift.render(text_string, True, (255, 255, 255))
    
    # ── Kosten-Text ───────────────────────────────────────────────────────
    kosten_text = schrift_klein.render(kosten_text_string, True, (200, 200, 200))

    # ── Produktion & Verbrauch — NEU in Stunde 9 ───────────────────────────
    # Verbesserungsvorschlag 2: Der Spieler soll auch sehen, was ein Gebäude
    # produziert und was es verbraucht — nicht nur die Baukosten.
    #   z.B. Produziert: +5 Energie   /   Verbraucht: -2 Holz
    if gebaeude_wirtschaft is not None and gebaeude_auswahl < len(gebaeude_wirtschaft):
        wirtschaft = gebaeude_wirtschaft[gebaeude_auswahl]
        produktion = wirtschaft.get("produktion", {})
        verbrauch  = wirtschaft.get("verbrauch", {})
    else:
        produktion = {}
        verbrauch  = {}

    # Produktion als lesbaren String formatieren (z.B. "+5 Energie")
    if produktion:
        prod_teile = []
        for ress_name, menge in produktion.items():
            prod_teile.append(f"+{menge} {_ressourcen_name(ress_name)}")
        produktion_text = "Produziert: " + ", ".join(prod_teile)
    else:
        produktion_text = "Produziert: nichts"

    # Verbrauch als lesbaren String formatieren (z.B. "-2 Holz")
    if verbrauch:
        verb_teile = []
        for ress_name, menge in verbrauch.items():
            verb_teile.append(f"-{menge} {_ressourcen_name(ress_name)}")
        verbrauch_text = "Verbraucht: " + ", ".join(verb_teile)
    else:
        verbrauch_text = "Verbraucht: nichts"

    # Personalbedarf sichtbar machen.
    personalbedarf = wirtschaft.get("personalbedarf", 0) if gebaeude_wirtschaft else 0
    personal_text = f"Personalbedarf: {personalbedarf}" if personalbedarf else "Personalbedarf: keiner"
    personal_surface = schrift_klein.render(personal_text, True, (220, 205, 130))

    # Die Texte vorher als Grafiken rendern (für die Breiten-Berechnung)
    produktion_surface = schrift_klein.render(produktion_text, True, (120, 220, 120))
    verbrauch_surface  = schrift_klein.render(verbrauch_text, True, (220, 120, 120))

    # ── Breite des Hintergrunds an den breiteren Text anpassen ───────────

    # (entweder Haupttext oder Kosten-Text, je nachdem was breiter ist)
    maximal_breite = max(text.get_width(), kosten_text.get_width(),
                         produktion_surface.get_width(), verbrauch_surface.get_width(),
                         personal_surface.get_width())

    hintergrund_padding = 10
    
    # Position: Mitte unten am Bildschirm
    mitte_x = _fenster.get_width() // 2
    
    # Hintergrund-Rechteck (breit genug für alle Texte)
    hintergrund_breite = maximal_breite + 2 * hintergrund_padding + 58  # Platz für Bildvorschau

    # NEU in Stunde 9: Höher, weil jetzt 4 Zeilen drinstehen:
    # Haupttext + Kosten + Produktion + Verbrauch
    hintergrund_hoehe = 152
    hintergrund_y = _fenster.get_height() - 160

    hintergrund_x = mitte_x - hintergrund_breite // 2
    
    hintergrund_rect = pygame.Rect(
        hintergrund_x, hintergrund_y,
        hintergrund_breite, hintergrund_hoehe,
    )
    pygame.draw.rect(_fenster, (20, 20, 30, 200), hintergrund_rect)   # Halb-transparent
    pygame.draw.rect(_fenster, farbe, hintergrund_rect, 2)   # Rahmen in Gebäude-Farbe
    
    # ── Haupttext zeichnen (oben im Hintergrund) ─────────────────────────
    text_x = hintergrund_x + hintergrund_padding + 50  # Platz für Bildvorschau

    text_y = hintergrund_y + 8
    _fenster.blit(text, (text_x, text_y))
    
    # ── Kosten-Text zeichnen (darunter, kleinere Schrift) ────────────────
    kosten_y = text_y + 24
    _fenster.blit(kosten_text, (text_x, kosten_y))

    # ── Produktion-Text (grün) — NEU in Stunde 9 ─────────────────────────
    produktion_y = kosten_y + 22
    _fenster.blit(produktion_surface, (text_x, produktion_y))

    # ── Verbrauch-Text (rot) — NEU in Stunde 9 ───────────────────────────
    verbrauch_y = produktion_y + 22
    _fenster.blit(verbrauch_surface, (text_x, verbrauch_y))
    
    # ── Personalbedarf zeichnen ───────────────────────────────────────────
    personal_y = verbrauch_y + 22
    _fenster.blit(personal_surface, (text_x, personal_y))

    # ── Bildvorschau links im Hintergrund zeichnen ───────────────────────
    # Kinder sehen dadurch sofort, welches Gebäude sie gerade ausgewählt haben.
    icon_groesse = 42
    icon_x = hintergrund_x + hintergrund_padding
    icon_y = hintergrund_y + (hintergrund_hoehe - icon_groesse) // 2
    icon_rect = pygame.Rect(icon_x, icon_y, icon_groesse, icon_groesse)
    bild = bild_funktion(gebaeude_auswahl, (icon_groesse, icon_groesse)) if bild_funktion else None
    if bild is not None:
        _fenster.blit(bild, icon_rect)
    else:
        pygame.draw.rect(_fenster, farbe, icon_rect)
        kuerzel_text = schrift_klein.render(kuerzel, True, (20, 20, 20))
        _fenster.blit(kuerzel_text, kuerzel_text.get_rect(center=icon_rect.center))
    pygame.draw.rect(_fenster, (255, 255, 255), icon_rect, 1)


def _ressourcen_name(ress_name):
    """
    Kleine Hilfsfunktion — macht aus einem Ressourcen-Schlüssel einen
    schönen deutschen Anzeige-Namen (z.B. "bevoelkerung" → "Bevoelkerung").
    Wird für die Produktions-/Verbrauchs-Anzeige (Stunde 9) genutzt.
    """
    namen = {
        "gold":          "Gold",
        "energie":       "Energie",
        "holz":          "Holz",
        "stein":         "Stein",
        "bevoelkerung":  "Bevoelkerung",
        "nahrung":       "Nahrung",
        "forschung":     "Forschungspunkte",
        "kohle":         "Kohle",
        "eisen":         "Eisen",
        "roboter":       "Roboter",
        "zufriedenheit": "Zufriedenheit",
    }

    # get() mit Standardwert: falls ein neuer Schlüssel dazukommt
    return namen.get(ress_name, ress_name)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: KAMERA- UND STEUERUNGS-INFORMATIONEN
# ═════════════════════════════════════════════════════════════════════════════
# Zeigt Kameraposition und Bedienhinweise — vom Info-Text aus main.py übernommen.
# ═════════════════════════════════════════════════════════════════════════════

def _kamera_info_zeichnen(kamera_x, kamera_y, karte_breite, karte_hoehe, 
                          kachel_groesse, bild_breite, bild_hoehe):
    """
    Zeigt Kameraposition und Steuerungshinweise an.
    
    Wie in Final Earth 2 siehst du Informationen:
    - Wo bist du gerade auf der Karte? (Kameraposition)
    - Wie bedienst du das Spiel? (Steuerung)
    - Was bedeuten die Farben? (Legende der Bodentypen)
    
    Parameter:
        kamera_x      — aktuelle Kamera-x-Position (aus main.py)
        kamera_y      — aktuelle Kamera-y-Position (aus main.py)
        karte_breite  — Breite der Karte in Kacheln
        karte_hoehe   — Höhe der Karte in Kacheln
        kachel_groesse — Größe einer Kachel in Pixeln
        bild_breite   — Breite des Fensters in Pixeln
        bild_hoehe    — Höhe des Fensters in Pixeln
    """
    if _fenster is None:
        return   # Noch nicht initialisiert
    
    schrift = _font(20)
    
    # ── Kameraposition ──────────────────────────────────────────────────
    # Welche Kachel sehen wir gerade in der oberen linken Ecke?
    kachel_x = max(0, kamera_x // kachel_groesse)
    kachel_y = max(0, kamera_y // kachel_groesse)
    
    kamera_info = schrift.render(
        f"Kamera: Kachel ({kachel_x}, {kachel_y})  |  x={kamera_x}  y={kamera_y}",
        True, (220, 220, 220)
    )
    _fenster.blit(kamera_info, (15, 94))

    # ── Karten-Größe und Steuerung ──────────────────────────────────────
    steuerung_info = schrift.render(
        f"Karte: {karte_breite} x {karte_hoehe} Kacheln  |  "
        f"Pfeiltasten scrollen  |  P / ESC = Pause",

        True, (150, 150, 160)
    )
    _fenster.blit(steuerung_info, (15, 119))

    # ── Legende der Bodentypen ───────────────────────────────────────────
    legende_text = schrift.render(
        "Boden:  Erde  |  Gras  |  Gestein  |  Sand",
        True, (150, 150, 160)
    )
    _fenster.blit(legende_text, (15, 144))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HUD ZEICHNEN (HAUPTFUNKTION)
# ═════════════════════════════════════════════════════════════════════════════
# Diese Funktion wird von main.py aufgerufen.
# Sie zeichnet ALLE HUD-Elemente auf den Bildschirm.
# ═════════════════════════════════════════════════════════════════════════════

def hud_zeichnen(ressourcen, gebaeude_auswahl, gebaeude_typen,
                 kamera_x, kamera_y,
                 gebaeude_wirtschaft=None, maus_pos=None,
                 personal_info=None, ressourcen_limits=None,
                 baukosten_funktion=None, kategorie_name="",
                 kategorie_position=0, bild_funktion=None):

    """
    Zeichnet das gesamte HUD (Heads-Up Display) auf den Bildschirm.
    
    Das HUD besteht aus mehreren Teilen:
    1. Ressourcen-Leiste oben (Gold, Energie, Holz, Stein — 4 Werte!)
    2. Ausgewählter Gebäude-Typ (unten mittig) — mit Baukosten
    3. Kameraposition und Steuerungshinweise (oben links)
    4. Meldungs-Banner oben (NEU in Stunde 9) — z.B. zu wenig Rohstoffe
    
    Aufruf in main.py (Stunde 6):
        hud.hud_zeichnen(ressourcen_dict, gebaeude_auswahl,
                          gebaeude.GEBAEUDE_TYPEN,
                          kamera_x, kamera_y,
                          ressourcen.GEBAEUDE_WIRTSCHAFT)
    
    NEU in Stunde 9: Der Aufruf bekommt zusätzlich die Mausposition:
        hud.hud_zeichnen(..., ressourcen.GEBAEUDE_WIRTSCHAFT,
                          pygame.mouse.get_pos())
    
    Parameter:
        ressourcen           — Dictionary mit Ressourcen: {"gold": 100, ...}
        gebaeude_auswahl     — Index des ausgewählten Gebäude-Typs (0-4)
        gebaeude_typen       — Liste aller Gebäude-Typen (aus gebaeude.py)
        kamera_x             — aktuelle Kamera-x-Position
        kamera_y             — aktuelle Kamera-y-Position
        gebaeude_wirtschaft  — Liste mit Wirtschaftsdaten (aus ressourcen.py)
        maus_pos             — aktuelle Mausposition (x, y) für den Tooltip
    """
    # ── Teil 1: Ressourcen-Leiste oben zeichnen ─────────────────────────
    # Zeigt Gold, Energie, Holz und Stein mit farbigen Icons und Werten
    # Neu in Stunde 6: Auch Stein wird angezeigt!
    # Neu in Stunde 9: Mit Mausposition → Tooltip beim Hovern über ein Icon
    _ressourcen_leiste_zeichnen(ressourcen, maus_pos, gebaeude_wirtschaft,
                                ressourcen_limits)

    # ── Teil 2: Ausgewähltes Gebäude anzeigen (mit Baukosten!) ──────────
    # Zeigt unten in der Mitte welches Gebäude wir bauen wollen
    # UND was es kostet (seit Stunde 9 auch Produktion + Verbrauch)
    _gebaeude_auswahl_zeichnen(gebaeude_auswahl, gebaeude_typen,
                                gebaeude_wirtschaft, baukosten_funktion,
                                kategorie_name, kategorie_position,
                                bild_funktion)

    # ── Teil 3: Kameraposition und Steuerung ────────────────────────────
    # Zeigt wo wir sind und wie wir steuern
    _kamera_info_zeichnen(
        kamera_x, kamera_y,
        60, 40, 48,  # KARTE_BREITE, KARTE_HOEHE, KACHEL_GROESSE aus main.py
        _fenster.get_width() if _fenster else 1000,   # BILD_BREITE
        _fenster.get_height() if _fenster else 700,    # BILD_HOEHE
    )

    # ── Teil 4: Meldung oben — NEU in Stunde 9 ──────────────────────────
    # Wenn eine Meldung aktiv ist (Timer > 0), zeichnen wir sie als
    # auffälligen roten Banner am oberen Bildschirmrand und zählen den
    # Timer pro Frame herunter (bei 60 FPS: 120 Frames = 2 Sekunden).
    global _meldung_timer
    if personal_info is not None:
        verfuegbar, bedarf = personal_info
        schrift_personal = _font(22)
        personal_text = schrift_personal.render(
            f"Personal: {verfuegbar}/{bedarf}   |   Forschung: {ressourcen.get('forschung', 0):.0f}",
            True, (230, 220, 170))
        _fenster.blit(personal_text, (15, 174))

    if _meldung_timer > 0:

        _meldung_banner_zeichnen()
        _meldung_timer -= 1


def _meldung_banner_zeichnen():
    """
    Zeichnet die aktuelle Meldung als roten Banner am oberen Rand.
    Wird von hud_zeichnen() aufgerufen, solange _meldung_timer > 0 ist.
    """
    if _fenster is None:
        return

    schrift = _font(30)
    text = schrift.render(_meldung_text, True, (255, 255, 255))

    # Banner-Breite an den Text anpassen
    padding = 12
    banner_breite = text.get_width() + 2 * padding
    banner_hoehe  = 36

    # Oben in der Mitte platzieren (unter der Ressourcen-Leiste)
    banner_x = _fenster.get_width() // 2 - banner_breite // 2
    banner_y = 60

    # Banner zeichnen — rot (auffällig!) mit Rahmen
    banner_rect = pygame.Rect(banner_x, banner_y, banner_breite, banner_hoehe)
    pygame.draw.rect(_fenster, (200, 30, 30), banner_rect)       # Rot
    pygame.draw.rect(_fenster, (255, 255, 255), banner_rect, 2)  # Weißer Rahmen

    # Text mittig in den Banner setzen
    text_rect = text.get_rect(center=banner_rect.center)
    _fenster.blit(text, text_rect)


# =============================================================================
# ENDE STUNDE 9
# =============================================================================
# Wiederholung: Was wir in Stunde 9 in diesem Modul NEU gelernt haben
#
# Stunde 9 (NEU):
#   ✓ _gebaeude_auswahl_zeichnen() zeigt jetzt Produktion + Verbrauch
#     (nicht nur die Baukosten) — das Kästchen ist höher (118 px)
#   ✓ _ressourcen_leiste_zeichnen() bekommt maus_pos und gebaeude_wirtschaft
#     → Tooltip beim Hovern über ein Ressourcen-Icon
#   ✓ Meldungssystem: meldung_anzeigen(text) + _meldung_timer (120 Frames)
#   ✓ hud_zeichnen() hat neuen Parameter maus_pos und zeichnet den Banner
#
# HÄUFIGE FEHLER zum Merken (Stunde 9):
#   ✗ Vergessen, die Mausposition in main.py an hud_zeichnen() zu übergeben
#     → dann funktioniert der Tooltip nicht (maus_pos bleibt None)
#   ✗ _meldung_timer nicht herunterzählen → Meldung bleibt ewig stehen
#   ✗ Die Icon-Position im Ressourcen-Dictionary ändern, aber die Tooltip-
#     Prüfung vergessen → Tooltip erscheint an der falschen Stelle
# =============================================================================