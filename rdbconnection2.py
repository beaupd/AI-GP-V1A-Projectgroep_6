# studentnr.: 1778287
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def conrdb():
    try:
        connectionRDB = psycopg2.connect(
            user='postgres',
            password='Nguyen1996',
            password=os.getenv('RDB_PASS'),
            host='localhost',
            database='DocumentStore'
        )
        cursor = connectionRDB.cursor()
        return connectionRDB, cursor
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)