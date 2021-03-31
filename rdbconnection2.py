# studentnr.: 1778287
import psycopg2

def conrdb():
    try:
        connectionRDB = psycopg2.connect(
            user='postgres',
            password='<Password>',
            host='localhost',
            database='postgres'
        )
        cursor = connectionRDB.cursor()
        return connectionRDB, cursor
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)