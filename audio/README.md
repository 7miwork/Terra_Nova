# Audio

Dieser Ordner enthält alle WAV-Soundeffekte und die Hintergrundmusik
(`hintergrundmusik.wav`) von Terra_Nova.

Das Modul `spielmodule/ton.py` lädt die Dateien über den zentralen Audio-Pfad
aus `spielmodule/pfade.py`. Mit `werkzeuge/sounds_erzeugen.py` können die
Standard-Sounds neu erzeugt werden. Bilder und Python-Module bleiben getrennt,
damit Dateien leichter gefunden und ersetzt werden können.
