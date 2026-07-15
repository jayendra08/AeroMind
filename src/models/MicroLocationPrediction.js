const mongoose = require('mongoose');

const driverSchema = new mongoose.Schema(
  {
    feature: { type: String, required: true },
    importance: { type: Number, required: true },
    value: { type: Number, required: true },
  },
  { _id: false }
);

const neighborSchema = new mongoose.Schema(
  {
    station: { type: String, required: true },
    state: { type: String, required: true },
    latitude: { type: Number, required: true },
    longitude: { type: Number, required: true },
    aqi: { type: Number, required: true },
    distance_km: { type: Number, required: true },
    pollution_load: { type: Number, required: true },
  },
  { _id: false }
);

const microLocationPredictionSchema = new mongoose.Schema(
  {
    latitude: { type: Number, required: true },
    longitude: { type: Number, required: true },
    timestamp: { type: String, required: true },
    estimatedAqi: { type: Number, required: true },
    category: { type: String, required: true },
    confidence: { type: Number, required: true },
    hotspotScore: { type: Number, required: true },
    uncertaintyBand: {
      lower: { type: Number, required: true },
      upper: { type: Number, required: true },
    },
    nearestStation: {
      name: { type: String, required: true },
      state: { type: String, required: true },
      distanceKm: { type: Number, required: true },
      aqi: { type: Number, required: true },
    },
    recommendation: { type: String, required: true },
    neighborSnapshot: { type: [neighborSchema], default: [] },
    drivers: { type: [driverSchema], default: [] },
    modelVersion: { type: String, required: true },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model('MicroLocationPrediction', microLocationPredictionSchema);
