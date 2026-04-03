import math
from config.settings import RISK_DECAY_LAMBDA


def compute_accuracy(attempts, correct_attempts):
	if attempts == 0:
		return 0.5
	return correct_attempts / attempts


def compute_recency(current_time, last_seen_timestamp):
	time_diff = max(0, current_time - last_seen_timestamp)
	return min(1.0, math.exp(-RISK_DECAY_LAMBDA * time_diff))


def build_feature_vector(data, current_time):
	mastery = data["mastery"]
	confidence = data["confidence"]
	recency = compute_recency(current_time, data["last_seen_timestamp"])
	accuracy = compute_accuracy(data["attempts"], data["correct_attempts"])
	return [mastery, confidence, recency, accuracy]
