from typing import Literal

import numpy as np
from pydantic import BaseModel, Field, conint, ConfigDict, field_validator

from config import POSTAL_CODES


class PropertySchemaIn(BaseModel):
    model_config = ConfigDict(populate_by_name=False)
    habitable_surface: conint(gt=0, lt=1001) = Field(
        default=100,
        description="The surface of the house that is habitable in square meters.",
        example=100,
        alias="Habitable Surface"
    )
    subtype: Literal['HOUSE', 'VILLA', 'MANSION', 'EXCEPTIONAL_PROPERTY', 'APARTMENT', 'PENTHOUSE', 'DUPLEX',
    'GROUND_FLOOR', 'TOWN_HOUSE', 'FLAT_STUDIO', 'SERVICE_FLAT'] = Field(
        default='HOUSE',
        description="The subtype of the house.",
        alias="Subtype"
    )
    land_surface: conint(gt=-1, lt=10001) = Field(
        default=500,
        description="The surface of the land in square meters.",
        example=500,
        alias="Land Surface",
    )
    bedroom_count: conint(gt=-1, lt=11) = Field(
        default=3,
        description="The number of bedrooms in the house.",
        example=3,
        alias="Bedroom Count",
    )
    bathroom_count: conint(gt=-1, lt=11) = Field(
        default=1,
        description="The number of bathrooms in the house.",
        example=1,
        alias="Bathroom Count",
    )
    toilet_count: conint(gt=-1, lt=11) = Field(
        default=2,
        description="The number of toilets in the house.",
        example=2,
        alias="Toilet Count",
    )
    facades: conint(gt=1, lt=5) = Field(
        default=4,
        description="The number of facades of the house.",
        example=4,
        alias="Facades",
    )
    consumption: conint(gt=-1, lt=1001) = Field(
        default=100,
        description="The energy consumption of the house in kWh/m²/year.",
        example=100,
        alias="Consumption",
    )
    kitchen_type: Literal['HYPER_EQUIPPED', 'EQUIPPED', 'SEMI_EQUIPPED', 'NOT_EQUIPPED'] = Field(
        default='EQUIPPED',
        description="The type of kitchen in the house.",
        alias="Kitchen Type",
    )
    state_of_building: Literal['NEW', 'GOOD', 'TO_BE_DONE_UP', 'TO_RENOVATE', 'JUST_RENOVATED'] = Field(
        default='NEW',
        description="The state of the building.",
        alias="State of Building",
    )
    postal_code: int = Field(
        default='1000',
        description="The postal code of the house.",
        alias="Postal Code",
    )
    longitude: float = Field(
        default=0,
        description="The longitude of the house.",
        alias="Longitude",
    )
    latitude: float = Field(
        default=0,
        description="The latitude of the house.",
        alias="Latitude",
    )
    @field_validator('postal_code')
    @classmethod
    def check_postal_code(cls, v):
        if v not in POSTAL_CODES:
            raise ValueError(f"{v} is not an allowed postal code, it has to be one of {POSTAL_CODES}")
        return v