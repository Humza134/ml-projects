from fastapi import FastAPI, HTTPException
from schema.heart_dis_schema import UserInput, PredictionResponse
import joblib
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()

model_path = os.getenv("MODEL_PATH")
print(model_path)
try:
    if model_path is not None:
        with open(model_path, "rb") as f:
            model = joblib.load(f)
        print("✅ Model loaded successfully.")
    else:
        raise ValueError("MODEL_PATH is not set in the environment variables.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

app = FastAPI(
    title="Heart Disease Prediction API",
    description="An API to predict heart disease based on patient data.",
    version="1.0.0"
)

# ---------------------------
# Utility function to map 0/1 -> yes/no
# ---------------------------
def map_prediction(value: int) -> str:
    return "yes" if value == 1 else "no"

# ---------------------------
# Prediction Endpoint
# ---------------------------
@app.post("/predict", response_model=PredictionResponse)
async def predict(user: UserInput):
    try:
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded.")

        # Convert input to pandas DataFrame
        input_data = pd.DataFrame([{
            "age": user.age,
            "gender": user.gender,
            "current_smoker": user.current_smoker,
            "cigs_per_day": user.cigs_per_day,
            "bp_medication": user.bp_medication,
            "prevalent_stroke": user.prevalent_stroke,
            "prevalent_hypertensive": user.prevalent_hypertensive,
            "diabetes": user.diabetes,
            "total_cholesterol": user.total_cholesterol,
            "systolic_bp": user.systolic_bp,
            "diastolic_bp": user.diastolic_bp,
            "bmi": user.bmi,
            "heart_rate": user.heart_rate,
            "glucose": user.glucose
        }])

        # Make prediction (0 or 1)
        prediction_value = model.predict(input_data)[0]

        # Map to yes/no
        prediction_str = map_prediction(prediction_value)

        return PredictionResponse(prediction=prediction_str)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error during prediction: {str(e)}")

@app.get("/")
async def health_check():
    return {"status": "API is running"}


