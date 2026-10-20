# blackjack

Egy letisztult blackjack játék ami Python-t és a pygame könyvtárat használva készűlt. Egyedi tétrakási chipekkel, mentéskezeléssel és dinamikus kártyamegjelenítéssel rendelkezik.

IteraktÍv fogadási rendszer: a választható chippek értéke (10-től 1000-ig) a saját pénzed mennyiségén alapszik.
Mentési rendszer: Automatikusan betölti és elmenti az egyenleged egy "mentes.txt" fájlba, így az egyenleged megmarad a játékmenetek között.
Dinamikus kártya-és szimbólum keverés: Minden kiosztott kártya egyedi jelöléssel kap a hagyományos francia kártya jelek alapján (pikk, káró, kőr és treff).
Osztó MI logika: Automatikus osztó kezelés a hagyományos kaszinó szabályok alapján (17 alatt lapot húz).

A programm .exe file-ként elinditható hogyha a "dist" mappába van rakva a pyinstaller könyvtárnak köszönhetően (python környezet nélkül is megy).
dist mappa tartama: 
-"main.exe"
-"hatter.png"
-"mentes.txt"
 