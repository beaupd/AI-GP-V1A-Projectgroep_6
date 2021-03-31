import interfaces as face
import data_insert as data_in

class Pactum:

    def __init__(self, conn):
        self.conn = conn

    def recommend_production(self, product_id):
        pass

    def populate_table(self):
        pass

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS equals CASCADE")
        cur.execute("""
            CREATE TABLE equals (
                keyfield VARCHAR,
                value VARCHAR PRIMARY KEY,
                products VARCHAR[],
                length INT
            );
        """)
        self.conn.commit()
        cur.close()

with face.InterfaceDB() as conn:
    with face.InterfaceDDB() as DDBconn:
        data_in.insertData(DDBconn, conn, data_in.config_profile)


# createTableQuery = """
#     DROP TABLE IF EXISTS Profile CASCADE;
#     DROP TABLE IF EXISTS BUIDS CASCADE;
#     DROP TABLE IF EXISTS Sessions CASCADE;
#     DROP TABLE IF EXISTS Product CASCADE;
#     DROP TABLE IF EXISTS Orders CASCADE;
#     DROP TABLE IF EXISTS Events CASCADE;

#     CREATE TABLE Profile (
#     profile_id varchar(255) PRIMARY KEY,
#     previously_recommended text[],
#     viewed_before text[],
#     segment VARCHAR(50)
#     );
#     CREATE TABLE BUIDS (
#         browser_id varchar(255) PRIMARY KEY,
#         profile_id varchar(255),
#         FOREIGN KEY (profile_id)
#             REFERENCES Profile (profile_id)
#     );
#     CREATE TABLE Product (
#         product_id varchar(255) NOT NULL,
#         naam varchar(255),
#         brand varchar(255),
#         gender varchar(255),
#         category varchar(255),
#         sub_category varchar(255),
#         sub_sub_category varchar(255),
#         PRIMARY KEY (product_id) 
#     );
#     CREATE TABLE Sessions (
#         session_id varchar(255) PRIMARY KEY,
#         browser_id varchar(255),
#         FOREIGN KEY (browser_id)
#             REFERENCES BUIDS (browser_id)
#     );
#     CREATE TABLE Orders (
#         session_id varchar(255),
#         product_id varchar(255),
#         FOREIGN KEY (session_id)
#             REFERENCES Sessions (session_id),
#         FOREIGN KEY (product_id)
#             REFERENCES Product (product_id)
#     );
#     CREATE TABLE Events (
#         product_id varchar(255) NOT NULL,
#         session_id varchar(255) NOT NULL,
#         FOREIGN KEY (product_id)
#             REFERENCES Product (product_id),
#         FOREIGN KEY (session_id)
#             REFERENCES Sessions (session_id)
#     );
# """

# with face.InterfaceDB() as conn:
#     curr = conn.cursor()
#     curr.execute(createTableQuery) 
#     conn.commit()
#     curr.close()

    