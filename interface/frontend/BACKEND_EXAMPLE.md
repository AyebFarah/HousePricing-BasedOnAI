# Backend API Python pour ImmoPredict

Ce fichier contient un exemple de backend Flask pour servir le modèle de prédiction de prix immobilier.

## Installation des dépendances

```bash
pip install flask flask-cors pandas scikit-learn numpy joblib
```

## Code Python (Flask)

Créez un fichier `app.py` :

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
# ou si vous utilisez pickle: import pickle

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend React

# Chargez votre modèle entraîné (Ridge, XGBoost, etc.)
# Exemple avec joblib:
# model = joblib.load('model_ridge.pkl')
# ou avec pickle:
# with open('model_ridge.pkl', 'rb') as f:
#     model = pickle.load(f)

# Pour cet exemple, nous utilisons un modèle factice
class DummyModel:
    def predict(self, X):
        # Simuler une prédiction basée sur les features
        # Dans votre cas réel, votre modèle prédit log_price
        # donc vous devrez faire np.exp(prediction) pour obtenir le prix réel
        base_price = 50000 + X[0][2] * 800  # Prix de base + taille * 800
        return np.array([np.log(base_price)])

model = DummyModel()

# Erreur moyenne pour l'intervalle de confiance (en TND)
ERROR_MARGIN = 430

# Mapping pour l'encodage des features catégorielles
# Ajustez selon votre entraînement
LOCATION_MAPPING = {
    "Tunis": 0, "Sfax": 1, "Sousse": 2, "Kairouan": 3, "Bizerte": 4,
    "Gabès": 5, "Ariana": 6, "Gafsa": 7, "Monastir": 8, "Ben Arous": 9,
    # ... ajoutez toutes vos villes
}

CATEGORY_MAPPING = {
    "Appartement": 0, "Maison": 1, "Villa": 2, 
    "Studio": 3, "Duplex": 4, "Terrain": 5
}

TYPE_MAPPING = {
    "Vente": 0, "Location": 1
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extraction des données
        rooms = float(data.get('rooms'))
        bathrooms = float(data.get('bathrooms'))
        size = float(data.get('size'))
        age = float(data.get('age'))
        location = data.get('location')
        category = data.get('category')
        transaction_type = data.get('type')
        
        # Encodage des features catégorielles
        location_encoded = LOCATION_MAPPING.get(location, 0)
        category_encoded = CATEGORY_MAPPING.get(category, 0)
        type_encoded = TYPE_MAPPING.get(transaction_type, 0)
        
        # Créer le vecteur de features dans le même ordre que lors de l'entraînement
        # Ajustez selon votre ordre exact de features
        features = np.array([[
            rooms, 
            bathrooms, 
            size, 
            age, 
            location_encoded, 
            category_encoded, 
            type_encoded
        ]])
        
        # Prédiction (votre modèle prédit log_price)
        log_price_pred = model.predict(features)[0]
        
        # Convertir en prix réel
        price = np.exp(log_price_pred)
        
        # Calculer l'intervalle de confiance
        min_price = price - ERROR_MARGIN
        max_price = price + ERROR_MARGIN
        
        # S'assurer que les prix sont positifs
        min_price = max(0, min_price)
        
        return jsonify({
            'price': float(price),
            'min_price': float(min_price),
            'max_price': float(max_price),
            'log_price': float(log_price_pred)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API is running'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Utilisation

1. **Entraînez votre modèle** et sauvegardez-le :
```python
import joblib
# Après avoir entraîné votre modèle Ridge ou XGBoost
joblib.dump(model, 'model_ridge.pkl')
```

2. **Lancez le serveur Flask** :
```bash
python app.py
```

3. **Le frontend React se connectera automatiquement** à `http://localhost:5000/predict`

4. **Pour le déploiement en production** :
   - Utilisez Gunicorn : `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
   - Déployez sur Heroku, AWS, DigitalOcean, etc.
   - Mettez à jour l'URL de l'API dans `PredictionForm.tsx`

## Structure des données

Le frontend envoie :
```json
{
  "rooms": 3,
  "bathrooms": 2,
  "size": 120,
  "age": 5,
  "location": "Tunis",
  "category": "Appartement",
  "type": "Vente"
}
```

L'API retourne :
```json
{
  "price": 150000,
  "min_price": 149570,
  "max_price": 150430,
  "log_price": 11.918
}
```

## Notes importantes

1. **Ordre des features** : Assurez-vous que l'ordre des features dans le vecteur correspond exactement à celui utilisé lors de l'entraînement
2. **Encodage** : Utilisez le même encodage (Label Encoding, One-Hot, etc.) que lors de l'entraînement
3. **Log transformation** : Si votre modèle prédit `log_price`, utilisez `np.exp()` pour obtenir le prix réel
4. **CORS** : Flask-CORS est nécessaire pour permettre les requêtes depuis le frontend React

## Alternative avec FastAPI

Si vous préférez FastAPI :

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    rooms: float
    bathrooms: float
    size: float
    age: float
    location: str
    category: str
    type: str

@app.post("/predict")
async def predict(request: PredictionRequest):
    # Même logique que Flask
    pass
```

Lancez avec : `uvicorn app:app --reload --host 0.0.0.0 --port 5000`
