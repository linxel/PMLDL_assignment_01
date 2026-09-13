import os
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split


def run_data_engineering():
    base_dir = Path(__file__).resolve().parents[2]
    raw_path = base_dir / "data" / "raw" / "iris.csv"
    processed_dir = base_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path)

    # Clean missing values
    df = df.dropna()

    # Outlier removal via IQR for feature columns: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    for col in features:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    # Train / Test split
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["target"]
    )

    train_df.to_csv(processed_dir / "train.csv", index=False)
    test_df.to_csv(processed_dir / "test.csv", index=False)


if __name__ == "__main__":
    run_data_engineering()
