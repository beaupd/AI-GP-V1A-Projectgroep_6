# studentnr.: 1778287
import psycopg2

def conrdb():
    try:
        connectionRDB = psycopg2.connect(
            user='postgres',
            password='!qAz@wSx#4%620',
            host='localhost',
            database='DocumentStore'
        )
        cursor = connectionRDB.cursor()
        return connectionRDB, cursor
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)