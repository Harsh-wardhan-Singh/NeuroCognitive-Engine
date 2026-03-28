from engines.quiz_engine.exploration import should_explore
from engines.quiz_engine.utils import choose_random_concept


def compute_priority_score(concept, risk):
	mastery = concept["mastery"]
	confidence = concept["confidence"]
	p_error = risk["p_error"]
	return (1 - mastery) * 0.5 + p_error * 0.3 + (1 - confidence) * 0.2


def select_concept(concepts, risks, session_state):
	recent_concepts = session_state.get("recent_concepts", [])
	last_concept = session_state.get("last_concept")

	scored_concepts = []
	for concept in concepts:
		concept_id = concept["concept_id"]
		risk = risks[concept_id]
		score = compute_priority_score(concept, risk)
		if concept_id in recent_concepts:
			score *= 0.8
		scored_concepts.append((concept, risk, score))

	filtered = []
	for concept, risk, score in scored_concepts:
		if concept["concept_id"] == last_concept and risk["risk_level"] != "HIGH":
			continue
		filtered.append((concept, risk, score))

	candidates = filtered if filtered else scored_concepts

	if should_explore(0.15):
		concept_list = [concept for concept, _, _ in candidates]
		selected = choose_random_concept(concept_list)
		return selected, "exploration"

	selected_concept, selected_risk, _ = max(candidates, key=lambda item: item[2])
	if selected_risk["risk_level"] == "HIGH":
		reason = "high_risk_intervention"
	else:
		reason = "low_mastery_exploit"
	return selected_concept, reason
