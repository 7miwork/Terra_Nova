"""
=============================================================================
PROJEKT: Terra_Nova  —  Koloniespiel auf einem fremden Planeten
STUNDE 7 — Bevölkerung & Wohnungen
=============================================================================

Worum geht es?
    In diesem Spiel landest du auf einem fremden Planeten und baust
    eine Kolonie auf. Du startest mit einem kleinen Raumschiff und
    musst Ressourcen sammeln, Gebäude bauen und die Kolonie erweitern.
    Das Ziel: Eine blühende Kolonie auf einem fremden Planeten!

    Dieses Spiel ist inspiriert von "Final Earth 2" — einem Kolonie-
    Aufbauspiel auf einem fremden Planeten.

Bisher gelernt (Stunde 1 — Das Fundament):
    ✓ pygame.init() startet Pygame
    ✓ display.set_mode() erstellt das Fenster
    ✓ Die Spielschleife: Eingaben → Logik → Zeichnen
    ✓ Farben als (R, G, B) Tupel
    ✓ Konstanten in GROSSBUCHSTABEN
    ✓ Funktionen mit def
    ✓ Schwarzer Weltraum-Hintergrund

Bisher gelernt (Stunde 2 — Die Mondkarte und Kamera-Scroll):
    ✓ Karte aus Kacheln (Gitter) wird gezeichnet
    ✓ Mit Pfeiltasten über die Karte scrollen
    ✓ Kamera merkt sich wo wir hingeschaut haben
    ✓ Mond-Oberfläche mit verschiedenen Boden-Farben
    ✓ Sterne im Weltraum-Hintergrund
    ✓ Wie in Final Earth 2!

Bisher gelernt (Stunde 3 — Gebäude bauen):
    ✓ Mausklick erkennen mit pygame.MOUSEBUTTONDOWN
    ✓ Kachel unter dem Mauszeiger berechnen
    ✓ Gebäude auf der Karte platzieren (wie in Final Earth 2!)
    ✓ Gebäude zeichnen (farbige Rechtecke auf der Karte)
    ✓ Erste Kolonie-Gebäude: Basis, Reaktor, Farm
    ✓ Gebäude speichern in einer Liste

Bisher gelernt (Stunde 4 — HUD & Ressourcenanzeige):
    ✓ HUD (Heads-Up Display) am oberen Bildschirmrand zeichnen
    ✓ Ressourcen-Anzeige: Gold, Energie, Holz
    ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2!)
    ✓ Ressourcen als Dictionary speichern {"gold": 100, ...}

Bisher gelernt (Stunde 5 — Ressourcen-Logik & Wirtschaft):
    ✓ Ressourcen-Produktion und Verbrauch pro Gebäude
    ✓ Baukosten: Gebäude bauen kostet jetzt Ressourcen
    ✓ Tick-System: 1× pro Sekunde produzieren/verbrauchen Gebäude
    ✓ Basis kann nur 1× gebaut werden
    ✓ Wenn Rohstoffe fehlen → Gebäude produziert nichts

Heute in Stunde 7 lernen wir NEU dazu:
    ✓ Neuer Rohstoff: Bevölkerung (fünfte Ressource)
    ✓ Neues Gebäude: Wohnhaus (produziert Bevölkerung, verbraucht Energie)
    ✓ Taste 7 für das Wohnhaus
    ✓ Bevölkerung wächst mit jedem Wohnhaus

Heute in Stunde 9 lernen wir NEU dazu (die Verbesserungsvorschläge der Schüler!):
    ✓ Gebäude abreißen können mit Rechtsklick — 50 % der Baukosten zurück
    ✓ Bei der Gebäude-Auswahl: Produktion + Verbrauch werden angezeigt
    ✓ Baumenü mit der Taste TAB (zeigt ALLE Gebäudetypen)
    ✓ Tooltip beim Hovern über ein Ressourcen-Icon
    ✓ Rote Meldung im Spiel, wenn zu wenig Rohstoffe zum Bauen da sind
    ✓ Stufenweise Freischaltung: Marktplatz ab 5 Bevölkerung, Wohnhaus ab 20 Holz

=============================================================================
"""

import pygame
import sys
import random       # Für zufällige Planeten-Generation
import gebaeude     # Gebäude-Modul aus Stunde 3 (+ Stunde 6)
import hud          # HUD-Modul aus Stunde 4 (+ Stunde 6)
import ressourcen   # Ressourcen-Modul aus Stunde 5 (+ Stunde 6)
import menu         # Baumenü-Modul — NEU in Stunde 9
import forschung    # Forschungs-Modul — Stunde 10/11
import handel       # Marktplatz- und NPC-Handel — Stunde 11
import spiel_menue  # Haupt-, Pausen- und Endmenü
import spielstand   # JSON-Speichern und -Laden
import achievements # Fortschritte und Punkte
import missionen    # Missionszentrale und Belohnungen
import ton          # Musik und Soundeffekte (Fortgeschrittener Kurs)
import logistik     # Strassen, Netz und Versorgung (Fortgeschrittener Kurs)
import gegner       # Feindliche Angriffe und Verteidigung (Fortgeschrittener Kurs)
import panel        # Schwebende Info-Fenster (Fortgeschrittener Kurs)
import einstellungen  # Einstellungsmenü mit eigener JSON-Datei
import ereignisse    # Zufallsereignisse (Systemausfall, Raumschiff, Meteoritenschauer)
import statistik     # Dauerhafte Spielstatistik (Hauptmenü)
import planeten      # Planeten, Rohstoffe, Kartenparameter (Wunschliste)
import kolonien      # Mehrere Kolonien auf verschiedenen Planeten (Wunschliste)


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: EINSTELLUNGEN (KONSTANTEN)
# ═════════════════════════════════════════════════════════════════════════════
# Konstanten sind Werte die sich während des Spiels NICHT ändern.
# Wir schreiben sie GROSS damit wir sofort sehen dass sie Konstanten sind.
# In Final Earth 2 gibt es viele verschiedene Einstellungen für die Welt.
# ═════════════════════════════════════════════════════════════════════════════

# ── Fenster-Einstellungen ──────────────────────────────────────────────────
# Das Fenster ist 1000 Pixel breit und 700 Pixel hoch.
# In Final Earth 2 ist das Fenster ähnlich groß, damit man viel sieht.
BILD_BREITE         = 1000
BILD_HOEHE          = 700
# Der Spielname steht NUR HIER. Fenstertitel, Hauptmenü und alle anderen
# Anzeigen holen den Namen aus dieser einen Konstanten.
SPIELNAME           = "Terra_Nova"
# Der Fenstertitel ist genau der Spielname - ohne Zusatz wie "wie Final Earth 2".
BILD_TITEL          = SPIELNAME
BILDER_PRO_SEKUNDE  = 60     # FPS — wie flüssig das Spiel läuft (Standard; im Einstellungsmenü änderbar)

# ── Karten-Einstellungen ────────────────────────────────────────────────────
# Die Karte ist 60×40 Kacheln groß — wie in Final Earth 2 eine schöne
# große Welt zum Erkunden.
KACHEL_GROESSE  = 48         # Jede Kachel ist 48×48 Pixel groß
KARTE_BREITE    = 60         # 60 Kacheln breit
KARTE_HOEHE     = 40         # 40 Kacheln hoch
KAMERA_SPEED    = 8          # Kamera-Scrolltempo in Pixeln (Standard bei 60 FPS; im Einstellungsmenü änderbar)

# ── Farben — Weltraum (Hintergrund) ───────────────────────────────────────
# Der schwarze Weltraum-Hintergrund aus Stunde 1.
# In Final Earth 2 siehst du das Weltall rund um den Planeten.
FARBE_SCHWARZ       = (0,   0,   0  )    # Reines Schwarz — der Weltraum
FARBE_WEISS         = (255, 255, 255)    # Für Texte und helle Sterne
FARBE_GELB_STERN    = (255, 240, 200)    # Warme Sterne
FARBE_BLAU_STERN    = (200, 220, 255)    # Blaue Sterne

# ── Farben — Planeten-Oberfläche (wie Final Earth 2) ──────────────────────
# Auf einem fremden Planeten gibt es verschiedene Bodenarten.
# Jede Bodenart hat eine eigene Farbe — wie in Final Earth 2!
# Hellbraun — normaler Erdboden (der häufigste Untergrund)
FARBE_ERDE_HELL     = (160, 140, 110)
# Dunkelbraun — fruchtbare Erde (gut für Pflanzen)
FARBE_ERDE_DUNKEL   = (130, 110, 80)
# Grün — Grasfläche (kommt später für Gebäude)
FARBE_GRAS          = (100, 160, 80)
# Dunkelgrau — Gestein / Felsen (schwer zu bearbeiten)
FARBE_GESTEIN       = (90,  90,  95)
# Sandfarbe — Wüstenfläche (wie in Final Earth 2)
FARBE_SAND          = (195, 185, 150)

# ── Farben — Gitterlinien ───────────────────────────────────────────────────
# Die Gitternetz-Linien zwischen den Kacheln.
# In Final Earth 2 siehst du ein feines Gitter auf der Oberfläche.
FARBE_GITTER       = (60, 55, 50)       # Dunkle Gitterlinien

# ── Farben — Text und HUD ──────────────────────────────────────────────────
# In Final Earth 2 gibt es eine Anzeige mit Informationen.
FARBE_TEXT_HELL     = (220, 220, 220)   # Helles Grau für Text
FARBE_TEXT_DUNKEL   = (150, 150, 160)   # Dunkleres Grau für Hinweise


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: PYGAME INITIALISIERUNG
# ═════════════════════════════════════════════════════════════════════════════
# pygame.init() startet alle Pygame-Module.
# Das passiert nur EINMAL ganz am Anfang — bevor alles andere kommt.
# Ohne diesen Schritt können wir keine Grafiken, Töne oder Eingaben nutzen.
# ═════════════════════════════════════════════════════════════════════════════

pygame.init()

# Das Spiel-Fenster erstellen — hier wird alles gezeichnet
fenster = pygame.display.set_mode((BILD_BREITE, BILD_HOEHE))

# Titel in der Fenster-Leiste (oben am Rand)
pygame.display.set_caption(BILD_TITEL)

# Ein Taktgeber (Clock) sorgt dafür dass das Spiel auf jedem Computer
# gleich schnell läuft — egal wie stark der Prozessor ist.
uhr = pygame.time.Clock()


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELZUSTAND (Globale Variablen)
# ═════════════════════════════════════════════════════════════════════════════
# Hier speichern wir den aktuellen Zustand des Spiels.
# In Final Earth 2 gibt es viele Werte: Kameraposition, Ressourcen, Gebäude...
# ═════════════════════════════════════════════════════════════════════════════

# ── Kamera-Position ─────────────────────────────────────────────────────────
# Die Kamera bestimmt welchen Ausschnitt der Karte wir sehen.
# 0, 0 = wir schauen auf die obere linke Ecke — Kachel (0, 0) liegt dann
# genau UNTER der Ressourcenleiste, keine Kachel wird vom HUD verdeckt.
kamera_x = 0
kamera_y = 0


def kamera_zeichnen_y():
    """Kamera-Y für das Weltzeichnen — um das HUD nach unten versetzt.

    Die Ressourcenleiste (hud.HUD_HOEHE Pixel hoch) liegt über den oberen
    Kacheln der Karte. Beim Zeichnen schieben wir die Welt deshalb um
    diese Höhe nach unten. Bei der Umrechnung Maus → Kachel kommt
    derselbe Versatz in umgekehrter Richtung zum Tragen:

        kachel_y = (maus_y + kamera_zeichnen_y()) // KACHEL_GROESSE
    """
    return kamera_y - hud.HUD_HOEHE

# ── Karten-Daten (wie in Final Earth 2) ────────────────────────────────────
# Die Karte ist ein 2D-Array (Liste von Listen).
# Jede Kachel hat einen Typ: 0 = Erde, 1 = Gras, 2 = Gestein, 3 = Sand
# In Final Earth 2 bestimmt der Bodentyp was du dort bauen kannst.
#
# karten_daten[zeile][spalte] gibt den Typ der Kachel an Position (spalte, zeile)
# Beispiel: karten_daten[5][3] = 0 → Kachel in Zeile 5, Spalte 3 ist Erde
karten_daten = []      # Wird in karte_generieren() befüllt

# ── Sterne für den Hintergrund ─────────────────────────────────────────────
# Wie in Final Earth 2 funkeln Sterne im Weltraum-Hintergrund.
# Jeder Stern hat eine x/y-Position und eine Helligkeit.
sterne_liste = []
_hintergrund_surface = None

# ── Ressourcen (ab Stunde 4) ────────────────────────────────────────────────
# In Final Earth 2 verwaltest du Ressourcen wie Gold, Energie und Nahrung.
# Diese Ressourcen werden ab Stunde 5 automatisch produziert und verbraucht.
# Das Dictionary speichert jede Ressource mit ihrem Namen und aktuellen Wert.
#
# Neu in Stunde 6: Der Rohstoff "stein" kommt dazu!
# Startwert = 20, damit der Steinmetz direkt nach dem Bau loslegen kann.
#
# Neu in Stunde 7: Der Rohstoff "bevoelkerung" kommt dazu!
# Startwert = 10 — damit der Spieler direkt ein paar Bewohner hat
# für die ersten Produktionsgebäude.
#
# Neu in Stunde 8: Der Rohstoff "nahrung" kommt dazu!
# Startwert = 50 — damit die ersten Wohnhäuser versorgt werden können.
# Neu in Stunde 10: Der Rohstoff "forschung" kommt dazu!
# Startwert = 0 — Forschungspunkte werden im Labor produziert.
ressourcen_dict = {"gold": 100, "energie": 50, "holz": 30, "stein": 20,
                   "bevoelkerung": 10, "nahrung": 50, "forschung": 0,
                   "kohle": 0, "eisen": 0, "roboter": 0, "stahl": 0}

# ├────────────────────────────────────────────────────────────────────────────
# │ STUNDE 3 — NEUE VARIABLEN                                                 │
# │                                                                           │
# │ In dieser Stunde kommen neue Variablen dazu:                              │
# │ Wir brauchen eine Liste für alle Gebäude, die auf der Karte stehen.       │
# │ Wir brauchen eine Variable, welches Gebäude gerade ausgewählt ist.        │
# │ Wir brauchen die Maus-Position und wo der Spieler geklickt hat.           │
# │                                                                           │
# │ Diese Variablen werden hier definiert (global):                          │
# └────────────────────────────────────────────────────────────────────────────┘

liste_gebaeude = []       # Alle Gebäude auf der Karte
# Neu in Stunde 7: 0=Basis, 1=Reaktor, 2=Farm, 3=Holzfaeller,
#                   4=Steinmetz, 5=Marktplatz, 6=Wohnhaus, 7=Labor
gebaeude_auswahl = 0      # Aktuell ausgewähltes Gebäude
_auswahl_kategorie = "1"  # Aktuelle Kategorie der Zifferntasten
_auswahl_position = 0     # Position innerhalb der Kategorie
_letztes_gebaeude = 0    # Schnellzugriff mit Taste 0
maus_x = 0                # Maus-X-Position auf dem Bildschirm

maus_y = 0                # Maus-Y-Position auf dem Bildschirm
klick_x = -1              # Zuletzt angeklickte Kachel (Spalte)
klick_y = -1              # Zuletzt angeklickte Kachel (Zeile)

# ── Tick-System (aus Stunde 5) ─────────────────────────────────────────────
# Der tick_zaehler zählt die Frames (Bilder pro Sekunde).
# Bei 60 FPS ist 1 Sekunde = 60 Frames.
# Wenn tick_zaehler 60 erreicht, rufen wir ressourcen_produzieren() auf
# und setzen den Zähler zurück auf 0.
# So läuft die Wirtschaft 1× pro Sekunde — nicht jeden Frame!
#
# Neu in Stunde 8: spiel_geschwindigkeit für Pause/Start/Beschleunigen
#   1 = normal (1× pro Sekunde)
#   0 = pausiert
#   2 = doppelt so schnell (alle 30 Frames)
tick_zaehler = 0
spiel_geschwindigkeit = 1   # Normal-Geschwindigkeit
_hilfe_offen = False         # Hilfe-Overlay ein/aus
_terraform_modus = False     # Stunde 11: freie Kachel in fruchtbaren Boden umwandeln

# ── Regelwerke und Spielzustände ─────────────────────────────────────────────
SIEG_BEVOELKERUNG = 30
SIEG_GEBAEUDE_TYP = 17  # Koloniezentrum
NIEDERLAGE_NULLRESSOURCE_TICKS = 12

REGELWERKE = {
    "standard": {
        "name": "Standard",
        "beschreibung": "30 Bewohner + Zentrum; 12 Ticks ohne Versorgung = Niederlage. Gegner greifen an.",
        "gegner_aktiv": True,
        "gegner_faktor": 1.0,
        "sieg_bevoelkerung": 30,
        "sieg_aktiv": True,
        "niederlage_ticks": 12,
    },
    "entspannt": {
        "name": "Entspannt",
        "beschreibung": "30 Bewohner + Zentrum; keine Niederlage und keine feindlichen Angriffe.",
        "gegner_aktiv": False,
        "gegner_faktor": 1.0,
        "sieg_bevoelkerung": 30,
        "sieg_aktiv": True,
        "niederlage_ticks": None,
    },
    "freies_spiel": {
        "name": "Freies Spiel",
        "beschreibung": "Keine automatische Sieg-/Niederlage; dafür ganz ohne feindliche Angriffe.",
        "gegner_aktiv": False,
        "gegner_faktor": 1.0,
        "sieg_bevoelkerung": 0,
        "sieg_aktiv": False,
        "niederlage_ticks": None,
    },
    "ueberleben": {
        "name": "Überleben",
        "beschreibung": "40 Bewohner + Zentrum; nur 6 Ticks ohne Versorgung. Gegner +30% stärker.",
        "gegner_aktiv": True,
        "gegner_faktor": 1.3,
        "sieg_bevoelkerung": 40,
        "sieg_aktiv": True,
        "niederlage_ticks": 6,
    },
}

# Mögliche Werte: hauptmenue, regelmenue, achievements, missionen, einstellungen, spiel, pause, sieg, niederlage
spiel_status = "hauptmenue"
_regel_auswahl = "standard"
_regelmenue_ziel = "hauptmenue"
_achievementmenue_ziel = "hauptmenue"
_missionenmenue_ziel = "hauptmenue"
_ziel_anzeige_sichtbar = True
spiel_ende_titel = ""
spiel_ende_grund = ""
_null_nahrung_ticks = 0
_null_energie_ticks = 0
_geschwindigkeit_vor_pause = 1


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: PLANETEN-GENERIERUNG
# ═════════════════════════════════════════════════════════════════════════════
# In Final Earth 2 wird jeder Planet zufällig generiert.
# Das bedeutet: Jedes Spiel sieht anders aus!
# Hier erstellen wir unsere eigene zufällige Planeten-Oberfläche.
# ═════════════════════════════════════════════════════════════════════════════

def karte_generieren(planet_id="erde"):
    """
    Generiert eine zufällige Planeten-Oberfläche.
    
    Wie in Final Earth 2 gibt es verschiedene Bodentypen:
    - Erde (0):   Der normale Boden — überall zu finden
    - Gras (1):   Fruchtbare Flächen — gut für Farmen
    - Gestein (2): Felsen — schwer zu bearbeiten aber wertvoll
    - Sand (3):   Wüstenfläche
    
    Die Karte wird zufällig erstellt, aber mit "Bereichen":
    - Große Flächen mit demselben Bodentyp (wie richtige Landschaften)
    - Kein wildes Durcheinander!
    """
    global karten_daten
    
    # Fortgeschrittener Kurs (Planeten): Flaechenverteilung je Planet.
    parameter = planeten.karten_parameter(planet_id)

    # Leere Karte erstellen (erstmal alles Erde)
    karten_daten = []
    for zeile in range(KARTE_HOEHE):
        neue_zeile = []
        for spalte in range(KARTE_BREITE):
            neue_zeile.append(0)  # 0 = Erde (Standard)
        karten_daten.append(neue_zeile)
    
    # ── Schritt 1: Große Gras-Flächen erzeugen ────────────────────────────
    anzahl_gras_flaechen = parameter["gras_flaechen"]
    for _ in range(anzahl_gras_flaechen):
        mitte_x = random.randint(5, KARTE_BREITE - 5)
        mitte_y = random.randint(5, KARTE_HOEHE - 5)
        radius = random.randint(4, 10)
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 1  # 1 = Gras
    
    # ── Schritt 2: Gesteins-Flächen erzeugen ──────────────────────────────
    anzahl_gestein_flaechen = parameter["gestein_flaechen"]
    for _ in range(anzahl_gestein_flaechen):
        mitte_x = random.randint(5, KARTE_BREITE - 5)
        mitte_y = random.randint(5, KARTE_HOEHE - 5)
        radius = random.randint(3, 7)
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 2  # 2 = Gestein
    
    # ── Schritt 3: Sand-Flächen erzeugen ──────────────────────────────────
    anzahl_sand_flaechen = parameter["sand_flaechen"]
    for _ in range(anzahl_sand_flaechen):
        mitte_x = random.randint(5, KARTE_BREITE - 5)
        mitte_y = random.randint(5, KARTE_HOEHE - 5)
        radius = random.randint(3, 8)
        for zeile in range(KARTE_HOEHE):
            for spalte in range(KARTE_BREITE):
                abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                if abstand < radius:
                    karten_daten[zeile][spalte] = 3  # 3 = Sand


def _hintergrund_aus_sternen_aufbauen():
    """Baut den statischen Sternen-Layer aus dem aktuellen Sternzustand."""
    global _hintergrund_surface
    _hintergrund_surface = pygame.Surface((BILD_BREITE, BILD_HOEHE))
    _hintergrund_surface.fill(FARBE_SCHWARZ)
    for stern in sterne_liste:
        if "farbe" in stern:
            stern_farbe = tuple(stern["farbe"])
        else:
            # Kompatibilität mit älteren Spielständen, die nur Helligkeit
            # gespeichert haben.
            helligkeit = int(stern.get("helligkeit", 180))
            stern_farbe = (helligkeit, helligkeit, helligkeit)
        pygame.draw.circle(
            _hintergrund_surface, stern_farbe,
            (int(stern["x"]), int(stern["y"])), int(stern.get("groesse", 1)))


def sterne_generieren():
    """Erzeugt Sterne und rendert den statischen Hintergrund einmalig.

    Die alte Version würfelte in jedem Frame für jeden Stern neue Farben aus.
    Das erzeugte unnötige Arbeit und ließ die Sterne flackern. Jetzt werden
    Position, Größe und Farbe einmalig beim Start der Welt festgelegt.
    """
    global sterne_liste
    sterne_liste = []
    for _ in range(150):
        helligkeit = random.randint(100, 255)
        farbvariante = random.randint(0, 9)
        if farbvariante < 2:
            stern_farbe = (helligkeit - 55, helligkeit - 35, helligkeit)
        elif farbvariante < 4:
            stern_farbe = (helligkeit, helligkeit - 15, helligkeit - 55)
        else:
            stern_farbe = (helligkeit, helligkeit, helligkeit)
        stern = {
            "x": random.randint(0, BILD_BREITE),
            "y": random.randint(0, BILD_HOEHE),
            "groesse": random.randint(1, 3),
            "farbe": stern_farbe,
        }
        sterne_liste.append(stern)
    _hintergrund_aus_sternen_aufbauen()


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: KARTE ZEICHNEN
# ═════════════════════════════════════════════════════════════════════════════

# Farben werden einmalig angelegt und nicht bei jedem Frame neu erstellt.
BODEN_FARBEN = {
    0: FARBE_ERDE_HELL,
    1: FARBE_GRAS,
    2: FARBE_GESTEIN,
    3: FARBE_SAND,
}


def karte_zeichnen():
    """Zeichnet nur den sichtbaren Ausschnitt der Planetenoberfläche.

    Früher wurden alle 60 x 40 = 2.400 Kacheln geprüft. Sichtbar sind je nach
    Kamera aber nur ungefähr 22 x 15 Kacheln. Die Start- und Endindizes sparen
    deshalb viele Schleifendurchläufe und unnötige Rechteckprüfungen.
    """
    # Einstellung "Gitterlinien": lässt sich im Einstellungsmenü abschalten.
    gitter_an = einstellungen.wert("gitter_an")
    erste_spalte = max(0, kamera_x // KACHEL_GROESSE)
    letzte_spalte = min(
        KARTE_BREITE,
        (kamera_x + BILD_BREITE) // KACHEL_GROESSE + 2,
    )
    # Die Welt beginnt unter der Ressourcenleiste (siehe kamera_zeichnen_y).
    kamera_anzeige_y = kamera_zeichnen_y()
    erste_zeile = max(0, kamera_anzeige_y // KACHEL_GROESSE)
    letzte_zeile = min(
        KARTE_HOEHE,
        (kamera_anzeige_y + BILD_HOEHE) // KACHEL_GROESSE + 2,
    )

    for zeile in range(erste_zeile, letzte_zeile):
        pixel_y = zeile * KACHEL_GROESSE - kamera_anzeige_y
        for spalte in range(erste_spalte, letzte_spalte):
            pixel_x = spalte * KACHEL_GROESSE - kamera_x
            kachel_rect = pygame.Rect(
                pixel_x, pixel_y, KACHEL_GROESSE, KACHEL_GROESSE)
            pygame.draw.rect(
                fenster, BODEN_FARBEN[karten_daten[zeile][spalte]], kachel_rect)
            if gitter_an:
                pygame.draw.rect(fenster, FARBE_GITTER, kachel_rect, 1)


# ── Gebäude zeichnen ────────────────────────────────────────────────────────
# Die Funktion gebaeude_zeichnen() wurde in Stunde 3 in das Modul
# gebaeude.py ausgelagert. Sie wird in der Spielschleife aufgerufen:
#   gebaeude.gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_y)
# Neu in Stunde 6: Die Funktion funktioniert automatisch für alle
# 5 Gebäudetypen, weil sie Farbe+Kürzel aus GEBAEUDE_TYPEN holt.


def kamera_begrenzen():
    """
    Verhindert dass die Kamera über den Rand der Karte scrollt.

    Nach oben endet die Kamera bei 0 — Kachel (0, 0) liegt dann genau
    unter der Ressourcenleiste (die Welt wird um HUD_HOEHE nach unten
    gezeichnet, siehe kamera_zeichnen_y). Nach unten darf die Kamera um
    HUD_HOEHE weiter scrollen, damit die letzte Kachelreihe noch unter
    der Leiste vollstaendig sichtbar wird.
    """
    global kamera_x, kamera_y
    karte_pixel_breite = KARTE_BREITE * KACHEL_GROESSE
    karte_pixel_hoehe  = KARTE_HOEHE  * KACHEL_GROESSE
    max_kamera_x = karte_pixel_breite - BILD_BREITE
    max_kamera_y = karte_pixel_hoehe - BILD_HOEHE + hud.HUD_HOEHE
    kamera_x = max(0, min(max_kamera_x, kamera_x))
    kamera_y = max(0, min(max_kamera_y, kamera_y))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: WELTRAUM-HINTERGRUND
# ═════════════════════════════════════════════════════════════════════════════

def hintergrund_zeichnen():
    """Blendet den einmalig gerenderten Weltraumhintergrund ein."""
    if _hintergrund_surface is None:
        _hintergrund_aus_sternen_aufbauen()
    fenster.blit(_hintergrund_surface, (0, 0))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HUD / ANZEIGE
# ═════════════════════════════════════════════════════════════════════════════
# Hinweis: Die alte Funktion info_text_zeichnen() wurde in Stunde 4 durch
# das HUD-Modul (hud.py) ersetzt. Alle Anzeigen laufen jetzt über:
#   hud.hud_zeichnen(ressourcen, gebaeude_auswahl, gebaeude.GEBAEUDE_TYPEN,
#                    kamera_x, kamera_y)
# ═════════════════════════════════════════════════════════════════════════════


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: GEBÄUDE-KATEGORIEN AUSWÄHLEN
# ═════════════════════════════════════════════════════════════════════════════

def kategorie_waehlen(kategorie_taste):
    """Wählt den ersten Eintrag einer Ziffern-Kategorie aus."""
    global gebaeude_auswahl, _auswahl_kategorie, _auswahl_position
    _auswahl_kategorie = str(kategorie_taste)
    _auswahl_position = 0
    gebaeude_auswahl = gebaeude.kategorie_auswahl(_auswahl_kategorie, _auswahl_position)
    print(f"Kategorie {_auswahl_kategorie}: {gebaeude.kategorie_name(_auswahl_kategorie)}")
    print(f"Gebäude-Auswahl: {gebaeude.GEBAEUDE_TYPEN[gebaeude_auswahl]['name']}")


def kategorie_weiter(delta):
    """Schaltet innerhalb der aktuell gewählten Kategorie weiter."""
    global gebaeude_auswahl, _auswahl_position
    _auswahl_position, gebaeude_auswahl = gebaeude.kategorie_weiter(
        _auswahl_kategorie, _auswahl_position, delta)
    print(f"Kategorie: {gebaeude.kategorie_name(_auswahl_kategorie)} | "
          f"Auswahl: {gebaeude.GEBAEUDE_TYPEN[gebaeude_auswahl]['name']}")


# ── Spielstände, Menüs, Regeln und Achievements ─────────────────────────────

def aktives_regelwerk():
    return REGELWERKE.get(_regel_auswahl, REGELWERKE["standard"])


def regelmenue_optionen():
    return [(regel_id, regel["name"], str(index + 1))
            for index, (regel_id, regel) in enumerate(REGELWERKE.items())] + [
                ("start", "Spiel starten", "Enter"),
                ("zurueck", "Zurück zum Hauptmenü", "Esc")]


def achievements_pruefen():
    """Aktualisiert alle Achievement-Ziele und meldet neue Erfolge."""
    neue = achievements.pruefen(
        ressourcen_dict, liste_gebaeude, karten_daten,
        forschung.anzahl_erforscht(),
        ressourcen_dict.get("wirtschafts_tick", 0),
        spiel_status,
        {name: ressourcen.maximaler_speicher(name)
         for name in ressourcen.SPEICHER_BASIS},
        profil=statistik.profil())
    if neue:
        erster_titel = achievements.titel(neue[0])
        zusatz = f" (+{achievements.eintrag(neue[0])['punkte']} Punkte)"
        hud.meldung_anzeigen("Achievement erreicht: " + erster_titel + zusatz)
        # Fortgeschrittener Kurs: Jedes neue Achievement bekommt einen Jingle.
        ton.sound_abspielen("achievement")


def gegner_ereignis_verarbeiten(ereignis):
    """Wertet die Rueckgabe von gegner.gegner_tick() aus (HUD + Erfolge).

    Die Sounds (Sirene, Abwehr-Jingle, Pluenderung) spielt bereits das
    gegner-Modul selbst ab - hier geht es nur um HUD-Text und Achievements.
    """
    if not isinstance(ereignis, dict):
        return
    art = ereignis.get("ereignis")
    if art == "warnung":
        hud.meldung_anzeigen(
            f"ACHTUNG: Angriff in {ereignis.get('warnzeit', 0)} Ticks! "
            f"Gegnerstaerke {ereignis.get('staerke', 0):.1f}")
    elif art == "abwehr_erfolg":
        belohnung = ereignis.get("belohnung", {})
        verluste = ereignis.get("verluste", {})
        hud.meldung_anzeigen(
            f"Angriff abgewehrt! +{belohnung.get('gold', 0)} Gold, "
            f"+{belohnung.get('forschung', 0)} Forschung "
            f"({verluste.get('verteidiger', 0)} Verteidiger, "
            f"{verluste.get('raumschiffe', 0)} Schiffe gefallen)")
        achievements.angriff_abgewehrt()
        achievements_pruefen()
    elif art == "ausgeraubt":
        verluste = ereignis.get("verluste", {})
        hud.meldung_anzeigen(
            "Kolonie ausgeraubt! 30 Prozent der Rohstoffe weg "
            f"({verluste.get('verteidiger', 0)} Verteidiger gefallen)")


def ereignis_meldung_verarbeiten(ereignis):
    """Zeigt die Textmeldung aus ereignisse.py im HUD an.

    Die Logik und die Sound-Effekte liegen komplett im Ereignismodul -
    hier steht nur noch der Text.
    """
    if not isinstance(ereignis, dict):
        return
    text = ereignis.get("text")
    if text:
        hud.meldung_anzeigen(text)


def menues_schliessen():
    """Schließt alle bisherigen Vollbild-Overlays vor dem Wechsel."""
    if menu.menu_ist_offen():
        menu.menu_umschalten()
    if forschung.forschung_menu_ist_offen():
        forschung.forschung_menu_umschalten()
    if handel.handelsmenue_ist_offen():
        handel.handelsmenue_umschalten()


def pause_oeffnen():
    """Friert die Wirtschaft ein und öffnet das ESC-Pausenmenü."""
    global spiel_status, spiel_geschwindigkeit, _geschwindigkeit_vor_pause
    global _hilfe_offen, _terraform_modus
    if spiel_status != "spiel":
        return
    _geschwindigkeit_vor_pause = max(1, spiel_geschwindigkeit)
    spiel_geschwindigkeit = 0
    spiel_status = "pause"
    _hilfe_offen = False
    _terraform_modus = False
    # Fortgeschrittener Kurs: Im Pausenmenue ist die Musik angehalten.
    ton.musik_pausieren()
    menues_schliessen()


def pause_schliessen():
    """Setzt das Spiel mit der Geschwindigkeit vor der Pause fort."""
    global spiel_status, spiel_geschwindigkeit
    if spiel_status == "pause":
        spiel_status = "spiel"
        spiel_geschwindigkeit = max(1, _geschwindigkeit_vor_pause)
        # Fortgeschrittener Kurs: Musik laeuft wieder (nur wenn sie an ist).
        ton.musik_fortsetzen()


def pause_umschalten():
    """Öffnet oder schließt die Pause mit einer einzigen Taste."""
    if spiel_status == "spiel":
        pause_oeffnen()
    elif spiel_status == "pause":
        pause_schliessen()


def _kosten_text(kosten):
    """Baut '120 Gold, 60 Energie, ...' aus einem Kosten-Dict."""
    return ", ".join(f"{int(menge)} {name.capitalize()}"
                     for name, menge in kosten.items())


def kolonie_wechseln(ziel_id):
    """Sichert die laufende Kolonie und laedt die Ziel-Kolonie (Pause: K)."""
    global _hintergrund_surface, _hilfe_offen, _terraform_modus
    if ziel_id == kolonien.aktuelle_id():
        hud.meldung_anzeigen("Wir sind schon auf dieser Kolonie.")
        return False
    if not kolonien.wechseln(ziel_id):
        hud.meldung_anzeigen("Diese Kolonie konnte nicht geladen werden.")
        return False
    # Abgeleitete Zustände der anderen Kolonie neu aufbauen.
    _hintergrund_surface = None      # Sternenhimmel der anderen Kolonie
    _hilfe_offen = False
    _terraform_modus = False
    menues_schliessen()
    logistik.netz_aktualisieren(liste_gebaeude)
    panels_anordnen()
    panel.zustand_zuruecksetzen()
    kamera_begrenzen()
    hud.meldung_anzeigen(f"Gewechselt zu: {kolonien.aktuelle_beschreibung()}")
    return True


def kolonie_naechste_wechseln():
    """Wechselt zur nächsten Kolonie in der Liste (Pause: K)."""
    ids = kolonien.alle_ids()
    if len(ids) < 2:
        hud.meldung_anzeigen(
            "Erst eine Kolonie vorhanden - mit G gründest du eine zweite.")
        return False
    ziel = ids[(ids.index(kolonien.aktuelle_id()) + 1) % len(ids)]
    return kolonie_wechseln(ziel)


def kolonie_gruenden():
    """Gründet die nächste freie Kolonie auf einem neuen Planeten (Pause: G)."""
    ziel = kolonien.naechster_freier_planet()
    if ziel is None:
        hud.meldung_anzeigen("Alle spielbaren Planeten sind bereits besiedelt.")
        return False
    kosten = planeten.gruendungskosten(ziel)
    fehlend = [f"{int(menge)} {name.capitalize()}"
               for name, menge in kosten.items()
               if ressourcen_dict.get(name, 0) < menge]
    if fehlend:
        hud.meldung_anzeigen("Gründung braucht: " + ", ".join(fehlend))
        return False
    for name, menge in kosten.items():
        ressourcen_dict[name] = ressourcen_dict.get(name, 0) - menge
    # Reihenfolge ist wichtig: alte Kolonie sichern, frische Welt bauen,
    # dann die neue Kolonie in der Liste registrieren.
    kolonien.stand_merken()
    neues_spiel_starten(planet_id=ziel, partei_neustart=False)
    if not kolonien.gruenden(ziel):
        for name, menge in kosten.items():          # Kosten zurueck
            ressourcen_dict[name] = ressourcen_dict.get(name, 0) + menge
        hud.meldung_anzeigen(
            f"Kolonie auf dem {planeten.name(ziel)} klappt nicht.")
        return False
    hud.meldung_anzeigen(
        f"Neue Kolonie: {kolonien.aktuelle_beschreibung()} "
        f"(Kosten: {_kosten_text(kosten)})")
    return True


def _neue_ressourcen(planet_id="erde"):
    ressourcen_neu = {"gold": 100, "energie": 50, "holz": 30, "stein": 20,
                      "bevoelkerung": 10, "nahrung": 50, "forschung": 0,
                      "kohle": 0, "eisen": 0, "roboter": 0, "stahl": 0,
                      "verteidiger": 0, "raumschiffe": 0, "zufriedenheit": 0.0}
    # Fortgeschrittener Kurs (Planeten): Startvorräte des Planeten legen
    # sich ueber die Grundwerte (der Mond beginnt knapper als die Erde).
    ressourcen_neu.update(planeten.startressourcen(planet_id))
    return ressourcen_neu


def neues_spiel_starten(planet_id="erde", partei_neustart=True):
    """Erzeugt eine frische Welt auf dem Planeten planet_id.

    partei_neustart=True  - ganz neues Spiel: Statistik, Ereignisse,
                             Gegner, Handel und Kolonie-Liste starten neu.
    partei_neustart=False - nur die WELT wird neu gebaut; so entsteht eine
                             weitere Kolonie auf einem anderen Planeten.
    """
    global karten_daten, sterne_liste, ressourcen_dict, liste_gebaeude
    global kamera_x, kamera_y, tick_zaehler, spiel_geschwindigkeit
    global gebaeude_auswahl, _auswahl_kategorie, _auswahl_position
    global _letztes_gebaeude, _hilfe_offen, _terraform_modus
    global _ziel_anzeige_sichtbar
    global spiel_status, spiel_ende_titel, spiel_ende_grund
    global _null_nahrung_ticks, _null_energie_ticks, _geschwindigkeit_vor_pause

    karte_generieren(planet_id)
    sterne_generieren()
    ressourcen_dict = _neue_ressourcen(planet_id)
    liste_gebaeude = []
    kamera_x = 0
    kamera_y = 0
    tick_zaehler = 0
    spiel_geschwindigkeit = 1
    gebaeude_auswahl = 0
    _auswahl_kategorie = "1"
    _auswahl_position = 0
    _letztes_gebaeude = 0
    _hilfe_offen = False
    _terraform_modus = False
    _ziel_anzeige_sichtbar = True
    # Schwebende Fenster: Standardpositionen setzen, alles einblenden.
    panels_anordnen()
    panel.zustand_zuruecksetzen()
    spiel_ende_titel = ""
    spiel_ende_grund = ""
    _null_nahrung_ticks = 0
    _null_energie_ticks = 0
    _geschwindigkeit_vor_pause = 1
    forschung.forschung_zuruecksetzen()
    ressourcen.zustand_importieren({})
    # Fortgeschrittener Kurs (Planeten): Rohstoff-Boni des Planeten
    # gehoeren zur frischen Kolonie und stehen sofort bereit.
    ressourcen.planeten_faktoren_setzen(planeten.rohstoffe(planet_id))
    # Fortgeschrittener Kurs (Logistik): Netz und Ansicht zuruecksetzen
    # und fuer die leere Kolonie sofort neu berechnen.
    logistik.zustand_zuruecksetzen()
    logistik.netz_aktualisieren(liste_gebaeude)
    if partei_neustart:
        handel.handel_zuruecksetzen()
        # Fortgeschrittener Kurs (Gegner): neues Spiel = Friedenszeit von vorn.
        gegner.zustand_zuruecksetzen()
        # Zufallsereignisse starten neu, die Statistik zaehlt die Partie.
        ereignisse.ereignisse_zuruecksetzen()
        statistik.neue_partie()
        # Neue Partie = frische Kolonie-Liste mit dem Startplaneten.
        kolonien.zuruecksetzen(planet_id)
    spiel_status = "spiel"
    # Fortgeschrittener Kurs: Nach dem Endmenue darf die Musik wieder laufen.
    ton.musik_starten()
    # War die Musik noch aus der Pause angehalten, läuft sie jetzt wieder.
    ton.musik_fortsetzen()


def spielstand_speichern():
    """Speichert alle Kolonien und zeigt das Ergebnis im HUD an."""
    # Fortgeschrittener Kurs (Planeten): aktive Kolonie zuerst sichern,
    # dann den kompletten Kolonie-Bestand mitspeichern.
    kolonien.stand_merken()
    erfolg, meldung = spielstand.speichern(
        karten_daten, sterne_liste, ressourcen_dict, liste_gebaeude,
        kamera_x, kamera_y, tick_zaehler, max(1, spiel_geschwindigkeit),
        _auswahl_kategorie, _auswahl_position, gebaeude_auswahl,
        _letztes_gebaeude, spiel_status,
        {"nahrung": _null_nahrung_ticks, "energie": _null_energie_ticks},
        _regel_auswahl, kolonien_daten=kolonien.zustand_fuer_spielstand())
    print(meldung)
    hud.meldung_anzeigen(meldung)
    return erfolg


def spielstand_laden():
    """Lädt eine Welt, validiert Grunddaten und startet sie im Spielmodus."""
    global karten_daten, sterne_liste, ressourcen_dict, liste_gebaeude
    global kamera_x, kamera_y, tick_zaehler, spiel_geschwindigkeit
    global gebaeude_auswahl, _auswahl_kategorie, _auswahl_position
    global _letztes_gebaeude, _hilfe_offen, _terraform_modus
    global _ziel_anzeige_sichtbar
    global spiel_status, spiel_ende_titel, spiel_ende_grund
    global _null_nahrung_ticks, _null_energie_ticks, _regel_auswahl
    global _hintergrund_surface

    daten, meldung = spielstand.laden()
    if daten is None:
        return False, meldung
    try:
        karte = daten["karten_daten"]
        if (not isinstance(karte, list) or len(karte) != KARTE_HOEHE or
                any(not isinstance(zeile, list) or len(zeile) != KARTE_BREITE
                    for zeile in karte)):
            return False, "Die Karte im Spielstand ist ungültig."
        gebaeude_liste = daten["gebaeude"]
        if not isinstance(gebaeude_liste, list):
            return False, "Die Gebäudeliste im Spielstand ist ungültig."
        for ein_gebaeude in gebaeude_liste:
            if not isinstance(ein_gebaeude, dict) or "typ" not in ein_gebaeude:
                return False, "Ein Gebäude im Spielstand ist ungültig."
    except (KeyError, TypeError):
        return False, "Der Spielstand ist unvollständig."

    # Fortgeschrittener Kurs (Planeten): Kolonie-Liste uebernehmen.
    kolonien.zustand_uebernehmen(daten.get("kolonien"))

    karten_daten = karte
    sterne_liste = daten.get("sterne_liste") or sterne_liste
    _hintergrund_surface = None
    ressourcen_dict = dict(daten.get("ressourcen", {}))
    # Alte Spielstände kennen Zufriedenheit noch nicht. Dann startet die
    # Kolonie neutral bei 0 statt mit einem fehlenden Dictionary-Schlüssel.
    ressourcen_dict.setdefault("zufriedenheit", 0.0)
    # Fortgeschrittener Kurs (Gegner): alte Spielstaende kennen die
    # Militaerressourcen noch nicht - dann startet die Kolonie ohne beide.
    ressourcen_dict.setdefault("verteidiger", 0)
    ressourcen_dict.setdefault("raumschiffe", 0)
    ressourcen.zufriedenheit_begrenzen(ressourcen_dict)
    liste_gebaeude = gebaeude_liste
    kamera = daten.get("kamera", {})
    kamera_x = int(kamera.get("x", 0))
    kamera_y = int(kamera.get("y", 0))
    tick_zaehler = int(daten.get("tick_zaehler", 0))
    spiel_geschwindigkeit = max(1, int(daten.get("spiel_geschwindigkeit", 1)))
    auswahl = daten.get("auswahl", {})
    _auswahl_kategorie = str(auswahl.get("kategorie", "1"))
    _auswahl_position = int(auswahl.get("position", 0))
    gebaeude_auswahl = int(auswahl.get("gebaeude", 0))
    _letztes_gebaeude = int(auswahl.get("letztes_gebaeude", 0))
    geladene_regel = str(daten.get("regel_auswahl", "standard"))
    _regel_auswahl = geladene_regel if geladene_regel in REGELWERKE else "standard"
    _hilfe_offen = False
    _terraform_modus = False
    _ziel_anzeige_sichtbar = True
    panels_anordnen()
    panel.sichtbar_setzen("ziel", True)
    spiel_ende_titel = ""
    spiel_ende_grund = ""
    versorgungszaehler = daten.get("versorgungszaehler", {})
    try:
        _null_nahrung_ticks = max(0, int(versorgungszaehler.get("nahrung", 0)))
        _null_energie_ticks = max(0, int(versorgungszaehler.get("energie", 0)))
    except (AttributeError, TypeError, ValueError):
        _null_nahrung_ticks = 0
        _null_energie_ticks = 0
    # Fortgeschrittener Kurs (Logistik): Nach dem Laden muss das Netz aus
    # den geladenen Gebaeuden neu berechnet werden.
    logistik.netz_aktualisieren(liste_gebaeude)
    kamera_begrenzen()
    menues_schliessen()
    spiel_status = "spiel"
    return True, meldung


def spielstatus_pruefen():
    """Prüft nach jedem Wirtschaftstick Sieg und Niederlage."""
    global spiel_status, spiel_ende_titel, spiel_ende_grund
    global _null_nahrung_ticks, _null_energie_ticks
    if spiel_status != "spiel":
        return

    regel = aktives_regelwerk()
    hat_koloniezentrum = any(g.get("typ") == SIEG_GEBAEUDE_TYP
                             for g in liste_gebaeude)
    bevoelkerung = ressourcen_dict.get("bevoelkerung", 0)
    if (regel["sieg_aktiv"] and hat_koloniezentrum and
            bevoelkerung >= regel["sieg_bevoelkerung"]):
        spiel_status = "sieg"
        # Fortgeschrittener Kurs: Musik aus, dafuer einmal der Sieg-Sound.
        ton.musik_stoppen()
        ton.sound_abspielen("sieg")
        spiel_ende_titel = "KOLONIE GERETTET"
        spiel_ende_grund = (f"Deine Kolonie hat {int(bevoelkerung)} Bewohner "
                            f"und ein Koloniezentrum erreicht ({regel['name']}).")
        statistik.partie_beendet("sieg")
        achievements_pruefen()
        menues_schliessen()
        return

    if regel["niederlage_ticks"] is None:
        _null_nahrung_ticks = 0
        _null_energie_ticks = 0
        achievements_pruefen()
        return

    if ressourcen_dict.get("nahrung", 0) <= 0:
        _null_nahrung_ticks += 1
    else:
        _null_nahrung_ticks = 0
    if ressourcen_dict.get("energie", 0) <= 0:
        _null_energie_ticks += 1
    else:
        _null_energie_ticks = 0

    if _null_nahrung_ticks >= regel["niederlage_ticks"]:
        spiel_status = "niederlage"
        # Fortgeschrittener Kurs: Musik aus, dafuer der Verlierer-Sound.
        ton.musik_stoppen()
        ton.sound_abspielen("niederlage")
        spiel_ende_titel = "KOLONIE VERLOREN"
        spiel_ende_grund = "Die Nahrung ist zu lange auf 0 gefallen."
        statistik.partie_beendet("niederlage")
        statistik.partie_beendet("niederlage")
        menues_schliessen()
    elif _null_energie_ticks >= regel["niederlage_ticks"]:
        spiel_status = "niederlage"
        ton.musik_stoppen()
        ton.sound_abspielen("niederlage")
        spiel_ende_titel = "KOLONIE VERLOREN"
        spiel_ende_grund = "Die Energie ist zu lange auf 0 gefallen."
        statistik.partie_beendet("niederlage")
        statistik.partie_beendet("niederlage")
        menues_schliessen()
    achievements_pruefen()


def panels_anordnen():
    """Setzt die Standardpositionen der schwebenden Info-Fenster.

    Alle Fenster sitzen unterhalb des HUD-Balkens und ueberlappen sich
    nicht — genau das war im Screenshot das Problem. Danach bleiben sie
    frei verschiebbar; Taste L stellt diese Anordnung wieder her.
    """
    panel.initialisieren(fenster)
    breite = fenster.get_width()
    oben = hud.HUD_HOEHE + 8
    panel.standard_setzen("uebersicht", 14, oben)
    panel.standard_setzen("verteidigung", breite - 238, oben)
    panel.standard_setzen("ziel", breite - 312, oben + 158)
    panel.standard_setzen("bauinfo", max(10, breite // 2 - 260), 520)


def ziel_schalter_rect():
    """Klickbereich zum Ein-/Ausblenden der Zielanzeige.

    Sichtbar: die Titelzeile des Fensters (dort sitzen auch "-" und "X").
    Ausgeblendet: ein kleiner Knopf, der die Ziele wieder oeffnet.
    """
    if panel.ist_sichtbar("ziel"):
        titel = panel.titel_rect("ziel")
        if titel is not None:
            return titel
    return pygame.Rect(BILD_BREITE - 118, 54, 100, 26)


def ziel_anzeige_umschalten():
    """Schaltet die Zielanzeige um, ohne den Spielzustand zu verändern."""
    global _ziel_anzeige_sichtbar
    _ziel_anzeige_sichtbar = panel.umschalten("ziel")
    return _ziel_anzeige_sichtbar


def ziel_zeichnen():
    """Zeigt Sieg-/Niederlageziele als schwebendes Fenster.

    Das Fenster laesst sich an der Titelzeile verschieben, mit "-"
    minimieren und mit "X" ausblenden (Taste O holt es zurueck). Frueher
    lag es fest im HUD-Balken und hat die Ressourcen verdeckt.
    """
    global _ziel_anzeige_sichtbar
    if not panel.ist_sichtbar("ziel"):
        _ziel_anzeige_sichtbar = False
        # Kleiner Knopf, damit man die Anzeige wiederfindet (Taste O).
        mini = ziel_schalter_rect()
        pygame.draw.rect(fenster, (8, 14, 28), mini, border_radius=5)
        pygame.draw.rect(fenster, (75, 110, 150), mini, 1, border_radius=5)
        schrift = pygame.font.Font(None, 17)
        fenster.blit(schrift.render("O: Ziele", True, (190, 220, 245)),
                     (mini.left + 8, mini.top + 5))
        return

    _ziel_anzeige_sichtbar = True
    schrift = pygame.font.Font(None, 19)
    regel = aktives_regelwerk()
    bevoelkerung = int(ressourcen_dict.get("bevoelkerung", 0))
    hat_zentrum = any(g.get("typ") == SIEG_GEBAEUDE_TYP for g in liste_gebaeude)
    if regel["sieg_aktiv"]:
        zieltext = f"{regel['name']}: {regel['sieg_bevoelkerung']} Bew. + Zentrum"
        status = (f"Fortschritt: {bevoelkerung}/{regel['sieg_bevoelkerung']} | "
                  f"Zentrum: {'ja' if hat_zentrum else 'nein'}")
    else:
        zieltext = "Freies Spiel: kein Endziel"
        status = "Baue und experimentiere ohne Zeitdruck."
    zeilen_inhalt = [(zieltext, (235, 240, 255)), (status, (160, 215, 245))]
    if (regel["niederlage_ticks"] is not None and
            (_null_nahrung_ticks or _null_energie_ticks)):
        zeilen_inhalt.append(("Versorgung kritisch!", (255, 180, 100)))

    def inhalt(x0, y0, b, h):
        """Malt die Ziel-Zeilen in das Fenster."""
        y = y0
        for text, farbe in zeilen_inhalt:
            fenster.blit(schrift.render(text, True, farbe), (x0, y))
            y += 20

    panel.zeichnen("ziel", "Ziel  [O]", 300, len(zeilen_inhalt) * 20 + 2,
                   inhalt, standard_x=BILD_BREITE - 312,
                   standard_y=hud.HUD_HOEHE + 8)


def menue_titel():
    """Titel des Hauptmenüs: SPIELNAME in Großbuchstaben, wenn das gefahrlos ist.

    Großschreibung kann Zeichen verändern (ß wird zu SS). Deshalb wird der
    Name nur dann in Versalien gezeigt, wenn er sich abgesehen von der
    Groß-/Kleinschreibung nicht ändert — sonst bleibt er wie geschrieben.
    """
    gross = SPIELNAME.upper()
    return gross if gross.lower() == SPIELNAME.lower() else SPIELNAME


def hauptmenue_zeichnen():
    info = [
        f"Aktive Regeln: {aktives_regelwerk()['name']} - mit R im Hauptmenü änderbar",
        "Im Spiel: ESC öffnet die Pause. A zeigt Achievements, M die Missionen.",
    ]
    optionen = [("neues_spiel", "Neues Spiel", "Enter"),
                ("regelmenue", "Spielregeln auswählen", "R"),
                ("achievements", "Achievements anzeigen", "A"),
                ("missionen", "Missionszentrale", "M"),
                ("statistik", "Gesamtstatistik", "T"),
                ("einstellungen", "Einstellungen", "E"),
                ("laden", "Spielstand laden", "L"),
                ("beenden", "Spiel beenden", "Esc")]
    deaktiviert = set() if spielstand.existiert() else {"laden"}
    spiel_menue.menu_zeichnen(menue_titel(), "Baue eine sichere Heimat auf dem fremden Planeten.",
                              optionen, deaktiviert, info, (90, 190, 255))


def regelmenue_zeichnen():
    optionen = []
    for regel_id, regel in REGELWERKE.items():
        markierung = "✓ " if regel_id == _regel_auswahl else "  "
        optionen.append((regel_id, markierung + regel["name"], str(len(optionen) + 1)))
    optionen.extend([("start", "Mit dieser Regel starten", "Enter"),
                     ("zurueck", "Zurück zum Hauptmenü", "Esc")])
    regel = aktives_regelwerk()
    info = [
        f"Ausgewählt: {regel['name']}",
        regel["beschreibung"],
        "1–4 wählen eine Regel; Enter übernimmt die Auswahl.",
    ]
    spiel_menue.menu_zeichnen("SPIELREGELN", "Du entscheidest, wie viel Druck die Kolonie bekommt.",
                              optionen, info_zeilen=info, akzent=(170, 140, 255))


def achievements_zeichnen():
    achievements.menu_zeichnen()


def missionen_kontext():
    """Baut die aktuellen Werte für die Missionsprüfung zusammen."""
    zaehler = missionen.zustand_exportieren().get("zaehler", {})
    gebaeude_typen = {}
    for ein_gebaeude in liste_gebaeude:
        schluessel = f"gebaeude_typ_{ein_gebaeude.get('typ', -1)}"
        gebaeude_typen[schluessel] = gebaeude_typen.get(schluessel, 0) + 1
    zaehler.update(gebaeude_typen)
    zaehler["gebaeude_gesamt"] = max(
        zaehler.get("gebaeude_gesamt", 0), len(liste_gebaeude))
    zaehler["bevoelkerung"] = ressourcen_dict.get("bevoelkerung", 0)
    zaehler["stahl"] = ressourcen_dict.get("stahl", 0)
    zaehler["roboter"] = ressourcen_dict.get("roboter", 0)
    zaehler["zufriedenheit"] = ressourcen_dict.get("zufriedenheit", 0)
    zaehler["forschungen"] = forschung.anzahl_erforscht()
    zaehler["handelsaktionen"] = handel.handel_aktionszahl()
    zaehler["terraformierungen"] = missionen.zustand_exportieren().get("zaehler", {}).get("terraformierungen", 0)
    zaehler["wirtschafts_ticks"] = ressourcen_dict.get("wirtschafts_tick", 0)
    return zaehler


def missionen_pruefen():
    """Prüft Missionen und zahlt jede Belohnung genau einmal aus."""
    neue = missionen.pruefen(missionen_kontext())
    if not neue:
        return
    for mission_id in neue:
        belohnung = missionen.belohnung(mission_id)
        for ressourcen_name, menge in belohnung.items():
            ressourcen_dict[ressourcen_name] = (
                ressourcen_dict.get(ressourcen_name, 0) + menge)
        name = missionen.titel(mission_id)
        belohnung_text = ", ".join(
            f"+{menge} {ressourcen_name}"
            for ressourcen_name, menge in belohnung.items())
        hud.meldung_anzeigen(f"Mission erledigt: {name} ({belohnung_text})")
    # Fortgeschrittener Kurs: kurzer Jingle, sobald mindestens eine Mission
    # in diesem Aufruf abgeschlossen wurde.
    ton.sound_abspielen("mission_erledigt")
    ressourcen.ressourcen_begrenzen(ressourcen_dict)


def missionen_zeichnen():
    missionen.menu_zeichnen(missionen_kontext())


def pausemenue_zeichnen():
    optionen = [("fortsetzen", "Fortsetzen", "Esc / P / Enter"),
                ("kolonie_wechseln", "Zu anderer Kolonie wechseln", "K"),
                ("kolonie_gruenden", "Neue Kolonie gründen", "G"),
                ("speichern", "Spielstand speichern", "S"),
                ("achievements", "Achievements anzeigen", "A"),
                ("missionen", "Missionszentrale", "I"),
                ("einstellungen", "Einstellungen", "E"),
                ("hauptmenue", "Zum Hauptmenü", "M"),
                ("beenden", "Spiel beenden", "Q")]
    kosten = planeten.gruendungskosten()
    spiel_menue.menu_zeichnen("PAUSE", "Das Spiel steht still.", optionen, info_zeilen=[
        f"Aktuelle Kolonie: {kolonien.aktuelle_beschreibung()}",
        f"Neue Kolonie gründen kostet: {_kosten_text(kosten)}",
        "Beim Wechsel zum Hauptmenü bleibt der Spielstand erhalten.",
    ], akzent=(255, 205, 95))


def endmenue_zeichnen():
    optionen = [("neues_spiel", "Neues Spiel", "N / Enter"),
                ("hauptmenue", "Zum Hauptmenü", "M"),
                ("beenden", "Spiel beenden", "Esc")]
    farbe = (110, 225, 145) if spiel_status == "sieg" else (245, 105, 105)
    spiel_menue.menu_zeichnen(spiel_ende_titel, spiel_ende_grund, optionen,
                              info_zeilen=["N oder Enter startet eine neue Kolonie."],
                              akzent=farbe)


def _hauptmenue_aktion(aktion):
    global spiel_status, _regelmenue_ziel, _achievementmenue_ziel, _missionenmenue_ziel
    if aktion == "neues_spiel":
        neues_spiel_starten()
        return True
    if aktion == "einstellungen":
        einstellungen.ziel_setzen("hauptmenue")
        einstellungen.menue_oeffnen()
        spiel_status = "einstellungen"
        return True
    if aktion == "regelmenue":
        _regelmenue_ziel = "hauptmenue"
        spiel_status = "regelmenue"
        return True
    if aktion == "achievements":
        _achievementmenue_ziel = "hauptmenue"
        spiel_status = "achievements"
        return True
    if aktion == "missionen":
        _missionenmenue_ziel = "hauptmenue"
        spiel_status = "missionen"
        return True
    if aktion == "statistik":
        spiel_status = "statistik"
        return True
    if aktion == "laden":
        erfolg, meldung = spielstand_laden()
        if not erfolg:
            print(meldung)
        return erfolg
    if aktion == "beenden":
        return False
    return True


def hauptmenue_verarbeiten():
    """Verarbeitet Tastatur und Maus im Hauptmenü."""
    global spiel_status, _regelmenue_ziel, _achievementmenue_ziel, _missionenmenue_ziel
    optionen = [("neues_spiel", "Neues Spiel", "Enter"),
                ("regelmenue", "Spielregeln auswählen", "R"),
                ("achievements", "Achievements anzeigen", "A"),
                ("missionen", "Missionszentrale", "M"),
                ("statistik", "Gesamtstatistik", "T"),
                ("einstellungen", "Einstellungen", "E"),
                ("laden", "Spielstand laden", "L"),
                ("beenden", "Spiel beenden", "Esc")]
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_ESCAPE:
                return False
            if ereignis.key in (pygame.K_RETURN, pygame.K_SPACE):
                neues_spiel_starten()
                return True
            if ereignis.key == pygame.K_r:
                _regelmenue_ziel = "hauptmenue"
                spiel_status = "regelmenue"
                return True
            if ereignis.key == pygame.K_a:
                _achievementmenue_ziel = "hauptmenue"
                spiel_status = "achievements"
                return True
            if ereignis.key == pygame.K_m:
                _missionenmenue_ziel = "hauptmenue"
                spiel_status = "missionen"
                return True
            if ereignis.key == pygame.K_t:
                return _hauptmenue_aktion("statistik")
            if ereignis.key == pygame.K_e:
                return _hauptmenue_aktion("einstellungen")
            if ereignis.key == pygame.K_l and spielstand.existiert():
                erfolg, meldung = spielstand_laden()
                if not erfolg:
                    print(meldung)
                return True
        if ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1:
            aktion = spiel_menue.aktion_fuer_klick(
                ereignis.pos, optionen,
                set() if spielstand.existiert() else {"laden"})
            if aktion is not None:
                return _hauptmenue_aktion(aktion)
    return True


def regelmenue_verarbeiten():
    """Verarbeitet Auswahl und Rückkehr im Regelmenü."""
    global spiel_status, _regel_auswahl
    optionen = regelmenue_optionen()
    regel_ids = list(REGELWERKE)
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key == pygame.K_ESCAPE:
                spiel_status = _regelmenue_ziel
                return True
            if pygame.K_1 <= ereignis.key <= pygame.K_4:
                _regel_auswahl = regel_ids[ereignis.key - pygame.K_1]
            elif ereignis.key in (pygame.K_RETURN, pygame.K_SPACE):
                neues_spiel_starten()
                return True
        if ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1:
            aktion = spiel_menue.aktion_fuer_klick(ereignis.pos, optionen)
            if aktion in REGELWERKE:
                _regel_auswahl = aktion
            elif aktion == "start":
                neues_spiel_starten()
                return True
            elif aktion == "zurueck":
                spiel_status = _regelmenue_ziel
                return True
    return True


def achievementsmenue_verarbeiten():
    """Verarbeitet Rückkehr aus der Achievement-Übersicht."""
    global spiel_status
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key in (pygame.K_ESCAPE, pygame.K_a, pygame.K_RETURN, pygame.K_SPACE):
                spiel_status = _achievementmenue_ziel
                return True
        if (ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1 and
                achievements.zurueck_rect().collidepoint(ereignis.pos)):
            spiel_status = _achievementmenue_ziel
            return True
    return True


def missionenmenue_verarbeiten():
    """Verarbeitet die Rückkehr aus der Missionszentrale."""
    global spiel_status
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key in (pygame.K_ESCAPE, pygame.K_m, pygame.K_RETURN, pygame.K_SPACE):
                spiel_status = _missionenmenue_ziel
                return True
        if (ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1 and
                missionen.zurueck_rect().collidepoint(ereignis.pos)):
            spiel_status = _missionenmenue_ziel
            return True
    return True


def statistikmenue_verarbeiten():
    """Verarbeitet die Rueckkehr aus der Gesamtstatistik."""
    global spiel_status
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key in (pygame.K_ESCAPE, pygame.K_t, pygame.K_RETURN, pygame.K_SPACE):
                spiel_status = "hauptmenue"
                return True
        if (ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1 and
                statistik.zurueck_rect().collidepoint(ereignis.pos)):
            spiel_status = "hauptmenue"
            return True
    return True


def einstellungen_verarbeiten():
    """Verarbeitet das Einstellungsmenü (Tastatur, Maus, Slider-Ziehen)."""
    global spiel_status
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            ergebnis = einstellungen.taste(ereignis.key)
            if ergebnis == "zurueck":
                spiel_status = einstellungen.ziel()
                return True
        elif ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1:
            ergebnis = einstellungen.mausklick(ereignis.pos)
            if ergebnis == "zurueck":
                spiel_status = einstellungen.ziel()
                return True
        elif ereignis.type == pygame.MOUSEMOTION:
            einstellungen.maus_ziehen(ereignis.pos, ereignis.buttons[0] == 1)
        elif ereignis.type == pygame.MOUSEBUTTONUP and ereignis.button == 1:
            einstellungen.maus_loslassen()
    return True


def pausemenue_verarbeiten():
    """Verarbeitet das ESC-Pausenmenü."""
    global spiel_status, _achievementmenue_ziel, _missionenmenue_ziel
    optionen = [("fortsetzen", "Fortsetzen", "Esc / P / Enter"),
                ("kolonie_wechseln", "Zu anderer Kolonie wechseln", "K"),
                ("kolonie_gruenden", "Neue Kolonie gründen", "G"),
                ("speichern", "Spielstand speichern", "S"),
                ("achievements", "Achievements anzeigen", "A"),
                ("missionen", "Missionszentrale", "I"),
                ("einstellungen", "Einstellungen", "E"),
                ("hauptmenue", "Zum Hauptmenü", "M"),
                ("beenden", "Spiel beenden", "Q")]
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key in (pygame.K_ESCAPE, pygame.K_p,
                                 pygame.K_RETURN, pygame.K_SPACE):
                pause_schliessen()
                return True
            if ereignis.key == pygame.K_s:
                spielstand_speichern()
            elif ereignis.key == pygame.K_a:
                _achievementmenue_ziel = "pause"
                spiel_status = "achievements"
                return True
            elif ereignis.key == pygame.K_i:
                _missionenmenue_ziel = "pause"
                spiel_status = "missionen"
                return True
            elif ereignis.key == pygame.K_e:
                einstellungen.ziel_setzen("pause")
                einstellungen.menue_oeffnen()
                spiel_status = "einstellungen"
                return True
            elif ereignis.key == pygame.K_m:
                spiel_status = "hauptmenue"
                menues_schliessen()
            elif ereignis.key == pygame.K_k:
                # Fortgeschrittener Kurs (Planeten): Kolonie wechseln.
                if kolonie_naechste_wechseln():
                    pause_schliessen()
                    return True
            elif ereignis.key == pygame.K_g:
                # Fortgeschrittener Kurs (Planeten): neue Kolonie gruenden.
                if kolonie_gruenden():
                    pause_schliessen()
                    return True
            elif ereignis.key == pygame.K_q:
                return False
        if ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1:
            aktion = spiel_menue.aktion_fuer_klick(ereignis.pos, optionen)
            if aktion == "fortsetzen":
                pause_schliessen()
                return True
            if aktion == "kolonie_wechseln":
                if kolonie_naechste_wechseln():
                    pause_schliessen()
                    return True
            if aktion == "kolonie_gruenden":
                if kolonie_gruenden():
                    pause_schliessen()
                    return True
            if aktion == "speichern":
                spielstand_speichern()
            if aktion == "einstellungen":
                einstellungen.ziel_setzen("pause")
                einstellungen.menue_oeffnen()
                spiel_status = "einstellungen"
                return True
            if aktion == "achievements":
                _achievementmenue_ziel = "pause"
                spiel_status = "achievements"
                return True
            elif aktion == "missionen":
                _missionenmenue_ziel = "pause"
                spiel_status = "missionen"
                return True
            elif aktion == "hauptmenue":

                spiel_status = "hauptmenue"
                menues_schliessen()
            elif aktion == "beenden":
                return False
    return True


def endmenue_verarbeiten():
    """Verarbeitet die Aktionen nach Sieg oder Niederlage."""
    global spiel_status
    optionen = [("neues_spiel", "Neues Spiel", "N / Enter"),
                ("hauptmenue", "Zum Hauptmenü", "M"),
                ("beenden", "Spiel beenden", "Esc")]
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        if ereignis.type == pygame.KEYDOWN:
            if ereignis.key in (pygame.K_n, pygame.K_RETURN):
                neues_spiel_starten()
                return True
            if ereignis.key == pygame.K_m:
                spiel_status = "hauptmenue"
                menues_schliessen()
                return True
            if ereignis.key in (pygame.K_q, pygame.K_ESCAPE):
                return False
        if ereignis.type == pygame.MOUSEBUTTONDOWN and ereignis.button == 1:
            aktion = spiel_menue.aktion_fuer_klick(ereignis.pos, optionen)
            if aktion == "neues_spiel":
                neues_spiel_starten()
                return True
            if aktion == "hauptmenue":
                spiel_status = "hauptmenue"
                menues_schliessen()
                return True
            if aktion == "beenden":
                return False
    return True


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: EREIGNISSE VERARBEITEN
# ═════════════════════════════════════════════════════════════════════════════

def ereignisse_verarbeiten():

    """
    Geht alle Ereignisse durch die seit dem letzten Frame passiert sind.
    Gibt True zurück wenn das Spiel weiterlaufen soll, False zum Beenden.
    """
    global kamera_x, kamera_y, gebaeude_auswahl, _terraform_modus
    global _auswahl_kategorie, _auswahl_position, _letztes_gebaeude, spiel_geschwindigkeit
    global spiel_status, _missionenmenue_ziel

    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            return False
        
        if ereignis.type == pygame.KEYDOWN:
            # Zufallsereignisse haben Vorrang: Raumschiff-Fenster (darin
            # sind die Buchstaben Q..X die Auswahl) und die Reparatur mit R.
            if ereignisse.taste(ereignis.key, ressourcen_dict):
                continue
            if ereignis.key in (pygame.K_ESCAPE, pygame.K_p):
                pause_umschalten()
                return True
            if ereignis.key == pygame.K_o:
                ziel_anzeige_umschalten()
                return True

            # Fortgeschrittener Kurs: schwebende Fenster ein-/ausblenden.
            # S = Verteidigung, C = Bauinfo, I = Uebersicht, L = Layout zurueck.
            if ereignis.key == pygame.K_s:
                panel.umschalten("verteidigung")
                return True
            if ereignis.key == pygame.K_c:
                panel.umschalten("bauinfo")
                return True
            if ereignis.key == pygame.K_i:
                panel.umschalten("uebersicht")
                return True
            if ereignis.key == pygame.K_l:
                panels_anordnen()
                panel.zustand_zuruecksetzen()
                hud.meldung_anzeigen("Fenster-Layout zurückgesetzt")
                return True
            # ── Fortgeschrittener Kurs: N schaltet die Musik an/aus ──
            # N ist im laufenden Spiel frei. Im Endmenue bedeutet N weiterhin
            # "neues Spiel", deshalb steht diese Pruefung nur hier.
            if ereignis.key == pygame.K_n:
                an = ton.musik_umschalten()
                einstellungen.setzen("musik_an", an)
                hud.meldung_anzeigen(
                    "Musik " + ("eingeschaltet" if an else "ausgeschaltet") + ".")
                continue
            # ── Fortgeschrittener Kurs: V zeigt das Strassennetz ──────
            # Gruene Kacheln = Netz an der Basis, rote Rahmen = Gebaeude
            # ohne Anbindung. Die Ansicht aendert keine Spielregeln.
            if ereignis.key == pygame.K_v:
                sichtbar = logistik.ansicht_umschalten()
                hud.meldung_anzeigen(
                    "Logistik-Ansicht " +
                    ("eingeschaltet" if sichtbar else "ausgeschaltet") + ".")
                continue
            if ereignis.key == pygame.K_m:
                _missionenmenue_ziel = "spiel"
                spiel_status = "missionen"
                return True

            # Stunde 11: Zifferntasten wählen Kategorien.
            # Pfeil links/rechts blättern innerhalb der Kategorie weiter.
            tasten_kategorien = {
                pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
                pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6",
                pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9",
            }
            if ereignis.key in tasten_kategorien:
                kategorie_waehlen(tasten_kategorien[ereignis.key])
            elif ereignis.key == pygame.K_0:
                gebaeude_auswahl = _letztes_gebaeude
                print(f"Schnellzugriff: {gebaeude.GEBAEUDE_TYPEN[gebaeude_auswahl]['name']}")
            elif ereignis.key == pygame.K_LEFT:
                kategorie_weiter(-1)
            elif ereignis.key == pygame.K_RIGHT:
                kategorie_weiter(1)
            # Die alten Spezialtasten bleiben als leicht merkbare Abkürzungen.
            elif ereignis.key == pygame.K_g:
                gebaeude_auswahl = 10
                print("Spezialauswahl: Fusionsreaktor")
            elif ereignis.key == pygame.K_t and not handel.handelsmenue_ist_offen():
                gebaeude_auswahl = 11
                print("Spezialauswahl: Roboterfabrik")

            # ── Stunde 11: Terraforming ────────────────────────────────────
            if ereignis.key == pygame.K_z:
                _terraform_modus = not _terraform_modus
                status = "an" if _terraform_modus else "aus"
                hud.meldung_anzeigen(f"Terraforming-Modus {status}.")

            # ── STUNDE 9 — NEU: TAB öffnet/schließt das Baumenü ────────────

            # Verbesserungsvorschlag 3: Mit TAB sieht man ALLE Gebäudetypen
            # gleichzeitig (mit Baukosten und Freischaltung) im Overlay.
            # menu.menu_umschalten() togglet den Zustand (_menu_offen).
            if ereignis.key == pygame.K_TAB:
                menu.menu_umschalten()
            elif menu.menu_ist_offen() and menu.menu_taste(ereignis.key):
                continue

            # ── Stunde 11: Forschungsmenü mit F1–F12 und Scrollen ─────────
            if ereignis.key == pygame.K_f:
                forschung.forschung_menu_umschalten()
            elif forschung.forschung_menu_ist_offen():
                forschung.forschung_menu_taste(ereignis.key, ressourcen_dict)
                continue

            # ── Stunde 11: Handelstasten nur im Handelsmenü auswerten ──────
            if ereignis.key == pygame.K_e:
                handel.handelsmenue_umschalten()
            elif handel.handelsmenue_ist_offen():
                handel.handelsmenue_taste(ereignis.key, ressourcen_dict)
                continue

            # ── STUNDE 10 — NEU: H öffnet/schließt die Hilfe ────────────────
            if ereignis.key == pygame.K_h:
                global _hilfe_offen
                _hilfe_offen = not _hilfe_offen
            
            # ── Stunde 11: Pause und Geschwindigkeit ohne Ziffernkonflikt ──
            # Leertaste pausiert. Plus und Minus ändern die Spielgeschwindigkeit.
            if ereignis.key == pygame.K_SPACE:
                spiel_geschwindigkeit = 1 if spiel_geschwindigkeit == 0 else 0
                status = "pausiert" if spiel_geschwindigkeit == 0 else "gestartet"
                print(f"Spiel {status}!")
            elif ereignis.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                spiel_geschwindigkeit = min(4, max(1, spiel_geschwindigkeit + 1))
                print(f"Geschwindigkeit: {spiel_geschwindigkeit}×")
            elif ereignis.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                spiel_geschwindigkeit = max(1, spiel_geschwindigkeit - 1)
                print(f"Geschwindigkeit: {spiel_geschwindigkeit}×")

            # ── STUNDE 7 — NEU: Taste B springt zur Basis ──────────────────
            # Die Basis ist das erste Gebäude (Index 0).
            # Wenn der Spieler "B" drückt, suchen wir die Basis in der Liste
            # und setzen die Kamera direkt darauf — ohne Animation.
            # Das ist hilfreich bei großen Karten, um schnell zurückzufinden.
            # Achtung: Die Schleifen-Variable heißt "ein_gebaeude" und NICHT
            # "gebaeude" — sonst würden wir das importierte Modul überschreiben!
            if ereignis.key == pygame.K_b:
                for ein_gebaeude in liste_gebaeude:
                    if ein_gebaeude["typ"] == 0:  # 0 = Basis
                        # Mitte der Basis-Kachel berechnen
                        ziel_x = ein_gebaeude["kachel_x"] * KACHEL_GROESSE
                        ziel_y = ein_gebaeude["kachel_y"] * KACHEL_GROESSE
                        # Kamera zentrieren: Ziel in die Mitte des sichtbaren Spielfelds
                        # unter der Ressourcenleiste (Fenster-Mitte minus HUD minus halbe Kachel)
                        kamera_x = ziel_x - BILD_BREITE // 2 + KACHEL_GROESSE // 2
                        kamera_y = (ziel_y - (BILD_HOEHE - hud.HUD_HOEHE) // 2
                            + KACHEL_GROESSE // 2)
                        kamera_begrenzen()  # Nicht über den Rand scrollen!
                        print(f"Kamera zur Basis gesprungen! ({ziel_x}, {ziel_y})")
                        break  # Nur die erste Basis suchen


        # ── Schwebende Info-Fenster: Ziehen und Loslassen ──────────────────
        # MOUSEMOTION und MOUSEBUTTONUP werden sonst nirgends gebraucht:
        # Sie dienen nur dem Verschieben der Fenster an ihrer Titelzeile.
        if ereignis.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            panel.maus_ereignis(ereignis)
            continue

        # STUNDE 3 — MAUSKLICK ERKENNEN
        # pygame.MOUSEBUTTONDOWN wird ausgelöst, wenn der Spieler klickt.
        # Wir fragen die Mausposition ab und berechnen die Kachel.
        # Dann speichern wir ein neues Gebäude in liste_gebaeude.
        #
        # STUNDE 5 — BAUEN KOSTET JETZT RESSOURCEN!
        # Bevor wir bauen, prüfen wir:
        #   1. Kann das Gebäude überhaupt gebaut werden?
        #      (Basis nur 1×, genug Ressourcen?)
        #   2. Wenn ja: Baukosten abziehen + Gebäude platzieren
        #   3. Wenn nein: Konsolenausgabe, kein Bau
        #
        # STUNDE 9 — NEU: Abreißen mit der RECHTEN Maustaste (button 3)
        # Verbesserungsvorschlag 1. Man bekommt 50 % der Baukosten zurück.

        # Mausklick erkennen (linke Maustaste) - platziert ein Gebäude
        if ereignis.type == pygame.MOUSEBUTTONDOWN:
            # Geöffnete Overlays erhalten den Klick vollständig; sonst würde
            # ein Menü-Klick versehentlich ein Gebäude auf der Karte bauen.
            if forschung.forschung_menu_ist_offen():
                if ereignis.button == 4:
                    forschung.forschung_menu_scroll(-3)
                elif ereignis.button == 5:
                    forschung.forschung_menu_scroll(3)
                elif ereignis.button == 1:
                    forschung.forschung_menu_mausevent(ereignis.pos, ressourcen_dict)
                continue
            if menu.menu_ist_offen():
                if ereignis.button == 4:
                    menu.menu_scroll(-3)
                elif ereignis.button == 5:
                    menu.menu_scroll(3)
                continue
            if handel.handelsmenue_ist_offen():
                continue
            # Schwebende Fenster liegen ÜBER der Karte: Ein Klick darauf
            # darf kein Gebäude bauen, abreißen oder terraformen.
            if panel.maus_ereignis(ereignis):
                continue

            # Der Schalter liegt über der Karte. Deshalb muss der Klick vor
            # der Umrechnung in eine Kachelposition abgefangen werden.
            if (ereignis.button == 1 and
                    ziel_schalter_rect().collidepoint(ereignis.pos)):
                ziel_anzeige_umschalten()
                continue
            # Die Ressourcenleiste liegt ueber der Karte — Klicks darauf
            # duerfen kein Gebäude bauen, abreißen oder terraformen
            # (sonst wuerde im Verborgenen hinter dem HUD gebaut).
            if (ereignis.button in (1, 3) and
                    ereignis.pos[1] < hud.balkenhoehe_aktuell()):
                continue
            if ereignis.button == 1:  # 1 = linke Maustaste

                maus_x, maus_y = ereignis.pos
                # Bildschirm-Position -> Kachel-Position umrechnen
                # (Kamera-Versatz addieren, dann durch Kachelgröße teilen).
                # y nutzt kamera_zeichnen_y() — die Welt liegt um das HUD
                # versetzt, siehe Definition der Funktion.
                kachel_x = (maus_x + kamera_x) // KACHEL_GROESSE
                kachel_y = (maus_y + kamera_zeichnen_y()) // KACHEL_GROESSE
                
                # ── STUNDE 8: Boden-Typ der Kachel prüfen ──────────────────
                # Hole den Bodentyp der angeklickten Kachel
                if 0 <= kachel_y < KARTE_HOEHE and 0 <= kachel_x < KARTE_BREITE:
                    boden_typ = karten_daten[kachel_y][kachel_x]
                else:
                    boden_typ = None  # Außerhalb der Karte
                
                # ── Stunde 11: Terraforming vor dem normalen Bauen ────────
                if _terraform_modus:
                    erfolgreich, meldung = ressourcen.terraformieren(
                        ressourcen_dict, karten_daten, kachel_x, kachel_y)
                    hud.meldung_anzeigen(meldung)
                    ton.sound_abspielen("terraforming" if erfolgreich else "fehler")
                    if erfolgreich:
                        achievements.terraformierung()
                        achievements_pruefen()
                        missionen.terraformiert()
                        missionen_pruefen()
                    continue

                # ── Bauprüfung mit verständlicher Rückmeldung ──────────────
                # Wir prüfen bewusst in einer festen Reihenfolge:
                # 1. Fehlt Forschung oder eine andere Freischaltung?
                # 2. Ist der Bauplatz frei und für das Gebäude geeignet?
                # 3. Fehlen echte Baurohstoffe?
                # So bekommt die Spielperson nicht fälschlich die Meldung
                # „Rohstoffe fehlen“, wenn eigentlich Forschung fehlt.
                gebaeude_name = gebaeude.GEBAEUDE_TYPEN[gebaeude_auswahl]["name"]
                freischaltung = ressourcen.freischaltung_hinweis(
                    ressourcen_dict, gebaeude_auswahl)
                bauplatz_frei = gebaeude.kann_platzieren(
                    liste_gebaeude, gebaeude_auswahl, kachel_x, kachel_y,
                    KARTE_BREITE, KARTE_HOEHE)
                baukosten_fehlen = ressourcen.fehlende_baukosten(
                    ressourcen_dict, gebaeude_auswahl)

                if freischaltung:
                    hud.meldung_anzeigen(
                        f"{gebaeude_name}: {freischaltung}")
                    ton.sound_abspielen("fehler")
                elif not bauplatz_frei:
                    hud.meldung_anzeigen(
                        f"{gebaeude_name}: Bauplatz ist belegt, ungeeignet oder außerhalb der Karte.")
                    ton.sound_abspielen("fehler")
                elif baukosten_fehlen:
                    hud.meldung_anzeigen(
                        f"{gebaeude_name}: Rohstoffe fehlen — {baukosten_fehlen}.")
                    ton.sound_abspielen("fehler")
                else:
                    # Jetzt sind alle Prüfungen erfolgreich. Erst danach
                    # ziehen wir Ressourcen ab und platzieren das Gebäude.
                    ressourcen.baukosten_abziehen(ressourcen_dict,
                                                   gebaeude_auswahl)
                    gebaut = gebaeude.gebaeude_platzieren(
                        liste_gebaeude, gebaeude_auswahl, kachel_x, kachel_y,
                        KARTE_BREITE, KARTE_HOEHE)
                    if gebaut:
                        _letztes_gebaeude = gebaeude_auswahl
                        # Fortgeschrittener Kurs: kurzer Bau-Sound.
                        ton.sound_abspielen("bauen")
                        # Fortgeschrittener Kurs (Logistik): Das Netz kann sich
                        # durch eine neue Strasse geaendert haben. Deshalb wird es
                        # genau hier neu berechnet - und nicht in jedem Frame.
                        logistik.netz_aktualisieren(liste_gebaeude)
                        if (liste_gebaeude and
                                liste_gebaeude[-1].get("stillstand_grund")):
                            # Einmaliger, nicht blockierender Hinweis: Bauen
                            # bleibt erlaubt, sonst gaebe es einen Stillstand.
                            hud.meldung_anzeigen(
                                f"Hinweis: {gebaeude_name} hat keine "
                                "Strassenanbindung - baue eine Strasse zur Basis.")
                        achievements.gebaeude_gebaut(gebaeude_auswahl)
                        statistik.gebaeude_gebaut()
                        achievements_pruefen()
                        missionen.gebaeude_gebaut(gebaeude_auswahl)
                        missionen_pruefen()

            # ── STUNDE 9 — NEU: Rechtsklick reißt ein Gebäude ab ──────────
            # ereignis.button == 3 ist die RECHTE Maustaste.
            elif ereignis.button == 3:
                maus_x, maus_y = ereignis.pos
                kachel_x = (maus_x + kamera_x) // KACHEL_GROESSE
                kachel_y = (maus_y + kamera_zeichnen_y()) // KACHEL_GROESSE

                # 1. Gebäude von der Kachel entfernen.
                #    gebaeude_abreissen() gibt den typ_index zurück oder None.
                #    Die Basis (Index 0) kann NICHT abgerissen werden!
                typ_index = gebaeude.gebaeude_abreissen(
                    liste_gebaeude, kachel_x, kachel_y)

                # 2. Nur wenn wirklich ein Gebäude abgerissen wurde:
                if typ_index is not None:
                    # Fortgeschrittener Kurs: Abriss hoerbar machen.
                    ton.sound_abspielen("abriss")
                    # Fortgeschrittener Kurs (Logistik): Wurde eine Strasse
                    # abgerissen, kann das Netz sofort auseinanderfallen.
                    logistik.netz_aktualisieren(liste_gebaeude)
                    # 3. 50 % der Baukosten zurückbekommen.
                    #    Die Funktion fügt die Werte zu ressourcen_dict hinzu
                    #    und liefert ein Dictionary mit den Beträgen zurück.
                    rueckerstattung = ressourcen.ressourcen_zurueckerstatten(
                        ressourcen_dict, typ_index)

                    # 4. Konsolenausgabe wie beim Bauen:
                    #    z.B. "Reaktor abgerissen! +10 gold zurueckerstattet"
                    name = gebaeude.GEBAEUDE_TYPEN[typ_index]["name"]
                    for ress_name, betrag in rueckerstattung.items():
                        print(f"{name} abgerissen! "
                              f"+{betrag} {ress_name} zurueckerstattet")
        
        # WICHTIG (Stunde 9): Das Baumenü blockiert die Mausklicks NICHT.
        # Solange es offen ist, kann man trotzdem weiterbauen. Das ist
        # bewusst so einfach gehalten — mehr dazu steht in menu.py.
        
    # ── Schritt 2: Gehaltene WASD-Tasten prüfen ─────────────────────────
    # Pfeil links/rechts sind in Stunde 11 für die Gebäude-Unterauswahl
    # reserviert. WASD bleibt deshalb die konfliktfreie Kamerasteuerung.
    # Das Einstellungsmenü kann FPS und Kamera-Tempo geändert haben: pro
    # Frame neu berechnet - bei weniger FPS mehr Pixel pro Frame, damit
    # die Kamera trotzdem gleich schnell über den Bildschirm scrollt.
    KAMERA_SPEED = (einstellungen.wert("kamera_tempo") * 60
                    // max(1, einstellungen.wert("fps")))
    gedrueckte_tasten = pygame.key.get_pressed()
    if gedrueckte_tasten[pygame.K_a]:
        kamera_x -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_d]:
        kamera_x += KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_w]:
        kamera_y -= KAMERA_SPEED
    if gedrueckte_tasten[pygame.K_s]:
        kamera_y += KAMERA_SPEED

    # ── Schritt 3: Rand-Scrolling mit der Maus ────────────────────────
    # Wie in Final Earth 2 (und vielen Strategiespielen): Wenn der
    # Mauszeiger nah an den Bildschirmrand kommt, scrollt die Kamera
    # automatisch in diese Richtung — ohne dass eine Taste gedrückt wird.
    RAND_ABSTAND = 25
    maus_pos_x, maus_pos_y = pygame.mouse.get_pos()
    
    if maus_pos_x < RAND_ABSTAND:
        kamera_x -= KAMERA_SPEED
    if maus_pos_x > BILD_BREITE - RAND_ABSTAND:
        kamera_x += KAMERA_SPEED
    if maus_pos_y < RAND_ABSTAND:
        kamera_y -= KAMERA_SPEED
    if maus_pos_y > BILD_HOEHE - RAND_ABSTAND:
        kamera_y += KAMERA_SPEED
    
    kamera_begrenzen()
    return True


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: SPIELSCHLEIFE (GAME LOOP)
# ═════════════════════════════════════════════════════════════════════════════

def spielwelt_zeichnen():
    """Zeichnet die aktuelle Welt und alle zustandsabhängigen Overlays."""
    panel.frame_start()      # Merkliste der schwebenden Fenster leeren
    if spiel_status == "einstellungen" and einstellungen.ziel() == "hauptmenue":
        # Von aus dem Hauptmenü geöffnet: da existiert noch keine Spielwelt
        # unter dem Overlay - deshalb nur der Sternenhintergrund.
        hintergrund_zeichnen()
        einstellungen.menu_zeichnen()
        return
    hintergrund_zeichnen()
    if spiel_status == "hauptmenue":
        hauptmenue_zeichnen()
        return
    if spiel_status == "regelmenue":
        regelmenue_zeichnen()
        return
    if spiel_status == "achievements":
        achievements_zeichnen()
        return
    if spiel_status == "missionen":
        missionen_zeichnen()
        return
    if spiel_status == "statistik":
        statistik.menu_zeichnen()
        return

    karte_zeichnen()
    # gebaeude und logistik zeichnen die Welt — deshalb die um das HUD
    # versetzte Kamera uebergeben (karte_zeichnen rechnet intern gleich).
    gebaeude.gebaeude_zeichnen(liste_gebaeude, kamera_x, kamera_zeichnen_y())
    # Fortgeschrittener Kurs: Logistik-Ansicht nur bei Bedarf zeichnen.
    logistik.zeichnen(liste_gebaeude, kamera_x, kamera_zeichnen_y(),
                      KACHEL_GROESSE)
    hud.hud_zeichnen(ressourcen_dict, gebaeude_auswahl,
                     gebaeude.GEBAEUDE_TYPEN,
                     kamera_x, kamera_y,
                     ressourcen.GEBAEUDE_WIRTSCHAFT,
                     pygame.mouse.get_pos(),
                     ressourcen.personal_info(ressourcen_dict, liste_gebaeude),
                     {name: ressourcen.maximaler_speicher(name)
                      for name in ressourcen.SPEICHER_BASIS},
                     ressourcen.baukosten_berechnen,
                     gebaeude.kategorie_name(_auswahl_kategorie),
                     _auswahl_position,
                     gebaeude.bild_fuer_typ)
    ziel_zeichnen()
    # Fortgeschrittener Kurs (Gegner): Verteidigungs-Panel rechts und
    # Ergebnis-Banner oben mittig (reine Anzeige, Logik in gegner.py).
    gegner.panel_zeichnen(ressourcen_dict, liste_gebaeude,
                          aktives_regelwerk())
    gegner.banner_zeichnen()
    menu.menu_zeichnen(gebaeude.GEBAEUDE_TYPEN,
                       ressourcen.GEBAEUDE_WIRTSCHAFT,
                       ressourcen_dict,
                       gebaeude.GEBAEUDE_KATEGORIEN,
                       gebaeude.bild_fuer_typ)
    forschung.forschung_menu_zeichnen(ressourcen_dict,
                                       gebaeude.GEBAEUDE_TYPEN)
    handel.handelsmenue_zeichnen(ressourcen_dict)
    # Zufallsereignisse: Raumschiff-Fenster liegt ueber allem anderen.
    ereignisse.menu_zeichnen(ressourcen_dict)
    if _hilfe_offen:
        hilfe_zeichnen()
    if spiel_status == "pause":
        pausemenue_zeichnen()
    elif spiel_status in ("sieg", "niederlage"):
        endmenue_zeichnen()
    elif spiel_status == "einstellungen":
        einstellungen.menu_zeichnen()


def spiel_starten():

    """
    Startet die Hauptspielschleife.
    Reihenfolge wie in Final Earth 2:
    1. Weltraum-Hintergrund
    2. Planeten-Oberfläche
    3. HUD / Anzeigetexte
    """
    global tick_zaehler, spiel_geschwindigkeit

    print("Initialisiere Menüs und Spielmodule...")
    sterne_generieren()
    gebaeude.gebaeude_initialisieren(fenster, KACHEL_GROESSE)
    hud.hud_initialisieren(fenster)
    menu.menu_initialisieren(fenster)
    spiel_menue.menue_initialisieren(fenster)
    einstellungen.menue_initialisieren(fenster)
    ereignisse.ereignisse_initialisieren(fenster)
    statistik.initialisieren(fenster)
    statistik.laden()
    achievements.initialisieren(fenster)
    missionen.initialisieren(fenster)
    forschung.forschung_initialisieren(fenster)
    handel.handel_initialisieren(fenster)
    # Fortgeschrittener Kurs: Ton einschalten und Musik starten.
    # Ohne Audiogeraet sind beide Aufrufe wirkungslos - das Spiel laeuft weiter.
    # Einstellungen aus der JSON-Datei holen und auf den Ton anwenden.
    einstellungen.laden()
    ton.initialisieren()
    einstellungen.alle_anwenden()
    ton.musik_starten()
    logistik.initialisieren(fenster)
    gegner.initialisieren(fenster)
    panel.initialisieren(fenster)

    # Fortgeschrittener Kurs (Planeten): main.py als Ziel der Stände.
    kolonien.hauptmodul_setzen(sys.modules[__name__], KARTE_BREITE, KARTE_HOEHE)

    print("Hauptmenü geöffnet. Enter startet ein neues Spiel, L lädt einen Spielstand.")
    print(f"Karte: {KARTE_BREITE} x {KARTE_HOEHE} Kacheln = "
          f"{KARTE_BREITE * KACHEL_GROESSE} x {KARTE_HOEHE * KACHEL_GROESSE} Pixel")

    laeuft = True

    while laeuft:
        if spiel_status == "hauptmenue":
            laeuft = hauptmenue_verarbeiten()
        elif spiel_status == "regelmenue":
            laeuft = regelmenue_verarbeiten()
        elif spiel_status == "achievements":
            laeuft = achievementsmenue_verarbeiten()
        elif spiel_status == "missionen":
            laeuft = missionenmenue_verarbeiten()
        elif spiel_status == "statistik":
            laeuft = statistikmenue_verarbeiten()
        elif spiel_status == "einstellungen":
            laeuft = einstellungen_verarbeiten()
        elif spiel_status == "spiel":
            laeuft = ereignisse_verarbeiten()
        elif spiel_status == "pause":
            laeuft = pausemenue_verarbeiten()
        else:
            laeuft = endmenue_verarbeiten()

        # ── TICK-SYSTEM — 1× pro Sekunde (abhängig von Geschwindigkeit) ─────

        # tick_zaehler zählt die Frames (Bilder pro Sekunde).
        # Bei 60 FPS: 60 Frames = 1 Sekunde.
        # Wenn tick_zaehler 60 erreicht → produzieren → zurücksetzen.
        # Neu in Stunde 6: Auch Holzfäller und Steinmetz produzieren jetzt!
        # Neu in Stunde 8: Die Geschwindigkeit ist einstellbar:
        #   spiel_geschwindigkeit = 1 → 60 Frames (normal)
        #   spiel_geschwindigkeit = 2 → 30 Frames (doppelt)
        #   spiel_geschwindigkeit = 0 → pausiert
        # Waehrend das Raumschiff-Fenster offen ist, laeuft die Wirtschaft
        # nicht weiter - sonst waere die Fracht weg, waehrend man waehlt.
        if (spiel_status == "spiel" and spiel_geschwindigkeit > 0
                and not ereignisse.angebot_ist_offen()):
            tick_zaehler += 1
            if tick_zaehler >= max(1, einstellungen.wert("fps") // spiel_geschwindigkeit):
                tick_zaehler = 0
                # Vorher merken: Forschung und Stahl koennen durch laufende
                # Auftraege sinken - gezaehlt wird nur der Zuwachs.
                forschung_vorher = ressourcen_dict.get("forschung", 0)
                stahl_vorher = ressourcen_dict.get("stahl", 0)
                ressourcen.ressourcen_produzieren(ressourcen_dict,
                                                   liste_gebaeude,
                                                   karten_daten)
                forschung_delta = ressourcen_dict.get("forschung", 0) - forschung_vorher
                if forschung_delta > 0:
                    statistik.forschung_erzeugt(forschung_delta)
                stahl_delta = ressourcen_dict.get("stahl", 0) - stahl_vorher
                if stahl_delta > 0:
                    achievements.stahl_erzeugt(stahl_delta)
                handel.handel_tick(ressourcen_dict, liste_gebaeude)
                # Fortgeschrittener Kurs (Gegner): Angriffe und Abwehr
                # laufen als eigener Zustandsautomat nach dem Handel.
                gegner_ereignis_verarbeiten(
                    gegner.gegner_tick(ressourcen_dict, liste_gebaeude,
                                       aktives_regelwerk()))
                statistik.tick(ressourcen_dict, liste_gebaeude)
                ereignis_meldung_verarbeiten(
                    ereignisse.ereignisse_tick(ressourcen_dict, liste_gebaeude))
                spielstatus_pruefen()
                missionen_pruefen()

        spielwelt_zeichnen()
        pygame.display.flip()

        uhr.tick(einstellungen.wert("fps"))


# ═════════════════════════════════════════════════════════════════════════════
# BLOCK: HILFE ANZEIGE
# ═════════════════════════════════════════════════════════════════════════════

def hilfe_zeichnen():
    """
    Zeichnet ein halbtransparentes Hilfe-Overlay mit allen Tasten und
    ihrer Funktion — wie ein Spickzettel für neue Spieler.

    Wird bei Taste H ein-/ausgeblendet.
    """
    overlay = pygame.Surface(fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    fenster.blit(overlay, (0, 0))

    schrift_gross  = pygame.font.Font(None, 36)
    schrift_normal = pygame.font.Font(None, 24)

    titel = schrift_gross.render("HILFE — Steuerung", True, (255, 255, 100))
    fenster.blit(titel, (30, 25))

    zeilen = [
        "1-9          — Kategorie wählen; Pfeil links/rechts = Gebäude wechseln",
        "0            — letztes gebautes Gebäude erneut auswählen",
        "TAB          — Baumenü öffnen/schließen",
        "F            — Forschungsmenü öffnen/schließen",
        "F1-F12       — sichtbare Forschung starten; Mausrad/Bild auf-ab scrollen",
        "E            — Handelsmenü; Q/W/R/T/Y/U = 3:1-Ressourcentausch",
        "J / K        — NPC-Angebot annehmen / ablehnen",
        "Z            — Terraforming-Modus ein/aus (nach Forschung)",
        "H            — Diese Hilfe ein-/ausblenden",
        "P / ESC      — Pausenmenü öffnen bzw. schließen",
        "O            — Zielfenster ein-/ausblenden; X bzw. Klick öffnet/schließt es",
        "N            — Musik an-/ausschalten",
        "V            — Logistik-Ansicht (Strassennetz) ein-/ausblenden",
        "S            — Im Pausenmenü den Spielstand speichern",
        "L            — Im Hauptmenü den Spielstand laden",
        "E            — Einstellungen im Hauptmenü und in der Pause",
        "T            — Gesamtstatistik im Hauptmenü",
        "R            — Systemausfall sofort reparieren (100 Gold)",
        "Raumschiff   — Q W E R T Z X wählen, Pfeiltasten = Menge, Enter = einsetzen",
        "R            — Im Hauptmenü Spielregeln auswählen",
        "A            — Achievements anzeigen (Haupt-/Pausenmenü)",
        "M            — Missionszentrale im Hauptmenü öffnen",
        "I            — Missionszentrale in der Pause öffnen",
        "K            — In der Pause: zu anderer Kolonie wechseln",
        "G            — In der Pause: neue Kolonie gründen",
        "",
        "Maus         — Linksklick = bauen/terraformen; Rechtsklick = abreißen",
        "WASD         — Kamera scrollen; Pfeil links/rechts = Auswahl",
        "B            — Springe zur Basis",
        "Leertaste    — Pause / Start; + / - = Geschwindigkeit",
        "S            — Verteidigungs-Fenster ein-/ausblenden",
        "C            — Bauinfo-Fenster ein-/ausblenden",
        "I            — Uebersicht-Fenster ein/aus (Pause: Missionen)",
        "L            — Fenster-Layout zurücksetzen",
        "",
        "Fenster      — an der Titelzeile ziehen; - = minimieren, X = schliessen",
    ]

    # Zwei Spalten: So bleiben auch die neuen Zeilen gut lesbar.
    haelfte = (len(zeilen) + 1) // 2
    spalten_x = (50, 520)
    for index, eintrag in enumerate(zeilen):
        spalte = 0 if index < haelfte else 1
        y = 80 + (index % haelfte) * 28
        text = schrift_normal.render(eintrag, True, (220, 220, 220))
        fenster.blit(text, (spalten_x[spalte], y))
    y = 80 + haelfte * 28

    hinweis = schrift_normal.render("(H drücken zum Schließen)", True, (150, 150, 150))
    fenster.blit(hinweis, (50, y + 10))


# ═════════════════════════════════════════════════════════════════════════════
# PROGRAMMSTART
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    spiel_starten()
    pygame.quit()
    sys.exit()


# =============================================================================
# ENDE STUNDE 9
# =============================================================================
# Wiederholung: Was wir heute gelernt haben
#
# Stunde 1 (Wiederholung):
#   ✓ pygame.init() startet Pygame
#   ✓ display.set_mode() erstellt das Fenster
#   ✓ Die Spielschleife: Eingaben → Logik → Zeichnen
#   ✓ Farben als (R, G, B) Tupel
#   ✓ Konstanten in GROSSBUCHSTABEN
#   ✓ Funktionen mit def
#   ✓ Kein Umlaut in Variablennamen! (laeuft statt läuft)
#
# Stunde 2 (Wiederholung):
#   ✓ Verschachtelte Schleifen (for zeile ... for spalte ...)
#   ✓ Kamera-Prinzip: pixel_x = spalte × KACHEL_GROESSE − kamera_x
#   ✓ continue = Schleifenrunde überspringen
#   ✓ pygame.key.get_pressed() für gehaltene Tasten
#   ✓ global Keyword zum Ändern globaler Variablen
#   ✓ 2D-Arrays (karten_daten[zeile][spalte])
#   ✓ Zufällige Kartengenerierung mit random
#   ✓ Sternenhimmel im Hintergrund
#
# Stunde 3 (Wiederholung):
#   ✓ pygame.MOUSEBUTTONDOWN — Mausklicks erkennen
#   ✓ ereignis.pos — Mausposition abfragen
#   ✓ Kachel aus Mausposition berechnen: kachel_x = (maus + kamera_x) // GROESSE,
#     kachel_y = (maus + kamera_zeichnen_y()) // GROESSE (y ist um das HUD versetzt)
#   ✓ Gebäude speichern als Wörterbuch: {"typ": 0, "x": ..., "y": ...}
#   ✓ Gebäude zeichnen — farbige Rechtecke auf der Karte
#   ✓ Doppelbelegung prüfen — Ist die Kachel schon belegt?
#   ✓ gebaeude_zeichnen() in der richtigen Reihenfolge aufrufen
#
# Stunde 4 (Wiederholung):
#   ✓ HUD (Heads-Up Display) am oberen Bildschirmrand zeichnen
#   ✓ Ressourcen-Anzeige: Gold, Energie, Holz
#   ✓ Tasten 1/2/3 für Gebäude-Auswahl (wie in Final Earth 2!)
#   ✓ Ressourcen als Dictionary speichern {"gold": 100, ...}
#
# Stunde 5 (Wiederholung):
#   ✓ Tick-System: tick_zaehler zählt Frames, bei 60 = 1 Sekunde
#   ✓ ressourcen.ressourcen_produzieren() — 1× pro Sekunde
#   ✓ Gebäude produzieren und verbrauchen automatisch
#   ✓ Baukosten: Gebäude bauen kostet jetzt Ressourcen
#   ✓ kann_bauen() prüft vor dem Bauen (Ressourcen + Basis-Limit)
#   ✓ baukosten_abziehen() zieht Baukosten ab
#   ✓ Wenn Rohstoffe fehlen → Gebäude produziert nichts
#   ✓ Basis kann nur 1× gebaut werden
#   ✓ Baukosten-Anzeige im HUD
#
# Stunde 6 (Wiederholung):
#   ✓ Neuer Rohstoff: Stein (vierte Ressource, Startwert 20)
#   ✓ Neues Gebäude: Holzfäller (Index 3, produziert +6 Holz, kostet 1480 Gold + 5 Energie)
#   ✓ Neues Gebäude: Steinmetz (Index 4, produziert +5 Stein, kostet 15 Gold + 10 Energie)
#   ✓ Tasten 4 und 5 für Holzfäller / Steinmetz
#   ✓ GEBAEUDE_TYPEN und GEBAEUDE_WIRTSCHAFT auf 5 Einträge erweitert
#   ✓ ressourcen_produzieren() funktioniert automatisch für alle Indizes
#   ✓ gebaeude_zeichnen() funktioniert automatisch — holt Farbe aus GEBAEUDE_TYPEN
#   ✓ HUD zeigt jetzt 4 Ressourcen: Gold, Energie, Holz, Stein
#
# Stunde 7 (Wiederholung):
#   ✓ Neuer Rohstoff: Bevölkerung (fünfte Ressource, Startwert 0)
#   ✓ Neues Gebäude: Wohnhaus (Index 6, produziert +2 Bevölkerung, kostet 20 Gold + 15 Holz + 10 Stein)
#   ✓ Wohnhaus verbraucht −3 Energie pro Sekunde
#   ✓ Taste 7 für das Wohnhaus
#   ✓ GEBAEUDE_TYPEN und GEBAEUDE_WIRTSCHAFT auf 7 Einträge erweitert
#   ✓ HUD zeigt jetzt 5 Ressourcen: Gold, Energie, Holz, Stein, Bevölkerung
#   ✓ Je mehr Wohnhäuser, desto mehr Bevölkerung!
#
# Stunde 9 (HEUTE NEU):
#   ✓ Gebäude abreißen mit Rechtsklick (ereignis.button == 3)
#   ✓ 50 % der Baukosten zurück: gebaeude_abreissen() + ressourcen_zurueckerstatten()
#   ✓ Die Basis (Index 0) kann NICHT abgerissen werden
#   ✓ Baumenü mit Taste TAB (menu.py) — zeigt ALLE Gebäudetypen
#   ✓ Tooltip beim Hovern über ein Ressourcen-Icon
#   ✓ Rote Meldung im Spiel bei zu wenig Rohstoffen (hud.meldung_anzeigen)
#   ✓ Stufenweise Freischaltung: Marktplatz ab 5 Bevölkerung, Wohnhaus ab 20 Holz
#
# HÄUFIGE FEHLER zum Merken (alle Stunden):
#   ✗ spiel_laeuft ≠ spiel_laeuft  → Python sieht das als 2 verschiedene Variablen!
#   ✗ Einrückung vergessen        → IndentationError
#   ✗ Klammern nicht geschlossen  → SyntaxError
#   ✗ karte_zeichnen() vergessen  → nur schwarzer Bildschirm!
#   ✗ global kamera_x vergessen   → UnboundLocalError
#   ✗ hintergrund NACH karte      → Karte wird übermalt!
#   ✗ karten_daten[zeile][spalte] → zeile zuerst, dann spalte!
#   ✗ Kachel-Berechnung: (maus_x + kamera_x) // GROESSE vergessen
#   ✗ gebaeude_zeichnen() in falscher Reihenfolge aufgerufen
#   ✗ Kameraposition nicht in die Berechnung einbezogen
#   ✗ tick_zaehler nicht global deklariert → UnboundLocalError!
#   ✗ kann_bauen() vergessen → Gebäude gebaut ohne Ressourcen zu bezahlen
#   ✗ baukosten_abziehen() ohne vorherige kann_bauen()-Prüfung → Schulden!
#   ✗ GEBAEUDE_TYPEN und GEBAEUDE_WIRTSCHAFT müssen gleiche Länge haben!
#   ✗ Beim Hinzufügen neuer Gebäude beide Listen gleichzeitig erweitern!
#   ✗ Rückerstattung ohne vorherige Abriss-Prüfung → Gold geschenkt!
#     (Erst gebaeude_abreissen() aufrufen und typ_index auf None prüfen.)
#   ✗ TAB-Menü blockiert nicht den Mausklick — daran denken!
#     (Solange es offen ist, kann man trotzdem bauen.)
#   ✗ Freischaltung vergessen bei neuen Gebäuden nachzutragen!
#     (Sonst Index- bzw. KeyError zwischen den beiden Listen.)
#   ✗ Mausposition nicht an hud_zeichnen() übergeben → kein Tooltip.
#
# Nächste Stunde (Stunde 10):
#   → Volles Forschungssystem als eigenes Modul (forschung.py)
#   → Feinschliff, Balancing & mehr Gebäude
# =============================================================================
