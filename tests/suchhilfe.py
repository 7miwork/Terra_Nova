"""Einmalige Suchhilfe Schritt 5 (wird danach geloescht)."""
import pathlib
projekt = pathlib.Path(__file__).resolve().parent.parent
main_text = (projekt / "main.py").read_text(encoding="utf-8")
for nummer, zeile in enumerate(main_text.splitlines(), start=1):
    if ("logistik.zeichnen" in zeile or "gebaeude_zeichnen" in zeile
            or "karte_zeichnen()" in zeile):
        print(nummer, zeile.strip()[:110])
print("--- Strasse in gebaeude.py ---")
geo_text = (projekt / "gebaeude.py").read_text(encoding="utf-8")
for nummer, zeile in enumerate(geo_text.splitlines(), start=1):
    klein = zeile.lower()
    if "strasse" in klein and ("typ" in klein or "9" in zeile or "bild" in klein):
        print(nummer, zeile.strip()[:110])
