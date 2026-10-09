import random

chip_ertekek = [10, 25, 50, 100, 200, 500, 1000]
visszaallitos_penz = 1000

ertekek = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10,10,10,10]
fel_huzo= [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0, 0, 0,0,0]

class Kartya():
    def __init__(self, ertek,lathato):
        self.ertek = ertek
        self.lathato = lathato
    def mennyiseg_donto():
        for i in range(ertekek):
            if ertek == ertekek[i]:
                ful_huzo[i] += 1
                break

uj_jatek = input("új játékot szeretnél kezdeni? ")
    
if uj_jatek == "igen":
    with open ('mentes.txt', "w", encoding="utf-8") as visszaallitas:
        visszaallitas.write(str(visszaallitos_penz))
    with open('mentes.txt', "r"  , encoding="utf-8") as mentett:
        te_penzed = int(mentett.read().strip())
    folytatas = "igen"
    
else:        
    with open('mentes.txt', "r"  , encoding="utf-8") as mentett:
        te_penzed = int(mentett.read().strip())
    folytatas = "igen"
          
while folytatas == "igen":            

    print(f"Az összes pénzed: {te_penzed}")
    te_tet = int(input("add meg a tétet! "))
    te_osz_tet = 0

    while te_tet != "":
        if te_tet not in chip_ertekek:
            print("rossz értéket adtál meg")
            te_tet = int(input("add meg a tétet! "))
        else:
            te_penzed = te_penzed - te_tet
            te_osz_tet += te_tet
            try:
                te_tet = int(input("add meg a tétet! "))
            except ValueError:
                print(f"a téted: {te_osz_tet}")
                break

    osz_ol = []
    osz_ol.append(Kartya(random.choice(ertekek),True))
    osz_ol.append(Kartya(random.choice(ertekek),False))    
    osz_ossz = 0
    for i in range(len(osz_ol)):
        osz_ossz += osz_ol[i].ertek

    te_ol = []
    te_ol.append(Kartya(random.choice(ertekek),True))
    te_ol.append(Kartya(random.choice(ertekek),True))

    for i in range(len(te_ol)):
        print(te_ol[i].ertek)
    
    te_ossz = 0
    for i in range(len(te_ol)):
        te_ossz += te_ol[i].ertek

    dontes = input("Húzol vagy maradsz? ")

    while dontes.lower() == "húzok" and te_ossz < 21:
        te_ol.append(Kartya(random.choice(ertekek),True))
        te_ossz = 0
        for i in range(len(te_ol)):
            print(te_ol[i].ertek) or te_ossz > osz_ossz
            te_ossz += te_ol[i].ertek
        if te_ossz < 21:
            dontes = input("Húzol? ")
        
    for i in range(len(osz_ol)):
        osz_ol[i].lathato = True
    
    while osz_ossz < 17:
        osz_ol.append(Kartya(random.choice(ertekek),True))
        osz_ossz = 0
        for i in range(len(osz_ol)):
            osz_ossz += osz_ol[i].ertek
    print(f"játékos: {te_ossz}")
    print(f"dealer:{osz_ossz}")

    if te_ossz > 21:
        print("Vesztettél!")
        te_osz_tet = 0
    elif te_ossz == 21 and not osz_ossz == te_ossz or osz_ossz > 21 or te_ossz > osz_ossz:
        print("Nyertél!")
        te_penzed = te_penzed + (2* te_osz_tet)
    elif osz_ossz == te_ossz:
        print("Döntetlen!")
        te_penzed += te_osz_tet
    elif osz_ossz > te_ossz:
        print("Vesztettél!")
        te_osz_tet = 0
        
    if te_penzed <= 0:
        break

    folytatas = input("Szeretnéd folytatni? ")
    
print(F"Ennyi pénzel végezted a játszmát: ", te_penzed)

if te_penzed > 0:
    with open ('mentes.txt', "w", encoding="utf-8") as mentes:
        mentes.write(str(te_penzed))
else:
    with open ('mentes.txt', "w", encoding="utf-8") as visszaallitas:
            visszaallitas.write(str(visszaallitos_penz))
