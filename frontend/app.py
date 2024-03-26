import os.path
from pprint import pprint

import streamlit as st
import requests

from config import POSTAL_CODES
from utils import get_epc_label

subtype_options = {
    '🏠 House': 'HOUSE',
    '🏢 Apartment': 'APARTMENT',
    '🏡 Villa': 'VILLA',
    'Mansion': 'MANSION',
    'Exceptional Property': 'EXCEPTIONAL_PROPERTY',
    'Penthouse': 'PENTHOUSE',
    'Duplex': 'DUPLEX',
    'Ground Floor': 'GROUND_FLOOR',
    'Town House': 'TOWN_HOUSE',
    'Flat Studio': 'FLAT_STUDIO',
    'Service Flat': 'SERVICE_FLAT',
}
state_of_building_options = {
    'New': 'NEW',
    'Just Renovated': 'JUST_RENOVATED',
    'Good': 'GOOD',
    'To Be Done Up': 'TO_BE_DONE_UP',
    'To Renovate': 'TO_RENOVATE',
}
kitchen_options = {
    'Hyper Equipped': 'HYPER_EQUIPPED',
    'Equipped': 'EQUIPPED',
    'Semi Equipped': 'SEMI_EQUIPPED',
    'Not Equipped': 'NOT_EQUIPPED',
}


# st.session_state.subtype = 'HOUSE'
def predict_price(data):
    print('Predicting price...')
    url = 'http://127.0.0.1:8000/property-value-inference/'
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get the prediction. Please check the API and try again.")
        return None


def recalculate_prediction():
    data = {
        "Habitable Surface": st.session_state.get("Habitable Surface"),
        "Subtype": subtype_options[st.session_state.get("Subtype", '🏠 House')],
        "Land Surface": st.session_state.get("Land Surface", 500),
        "Bedroom Count": st.session_state.get("Bedroom Count", 3),
        "Bathroom Count": st.session_state.get("Bathroom Count", 3),
        "Toilet Count": st.session_state.get("Toilet Count", 3),
        "Facades": st.session_state.get("Facades", 4),
        "Consumption": st.session_state.get("Consumption"),
        "Kitchen Type": kitchen_options[st.session_state.get("Kitchen Type", 'Equipped')],
        "State of Building": state_of_building_options[st.session_state.get("State of Building", 'New')],
        "Postal Code": POSTAL_CODES[st.session_state.get("Postal Code", "1000 - Brussel")]
    }
    prediction = predict_price(data)
    if prediction:
        st.session_state['price'] = price = prediction.get('value')
        st.session_state['unit'] = unit = prediction.get('unit')
        st.session_state[
            'output'] = f"The predicted price of the house is:\n# {unit} {f'{price:,.0f}'.replace(',', '.')},-"


title = st.sidebar.title('Prediction')

st.sidebar.success(f"{st.session_state['output'] if 'output' in st.session_state else 'Move a slider to predict'}")

st.image(os.path.join('images', 'house.png'), use_column_width='always')

# Streamlit app layout
st.title('🇧🇪 Belgian House Price Prediction')

st.subheader('Housing Type')

st.selectbox(
    'Subtype',
    key='Subtype',
    options=subtype_options,
    index=0,
    on_change=recalculate_prediction
)
st.slider(
    'Facades',
    key="Facades",
    min_value=2, max_value=4, value=4, step=1,
    on_change=recalculate_prediction
)
st.subheader('Surface')
st.slider(
    'Habitable Surface',
    key="Habitable Surface",
    min_value=20, max_value=1000, value=100, step=5, format="%d m²",
    on_change=recalculate_prediction
)
if subtype_options[st.session_state.get('Subtype')] != 'APARTMENT':  # Check if the selected subtype is not 'APARTMENT'
    land_surface = st.slider(
        'Land Surface',
        key="Land Surface",
        min_value=0, max_value=10000, value=500, step=25, format="%d m²",
        on_change=recalculate_prediction,
    )
else:
    st.session_state['Land Surface'] = 0
st.subheader('Rooms')
bedroom_count = st.slider(
    'Bedroom Count',
    key="Bedroom Count",
    min_value=0, max_value=10, value=3, step=1,
    on_change=recalculate_prediction,
)
bathroom_count = st.slider(
    'Bathroom Count',
    key="Bathroom Count",
    min_value=0, max_value=10, value=1, step=1,
    on_change=recalculate_prediction,
)
toilet_count = st.slider(
    'Toilet Count',
    key="Toilet Count",
    min_value=0, max_value=10, value=2, step=1,
    on_change=recalculate_prediction,
)
st.subheader('State of the House')

state_of_building = st.selectbox(
    'State of Building',
    key="State of Building",
    options=state_of_building_options,
    index=1,
    on_change=recalculate_prediction,
)

kitchen_type = st.selectbox(
    'Kitchen Type',
    key="Kitchen Type",
    options=kitchen_options,
    index=1,
    on_change=recalculate_prediction,
)

consumption = st.slider(
    'Consumption',
    key="Consumption",
    min_value=0, max_value=1000, value=100, step=10, format="%d kWh/m²/year",
    on_change=recalculate_prediction
)
epc_category, epc_image_path = get_epc_label(consumption)
st.image(epc_image_path, width=100)

st.subheader('Address')
postal_code = st.selectbox(
    'Postal Code',
    key="Postal Code",
    options=POSTAL_CODES,
    index=0,
    on_change=recalculate_prediction,
)
street_name = st.text_input(
    'Street Name',
    'Rue de la Loi',
    key="Street Name",
)
street_number = st.number_input(
    'Street Number (No letters)]',
    1,
    key="Street Number",
)
st.text(
    "The model is predicting listing price as it is trained on listing prices.\n"
    "The model is trained on Belgian real estate data.\n"
    "It is trained on a limited set of features that are listed above.\n"
)