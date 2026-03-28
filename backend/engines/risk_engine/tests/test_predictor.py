import math

from engines.risk_engine.predictor import predict_risk
from engines.risk_engine.utils import is_close


def test_predictor_low_risk_case():
    concept_data = {
        "concept_id": "fractions_basic",
        "mastery": 0.8,
        "confidence": 0.7,
        "last_seen_timestamp": 1000.0,
        "attempts": 10,
        "correct_attempts": 9,
    }
    output = predict_risk(concept_data, current_time=1000.0)
    expected = "LOW"
    print("Expected:", expected)
    print("Got:", output["risk_level"])
    assert output["risk_level"] == expected


def test_predictor_output_features_values():
    concept_data = {
        "concept_id": "fractions_basic",
        "mastery": 0.72,
        "confidence": 0.41,
        "last_seen_timestamp": 1000.0,
        "attempts": 5,
        "correct_attempts": 3,
    }
    output = predict_risk(concept_data, current_time=1010.0)

    expected_mastery = 0.72
    expected_confidence = 0.41
    expected_recency = math.exp(-0.001 * 10)
    expected_accuracy = 0.6

    print("Expected:", expected_mastery)
    print("Got:", output["features_used"]["mastery"])
    assert is_close(output["features_used"]["mastery"], expected_mastery)

    print("Expected:", expected_confidence)
    print("Got:", output["features_used"]["confidence"])
    assert is_close(output["features_used"]["confidence"], expected_confidence)

    print("Expected:", expected_recency)
    print("Got:", output["features_used"]["recency"])
    assert is_close(output["features_used"]["recency"], expected_recency)

    print("Expected:", expected_accuracy)
    print("Got:", output["features_used"]["accuracy"])
    assert is_close(output["features_used"]["accuracy"], expected_accuracy)


def run_all():
    test_predictor_low_risk_case()
    test_predictor_output_features_values()


if __name__ == "__main__":
    run_all()