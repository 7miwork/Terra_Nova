"""Erzeugt die Platzhalter-Bilder fuer die Verteidigungsgebaeude.

Fortgeschrittener Kurs (Gegner)
    Fuer Kaserne, Raumschiffwerft und Laserturm gibt es (noch) keine
    echten Bilder. Dieses Skript zeichnet einfache 64x64-Platzhalter:
    eine flache Farbe, ein paar deutliche Formen und ein grosser
    Anfangsbuchstabe. Die fertigen PNGs liegen im Ordner bilder/ und
    werden MITGELIEFERT — das Spiel braucht dieses Skript also nicht
    zum Starten. Es dient nur zum Nachvollziehen (und zum Neuerzeugen,
    falls jemand die Farben aendern will).

    Schuelerinnen und Schueler koennen spaeter eigene Bilder zeichnen
    und sie einfach unter demselben Dateinamen in bilder/ speichern
    (wie beim Park und beim Solarreaktor).

Nur Standardbibliothek + Pygame (kein numpy).
"""

import os

import pygame

# ── Konfiguration: Hier kann man Groesse und Farben aendern ──────────────
GROESSE = 64                 # Pixel (Kante); die Welt nutzt 48er-Kacheln
HINTERGRUND = (0, 0, 0, 0)   # voll transparent — das Bild ist nur die Form

# Gebaeudeindex → (Dateiname, Grundfarbe, Form, Buchstabe)
# Form "turm"  = schmaler Turm mit Querbalken (Laserturm)
# Form "block" = massiger Block mit Streben (Kaserne)
# Form "werk"  = breite Halle mit Gate (Raumschiffwerft)
BILDER = {
    21: ("kaserne.png", (190, 90, 90), "block", "K"),
    22: ("raumschiffwerft.png", (150, 160, 220), "werk", "W"),
    23: ("laserturm.png", (255, 120, 120), "turm", "T"),
}


def bild_zeichnen(grundfarbe, form, buchstabe):
    """Zeichnet einen Platzhalter und gibt die Surface zurueck.

    Schritte:
        1. Transparente Leinwand anlegen (damit keine weissen Ecken
           im Spiel sichtbar sind).
        2. Die Grundform zeichnen (je nach Gebaeudetyp).
        3. Einen dunklen Rahmen setzen, damit sich das Gebaeude vom
           Kartenboden abhebt.
        4. Den grossen Anfangsbuchstaben in die Mitte schreiben.
    """
    flaeche = pygame.Surface((GROESSE, GROESSE), pygame.SRCALPHA)
    flaeche.fill(HINTERGRUND)

    # Abgedunkelte Variante der Grundfarbe fuer Details und Rahmen.
    schatten = (grundfarbe[0] // 2, grundfarbe[1] // 2, grundfarbe[2] // 2)

    if form == "turm":
        # Schmaler Turmschaft plus Querbalken unten (Sockel).
        pygame.draw.rect(flaeche, grundfarbe, (24, 8, 16, 48))
        pygame.draw.rect(flaeche, schatten, (16, 50, 32, 8))
        # "Laser-Kopf" oben als hellerer Punkt.
        pygame.draw.circle(flaeche, (255, 255, 220), (32, 10), 5)
    elif form == "werk":
        # Breite Halle mit grossem Tor (wie eine Fabrikhalle).
        pygame.draw.rect(flaeche, grundfarbe, (4, 16, 56, 44))
        pygame.draw.rect(flaeche, schatten, (20, 34, 24, 26))
        # Dachstreben machen die Halle auf einen Blick erkennbar.
        for x in range(8, 56, 10):
            pygame.draw.line(flaeche, schatten, (x, 20), (x, 30), 2)
    else:
        # Massiger Block mit drei Schlitzen (Fenster einer Kaserne).
        pygame.draw.rect(flaeche, grundfarbe, (8, 14, 48, 44))
        pygame.draw.rect(flaeche, schatten, (8, 14, 48, 8))
        for y in (32, 42):
            pygame.draw.rect(flaeche, schatten, (16, y, 32, 5))

    # Dunkler Rahmen rund um die Grundflaeche (sichtbarer Umriss).
    pygame.draw.rect(flaeche, (40, 40, 50), (0, 0, GROESSE, GROESSE), 2)

    # Grosser Anfangsbuchstabe in der Bildmitte.
    schrift = pygame.font.Font(None, 44)
    zeichen = schrift.render(buchstabe, True, (255, 255, 255))
    umriss = schrift.render(buchstabe, True, (30, 30, 40))
    mitte = zeichen.get_rect(center=(GROESSE // 2, GROESSE // 2))
    for versatz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        flaeche.blit(umriss, umriss.get_rect(center=(mitte.centerx + versatz[0],
                                                     mitte.centery + versatz[1])))
    flaeche.blit(zeichen, mitte)
    return flaeche


def main():
    """Erzeugt alle Platzhalter und speichert sie im Ordner bilder/."""
    pygame.init()
    # Anzeige initialisieren, damit convert_alpha() funktioniert — im
    # Testbetrieb mit SDL_VIDEODRIVER=dummy ist das ebenfalls erlaubt.
    pygame.display.set_mode((1, 1))
    ordner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bilder")
    os.makedirs(ordner, exist_ok=True)
    for index, (dateiname, farbe, form, buchstabe) in BILDER.items():
        pfad = os.path.join(ordner, dateiname)
        pygame.image.save(bild_zeichnen(farbe, form, buchstabe), pfad)
        print(f"Platzhalter erzeugt: bilder/{dateiname} (Gebaeudetyp {index})")
    pygame.quit()


if __name__ == "__main__":
    main()
