import argparse
from pathlib import Path
from typing import Any

import joblib


def load_model(model_path: Path) -> Any:
    """Load the trained model object from disk."""
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)


def predict_gender(name: str, model_object: Any) -> dict[str, Any]:
    """Predict gender and confidence for a given name."""
    text = name.strip()
    if not text:
        raise ValueError("Name must not be empty.")

    pipeline = model_object["pipeline"]
    label_encoder = model_object["label_encoder"]
    processed_name = text.lower()
    predicted_label = pipeline.predict([processed_name])[0]

    confidence = 1.0
    if hasattr(pipeline, "predict_proba"):
        probabilities = pipeline.predict_proba([processed_name])[0]
        best_index = int(predicted_label)
        confidence = float(probabilities[best_index])

    predicted_gender = label_encoder.inverse_transform([predicted_label])[0]
    return {
        "name": text,
        "predicted_gender": predicted_gender,
        "confidence": confidence,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict gender from a first name using a trained ML model."
    )
    parser.add_argument("name", help="First name to predict gender for.")
    args = parser.parse_args()

    model_path = Path(__file__).resolve().parents[1] / "models" / "gender_name_clf.joblib"
    model_object = load_model(model_path)
    result = predict_gender(args.name, model_object)

    print(f"Name: {result['name'].title()}")
    print(f"Predicted Gender: {result['predicted_gender'].title()}")
    print(f"Confidence: {result['confidence'] * 100:.1f}%")


if __name__ == "__main__":
    main()
