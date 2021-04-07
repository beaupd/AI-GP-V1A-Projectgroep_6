"""
 ________________________________________________________________________________________________
(________________________ TEST OMSCHRIJVING VOOR VALIDATIE ALGORITME ____________________________)
Er zijn 5 mogelijke users:
1. User is bekend en heeft eerdere orders
2. User is bekend en heeft geen eerdere orders en geen huidige klik events
3. User is bekend en heeft geen eerdere orders en wel huisige klik events
4. User is onbekend en heeft geen huidige klik events
5. User is onbekend en heeft wel huidige klik events

Voor elke verzameling soorten users zijn 12 profielen aangesteld.
Daarnaast wordt er gekeken voor elk profiel naar 
de categoriepagina's: gezond & verzorging, op=opruiming, wonen & vrije tijd en make-up & geuren.
Verder wordt gebruik gemaakt van drie mogelijke gender verhoudingen qua producten: (1) man:2, 
vrouw:1, unisex:1, (2) man:1, vrouw:2, unisex:1 en (3) man:1, vrouw:1, unisex: 2. 
Deze dienen als de huidige klik events.

Hierdoor ontstaat straks de volgende test:
Voor elke verzameling in mogelijke_users loop
    Voor elke profiel in verzameling loop
        Voor elke categorie in verzameling categorieën loop
            Voor elke verzameling producten (1/2/3) loop
                Vraag om recommendations op basis van het profiel, categorie en verzameling producten
                Als verzameling 1 dan
                    select segment profiel
                    select meestvoorkomende gender van producten van eerdere orders
                    select productid's die horen bij deze recommendation
                    Als productid's overeenkomen met de recommendations, 1
                    Anders 0
                Als verzameling 2 of 3 dan
                    select productid's die horen bij simple recommendation met category categorie
                    Als productid's overeenkomen met de recommendations, 1
                    Anders 0
                Als verzameling 3 of 5 dan
                    select meestvoorkomende gender van producten in verzameling producten (1/2/3)
                    select productid's die horen bij dit gender en de categorie uit gender_category
                    Als productid's overeenkomen met de recommendations, 1
                    Anders 0

"""