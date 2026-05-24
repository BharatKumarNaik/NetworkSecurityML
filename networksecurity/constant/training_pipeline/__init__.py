import os
import sys
import numpy as np
import pandas as pd

# Common constants variables for the project
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurityPipeline"
ARTIFACT_DIR: str = "artifact"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"    
DATA_INGESTION_FEATURE_STORE_FILENAME:str = "raw_data.csv"

# Data Ingestion related constant variables
DATA_INGESTION_COLLECTION_NAME: str = "PhishingData"
DATA_INGESTION_DATABASE_NAME: str = "NetworkDB"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2

# Data Validation related constant variables
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str= "invalid"
DATA_VALLIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")


# Data Transformation related constant variables
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessor.pkl"

# Used for knn imputer class to replace nan values
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform",
}


# Model Trainer related constants
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float = 0.05
SAVED_MODEL_DIR:str =os.path.join("saved_model")
MODEL_FILE_NAME:str = "model.pkl"