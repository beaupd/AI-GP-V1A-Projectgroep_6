import pandas as pd
import time
from time import perf_counter
from io import BytesIO
import pandas as pd
from sqlalchemy import create_engine

config_products = {
    "collection": "products",   # Welke collection van mongodb (DATA IN)
    "keys": ["_id", "name", "brand", "gender", "category", "sub_category", "sub_sub_category"],   # Mongodb collection keys
    "sub_keys": [],
    "table": "product",    # Hoe heet de tabel in de relationele databasse
    "sep": ";",     # Door welk teken zijn de verschillende columns geseperate
    "columns": [
        {"id": 0, "key": "_id", "column": "product_id"},
        {"id": 1, "key": "name", "column": "name"},
        {"id": 2, "key": "brand", "column": "brand"},
        {"id": 3, "key": "gender", "column": "gender"},
        {"id": 4, "key": "category", "column": "category"},
        {"id": 5, "key": "sub_category", "column": "sub_category"},
        {"id": 6, "key": "sub_sub_category", "column": "sub_sub_category"}
    ] # De namen van de columns met de plaats en bijbehorende key
}

config_profile = {
    "collection": "visitors",   # Welke collection van mongodb (DATA IN)
    "keys": ["_id", "recommendations", "previously_recommended"],   # Mongodb collection keys
    "sub_keys": [
        { "key":"recommendations", "sub_keys": ["viewed_before", "segment"]}
        ],
    "table": "profile",    # Hoe heet de tabel in de relationele databasse
    "sep": ";",     # Door welk teken zijn de verschillende columns geseperate
    "columns": [
        {"id": 0, "key": "_id", "column": "profile_id"},
        {"id": 1, "key": "viewed_before", "column": "viewed_before"},
        {"id": 2, "key": "previously_recommended", "column": "previously_recommended"},
        {"id": 3, "key": "segment", "column": "segment"}
    ] # De namen van de columns met de plaats en bijbehorende key
}

buids_profile = {

}

def get_length(db, collection):
        return db[collection].find().count()

def get_dataframe(db, collection, query, limit, skip):
    data = db[collection].find({}, query).limit(limit)
    df = pd.DataFrame(list(data))
    return df

def insertData(ddbconn, conn, config, limit=200000):
    length = get_length(ddbconn, config["collection"])
    position = 0
    while length > 0:
        if length - limit > 0:
            length -= limit
            count = limit
        else:
            count = length
            length = 0
        curr = conn.cursor()
        start = perf_counter()
        print(f"Collecting dataframe from collection {config['collection']}")
        df = get_dataframe(ddbconn, config["collection"], {k : 1 for k in config["keys"]}, count, position)
        eind = perf_counter()
        print(f"Collected {count} dataframes position is {position} and {length} left, took {eind - start} second(s)")
        if len(config["sub_keys"]) > 0:
            print("dissecting sub keys from dictionary")
            for k in config["sub_keys"]:
                print(f"Dissection {k['key']} with subkey(s) {k['sub_keys']}")
                start = perf_counter()
                extra_df = df[k["key"]].apply(pd.Series)
                extra_clean_df = extra_df[k["sub_keys"]]
                df = df.drop(k["key"], axis=1)
                df = pd.concat([df, extra_clean_df], axis=1)
                eind = perf_counter()
                print(f"succesfully added subkeys to frame, took {eind - start} second(s)")
        else:
            df = df[config["keys"]] # remove not needed columns
        df.reset_index(drop=True) # remove row index
        # print(df.head())
        # print(df["previously_recommended"])
        # df['previously_recommended'] = df['previously_recommended'].apply(set)
        # print(df.head())
        memory_buffer = BytesIO()
        df.to_csv(memory_buffer, sep=config["sep"], header=False, index=False) # write panda series to csv format 
        memory_buffer.seek(0)
        
        print(f"Inserting into {config['table']}")
        start = perf_counter()
        curr.copy_from(memory_buffer, config["table"], config["sep"])
        conn.commit()
        curr.close()
        eind = perf_counter()
        print(f"Inserting {config['collection']} into {config['table']}  took {eind - start} second(s)")
        position += count
        time.sleep(0.1)