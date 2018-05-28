from math import log

def generowaniePrzypadkow(playerhp, przypadki, countprzypadki):
    # czy użyć miecza stalowego?
    #liczymy entropię dla przypadku playerhp
    #BROŃ PUNKTY LATA PODŁOŻE TARCZA POTWÓR, HP
    przypadkX = [] #Najpierw entropia wg której będziemy sortować, potem
    damageTable = [ #będzie potrzebna do generowania dzieci każdego z przypadków dla każdej broni
    [[0,6],[0,3,6],[0,2],[0,3]], #dla miecza stalowego
    [[0,6],[0,3,6],[0,2],[2,0]], #dla miecza srebrnego
    [[0,6],[0,3,6],[0,0],[0,3]], #dla topora
    [[0,0],[0,0,6],[0,2],[0,0]], #dla łuku
    [[0,0],[0,0,6],[0,0],[0,0]]  #dla kuli ognia
    ]
    for i in range (0, 5):
        fly = [[0,0],[0,0]] #dla True sprawdzamy kiedy przeżył i dla False
        podloze = [[0,0],[0,0],[0,0]] # przypadki ok 0-2 i wszystkie 3
        tarcza = [[0,0],[0,0]]
        potwor = [[0,0],[0,0]]
        counterprzypadku = 0
        counterPrzezyc = 0
        for j in range(0, countprzypadki[i]):
            if int(przypadki[i][j][6]) - int(przypadki[i][j][7]) <= playerhp: # liczymy tylko te przypadki gdzie mamy ok hp
                counterprzypadku += 1
                if przypadki[i][j][1] != '-2000':
                    counterPrzezyc += 1
            # SPRAWDZAMY FLY
                if przypadki[i][j][2] == 'True':
                    if przypadki[i][j][1] != '-2000':
                        fly[0][0] += 1
                    fly[0][1] += 1
                else:
                    if przypadki[i][j][1] != '-2000':
                        fly[1][0] += 1
                    fly[1][1] += 1
            # SPRAWDZAMY PODŁOŻE
                if przypadki[i][j][3] == '.':
                    if przypadki[i][j][1] != '-2000':
                        podloze[0][0] += 1
                    podloze[0][1] += 1
                elif przypadki[i][j][3] == '5':
                    if przypadki[i][j][1] != '-2000':
                        podloze[1][0] += 1
                    podloze[1][1] += 1
                else:
                    if przypadki[i][j][1] != '-2000':
                        podloze[2][0] += 1
                    podloze[2][1] += 1
            #SPRAWDZAMY TARCZĘ
                if przypadki[i][j][4] == '1':
                    if przypadki[i][j][1] != '-2000':
                        tarcza[0][0] += 1
                    tarcza[0][1] += 1
                else:
                    if przypadki[i][j][1] != '-2000':
                        tarcza[1][0] += 1
                    tarcza[1][1] += 1
            #SPRAWDZAMY POTWORA
                if przypadki[i][j][2] == 'True':
                    if przypadki[i][j][1] != '-2000':
                        potwor[0][0] += 1
                    potwor[0][1] += 1
                else:
                    if przypadki[i][j][1] != '-2000':
                        potwor[1][0] += 1
                    potwor[1][1] += 1
        #print(i)
        #print("fly:")
        #print(fly)
        #print("podloze:")
        #print(podloze)
        print("tarcza")
        print(tarcza)
        #print("potwor")
        #print(potwor)

        #ENTROPIA DLA FLY
        if fly[0][1] > 0 and fly[0][0] > 0 and fly[0][1] != fly[0][0]:
            ent_fly_true = -(fly[0][0]/fly[0][1]*log(fly[0][0]/fly[0][1]) + (1 - fly[0][0]/fly[0][1])*log(1 - fly[0][0]/fly[0][1])  )
        else:
            ent_fly_true = 0
        #print("ent_fly_true: " + str(ent_fly_true))
        if fly[1][1] > 0 and fly[1][0] > 0 and fly[1][1] != fly[1][0]:
            ent_fly_false = -(fly[1][0]/fly[1][1]*log(fly[1][0]/fly[1][1]) + (1 - fly[1][0]/fly[1][1])*log(1 - fly[1][0]/fly[1][1])  )
        else:
            ent_fly_false = 0
        #print("ent_fly_false: " + str(ent_fly_false))

        if fly[0][1]+fly[1][1] >0:
            ent_fly = fly[0][1]/ (fly[0][1]+fly[1][1])*ent_fly_true + fly[1][1]/ (fly[0][1]+fly[1][1])*ent_fly_false
        else:
            ent_fly = 0
        #print("ent_fly: " + str(ent_fly))

        #ENTROPIA DLA PODŁOŻA
        if podloze[0][1] > 0 and podloze[0][0] > 0 and podloze[0][1] != podloze[0][0]:
            ent_podloze_trawa = -(podloze[0][0]/podloze[0][1]*log(podloze[0][0]/podloze[0][1]) + (1 - podloze[0][0]/podloze[0][1])*log(1 -podloze[0][0]/podloze[0][1])  )
        else:
            ent_podloze_trawa = 0
        #print("ent_podloze_trawa: " + str(ent_podloze_trawa))

        if podloze[1][1] > 0 and podloze[1][0] > 0 and podloze[1][1] != podloze[1][0]:
            ent_podloze_woda = -(podloze[1][0]/podloze[1][1]*log(podloze[1][0]/podloze[1][1]) + (1 - podloze[1][0]/podloze[1][1])*log(1 -podloze[1][0]/podloze[1][1])  )
        else:
            ent_podloze_woda = 0
        #print("ent_podloze_woda: " + str(ent_podloze_woda))

        if podloze[2][1] > 0 and podloze[2][0] > 0 and podloze[2][1] != podloze[2][0]:
            ent_podloze_bloto = -(podloze[2][0]/podloze[2][1]*log(podloze[2][0]/podloze[2][1]) + (1 - podloze[2][0]/podloze[2][1])*log(1 -podloze[2][0]/podloze[2][1])  )
        else:
            ent_podloze_bloto = 0
        #print("ent_podloze_bloto: " + str(ent_podloze_bloto))

        if podloze[0][1]+podloze[1][1]+podloze[2][1] >0:
            ent_podloze = podloze[0][1]/ (podloze[0][1]+podloze[1][1]+podloze[2][1])*ent_podloze_trawa + podloze[1][1]/ (podloze[0][1]+podloze[1][1]+podloze[2][1])*ent_podloze_woda
            ent_podloze += podloze[2][1]/ (podloze[0][1]+podloze[1][1]+podloze[2][1])*ent_podloze_bloto
        else:
            ent_podloze = 0
        #print("ent_podloze: " + str(ent_podloze))

        #ENTROPIA DLA TARCZA
        if tarcza[0][1] > 0 and tarcza[0][0] > 0 and tarcza[0][1] != tarcza[0][0]:
            ent_tarcza_true = -(tarcza[0][0]/tarcza[0][1]*log(tarcza[0][0]/tarcza[0][1]) + (1 - tarcza[0][0]/tarcza[0][1])*log(1 - tarcza[0][0]/tarcza[0][1])  )
        else:
            ent_tarcza_true = 0
        print("ent_tarcza_true: " + str(ent_tarcza_true))
        if tarcza[1][1] > 0 and tarcza[1][0] > 0 and tarcza[1][1] != tarcza[1][0]:
            ent_tarcza_false = -(tarcza[1][0]/tarcza[1][1]*log(tarcza[1][0]/tarcza[1][1]) + (1 - tarcza[1][0]/tarcza[1][1])*log(1 - tarcza[1][0]/tarcza[1][1])  )
        else:
            ent_tarcza_false = 0
        print("ent_tarcza_false: " + str(ent_tarcza_false))

        if tarcza[0][1]+tarcza[1][1] >0:
            ent_tarcza = tarcza[0][1]/ (tarcza[0][1]+tarcza[1][1])*ent_tarcza_true + tarcza[1][1]/ (tarcza[0][1]+tarcza[1][1])*ent_tarcza_false
        else:
            ent_tarcza = 0
        print("ent_tarcza: " + str(ent_tarcza))

        #ENTROPIA DLA POTWÓR
        if potwor[0][1] > 0 and potwor[0][0] > 0 and potwor[0][1] != potwor[0][0]:
            ent_potwor_true = -(potwor[0][0]/potwor[0][1]*log(potwor[0][0]/potwor[0][1]) + (1 - potwor[0][0]/potwor[0][1])*log(1 - potwor[0][0]/potwor[0][1])  )
        else:
            ent_potwor_true = 0
        #print("ent_potwor_true: " + str(ent_potwor_true))
        if potwor[1][1] > 0 and potwor[1][0] > 0 and potwor[1][1] != potwor[1][0]:
            ent_potwor_false = -(potwor[1][0]/potwor[1][1]*log(potwor[1][0]/potwor[1][1]) + (1 - potwor[1][0]/potwor[1][1])*log(1 - potwor[1][0]/potwor[1][1])  )
        else:
            ent_potwor_false = 0
        #print("ent_potwor_false: " + str(ent_potwor_false))

        if potwor[0][1]+potwor[1][1] >0:
            ent_potwor = potwor[0][1]/ (potwor[0][1]+potwor[1][1])*ent_potwor_true + potwor[1][1]/ (potwor[0][1]+potwor[1][1])*ent_potwor_false
        else:
            ent_potwor = 0
        #print("ent_potwor: " + str(ent_potwor))
        przypadkX.append( #dodajemy przypadki postaci - entropia, a potem tabela damage
            [
                [ent_fly, damageTable[i][0], "fly"],
                [ent_podloze, damageTable[i][1], "podloze"],
                [ent_tarcza, damageTable[i][2], "tarcza"],
                [ent_potwor, damageTable[i][3], "potwor"]
            ])
        przypadkX[i].sort() # i mamy sortowanie wg entropii, dzięki temu na samym szczycie drzewa będą przypadki o najniższej entropii
    #print(przypadkX)
    return przypadkX

class Node():
    def __init__(self, przypadki, hp, iterator):
        self.allprzypadki = przypadki
        print(iterator)
        self.iterator = iterator # dane do tworzenia drzewa będą przesyłane w tablicy, a iterator podaje kolejność podawania danych
        if self.iterator >= 0:
            self.przypadki = list(przypadki[3-self.iterator][1]) # przechowuje informacje ile hp traci bohater w każdym z przypadków
            self.hp = hp
            self.name = przypadki[3-self.iterator][2]
            self.childs = []
            #print("Oto przypadek: " + str(self.przypadki)+ self.name + str(self.iterator))
            self.done = False
            self.createChilds()
        else:
            self.przypadki = []
            self.hp = hp
            self.name = "End"
            self.done = True
            self.childs = []
            self.iterator = -1
            #print("Oto przypadek: " + str(self.przypadki)+ self.name + str(self.iterator))


    def createChilds(self):
        for i in range (0, len(self.przypadki)):
            if self.hp > 0:
                thisHp = self.hp - self.przypadki[i]
                if self.hp <= 0:
                    self.childs.append(Node([], 0 ,self.iterator-1) ) #Gdy bohater ma 0 lub mniej hp nie ma sensu sprawdzać dalej
                else:
                    self.childs.append(Node(self.allprzypadki, thisHp, self.iterator-1))

    def iteratorPrints(self):
        print(self.iterator)
        for i in range (0, len(self.childs)):
            self.childs[i].iteratorPrints()

    def czyPrzezyje(self, przypadek, ok, iterator):
        if iterator > 0:
            print(iterator)
            if len(self.childs) > 0 and ok != 1:
                i = 0 # dopasowujemy klucze
                while przypadek[i][0] != self.name:
                    i += 1
                self.childs[przypadek[i][1]].czyPrzezyje(przypadek, ok, iterator-1)
        else:
            print(iterator)
            print(self.hp)
            if self.hp > 0:
                print("Użyj tej broni")
                ok = 1
                return 1







#Podejmij decyzję sprawdza wszystkie przypadki od tego, któy daje najwięcej punktów do teog, który daje ich najmniej
def podejmijDecyzje(przypadek, przypadki, playerhp):
    dec = czyStalowy(przypadek, przypadki[0], playerhp)
    if dec == False:
        dec = czySrebrny(przypadek, przypadki[1], playerhp)
        if dec == False:
            dec = czyTopor(przypadek, przypadki[2], playerhp)
            if dec == False:
                dec = czyLuk(przypadek, przypadki[3], playerhp)
                if dec == False:
                    dec = czyKulaognia(przypadek, przypadki[4], playerhp)
                    if dec == False:
                        print("ZŁAP GO W YRDEN! - SAMA ZŁAP GO W YRDEN! (nie atakuj)")

def czyStalowy(przypadek, przypadki, playerhp):
    drzewko = Node(przypadki, playerhp, 3)
    ok = 0
    prawda = 0
    prawda = drzewko.czyPrzezyje(przypadek, ok, 3)
    if prawda:
        print("Użyj miecza stalowego")
        return True
    else:
        print("Nie używaj miecza stalowego")
        return False

def czySrebrny(przypadek, przypadki, playerhp):
    drzewko = Node(przypadki, playerhp, 3)
    ok = 0
    prawda = 0
    prawda = drzewko.czyPrzezyje(przypadek, ok, 3)
    if prawda:
        print("Użyj miecza srebrnego")
        return True
    else:
        print("Nie używaj miecza srebrnego")
        return False

def czyTopor(przypadek, przypadki, playerhp):
    drzewko = Node(przypadki, playerhp, 3)
    ok = 0
    prawda = 0
    prawda = drzewko.czyPrzezyje(przypadek, ok, 3)
    if prawda:
        print("Użyj topora")
        return True
    else:
        print("Nie używaj topora")
        return False

def czyLuk(przypadek, przypadki, playerhp):
    drzewko = Node(przypadki, playerhp, 3)
    ok = 0
    prawda = 0
    prawda = drzewko.czyPrzezyje(przypadek, ok, 3)
    if prawda:
        print("Użyj łuku")
        return True
    else:
        print("Nie używaj łuku")
        return False

def czyKulaognia(przypadek, przypadki, playerhp):
    drzewko = Node(przypadki, playerhp, 3)
    ok = 0
    prawda = 0
    drzewko.czyPrzezyje(przypadek, ok, 3)
    if prawda:
        print("Użyj Igni (kuli ognia)")
        return True
    else:
        print("Nie używaj Igni(kuli ognia)")
        return False
