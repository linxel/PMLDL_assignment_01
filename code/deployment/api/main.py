import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel

app = FastAPI(title="Iris Classification API")

MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/model.joblib")
model = None


class InferenceInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.on_event("startup")
def load_model():
    global model
    path = Path(MODEL_PATH)
    if path.exists():
        model = joblib.load(path)
    else:
        model = None


@app.get("/health")
def health_check():
    return {"status": "healthy" if model is not None else "model_missing"}


@app.post("/predict")
def predict(features: InferenceInput):
    global model
    if model is None:
        load_model()
    if model is None:
        raise HTTPException(status_code=503, detail="Model artifact not available")

    input_vector = [[
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    ]]
    prediction = model.predict(input_vector)[0]
    return {"prediction": int(prediction)}
