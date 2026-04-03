from config.settings import (
    CONFIDENCE_ADAPTIVE_LR,
    CONFIDENCE_BASE_LR,
    CONFIDENCE_EPSILON,
    CONFIDENCE_SPEED_MAX,
    CONFIDENCE_SPEED_MIN,
)


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
    speed_factor = max(CONFIDENCE_SPEED_MIN, min(CONFIDENCE_SPEED_MAX, avg_time / (response_time + CONFIDENCE_EPSILON)))
    # Adaptive learning rate
    lr = CONFIDENCE_BASE_LR + CONFIDENCE_ADAPTIVE_LR * abs(calibration_error)
    # Update
    delta = lr * calibration_error * speed_factor
    new_confidence = previous_confidence + delta
    return max(0.0, min(1.0, new_confidence))