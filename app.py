from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import re

app = Flask(__name__)
CORS(app)

FIELD_KEYS = {
    "Age": "age",
    "Sex": "sex",
    "Chest Pain Type": "cp",
    "Resting Blood Pressure": "trestbps",
    "Serum Cholestoral": "chol",
    "Fasting Blood Sugar": "fbs",
    "Resting ECG": "restecg",
    "Maximum Heart Rate Achieved": "thalach",
    "Exercise Induced Angina": "exang",
    "Oldpeak": "oldpeak",
    "Slope": "slope",
    "Number of Major Vessels": "ca",
    "Thalassemia": "thal"
}

@app.route("/extract-pdf", methods=["POST"])
def extract_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["pdf"]
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = "\n".join([page.get_text() for page in doc])

    extracted = {}
    for label, key in FIELD_KEYS.items():
        match = re.search(rf"{label}.*?\(?(\d+\.?\d*)\)?", text)
        if match:
            extracted[key] = float(match.group(1))
        else:
            extracted[key] = 0.0

    # Also try to extract Age as a fallback
    if "age" not in extracted or extracted["age"] == 0.0:
        age_match = re.search(r"Age[:\s]+(\d+)", text)
        if age_match:
            extracted["age"] = float(age_match.group(1))

    return jsonify({"features": extracted})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = data.get("features", [])

    if not isinstance(features, list) or len(features) != 13:
        return jsonify({"error": "Invalid input"}), 400

    # Dummy prediction (for example purpose)
    prediction = int(sum(features) % 2 == 0)
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)
