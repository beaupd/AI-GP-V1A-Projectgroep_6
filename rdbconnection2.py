# studentnr.: 1778287
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conrdb():
    try:
        connectionRDB = psycopg2.connect(
            user='postgres',
            password=os.getenv('RDB_PASS'),
            host='localhost',
            database='DocumentStore',
            port=os.getenv('RDB_PORT')
        )
        cursor = connectionRDB.cursor()
        return connectionRDB, cursor
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)