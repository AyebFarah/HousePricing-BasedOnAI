import joblib
import pandas as pd
import numpy as np
from .feature_engineering import engineer_features
from utils.constants import VILLES, CATEGORIES, TYPES_TRANSACTION
from config import MODEL_PATH, SCALER_PATH, FEATURES_PATH

# Charger les objets
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_cols = joblib.load(FEATURES_PATH)

def create_price_segment(price_estimate):
    if price_estimate < 200000:
        return 'budget'
    elif price_estimate < 500000:
        return 'mid_range'
    elif price_estimate < 1000000:
        return 'high_end'
    else:
        return 'luxury'

def prepare_input(room_count, bathroom_count, size, location, category, transaction_type):
    if transaction_type == 'À Louer':
        price_estimate = size * 5 + room_count * 200
    else:
        price_estimate = size * 1500 + room_count * 50000

    price_segment = create_price_segment(price_estimate)

    input_data = pd.DataFrame({
        'room_count': [room_count],
        'bathroom_count': [bathroom_count],
        'size': [size],
        'category': [category],
        'type': [transaction_type],
        'location': [location],
        'price_segment': [price_segment]
    })
    
    # Before using the values, normalize to lowercase for cities
    if location.lower() not in [v.lower() for v in VILLES]:
        location = 'tunis'  # default city

    if category not in CATEGORIES:
        category = 'Appartements'  # default category


    input_data = engineer_features(input_data)

    input_encoded = pd.get_dummies(input_data, columns=['category','type','location','price_segment'])
    X_pred = pd.DataFrame(0, index=[0], columns=feature_cols)
    for col in input_encoded.columns:
        if col in X_pred.columns:
            X_pred[col] = input_encoded[col].values

    num_cols = ['room_count', 'bathroom_count', 'size', 'room_bathroom_ratio', 
                'total_rooms', 'size_per_room', 'bathroom_density',
                'size_x_rooms', 'size_x_bathrooms']
    X_pred[num_cols] = scaler.transform(X_pred[num_cols])

    return X_pred, transaction_type

def predict_price(room_count, bathroom_count, size, location, category, transaction_type):
    X_pred, prop_type = prepare_input(room_count, bathroom_count, size, location, category, transaction_type)
    log_price_pred = model.predict(X_pred)[0]
    price_pred = 10 ** log_price_pred

    bias_factors = {'À Vendre': 1.0022, 'À Louer': 0.9935}
    price_pred = price_pred * bias_factors.get(prop_type, 1.0)

    conf_low = price_pred * 0.8
    conf_high = price_pred * 1.2

    return price_pred, conf_low, conf_high
