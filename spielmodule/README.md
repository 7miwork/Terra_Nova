# Spielmodule

Dieser Ordner enthält die Python-Module des Spiels, zum Beispiel Gebäude,
Gegner, Handel, Logistik, Menüs, Ressourcen und Speichern. `main.py` bleibt
im Projektordner und fügt diesen Ordner zu `sys.path` hinzu.

`pfade.py` stellt die zentralen Projektpfade bereit. Neue Python-Module für
das Spiel werden hier abgelegt. Pfade zu Bildern, Audio und Saves sollen nur
über `pfade.py` gebaut werden.
