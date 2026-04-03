import math
from config.settings import DECAY_RATE


def apply_decay(
	mastery: float,
	last_seen_timestamp: float,
	current_time: float,
	decay_rate: float = DECAY_RATE,
) -> float:
	time_diff = max(0.0, current_time - last_seen_timestamp)
	decayed_mastery = mastery * math.exp(-decay_rate * time_diff)
	return decayed_mastery
