from flask import Flask, request, jsonify
from flask_cors import CORS
from models.predictor import predict_price
from utils.constants import VILLES, CATEGORIES, TYPES_TRANSACTION

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "API running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        room_count = int(data.get('room_count'))
        bathroom_count = int(data.get('bathroom_count'))
        size = float(data.get('size'))
        location = data.get('location', 'Tunis')
        category = data.get('category', 'Appartements')
        transaction_type = data.get('type', 'À Vendre')

        if location not in VILLES:
            location = 'Tunis'
        if category not in CATEGORIES:
            category = 'Appartements'
        if transaction_type not in TYPES_TRANSACTION:
            transaction_type = 'À Vendre'

        price, conf_low, conf_high = predict_price(room_count, bathroom_count, size, location, category, transaction_type)

        response = {
            "predicted_price": float(price),
            "conf_low": float(conf_low),
            "conf_high": float(conf_high),
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
