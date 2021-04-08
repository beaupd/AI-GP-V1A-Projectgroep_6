import psycopg2

con = psycopg2.connect(
    host='localhost',
    database='DocumentStore',
    user='postgres',
    password='Robinson1',
    port=5433
)

cur = con.cursor()


def gender_check():
    products_list = []
    mannen_producten = 0
    vrouwen_producten = 0
    for i in range(1000):
        query1 = "SELECT viewed_before FROM profile ORDER BY RANDOM() LIMIT 1;"
        cur.execute(query1)
        products = cur.fetchall()
        for p in products:
            for j in p:
                for product in j:
                    query2 = "SELECT gender from product where product_id = %s;"
                    cur.execute(query2, [product])
                    gender = cur.fetchall()
                    if gender[0][0] == 'Man':
                        mannen_producten += 1
                    if gender[0][0] == 'Vrouw':
                        vrouwen_producten += 1
    print(f"mannen producten bekeken: {mannen_producten}\nvrouwen producten bekeken: {vrouwen_producten}")
    cur.close()
    con.close()
    return


gender_check()