"""
===============================================================================
MODUL: einstellungen.py  —  Einstellungsmenü mit JSON-Speicherung
===============================================================================

Wozu ist dieses Modul da?
    Das Spiel braucht Einstellungen, die NICHT im Spielstand stecken, weil
    sie auch ohne laufende Partie gelten: Lautstärke, Gitterlinien, FPS ...
    Das Modul verwaltet zwei Dinge:

        1. Die Werte selbst (laden/speichern als eigene JSON-Datei)
        2. Das Einstellungsmenü selbst (Zeichnen + Maus/Tastatur)

    Das Menü ist von überall aufrufbar — im Hauptmenü UND in der Pause:

        einstellungen.ziel_setzen("hauptmenue")   # oder "pause"
        spiel_status = "einstellungen"

    Beim Schließen fragt main.py den Ursprung mit einstellungen.ziel() ab.

    Werte wirken SOFORT: Lautstärke wird direkt auf ton.py angewandt,
    Gitter/FPS/Kamera-Tempo liest main.py bei jedem Frame aus wert().

Konzepte in dieser Datei:
    ✓ Dictionary mit Standardwerten (fehlende Werte = Standard)
    ✓ try/except beim Laden — eine kaputte Datei stürzt das Spiel nie ab
    ✓ Slider, Schalter und Stufen als einfache Zeilen-Liste (ZEILEN)
===============================================================================
"""

import json
import os

import pygame

import ton

# Pfad neben dem Spielstand — gehört in .gitignore (persönliche Werte).
DATEI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "einstellungen.json")

# Alle Einstellungen mit ihren Startwerten. Neue Einstellung? Hier eintragen —
# Menü-Zeile, Begrenzung und Fehlbehandlung laufen darüber automatisch.
STANDARD = {
    "musik_lautstaerke": 0.45,   # 0.0 = stumm, 1.0 = voll (Standard aus ton.py)
    "effekt_lautstaerke": 0.70,
    "musik_an": True,            # Hintergrundmusik grundsätzlich erlaubt
    "gitter_an": True,           # Gitterlinien zwischen den Kacheln
    "fps": 60,                   # Bildwiederholrate (Begrenzung)
    "kamera_tempo": 8,           # Kamera-Pixel pro Frame bei 60 FPS
}

# Erlaubte Wertebereiche — alles außerhalb wird automatisch begrenzt.
GRENZEN = {
    "musik_lautstaerke": (0.0, 1.0),
    "effekt_lautstaerke": (0.0, 1.0),
    "fps": (30, 120),
    "kamera_tempo": (4, 16),
}

# Auswahllisten für die "Stufen"-Zeilen im Menü.
FPS_STUFEN = (30, 60, 120)
KAMERA_STUFEN = (4, 8, 12, 16)

# Die Zeilen des Menüs: (Art, Schlüssel, Beschriftung)
#   slider   = Regler von 0–100 %
#   schalter = an/aus
#   stufe    = feste Auswahlwerte (links/rechts blättern)
#   knopf    = Aktion
ZEILEN = (
    ("slider",   "musik_lautstaerke", "Musik-Lautstärke"),
    ("slider",   "effekt_lautstaerke", "Effekt-Lautstärke"),
    ("schalter", "musik_an",         "Musik"),
    ("schalter", "gitter_an",        "Gitterlinien"),
    ("stufe",    "fps",              "FPS-Limit"),
    ("stufe",    "kamera_tempo",     "Kamera-Tempo"),
    ("knopf",    "zuruecksetzen",    "Auf Standard zurücksetzen"),
    ("knopf",    "zurueck",          "Fertig (Esc)"),
)

_werte = dict(STANDARD)   # die aktuellen Werte (eigene Kopie)
_ziel = "hauptmenue"      # wohin das Menü nach dem Schließen zurückführt

# Zustand der Menü-Darstellung
_fenster = None
_auswahl = 0              # welche Zeile mit den Pfeiltasten gewählt ist
_ziehen = None            # Slider-Index, den die Maus gerade zieht

# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 1: WERTE LADEN, SPEICHERN, SETZEN
# ═════════════════════════════════════════════════════════════════════════════

def _bereinigen(name, wert_wert):
    """Passt einen Wert auf Typ und Bereich des Standards an."""
    standard = STANDARD[name]
    if isinstance(standard, bool):
        return bool(wert_wert)
    try:
        if isinstance(standard, int):
            wert_wert = int(wert_wert)
        else:
            wert_wert = float(wert_wert)
    except (TypeError, ValueError):
        return standard
    if name in GRENZEN:
        klein, gross = GRENZEN[name]
        wert_wert = max(klein, min(gross, wert_wert))
    return wert_wert


def laden():
    """Lädt die Einstellungs-Datei. Rückgabe: True, wenn Daten ankamen.

    Eine fehlende oder kaputte Datei ist KEIN Fehler — dann gelten die
    Standards. So stürzt das Spiel nie wegen einer schlechten JSON-Datei ab.
    """
    global _werte
    _werte = dict(STANDARD)
    try:
        with open(DATEI, "r", encoding="utf-8") as datei:
            daten = json.load(datei)
    except FileNotFoundError:
        return False
    except (OSError, ValueError):
        print("[einstellungen] Datei unlesbar - es gelten die Standards.")
        return False
    if not isinstance(daten, dict):
        return False
    for name, wert_wert in daten.items():
        if name in STANDARD:
            _werte[name] = _bereinigen(name, wert_wert)
    return True


def speichern():
    """Schreibt die Einstellungen. Fehler werden geduldet, nie Absturz."""
    try:
        with open(DATEI, "w", encoding="utf-8") as datei:
            json.dump(_werte, datei, indent=2, ensure_ascii=False)
        return True
    except OSError as fehler:
        print(f"[einstellungen] Speichern nicht moeglich: {fehler}")
        return False


def wert(name):
    """Liefert den aktuellen Wert (Standard bei unbekanntem Namen)."""
    return _werte.get(name, STANDARD.get(name))


def setzen(name, neuer_wert, datei_speichern=True):
    """Setzt einen Wert (begrenzt auf den gültigen Bereich) und wendet ihn an.

    Ton-Werte werden sofort auf ton.py übertragen; Gitter/FPS/Kamera liest
    main.py bei jedem Frame direkt aus wert() — beide Wege wirken also sofort.
    """
    if name not in STANDARD:
        return wert(name)
    _werte[name] = _bereinigen(name, neuer_wert)
    _anwenden(name)
    if datei_speichern:
        speichern()
    return _werte[name]


def zuruecksetzen():
    """Stellt alle Standardwerte wieder her und speichert."""
    global _werte
    _werte = dict(STANDARD)
    speichern()


def ziel_setzen(neues_ziel):
    """Merkt sich, aus welchem Menü das Einstellungsmenü kam."""
    global _ziel
    if neues_ziel in ("hauptmenue", "pause"):
        _ziel = neues_ziel


def ziel():
    """Wohin es nach dem Schließen zurückgeht ("hauptmenue" oder "pause")."""
    return _ziel


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 2: WERTE SOFORT WIRKSAM MACHEN (TON)
# ═════════════════════════════════════════════════════════════════════════════

def _anwenden(name):
    """Macht einen geänderten Ton-Wert sofort hörbar.

    Gitter, FPS und Kamera-Tempo brauchen das nicht: main.py liest sie
    bei jedem Frame direkt aus wert() und reagiert also sofort.
    """
    if name == "musik_lautstaerke":
        ton.musik_lautstaerke_setzen(_werte[name])
    elif name == "effekt_lautstaerke":
        ton.effekt_lautstaerke_setzen(_werte[name])
    elif name == "musik_an":
        ton.musik_an_setzen(_werte[name])


def alle_anwenden():
    """Stellt alle Ton-Einstellungen nach dem Laden/Zurücksetzen wieder her."""
    _anwenden("musik_lautstaerke")
    _anwenden("effekt_lautstaerke")
    _anwenden("musik_an")

# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 3: MENÜ ZEICHNEN (Muster wie spiel_menue.py)
# ═════════════════════════════════════════════════════════════════════════════

def menue_initialisieren(fenster_obj):
    """Merkt sich das Pygame-Fenster für die Menüzeichnung."""
    global _fenster
    _fenster = fenster_obj


def menue_oeffnen():
    """Frischt den Menüzustand beim Öffnen auf."""
    global _auswahl, _ziehen
    _auswahl = 0
    _ziehen = None


def menue_schliessen():
    """Hält den letzten Slider-Wert fest und räumt den Zustand auf."""
    global _ziehen
    _ziehen = None
    speichern()


def _panel_rect():
    return pygame.Rect(170, 78, 660, 592)


def _zeile_rect(index):
    """Bereich einer Menüzeile (Zeile 0 beginnt unter dem Untertitel)."""
    return pygame.Rect(190, 196 + index * 52, 620, 44)


def _balken_rect(index):
    """Der Slider-Balken innerhalb einer slider-Zeile."""
    rect = _zeile_rect(index)
    return pygame.Rect(450, rect.y + 15, 260, 14)


def _wert_rect(index):
    """Das Wertefeld rechts bei Schaltern und Stufen."""
    rect = _zeile_rect(index)
    return pygame.Rect(600, rect.y + 6, 210, 32)


def _wert_text(index):
    """Der angezeigte Wert einer Zeile (Prozent, an/aus oder Zahl)."""
    art, schluessel, _ = ZEILEN[index]
    if art == "slider":
        return f"{int(round(_werte[schluessel] * 100))} %"
    if art == "schalter":
        # Die Musik zeigt den echten Zustand aus ton.py (auch Taste N).
        an = ton.musik_ist_an() if schluessel == "musik_an" else _werte[schluessel]
        return "an" if an else "aus"
    if art == "stufe":
        return str(_werte[schluessel])
    return ""


def menu_zeichnen():
    """Zeichnet das Einstellungsmenü als zentriertes Overlay."""
    if _fenster is None:
        return
    akzent = (90, 190, 255)

    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((3, 7, 18, 232))
    _fenster.blit(overlay, (0, 0))

    panel = _panel_rect()
    pygame.draw.rect(_fenster, (17, 24, 42), panel, border_radius=14)
    pygame.draw.rect(_fenster, akzent, panel, width=2, border_radius=14)

    gross = pygame.font.Font(None, 48)
    mittel = pygame.font.Font(None, 27)
    klein = pygame.font.Font(None, 20)

    titel = gross.render("EINSTELLUNGEN", True, (245, 248, 255))
    _fenster.blit(titel, (500 - titel.get_width() // 2, 96))
    untertitel = mittel.render("Werte gelten sofort und werden gespeichert.",
                               True, (175, 190, 210))
    _fenster.blit(untertitel, (500 - untertitel.get_width() // 2, 148))

    for index, (art, schluessel, beschriftung) in enumerate(ZEILEN):
        rect = _zeile_rect(index)
        gewaehlt = index == _auswahl
        pygame.draw.rect(_fenster, (40, 52, 78) if gewaehlt else (30, 38, 58),
                         rect, border_radius=8)
        if gewaehlt:
            pygame.draw.rect(_fenster, akzent, rect, width=2, border_radius=8)

        label = mittel.render(beschriftung, True, (240, 245, 255))
        _fenster.blit(label, (rect.x + 12, rect.y + 9))

        if art == "slider":
            balken = _balken_rect(index)
            pygame.draw.rect(_fenster, (24, 32, 50), balken, border_radius=6)
            fuell = pygame.Rect(balken.x, balken.y,
                                int(balken.w * _werte[schluessel]), balken.h)
            pygame.draw.rect(_fenster, akzent, fuell, border_radius=6)
            text = klein.render(_wert_text(index), True, (240, 245, 255))
            _fenster.blit(text, (balken.right + 12, rect.y + 12))
        elif art in ("schalter", "stufe"):
            wert_feld = _wert_rect(index)
            pygame.draw.rect(_fenster, (24, 32, 50), wert_feld, border_radius=8)
            pygame.draw.rect(_fenster, (95, 110, 140), wert_feld,
                             width=1, border_radius=8)
            zeige_an = art == "schalter" and _wert_text(index) == "an"
            farbe = (110, 225, 145) if zeige_an else (240, 245, 255)
            text = mittel.render(_wert_text(index), True, farbe)
            _fenster.blit(text, (wert_feld.centerx - text.get_width() // 2,
                                 wert_feld.y + 5))
        else:  # knopf
            text = mittel.render(beschriftung, True, (240, 245, 255))
            _fenster.blit(text, (rect.centerx - text.get_width() // 2,
                                 rect.y + 9))

    hinweis = klein.render(
        "↑/↓ auswählen · ←/→ ändern · Enter bestätigen · Esc zurück",
        True, (175, 190, 210))
    _fenster.blit(hinweis, (500 - hinweis.get_width() // 2, 630))

# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 4: EINGABEN (TASTATUR UND MAUS)
# ═════════════════════════════════════════════════════════════════════════════

def _setzen(name, neuer_wert, datei_speichern=True):
    """Setzt einen Wert im Menü — wirkt wie setzen() sofort."""
    setzen(name, neuer_wert, datei_speichern)


def _slider_setzen(index, x):
    """Stellt den Slider über die Maus-X-Position ein (0.0–1.0)."""
    art, schluessel, _ = ZEILEN[index]
    if art != "slider":
        return
    balken = _balken_rect(index)
    anteil = (x - balken.x) / balken.w
    # Während des Ziehens wird noch nicht gespeichert — das passiert beim
    # Loslassen (menue_schliessen oder maus_loslassen).
    _setzen(schluessel, round(max(0.0, min(1.0, anteil)), 2),
            datei_speichern=_ziehen is None)


def _stufe_wechseln(name, richtung):
    """Bewegt eine Stufen-Zeile (FPS-Limit, Kamera-Tempo) eine Stufe weiter."""
    stufen = FPS_STUFEN if name == "fps" else KAMERA_STUFEN
    aktuell = _werte[name]
    index = stufen.index(aktuell) if aktuell in stufen else 0
    _setzen(name, stufen[(index + richtung) % len(stufen)])


def _schalter_umschalten(schluessel):
    """Schaltet eine an/aus-Zeile um."""
    if schluessel == "musik_an":
        # Der Merker in ton.py ist die Wahrheit (auch Taste N im Spiel).
        ton.musik_an_setzen(not ton.musik_ist_an())
        setzen("musik_an", ton.musik_ist_an())
    else:
        _setzen(schluessel, not _werte[schluessel])


def _knopf_druecken(schluessel):
    """Führt eine Knopf-Zeile aus. Rückgabe "zurueck" zum Schließen."""
    if schluessel == "zuruecksetzen":
        zuruecksetzen()
        alle_anwenden()
        return None
    menue_schliessen()
    return "zurueck"


def taste(key):
    """Verarbeitet eine gedrückte Taste.

    Rückgabe: "zurueck" wenn das Menü geschlossen werden soll, sonst None.
    """
    global _auswahl
    if key == pygame.K_ESCAPE:
        menue_schliessen()
        return "zurueck"
    if key in (pygame.K_UP, pygame.K_DOWN):
        richtung = -1 if key == pygame.K_UP else 1
        _auswahl = (_auswahl + richtung) % len(ZEILEN)
        return None

    art, schluessel, _ = ZEILEN[_auswahl]
    if key in (pygame.K_LEFT, pygame.K_RIGHT):
        richtung = -1 if key == pygame.K_LEFT else 1
        if art == "slider":
            neu = _werte[schluessel] + 0.05 * richtung
            _setzen(schluessel, round(max(0.0, min(1.0, neu)), 2))
        elif art == "schalter":
            _schalter_umschalten(schluessel)
        elif art == "stufe":
            _stufe_wechseln(schluessel, richtung)
        return None
    if key in (pygame.K_RETURN, pygame.K_SPACE):
        if art == "schalter":
            _schalter_umschalten(schluessel)
        elif art == "stufe":
            _stufe_wechseln(schluessel, +1)
        elif art == "knopf":
            return _knopf_druecken(schluessel)
    return None


def mausklick(pos):
    """Verarbeitet einen Linksklick. Rückgabe wie taste()."""
    global _auswahl, _ziehen
    for index, (art, schluessel, _) in enumerate(ZEILEN):
        if not _zeile_rect(index).collidepoint(pos):
            continue
        _auswahl = index
        if art == "slider":
            _ziehen = index
            _slider_setzen(index, pos[0])
        elif art == "schalter":
            _schalter_umschalten(schluessel)
        elif art == "stufe":
            _stufe_wechseln(schluessel, +1)
        else:
            return _knopf_druecken(schluessel)
        return None
    return None


def maus_ziehen(pos, taste_gedrueckt):
    """Ziehen mit gehaltener Maustaste (nur Slider-Zeilen)."""
    if _ziehen is None or not taste_gedrueckt:
        return
    _slider_setzen(_ziehen, pos[0])


def maus_loslassen():
    """Beendet das Ziehen und speichert den neuen Wert."""
    global _ziehen
    if _ziehen is not None:
        _ziehen = None
        speichern()



