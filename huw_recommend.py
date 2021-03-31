from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from rdbconnection2 import conrdb
from collections import Counter
import ast
import personalrecommendation as personalrec
from pactum import Pactum

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

def HighestFrequency(lijst):
    """
    Geeft het element met de hoogste frequentie in de lijst terug.
    """
    freq = Counter(lijst)
    return freq.most_common(1)[0][0]

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

    def get(self, profileid, count, type_rec, shopping_list, pagecat):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. 
        
        :param type_rec: str : is één van de keys uit 'recommendationtypes' huw.py
        :param shopping_list: str: str met daarin de boodschappenlijst """
        
        if type_rec == "popular":
            pagecat = ast.literal_eval(pagecat)
            cat = pagecat[0].replace("-", " ")
            cat = cat.replace(" en ", " & ")
            cat = cat.replace("make up", "make-up")
            user_segment_query = """select lower(segment) from profile where profile_id=%s"""
            user_segment = ReturnSelectExecution(user_segment_query, (profileid,))
            user_gender_query = """
            select array(select ARRAY[lower(gender), count(*)::varchar] from product
                         natural join(select product_id from orders
                         natural join(select session_id, segment from sessions
                         natural join(select * from buids
                         natural join profile
                         where profile_id=%s) as _id) as __id) as ___id
                         group by lower(gender)
                         order by lower(gender));
            """
            user_gender_freq_list = ReturnSelectExecution(user_gender_query, (profileid,))
            highest_freq = 0
            user_gender = ''
            for gender_freq in user_gender_freq_list:
                freq = int(gender_freq[1])
                if freq > highest_freq:
                    highest_freq = freq
                    user_gender = gender_freq[0]
            
            popular_query = """
            select array[product_id1, product_id2, product_id3, product_id4] from popular
            where lower(segment)=%s
            and lower(gender)=%s
            and lower(category)=%s;
            """
            prodids = ReturnSelectExecution(popular_query, (user_segment, user_gender, cat,))
            
        elif type_rec == "similar":
            pact = Pactum(conrdb)
            prodids = [p[0] for p in pact.get_n_recommended(profileid, count)]

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
        else:
            randcursor = database.products.aggregate([{ '$sample': { 'size': count } }])
            prodids = list(map(lambda x: x['_id'], list(randcursor)))
        return prodids, 200


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:type_rec>/<string:shopping_list>/<string:pagecat>")