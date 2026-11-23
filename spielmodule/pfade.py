"""Zentrale Projektpfade fuer Terra_Nova."""

import os


# Der Projektordner ist eine Ebene ueber dem Ordner spielmodule/.
# Alle anderen Pfade werden von diesem festen Ausgangspunkt abgeleitet,
# damit das Spiel unabhaengig vom Speicherort einzelner Module funktioniert.
PROJEKT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Ordner fuer Bilder, Töne und persönliche JSON-Daten.
BILDER = os.path.join(PROJEKT, "bilder")
BILDER_GEBAEUDE = os.path.join(BILDER, "gebaeude")
BILDER_STRASSE = os.path.join(BILDER, "strasse")
BILDER_TERRAIN = os.path.join(BILDER, "terrain")
BILDER_ITEMS = os.path.join(BILDER, "items")
AUDIO = os.path.join(PROJEKT, "audio")
SAVES = os.path.join(PROJEKT, "saves")

# Das Spiel darf neu gestartet werden, wenn noch keine Saves vorhanden sind.
# Dieser Aufruf legt nur den Ordner an, nicht irgendeine JSON-Datei.
os.makedirs(SAVES, exist_ok=True)

