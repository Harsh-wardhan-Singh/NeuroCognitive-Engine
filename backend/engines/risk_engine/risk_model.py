import math


def linear_combination(features):
	mastery, confidence, recency, accuracy = features
	return (
		mastery * -2.0
		+ confidence * -1.5
		+ recency * -1.0
		+ accuracy * -2.5
		+ 1.5
	)


def sigmoid(z):
	return 1 / (1 + math.exp(-z))


def predict_probability(features):
	z = linear_combination(features)
	return sigmoid(z)
