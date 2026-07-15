const MicroLocationPrediction = require('../models/MicroLocationPrediction');
const { runPythonPrediction } = require('../services/pythonBridge');

function parseCoordinate(value, fieldName) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    throw new Error(`${fieldName} must be a valid number.`);
  }
  return parsed;
}

async function estimateMicroLocation(req, res, next) {
  try {
    const latitude = parseCoordinate(req.body.latitude, 'latitude');
    const longitude = parseCoordinate(req.body.longitude, 'longitude');
    const timestamp = req.body.timestamp || new Date().toISOString();
    const neighborCount = Number(req.body.neighborCount || 5);

    if (latitude < -90 || latitude > 90) {
      throw new Error('latitude must be between -90 and 90.');
    }

    if (longitude < -180 || longitude > 180) {
      throw new Error('longitude must be between -180 and 180.');
    }

    const prediction = await runPythonPrediction({
      latitude,
      longitude,
      timestamp,
      neighborCount,
    });

    const nearestStation = prediction.nearestStation || {};
    const safeNearestStation = {
      name: nearestStation.name || 'Nearest monitoring station',
      state: nearestStation.state || 'Unknown area',
      distanceKm: Number.isFinite(Number(nearestStation.distanceKm)) ? Number(nearestStation.distanceKm) : 0,
      aqi: Number.isFinite(Number(nearestStation.aqi)) ? Number(nearestStation.aqi) : 0,
    };

    if (MicroLocationPrediction.db && MicroLocationPrediction.db.readyState === 1) {
      MicroLocationPrediction.create({
        latitude,
        longitude,
        timestamp,
        estimatedAqi: prediction.estimatedAqi,
        category: prediction.category,
        confidence: prediction.confidence,
        hotspotScore: prediction.hotspotScore,
        uncertaintyBand: prediction.uncertaintyBand,
        nearestStation: safeNearestStation,
        recommendation: prediction.recommendation,
        neighborSnapshot: prediction.neighborSnapshot,
        drivers: prediction.drivers,
        modelVersion: prediction.modelVersion,
      }).catch((error) => {
        console.error('[mongo] Failed to persist micro-location prediction:', error.message);
      });
    }

    return res.json({
      ...prediction,
      nearestStation: safeNearestStation,
    });
  } catch (error) {
    return next(error);
  }
}

module.exports = { estimateMicroLocation };
