from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import re

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file uploaded'}), 400

        pdf_file = request.files['pdf']
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        # Extract values using regex
        keys = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
        values = {}
        for key in keys:
            match = re.search(rf"{key}[:\s]+([\d.]+)", text, re.IGNORECASE)
            if match:
                values[key] = match.group(1)
        
        return jsonify({"features": values})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
