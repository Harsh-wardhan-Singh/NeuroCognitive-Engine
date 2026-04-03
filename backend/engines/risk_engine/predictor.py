from config.settings import RISK_HIGH_THRESHOLD, RISK_MEDIUM_THRESHOLD, RISK_TOLERANCE
from engines.risk_engine.feature_extractor import build_feature_vector
from engines.risk_engine.risk_model import predict_probability


def predict_risk(concept_data, current_time):
	features = build_feature_vector(concept_data, current_time)
	p_error = predict_probability(features)
	if p_error > RISK_HIGH_THRESHOLD + RISK_TOLERANCE:
		risk_level = "HIGH"
	elif p_error > RISK_MEDIUM_THRESHOLD + RISK_TOLERANCE:
		risk_level = "MEDIUM"
	else:
		risk_level = "LOW"
	return {
		"concept_id": concept_data["concept_id"],
		"p_error": p_error,
		"risk_level": risk_level,
		"features_used": {
			"mastery": features[0],
			"confidence": features[1],
			"recency": features[2],
			"accuracy": features[3],
		},
	}
