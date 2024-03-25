# Input
required = ['Habitable Surface', 'Land Surface', 'Price', 'Subtype', 'Bedroom Count', 'Postal Code', 'Bathroom Count']
optional = ['Consumption', 'Facades', 'Toilet Count', 'Kitchen Type', 'State of Building',]
calculated = ['Longitude', 'Latitude', ]  # calculated from postal code

# Input fields
## Habitable Surface
- Type: integer
- Description: The surface of the house that is habitable in square meters.
- Example: 100
- Default: 100
- Range: [0, 1000]
- Unit: m²
- Validation: The value must be in the range [0, 1000].
- A slider can be used to select the value.
## Subtype
- Type: string
- Description: The subtype of the house.
- Example: House
- Required: True
- Options: 'HOUSE', 'VILLA', 'MANSION', 'EXCEPTIONAL_PROPERTY', 'APARTMENT', 'PENTHOUSE', 'DUPLEX', 'GROUND_FLOOR', 'TOWN_HOUSE', 'FLAT_STUDIO', 'SERVICE_FLAT'
- Validation: The value must be one of the options.
- A dropdown can be used to select the value.
- Default: 'HOUSE'
- Note: The options are defined in the API documentation.
## Land Surface
- Type: integer
- Description: The surface of the land in square meters.
- Example: 200
- Default: 500
- Range: [0, 10000]
- Unit: m²
- Validation: The value must be in the range [0, 10000].
- A slider can be used to select the value.
## Bedroom Count
- Type: integer
- Description: The number of bedrooms in the house.
- Example: 3
- Default: 3
- Range: [0, 10]
- Validation: The value must be in the range [0, 10].
- A slider can be used to select the value.
## Bathroom Count
- Type: integer
- Description: The number of bathrooms in the house.
- Example: 1
- Default: 1
- Range: [0, 10]
- Validation: The value must be in the range [0, 10].
- A slider can be used to select the value.
## Toilet Count
- Type: integer
- Description: The number of toilets in the house.
- Example: 2
- Default: 2
- Range: [0, 10]
- Validation: The value must be in the range [0, 10].
- A slider can be used to select the value.
## Facades
- Type: integer
- Description: The number of facades of the house.
- Example: 4
- Default: 4
- Range: [2, 4]
- Validation: The value must be in the range [2, 4].
- A slider can be used to select the value.
## Consumption
- Type: integer
- Description: The energy consumption of the house in kWh/m²/year.
- Example: 100
- Default: 100
- Range: [0, 1000]
- Unit: kWh/m²/year
- Validation: The value must be in the range [0, 1000].
- A slider can be used to select the value.
## Kitchen Type
- Type: string
- Description: The type of kitchen in the house.
- Example: Equipped
- Options: 'HYPER_EQUIPPED', 'EQUIPPED', 'SEMI_EQUIPPED', 'NOT_EQUIPPED'
- Validation: The value must be one of the options.
- A dropdown can be used to select the value.
- Default: 'EQUIPPED'
## State of Building
- Type: string
- Description: The state of the building.
- Example: New
- Options: 'NEW', 'GOOD', 'TO_BE_DONE_UP', 'TO_RENOVATE', 'JUST_RENOVATED'
- Validation: The value must be one of the options.
- A dropdown can be used to select the value.
- Default: 'NEW'
## Postal Code
- Type: string
- Description: The postal code of the house.
- Example: 1000
- Options: [1000, 9000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000]
- Validation: The value must be one of the options.
- A dropdown can be used to select the value.
- Default: 1000
# Outputfields
## Price
- Type: integer
- Description: The price of the house in euros.
- Example: 100000
- Unit: €
- A text element can be used to display the value.
- The value is calculated based on the input fields.
- The value is calculated using an API at 127.0.0.1:50748/property-value-inference/
There should be sent a post request to the endpoint with all the input fields as JSON data.
The response will contain the price of the house in euros.
