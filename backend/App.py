# app.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
import traceback
from flask_cors import CORS
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
CORS(app)

# Load trained ML model and preprocessors
try:
    kmeans = joblib.load("kmeans_model.pkl")
    #scaler = joblib.load("scaler.pkl")
    encoder = joblib.load("encoder.pkl")
    print("✅ Model and preprocessors loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Function to preprocess input before prediction
def preprocess_input(data):
    try:
        print("📥 Received Data:", data)

        # One-Hot Encode each club separately
        club_encoded1 = encoder.fit_transform([[data['club1']]]).toarray()
        club_encoded2 = encoder.fit_transform([[data['club2']]]).toarray()
        club_encoded3 = encoder.fit_transform([[data['club3']]]).toarray()
        
        # Encode activity
        activity_encoded = encoder.fit_transform([[data['activity']]]).toarray()

        # Combine encoded features
        features = np.hstack((club_encoded1, club_encoded2, club_encoded3, activity_encoded))

        print("✅ Encoded Features:", features)

        # Scale features
        scaler = StandardScaler()
        scaled = scaler.fit_transform(features)
        return scaled
        
        

    except Exception as e:
        print(f"❌ Error in preprocessing: {e}")
        print(traceback.format_exc())
        return None

# API Status Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Flask ML API is running!"})

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Validate input data
        required_fields = ["club1", "club2", "club3", "activity"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Preprocess input
        X = preprocess_input(data)
        if X is None:
            return jsonify({"error": "Preprocessing failed!"}), 500

        # Predict the cluster
        cluster = kmeans.predict(X)[0]

        return jsonify({
            "Cluster": int(cluster),
            "message": "✅ Prediction successful!"
        })

    except Exception as e:
        print(f"❌ Error in prediction: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Internal Server Error", "details": str(traceback.format_exc())}), 500

if __name__ == "__main__":
    app.run(debug=True)
