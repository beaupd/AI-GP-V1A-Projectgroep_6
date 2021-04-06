from rdbconnection2 import conrdb

rdbcon, rdbcur = conrdb()

query_popular_table = """
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
"""

query_meest_gekocht_table = """
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
"""

rdbcur.execute(query_popular_table)
rdbcur.execute(query_meest_gekocht_table)
rdbcon.commit()
rdbcur.close()
rdbcon.close()
