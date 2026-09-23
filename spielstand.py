"""Speichern und Laden kompletter Spielstände als lesbare JSON-Datei."""

import json
import os
from datetime import datetime

import forschung
import handel
import ressourcen
import logistik
import achievements
import missionen
import gegner


DATEI = os.path.join(os.path.dirname(__file__), "spielstand.json")
VERSION = 1


def _kopie_wert(wert):
    """Erzeugt eine JSON-sichere Kopie einfacher Spielzustandsdaten."""
    if isinstance(wert, dict):
        return {str(schluessel): _kopie_wert(wert) for schluessel, wert in wert.items()}
    if isinstance(wert, list):
        return [_kopie_wert(element) for element in wert]
    if isinstance(wert, tuple):
        return [_kopie_wert(element) for element in wert]
    if isinstance(wert, (int, float, str, bool)) or wert is None:
        return wert
    return None


def existiert():
    """Prüft, ob bereits ein lokaler Spielstand vorhanden ist."""
    return os.path.isfile(DATEI)


def speichern(karten_daten, sterne_liste, ressourcen_dict, liste_gebaeude,
              kamera_x, kamera_y, tick_zaehler, spiel_geschwindigkeit,
              auswahl_kategorie, auswahl_position, gebaeude_auswahl,
              letztes_gebaeude, spielstatus="spiel", versorgungszaehler=None,
              regel_auswahl="standard"):
    """Speichert den übergebenen Weltzustand und liefert Erfolg plus Text."""
    daten = {
        "version": VERSION,
        "gespeichert_am": datetime.now().isoformat(timespec="seconds"),
        "karten_daten": _kopie_wert(karten_daten),
        "sterne_liste": _kopie_wert(sterne_liste),
        "ressourcen": _kopie_wert(ressourcen_dict),
        "gebaeude": _kopie_wert(liste_gebaeude),
        "kamera": {"x": kamera_x, "y": kamera_y},
        "tick_zaehler": tick_zaehler,
        "spiel_geschwindigkeit": spiel_geschwindigkeit,
        "auswahl": {
            "kategorie": auswahl_kategorie,
            "position": auswahl_position,
            "gebaeude": gebaeude_auswahl,
            "letztes_gebaeude": letztes_gebaeude,
        },
        "spielstatus": spielstatus,
        "regel_auswahl": regel_auswahl,
        "versorgungszaehler": _kopie_wert(versorgungszaehler or {}),
        "forschung": forschung.zustand_exportieren(),
        "handel": handel.zustand_exportieren(),
        "logistik": logistik.zustand_exportieren(),
        "wirtschaft": ressourcen.zustand_exportieren(),
        "achievements": achievements.zustand_exportieren(),
        "missionen": missionen.zustand_exportieren(),
        "gegner": gegner.zustand_exportieren(),
    }
    try:
        temporaer = DATEI + ".tmp"
        with open(temporaer, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, ensure_ascii=False, indent=2)
        os.replace(temporaer, DATEI)
    except (OSError, TypeError, ValueError) as fehler:
        try:
            if os.path.exists(DATEI + ".tmp"):
                os.remove(DATEI + ".tmp")
        except OSError:
            pass
        return False, f"Speichern fehlgeschlagen: {fehler}"
    return True, "Spielstand gespeichert."


def laden():
    """Liest den Spielstand und stellt die Modulzustände wieder her."""
    if not existiert():
        return None, "Kein Spielstand vorhanden."
    try:
        with open(DATEI, "r", encoding="utf-8") as datei:
            daten = json.load(datei)
        if daten.get("version") != VERSION:
            return None, "Dieser Spielstand hat eine unbekannte Version."
        pflichtfelder = ("karten_daten", "ressourcen", "gebaeude", "kamera", "auswahl")
        if any(feld not in daten for feld in pflichtfelder):
            return None, "Der Spielstand ist unvollständig."
        forschung.zustand_importieren(daten.get("forschung", {}))
        handel.zustand_importieren(daten.get("handel", {}))
        logistik.zustand_importieren(daten.get("logistik", {}))
        ressourcen.zustand_importieren(daten.get("wirtschaft", {}))
        if "achievements" in daten:
            achievements.zustand_importieren(daten.get("achievements", {}))
        if "missionen" in daten:
            missionen.zustand_importieren(daten.get("missionen", {}))
        # Fortgeschrittener Kurs (Gegner): Alte Spielstaende ohne das
        # Feld "gegner" landen hier mit {} = frischer Friedenszeit.
        gegner.zustand_importieren(daten.get("gegner", {}))
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as fehler:
        return None, f"Laden fehlgeschlagen: {fehler}"
    return daten, "Spielstand geladen."
