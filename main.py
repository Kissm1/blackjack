import random
import pygame
import math
import time
import os
import sys

pygame.init()

pygame.init()
pygame.font.init()
te_penzed = 1000
visszaallitos_penz = 1000

WIDTH, HEIGHT = (580, 800)
# A háttér és mentés.txt fájlok helyének meghatározása script és .exe esetében
if getattr(sys, "frozen", False):
  eleresi_ut = os.path.dirname(sys.executable)  # Az exe mappája
else:
  eleresi_ut = os.path.dirname(os.path.abspath(__file__))  # A script mappája

screen = pygame.display.set_mode((WIDTH, HEIGHT))

logos = ["♠","♥","♦","♣"]
ertek_huzas_nezo = {}
hatter_foto = os.path.join(eleresi_ut, "hatter.png")
mentes_fajl = os.path.join(eleresi_ut, "mentes.txt")
white = (255,255,255)
green = (20,50,10)
black = (0,0,0)
brown = (101, 67, 33)
gold = (212, 175, 55)
light_gold = (232, 195, 75)
red = (255,0,0)

kartya_kep = pygame.image.load(hatter_foto).convert_alpha()

jelenlegi_allapot = 1

jTC = {10: 0, 25: 0, 50: 0, 100: 0, 200: 0, 500: 0, 1000: 0}
chip_ertekek = [10, 25, 50, 100, 200, 500, 1000]

ertekek = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10,10,10,10]
fel_huzo= [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0, 0, 0,0,0]

te_osz_tet = 0
fogadas_elott = te_penzed

# Meglévő pénz beolvasása mentes.txt-ből
with open(mentes_fajl,"r", encoding="utf-8") as mentett:
    te_penzed = int(mentett.read().strip())

class Kartya():
    def __init__(self, ertek, lathato):
        self.ertek = ertek
        self.lathato = lathato
        self.mennyiseg = 0
        if ertek not in ertek_huzas_nezo:
            ertek_huzas_nezo[ertek] = 0

        # Assign symbol sequentially (0 -> ♠, 1 -> ♥, 2 -> ♦, 3 -> ♣)
        suit_index = ertek_huzas_nezo[ertek] % len(logos)
        self.szimbolum = logos[suit_index]

        # Mennyiség növelő minden alkalommal amikor fel van húzva
        ertek_huzas_nezo[ertek] += 1
    
def draw_text(text, color, x, y, size):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_symbols(text,color,x,y,size):
    font = pygame.font.SysFont("segoeuisymbol", size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def doboz_draw(text):
    pygame.draw.rect(screen, black, (85,0,410,105))
    pygame.draw.rect(screen, green, (90,0,400,100))
    draw_text(text, white,115,35,40)

def chip_terulet_draw():
    pygame.draw.rect(screen, brown, (0,580,580,200))

def bank_draw():
    pygame.draw.rect(screen, gold, (0,750,580,50))
    pygame.draw.rect(screen,light_gold, (WIDTH // 2 -120, 760, 240, 35))
    draw_text(f"Egyenleged: {te_penzed}", white,WIDTH // 2 - 110,765,35)

# A dinamikus pénz logikája
def melyik_chippek(fogadas_elott): 
    if fogadas_elott < 2000:
        return chip_ertekek[0:4] 
    elif fogadas_elott < 5000:
        return chip_ertekek[1:5] 
    elif fogadas_elott < 10000:
        return chip_ertekek[2:6] 
    else:
        return chip_ertekek[3:7] 

# A chippek megrajzolása
def chip_center(x):
  center_x = 60 * (x - 1) + 60 * x + 20 * x
  center_y = 680
  return center_x, center_y

def chippek_draw(x):
    aktiv_chippek = melyik_chippek(fogadas_elott)
    center_x, center_y = chip_center(x)
    pygame.draw.circle(screen, red, (center_x, center_y),60, 60)
    
    ertek = aktiv_chippek[x-1]
    if len(str(ertek)) == 2:
        draw_text(f"{ertek}", white,center_x - 20,660,60)
    elif len(str(ertek)) == 3: 
        draw_text(f"{ertek}", white,center_x - 35,660,60)
    else:
        draw_text(f"{ertek}", white,center_x - 50,660,60)
    
def nyomott_chip(eger_poz):
    active_chips = melyik_chippek(fogadas_elott)
    eger_x, eger_y = eger_poz
    radiusz = 60

    for x in range(1, 5):
        center_x, center_y = chip_center(x)

        distance = math.hypot(eger_x - center_x, eger_y - center_y)

        if distance <= radiusz:
            return active_chips[x - 1]

    return None

def fogadott_penzek():
  aktiv_chip = melyik_chippek(fogadas_elott)

  kezdo_x = 45
  kezdo_y = 150
  offset_y = 0

  for chip_ertek in aktiv_chip:
    db = jTC[chip_ertek]

    if db > 0:
        pygame.draw.circle(screen, red, (kezdo_x, kezdo_y + offset_y), 45, 45)

        szoveg = f"{db}db {chip_ertek}"
        if len(str(chip_ertek)) == 2:
            draw_text(szoveg, white, kezdo_x-30, kezdo_y + offset_y - 10, 30)
        elif len(str(chip_ertek)) == 3:
            draw_text(szoveg, white, kezdo_x-37.5, kezdo_y + offset_y - 10, 30)
        else:
            draw_text(szoveg, white, kezdo_x-45, kezdo_y + offset_y - 10, 30)
        offset_y += 100

start_btn = pygame.Rect(WIDTH // 2 - 100, 520,200,50)

# A kártyák megrajzolása
def kartya_draw(kartya, x, y):
    kartya_szelesseg = 70
    kartya_magassag = 100
    kartya_negyszög = pygame.Rect(x, y, kartya_szelesseg, kartya_magassag)

    logo = kartya.szimbolum
            
    if kartya.lathato:
        pygame.draw.rect(screen, (255, 255, 255), kartya_negyszög, border_radius=8)
        pygame.draw.rect(screen, (black), kartya_negyszög, 2, border_radius=8)
        if logo == "♥" or logo == "♦":
            draw_symbols(str(logo), (red), x + 3, y + 3, 20)
            draw_symbols(str(logo), (red), x + 3, y + 70, 20)
            draw_symbols(str(logo), (red), x + 53, y + 3, 20)
            draw_symbols(str(logo), (red), x + 53, y + 70, 20)
            draw_text(str(kartya.ertek), (red), x + 22, y + 35, 40)
        else:
            draw_symbols(str(logo), (black), x + 3, y + 3, 20)
            draw_symbols(str(logo), (black), x + 3, y + 70, 20)
            draw_symbols(str(logo), (black), x + 53, y + 3, 20)
            draw_symbols(str(logo), (black), x + 53, y + 70, 20)
            draw_text(str(kartya.ertek), (black), x + 22, y + 35, 40)
    else:
        pygame.draw.rect(screen, (30, 30, 150), kartya_negyszög, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), kartya_negyszög, 2, border_radius=8)

def kartya_jelenito(te_ol, osz_ol):
  oszto_start_x = 200 / len(osz_ol) + 100
  oszto_start_y = 120
  for index, kartya in enumerate(osz_ol):
    if len(osz_ol) > 4:
        if index + 1 > 4:
            kartya_draw(kartya, oszto_start_x + ((index - 4) * 85), oszto_start_y + 100)
        else:
            kartya_draw(kartya, oszto_start_x + (index * 85), oszto_start_y)
    else:
        kartya_draw(kartya, oszto_start_x + (index * 85), oszto_start_y)

  te_start_x = 200 / len(te_ol) + 100
  te_start_y = 460
  for index, kartya in enumerate(te_ol):
    if len(te_ol) > 4:
        if index + 1 > 4:
            kartya_draw(kartya, te_start_x + ((index - 4) * 85), te_start_y - 100)
        else:
            kartya_draw(kartya, te_start_x + (index * 85), te_start_y)
    else:
        kartya_draw(kartya, te_start_x + (index * 85), te_start_y)

#gombok megrajzolása
def gomb_center(x):
    center_x = (60 * (x - 1) + 60 * x + 20 * x) * 2
    center_y = 680
    return center_x, center_y

def s2_gombok_draw(x):
    center_x, center_y = gomb_center(x)
    pygame.draw.circle(screen, red, (center_x, center_y),60, 60)
    if x == 1:
        draw_text(f"{gombok[x-1]}", white,center_x - 40,660,60)
    elif x == 2: 
        draw_text(f"{gombok[x-1]}", white,center_x - 45,660,60)

def gomb_funkciok(eger_poz):
    eger_x, eger_y = eger_poz
    radiusz = 60

    for x in range(1,3):
        center_x, center_y = gomb_center(x)

        distance = math.hypot(eger_x - center_x, eger_y - center_y)

        if distance <= radiusz:
            return gombok[x-1]

    return None

# Kép és állapotok megjelenítése
def board_draw():
    screen.blit(kartya_kep, (0, 0))
    if jelenlegi_allapot == 1:
        doboz_draw("Kérlek helyezz be chippet")
    elif jelenlegi_allapot == 2:
        doboz_draw("Húzz fel kártyát!")
    elif jelenlegi_allapot == 3:
        doboz_draw("Az osztó húz kártyákat")
    chip_terulet_draw()
    bank_draw()
    
def oKSZ():
    te_ossz = 0
    for i in range(len(te_ol)):
        te_ossz += te_ol[i].ertek

    draw_text(f"Össz: {te_ossz}", white, 450, 590, 45)
    osz_ossz = 0
    for i in range(len(osz_ol)):
        if osz_ol[i].lathato == True:
            osz_ossz += osz_ol[i].ertek
    pygame.draw.rect(screen,black,(438,188,144,59), border_radius=8)
    pygame.draw.rect(screen,brown,(440,190,140,55), border_radius=8)
    draw_text(f"Össz: {osz_ossz}", white, 450, 200, 45)

    return te_ossz, osz_ossz

def allapot_egy_draw():
    pygame.draw.rect(screen,red, (WIDTH // 2 - 100, 520,200,50))
    draw_text("Induljon!", white, WIDTH // 2 - 80, 525, 55)
    for x in range(1,5):
        chippek_draw(x)
    fogadott_penzek()
    start_btn

def allapot_ketto_draw():
    draw_text(f"Téted: {te_osz_tet}", white, 10, 590, 45)
    kartya_jelenito(te_ol, osz_ol)
    for x in range(1,3):
        s2_gombok_draw(x)
    te_ossz,osz_ossz = oKSZ()
    return te_ossz, osz_ossz

def allapot_harom_draw():
    draw_text(f"Téted: {te_osz_tet}", white, 10, 590, 45)
    kartya_jelenito(te_ol, osz_ol)
    te_ossz,osz_ossz = oKSZ()
    return te_ossz, osz_ossz

def allapot_negy_draw(donto):
    pygame.draw.rect(screen,black,(WIDTH // 2 - 275, HEIGHT // 2 - 65, 550, 170), border_radius=12)
    pygame.draw.rect(screen,brown,(WIDTH // 2 - 270, HEIGHT // 2 - 60, 540, 160), border_radius=12)
    if donto == 2:
        draw_text("Nyertél!", white, WIDTH //2 - 85, HEIGHT // 2 - 50, 50)
    elif donto == 1:
        draw_text("Veszítettél!", white, WIDTH //2 - 100, HEIGHT // 2 - 50, 50)
    else:
        draw_text("Döntetlen!", white, WIDTH //2 - 93, HEIGHT // 2 - 50, 50)
    if te_penzed > 0:
        draw_text("Kattints az újra játszáshoz!", white, WIDTH //2 - 230, HEIGHT // 2, 50)
    else:
        draw_text("Kifogytál pénzből!", white, WIDTH //2 - 150, HEIGHT // 2, 50)
        draw_text("Kattints a kilépéshez!!", white, WIDTH //2 - 180, HEIGHT // 2 + 50, 50)

# Alaphelyzet kialakítása
helyzet = 0
te_ossz = 0
gombok = ["Húz", "Elég"]
osz_ol = []
kartya_1 = Kartya(random.choice(ertekek),True)
osz_ol.append(kartya_1)

kartya_1 = Kartya(random.choice(ertekek),False)
osz_ol.append(kartya_1) 

osz_ossz = 0
te_ol = []
kartya_1 = Kartya(random.choice(ertekek),True)
te_ol.append(kartya_1)

kartya_1 = Kartya(random.choice(ertekek),True)
te_ol.append(kartya_1)

run = True
oszto_ido = 0
while run:
    board_draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if jelenlegi_allapot == 1:
                    nyCE = nyomott_chip(event.pos)
                    if nyCE is not None:
                        if te_penzed >= nyCE:
                            te_penzed -= nyCE
                            te_osz_tet += nyCE
                            jTC[nyCE] += 1
                    if start_btn.collidepoint(event.pos) and te_osz_tet > 0:
                        jelenlegi_allapot = 2
                elif jelenlegi_allapot == 2:
                    
                    lG = gomb_funkciok(event.pos)
                    if lG is not None:
                        if lG == "Húz":
                            kartya_1 = Kartya(random.choice(ertekek),True)
                            while fel_huzo[kartya_1.ertek] > 4:
                                kartya_1 = Kartya(random.choice(ertekek),True)
                            te_ol.append(kartya_1)
                            
                            te_ossz = 0
                        if lG == "Elég":
                            jelenlegi_allapot = 3
                            oszto_ido = pygame.time.get_ticks()
                elif jelenlegi_allapot == 3:
                    pass
                elif jelenlegi_allapot == 4:
                    if te_penzed > 0: # Reset alapheéyzetre
                        ertek_huzas_nezo.clear()
                        te_osz_tet = 0
                        helyzet = 0
                        te_ossz = 0
                        osz_ol = []
                        kartya_1 = Kartya(random.choice(ertekek),True)
                        osz_ol.append(kartya_1)
                        kartya_1 = Kartya(random.choice(ertekek),False)
                        osz_ol.append(kartya_1) 
                        osz_ossz = 0
                        te_ol = []
                        kartya_1 = Kartya(random.choice(ertekek),True)
                        te_ol.append(kartya_1)
                        kartya_1 = Kartya(random.choice(ertekek),True)
                        te_ol.append(kartya_1)
                        jTC = {10: 0, 25: 0, 50: 0, 100: 0, 200: 0, 500: 0, 1000: 0}
                        jelenlegi_allapot = 1
                    else:
                        run = False

    if jelenlegi_allapot == 1:
        allapot_egy_draw()
        
    elif jelenlegi_allapot == 2:
        te_ossz, osz_ossz = allapot_ketto_draw()
        if te_ossz > 21:
            helyzet = 1
            fogadas_elott = te_penzed
            jelenlegi_allapot = 4
        if te_ossz == 21:
            helyzet = 2
            te_penzed += te_osz_tet * 2
            fogadas_elott = te_penzed
            jelenlegi_allapot = 4
    elif jelenlegi_allapot == 3:
        te_ossz, osz_ossz = allapot_harom_draw()
        for i in range(len(osz_ol)):
            osz_ol[i].lathato = True
        if 17 > osz_ossz:
            if pygame.time.get_ticks() - oszto_ido >= 1000:
                kartya_1 = Kartya(random.choice(ertekek),True)
                while fel_huzo[kartya_1.ertek] > 4:
                    kartya_1 = Kartya(random.choice(ertekek),True)
                osz_ol.append(kartya_1)
                oszto_ido = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - oszto_ido >= 1000:
                if osz_ossz > 21 or te_ossz > osz_ossz:
                    helyzet = 2
                    te_penzed += te_osz_tet * 2
                    fogadas_elott = te_penzed
                    jelenlegi_allapot = 4
                elif osz_ossz > te_ossz:
                    helyzet = 1
                    jelenlegi_allapot = 4
                    fogadas_elott = te_penzed
                elif osz_ossz == te_ossz:
                    helyzet = 0
                    te_penzed += te_osz_tet
                    fogadas_elott = te_penzed
                    jelenlegi_allapot = 4

    elif jelenlegi_allapot == 4:
        allapot_negy_draw(helyzet)

        
    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()

# Mentés
with open (mentes_fajl, "w", encoding="utf-8") as mentes:
    if te_penzed > 0:
        mentes.write(str(te_penzed))
    else:
        mentes.write(str(visszaallitos_penz))
