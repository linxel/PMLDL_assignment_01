from pathlib import Path
import joblib
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def run_model_engineering():
    base_dir = Path(__file__).resolve().parents[2]
    processed_dir = base_dir / "data" / "processed"
    models_dir = base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    train_df = pd.read_csv(processed_dir / "train.csv")
    test_df = pd.read_csv(processed_dir / "test.csv")

    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    target = "target"

    x_train, y_train = train_df[features], train_df[target]
    x_test, y_test = test_df[features], test_df[target]

    mlflow.set_tracking_uri((base_dir / "mlruns").as_uri())
    mlflow.set_experiment("iris_training_pipeline")
    with mlflow.start_run():
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier(n_estimators=20, random_state=42)),
        ])
        pipeline.fit(x_train, y_train)

    predictions = pipeline.predict(x_test)
    acc = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average="weighted")

    mlflow.log_param("n_estimators", 20)
    mlflow.log_metric("accuracy", float(acc))
    mlflow.log_metric("f1_weighted", float(f1))

    # Model packaging
    model_artifact_path = models_dir / "model.joblib"
    joblib.dump(pipeline, model_artifact_path)
    mlflow.log_artifact(str(model_artifact_path))


if __name__ == "__main__":
    run_model_engineering()
