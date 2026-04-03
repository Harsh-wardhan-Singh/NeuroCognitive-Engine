from pathlib import Path
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from orchestrator.utils import (
    build_concept_id,
    datetime_to_unix_timestamp,
    get_default_concepts,
    get_avg_time_for_concept,
    is_strong_concept,
    is_weak_concept,
    validate_num_questions,
    validate_submit_input,
)


def test_build_concept_id() -> None:
    output = build_concept_id("math", "algebra", "linear_equations")
    expected = "math.algebra.linear_equations"

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_validate_num_questions_valid() -> None:
    expected = "ok"
    actual = "ok"
    validate_num_questions(10)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def test_validate_submit_input_valid() -> None:
    expected = "ok"
    actual = "ok"
    validate_submit_input("B", 0.8, 4.2)

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def test_datetime_to_unix_timestamp_returns_float() -> None:
    output = datetime_to_unix_timestamp(datetime(2026, 4, 4, 10, 0, 0))
    expected = "float"
    actual = type(output).__name__

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def test_get_avg_time_config_lookup() -> None:
    output = get_avg_time_for_concept("math.algebra.linear_equations")
    expected = 45.0

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_get_default_concepts_lookup() -> None:
    output = get_default_concepts("math", "algebra")
    expected = ["linear_equations", "quadratic_equations"]

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def test_weak_and_strong_threshold_helpers() -> None:
    weak_output = is_weak_concept(0.4)
    strong_output = is_strong_concept(0.8)
    expected = {"weak": True, "strong": True}
    actual = {"weak": weak_output, "strong": strong_output}

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def run_all() -> None:
    test_build_concept_id()
    test_validate_num_questions_valid()
    test_validate_submit_input_valid()
    test_datetime_to_unix_timestamp_returns_float()
    test_get_avg_time_config_lookup()
    test_get_default_concepts_lookup()
    test_weak_and_strong_threshold_helpers()


if __name__ == "__main__":
    run_all()
