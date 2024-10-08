import os

# Set the environment variable (if necessary)
os.environ['SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL'] = 'True'

# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pandas import DataFrame
from typing import List
import xgboost as xgb
import logging
import joblib
import pandas as pd
import sklearn # Ensure scikit-learn is installed
# Configure logging
logging.basicConfig(level=logging.INFO)

class PredictionRequest(BaseModel):
    depth_cm: float
    total_precipitation: float
    mean_temperature: float
    dem: float
    slope: float
    aspect: float
    hillshade: float
    bd_mean: float
    clay_mean: float
    om_mean: float
    ph_mean: float
    sand_mean: float
    land_use: int
    land_cover: int


class PredictionResponse(BaseModel):
    soil_organic_carbon: float
    soil_organic_carbon_stock: float


def transform_to_dataframe(requests: List[PredictionRequest]) -> DataFrame:
    """
    Transforms a list of PredictionRequest instances into a DataFrame.
    """
    # Convert the request data to a dictionary and then to a DataFrame
    dictionary = {key: [getattr(req, key) for req in requests] for key in requests[0].dict().keys()}
    df1 = DataFrame(dictionary)
    df = pd.get_dummies(df1, columns=['land_use', 'land_cover'])

    # Initialize all expected columns with 0 or False
    expected_columns = [
        'depth_cm', 'total_precipitation', 'mean_temperature',
        'dem', 'slope', 'aspect', 'hillshade', 'bd_mean',
        'clay_mean', 'om_mean', 'ph_mean', 'sand_mean',
        'land_use_1.0', 'land_use_2.0', 'land_use_3.0', 'land_use_4.0',
        'land_use_5.0', 'land_use_6.0', 'land_cover_1.0', 'land_cover_3.0',
        'land_cover_4.0', 'land_cover_7.0', 'land_cover_8.0', 'land_cover_9.0',
        'land_cover_10.0', 'land_cover_12.0', 'land_cover_14.0'
    ]

    # Reindex the DataFrame to ensure it includes all expected columns
    df = df.reindex(columns=expected_columns, fill_value=0)

    return df


def get_prediction(request: PredictionRequest) -> PredictionResponse:
    """
    Generates a prediction using a pre-trained model.
    """
    try:
        # Load the pre-trained model
        model = xgb.XGBRegressor()
        model.load_model('xgb_model.json')

        # Transform request into a DataFrame
        data_input = transform_to_dataframe([request])

        # Make predictions
        prediction = model.predict(data_input)
        soil_organic_carbon = prediction[0]

        # Calculate soil organic carbon stock
        soil_organic_carbon_stock = soil_organic_carbon * request.depth_cm * request.bd_mean

        return PredictionResponse(
            soil_organic_carbon=soil_organic_carbon,
            soil_organic_carbon_stock=soil_organic_carbon_stock
        )
    except Exception as e:
        logging.error(f"Error during model prediction: {e}")
        raise HTTPException(status_code=500, detail=f"{e}")


app = FastAPI(
    docs_url='/',
    title="SoilOrganicCarbon",
    description="The Soil Organic Carbon tool provides a prediction of soil organic carbon in an specific location.",
)


@app.post('/v1/prediction', response_model=PredictionResponse)
def make_model_prediction(request: PredictionRequest):
    """
    Make a prediction based on the provided input.
    """
    prediction = get_prediction(request)
    return prediction