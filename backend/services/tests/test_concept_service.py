from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from services.concept_service import get_concepts


def test_get_concepts_uses_current_default_mapping() -> None:
    output = get_concepts("math", "algebra")
    expected = ["linear_equations", "quadratic_equations"]

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected


def run_all() -> None:
    test_get_concepts_uses_current_default_mapping()


if __name__ == "__main__":
    run_all()
