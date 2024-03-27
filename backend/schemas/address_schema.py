from pydantic import BaseModel, Field, conint


class AddressSchemaIn(BaseModel):
    street_name: str = Field(
        ...,
        description="The name of the street where the house is located.",
        alias="Street Name",
    )
    street_number: conint(gt=-1) = Field(
        ...,
        description="The number of the house on the street.",
        alias="Street Number",
    )
    postal_code: int = Field(
        ...,
        description="The postal code of the house.",
        alias="Postal Code",
    )


class LongLatSchemaOut(BaseModel):
    Latitude: float
    Longitude: float
