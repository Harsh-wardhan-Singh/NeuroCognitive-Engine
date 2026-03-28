import math

from engines.risk_engine.risk_model import (
    linear_combination,
    predict_probability,
    sigmoid,
)
from engines.risk_engine.utils import is_close


def test_sigmoid_zero():
    expected = 0.5
    output = sigmoid(0.0)
    print("Expected:", expected)
    print("Got:", output)
    assert is_close(output, expected)


def test_linear_combination_manual_case():
    features = [0.8, 0.7, 1.0, 0.9]
    expected = -4.4
    output = linear_combination(features)
    print("Expected:", expected)
    print("Got:", output)
    assert is_close(output, expected)


def test_predict_probability_matches_manual_value():
    features = [0.8, 0.7, 1.0, 0.9]
    expected = 1 / (1 + math.exp(4.4))
    output = predict_probability(features)
    print("Expected:", expected)
    print("Got:", output)
    assert is_close(output, expected)


def test_monotonicity_higher_mastery_lower_error():
    low_mastery_features = [0.2, 0.7, 1.0, 0.9]
    high_mastery_features = [0.8, 0.7, 1.0, 0.9]
    p_low_mastery = predict_probability(low_mastery_features)
    p_high_mastery = predict_probability(high_mastery_features)
    expected = True
    output = p_high_mastery < p_low_mastery
    print("Expected:", expected)
    print("Got:", output)
    assert output


def run_all():
    test_sigmoid_zero()
    test_linear_combination_manual_case()
    test_predict_probability_matches_manual_value()
    test_monotonicity_higher_mastery_lower_error()


if __name__ == "__main__":
    run_all()