import logging
from pathlib import Path
from typing import Any, Dict, Tuple

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_dataset(dataset_path: Path) -> pd.DataFrame:
    """Load the gender name dataset from a CSV file."""
    dataset = pd.read_csv(dataset_path)
    if "name" not in dataset.columns or "gender" not in dataset.columns:
        raise ValueError("Dataset must contain 'name' and 'gender' columns.")
    return dataset


def clean_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset by handling missing values and duplicates."""
    dataset = dataset.copy()
    dataset["name"] = dataset["name"].astype(str).str.strip()
    dataset["gender"] = dataset["gender"].astype(str).str.strip().str.lower()
    dataset = dataset[dataset["name"] != ""].dropna(subset=["name", "gender"])
    dataset = dataset.drop_duplicates(subset=["name", "gender"])  # preserve class label pairs
    return dataset


def build_pipeline(classifier: Any) -> Pipeline:
    """Build a text classification pipeline using character-level features."""
    vectorizer = CountVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    return Pipeline([("vectorizer", vectorizer), ("classifier", classifier)])


def train_models(x_train: pd.Series, y_train: pd.Series) -> Dict[str, Pipeline]:
    """Train candidate models and return trained pipelines."""
    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000, solver="liblinear"),
        "Naive Bayes": MultinomialNB(),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    }
    pipelines = {}
    for name, classifier in models.items():
        pipeline = build_pipeline(classifier)
        pipeline.fit(x_train, y_train)
        pipelines[name] = pipeline
        logging.info("Trained %s", name)
    return pipelines


def evaluate_model(pipeline: Pipeline, x_test: pd.Series, y_test: pd.Series) -> Dict[str, Any]:
    """Evaluate a trained model and return key metrics."""
    y_pred = pipeline.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, digits=4)
    matrix = confusion_matrix(y_test, y_pred, labels=pipeline.classes_)
    return {
        "accuracy": accuracy,
        "classification_report": report,
        "confusion_matrix": matrix,
        "labels": pipeline.classes_.tolist(),
    }


def save_best_model(model_object: Dict[str, Any], model_path: Path) -> None:
    """Save the selected model and encoder to disk."""
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_object, model_path)
    logging.info("Saved trained model to %s", model_path)


def save_classification_report(report_text: str, output_path: Path) -> None:
    """Save classification report text to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")
    logging.info("Saved classification report to %s", output_path)


def save_confusion_matrix(matrix: Any, labels: list[str], output_path: Path) -> None:
    """Save a confusion matrix figure to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 5))
    plt.imshow(matrix, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = range(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)

    thresh = matrix.max() / 2.0
    for i, j in [(i, j) for i in range(matrix.shape[0]) for j in range(matrix.shape[1])]:
        plt.text(j, i, str(matrix[i, j]), horizontalalignment="center",
                 color="white" if matrix[i, j] > thresh else "black")
    plt.ylabel("True label")
    plt.xlabel("Predicted label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()
    logging.info("Saved confusion matrix plot to %s", output_path)


def find_best_model(evaluations: Dict[str, Dict[str, Any]]) -> str:
    """Select the best model name based on accuracy."""
    return max(evaluations.items(), key=lambda item: item[1]["accuracy"])[0]


def main() -> None:
    base_path = Path(__file__).resolve().parents[1]
    dataset_path = base_path / "data" / "gender_dataset.csv"
    model_path = base_path / "models" / "gender_name_clf.joblib"
    report_path = base_path / "outputs" / "classification_report.txt"
    confusion_path = base_path / "outputs" / "confusion_matrix.png"

    dataset = load_dataset(dataset_path)
    dataset = clean_dataset(dataset)
    if dataset.empty:
        raise ValueError("No valid records found after cleaning the dataset.")

    x = dataset["name"].str.lower()
    y = dataset["gender"].str.lower()
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded,
    )

    pipelines = train_models(x_train, y_train)
    evaluations: dict[str, dict[str, Any]] = {}
    for name, pipeline in pipelines.items():
        evaluations[name] = evaluate_model(pipeline, x_test, y_test)
        logging.info(
            "%s accuracy: %.4f", name, evaluations[name]["accuracy"]
        )

    best_name = find_best_model(evaluations)
    best_pipeline = pipelines[best_name]
    logging.info("Best model selected: %s", best_name)

    model_object = {
        "pipeline": best_pipeline,
        "label_encoder": label_encoder,
    }
    save_best_model(model_object, model_path)
    save_classification_report(
        f"Best model: {best_name}\n\n" + evaluations[best_name]["classification_report"],
        report_path,
    )
    save_confusion_matrix(
        evaluations[best_name]["confusion_matrix"],
        label_encoder.inverse_transform(best_pipeline.classes_).tolist(),
        confusion_path,
    )

    logging.info("Training complete. Best model: %s", best_name)


if __name__ == "__main__":
    main()
