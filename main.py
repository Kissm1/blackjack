import random

chip_ertekek = [10, 25, 50, 100, 200, 500, 1000]
te_penzed = 1000

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
            print(f"a téted: {1000 - te_penzed}")
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

print(te_penzed)