from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split


from dotenv import load_dotenv
load_dotenv()
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB_URL = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.cxcru7u.mongodb.net/?appName=Cluster0"

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    # To read data from MongoDB. 
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        try:
            databse_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_clinet = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_clinet[databse_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            # Dropping unnecessary columns and replacing "na" with NaN
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    # To avoid reading of data again and again from MongoDB, 
    # we will export the data into feature store in csv format and read from there for further processing 
    def export_data_into_feature_store(self, df: pd.DataFrame):
        try:
            feature_store_path = os.path.dirname(self.data_ingestion_config.feature_store_path)
            os.makedirs(feature_store_path, exist_ok=True)
            df.to_csv(self.data_ingestion_config.feature_store_path, index=False)
            logging.info(f"Exporting feature store to {self.data_ingestion_config.feature_store_path}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    # Train-Test split of the data and exporting into respective file paths.
    def split_Data_as_train_test(self,df: pd.DataFrame):
        try:
            train_set,test_set = train_test_split(df,test_size=0.2, random_state=43)
            logging.info(f"Train set and test set are splitted with test size 0.2")
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False,header=True)
            logging.info(f"Exporting train set to {self.data_ingestion_config.train_file_path}")
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False,header=True)
            logging.info(f"Exporting test set to {self.data_ingestion_config.test_file_path}")
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_data_ingestion(self):
        try:
            logging.info("Initiating data ingestion")
            df = self.export_collection_as_dataframe()
            df = self.export_data_into_feature_store(df)
            self.split_Data_as_train_test(df)
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e