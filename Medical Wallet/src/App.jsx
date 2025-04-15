import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [formData, setFormData] = useState({
    age: "", sex: "", cp: "", trestbps: "", chol: "", fbs: "",
    restecg: "", thalach: "", exang: "", oldpeak: "", slope: "", ca: "", thal: ""
  });

  const [result, setResult] = useState("");
  const [pdfFile, setPdfFile] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePDFUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPdfFile(file);
    const fd = new FormData();
    fd.append("pdf", file);

    try {
      const res = await axios.post("http://localhost:5000/extract-pdf", fd, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      const values = res.data.features;
      setFormData(prev => ({ ...prev, ...values }));
    } catch (err) {
      console.error("PDF upload failed:", err.response?.data || err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const values = Object.values(formData).map(Number);
    if (values.some(v => isNaN(v))) {
      setResult("Please fill all fields with valid numbers.");
      return;
    }

    try {
      const res = await axios.post("http://localhost:5000/predict", { features: values });
      setResult(res.data.prediction === 0 ? "✅ No Heart Disease" : "⚠️ Heart Disease Detected");
    } catch (err) {
      console.error("Prediction failed:", err);
      setResult("Error occurred while predicting.");
    }
  };

  return (
    <div style={{ fontFamily: "Segoe UI", maxWidth: "600px", margin: "2rem auto", padding: "2rem", background: "#222", color: "#fff", borderRadius: "10px" }}>
      <h1 style={{ textAlign: "center", color: "#4FC3F7" }}>Heart Disease Prediction</h1>
      <input type="file" accept="application/pdf" onChange={handlePDFUpload} style={{ marginBottom: "20px" }} />

      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map(key => (
          <div key={key} style={{ marginBottom: "1rem" }}>
            <label>{key.toUpperCase()}:</label>
            <input
              type="number"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              required
              style={{ width: "100%", padding: "0.5rem", borderRadius: "5px", marginTop: "5px" }}
            />
          </div>
        ))}
        <button type="submit" style={{ width: "100%", padding: "0.75rem", backgroundColor: "#4FC3F7", color: "#000", border: "none", borderRadius: "5px", fontSize: "1rem" }}>
          Predict
        </button>
      </form>

      {result && <h2 style={{ marginTop: "2rem", color: result.includes("No") ? "#00e676" : "#ff1744" }}>Result: {result}</h2>}
    </div>
  );
};

export default App;
