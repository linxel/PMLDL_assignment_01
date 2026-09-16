# Automated MLOps Pipeline

This repository implements an end-to-end automated MLOps pipeline for Iris flower classification.

The pipeline consists of four main parts:

1. **Data Engineering** — loading, cleaning, outlier removal, and train/test splitting.
2. **Model Engineering** — feature scaling, model training, evaluation, MLflow tracking, and model packaging.
3. **Deployment** — FastAPI model API and Streamlit web application running in separate Docker containers.
4. **Automation** — Apache Airflow orchestrating all three stages every 5 minutes.

---

## Project Structure

```text
PMLDL_assignment_01/
├── code/
│   ├── datasets/
│   │   └── data_engineering.py
│   ├── deployment/
│   │   ├── api/
│   │   │   ├── Dockerfile
│   │   │   └── main.py
│   │   ├── app/
│   │   │   ├── Dockerfile
│   │   │   └── app.py
│   │   └── docker-compose.yml
│   └── models/
│       └── model_engineering.py
├── data/
│   ├── processed/
│   └── raw/
│       └── iris.csv
├── models/
├── services/
│   └── airflow/
│       ├── dags/
│       │   └── mlops_pipeline_dag.py
│       └── logs/
├── requirements.txt
├── .gitignore
└── README.md
```

Generated files such as processed datasets, MLflow database files, Airflow logs, and the packaged model are not stored in Git and are created when the pipeline runs.

---

# Requirements

Before starting, install:

* Python 3.11+
* Docker
* Docker Compose
* Git

Check the installed versions:

```bash
python3 --version
docker --version
docker compose version
git --version
```

Make sure Docker is running and the current user can access it:

```bash
docker ps
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/linxel/PMLDL_assignment_01.git
cd PMLDL_assignment_01
```

## 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

Verify the main dependencies:

```bash
python -c "import pandas, sklearn, mlflow, joblib; print('Dependencies OK')"
```

---

# Pipeline Overview

The complete pipeline is:

```text
Raw Iris Dataset
       │
       ▼
Data Engineering
       │
       ├── remove missing values
       ├── remove outliers using IQR
       └── train/test split
       │
       ▼
data/processed/
       │
       ├── train.csv
       └── test.csv
       │
       ▼
Model Engineering
       │
       ├── feature scaling
       ├── Random Forest training
       ├── evaluation
       ├── MLflow logging
       └── model packaging
       │
       ▼
models/model.joblib
       │
       ▼
Deployment
       │
       ├── FastAPI container
       └── Streamlit container
```

Airflow connects these stages and executes them automatically.

---

# Manual Pipeline Execution

The pipeline can be tested manually before starting Airflow.

Run all commands from the repository root.

## Stage 1 — Data Engineering

Run:

```bash
python code/datasets/data_engineering.py
```

This stage:

* loads `data/raw/iris.csv`;
* removes missing values;
* removes outliers using the IQR method;
* performs an 80/20 stratified train/test split;
* saves the resulting datasets.

Expected output files:

```text
data/processed/train.csv
data/processed/test.csv
```

You can verify them with:

```bash
ls data/processed/
```

---

## Stage 2 — Model Engineering

Run:

```bash
python code/models/model_engineering.py
```

This stage:

* loads `train.csv` and `test.csv`;
* applies feature scaling using `StandardScaler`;
* trains a `RandomForestClassifier`;
* evaluates the model on the testing data;
* calculates accuracy and weighted F1-score;
* logs parameters and metrics to MLflow;
* packages the trained model as a `.joblib` file.

Expected model artifact:

```text
models/model.joblib
```

---

## Stage 3 — Deployment

After the model has been created, start the API and web application:

```bash
docker compose -f code/deployment/docker-compose.yml up -d --build
```

Check the running containers:

```bash
docker ps
```

The following containers should be running:

```text
mlops_fastapi
mlops_streamlit
```

The API receives the model from the `models` directory through a Docker volume.

---

# Using the Web Application

Open:

```text
http://localhost:8501
```

The Streamlit application provides four Iris measurements:

* Sepal Length
* Sepal Width
* Petal Length
* Petal Width

Enter the values and press:

```text
Make Prediction
```

The application sends the input data to the FastAPI model API and displays the predicted Iris species.

The supported classes are:

```text
0 → Setosa
1 → Versicolor
2 → Virginica
```

---

# FastAPI

FastAPI is available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```
Open the Swagger documentation and use the `POST /predict` endpoint to test the model.

Click **Try it out**, enter the Iris flower measurements, and click **Execute**.

Health check:

```text
http://localhost:8000/health
```
The health check confirms that the API is running and that the trained model has been loaded successfully.

---

# MLflow

The model training stage uses MLflow to track experiments, parameters, testing metrics, and the trained model.

The MLflow tracking database is stored locally in:

```text
mlflow.db
```

Start the MLflow UI from the repository root:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Open:

```text
http://localhost:5000
```

The experiment is:

```text
iris_training_pipeline
```

The logged metrics include:

* Accuracy
* Weighted F1-score

The trained model is also stored as an MLflow artifact.

---

# Automated Pipeline with Airflow

The complete pipeline is orchestrated by Apache Airflow.

The DAG is located at:

```text
services/airflow/dags/mlops_pipeline_dag.py
```

The DAG executes the stages in the following order:

```text
Data Engineering
       ↓
Model Engineering
       ↓
Deployment
```

The schedule is:

```text
*/5 * * * *
```

which means that the pipeline is scheduled to run every 5 minutes.

## 1. Activate the virtual environment

```bash
source .venv/bin/activate
```

Make sure Airflow is started from this same virtual environment.

You can check:

```bash
which python
which airflow
```

Both should point to the same virtual environment.

## 2. Set Airflow home

From the repository root:

```bash
export AIRFLOW_HOME="$(pwd)/services/airflow"
```

## 3. Initialize the Airflow database

```bash
airflow db migrate
```

## 4. Start Airflow

```bash
airflow standalone
```

Keep this terminal running.

Airflow will start its required local services and expose the web interface on:

```text
http://localhost:8080
```

The standalone command may generate login credentials during startup. Use the credentials shown in the terminal.

## 5. Check the DAG

In a second terminal:

```bash
cd PMLDL_assignment_01
source .venv/bin/activate
export AIRFLOW_HOME="$(pwd)/services/airflow"
```

Check that the DAG is available:

```bash
airflow dags list
```

The expected DAG ID is:

```text
mlops_automated_pipeline
```

Open the Airflow UI:

```text
http://localhost:8080
```

Enable the DAG if it is paused.

---

# Testing the Automated Pipeline

For the first test, it is useful to trigger the DAG manually:

```bash
airflow dags trigger mlops_automated_pipeline
```

Then open the Airflow UI and verify that all three tasks complete successfully:

```text
data_engineering
       ↓
model_engineering
       ↓
deployment
```

After a successful run, verify the generated files:

```bash
ls data/processed/
```

Expected:

```text
train.csv
test.csv
```

Verify the model:

```bash
ls models/
```

Expected:

```text
model.joblib
```

Verify the Docker containers:

```bash
docker ps
```

Expected:

```text
mlops_fastapi
mlops_streamlit
```

Finally, open:

```text
http://localhost:8501
```

and make a prediction through the web application.

---

# Stopping the Services

Stop the API and Streamlit containers:

```bash
docker compose -f code/deployment/docker-compose.yml down
```
---

# Assignment Requirements

| Assignment Requirement   | Implementation                      |
| ------------------------ | ----------------------------------- |
| Data loading             | `code/datasets/data_engineering.py` |
| Data cleaning            | Missing-value removal               |
| Outlier removal          | IQR method                          |
| Train/test split         | Stratified 80/20 split              |
| Data pipeline automation | Apache Airflow                      |
| Feature engineering      | `StandardScaler`                    |
| Model training           | `RandomForestClassifier`            |
| Model evaluation         | Accuracy and weighted F1-score      |
| Metric logging           | MLflow                              |
| Model logging            | MLflow                              |
| Model packaging          | `models/model.joblib`               |
| Model API                | FastAPI                             |
| Web application          | Streamlit                           |
| API container            | `code/deployment/api/Dockerfile`    |
| App container            | `code/deployment/app/Dockerfile`    |
| Container orchestration  | Docker Compose                      |
| API ↔ App communication  | HTTP requests                       |
| Automated pipeline       | Apache Airflow                      |
| Schedule                 | Every 5 minutes                     |
| Repository               | Public GitHub repository            |

---

# Notes

The project uses the Iris dataset.

The generated processed datasets, MLflow database, Airflow runtime files, and packaged model are excluded from Git using `.gitignore`. They are recreated when the pipeline is executed.

