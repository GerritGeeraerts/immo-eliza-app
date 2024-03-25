from pydantic import Field, BaseModel, field_validator


class ValueSchemaOut(BaseModel):
    value: float = Field(
        ...,
        description="The numerical value to be rounded and output."
    )
    unit: str = Field(
        default="EUR",
        description="The unit of measurement for the value, defaulting to 'EUR'."
    )

    @field_validator('value')
    @classmethod
    def rounded_value(cls, value: float) -> int:
        """
        Round the value to the nearest thousand.
        """
        return int(round(value, -3))
