import os
import sys
import pickle
import keras
from tensorflow.keras.utils import pad_sequences

from src.logger import logging
from src.utils.main_utils import load_object
from src.constants import *
from src.exception import USvisaException
from src.components.data_transformation import DataTransformation
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact, ModelTrainerArtifact, DataTransformationArtifact


class PredictionPipeline:
    def __init__(
        self,
        model_trainer_artifact: ModelTrainerArtifact,
        data_transformation_artifact: DataTransformationArtifact
    ):
        self.model_trainer_artifact = model_trainer_artifact
        self.data_transformation_artifact = data_transformation_artifact

        self.data_transformation = DataTransformation(
            data_transformation_config=DataTransformationConfig,
            data_ingestion_artifacts=DataIngestionArtifact
        )

    def predict(self, text: str) -> str:
        """
        Clean, tokenize, and predict sentiment.
        """
        logging.info("Running the predict method of PredictionPipeline class")
        try:
            # Load trained model
            model = load_object(self.model_trainer_artifact.trained_model_file_path)
            logging.info(f"Model loaded from: {self.model_trainer_artifact.trained_model_file_path}")

            # Load tokenizer
            tokenizer = load_object(self.data_transformation_artifact.transformed_object_file_path)
            logging.info(f"Tokenizer loaded from: {self.data_transformation_artifact.transformed_object_file_path}")

            # Clean and tokenize input text
            cleaned_text = self.data_transformation.concat_data_cleaning(text)
            sequence = tokenizer.texts_to_sequences([cleaned_text])
            padded = pad_sequences(sequence, maxlen=300)

            # Get prediction
            prediction_score = model.predict(padded)[0][0]
            logging.info(f"Prediction score: {prediction_score}")

            return "Positive" if prediction_score == 0 else "Negative"

        except Exception as e:
            raise USvisaException(e, sys) from e

    def run_pipeline(self, text: str) -> str:
        """
        Run the full prediction pipeline.
        """
        logging.info("Entered run_pipeline method of PredictionPipeline class")
        try:
            result = self.predict(text)
            logging.info("Exited run_pipeline method of PredictionPipeline class")
            return result
        except Exception as e:
            raise USvisaException(e, sys) from e
