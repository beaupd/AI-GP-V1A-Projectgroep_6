from flask import Flask, request, session, render_template, redirect, url_for, g
from flask_restful import Api, Resource, reqparse
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from rdbconnection2 import conrdb
from collections import Counter
import ast

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

    def get(self, profileid, count, type_rec, pagecat):
        """ This function represents the handler for GET requests coming in
        through the API. It currently returns a random sample of products. 
        
        :param type_rec: str : is één van de keys uit 'recommendationtypes' huw.py
        :param shopping_list: str: str met daarin de boodschappenlijst """
        
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
        else:
            randcursor = database.products.aggregate([{ '$sample': { 'size': count } }])
            prodids = list(map(lambda x: x['_id'], list(randcursor)))
        return prodids, 200

# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below.
api.add_resource(Recom, "/<string:profileid>/<int:count>/<string:type_rec>/<string:pagecat>")
