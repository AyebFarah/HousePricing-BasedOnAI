import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

MODEL_PATH = os.path.join(OUTPUT_DIR, 'best_model.pkl')
SCALER_PATH = os.path.join(OUTPUT_DIR, 'scaler.pkl')
FEATURES_PATH = os.path.join(OUTPUT_DIR, 'feature_cols.pkl')
LOCATION_STATS_PATH = os.path.join(OUTPUT_DIR, 'location_stats.pkl')
PREMIUM_LOCATIONS_PATH = os.path.join(OUTPUT_DIR, 'premium_locations.pkl')