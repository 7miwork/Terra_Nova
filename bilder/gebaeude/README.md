# Gebäude-Bilder

Dieser Ordner enthält die PNG-Dateien für die Gebäude, zum Beispiel
`basis.png`, `farm.png`, `wohnhaus.png` und `kaserne.png`.

Das Modul `spielmodule/gebaeude.py` lädt die Bilder aus diesem Ordner über
`spielmodule/pfade.py`. Die Trennung von Straße, Terrain und Items macht die
Grafiken übersichtlich und verhindert Namenskonflikte.
