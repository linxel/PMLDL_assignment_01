import os
import requests
import streamlit as st

st.set_page_config(page_title="Model Inference UI", layout="centered")

st.title("Iris Species Predictor")
st.write("Enter the floral measurements below to request a prediction from the API.")

api_url = os.getenv("API_URL", "http://api:8000/predict")

sepal_length = st.number_input("Sepal Length (cm)", min_value=0.0, max_value=15.0, value=5.1, step=0.1)
sepal_width = st.number_input("Sepal Width (cm)", min_value=0.0, max_value=15.0, value=3.5, step=0.1)
petal_length = st.number_input("Petal Length (cm)", min_value=0.0, max_value=15.0, value=1.4, step=0.1)
petal_width = st.number_input("Petal Width (cm)", min_value=0.0, max_value=15.0, value=0.2, step=0.1)

if st.button("Make Prediction"):
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }
    try:
        response = requests.post(api_url, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json().get("prediction")
            labels = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
            class_name = labels.get(result, f"Class {result}")
            st.success(f"Model Prediction: **{class_name}** (Code: {result})")
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
    except requests.exceptions.RequestException as exc:
        st.error(f"Failed to connect to API: {exc}")
