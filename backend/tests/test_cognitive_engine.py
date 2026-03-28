from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engines.cognitive_engine.mastery_update import update_mastery
from engines.cognitive_engine.retention_decay import apply_decay
from engines.cognitive_engine.confidence_model import update_confidence
from engines.cognitive_engine.dependency_propagation import propagate_mastery


def test_update_mastery_spec_case() -> None:
	expected = 0.86
	output = update_mastery(
		prior_mastery=0.5,
		is_correct=True,
		slip=0.1,
		guess=0.2,
		learn=0.1,
	)

	print("Expected:", expected)
	print("Got:", output)
	assert abs(output - expected) < 0.03


def test_apply_decay_spec_case() -> None:
	expected = 0.48
	output = apply_decay(
		mastery=0.8,
		last_seen_timestamp=0.0,
		current_time=10.0,
		decay_rate=0.05,
	)

	print("Expected:", expected)
	print("Got:", output)
	assert abs(output - expected) < 0.01


def test_update_confidence_spec_case() -> None:
	expected = 0.42
	output = update_confidence(
		previous_confidence=0.5,
		reported_confidence=0.8,
		correctness=False,
	)

	print("Expected:", expected)
	print("Got:", output)
	assert abs(output - expected) < 1e-9


def test_propagate_mastery_spec_case() -> None:
	concept_graph = {
		"A": ["B", "C"],
		"B": ["D"],
		"C": [],
		"D": [],
	}
	expected = {"B": 0.72, "C": 0.72}
	output = propagate_mastery(
		concept_id="A",
		mastery=0.9,
		concept_graph=concept_graph,
	)

	print("Expected:", expected)
	print("Got:", output)
	assert set(output.keys()) == set(expected.keys())
	for key in expected:
		assert abs(output[key] - expected[key]) < 1e-9


def run_all_cognitive_engine_tests() -> None:
	test_update_mastery_spec_case()
	test_apply_decay_spec_case()
	test_update_confidence_spec_case()
	test_propagate_mastery_spec_case()


if __name__ == "__main__":
	run_all_cognitive_engine_tests()
