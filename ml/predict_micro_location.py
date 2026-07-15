from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from feature_engineering import (
    FEATURE_COLUMNS,
    aqi_category,
    build_feature_row,
    clean_reference_rows,
    current_month_weekday,
    format_neighbors,
    recommendation_for_category,
)


ROOT = Path(__file__).resolve().parent
ARTIFACT_DIR = ROOT / "artifacts"
MODEL_EXTRA = ARTIFACT_DIR / "micro_location_extra_trees.joblib"
MODEL_KNN = ARTIFACT_DIR / "micro_location_knn.joblib"
REFERENCE_FILE = ARTIFACT_DIR / "micro_location_reference.json"
METADATA_FILE = ARTIFACT_DIR / "micro_location_metadata.json"


def load_reference_frame() -> pd.DataFrame:
    if not REFERENCE_FILE.exists():
        source_file = ROOT.parent / "public" / "aqi-data.json"
        raw_rows = json.loads(source_file.read_text(encoding="utf-8"))
        return clean_reference_rows(raw_rows)
    raw_reference = json.loads(REFERENCE_FILE.read_text(encoding="utf-8"))
    return pd.DataFrame(raw_reference)


def load_metadata() -> dict:
    if METADATA_FILE.exists():
        return json.loads(METADATA_FILE.read_text(encoding="utf-8"))
    return {"featureColumns": FEATURE_COLUMNS, "neighborCount": 5, "topFeatureImportances": []}


def main() -> None:
    if not MODEL_EXTRA.exists() or not MODEL_KNN.exists():
        print(
            json.dumps(
                {
                    "error": "Model artifacts are missing. Run ml/train_micro_location_model.py first.",
                }
            )
        )
        sys.exit(1)

    payload_raw = sys.stdin.read().strip() or "{}"
    payload = json.loads(payload_raw)
    latitude = float(payload.get("latitude"))
    longitude = float(payload.get("longitude"))
    timestamp_text = payload.get("timestamp")
    neighbor_count = int(payload.get("neighborCount") or 5)

    month, weekday = current_month_weekday(timestamp_text)
    reference_frame = load_reference_frame()
    metadata = load_metadata()

    extra_trees = joblib.load(MODEL_EXTRA)
    knn = joblib.load(MODEL_KNN)

    feature_row, neighbors = build_feature_row(
        reference_frame,
        latitude,
        longitude,
        month=month,
        weekday=weekday,
        k=neighbor_count,
    )

    feature_frame = pd.DataFrame([feature_row], columns=FEATURE_COLUMNS)
    tree_prediction = float(extra_trees.predict(feature_frame)[0])
    knn_prediction = float(knn.predict(feature_frame)[0])
    predicted_aqi = float((0.7 * tree_prediction) + (0.3 * knn_prediction))

    feature_array = feature_frame.to_numpy()
    tree_votes = np.array([estimator.predict(feature_array)[0] for estimator in extra_trees.estimators_], dtype=float)
    tree_std = float(tree_votes.std(ddof=0))
    neighbor_std = float(neighbors["aqi"].astype(float).std(ddof=0) or 0.0)
    nearest_distance = float(feature_row["distance_to_nearest_station"])

    spread = float(np.sqrt((0.65 * tree_std) ** 2 + (0.35 * neighbor_std) ** 2))
    distance_penalty = min(1.0, nearest_distance / 25.0)
    normalized_uncertainty = min(1.0, (spread / 90.0) + (distance_penalty * 0.35))
    confidence = round(max(0.05, 1.0 - normalized_uncertainty), 3)

    uncertainty_band = {
        "lower": max(0.0, round(predicted_aqi - (1.96 * spread), 2)),
        "upper": round(predicted_aqi + (1.96 * spread), 2),
    }

    category = aqi_category(predicted_aqi)
    hotspot_score = round(min(100.0, max(0.0, ((predicted_aqi - 50.0) / 250.0) * 100.0 + (1.0 - confidence) * 15.0)), 2)
    recommendation = recommendation_for_category(category)

    importance_map = {item["feature"]: item["importance"] for item in metadata.get("topFeatureImportances", [])}
    ranked_drivers = sorted(importance_map.items(), key=lambda item: item[1], reverse=True)[:6]
    local_drivers = [
        {
            "feature": feature_name,
            "importance": round(float(score), 6),
            "value": round(float(feature_row.get(feature_name, 0.0)), 4),
        }
        for feature_name, score in ranked_drivers
    ]

    response = {
        "status": "ok",
        "modelVersion": metadata.get("trainedAt", "unknown"),
        "location": {
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": timestamp_text or datetime.now(timezone.utc).isoformat(),
        },
        "estimatedAqi": round(predicted_aqi, 2),
        "category": category,
        "confidence": confidence,
        "hotspotScore": hotspot_score,
        "uncertaintyBand": uncertainty_band,
        "nearestStation": {
            "name": str(neighbors.iloc[0]["station"]),
            "state": str(neighbors.iloc[0]["state"]),
            "distanceKm": round(float(nearest_distance), 2),
            "aqi": round(float(neighbors.iloc[0]["aqi"]), 2),
        },
        "recommendation": recommendation,
        "neighborSnapshot": format_neighbors(neighbors),
        "drivers": local_drivers,
        "metrics": metadata.get("metrics", {}),
        "featureVector": feature_row,
    }

    print(json.dumps(response))


if __name__ == "__main__":
    main()
