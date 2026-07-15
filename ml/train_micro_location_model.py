from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

from feature_engineering import (
    FEATURE_COLUMNS,
    aqi_category,
    build_feature_frame,
    clean_reference_rows,
    recommendation_for_category,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "public" / "aqi-data.json"
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    raw_rows = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    reference_frame = clean_reference_rows(raw_rows)

    feature_frame, targets = build_feature_frame(reference_frame, k=5)

    x_train, x_test, y_train, y_test = train_test_split(
        feature_frame,
        targets,
        test_size=0.2,
        random_state=42,
    )

    extra_trees = ExtraTreesRegressor(
        n_estimators=320,
        random_state=42,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        n_jobs=-1,
    )
    knn = KNeighborsRegressor(n_neighbors=7, weights="distance", metric="minkowski")

    extra_trees.fit(x_train, y_train)
    knn.fit(x_train, y_train)

    extra_pred = extra_trees.predict(x_test)
    knn_pred = knn.predict(x_test)
    blended_pred = (0.7 * extra_pred) + (0.3 * knn_pred)

    rmse = float(mean_squared_error(y_test, blended_pred) ** 0.5)
    mae = float(mean_absolute_error(y_test, blended_pred))
    r2 = float(r2_score(y_test, blended_pred))

    joblib.dump(extra_trees, ARTIFACT_DIR / "micro_location_extra_trees.joblib")
    joblib.dump(knn, ARTIFACT_DIR / "micro_location_knn.joblib")

    reference_payload = reference_frame.to_dict(orient="records")
    (ARTIFACT_DIR / "micro_location_reference.json").write_text(
        json.dumps(reference_payload, indent=2),
        encoding="utf-8",
    )

    metadata = {
        "trainedAt": datetime.now(timezone.utc).isoformat(),
        "sourceFile": str(SOURCE_FILE),
        "datasetSize": int(len(reference_frame)),
        "featureColumns": FEATURE_COLUMNS,
        "metrics": {
            "rmse": rmse,
            "mae": mae,
            "r2": r2,
        },
        "neighborCount": 5,
        "topFeatureImportances": sorted(
            (
                {"feature": name, "importance": float(score)}
                for name, score in zip(FEATURE_COLUMNS, extra_trees.feature_importances_)
            ),
            key=lambda item: item["importance"],
            reverse=True,
        ),
    }
    (ARTIFACT_DIR / "micro_location_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "trained",
                "metrics": metadata["metrics"],
                "artifacts": [
                    str(ARTIFACT_DIR / "micro_location_extra_trees.joblib"),
                    str(ARTIFACT_DIR / "micro_location_knn.joblib"),
                    str(ARTIFACT_DIR / "micro_location_reference.json"),
                    str(ARTIFACT_DIR / "micro_location_metadata.json"),
                ],
                "sampleCategory": aqi_category(float(reference_frame.iloc[0]["aqi"])),
                "sampleRecommendation": recommendation_for_category(aqi_category(float(reference_frame.iloc[0]["aqi"]))),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
