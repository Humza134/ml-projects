from pydantic import BaseModel, Field, field_validator, conint, confloat, model_validator
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"

class UserInput(BaseModel):
    age: int = Field(..., description="Age of the person (years)", ge=30, le=80)
    gender: GenderEnum = Field(..., description="Gender: male/female")
    current_smoker: bool = Field(..., alias="currentSmoker", description="Is the person a current smoker?")
    cigs_per_day: float = Field(..., alias="cigsPerDay", description="Number of cigarettes per day", ge=0)
    bp_medication: bool = Field(..., alias="BP_medication", description="Is the person on BP medication?")
    prevalent_stroke: bool = Field(..., alias="prevalentStroke", description="Has the person had a stroke?")
    prevalent_hypertensive: bool = Field(..., alias="prevalentHypertensive", description="Is the person hypertensive?")
    diabetes: bool = Field(..., description="Does the person have diabetes?")
    total_cholesterol: float = Field(..., alias="totalCholesterol", description="Total cholesterol (mg/dL)", ge=100, le=600)
    systolic_bp: float = Field(..., alias="systolicBP", description="Systolic blood pressure", ge=80, le=250)
    diastolic_bp: float = Field(..., alias="diastolicBP", description="Diastolic blood pressure", ge=40, le=150)
    bmi: float = Field(..., alias="bmi", description="Body Mass Index (always uppercase BMI)", ge=10, le=60)
    heart_rate: int = Field(..., alias="heartRate", description="Heart rate (bpm)", ge=40, le=200)
    glucose: float = Field(..., description="Glucose level (mg/dL)", ge=50, le=300)

    @field_validator("current_smoker", "bp_medication", "prevalent_stroke", "prevalent_hypertensive", "diabetes", "gender")
    @classmethod
    def to_numeric(cls, v, field):
        if field.field_name == "gender":
            if isinstance(v, str):
                return 0 if v.strip().lower() == "female" else 1
            elif isinstance(v, int):
                return 0 if v == 0 else 1
        else:
            # binary fields
            if isinstance(v, str):
                v = v.strip().lower()
                if v in ["yes", "true", "1"]:
                    return 1
                if v in ["no", "false", "0"]:
                    return 0
            return 1 if bool(v) else 0

class PredictionResponse(BaseModel):
    prediction: str = Field(..., description="Predicted risk: 'yes' = Risk of TenYearCHD, 'no' = No risk")

# class PredictionResponse(BaseModel):
#     prediction_value: int  # model se 0/1
#     prediction: str = Field(..., description="Predicted risk: 'yes' = Risk, 'no' = No risk")

#     @model_validator(mode="after")
#     def convert_to_yes_no(cls, values):
#         values["prediction"] = "yes" if values["prediction_value"] == 1 else "no"
#         return values
