from time import perf_counter
from collections import Counter
from rdbconnection2 import conrdb

rdbcon, rdbcur = conrdb()

class Pactum:

    def __init__(self, conn):
        self.conn = conn

    def get_n_recommended(self, product_id, n):
        res = self.recommend_products(product_id)
        products = res["occurences"].most_common(n)
        if products:
            return products
        else:
            return None

    def setup_recommendation(self):
        self.create_table()
        self.populate_table()

    def recommend_products(self, product_id):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM equals WHERE '{product_id}'=ANY(products)") # kijken waar de gegeven product_id voorkomt in de array
        rows = cur.fetchall()
        if not rows:
            return None
        # print([item for sublist in [c[2] for c in rows] for item in sublist])
        # rows.sort(key = lambda rows: rows[-1]) # soorteren op groote array zodat we de kleinste kunnen pakken dit is meestal het meest overeenkomig qua eigenschappen.
        found_list = list(filter(lambda p: p != product_id, [item for sublist in [c[2] for c in rows] for item in sublist]))# lijst van alle gevonden producten met het gegeven product id eruit gefilterd
        res = {
            "length": len(found_list),
            "products": found_list,
            "occurences": Counter(found_list) # occurences van de items zodat je de products kan kiezen die met de meeste overeenkomen 
        }
        return res

    def populate_table(self):
        values = ["product_id", "brand", "gender", "category", "sub_category", "sub_sub_category"]
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

if __name__ == "__main__":
    p = Pactum(rdbcon)
    # p.create_table()
    # p.populate_table()
    # res = p.get_n_recommended("01001-jetblack", 3)
    # print(res)
    p.setup_recommendation()