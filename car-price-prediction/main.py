from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import pandas as pd
import pickle
import os

load_dotenv()

model_path = os.getenv("MODEL_PATH")


try:
    if model_path is not None:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print("✅ Model loaded successfully.")
    else:
        raise ValueError("MODEL_PATH environment variable is not set.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# --------------------------
# FastAPI App
# --------------------------
app = FastAPI(
    title="Car Price Prediction API",
    description="Predict car price using a trained ML model",
    version="1.0.0"
)

# --------------------------
# Input Schema (Swagger UI friendly)
# --------------------------
class CarFeatures(BaseModel):
    Make: str
    Model: str
    Fuel_Type: str
    Transmission: str
    Year: int
    Engine_Size: float
    Dist_Driven: int


# --------------------------
# Prediction Endpoint
# --------------------------
@app.post("/predict")
def predict_car_price(features: CarFeatures):
    if model is None:
        return {"error": "Model not loaded."}

    # Map API fields -> training column names
    input_data = pd.DataFrame([{
        "Make": features.Make,
        "Model": features.Model,
        "Fuel Type": features.Fuel_Type,     # Match training column exactly
        "Transmission": features.Transmission,
        "Year": features.Year,
        "Engine Size": features.Engine_Size, # Match training column exactly
        "Dist_Driven": features.Dist_Driven
    }])

    try:
        prediction = model.predict(input_data)
        return {"predicted_price": float(prediction[0])}
    except Exception as e:
        return {"error": str(e)}

# --------------------------
# Health Check
# --------------------------
@app.get("/")
def health_check():
    return {"status": "API is running!"}
