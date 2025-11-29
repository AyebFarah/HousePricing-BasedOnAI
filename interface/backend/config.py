import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "output", "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "output", "scaler.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "output", "feature_cols.pkl")