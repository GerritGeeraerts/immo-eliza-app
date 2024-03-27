from pydantic import Field, BaseModel, field_validator


class ValueSchemaOut(BaseModel):
    value: float = Field(
        ...,
        description="The numerical value to be rounded and output."
    )
    unit: str = Field(
        default="€",
        description="The unit of measurement for the value, defaulting to 'EUR'."
    )

    region_price: float = Field(
        ...,
        description="The price per square meter of the region."
    )

    region_price_unit: str = Field(
        default="€/m²",
        description="The price per square meter of the region."
    )

    @field_validator('value', 'region_price')
    @classmethod
    def rounded_value(cls, value: float) -> int:
        """
        Round the value to the nearest thousand.
        """
        return int(round(value))
