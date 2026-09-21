"""
===============================================================================
MODUL: ton.py  —  Musik und Soundeffekte für das Weltraum-Koloniespiel
===============================================================================

Wozu ist dieses Modul da?
    Das Spiel soll nicht stumm sein: Beim Bauen, beim Abriss, bei Erfolgen,
    bei Angriffen und im Hintergrund soll etwas zu hören sein. Dieses Modul
    kuemmert sich um ALLE Toene. Das restliche Spiel ruft nur noch auf:

        ton.initialisieren()            # einmal beim Spielstart
        ton.sound_abspielen("bauen")    # kurzer Effekt
        ton.musik_starten()             # Hintergrundmusik als Endlosschleife

Wichtig: Das Spiel darf NIE wegen Ton abstuerzen!
    Schulcomputer, Servertests und der Dummy-Treiber von SDL haben oft kein
    Audiogeraet. Deshalb steckt das Einschalten des Mixers in einem
    try/except. Wenn der Ton nicht funktioniert, sind alle Funktionen in
    diesem Modul einfach "No-Ops" (sie machen nichts) und das Spiel laeuft
    normal weiter.

Wie tausche ich einen Sound aus?
    Unten sind alle Effekte den Dateinamen zugeordnet:

        SOUNDS = {"bauen": "bauen.wav", ...}

    Lege einfach eine eigene Datei mit dem gleichen Namen in den Ordner
    ``sounds/`` — fertig. Die mitgelieferten Dateien erzeugt das Skript
    ``sounds_erzeugen.py`` mit der Standardbibliothek.

Konzepte in dieser Datei:
    ✓ try/except: Fehler abfangen, statt abzustuerzen
    ✓ Dictionary: Ereignisname → Dateiname
    ✓ Modul-Variablen als "Gedaechtnis" des Moduls
    ✓ Zeitmessung mit pygame.time.get_ticks() (Millisekunden)
===============================================================================
"""

import os

import pygame


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 1: KONSTANTEN — hier kannst du alles einstellen
# ═════════════════════════════════════════════════════════════════════════════

# Lautstaerken von 0.0 (still) bis 1.0 (voller Pegel).
MUSIK_LAUTSTAERKE = 0.45     # Hintergrundmusik: lieber etwas leiser
EFFEKT_LAUTSTAERKE = 0.70    # Effekte dürfen deutlicher sein

# Wenn derselbe Effekt sehr schnell erneut ausgeloest wird, klingt das wie ein
# Knistern. Deshalb wird derselbe Ton innerhalb dieser Zeit nur einmal gestartet.
SOUND_ABSTAND_MS = 80

# Hintergrundmusik: ruhiger Sci-Fi-Loop (wird von sounds_erzeugen.py erzeugt)
MUSIK_DATEI = "hintergrundmusik.wav"

# Ereignisname → Dateiname im Ordner sounds/
SOUNDS = {
    "bauen":              "bauen.wav",
    "abriss":             "abriss.wav",
    "fehler":             "fehler.wav",
    "achievement":        "achievement.wav",
    "mission_erledigt":   "mission_erledigt.wav",
    "forschung_fertig":   "forschung_fertig.wav",
    "terraforming":       "terraforming.wav",
    "handel":             "handel.wav",
    "sieg":               "sieg.wav",
    "niederlage":         "niederlage.wav",
    # Ab Phase "Gegner und Verteidigung":
    "angriff_warnung":    "angriff_warnung.wav",
    "abwehr_erfolg":      "abwehr_erfolg.wav",
    "ausgeraubt":         "ausgeraubt.wav",
}

ORDNER_NAME = "sounds"


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 2: MODUL-VARIABLEN (das "Gedaechtnis" des Moduls)
# ═════════════════════════════════════════════════════════════════════════════

_mixer_bereit = False        # True, wenn Pygame Toene abspielen kann
_musik_an = True             # Merker der Musik-Taste N
_musik_laeuft = False        # Läuft gerade Musik?
_effekte = {}                # schon geladene Sounds (Name → pygame.mixer.Sound)
_letzte_startzeit = {}       # Name → Zeitpunkt des letzten Starts in Millisekunden
_abspielzaehler = {}         # Name → wie oft der Effekt wirklich gestartet wurde
_dateien_gemeldet = set()    # Dateien, für die schon einmal gewarnt wurde


def sounds_ordner():
    """Liefert den vollstaendigen Pfad des Ordners ``sounds``."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ORDNER_NAME)


def _datei_pfad(dateiname):
    """Baut den vollstaendigen Pfad einer Sounddatei."""
    return os.path.join(sounds_ordner(), dateiname)


def _hinweis(text):
    """Gibt einen Hinweis in der Konsole aus.

    Bewusst ohne Umlaute: Manche Windows-Konsolen koennen sie nicht darstellen.
    """
    print("[ton] " + text)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 3: INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════

def initialisieren():
    """Schaltet den Pygame-Mixer ein und laedt alle Effekte.

    Rueckgabe: True, wenn Ton moeglich ist — sonst False.

    Der gesamte Vorgang ist abgesichert: Ohne Audiogeraet (Schulrechner,
    Testlauf mit SDL_AUDIODRIVER=dummy) meldet Pygame einen Fehler. Wir
    fangen ihn ab und arbeiten danach einfach ohne Ton weiter.
    """
    global _mixer_bereit
    try:
        # Nur initialisieren, wenn Pygame den Mixer nicht schon gestartet hat.
        if pygame.mixer.get_init() is None:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        _mixer_bereit = True
    except (pygame.error, AttributeError) as fehler:
        _mixer_bereit = False
        _hinweis("Kein Audiogeraet gefunden - das Spiel laeuft ohne Ton weiter "
                 f"({fehler})")
        return False

    # Alle Effekte vorladen: Beim ersten Abspielen soll nichts ruckeln.
    for name in SOUNDS:
        _effekt_laden(name)
    return True


def mixer_bereit():
    """Sagt, ob Toene technisch moeglich sind (fuer Tests und Hilfe nützlich)."""
    return _mixer_bereit


def _effekt_laden(name):
    """Laedt einen Effekt aus dem Ordner sounds/ und merkt ihn sich.

    Fehlt die Datei, gibt es EINEN Hinweis in der Konsole — und danach wird
    der Effekt einfach still uebersprungen. Kein Absturz.
    """
    if not _mixer_bereit:
        return None
    if name in _effekte:
        return _effekte[name]

    dateiname = SOUNDS.get(name)
    if dateiname is None:
        # Unbekannter Name: Das ist ein Programmierfehler, aber kein Grund
        # fuer einen Absturz. Einmal melden, dann ignorieren.
        if name not in _dateien_gemeldet:
            _dateien_gemeldet.add(name)
            _hinweis(f"Unbekannter Sound '{name}' - wird ignoriert.")
        return None

    pfad = _datei_pfad(dateiname)
    if not os.path.isfile(pfad):
        if dateiname not in _dateien_gemeldet:
            _dateien_gemeldet.add(dateiname)
            _hinweis(f"Sounddatei fehlt: sounds/{dateiname} - "
                     "starte 'python sounds_erzeugen.py'.")
        return None

    try:
        klang = pygame.mixer.Sound(pfad)
        klang.set_volume(EFFEKT_LAUTSTAERKE)
        _effekte[name] = klang
        return klang
    except (pygame.error, OSError) as fehler:
        if dateiname not in _dateien_gemeldet:
            _dateien_gemeldet.add(dateiname)
            _hinweis(f"Sound {dateiname} konnte nicht geladen werden: {fehler}")
        return None


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 4: EFFEKTE ABSPIELEN
# ═════════════════════════════════════════════════════════════════════════════

def sound_abspielen(name):
    """Spielt einen Soundeffekt. Unbekannte oder fehlende Sounds sind No-Ops.

    Zwei Schutzmassnahmen:
      1. Derselbe Effekt wird innerhalb von SOUND_ABSTAND_MS nur einmal
         gestartet (verhindert lautes Knistern bei schnellen Ereignissen).
      2. Ohne Mixer passiert gar nichts.
    """
    if not _mixer_bereit:
        return False
    klang = _effekt_laden(name)
    if klang is None:
        return False

    jetzt = pygame.time.get_ticks()
    letzter_zeitpunkt = _letzte_startzeit.get(name)
    if (letzter_zeitpunkt is not None and
            jetzt - letzter_zeitpunkt < SOUND_ABSTAND_MS):
        return False
    _letzte_startzeit[name] = jetzt

    try:
        klang.play()
    except (pygame.error, AttributeError):
        return False
    _abspielzaehler[name] = _abspielzaehler.get(name, 0) + 1
    return True


def abspielzaehler(name):
    """Wie oft wurde dieser Effekt wirklich gestartet? (fuer Tests und Doku)"""
    return _abspielzaehler.get(name, 0)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 5: HINTERGRUNDMUSIK
# ═════════════════════════════════════════════════════════════════════════════

def musik_starten():
    """Startet die Hintergrundmusik als Endlosschleife (wenn Musik erlaubt ist)."""
    global _musik_laeuft
    if not _mixer_bereit or not _musik_an:
        return False
    if _musik_laeuft:
        return True

    pfad = _datei_pfad(MUSIK_DATEI)
    if not os.path.isfile(pfad):
        if MUSIK_DATEI not in _dateien_gemeldet:
            _dateien_gemeldet.add(MUSIK_DATEI)
            _hinweis("Musikdatei fehlt: sounds/hintergrundmusik.wav - "
                     "starte 'python sounds_erzeugen.py'.")
        return False
    try:
        pygame.mixer.music.load(pfad)
        pygame.mixer.music.set_volume(MUSIK_LAUTSTAERKE)
        pygame.mixer.music.play(-1)      # -1 = immer wieder von vorne (Loop)
    except (pygame.error, OSError):
        return False
    _musik_laeuft = True
    return True


def musik_stoppen():
    """Stoppt die Hintergrundmusik (z. B. bei Sieg oder Niederlage)."""
    global _musik_laeuft
    if not _mixer_bereit:
        return
    try:
        pygame.mixer.music.stop()
    except (pygame.error, AttributeError):
        pass
    _musik_laeuft = False


def musik_pausieren():
    """Haelt die Musik an, ohne sie zu vergessen (fuer das Pausenmenue)."""
    if not _mixer_bereit or not _musik_laeuft:
        return
    try:
        pygame.mixer.music.pause()
    except (pygame.error, AttributeError):
        pass


def musik_fortsetzen():
    """Setzt eine mit musik_pausieren() angehaltene Musik wieder fort."""
    if not _mixer_bereit or not _musik_an or not _musik_laeuft:
        return
    try:
        pygame.mixer.music.unpause()
    except (pygame.error, AttributeError):
        pass


def musik_umschalten():
    """Schaltet die Musik mit einer Taste an oder aus (Taste N).

    Rueckgabe: True, wenn die Musik danach laeuft.
    """
    global _musik_an
    _musik_an = not _musik_an
    if _musik_an:
        musik_starten()
    else:
        musik_stoppen()
    return _musik_an


def musik_ist_an():
    """Ist die Musik eingeschaltet (auch wenn sie gerade pausiert ist)?"""
    return _musik_an


def musik_status_text():
    """Kurzer Text fuer HUD oder Hilfe: 'Musik: an' bzw. 'Musik: aus'."""
    return "Musik: " + ("an" if _musik_an else "aus")


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 6: ZUSTAND (Muster wie in den anderen Modulen)
# ═════════════════════════════════════════════════════════════════════════════

def zustand_exportieren():
    """Gibt die Einstellung der Musik fuer einen Spielstand zurueck."""
    return {"musik_an": bool(_musik_an)}


def zustand_importieren(daten):
    """Stellt die Musik-Einstellung aus einem Spielstand wieder her.

    Der Import startet oder stoppt die Musik nicht selbst. Das passiert erst
    beim naechsten Aufruf von musik_starten() bzw. musik_stoppen().
    """
    global _musik_an
    daten = daten if isinstance(daten, dict) else {}
    _musik_an = bool(daten.get("musik_an", True))


def zustand_zuruecksetzen():
    """Setzt Musik und Effekt-Gedaechtnis auf den Startzustand zurueck."""
    global _musik_an, _musik_laeuft
    _musik_an = True
    _musik_laeuft = False
    _letzte_startzeit.clear()
    _abspielzaehler.clear()
    musik_stoppen()
