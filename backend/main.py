from pprint import pprint
from typing import Union

import numpy as np
import pandas as pd

from fastapi import FastAPI
from sklearn.pipeline import Pipeline
from starlette.responses import RedirectResponse

from features.transformers import Log10Transformer
from utils import load_model_from_pickle
from schemas.property_schema import PropertySchemaIn
from schemas.value_shema import ValueSchemaOut

app = FastAPI()


@app.get('/')
def redirect():
    """Redirect to root to the generated api documentation"""
    response = RedirectResponse(url='/docs/')
    return response


@app.post('/property-value-inference/', response_model=ValueSchemaOut)
async def property_value_inference(property_: PropertySchemaIn):
    # Your price inference logic here

    property_dict = property_.dict(by_alias=True)
    property_dict['Longitude'] = np.nan
    property_dict['Latitude'] = np.nan
    property_dict = [property_dict]
    df = pd.DataFrame(property_dict)
    df['Price'] = 0

    base_pipeline = load_model_from_pickle('./models/base_pipeline.pkl')
    df = base_pipeline.transform(df)
    df.drop(columns=['Price'], inplace=True)

    after_split_pipeline = load_model_from_pickle('./models/base_after_split_pipeline.pkl')
    df = after_split_pipeline.transform(df)

    df = df.reindex(columns=['Bathroom Count', 'Bedroom Count', 'Habitable Surface', 'Land Surface',
                             'Consumption', 'Postal Code', 'Facades', 'Subtype', 'Toilet Count',
                             'Kitchen Type', 'State of Building', 'Longitude', 'Latitude'])

    # after_split_pipeline = load_model_from_pickle('./models/after_split_pipeline.pkl')
    random_forest_model = load_model_from_pickle('./models/random_forest.pkl')
    result = random_forest_model.predict(df)
    print(result)
    return {"value": 10 ** result[0]}
