# Automated MLOps Pipeline

This repository implements an end-to-end automated MLOps pipeline covering:
1. **Data Engineering**: Data loading, missing value removal, IQR outlier filtering, and stratified dataset splitting.
2. **Model Engineering**: Feature scaling via `StandardScaler`, model training with `RandomForestClassifier`, MLflow metric logging, and artifact packaging.
3. **Deployment**: Docker containerized FastAPI inference endpoint and Streamlit web interface orchestrated with Docker Compose.
4. **Automation**: Apache Airflow DAG scheduled to run every 5 minutes (`*/5 * * * *`).

## Repository Structure

```text
├── code
│   ├── datasets
│   │   └── data_engineering.py
│   ├── deployment
│   │   ├── api
│   │   │   ├── Dockerfile
│   │   │   └── main.py
│   │   ├── app
│   │   │   ├── Dockerfile
│   │   │   └── app.py
│   │   └── docker-compose.yml
│   └── models
│       └── model_engineering.py
├── data
│   ├── processed
│   └── raw
│       └── iris.csv
├── models
├── services
│   └── airflow
│       ├── dags
│       │   └── mlops_pipeline_dag.py
│       └── logs
├── requirements.txt
└── README.md
```

## Setup & Running Locally

### 1. Environment Initialization
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Manual Pipeline Execution (Optional)
Run individual stages sequentially from root:
```bash
python code/datasets/data_engineering.py
python code/models/model_engineering.py
docker compose -f code/deployment/docker-compose.yml up -d --build
```

### 3. Automated Execution with Airflow
Initialize Airflow home directory and start standalone services:
```bash
export AIRFLOW_HOME="$(pwd)/services/airflow"
airflow db init
airflow standalone
```
* Access the Airflow UI at `http://localhost:8080`.
* Enable the `mlops_automated_pipeline` DAG. It will trigger automatically every 5 minutes.

## Accessing Services

* **Streamlit UI**: Navigate to `http://localhost:8501`. Enter floral measurements and click **Make Prediction**.
* **FastAPI Swagger Docs**: Navigate to `http://localhost:8000/docs`.
* **FastAPI Health Check**: `http://localhost:8000/health`.
* **MLflow UI**: Run `mlflow ui` to inspect logged parameters and metrics.
