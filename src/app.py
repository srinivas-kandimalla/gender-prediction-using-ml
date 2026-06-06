from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request
import joblib


def create_app() -> Flask:
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    model_path = Path(__file__).resolve().parents[1] / "models" / "gender_name_clf.joblib"
    model_object = load_model(model_path)

    @app.route("/")
    def index() -> Any:
        return render_template("index.html")

    @app.route("/api/predict", methods=["POST"])
    def api_predict() -> Any:
        payload = request.get_json(silent=True)
        if not payload or "name" not in payload:
            return jsonify({"error": "Request body must contain a 'name' field."}), 400

        name = str(payload.get("name", "")).strip()
        if not name:
            return jsonify({"error": "Name must not be empty."}), 400

        try:
            result = predict_gender(name, model_object)
            return jsonify(result)
        except Exception as err:
            return jsonify({"error": str(err)}), 500

    return app


def load_model(model_path: Path) -> Any:
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(model_path)


def predict_gender(name: str, model_object: Any) -> dict[str, Any]:
    processed_name = name.strip().lower()
    pipeline = model_object["pipeline"]
    label_encoder = model_object["label_encoder"]
    predicted_label = pipeline.predict([processed_name])[0]
    confidence = 1.0
    if hasattr(pipeline, "predict_proba"):
        probabilities = pipeline.predict_proba([processed_name])[0]
        best_index = int(predicted_label)
        confidence = float(probabilities[best_index])

    predicted_gender = label_encoder.inverse_transform([predicted_label])[0]
    return {
        "name": name,
        "predicted_gender": predicted_gender,
        "confidence": round(confidence, 4),
    }


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
