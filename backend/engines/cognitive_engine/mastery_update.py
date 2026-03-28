def update_mastery(
	prior_mastery: float,
	is_correct: bool,
	slip: float,
	guess: float,
	learn: float,
) -> float:
	if is_correct:
		posterior = (prior_mastery * (1 - slip)) / (
			prior_mastery * (1 - slip) + (1 - prior_mastery) * guess
		)
	else:
		posterior = (prior_mastery * slip) / (
			prior_mastery * slip + (1 - prior_mastery) * (1 - guess)
		)

	new_mastery = posterior + (1 - posterior) * learn
	return max(0.0, min(1.0, new_mastery))
