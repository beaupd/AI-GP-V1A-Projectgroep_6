from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from rdbconnection2 import conrdb
from collections import Counter
import ast
import personalrecommendation as personalrec
import pactum as pactum
import popular_return_recoms as popularrec


app = Flask(__name__)
api = Api(app)

# We define these variables to (optionally) connect to an external MongoDB
# instance.
envvals = ["MONGODBUSER","MONGODBPASSWORD","MONGODBSERVER"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

# Since we are asked to pass a class rather than an instance of the class to the
# add_resource method, we open the connection to the database outside of the 
# Recom class.
load_dotenv()
if os.getenv(envvals[0]) is not None:
    envvals = list(map(lambda x: str(os.getenv(x)), envvals))
    client = MongoClient(dbstring.format(*envvals))
else:
    client = MongoClient()
database = client.huwebshop 

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

class Recom(Resource):
    """ This class represents the REST API that provides the recommendations for
    the webshop. At the moment, the API simply returns a random set of products
    to recommend."""

    def get(self, profileid, count, type_rec, shopping_list, pagecat, huidige_klik_events, productid):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. 
        
        :param type_rec: str : is één van de keys uit 'recommendationtypes' huw.py
        :param shopping_list: str: str met daarin de boodschappenlijst """
        
        if type_rec == "popular":
            pagecat = ast.literal_eval(pagecat)
            cat = pagecat[0].replace("-", " ")
            cat = cat.replace(" en ", " & ")
            cat = cat.replace("make up", "make-up")
            huidige_klik_events = ast.literal_eval(huidige_klik_events)
            
            prodids = popularrec.return_recommended_products(profileid, cat, huidige_klik_events)
            prodids = [niet_leeg_element for niet_leeg_element in prodids if niet_leeg_element]
            
        elif type_rec == "similar":
            pact = pactum.Pactum(personalrec.rdbcon)
            products = pact.get_n_recommended(productid, count)
            if products:
                prodids = [p[0] for p in products]
            else:
                prodids = [] # todo alternative/fallback
        
        elif type_rec == "combination":
            mogelijke_genders = ['Man', 'Vrouw']
            hoeveelheid_man = 0
            hoeveelheid_vrouw = 0
            gender_count_list = [hoeveelheid_man, hoeveelheid_vrouw]
            prod_man_list = []
            prod_vrouw_list = []
            bruikbare_producten = []
            prodids = []
            shopping_list = ast.literal_eval(shopping_list)
            for i in shopping_list:
                product_data = ReturnSelectExecution("""SELECT gender, sub_category from product Where product_id = %s""", [i[0]])
                if product_data in mogelijke_genders:
                    if product_data == 'Man':
                        hoeveelheid_man += 1
                        prod_man_list.append(i[0])
                    if product_data == 'Vrouw':
                        hoeveelheid_vrouw += 1
                        prod_vrouw_list.append(i[0])
            if hoeveelheid_vrouw > hoeveelheid_man:
                product = prod_vrouw_list[0]
            if hoeveelheid_man >= hoeveelheid_vrouw:
                product = prod_man_list[0]

            data_product = ReturnSelectExecution("SELECT array[gender, sub_category] from product Where product_id = %s", [product])
            gender = data_product[0]
            sub_category = data_product[1]
            index = mogelijke_genders.index(gender)
            for i in range(4):
                output = ReturnSelectExecution("SELECT product_id FROM product WHERE sub_category=%s AND gender=%s ORDER BY RANDOM() LIMIT 4", [sub_category, mogelijke_genders[index-1]])
                prodids.append(output)
        elif type_rec == "personal":
            prodids = personalrec.giveRecommendation(profileid)
        elif type_rec == "behaviour":
            rdbcon, rdbcur = conrdb()
            huidige_klik_events = ast.literal_eval(huidige_klik_events)
            fyp_list = [p for product in huidige_klik_events for p in pactum.Pactum(rdbcon).recommend_products(product)["products"]]
            prodids = [prod[0] for prod in Counter(fyp_list).most_common(4)]
        else:
            randcursor = database.products.aggregate([{ '$sample': { 'size': count } }])
            prodids = list(map(lambda x: x['_id'], list(randcursor)))
        return prodids, 200


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:type_rec>/<string:shopping_list>/<string:pagecat>/<string:huidige_klik_events>/<string:productid>")
