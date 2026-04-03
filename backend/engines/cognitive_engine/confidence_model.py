def update_confidence(
    previous_confidence: float,
    reported_confidence: float,
    correctness: bool,
    response_time: float,
    avg_time: float,
) -> float:
    # Ground truth
    target = 1.0 if correctness else 0.0
    # Calibration error
    calibration_error = target - reported_confidence
    # Speed factor (faster = more confident)
    speed_factor = max(0.5, min(1.5, avg_time / (response_time + 1e-5)))
    # Adaptive learning rate
    lr = 0.05 + 0.05 * abs(calibration_error)
    # Update
    delta = lr * calibration_error * speed_factor
    new_confidence = previous_confidence + delta
    return max(0.0, min(1.0, new_confidence))