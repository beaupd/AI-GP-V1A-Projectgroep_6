# studentnr.: 1778763, 1778287, 1779750, 1789287
from rdbconnection2 import conrdb

rdbcon, rdbcur = conrdb()

createTableQuery = """
    DROP TABLE IF EXISTS Profile CASCADE;
    DROP TABLE IF EXISTS BUIDS CASCADE;
    DROP TABLE IF EXISTS Sessions CASCADE;
    DROP TABLE IF EXISTS Product CASCADE;
    DROP TABLE IF EXISTS Orders CASCADE;
    DROP TABLE IF EXISTS Events CASCADE;

    CREATE TABLE Profile (
    profile_id varchar(255) PRIMARY KEY,
    viewed_before VARCHAR(255)[],
    previously_recommended VARCHAR(255)[],
    segment VARCHAR(50)
    );
    CREATE TABLE BUIDS (
        browser_id varchar(255) PRIMARY KEY,
        profile_id varchar(255),
        FOREIGN KEY (profile_id)
            REFERENCES Profile (profile_id)
    );
    CREATE TABLE Product (
        product_id varchar(255) NOT NULL,
        naam varchar(255),
        brand varchar(255),
        gender varchar(255),
        category varchar(255),
        sub_category varchar(255),
        sub_sub_category varchar(255),
        PRIMARY KEY (product_id) 
    );
    CREATE TABLE Sessions (
        session_id varchar(255) PRIMARY KEY,
        browser_id varchar(255),
        FOREIGN KEY (browser_id)
            REFERENCES BUIDS (browser_id)
    );
    CREATE TABLE Orders (
        session_id varchar(255),
        product_id varchar(255),
        FOREIGN KEY (session_id)
            REFERENCES Sessions (session_id),
        FOREIGN KEY (product_id)
            REFERENCES Product (product_id)
    );
    CREATE TABLE Events (
        product_id varchar(255) NOT NULL,
        session_id varchar(255) NOT NULL,
        FOREIGN KEY (product_id)
            REFERENCES Product (product_id),
        FOREIGN KEY (session_id)
            REFERENCES Sessions (session_id)
    );
"""

rdbcur.execute(createTableQuery)
rdbcon.commit()
rdbcur.close()
rdbcon.close()