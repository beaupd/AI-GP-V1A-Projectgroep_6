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
Verder wordt voor de verzamelingen 3 en 5 gebruik gemaakt van drie mogelijke gender verhoudingen 
qua producten: (1) man:2, vrouw:1, unisex:1, (2) man:1, vrouw:2, unisex:1 en 
(3) man:1, vrouw:1, unisex: 2. 
Deze dienen als de huidige klik events.

||------------------------------------- Verzameling 1 ------------------------------------------||
Bij verzameling 1 wordt er gewerkt met het popular algoritme van begin tot eind en wordt
dus gekeken naar het segment en gender kenmerk van een gebruiker. Op basis hiervan wordt gekeken
welke productid's passen bij deze kenmerken in combinatie met de categoriepagina waarop een 
user zich bevindt.

||---------------------------------- Verzameling 2 en 4 ----------------------------------------||
Bij verzameling 2 en 4 wordt allebei uitgegaan van profielen zonder huidige events en wordt in
eerste instantie alleen de meest verkochte producten per categoriepagina getoond. En wordt dus
gebruik gemaakt van het simple algoritme.

||---------------------------------- Verzameling 3 en 5 ---------------------------------------||
Bij verzamelingen 3 en 5 zijn er huidige klik events van een gebruiker en wordt op basis daarvan
bepaald wat het gender kenmerk is van de user. Dit in combinatie met de categoriepagina zorgt
voor de recommendations waarbij gebruik wordt gemaakt van de gender_category based filter tabel.

=================================================================================================
Voor elke verzameling wordt gekeken of de recommendations die gegeven worden overeenkomen met
de verwachte recommendations die we zouden moeten krijgen met de meegegeven input.
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
    cases = [
        (("5a97a846af47360001d62ee2", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("5a3a41d7ed29590001045639", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("5a3a41e9a825610001bc4373", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("5a3a4204ed2959000104566c", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("5a97a846af47360001d62ee2", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"]),
        (("5a3a41d7ed29590001045639", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"]),
        (("5a3a41e9a825610001bc4373", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"]),
        (("5a3a4204ed2959000104566c", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"]),
        (("a", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("b", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("c", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("d", "gezond & verzorging", []), ["1475", "151616", "152264", "1541"]),
        (("e", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"]),
        (("f", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"]),
        (("g", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"]),
        (("h", "wonen & vrije tijd", []), ["42678", "42679", "42684", "42694-blauw"])
    ]
    for case in cases:
        prodids = return_recommended_products(case[0][0], case[0][1], case[0][2])
        assert prodids == case[1], f"De input {case[0]} geeft de verkeerde output {prodids}. Verwachte output is {case[1]}"

def test_verzameling3_5():
    cases_gender_verzameling1 = [
        (("5a97a846af47360001d62ee2", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("5a3a41d7ed29590001045639", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("5a3a41e9a825610001bc4373", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("5a3a4204ed2959000104566c", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("5a97a846af47360001d62ee2", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"]),
        (("5a3a41d7ed29590001045639", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"]),
        (("5a3a41e9a825610001bc4373", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"]),
        (("5a3a4204ed2959000104566c", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"]),
        (("a", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("b", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("c", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("d", "gezond & verzorging", ['9196', '7149', '33298', '29438']), ["1475", "151616", "152264", "1542"]),
        (("e", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"]),
        (("f", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"]),
        (("g", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"]),
        (("h", "wonen & vrije tijd", ['9196', '7149', '33298', '29438']), ["44436", "44649", "44650", "45202"])
    ]
    cases_gender_verzameling2 = [
        (("5a97a846af47360001d62ee2", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("5a3a41d7ed29590001045639", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("5a3a41e9a825610001bc4373", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("5a3a4204ed2959000104566c", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("5a97a846af47360001d62ee2", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"]),
        (("5a3a41d7ed29590001045639", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"]),
        (("5a3a41e9a825610001bc4373", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"]),
        (("5a3a4204ed2959000104566c", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"]),
        (("a", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("b", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("c", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("d", "gezond & verzorging", ['9196', '33298', '6910', '29438']), ["16791", "1680", "16800", "1681"]),
        (("e", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"]),
        (("f", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"]),
        (("g", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"]),
        (("h", "wonen & vrije tijd", ['9196', '33298', '6910', '29438']), ["35936", "40147", "40152", "40153"])
    ]
    cases_gender_verzameling3 = [
        (("5a97a846af47360001d62ee2", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("5a3a41d7ed29590001045639", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("5a3a41e9a825610001bc4373", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("5a3a4204ed2959000104566c", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("5a97a846af47360001d62ee2", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("5a3a41d7ed29590001045639", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("5a3a41e9a825610001bc4373", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("5a3a4204ed2959000104566c", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("a", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("b", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("c", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("d", "gezond & verzorging", ['9196', '33298', '29438', '22309']), ["33070", "33086", "33122", "33191"]),
        (("e", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("f", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("g", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"]),
        (("h", "wonen & vrije tijd", ['9196', '33298', '29438', '22309']), ["38597", "38610", "38678", "38678-lathyrus"])
    ]
    for case in cases_gender_verzameling1:
        prodids = return_recommended_products(case[0][0], case[0][1], case[0][2])
        assert prodids == case[1], f"De input {case[0]} bij gender verzameling 1, geeft de verkeerde output {prodids}. Verwachte output is {case[1]}"
    for case in cases_gender_verzameling2:
        prodids = return_recommended_products(case[0][0], case[0][1], case[0][2])
        assert prodids == case[1], f"De input {case[0]} bij gender verzameling 2, geeft de verkeerde output {prodids}. Verwachte output is {case[1]}"
    for case in cases_gender_verzameling3:
        prodids = return_recommended_products(case[0][0], case[0][1], case[0][2])
        assert prodids == case[1], f"De input {case[0]} bij gender verzameling 3, geeft de verkeerde output {prodids}. Verwachte output is {case[1]}"


def main():
    try:
        test_verplichte_steekproef()
        print("Verplichte steekproef CHECK!")

        test_verzameling1()
        print("Steekproef met verzameling 1 CHECK!")

        test_verzameling2_4()
        print("Steekproef met verzameling 2 en 4CHECK!")

        test_verzameling3_5()
        print("Steekproef met verzameling 3 en 5 CHECK!")
    except AssertionError as ae:
        print(ae)

if __name__ == "__main__":
    main()