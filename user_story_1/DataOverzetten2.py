# studentnr.: 1778287
from mdbconnection2 import conmdb
from rdbconnection2 import conrdb
from time import perf_counter

mdbcur = conmdb()
rdbcon, rdbcur = conrdb()

def get_subvalue(dictio, *keys):
    return [dictio[key] for key in keys[0] if key in dictio]

def products():
    for element in mdbcur["products"].find():
        temp =[
            element[key]
            if not isinstance(element[key], dict) # ervan uitgaande dat er maar één dict in voorkomt
            else get_subvalue(element[key], None) # neem de values van de sub_keys
            for key in [
                "_id", 
                "name", 
                "brand", 
                "gender", 
                "category", 
                "sub_category", 
                "sub_sub_category"]
            if key in element # Doe bovenstaande als de key bestaat in het document
        ]
        while len(temp) <= 6:
            temp.append(None)
        product_query = "INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s)"
        rdbcur.execute(product_query, temp)
        rdbcon.commit()

def profiels():
    profile_var = []
    buids_var = []
    for element in mdbcur["profiles"].find():
        temp = [
            element[key]
            if not isinstance(element[key], dict) # ervan uitgaande dat er maar één dict in voorkomt
            else get_subvalue(element[key], ["segment", "viewed_before"]) # neem de values van de sub_keys
            for key in [
                "_id",
                "buids",
                "recommendations",
                "previously_recommended"]
            if key in element # Doe bovenstaande als de key bestaat in het document
        ]
        try:
            profile_var.append([str(temp[0]), temp[2][1], temp[3], temp[2][0]])
            for browserid in temp[1]:
                buids_var.append([browserid, str(temp[0])])
        except IndexError:
            pass
    profile_query = "INSERT INTO profile VALUES (%s, %s, %s, %s)"
    rdbcur.executemany(profile_query, profile_var)
    rdbcon.commit()
    buids_query = "INSERT INTO buids VALUES (%s, %s) ON CONFLICT (browser_id) DO NOTHING"
    rdbcur.executemany(buids_query, buids_var)
    rdbcon.commit()

def sessions():
    limit = 100000
    skip = 0
    time = 0
    for i in range(0, 34):
        begin_ses_ev_or = perf_counter()

        sessions_var = []
        events_var = []
        orders_var = []
        for element in mdbcur["sessions"].find().skip(skip).limit(limit):
            temp =[
                element[key]
                if not isinstance(element[key], dict) # ervan uitgaande dat er maar één dict in voorkomt
                else get_subvalue(element[key], ["products"]) # neem de values van de sub_keys
                for key in [
                    "_id", 
                    "buid", 
                    "events", 
                    "order"]
                if key in element # Doe bovenstaande als de key bestaat in het document
            ]
            try:
                if temp[3] is not None:
                    if temp[3][0] is not None:
                        for product in temp[3][0]:
                            orders_var.append([product["id"], temp[0], temp[0], product["id"]])
                sessions_var.extend([[temp[1][0], temp[0], temp[1][0]] if not isinstance(temp[1][0], list) else [temp[1][0][0], temp[0], temp[1][0][0]]])
                events_var.extend([
                    [event["product"], temp[0], event["product"], temp[0]]
                    if " " not in event["product"]
                    else [event["product"].split(" ")[0], temp[0], event["product"].split(" ")[0], temp[0]]
                    for event in temp[2]
                    if "product" in event and event["product"] is not None
                ])
            except IndexError:
                pass
            
        events_var = [event for event in events_var if event]

        sessions_query = "DO $$ BEGIN IF (SELECT EXISTS (SELECT browser_id FROM buids WHERE browser_id=%s)::int) THEN INSERT INTO sessions VALUES (%s, %s); END IF; END $$;"
        orders_query = "DO $$ BEGIN	IF (SELECT EXISTS (SELECT product_id FROM product WHERE product_id=%s)::int) THEN IF(SELECT EXISTS (SELECT session_id FROM sessions WHERE session_id=%s)::int) THEN INSERT INTO orders VALUES (%s, %s); END IF; END IF; END $$;"
        events_query = "DO $$ BEGIN IF (SELECT EXISTS (SELECT product_id FROM product WHERE product_id=%s)::int) THEN IF(SELECT EXISTS (SELECT session_id FROM sessions WHERE session_id=%s)::int) THEN INSERT INTO events VALUES (%s, %s); END IF; END IF; END $$;"

        rdbcur.executemany(sessions_query, sessions_var)
        rdbcon.commit()
        rdbcur.executemany(orders_query, orders_var)
        rdbcon.commit()
        rdbcur.executemany(events_query, events_var)
        rdbcon.commit()


        skip += limit
        eind_ses_ev_or = perf_counter()
        time = time + (eind_ses_ev_or - begin_ses_ev_or)
        print(f"Approximately {skip} documents have been handled in {time} second(s).")


start_product = perf_counter()
products()
eind_product = perf_counter()
print(f"Insertion of products took {eind_product - start_product} second(s).")
start_profiles = perf_counter()
profiles()
eind_profiles = perf_counter()
print(f"Insertion of profiles en buids took {eind_profiles - start_profiles} second(s).")
start_sessions = perf_counter()
sessions()
eind_sessions = perf_counter()
print(f"Insertion of sessions, events and orders took {eind_sessions - start_sessions} second(s).")

rdbcur.close()
rdbcon.close()