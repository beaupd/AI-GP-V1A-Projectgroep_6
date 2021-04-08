from time import perf_counter
from collections import Counter
from rdbconnection2 import conrdb

rdbcon, rdbcur = conrdb()

class Pactum:
    """
        De similar recommendation class ofwel pactum. Hierin zitten alle 
        functies die je nodig hebt om met een instance van de class
        similar recommendations te maken.
    """ 
    
    def __init__(self, conn):
        """
            De initiate functie deze word gecalled met een postgresql open connection
            deze variabele word aan de instance toegewezen met "self" en zo kan elke functie
            die self als parameter heeft de connectie gebruiken
        """
        self.conn = conn

    def get_n_recommended(self, product_id, n):
        """
            Deze functie returned met een gegeven product-id een n aantal recommendations
        """
        res = self.recommend_products(product_id) # vraag de response van de functie recommend_products deze returned een aantal lists in een dict
        products = res["occurences"].most_common(n) # pak n aantal recommendations van de opgetelde lijst van de recomend_products functie
        if products:
            return products
        else:
            return None

    def get_all(self, products):
        """
            (Deprecated)
            Deze functie zou met een gegeven lijst alle arrays opvragen waar 
            ze in voorkomen in de equals tabel. Deze functie werkt nog niet optimaal omdat
            tot mijn kennis was het niet mogelijk om het in een query statement te doen
            dus nu loopt de functie door de hele lijst wat erg onefficient is, 
            ik heb nog geen goeie oplossing kunnen bedenken. Deze functie was voor de foryoupage bedacht 
        """
        if len(products) > 0:
            cur = self.conn.cursor()
            query = ""
            for i, p in enumerate(products):
                if i == 0:
                    query = f"SELECT * FROM equals WHERE '{p}'=ANY(products)"
                elif i == len(products):
                    query += f"OR '{p}'=ANY(products);"
                else:
                    query += f"OR '{p}'=ANY(products)"
            cur.execute(query)
            rows = cur.fetchall()
            found_list = list(filter(lambda p: p not in products, [item for sublist in [c[2] for c in rows] for item in sublist]))# lijst van alle gevonden producten met het gegeven product id eruit gefilterd
            # products = found_list
            return found_list
        else:
            return None

    def setup_recommendation(self):
        """
            Call allebei de functies om de omgeving voor de pactum recommendation
            op te zetten, zodat er recommendations gemaakt kunnen worden
        """
        self.create_table()
        self.populate_table()

    def recommend_products(self, product_id):
        """
            Deze functie zoekt met een gegeven product-id op in welke arrays deze voorkomt in de equals tabel.
            Alle product-id's die in deze arrays voorkomen worden opgevraagd waardoor je een grote lijst gereturned krijgt.
            Het gegeven product-id word uit de lijst gefilterd en dan word er een response gereturned in de vorm van een dict,
            in deze dict zitten de lengte van de gevonden lijst, alle product-ids van de lijst, en alle product-ids opgeteld 
            en gesorteerd op frequente
        """
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
        """
            Deze functie vult aan de hand van een aantal column namen (variabele values) de equals tabel aan.
            In deze tabel staan alle product-id's die dezelfde waarde hebben bij een specificatie in een array.
            Op een row heb je een column de specificatie key met de waarde die de producten delen en een column 
            met een array van alle product-ids die die waarde delen.
        """
        values = ["product_id", "brand", "gender", "category", "sub_category", "sub_sub_category"] # De values van de columns
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
        """
            De functie om de equals tabel aan te maken.
        """
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
    # p.setup_recommendation()
    x = p.get_all_from_list(["01001-chalkwhite", "02045", "04001-chestnut"])
    y = p.recommend_products("02045")
    print(y)
