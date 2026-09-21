"""Darstellung und Mausklicks für Haupt-, Pausen- und Endmenüs."""

import pygame

_fenster = None


def menue_initialisieren(fenster_obj):
    """Merkt sich das Pygame-Fenster für die Menüzeichnung."""
    global _fenster
    _fenster = fenster_obj


def _button_rect(index):
    """Liefert die Position des index-ten Menüknopfs."""
    return pygame.Rect(220, 214 + index * 62, 560, 48)


def _zeilen_rect(anzahl, info_anzahl=0):
    """Liefert den Bereich, in dem Knöpfe und Hinweise liegen."""
    hoehe = min(588, max(220, 112 + anzahl * 62 + info_anzahl * 23 + 35))
    return pygame.Rect(170, 112, 660, hoehe)


def menu_zeichnen(titel, untertitel, optionen, deaktiviert=None,
                  info_zeilen=None, akzent=(90, 190, 255)):
    """Zeichnet ein zentriertes, klickbares Overlay.

    ``optionen`` besteht aus Tupeln der Form ``(id, beschriftung, taste)``.
    Die Rückgabe wird absichtlich nicht benötigt; die Positionen werden von
    ``aktion_fuer_klick`` mit denselben Regeln berechnet.
    """
    if _fenster is None:
        return

    deaktiviert = set(deaktiviert or ())
    info_zeilen = list(info_zeilen or ())

    overlay = pygame.Surface(_fenster.get_size(), pygame.SRCALPHA)
    overlay.fill((3, 7, 18, 232))
    _fenster.blit(overlay, (0, 0))

    panel = _zeilen_rect(len(optionen), len(info_zeilen))
    pygame.draw.rect(_fenster, (17, 24, 42), panel, border_radius=14)
    pygame.draw.rect(_fenster, akzent, panel, width=2, border_radius=14)

    gross = pygame.font.Font(None, 48)
    mittel = pygame.font.Font(None, 27)
    klein = pygame.font.Font(None, 20)

    titel_surface = gross.render(titel, True, (245, 248, 255))
    _fenster.blit(titel_surface,
                  (500 - titel_surface.get_width() // 2, 132))
    untertitel_surface = mittel.render(untertitel, True, (175, 190, 210))
    _fenster.blit(untertitel_surface,
                  (500 - untertitel_surface.get_width() // 2, 172))

    for index, option in enumerate(optionen):
        option_id, beschriftung, taste = option
        rect = _button_rect(index)
        ist_deaktiviert = option_id in deaktiviert
        fill = (35, 47, 70) if not ist_deaktiviert else (30, 32, 40)
        border = akzent if not ist_deaktiviert else (85, 88, 98)
        textfarbe = (240, 245, 255) if not ist_deaktiviert else (125, 130, 140)
        pygame.draw.rect(_fenster, fill, rect, border_radius=8)
        pygame.draw.rect(_fenster, border, rect, width=2, border_radius=8)
        label = f"{beschriftung}   [{taste}]"
        text_surface = mittel.render(label, True, textfarbe)
        _fenster.blit(text_surface,
                      (rect.centerx - text_surface.get_width() // 2,
                       rect.centery - text_surface.get_height() // 2))

    letzter_button = max(0, len(optionen) - 1)
    y = _button_rect(letzter_button).bottom + 18
    for zeile in info_zeilen:
        farbe = (220, 225, 235)
        if isinstance(zeile, tuple):
            zeile, farbe = zeile
        text_surface = klein.render(str(zeile), True, farbe)
        _fenster.blit(text_surface,
                      (500 - text_surface.get_width() // 2, y))
        y += 23


def aktion_fuer_klick(pos, optionen, deaktiviert=None):
    """Gibt die angeklickte Options-ID oder ``None`` zurück."""
    deaktiviert = set(deaktiviert or ())
    for index, option in enumerate(optionen):
        option_id = option[0]
        if option_id not in deaktiviert and _button_rect(index).collidepoint(pos):
            return option_id
    return None
