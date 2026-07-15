from __future__ import annotations

import math
from collections import Counter
from datetime import datetime
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd

AQI_CATEGORIES = [
    (0, 50, "Good"),
    (51, 100, "Satisfactory"),
    (101, 200, "Moderate"),
    (201, 300, "Poor"),
    (301, 400, "Very Poor"),
    (401, 500, "Severe"),
]

AQI_BREAKPOINTS = {
    "pm25": [
        (0, 30, 0, 50),
        (31, 60, 51, 100),
        (61, 90, 101, 200),
        (91, 120, 201, 300),
        (121, 250, 301, 400),
        (251, 500, 401, 500),
    ],
    "pm10": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 250, 101, 200),
        (251, 350, 201, 300),
        (351, 430, 301, 400),
        (431, 1000, 401, 500),
    ],
    "no2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 180, 101, 200),
        (181, 280, 201, 300),
        (281, 400, 301, 400),
        (401, 1000, 401, 500),
    ],
    "so2": [
        (0, 40, 0, 50),
        (41, 80, 51, 100),
        (81, 380, 101, 200),
        (381, 800, 201, 300),
        (801, 1600, 301, 400),
        (1601, 3000, 401, 500),
    ],
    "o3": [
        (0, 50, 0, 50),
        (51, 100, 51, 100),
        (101, 168, 101, 200),
        (169, 208, 201, 300),
        (209, 748, 301, 400),
        (749, 1000, 401, 500),
    ],
    "co": [
        (0, 1.0, 0, 50),
        (1.1, 2.0, 51, 100),
        (2.1, 10.0, 101, 200),
        (10.1, 17.0, 201, 300),
        (17.1, 34.0, 301, 400),
        (34.1, 50.0, 401, 500),
    ],
}

FEATURE_COLUMNS = [
    "latitude",
    "longitude",
    "month",
    "weekday",
    "is_weekend",
    "distance_to_nearest_station",
    "avg_distance_km",
    "neighbor_count",
    "neighbor_aqi_mean",
    "neighbor_aqi_std",
    "neighbor_pm25_mean",
    "neighbor_pm10_mean",
    "neighbor_no2_mean",
    "neighbor_so2_mean",
    "neighbor_o3_mean",
    "neighbor_co_mean",
    "neighbor_rh_mean",
    "neighbor_ws_mean",
    "neighbor_aod_mean",
    "neighbor_pollution_load_mean",
    "neighbor_traffic_signature_mean",
    "neighbor_cluster_mode",
]


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, str) and value.strip() in {"", "-", "NA", "null"}:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius_km = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    return 2 * radius_km * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def aqi_category(aqi: float) -> str:
    for low, high, label in AQI_CATEGORIES:
        if low <= aqi <= high:
            return label
    return "Severe"


def pollutant_sub_index(value: float, breakpoints: Sequence[Tuple[float, float, float, float]]) -> float:
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= value <= c_high:
            return ((i_high - i_low) / (c_high - c_low)) * (value - c_low) + i_low
    if value > breakpoints[-1][1]:
        _, c_high, _, i_high = breakpoints[-1]
        return i_high + min(100.0, (value - c_high) * 0.08)
    return 0.0


def compute_aqi_from_record(record: Dict[str, Any]) -> float:
    candidates = []
    mapping = {
        "pm25": "PM2.5",
        "pm10": "PM10",
        "no2": "NO2",
        "so2": "SO2",
        "o3": "Ozone",
        "co": "CO",
    }
    for pollutant_key, record_key in mapping.items():
        value = safe_float(record.get(record_key), 0.0)
        breakpoints = AQI_BREAKPOINTS[pollutant_key]
        candidates.append(pollutant_sub_index(value, breakpoints))

    return round(max(candidates) if candidates else 0.0, 2)


def parse_datetime_fields(record: Dict[str, Any]) -> Tuple[int, int, int]:
    date_text = str(record.get("From Date") or "")
    try:
        parsed = datetime.fromisoformat(date_text.split(" ")[0])
    except ValueError:
        parsed = datetime.utcnow()
    return parsed.month, parsed.weekday(), 1 if parsed.weekday() >= 5 else 0


def pollution_load(record: Dict[str, Any]) -> float:
    pm25 = safe_float(record.get("PM2.5"), 0.0)
    pm10 = safe_float(record.get("PM10"), 0.0)
    no2 = safe_float(record.get("NO2"), 0.0)
    so2 = safe_float(record.get("SO2"), 0.0)
    o3 = safe_float(record.get("Ozone"), 0.0)
    co = safe_float(record.get("CO"), 0.0)
    return round((pm25 / 100.0) + (pm10 / 150.0) + (no2 / 80.0) + (so2 / 40.0) + (o3 / 60.0) + (co / 4.0), 4)


def traffic_signature(record: Dict[str, Any]) -> float:
    return round(safe_float(record.get("NO"), 0.0) + safe_float(record.get("NO2"), 0.0) + safe_float(record.get("NOx"), 0.0), 4)


def clean_reference_rows(rows: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    cleaned_rows: List[Dict[str, Any]] = []
    for row_id, row in enumerate(rows):
        latitude = safe_float(row.get("Latitude"), np.nan)
        longitude = safe_float(row.get("Longitude"), np.nan)
        if np.isnan(latitude) or np.isnan(longitude):
            continue

        month, weekday, is_weekend = parse_datetime_fields(row)
        aqi_value = compute_aqi_from_record(row)

        cleaned_rows.append(
            {
                "row_id": row_id,
                "latitude": latitude,
                "longitude": longitude,
                "month": month,
                "weekday": weekday,
                "is_weekend": is_weekend,
                "aqi": aqi_value,
                "pm25": safe_float(row.get("PM2.5"), 0.0),
                "pm10": safe_float(row.get("PM10"), 0.0),
                "no": safe_float(row.get("NO"), 0.0),
                "no2": safe_float(row.get("NO2"), 0.0),
                "nox": safe_float(row.get("NOx"), 0.0),
                "nh3": safe_float(row.get("NH3"), 0.0),
                "so2": safe_float(row.get("SO2"), 0.0),
                "co": safe_float(row.get("CO"), 0.0),
                "o3": safe_float(row.get("Ozone"), 0.0),
                "benzene": safe_float(row.get("Benzene"), 0.0),
                "toluene": safe_float(row.get("Toluene"), 0.0),
                "ethyl_benzene": safe_float(row.get("Eth-Benzene"), 0.0),
                "m_p_xylene": safe_float(row.get("MP-Xylene"), 0.0),
                "o_xylene": safe_float(row.get("O-Xylene"), 0.0),
                "rh": safe_float(row.get("RH"), 0.0),
                "ws": safe_float(row.get("WS"), 0.0),
                "wd": safe_float(row.get("WD"), 0.0),
                "sr": safe_float(row.get("SR"), 0.0),
                "bp": safe_float(row.get("BP"), 0.0),
                "vws": safe_float(row.get("VWS"), 0.0),
                "aod": safe_float(row.get("AOD"), 0.0),
                "rh_merra": safe_float(row.get("RH_MERRA"), 0.0),
                "ws_merra": safe_float(row.get("WS_MERRA"), 0.0),
                "t_merra": safe_float(row.get("T_MERRA"), 0.0),
                "cluster": safe_float(row.get("Cluster"), 0.0),
                "state": str(row.get("State") or "Unknown"),
                "station": str(row.get("Station") or f"Station {row_id}"),
                "pincode": str(row.get("Pincode") or ""),
                "pollution_load": pollution_load(row),
                "traffic_signature": traffic_signature(row),
            }
        )

    frame = pd.DataFrame(cleaned_rows)
    if frame.empty:
        raise ValueError("No valid AQI rows found in the source dataset.")
    return frame


def nearest_neighbors(reference_frame: pd.DataFrame, latitude: float, longitude: float, k: int = 5, exclude_row_id: int | None = None) -> pd.DataFrame:
    if reference_frame.empty:
        raise ValueError("Reference frame is empty.")

    distances = reference_frame.apply(
        lambda row: haversine_km(latitude, longitude, float(row["latitude"]), float(row["longitude"])),
        axis=1,
    )
    ranked = reference_frame.assign(distance_km=distances)
    if exclude_row_id is not None:
        ranked = ranked[ranked["row_id"] != exclude_row_id]

    return ranked.sort_values("distance_km").head(k).copy()


def build_feature_row(
    reference_frame: pd.DataFrame,
    latitude: float,
    longitude: float,
    *,
    month: int,
    weekday: int,
    k: int = 5,
    exclude_row_id: int | None = None,
) -> Tuple[Dict[str, float], pd.DataFrame]:
    neighbors = nearest_neighbors(reference_frame, latitude, longitude, k=k, exclude_row_id=exclude_row_id)
    if neighbors.empty:
        raise ValueError("At least one neighbor is required for micro-location estimation.")

    nearest_distance = float(neighbors.iloc[0]["distance_km"])
    distances = neighbors["distance_km"].astype(float).to_numpy()
    weights = 1.0 / np.maximum(distances, 0.15)
    weights = weights / weights.sum()

    def weighted_mean(column: str) -> float:
        values = neighbors[column].astype(float).to_numpy()
        return float(np.sum(values * weights))

    def simple_mean(column: str) -> float:
        return float(neighbors[column].astype(float).mean())

    def safe_mode(column: str) -> float:
        series = neighbors[column].astype(float).round().astype(int).tolist()
        if not series:
            return 0.0
        return float(Counter(series).most_common(1)[0][0])

    feature_row = {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "month": float(month),
        "weekday": float(weekday),
        "is_weekend": float(1 if weekday >= 5 else 0),
        "distance_to_nearest_station": nearest_distance,
        "avg_distance_km": float(neighbors["distance_km"].mean()),
        "neighbor_count": float(len(neighbors)),
        "neighbor_aqi_mean": simple_mean("aqi"),
        "neighbor_aqi_std": float(neighbors["aqi"].astype(float).std(ddof=0) or 0.0),
        "neighbor_pm25_mean": weighted_mean("pm25"),
        "neighbor_pm10_mean": weighted_mean("pm10"),
        "neighbor_no2_mean": weighted_mean("no2"),
        "neighbor_so2_mean": weighted_mean("so2"),
        "neighbor_o3_mean": weighted_mean("o3"),
        "neighbor_co_mean": weighted_mean("co"),
        "neighbor_rh_mean": weighted_mean("rh"),
        "neighbor_ws_mean": weighted_mean("ws"),
        "neighbor_aod_mean": weighted_mean("aod"),
        "neighbor_pollution_load_mean": weighted_mean("pollution_load"),
        "neighbor_traffic_signature_mean": weighted_mean("traffic_signature"),
        "neighbor_cluster_mode": safe_mode("cluster"),
    }

    return feature_row, neighbors


def format_neighbors(neighbors: pd.DataFrame) -> List[Dict[str, Any]]:
    formatted: List[Dict[str, Any]] = []
    for _, row in neighbors.iterrows():
        formatted.append(
            {
                "station": row["station"],
                "state": row["state"],
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "aqi": float(row["aqi"]),
                "distance_km": round(float(row["distance_km"]), 2),
                "pollution_load": float(row["pollution_load"]),
            }
        )
    return formatted


def build_feature_frame(reference_frame: pd.DataFrame, k: int = 5) -> Tuple[pd.DataFrame, pd.Series]:
    feature_rows: List[Dict[str, float]] = []
    targets: List[float] = []

    for _, row in reference_frame.iterrows():
        feature_row, _ = build_feature_row(
            reference_frame,
            float(row["latitude"]),
            float(row["longitude"]),
            month=int(row["month"]),
            weekday=int(row["weekday"]),
            k=k,
            exclude_row_id=int(row["row_id"]),
        )
        feature_rows.append(feature_row)
        targets.append(float(row["aqi"]))

    feature_frame = pd.DataFrame(feature_rows, columns=FEATURE_COLUMNS)
    target_series = pd.Series(targets, name="aqi")
    return feature_frame, target_series


def current_month_weekday(timestamp_text: str | None = None) -> Tuple[int, int]:
    if timestamp_text:
        try:
            parsed = datetime.fromisoformat(timestamp_text.replace("Z", "+00:00"))
            return parsed.month, parsed.weekday()
        except ValueError:
            pass
    now = datetime.utcnow()
    return now.month, now.weekday()


def recommendation_for_category(category: str) -> str:
    messages = {
        "Good": "Air quality is favorable. Outdoor activity is safe, and this location can serve as a low-exposure corridor.",
        "Satisfactory": "Air quality is acceptable. Sensitive groups should still watch for localized exposure pockets.",
        "Moderate": "Limit long outdoor exercise and consider alternative routes for children, seniors, or asthma patients.",
        "Poor": "Avoid prolonged outdoor exposure and use air filtration indoors if possible.",
        "Very Poor": "High exposure risk. Prioritize indoor activities and mask use for unavoidable travel.",
        "Severe": "Emergency-level exposure. Avoid outdoor movement unless absolutely necessary.",
    }
    return messages.get(category, "Review the local AQI before stepping out.")
