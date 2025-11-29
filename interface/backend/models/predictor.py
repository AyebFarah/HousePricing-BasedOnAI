# =============================================================================
# prediction.py - Module de prédiction sans data leakage
# =============================================================================

import joblib
import pandas as pd
import numpy as np
from .feature_engineering import engineer_features
from utils.constants import VILLES, CATEGORIES, TYPES_TRANSACTION
from config import (MODEL_PATH, SCALER_PATH, FEATURES_PATH, 
                   LOCATION_STATS_PATH, PREMIUM_LOCATIONS_PATH)

# Charger les objets
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
feature_cols = joblib.load(FEATURES_PATH)
location_stats = joblib.load(LOCATION_STATS_PATH)  # Stats de location (train set)
premium_locations = joblib.load(PREMIUM_LOCATIONS_PATH)  # Zones premium


def prepare_input(room_count, bathroom_count, size, location, category, transaction_type):
    """
    Prépare les données d'entrée pour la prédiction SANS DATA LEAKAGE.
    
    Utilise:
    - luxury_score: calculé à partir de features disponibles
    - location_price_level: stats calculées sur train set
    - property_tier: basé sur luxury_score
    
    Args:
        room_count (int): Nombre de chambres
        bathroom_count (int): Nombre de salles de bain
        size (float): Surface en m²
        location (str): Ville
        category (str): Type de bien
        transaction_type (str): 'À Vendre' ou 'À Louer'
    
    Returns:
        tuple: (X_pred DataFrame, transaction_type)
    """
    
    # Normaliser les inputs (case-insensitive pour les villes)
    location_normalized = location.strip()
    if location_normalized.lower() not in [v.lower() for v in VILLES]:
        location_normalized = 'Tunis'  # Ville par défaut
    
    if category not in CATEGORIES:
        category = 'Appartements'  # Catégorie par défaut
    
    # Créer DataFrame de base
    input_data = pd.DataFrame({
        'room_count': [room_count],
        'bathroom_count': [bathroom_count],
        'size': [size],
        'category': [category],
        'type': [transaction_type],
        'location': [location_normalized]
    })
    
    # Feature engineering (sans leakage!)
    input_data = engineer_features(input_data, location_normalized, premium_locations)
    
    # Ajouter location_price_level (calculé sur train set)
    location_match = location_stats[
        location_stats['location'].str.lower() == location_normalized.lower()
    ]
    
    if len(location_match) > 0:
        input_data['location_price_level'] = location_match['location_price_level'].values[0]
    else:
        # Ville inconnue -> utiliser la médiane (1.0)
        input_data['location_price_level'] = 1.0
    
    # Créer property_tier basé sur luxury_score
    luxury_score = input_data['luxury_score'].values[0]
    if luxury_score < 0.5:
        property_tier = 'standard'
    elif luxury_score < 1.0:
        property_tier = 'upscale'
    else:
        property_tier = 'luxury'
    
    input_data['property_tier'] = property_tier
    
    # One-hot encoding
    input_encoded = pd.get_dummies(input_data, 
                                    columns=['category', 'type', 'location', 'property_tier'])
    
    # Créer DataFrame avec toutes les features attendues
    X_pred = pd.DataFrame(0, index=[0], columns=feature_cols)
    
    # Remplir les colonnes présentes
    for col in input_encoded.columns:
        if col in X_pred.columns:
            X_pred[col] = input_encoded[col].values
    
    # Standardiser les features numériques
    num_cols = ['room_count', 'bathroom_count', 'size', 'room_bathroom_ratio', 
                'total_rooms', 'size_per_room', 'bathroom_density',
                'size_x_rooms', 'size_x_bathrooms', 'luxury_score',
                'is_premium_location', 'location_price_level']
    
    # Ne transformer que les colonnes présentes
    num_cols_present = [col for col in num_cols if col in X_pred.columns]
    X_pred[num_cols_present] = scaler.transform(X_pred[num_cols_present])
    
    return X_pred, transaction_type


def predict_price(room_count, bathroom_count, size, location, category, transaction_type):
    """
    Prédit le prix d'une propriété.
    
    Args:
        room_count (int): Nombre de chambres
        bathroom_count (int): Nombre de salles de bain
        size (float): Surface en m²
        location (str): Ville
        category (str): Type de bien
        transaction_type (str): 'À Vendre' ou 'À Louer'
    
    Returns:
        tuple: (prix_prédit, intervalle_conf_bas, intervalle_conf_haut)
    """
    
    # Préparer les données (sans leakage!)
    X_pred, prop_type = prepare_input(
        room_count, bathroom_count, size, location, category, transaction_type
    )
    
    # Prédiction en log-space
    log_price_pred = model.predict(X_pred)[0]
    
    # Back-transform
    price_pred = 10 ** log_price_pred
    
    # Bias correction basé sur le type (calculé lors de l'entraînement)
    bias_factors = {'À Vendre': 1.0022, 'À Louer': 0.9935}
    price_pred = price_pred * bias_factors.get(prop_type, 1.0)
    
    # Intervalle de confiance (±20% pour l'immobilier)
    conf_low = price_pred * 0.8
    conf_high = price_pred * 1.2
    
    return price_pred, conf_low, conf_high

