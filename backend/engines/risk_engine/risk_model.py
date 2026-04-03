import math
from config.settings import (
	RISK_BIAS,
	RISK_WEIGHT_ACCURACY,
	RISK_WEIGHT_CONFIDENCE,
	RISK_WEIGHT_MASTERY,
	RISK_WEIGHT_RECENCY,
)


def linear_combination(features):
	mastery, confidence, recency, accuracy = features
	return (
		mastery * RISK_WEIGHT_MASTERY
		+ confidence * RISK_WEIGHT_CONFIDENCE
		+ recency * RISK_WEIGHT_RECENCY
		+ accuracy * RISK_WEIGHT_ACCURACY
		+ RISK_BIAS
	)


def sigmoid(z):
	return 1 / (1 + math.exp(-z))


def predict_probability(features):
	z = linear_combination(features)
	return sigmoid(z)