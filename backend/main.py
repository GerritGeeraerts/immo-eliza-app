from pprint import pprint
from typing import Union

from fastapi import FastAPI
from starlette.responses import RedirectResponse

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
    pprint(property_.dict(by_alias=True))
    return {"value": 15556.0568}

