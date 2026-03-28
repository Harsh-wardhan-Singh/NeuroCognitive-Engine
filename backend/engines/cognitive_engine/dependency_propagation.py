def propagate_mastery(
	concept_id: str,
	mastery: float,
	concept_graph: dict,
) -> dict:
	propagation_factor = 0.8
	dependents = concept_graph.get(concept_id, [])
	return {
		dependent: propagation_factor * mastery
		for dependent in dependents
	}
