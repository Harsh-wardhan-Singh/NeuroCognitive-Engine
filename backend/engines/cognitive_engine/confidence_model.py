def update_confidence(
	previous_confidence: float,
	reported_confidence: float,
	correctness: bool,
) -> float:
	target = 1 if correctness else 0
	error = target - reported_confidence
	new_confidence = previous_confidence + 0.1 * error
	return max(0.0, min(1.0, new_confidence))
