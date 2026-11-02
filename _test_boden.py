import sys, os, random
sys.path.insert(0, r'z:/Codes/Unterricht/Schuster/Fortgeschrittener Kurs/Terra_Nova')
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
pygame.init()
pygame.display.set_mode((800, 600))

import main

def karte_generieren_custom(gras=40, gestein=30, sand=30, r_gras=(6,12), r_gestein=(7,11), r_sand=(8,13)):
    karten_daten = []
    for zeile in range(main.WELT_HOEHE):
        neue_zeile = []
        for spalte in range(main.WELT_BREITE):
            neue_zeile.append(0)
        karten_daten.append(neue_zeile)

    configs = [
        ('sand', sand, r_sand, 3),
        ('gestein', gestein, r_gestein, 2),
        ('gras', gras, r_gras, 1),
    ]
    for typ_name, anzahl, r_range, typ_val in configs:
        for _ in range(anzahl):
            mitte_x = random.randint(5, main.WELT_BREITE - 5)
            mitte_y = random.randint(5, main.WELT_HOEHE - 5)
            radius = random.randint(*r_range)
            for zeile in range(main.WELT_HOEHE):
                for spalte in range(main.WELT_BREITE):
                    abstand = ((spalte - mitte_x) ** 2 + (zeile - mitte_y) ** 2) ** 0.5
                    if abstand < radius:
                        karten_daten[zeile][spalte] = typ_val
    
    return karten_daten

def messen(gras, gestein, sand, r_gras, r_gestein, r_sand, n=10):
    gesamt = [0, 0, 0, 0]
    for _ in range(n):
        kd = karte_generieren_custom(gras, gestein, sand, r_gras, r_gestein, r_sand)
        for zeile in kd:
            for val in zeile:
                gesamt[val] += 1
    total = sum(gesamt)
    pcts = [g/total*100 for g in gesamt]
    return pcts

pcts = messen(40, 30, 30, (6,12), (7,11), (8,13))
print(f'Erde: {pcts[0]:.1f}%, Gras: {pcts[1]:.1f}%, Gestein: {pcts[2]:.1f}%, Sand: {pcts[3]:.1f}%')