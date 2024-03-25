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

# 'Bathroom Count', 'Bedroom Count', 'Habitable Surface', 'Land Surface', 'Consumption', 'Postal Code',
#     'Facades', 'Subtype', 'Toilet Count', 'Kitchen Type', 'State of Building',  # 'Sea view', 'Swimming Pool',
#     'Price', 'Longitude', 'Latitude', 'EPC',
@app.post('/property-value-inference/', response_model=ValueSchemaOut)
async def property_value_inference(property_: PropertySchemaIn):
    # Your price inference logic here

    property_dict = property_.dict(by_alias=True)
    property_dict['Longitude'] = np.nan
    property_dict['Latitude'] = np.nan
    property_dict = [property_dict]
    df = pd.DataFrame(property_dict)
    print(df)
    log_pipe = Pipeline([
        ('Log Scale',
         Log10Transformer(columns=['Bathroom Count', 'Bedroom Count', 'Habitable Surface', 'Land Surface'])),
    ])

    df = log_pipe.fit_transform(df)


    # base_pipeline = load_model_from_pickle('./models/base_pipeline.pkl')
    after_split_pipeline = load_model_from_pickle('./models/after_split_pipeline.pkl')
    df = after_split_pipeline.transform(df)
    df = df.reindex(columns=['Bathroom Count', 'Bedroom Count', 'Habitable Surface', 'Land Surface',
                             'Consumption', 'Postal Code', 'Facades', 'Subtype', 'Toilet Count',
                             'Kitchen Type', 'State of Building', 'Longitude', 'Latitude'])

    # after_split_pipeline = load_model_from_pickle('./models/after_split_pipeline.pkl')
    linear_regression = load_model_from_pickle('./models/linearregression_log10.pkl')
    result = linear_regression.predict(df)
    print(result)
    return {"value": 10**result[0]}

