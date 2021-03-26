# studentnr. : 1778287
from pymongo import MongoClient

def conmdb():
    try:
        myclient = MongoClient()
        db = myclient["huwebshop"]
        return db
    except pymongo.DatabaseError:
        print("Connection with mongodb failed")