import numpy as np

def engineer_features(data, location, premium_locations):
    """
    Applique le feature engineering SANS DATA LEAKAGE.
    
    Toutes les features sont calculables sans connaître le prix!
    
    Args:
        data (pd.DataFrame): DataFrame avec les features de base
        location (str): Nom de la ville
        premium_locations (list): Liste des zones premium
    
    Returns:
        pd.DataFrame: DataFrame avec features ajoutées
    """
    
    # Features de base (ratios et interactions)
    data['room_bathroom_ratio'] = data['room_count'] / np.maximum(data['bathroom_count'], 1)
    data['total_rooms'] = data['room_count'] + data['bathroom_count']
    data['size_per_room'] = data['size'] / np.maximum(data['room_count'], 1)
    data['bathroom_density'] = data['bathroom_count'] / np.maximum(data['size'], 1)
    data['size_x_rooms'] = data['size'] * data['room_count']
    data['size_x_bathrooms'] = data['size'] * data['bathroom_count']
    
    # Premium location indicator (liste prédéfinie)
    data['is_premium_location'] = int(location in premium_locations)
    
    # Luxury score (SANS LEAKAGE - basé uniquement sur features disponibles)
    data['luxury_score'] = (
        (data['size'] / 100) * 0.3 +           # Surface normalisée
        (data['room_count'] / 5) * 0.2 +       # Nombre de chambres normalisé
        (data['bathroom_count'] / 2) * 0.2 +   # Nombre de SdB normalisé
        data['is_premium_location'] * 0.3      # Bonus zone premium
    )
    
    # Gestion des valeurs infinies/NaN
    numeric_cols = ['room_bathroom_ratio', 'total_rooms', 'size_per_room', 
                    'bathroom_density', 'size_x_rooms', 'size_x_bathrooms', 'luxury_score']
    
    for col in numeric_cols:
        if col in data.columns:
            # Remplacer inf par NaN
            data[col] = data[col].replace([np.inf, -np.inf], np.nan)
            # Remplir NaN avec la médiane (ou 0 si une seule ligne)
            if data[col].notna().sum() > 0:
                data[col] = data[col].fillna(data[col].median())
            else:
                data[col] = data[col].fillna(0)
    
    return data

