"""
===============================================================================
SKRIPT: sounds_erzeugen.py  —  Terra_Nova (Fortgeschrittener Kurs)
===============================================================================

Wozu ist dieses Skript da?
    Das Spiel braucht Sounddateien (Effekte und Hintergrundmusik). Damit wir
    keine fremden Dateien herunterladen muessen, erzeugt dieses Skript alle
    WAV-Dateien selbst — mit reinem Python (nur Standardbibliothek!).

    Das Spiel braucht dieses Skript NICHT zum Starten:
    Die fertigen WAV-Dateien liegen im Ordner ``sounds/`` und werden mit
    ausgeliefert. Wenn du einen Sound aendern willst, aenderst du hier die
    Werte, laeufst einmal ``python sounds_erzeugen.py`` und hoerst dir das
    Ergebnis im Spiel an.

Was lernst du hier?
    ✓ Wie eine WAV-Datei aufgebaut ist (Abtastrate, 16 Bit, mono)
    ✓ Wie man einen Sinus-Ton mit math.sin() selbst berechnet
    ✓ Wie man Toene aneinanderhaengt (Jingle) und uebereinanderlegt (Akkord)
    ✓ Wie man mit einer Huellkurve (Ein-/Ausblenden) Klicks vermeidet
    ✓ Warum man Zufallszahlen mit festem Seed wiederholbar macht

Technische Daten aller Dateien:
    Abtastrate : 22050 Hz   (CD-Qualitaet reicht fuer Spieleffekte locker)
    Aufloesung : 16 Bit     (= 2 Bytes pro Tonwert)
    Kanaele    : 1          (mono)

Aufruf (Windows, PowerShell):
    python sounds_erzeugen.py
===============================================================================
"""

import math
import os
import random
import struct
import wave


# ── Konstanten (hier kannst du experimentieren) ─────────────────────────────

ABTASTRATE = 22050          # Wie viele Tonwerte pro Sekunde gespeichert werden
KANAELE = 1                 # 1 = mono (ein Kanal), 2 = stereo
BYTES_PRO_WERT = 2          # 16 Bit sind 2 Bytes
MAX_WERT = 32767            # Groesster Wert einer 16-Bit-Zahl mit Vorzeichen

# Fester Zufalls-Seed: Damit klingt die Musik bei jedem Lauf gleich.
# So kannst du Aenderungen an der Musik wirklich vergleichen!
ZUFALLS_SEED = 20240521

ORDNER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 1: WAV-DATEI SCHREIBEN
# ═════════════════════════════════════════════════════════════════════════════

def _wav_schreiben(dateiname, werte):
    """Schreibt eine Liste von Fliesskommazahlen (-1.0 bis +1.0) als WAV.

    Der Aufbau einer WAV-Datei: Sie besteht aus einem Kopf (Kopfdaten) und
    danach den reinen Tonwerten. Genau diesen Kopf schreibt das Modul ``wave``
    fuer uns. Wir muessen nur noch jeden Tonwert von -1.0..+1.0 in eine
    16-Bit-Ganzzahl umrechnen:

        ganzer_wert = wert * 32767
    """
    daten = bytearray()
    for wert in werte:
        # Werte ausserhalb -1..1 wuerden "uebersteuern" und kratzen. Deshalb
        # begrenzen wir sie hier vorsichtig auf den erlaubten Bereich.
        if wert > 1.0:
            wert = 1.0
        elif wert < -1.0:
            wert = -1.0
        daten += struct.pack("<h", int(wert * MAX_WERT))

    pfad = os.path.join(ORDNER, dateiname)
    with wave.open(pfad, "w") as datei:
        datei.setnchannels(KANAELE)
        datei.setsampwidth(BYTES_PRO_WERT)
        datei.setframerate(ABTASTRATE)
        datei.writeframes(bytes(daten))
    return pfad


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 2: KLEINE BAUSTEINE FUER TOENE
# ═════════════════════════════════════════════════════════════════════════════

def _anzahl(dauer):
    """Rechnet eine Dauer in Sekunden in die Anzahl Tonwerte um."""
    return max(1, int(dauer * ABTASTRATE))


def _sinus(frequenz, dauer, lautstaerke=1.0, phase=0.0):
    """Erzeugt einen weichen Sinus-Ton.

    Ein Sinus ist der "reine" Ton: Er klingt weich und rund. Deshalb nutzen
    wir ihn fuer Musik und fuer freundliche Signale.
    """
    schritt = 2.0 * math.pi * frequenz / ABTASTRATE
    return [lautstaerke * math.sin(schritt * i + phase) for i in range(_anzahl(dauer))]


def _rechteck(frequenz, dauer, lautstaerke=1.0):
    """Erzeugt einen harten Rechteck-Ton (klingt rau und alarmierend)."""
    schritt = 2.0 * math.pi * frequenz / ABTASTRATE
    return [lautstaerke if math.sin(schritt * i) >= 0 else -lautstaerke
            for i in range(_anzahl(dauer))]


def _rauschen(dauer, lautstaerke=0.3, zufall=None):
    """Erzeugt weisses Rauschen (klingt wie Wind, Knistern oder Explosion)."""
    generator = zufall or random
    return [generator.uniform(-lautstaerke, lautstaerke)
            for _ in range(_anzahl(dauer))]


def _sweep(frequenz_start, frequenz_ende, dauer, lautstaerke=1.0):
    """Erzeugt einen Ton, dessen Hoehe langsam steigt oder faellt.

    Ein solcher "Sweep" klingt lebendig: aufsteigend = etwas entsteht,
    absteigend = etwas geht kaputt. Genau das passt zu Bauen und Abreissen.
    """
    anzahl = _anzahl(dauer)
    werte = []
    phase = 0.0
    for i in range(anzahl):
        # Der Anteil 0..1 sagt uns, wie weit der Sweep schon fortgeschritten ist.
        anteil = i / anzahl
        frequenz = frequenz_start + (frequenz_ende - frequenz_start) * anteil
        phase += 2.0 * math.pi * frequenz / ABTASTRATE
        werte.append(lautstaerke * math.sin(phase))
    return werte


def _huelle(werte, einblenden=0.01, ausblenden=0.05):
    """Blendet Anfang und Ende weich ein bzw. aus.

    Ohne diese Huellkurve "knackt" es am Anfang und Ende jedes Tons, weil der
    Ton schlagartig von 0 auf laut springt. Ein kurzes Ein-/Ausblenden hoert
    man nicht, verhindert aber das Knacken.
    """
    gesamt = len(werte)
    ein_anzahl = min(gesamt, _anzahl(einblenden))
    aus_anzahl = min(gesamt - ein_anzahl, _anzahl(ausblenden))
    ergebnis = list(werte)
    for i in range(ein_anzahl):
        ergebnis[i] *= i / ein_anzahl
    for i in range(aus_anzahl):
        ergebnis[gesamt - 1 - i] *= i / aus_anzahl
    return ergebnis


def _stille(dauer):
    """Erzeugt eine Pause (Stille) zwischen zwei Toenen."""
    return [0.0] * _anzahl(dauer)


def _aneinander(*teile):
    """Haengt mehrere Tonstuecke hintereinander (Sequenz)."""
    ergebnis = []
    for teil in teile:
        ergebnis.extend(teil)
    return ergebnis


def _gleichzeitig(*spuren):
    """Legt mehrere Tonstuecke uebereinander (Akkord).

    Die Spuren duerfen unterschiedlich lang sein: Die kuerzeren werden mit 0
    aufgefuellt, damit nichts verschoben wird.
    """
    laenge = max(len(spur) for spur in spuren)
    ergebnis = [0.0] * laenge
    for spur in spuren:
        for i, wert in enumerate(spur):
            ergebnis[i] += wert
    return ergebnis


def _normiere(werte, spitze=0.85):
    """Skaliert alle Werte so, dass der lauteste Wert ``spitze`` ergibt.

    So klingen alle Effekte etwa gleich laut, obwohl sie aus unterschiedlich
    vielen Toenen bestehen.
    """
    maximum = max(abs(wert) for wert in werte) if werte else 1.0
    if maximum == 0:
        return werte
    faktor = spitze / maximum
    return [wert * faktor for wert in werte]


def _stueck(werte, ein=0.006, aus=0.05):
    """Setzt eine kurze Huellkurve auf ein einzelnes Tonstueck."""
    return _huelle(werte, ein, aus)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 3: DIE EINZELNEN SOUNDEFFEKTE
# ═════════════════════════════════════════════════════════════════════════════
# Jede Funktion liefert eine Liste von Tonwerten. Die Namen entsprechen genau
# den Dateinamen aus dem Dictionary SOUNDS in ton.py.

def effekt_bauen():
    """Kurzer, freundlicher Ton: ein Gebaeude entsteht."""
    # Zwei aufsteigende Sweeps klingen wie "etwas baut sich auf".
    return _normiere(_aneinander(
        _stueck(_sweep(170, 430, 0.09, 0.70)),
        _stueck(_sweep(430, 640, 0.11, 0.55)),
        _stueck(_rauschen(0.04, 0.10)),
    ))


def effekt_abriss():
    """Ein Gebaeude wird abgerissen: es rummst und rieselt."""
    return _normiere(_aneinander(
        _stueck(_sweep(620, 90, 0.28, 0.70)),
        _stueck(_rauschen(0.22, 0.25)),
    ))


def effekt_fehler():
    """Zwei tiefe, harte Toene: das hat nicht funktioniert."""
    return _normiere(_aneinander(
        _stueck(_rechteck(180, 0.11, 0.45)),
        _stille(0.06),
        _stueck(_rechteck(140, 0.16, 0.45)),
    ), 0.55)


def effekt_achievement():
    """Kurzer aufsteigender Jingle: ein Erfolg wurde freigeschaltet."""
    return _normiere(_aneinander(
        _stueck(_sinus(523.25, 0.12, 0.50)),   # C
        _stueck(_sinus(659.25, 0.12, 0.50)),   # E
        _stueck(_sinus(783.99, 0.12, 0.50)),   # G
        # Am Ende klingen zwei Toene gleichzeitig — wie ein kleiner Akkord.
        _stueck(_gleichzeitig(_sinus(1046.50, 0.34, 0.45),
                              _sinus(1318.51, 0.34, 0.22)), 0.01, 0.12),
    ))


def effekt_mission_erledigt():
    """Etwas laengere kleine Melodie: eine Mission ist geschafft."""
    return _normiere(_aneinander(
        _stueck(_sinus(392.00, 0.14, 0.50)),   # G
        _stueck(_sinus(523.25, 0.14, 0.50)),   # C
        _stueck(_sinus(659.25, 0.16, 0.50)),   # E
        _stueck(_gleichzeitig(_sinus(783.99, 0.42, 0.45),
                              _sinus(523.25, 0.42, 0.25)), 0.01, 0.16),
    ))


def effekt_forschung_fertig():
    """Technischer "Blip": eine Forschung ist abgeschlossen."""
    return _normiere(_aneinander(
        _stueck(_sinus(880.00, 0.08, 0.45)),
        _stueck(_sinus(1174.66, 0.08, 0.45)),
        _stueck(_gleichzeitig(_sinus(1567.98, 0.20, 0.45),
                              _rechteck(783.99, 0.20, 0.10)), 0.01, 0.08),
    ))


def effekt_terraforming():
    """Weicher, wabernder Ton: eine Kachel wird fruchtbarer Boden."""
    anzahl = _anzahl(0.90)
    werte = []
    phase = 0.0
    for i in range(anzahl):
        anteil = i / anzahl
        # Die Tonhoehe steigt langsam an und zittert leicht (Vibrato).
        frequenz = 180 + 420 * anteil
        frequenz += 6.0 * math.sin(2.0 * math.pi * 5.0 * i / ABTASTRATE)
        phase += 2.0 * math.pi * frequenz / ABTASTRATE
        # sin(pi * anteil) ist am Anfang und Ende 0 → weiches Ein-/Ausblenden.
        lautstaerke = 0.5 * math.sin(math.pi * anteil)
        werte.append(lautstaerke * math.sin(phase))
    return _normiere(werte, 0.70)


def effekt_handel():
    """Klimpern wie Muenzen: ein Handel wurde abgeschlossen."""
    return _normiere(_aneinander(
        _stueck(_sinus(1174.66, 0.07, 0.45)),
        _stueck(_sinus(1567.98, 0.07, 0.45)),
        _stueck(_gleichzeitig(_sinus(2093.00, 0.16, 0.40),
                              _rauschen(0.16, 0.05)), 0.005, 0.06),
    ))


def effekt_sieg():
    """Kleine Fanfare: die Kolonie hat gewonnen."""
    return _normiere(_aneinander(
        _stueck(_sinus(523.25, 0.16, 0.50)),
        _stueck(_sinus(523.25, 0.16, 0.50)),
        _stueck(_sinus(659.25, 0.16, 0.50)),
        _stueck(_sinus(783.99, 0.22, 0.50)),
        _stueck(_gleichzeitig(_sinus(1046.50, 0.60, 0.45),
                              _sinus(783.99, 0.60, 0.30),
                              _sinus(523.25, 0.60, 0.30)), 0.01, 0.25),
    ))


def effekt_niederlage():
    """Traurige, absteigende Tonfolge: die Kolonie hat verloren."""
    return _normiere(_aneinander(
        _stueck(_rechteck(392.00, 0.30, 0.35)),
        _stueck(_rechteck(311.13, 0.30, 0.35)),
        _stueck(_rechteck(261.63, 0.30, 0.35)),
        _stueck(_gleichzeitig(_rechteck(196.00, 0.80, 0.35),
                              _rauschen(0.80, 0.06)), 0.02, 0.30),
    ), 0.60)


def effekt_angriff_warnung():
    """Sirene: Ein Angriff kündigt sich an (gut hoerbar!)."""
    teile = []
    for _ in range(3):
        teile.append(_stueck(_sweep(480, 900, 0.42, 0.60)))   # Sirene hoch
        teile.append(_stueck(_sweep(900, 480, 0.42, 0.60)))   # Sirene runter
    return _normiere(_aneinander(*teile), 0.80)


def effekt_abwehr_erfolg():
    """Heller Triumph-Ton: der Angriff wurde abgewehrt."""
    return _normiere(_aneinander(
        _stueck(_sinus(659.25, 0.10, 0.50)),
        _stueck(_sinus(880.00, 0.10, 0.50)),
        _stueck(_gleichzeitig(_sinus(1318.51, 0.45, 0.45),
                              _rauschen(0.45, 0.04)), 0.01, 0.18),
    ))


def effekt_ausgeraubt():
    """Duesterer Absturz-Ton: die Kolonie wurde ausgeraubt."""
    return _normiere(_aneinander(
        _stueck(_sweep(300, 110, 0.70, 0.60)),
        _stueck(_gleichzeitig(_rechteck(110, 0.45, 0.30),
                              _rauschen(0.45, 0.10)), 0.02, 0.20),
    ), 0.70)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 4: HINTERGRUNDMUSIK (ruhiger Sci-Fi-Loop)
# ═════════════════════════════════════════════════════════════════════════════
# Die Musik besteht aus drei Schichten:
#   1. Bass   — ein tiefer Dauerton, der die Stimmung "Weltraum" gibt
#   2. Pad    — weiche Akkorde, die alle 12 Sekunden wechseln
#   3. Glocken — einzelne hohe Toene mit Nachhall
# Damit die Musik als Endlosschleife funktioniert, wird der Schlussakkord
# (G-Dur) so gewaehlt, dass er wieder zum ersten Akkord (A-Moll) passt.

MUSIK_DAUER = 48.0      # Laenge des Loops in Sekunden

# (Name, Basston, Akkordtoene)
AKKORDE = [
    ("A-Moll", 110.00, (220.00, 261.63, 329.63)),
    ("F-Dur",   87.31, (174.61, 220.00, 261.63)),
    ("C-Dur",  130.81, (196.00, 261.63, 329.63)),
    ("G-Dur",   98.00, (196.00, 246.94, 293.66)),
]


def _schicht_hinzufuegen(spuren, start, laenge, frequenz, amplitude,
                         abklingen=0.0):
    """Addiert einen weichen Sinus-Ton in den Gesamtpuffer.

    ``abklingen`` > 0 laesst den Ton wie eine Glocke leiser werden.
    """
    schritt = 2.0 * math.pi * frequenz / ABTASTRATE
    for i in range(laenge):
        anteil = i / laenge
        if abklingen:
            # Glocken klingen schnell ab: exp(-3) ist nach der vollen
            # Laenge auf etwa 5 Prozent der Lautstaerke gesunken.
            huellwert = math.exp(-3.0 * anteil)
        else:
            # Flaeche: weich einblenden, dann halten, dann weich ausblenden.
            huellwert = min(1.0, anteil / 0.20, (1.0 - anteil) / 0.20)
        spuren[start + i] += amplitude * huellwert * math.sin(schritt * i)


def hintergrundmusik():
    """Erzeugt den etwa 48 Sekunden langen Musik-Loop."""
    zufall = random.Random(ZUFALLS_SEED)
    gesamt = _anzahl(MUSIK_DAUER)
    spuren = [0.0] * gesamt
    akkord_laenge = MUSIK_DAUER / len(AKKORDE)

    # 1. Bass und Pad je Akkord
    for index, (_name, bass, toene) in enumerate(AKKORDE):
        start = _anzahl(index * akkord_laenge)
        laenge = min(_anzahl(akkord_laenge), gesamt - start)
        _schicht_hinzufuegen(spuren, start, laenge, bass, 0.14)
        for versatz, frequenz in enumerate(toene):
            # Die hoeheren Toene sind etwas leiser, damit es nicht grell wird.
            _schicht_hinzufuegen(spuren, start, laenge, frequenz, 0.09 - versatz * 0.01)

    # 2. Einzelne Glocken ueber der Flaeche (alle 2 Sekunden)
    zeitpunkt = 0.5
    while zeitpunkt + 2.0 < MUSIK_DAUER:
        akkord_index = int(zeitpunkt // akkord_laenge) % len(AKKORDE)
        toene = AKKORDE[akkord_index][2]
        frequenz = zufall.choice(toene) * 4.0      # vierfach = zwei Oktaven hoeher
        start = _anzahl(zeitpunkt)
        laenge = min(_anzahl(1.8), gesamt - start)
        _schicht_hinzufuegen(spuren, start, laenge, frequenz, 0.07, abklingen=1.0)
        zeitpunkt += 2.0

    # 3. Gesamtlautstaerke begrenzen und Loop-Enden weich machen
    return _normiere(_huelle(spuren, 1.0, 1.5), 0.55)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK 5: ALLES ERZEUGEN
# ═════════════════════════════════════════════════════════════════════════════

# Diese Tabelle verbindet Dateinamen mit der Funktion, die sie erzeugt.
# Wenn du einen eigenen Sound ergaenzst, traegst du ihn hier ein.
SOUND_DATEIEN = [
    ("bauen.wav", effekt_bauen),
    ("abriss.wav", effekt_abriss),
    ("fehler.wav", effekt_fehler),
    ("achievement.wav", effekt_achievement),
    ("mission_erledigt.wav", effekt_mission_erledigt),
    ("forschung_fertig.wav", effekt_forschung_fertig),
    ("terraforming.wav", effekt_terraforming),
    ("handel.wav", effekt_handel),
    ("sieg.wav", effekt_sieg),
    ("niederlage.wav", effekt_niederlage),
    ("angriff_warnung.wav", effekt_angriff_warnung),
    ("abwehr_erfolg.wav", effekt_abwehr_erfolg),
    ("ausgeraubt.wav", effekt_ausgeraubt),
    ("hintergrundmusik.wav", hintergrundmusik),
]


def erzeugen():
    """Erzeugt alle Sounddateien und gibt eine kleine Übersicht aus."""
    if not os.path.isdir(ORDNER):
        os.makedirs(ORDNER)
    for dateiname, funktion in SOUND_DATEIEN:
        werte = funktion()
        pfad = _wav_schreiben(dateiname, werte)
        dauer = len(werte) / ABTASTRATE
        groesse_kb = os.path.getsize(pfad) / 1024.0
        print(f"  {dateiname:<24} {dauer:6.2f} s   {groesse_kb:8.1f} KB")


if __name__ == "__main__":
    print("Erzeuge Sounddateien in:", ORDNER)
    erzeugen()
    print("Fertig. Das Spiel kann diese Dateien jetzt abspielen.")

