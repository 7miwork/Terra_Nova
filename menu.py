"""Kategorisiertes Baumenü mit Bildvorschauen und scrollbarer Liste."""

import pygame
import ressourcen

_fenster = None
_menu_offen = False
_scroll = 0


def menu_initialisieren(fenster_obj):
    global _fenster
    _fenster = fenster_obj


def menu_umschalten():
    global _menu_offen, _scroll
    _menu_offen = not _menu_offen
    _scroll = 0


def menu_ist_offen():
    return _menu_offen


def menu_scroll(delta):
    global _scroll
    _scroll = max(0, _scroll + delta)


def menu_taste(key):
    if not _menu_offen:
        return False
    if key in (pygame.K_PAGEUP, pygame.K_UP):
        menu_scroll(-3)
        return True
    if key in (pygame.K_PAGEDOWN, pygame.K_DOWN):
        menu_scroll(3)
        return True
    return False


def _format_dict(d):
    if not d:
        return "nichts"
    namen = ressourcen.RESSOURCEN_NAMEN
    return ", ".join(f"{menge} {namen.get(name, name)}" for name, menge in d.items())


def _zeilen(gebaeude_typen, gebaeude_kategorien):
    if not gebaeude_kategorien:
        gebaeude_kategorien = {"": {"name": "Gebäude", "typen": list(range(len(gebaeude_typen)))}}
    ergebnis = []
    bereits = set()
    for taste, kategorie in gebaeude_kategorien.items():
        ergebnis.append(("kategorie", taste, kategorie["name"], None))
        for index in kategorie["typen"]:
            if 0 <= index < len(gebaeude_typen):
                ergebnis.append(("gebaeude", taste, gebaeude_typen[index]["name"], index))
                bereits.add(index)
    # Gebäude, die noch keiner Kategorie zugeordnet wurden, bleiben sichtbar.
    fehlende = [i for i in range(len(gebaeude_typen)) if i not in bereits]
    if fehlende:
        ergebnis.append(("kategorie", "", "Weitere Gebäude", None))
        for index in fehlende:
            ergebnis.append(("gebaeude", "", gebaeude_typen[index]["name"], index))
    return ergebnis


def menu_zeichnen(gebaeude_typen, gebaeude_wirtschaft, ressourcen_dict=None,
                  gebaeude_kategorien=None, bild_funktion=None):
    if _fenster is None or not _menu_offen:
        return
    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 215))
    _fenster.blit(overlay, (0, 0))
    gross = pygame.font.Font(None, 32)
    klein = pygame.font.Font(None, 16)
    _fenster.blit(gross.render("BAUMENÜ  (TAB schließt)", True, (255, 255, 255)), (24, 14))
    _fenster.blit(klein.render("Ziffer = Kategorie | Pfeile/Mausrad = innerhalb der Kategorie | Bildvorschau links", True, (180, 190, 205)), (24, 42))

    zeilen = _zeilen(gebaeude_typen, gebaeude_kategorien)
    sichtbare_zeilen = 14
    start = min(_scroll, max(0, len(zeilen) - sichtbare_zeilen))
    y = 68
    for typ, kat_taste, titel, index in zeilen[start:start + sichtbare_zeilen]:
        if typ == "kategorie":
            pygame.draw.rect(_fenster, (55, 70, 105), (22, y, 956, 25))
            text = f"[{kat_taste}]  {titel}" if kat_taste else titel
            _fenster.blit(klein.render(text, True, (255, 230, 120)), (32, y + 5))
            y += 28
            continue

        daten = gebaeude_typen[index]
        wirtschaft = gebaeude_wirtschaft[index]
        frei = ressourcen_dict is None or ressourcen.ist_freigeschaltet(ressourcen_dict, index)
        farbe = (245, 245, 245) if frei else (130, 130, 140)
        hoehe = 48
        pygame.draw.rect(_fenster, (24, 28, 40), (22, y, 956, hoehe))
        pygame.draw.rect(_fenster, daten["farbe"], (22, y, 5, hoehe))
        if bild_funktion is not None:
            bild = bild_funktion(index, (38, 38))
            if bild is not None:
                _fenster.blit(bild, (34, y + 5))
        taste = daten.get("taste") or "Kategorie"
        groesse = f"{daten.get('breite', 1)}x{daten.get('hoehe', 1)}"
        kosten = _format_dict(ressourcen.baukosten_berechnen(index))
        prod = _format_dict(wirtschaft.get("produktion", {}))
        verbrauch = _format_dict(wirtschaft.get("verbrauch", {}))
        personal = ressourcen.personalbedarf(index)
        status = "frei" if frei else ressourcen.freischaltung_hinweis(ressourcen_dict, index)
        text1 = f"{daten['name']} [{taste}]  {groesse} Kacheln | Kosten: {kosten} | Personal: {personal} | {status}"
        text2 = f"Produktion: {prod} | Verbrauch: {verbrauch}"
        _fenster.blit(klein.render(text1, True, farbe), (80, y + 5))
        _fenster.blit(klein.render(text2, True, (175, 185, 200)), (80, y + 25))
        y += hoehe + 3

    if start > 0:
        _fenster.blit(klein.render("↑ weitere Kategorien/ Gebäude", True, (170, 190, 220)), (760, 14))
    if start + sichtbare_zeilen < len(zeilen):
        _fenster.blit(klein.render("↓ weitere Kategorien/ Gebäude", True, (170, 190, 220)), (760, 42))
