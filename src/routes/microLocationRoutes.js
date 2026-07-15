const express = require('express');
const { estimateMicroLocation } = require('../controllers/microLocationController');

const router = express.Router();

router.post('/estimate', estimateMicroLocation);

module.exports = router;
