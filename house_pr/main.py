from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
from dotenv import load_dotenv
import os

load_dotenv()

model_path = os.getenv("MODEL_PATH")

try:
    if model_path is not None:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
        print("✅ Model loaded successfully.")
    else:
        raise ValueError("MODEL_PATH environment variable is not set.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

app = FastAPI(
    title="House Price Prediction API",
    description="Predict the price of a house based on its features.",
    version="1.0.0",
)

class HouseFeatures(BaseModel):
    area_type: str
    location: str
    total_sqft: float
    bath: int
    bhk: int

class PredictionResponse(BaseModel):
    predicted_price: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(house_features: HouseFeatures):
    if model is None:
        return {"error": "Model not loaded."}
    
    input_data = pd.DataFrame({
        "area_type": [house_features.area_type],
        "location": [house_features.location],
        "total_sqft": [house_features.total_sqft],
        "bath": [house_features.bath],
        "bhk": [house_features.bhk]
    })
    
    predicted_price = model.predict(input_data)[0]
    
    return {"predicted_price": predicted_price}

@app.get("/")
async def health_check():
    return {"status": "API is running!"}