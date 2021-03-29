# User story 3: Simple Recommendation

Meest gekocht

| _GP-V1A-Groep6_
| --- |
| TAAI-V1GP-19_2020 |
| TICT-AI-V1A |
| 1778287 |

![]()

Als we de tabel van de **O**rders zouden zien als een verzameling, dan geldt het volgende:
Elke mogelijke verzameling **C**ategorie van producten met categorie x is een subset van alle orders.

## Categorieën binnen de tabel orders

```sql
select category, count(*) from product
natural join orders as _id
group by category
order by category;
```

![]()

Bij het kijken naar de distributie van voorkomende categorieën in de verzameling orders valt op dat niet van elke mogelijke categorie producten zijn gekocht. 
Dit houdt in dat bij het opvragen, later, van producten bij een productpage waar geen producten van zijn gekocht, geen recommendations getoond zullen worden.

## Tabel meest_gekocht

De relaties die ontstaan bij het maken van een tabel met een categorie en vier product_id's:

_Product - meest_gekocht_

Een product kan bij 0 of 1 categorie behoren.

Meest_gekocht hoort bij meer producten.


Hierbij hoort het volgende logistiek datamodel:

![]()

### DDL script voor meest_gekocht

```sql
DO $$
DECLARE
    cat VARCHAR;
    i INT;
    index INT;
    r RECORD;
    prod_cat VARCHAR[];
    prod_freq VARCHAR[];
    temp VARCHAR[];
    temp2 INT[];
    temp3 INT[];
    cleanList VARCHAR[];
BEGIN
    DROP TABLE IF EXISTS meest_gekocht CASCADE;
    CREATE TABLE meest_gekocht(
        category VARCHAR(255),
        product_id1 VARCHAR(255),
        product_id2 VARCHAR(255),
        product_id3 VARCHAR(255),
        product_id4 VARCHAR(255),
        FOREIGN KEY (product_id1)
                REFERENCES product(product_id),
        FOREIGN KEY (product_id2)
                REFERENCES product(product_id),
        FOREIGN KEY (product_id3)
                REFERENCES product(product_id),
        FOREIGN KEY (product_id4)
                REFERENCES product(product_id)
    );

    foreach cat in ARRAY array(select lower(category) from product
                        natural join orders as _id
                        group by lower(category)
                        order by lower(category)) loop
      temp := ARRAY[Null];
      temp2 := ARRAY[Null];
      if cat is not Null then
         prod_cat := array(select ARRAY[product_id, count(*)::varchar] from product
                                       natural join orders as _id
                                       where lower(category)=cat
                                       group by product_id
                                       order by product_id);
      else
         prod_cat := array(select ARRAY[product_id, count(*)::varchar] from product
                                       natural join orders as _id
                                       where lower(category) is Null
                                       group by product_id
                                       order by product_id);
      end if;
      if array_length(prod_cat, 1) >= 1 then
            foreach prod_freq slice 1 in ARRAY prod_cat loop
               temp = array_append(temp, prod_freq[1]);
               temp2 = array_append(temp2, prod_freq[2]::int);
            end loop;
         end if;
         temp3 = ARRAY(select distinct unnest(temp2) order by 1);
         if array_length(temp3, 1) > 1 then
            for i in 1..4 loop
               for r in select max(x) as f from unnest(temp2) as x loop
                  index = array_position(temp2, r.f);
                  cleanList[i] = temp[index];
                  temp = array_remove(temp, temp[index]);
               end loop;
            end loop;
            INSERT INTO meest_gekocht VALUES (cat, cleanList[1], cleanList[2], cleanList[3], cleanList[4]);
         else
            if temp[2] is not Null then
                  INSERT INTO meest_gekocht VALUES (cat, temp[2], temp[3], temp[4], temp[5]);
            end if;
         end if;
    end loop;
END $$;
```

### ERD en meest_gekocht tabel na het uitvoeren van DDL

![]()

Alle attributen (categorie, 4 FK's) zijn tot kolommen gemaakt.

![]()

## Verbinden van tabel met fron-end

De functie die recommendations vraagt van populaire producten heet:'productpage'. In het stuk

```python
...
if len(nononescats) > 1:
            pagepath = "/producten/"+("/".join(nononescats))+"/"
        else:
            pagepath = "/producten/"
        return self.renderpackettemplate('products.html', {'products': prodlist, \
            'productcount': prodcount, \
            'pstart': skipindex + 1, \
            'pend': skipindex + session['items_per_page'] if session['items_per_page'] > 0 else prodcount, \
            'prevpage': pagepath+str(page-1) if (page > 1) else False, \
            'nextpage': pagepath+str(page+1) if (session['items_per_page']*page < prodcount) else False, \
            'r_products':self.recommendations(4, list(self.recommendationtypes.keys())[0], [], nononescats), \
            'r_type':list(self.recommendationtypes.keys())[0],\
            'r_string':list(self.recommendationtypes.values())[0]\
            })
...
```

is te zien dat ‘nononescats’ bepaald op welke categorie (en sub_categorie) pagina de user zit. 
En bij ‘r_products’ wordt aangegeven hoeveel producten bij de recommendations moeten staan. 
Deze ‘recommendations’ functie roept de huw_recommend.py aan voor producten die teruggegeven moeten worden.
Als we willen weten op welke pagina we zitten om specifiek daarvoor recommendations te geven en wat voor type recommendation, 
moeten we deze informatie dus meegegeven in de vorm van parameters.

```python
...
'r_products':self.recommendations(4, list(self.recommendationtypes.keys())[0], nononescats)
...
```

Deze parameter wordt gegeven aan de functie ‘recommendations’ dus moeten hiervoor parameters aangemaakt worden en 
moeten de meegegeven argumenten vervolgens ook meegegeven worden aan huw_recommend.py

```python
...
def recommendations(self, count, type_rec, pagecat):
        resp = requests.get(self.recseraddress+"/"+session['profile_id']+"/"+str(count)+"/"+type_rec+"/"+ str(pagecat))
...
```

Om nu onderscheid te maken op recommendationtype en productpage moeten deze parameters ook worden verwerkt in ‘Recom().get()’. 

Voor het ophalen van de product_id’s behorende bij de categorie is een functie nodig:

```python
def ReturnSelectExecution(sql_query, query_var):
    """
    Voert een query uit, met de meegegeven variabelen.
    (Gaat uit van een 'SELECT' query waarbij data terug moet worden gehaald.)
    Geeft de geselecteerde waardes terug.
    """
    rdbcon, rdbcur = conrdb()
    rdbcur.execute(sql_query, query_var)
    returnvalue = []
    try:
        returnvalue = rdbcur.fetchone()[0]
        rdbcur.close()
        rdbcon.close()
    except TypeError:
        pass
    return returnvalue
```

Nu kunnen we na het schoonmaken van de category string de productid’s terughalen die horen bij de productpage.

```python
def get(self, profileid, count, type_rec, pagecat):        
        if type_rec == "popular":
            pagecat = ast.literal_eval(pagecat)
            cat = pagecat[0].replace("-", " ")
            cat = cat.replace(" en ", " & ")
            cat = cat.replace("make up", "make-up")
            popular_query = """
            select array[product_id1, product_id2, product_id3, product_id4] from meest_gekocht
            where category=%s;
            """
            prodids = ReturnSelectExecution(popular_query, (cat,))
```

Bij het draaien van de front-end en het klikken op Gezond & verzorging, krijg je onderstaande scherm. 
De producten die het meest zijn gekocht in deze categorie worden bij ‘Anderen kochten ook’ weergegeven.

![]()

### Huishouden

![]()

### Wonen & vrije tijd

![]()
