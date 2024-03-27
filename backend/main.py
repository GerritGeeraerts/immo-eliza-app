import numpy as np
import pandas as pd

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from schemas.address_schema import AddressSchemaIn, LongLatSchemaOut
from utils import load_model_from_pickle, get_coordinates
from schemas.property_schema import PropertySchemaIn
from schemas.value_shema import ValueSchemaOut

app = FastAPI(
    title="Property Value Inference API",
    description="API to infer the value of a property",
)


@app.get('/')
def redirect():
    """Redirect to root to the generated api documentation"""
    response = RedirectResponse(url='/docs/')
    return response


@app.post('/property-value-inference/', response_model=ValueSchemaOut)
async def property_value_inference(property_: PropertySchemaIn):
    property_dict = property_.dict(by_alias=True)
    property_dict['Longitude'] = property_dict['Longitude'] if property_dict['Longitude'] else np.nan
    property_dict['Latitude'] = property_dict['Latitude'] if property_dict['Latitude'] else np.nan
    print(property_dict)
    property_dict = [property_dict]
    df = pd.DataFrame(property_dict)

    pipeline = load_model_from_pickle('./models/catboost.pkl')
    y_pred = pipeline.predict(df)

    df = pipeline.transform(df)
    region_price = df.iloc[0]['RegionPricePerSqm']

    return {"value": y_pred[0], "region_price": region_price}


@app.post('/lat-long-for-address', response_model=LongLatSchemaOut)
async def get_lat_lon(address: AddressSchemaIn):
    property_dict = address.dict(by_alias=True)
    lat, lon = get_coordinates(
        number=property_dict['Street Number'],
        street=property_dict['Street Name'],
        postalcode=property_dict['Postal Code']
    )
    return {"Latitude": lat, "Longitude": lon}