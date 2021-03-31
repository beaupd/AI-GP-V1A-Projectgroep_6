# User story 4: Popular recommendation

Anderen kochten ook

Op de productoage van het front-end staat een kopje: 'Anderen kochten ook'. Hier worden de producten geplaatst van profielen die hetzelfde koopgedrag als de user vertonen, 
in dezelfde geslachtscategorie zitten als de gebruiker en passen bij de categorie van de pagina.

| _GP-V1A-Groep6_
| --- |
| TAAI-V1GP-19_2020 |
| TICT-AI-V1A |
| 1778287 |

# Onderbouwing algoritme

Omdat de aanbevelingen zijn gebaseerd op eerdere aankopen van andere mensen, wordt gekeken naar mensen die eerder orders hebben gedaan.

![](src/VennDiagram.png)

Het **U**niversum van het Venn-diagram hierboven bestaat uit klanten. Deze verzameling klanten kan **B**ekend zijn of (B̅) niet bekend zijn. 
Van alle profielen van bekende klanten, heeft een groep **E**vents. Daarnaast heeft een groep mensen met Events ook **O**rders. 
Voor elk **S**egment binnen deze verzameling wordt vervolgens gekeken naar de producten die door deze groep profielen zijn gekocht. 
Vervolgens wordt gekeken naar de verschillende **G**enders binnen ’n verzameling segment x waardoor de combinatie segment-gender ontstaat voor elke mogelijke gender binnen de verzameling van segment x. 
En om met elke **C**ategorie product pagina verschillende producten te tonen, verdelen we de verzameling van producten in segment x, gender y op categorieën. 

## Huidige user behoort tot B̅
/

## Huidige user behoort tot B

Deze groep kan vervolgens verder worden onderverdeeld. Welke mensen vertonen hetzelfde koopgedrag als de user? Hiervoor wordt gekeken naar het segment dat bij een profiel hoort. 
Voor elke verzameling profielen bij ‘n segment geldt: _segment_ is een subset van _O_. Wat voor segmenten zijn er, en hoe vaak komen profielen met een bepaald segment voor?

```sql
select lower(segment), count(segment) as frequency
from profile
group by lower(segment)
order by lower(segment);
```

![](src/segmentfreq.png)

Als we hier zouden stoppen, dan zouden mensen die alleen vrouwelijke producten kopen ook mannelijke producten (of andersom, etc.) aangeboden krijgen.
Daarom wordt voor alle aankopen van de profielen bij 'n segment x gekeken naar 'n gender y.
Dus als we nu gaan kijken voor 'n segment: browser wat de distributie is van genders binnen de verzameling orders van dit segment dan krijgen we het volgende:


```sql
select lower(gender) as gender, count(*) as frequency from product
natural join(select product_id from orders
natural join(select * from sessions
natural join(select browser_id from buids
natural join profile where lower(segment)='browser')
as _id) as __id) as ___id
group by lower(gender)
order by lower(gender);
```

![](src/genderfreq.png)

Als we nu gaan kijken naar de frequencies van producten voor elke mogelijke combinatie van gender-category binnen de verzameling orders van profielen met het segment browser,
krijgen we de volgende uitkomst:

```sql
select lower(gender) as gender, lower(category) as category, count(*) as frequency from product
natural join(select product_id from orders
natural join(select * from sessions
natural join(select browser_id from buids
natural join profile where lower(segment)='browser')
as _id) as __id) as ___id
group by lower(gender), lower(category)
order by lower(gender), lower(category);
```

![](src/gendercatfreq.png)

Hierboven is de tabel getoond met de eerste 29 rijen van de in totaal 70 rijen. 
Hier kun je zien dat elke verzameling van producten voor 'n segment browser met gender x alle producten zijn onderverdeeld in categorieën die voorkomen binnen de verzameling producten.
Dan zie je ook dat verzamelingen als grootverpakking minder combinaties hebben. Blijkbaar komen binnen de verzameling van grootverpakking slechts twee categorieën voor.

Ook zien we dat sommige combinaties, niet voorkomen of maar 1 product bevatten zoals; gender: gezin, category: kleding & sieraden. Dit betekent dat bij een user met
het gedrag van een browser, gender kenmerk grootverpakking op de pagina van kleding & sieraden, maar 1 product krijgt aangeraden. Of soms geen enkel product als de category niet voorkomt
in de gekochte producten.

# Nuttigheid

Door het sorteren op segment kenmerk, gender kenmerk en vervolgens per categoriepagina
zou je kunnen zeggen dat mensen die dezelfde kenmerken als een user hadden statistisch gezien grotendeels hetzelfde gedrag zullen vertonen als de gebruiker. 
Neem bijvoorbeeld segment: browser en het gender kenmerk baby. Dan is de kans heel groot dat ze naar de categorie pagina van baby & kind kijken
waar ook de meeste producten van zijn gekocht. En dus volgt dan indirect dat ze minder of vrijwel niet naar de pagina gezond & verzorging zullen kijken 
en dat het tonen van minder recommendations voor die pagina daarom gerechtvaardigd is.

# Pseudocode

```python
Creëer tabel popular als deze nog niet bestond met de kolommen segment, gender, category, FK product_id1, FK product_id2, FK product_id3, FK product_id4, FK product_id5.
   Voor elk _segment in lijst met segments loop:
	     Stop alle mogelijke gender-category combinaties binnen de 	verzameling met producten, de orders van profielen met segment _segment in een lijst seg.
	     Voor elke _gender_category combinatie in seg loop:
		       Stop de eerste vijf producten binnen de verzameling producten uit de orders van profielen met segment _segment, die voldoen aan de _gender_category combinatie in een lijst prodids.
		
		       Voeg achtereenvolgens de volgende delen in de tabel in: segment, gender, category, prodids[0], prodids[1], prodids[2], prodids[3], prodids[4]

```

# Relations

_Product_ -- _Popular_

Een product kan bij **0 of 1** rij horen van popular.

Een rij van popular hoort bij **meerdere** producten.

# Logistiek Datamodel

![](src/ERD_product_popular.png)

# DDL

Hieronder volgt de query die wordt uitgevoerd in createRelationTables.py om de relatie tussen de tabel popular en product te maken.

```
DO $$
DECLARE
    _segment VARCHAR;
    i INT;
    index INT;
    r RECORD;
    clean_list VARCHAR[];
    _combi VARCHAR[];
    prod_freq_list VARCHAR[];
    prod_freq VARCHAR[];
    temp VARCHAR[];
    temp2 INT[];
    temp3 INT[];
BEGIN
    -- [ MAAK DE TABEL AAN OF UPDATE DE TABEL ]
    DROP TABLE IF EXISTS popular CASCADE;
    CREATE TABLE popular (
        segment VARCHAR(255),
        gender VARCHAR(255),
        category VARCHAR(255),
        product_id1 VARCHAR(255),
        product_id2 VARCHAR(255),
        product_id3 VARCHAR(255),
        product_id4 VARCHAR(255),
        FOREIGN KEY (product_id1)
                REFERENCES product (product_id),
        FOREIGN KEY (product_id2)
                REFERENCES product (product_id),
        FOREIGN KEY (product_id3)
                REFERENCES product (product_id),
        FOREIGN KEY (product_id4)
                REFERENCES product (product_id)
    );
    -- [ VUL DE TABEL ]
    ------------------------- || Voor elk segment bestaande binnen profielen
    foreach _segment in ARRAY(select array(select lower(segment) as segment
                                from profile
                                group by lower(segment)
                                order by lower(segment))) loop
        ------------------------ || Groepeer elke mogelijk combinatie gender-categorie van producten
        ------------------------ || gekocht door profielen met het segment _segment
        foreach _combi slice 1 in ARRAY(select array(select array[lower(gender), lower(category)] from product
                                        natural join(select product_id from orders
                                        natural join(select * from sessions
                                        natural join(select browser_id from buids
                                        natural join profile where lower(segment)=_segment)
                                        as _id) as __id) as ___id
                                        group by lower(gender), lower(category)
                                        order by lower(gender), lower(category))) loop
            if _combi[1] is not Null and _combi[2] is not Null then -- || Als zowel het gender als de categorie niet Null zijn
                ----------------------- || Neem dan de producten
                prod_freq_list := array(select ARRAY[product_id, count(*)::varchar] from product
                                        natural join(select product_id from orders
                                        natural join(select * from sessions
                                        natural join(select browser_id from buids
                                        natural join profile where lower(segment)=_segment)
                                        as _id) as __id) as ___id
                                        where lower(gender)=_combi[1] and lower(category)=_combi[2]
                                        group by product_id
                                        order by product_id);
            else -- || Als het gender Null is en de categorie niet
                if _combi[1] is Null and _combi[2] is not Null then
                    prod_freq_list := array(select ARRAY[product_id, count(*)::varchar] from product
                                        natural join(select product_id from orders
                                        natural join(select * from sessions
                                        natural join(select browser_id from buids
                                        natural join profile where lower(segment)=_segment)
                                        as _id) as __id) as ___id
                                        where lower(gender) is Null and lower(category)=_combi[2]
                                        group by product_id
                                        order by product_id);
                else -- || Categorie Null bestaat niet op de front-end en is dus overbodig voor de tabel
                    continue;
                end if;
            end if;
            temp := ARRAY[Null];
            temp2 := ARRAY[Null];
            foreach prod_freq slice 1 in array(prod_freq_list) loop
                    temp = array_append(temp, prod_freq[1]);
                    temp2 = array_append(temp2, prod_freq[2]::int);
            end loop;
            temp3 = ARRAY(select distinct unnest(temp2) order by 1);
            if array_length(temp3, 1) > 1 then
                for i in 1..4 loop
                    for r in select max(x) as f from unnest(temp2) as x loop
                            index = array_position(temp2, r.f);
                            clean_list[i] = temp[index];
                            temp = array_remove(temp, temp[index]);
                    end loop;
                end loop;
                if clean_list[1] is not Null then
                    INSERT INTO popular VALUES (_segment, _combi[1], _combi[2], clean_list[1], clean_list[2], clean_list[3], clean_list[4]);
                else
                    continue;
                end if;
            end if;
        end loop;
    end loop;
END $$;
```

# Tabel Popular

![](src/popular_table.PNG)

# Hoe werkt de recommendation?

![](src/FLOWCHART_userPop.png)

