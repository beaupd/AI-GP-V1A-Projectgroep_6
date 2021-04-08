"""
 ________________________________________________________________________________________________
(_________________________________ VERPLICHTE STEEKPROEVEN ______________________________________)
4.a.    Bezoeker met profiel 5b445abd61afda0001c57277 opent de categoriepagina 'Gezond & verzorging'. 
        Welke producten worden aanbevolen?
4.b.    Idem voor profiel 5a0d02e3a56ac6edb4c0ad5a 
4.c.    Idem voor profiel 5a7ce5090bce0f000198fcf5 
 ________________________________________________________________________________________________
(________________________ TEST OMSCHRIJVING VOOR VALIDATIE POPULAR ______________________________)
Er zijn 5 mogelijke users:
1. User is bekend en heeft eerdere orders
2. User is bekend en heeft geen eerdere orders en geen huidige klik events
3. User is bekend en heeft geen eerdere orders en wel huisige klik events
4. User is onbekend en heeft geen huidige klik events
5. User is onbekend en heeft wel huidige klik events

Verzameling 1 kan worden onderverdeeld in profielen met overduidelijke mannelijke producten, 
vrouwen producten en unisex producten. Voor deze verzameling worden elk 4 profielen aangesteld.
Voor de verzamelingen 2,3,4 en 5 soorten users zijn 4 profielen aangesteld.
Daarnaast wordt er gekeken voor elk profiel naar 
de categoriepagina's: gezond & verzorging, wonen & vrije tijd.
Verder wordt voor de verzamelingen 2,3,4 en 5 gebruik gemaakt van drie mogelijke gender verhoudingen 
qua producten: (1) man:2, vrouw:1, unisex:1, (2) man:1, vrouw:2, unisex:1 en 
(3) man:1, vrouw:1, unisex: 2. 
Deze dienen als de huidige klik events.

||------------------------------------- Verzameling 1 ------------------------------------------||
Voor elk gender in verzameling 1 loop
    Voor elke categorie in verzameling categorieën loop
        Vraag om recommendations op basis van het profiel en de categorie
        Voor elk product in recommendations loop
            Als product gender overeenkomt met gender in verzameling, 1
            Anders 0

||---------------------------------- Verzameling 2 en 4 ----------------------------------------||
Voor elke profiel in verzameling loop
    Voor elke verzameling producten (1/2/3) loop
        Vraag om recommendations op basis van het profiel, categorie en verzameling producten
        select genders van recommendations
        select categories van recommendations
        Als productverzameling 1 dan
            Als product genders overeenkomen met gender 'man', 1
            Anders 0
        Als productverzameling 2 dan
            Als product genders overeenkomen met gender 'vrouw', 1
            Anders 0
        Anders
            Als product genders overeenkomen met gender 'unisex', 1
            Anders 0

||---------------------------------- Verzameling 3 en 5 ---------------------------------------||
Voor elke profiel in verzameling loop
    Voor elke categorie in verzameling categorieën loop
        Voor elke verzameling producten (1/2/3) loop
            Vraag om recommendations op basis van het profiel, categorie en verzameling producten
            select genders van recommendations
            select categories van recommendations
            Als productverzameling 1 dan
                Als product genders overeenkomen met gender 'man' en catagory met categorie, 1
                Anders 0
            Als productverzameling 2 dan
                Als product genders overeenkomen met gender 'vrouw' en catagory met categorie, 1
                Anders 0
            Anders
                Als product genders overeenkomen met gender 'unisex' en catagory met categorie, 1
                Anders 0
"""
from popular_return_recoms import return_recommended_products

#  ________________________________________________________________________________________________
# (_________________________________ VERPLICHTE STEEKPROEVEN ______________________________________)
def test_verplichte_steekproef():
    # PROFILE                   BEKEND  ORDERS  SEGMENT GENDER  CATEGORY              EXPECTED RECOMS  
    # 5b445abd61afda0001c57277  1       1       buyer   Null    gezond & verzorging   43903
    #                                                                                 43911
    #                                                                                 43920
    #                                                                                 43928
    # 5a0d02e3a56ac6edb4c0ad5a  0       0                       gezond & verzorging   1475
    #                                                                                 151616
    #                                                                                 152264
    #                                                                                 1541
    # 5a7ce5090bce0f000198fcf5  1       1       browser baby    gezond & verzorging   43910
    cases = [
        ("5b445abd61afda0001c57277", ['43903', '43911', '43920', '43928']),
        ("5a0d02e3a56ac6edb4c0ad5a", ['1475', '151616', '152264', '1541']),
        ("5a7ce5090bce0f000198fcf5", ['43910', None, None, None])
    ]
    for case in cases:
        prodids = return_recommended_products(case[0], 'gezond & verzorging', [])
        assert prodids == case[1], f"De input {case[0]} geeft niet de juiste output {prodids}. De verwachte output is {cases[1]}"


#  ________________________________________________________________________________________________
# (________________________ TEST OMSCHRIJVING VOOR VALIDATIE POPULAR ______________________________)
def test_verzameling1():
    # PROFILE                   SEGMENT     GENDER      CATEGORY                EXPECTED RECOMS 
    # 59dce306a56ac6edb4c127a3  buyer       man         gezond & verzorging     1475
    #                                                                           151616
    #                                                                           152264
    #                                                                           1542
    # 59dce40ea56ac6edb4c37e1a  bouncer     man         gezond & verzorging     1475
    #                                                                           151616
    #                                                                           152264
    #                                                                           1542
    # 59dce40ea56ac6edb4c37e25  browser     man         gezond & verzorging     1475
    #                                                                           152264
    #                                                                           1542
    #                                                                           1551
    # 59dce306a56ac6edb4c127a3  buyer       man         gezond & verzorging     '...'
    # 5a3945b0ed29590001038fea  browser     vrouw       gezond & verzorging     16791
    #                                                                           1680
    #                                                                           16800
    #                                                                           1685
    # 5a39484fed2959000103930c  judger      vrouw       gezond & verzorging     16791
    #                                                                           16800
    #                                                                           16834
    #                                                                           1686
    # 5a394ab6a825610001bb7b02  buyer       vrouw       gezond & verzorging     4679
    #                                                                           4736
    #                                                                           4759
    #                                                                           4815
    # 5a395a04ed2959000103aa47  browser     vrouw       gezond & verzorging     '...'
    # 59dce306a56ac6edb4c12c6e  buyer       unisex      gezond & verzorging     40066
    #                                                                           40344
    #                                                                           40353
    #                                                                           42290
    # 59dce40ea56ac6edb4c37e5e  leaver      unisex      gezond & verzorging     33070
    #                                                                           33086
    #                                                                           33122
    #                                                                           33191
    # 59dce40fa56ac6edb4c37f56  leaver      unisex      gezond & verzorging     '...'
    # 59dce424a56ac6edb4c3d8d6  bouncer     unisex      gezond & verzorging     40066
    #                                                                           40344
    #                                                                           42290
    #                                                                           43148
    # etc.
    cases_male = [
        (("59dce306a56ac6edb4c127a3", "gezond & verzorging", []), ["1475", "151616", "152264", "1542"]),
        (("59dce40ea56ac6edb4c37e1a", "gezond & verzorging", []), ["1475", "151616", "152264", "1542"]),
        (("59dce40ea56ac6edb4c37e25", "gezond & verzorging", []), ["1475", "152264", "1542", "1551"]),
        (("59dce306a56ac6edb4c127a3", "gezond & verzorging", []), ["1475", "151616", "152264", "1542"]),
        (("59dce306a56ac6edb4c127a3", "wonen & vrije tijd", []), ["44436", "44649", "44650", "45202"]),
        (("59dce40ea56ac6edb4c37e1a", "wonen & vrije tijd", []), ["44436", "44649", "44650", "45202"]),
        (("59dce40ea56ac6edb4c37e25", "wonen & vrije tijd", []), ["44436", "44650", "45202", "45204-bulldog"]),
        (("59dce306a56ac6edb4c127a3", "wonen & vrije tijd", []), ["44436", "44649", "44650", "45202"])
    ]
    cases_female = [
        (("5a3945b0ed29590001038fea", "gezond & verzorging", []), ["16791", "1680", "16800", "1685"]),
        (("5a39484fed2959000103930c", "gezond & verzorging", []), ["16791", "16800", "16834", "1686"]),
        (("5a394ab6a825610001bb7b02", "gezond & verzorging", []), ["4679", "4736", "4759", "4815"]),
        (("5a395a04ed2959000103aa47", "gezond & verzorging", []), ["16791", "1680", "16800", "1685"]),
        (("5a3945b0ed29590001038fea", "wonen & vrije tijd", []), ["35936", "40147", "40152", "40157"]),
        (("5a39484fed2959000103930c", "wonen & vrije tijd", []), ["35936", "40845-stip", "41355", "42224"]),
        (("5a394ab6a825610001bb7b02", "wonen & vrije tijd", []), ["7523", None, None, None]),
        (("5a395a04ed2959000103aa47", "wonen & vrije tijd", []), ["35936", "40147", "40152", "40157"])
    ]
    cases_unisex = [
        (("59dce306a56ac6edb4c12c6e", "gezond & verzorging", []), ["40066", "40344", "40353", "42290"]),
        (("59dce40ea56ac6edb4c37e5e", "gezond & verzorging", []), ["33070", "33086", "33122", "33191"]),
        (("59dce40fa56ac6edb4c37f56", "gezond & verzorging", []), ["33070", "33086", "33122", "33191"]),
        (("59dce424a56ac6edb4c3d8d6", "gezond & verzorging", []), ["40066", "40344", "42290", "43148"]),
        (("59dce306a56ac6edb4c12c6e", "wonen & vrije tijd", []), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("59dce40ea56ac6edb4c37e5e", "wonen & vrije tijd", []), ["38597", "38678-petunia", "38960-blauw", "38960-groen"]),
        (("59dce40fa56ac6edb4c37f56", "wonen & vrije tijd", []), ["38597", "38678-petunia", "38960-blauw", "38960-groen"]),
        (("59dce424a56ac6edb4c3d8d6", "wonen & vrije tijd", []), ["38597", "38610", "38960-blauw", "38960-groen"])
    ]
    for case in cases_male:
        prodids = return_recommended_products(case[0][0], case[0][1], case[0][2])
        assert prodids == case[1], f"De input {case[0]} bij cases_male, geeft de verkeerde output {prodids}. Verwachte output is {case[1]}"
    for case in cases_female:
        prodids = return_recommended_products(case[0][0], case[0][1], case[0][2])
        assert prodids == case[1], f"De input {case[0]} bij cases_female, geeft de verkeerde output {prodids}. Verwachte output is {case[1]}"
    for case in cases_unisex:
        prodids = return_recommended_products(case[0][0], case[0][1], case[0][2])
        assert prodids == case[1], f"De input {case[0]} bij cases_unisex, geeft de verkeerde output {prodids}. Verwachte output is {case[1]}"

def test_verzameling2_4():
    pass

def test_verzameling3_5():
    pass


def main():
    try:
        test_verplichte_steekproef()
        print("Verplichte steekproef CHECK!")

        test_verzameling1()
        print("Steekproef met verzameling 1 CHECK!")

        test_verzameling2_4()
        print("Steekproef met verzameling 2 en 4 CHECK!")

        test_verzameling3_5()
        print("Steekproef met verzameling 3 en 5 CHECK!")
    except AssertionError as ae:
        print(ae)

if __name__ == "__main__":
    main()