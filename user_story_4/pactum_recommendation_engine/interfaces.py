import psycopg2
from pymongo import MongoClient

class InterfaceDB:

    config = {
        "db": "documentStore",
        "user": "postgres",
        "password": "admin "
    }

    def __enter__(self, config=config):
        self.conn = psycopg2.connect(f"dbname={config['db']} user={config['user']} password={config['password']}")
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

class InterfaceDDB:
    
    config = {
        "ip": "127.0.0.1",
        "port": "27017"
    }

    def __enter__(self, config=config):
        self.client = MongoClient(f"mongodb://{config['ip']}:{config['port']}")
        self.db = self.client["DocumentStore"]
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()