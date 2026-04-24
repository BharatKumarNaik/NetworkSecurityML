import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

import certifi
ca=certifi.where() # This is required to avoid SSL certificate errors when connecting to MongoDB Atlas
from pymongo.mongo_client import MongoClient
import pymongo

import pandas as pd
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def csv_to_json(self, csv_file_path: str) -> str:
        try:
            df = pd.read_csv(csv_file_path)
            df.reset_index(inplace=True, drop=True)
            json_data = df.to_json(orient='records')
            return json_data
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def insert_data_to_mongodb(self, json_data: str, db_name: str, collection):
        try:
            self.uri = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.cxcru7u.mongodb.net/?appName=Cluster0"
            # self.client = MongoClient(self.uri, tlsCAFile=ca)
            self.database=db_name
            self.collection = collection
            self.data = json.loads(json_data)
            self.mongo_client = pymongo.MongoClient(self.uri, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.data)
            return (len(self.data))
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
if __name__ == "__main__":
    try:
        FILE_PATH = "Network_Data/phisingData.csv"
        DATABSE_NAME = "NetworkDB"
        COLLECTION_NAME = "PhishingData"
        data_extractor = NetworkDataExtract()
        json_data = data_extractor.csv_to_json(FILE_PATH)
        print(json_data)
        no_of_records = data_extractor.insert_data_to_mongodb(json_data, DATABSE_NAME, COLLECTION_NAME)
        print(f"Number of records inserted: {no_of_records}")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e