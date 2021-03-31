import interfaces as face
import data_insert as data_in
from time import perf_counter
from collections import Counter

class Pactum:

    def __init__(self, conn):
        self.conn = conn

    def recommend_products(self, product_id):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM equals WHERE '{product_id}'=ANY(products)") # kijken waar de gegeven product_id voorkomt in de array
        rows = cur.fetchall()
        if not rows:
            return None
        rows.sort(key = lambda rows: rows[-1]) # soorteren op groote array zodat we de kleinste kunnen pakken dit is meestal het meest overeenkomig qua eigenschappen.
        found_list = list(filter(lambda p: p != product_id, rows[0][2]))# lijst van alle gevonden producten met het gegeven product id eruit gefilterd
        res = {
            "length": len(found_list),
            "products": found_list,
            "occurences": Counter(found_list) # occurences van de items zodat je de products kan kiezen die met de meeste overeenkomen 
        }
        return res

    def populate_table(self):
        values = ["product_id", "brand", "category", "sub_category", "sub_sub_category"]
        cur = self.conn.cursor()
        cur.execute(f"SELECT {', '.join(values)} from product")
        rows = cur.fetchall()
        
        print(f"Found {len(rows)} rows, inserting...")
        start_all = perf_counter()
        for idx, r in enumerate(rows): # loop door alle opgevraagde rows
            for i, c in enumerate(r[1:], 1): # loop door alle columns behalve de eerste want het id gebruiken we in de niewe tabel als identificator
                if c:# als de column niet leeg is
                    p = str(c).replace("'", "") # sommige columns hebben quote er in en dat geeft een error
                    p_id = r[0].replace("'", "") # sommige columns hebben quote er in en dat geeft een error
                    # hieronder de sql insert code om een row aan te maken of van een row met dezelfde "value" de array aan te passen(append) 
                    cur.execute(f"INSERT INTO equals(keyfield, value, products, length) VALUES ('{values[i]}', '{p}', ARRAY['{p_id}'], 1) ON CONFLICT (value) DO UPDATE SET products = array_append((SELECT products from equals where value='{p}'), '{p_id}'), length = array_length(array_append((SELECT products from equals where value='{p}'), '{p_id}'), 1);")
            if idx % 1000 == 0 and idx != 0: # x aantal executes committen vooral om efficientie te testen en om een coole tussentijdse tijden te berekenen
                temp = perf_counter()
                print(f"On row {idx}, current time is {temp - start_all}s estimated time is {((temp-start_all)/idx)*len(rows)}s\ncommiting...")
                self.conn.commit()
        self.conn.commit()
        eind_whole = perf_counter()
        print(f"Done, total took {eind_whole - start_all} seconds...")
        cur.close()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS equals CASCADE")
        cur.execute("""
            CREATE TABLE equals (
                keyfield VARCHAR,
                value VARCHAR PRIMARY KEY,
                products VARCHAR[],
                length INT
            );
        """)
        self.conn.commit()
        cur.close()

with face.InterfaceDB() as conn:
    p = Pactum(conn)
    # p.create_table()
    # p.populate_table()
    print(p.recommend_products("01001-chalkwhite"))


# with face.InterfaceDB() as conn:
#     with face.InterfaceDDB() as DDBconn:
#         data_in.insertData(DDBconn, conn, data_in.config_products)


# createTableQuery = """
#     DROP TABLE IF EXISTS Profile CASCADE;
#     DROP TABLE IF EXISTS BUIDS CASCADE;
#     DROP TABLE IF EXISTS Sessions CASCADE;
#     DROP TABLE IF EXISTS Product CASCADE;
#     DROP TABLE IF EXISTS Orders CASCADE;
#     DROP TABLE IF EXISTS Events CASCADE;

#     CREATE TABLE Profile (
#     profile_id varchar(255) PRIMARY KEY,
#     previously_recommended varchar(255)[],
#     viewed_before varchar(255)[],
#     segment VARCHAR(50)
#     );
#     CREATE TABLE BUIDS (
#         browser_id varchar(255) PRIMARY KEY,
#         profile_id varchar(255),
#         FOREIGN KEY (profile_id)
#             REFERENCES Profile (profile_id)
#     );
#     CREATE TABLE Product (
#         product_id varchar(255) NOT NULL,
#         naam varchar(255),
#         brand varchar(255),
#         gender varchar(255),
#         category varchar(255),
#         sub_category varchar(255),
#         sub_sub_category varchar(255),
#         PRIMARY KEY (product_id) 
#     );
#     CREATE TABLE Sessions (
#         session_id varchar(255) PRIMARY KEY,
#         browser_id varchar(255),
#         FOREIGN KEY (browser_id)
#             REFERENCES BUIDS (browser_id)
#     );
#     CREATE TABLE Orders (
#         session_id varchar(255),
#         product_id varchar(255),
#         FOREIGN KEY (session_id)
#             REFERENCES Sessions (session_id),
#         FOREIGN KEY (product_id)
#             REFERENCES Product (product_id)
#     );
#     CREATE TABLE Events (
#         product_id varchar(255) NOT NULL,
#         session_id varchar(255) NOT NULL,
#         FOREIGN KEY (product_id)
#             REFERENCES Product (product_id),
#         FOREIGN KEY (session_id)
#             REFERENCES Sessions (session_id)
#     );
# """

# with face.InterfaceDB() as conn:
#     curr = conn.cursor()
#     curr.execute(createTableQuery) 
#     conn.commit()
#     curr.close()

    