import math

from engines.risk_engine.feature_extractor import (
    build_feature_vector,
    compute_accuracy,
    compute_recency,
)
from engines.risk_engine.utils import is_close


def test_compute_accuracy_normal():
    expected = 0.6
    output = compute_accuracy(5, 3)
    print("Expected:", expected)
    print("Got:", output)
    assert is_close(output, expected)


def test_compute_accuracy_zero_attempts():
    expected = 0.5
    output = compute_accuracy(0, 0)
    print("Expected:", expected)
    print("Got:", output)
    assert is_close(output, expected)


def test_compute_recency_decay_behavior():
    expected = math.exp(-0.001 * 1000)
    output = compute_recency(2000.0, 1000.0)
    print("Expected:", expected)
    print("Got:", output)
    assert is_close(output, expected)


def test_compute_recency_clamped_non_negative():
    expected = 1.0
    output = compute_recency(100.0, 120.0)
    print("Expected:", expected)
    print("Got:", output)
    assert is_close(output, expected)


def test_build_feature_vector_order_and_values():
    data = {
        "concept_id": "fractions_basic",
        "mastery": 0.72,
        "confidence": 0.41,
        "last_seen_timestamp": 1000.0,
        "attempts": 5,
        "correct_attempts": 3,
    }
    expected = [0.72, 0.41, math.exp(-0.001 * 10), 0.6]
    output = build_feature_vector(data, 1010.0)
    print("Expected:", expected)
    print("Got:", output)
    assert len(output) == 4
    for index in range(4):
        assert is_close(output[index], expected[index])


def run_all():
    test_compute_accuracy_normal()
    test_compute_accuracy_zero_attempts()
    test_compute_recency_decay_behavior()
    test_compute_recency_clamped_non_negative()
    test_build_feature_vector_order_and_values()


if __name__ == "__main__":
    run_all()