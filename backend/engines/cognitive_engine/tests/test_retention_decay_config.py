from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from engines.cognitive_engine.retention_decay import apply_decay


def test_apply_decay_uses_default_config_rate() -> None:
    output = apply_decay(mastery=0.8, last_seen_timestamp=0.0, current_time=10.0)
    expected = 0.2943035529371539

    print("Expected:", expected)
    print("Got:", output)
    assert abs(output - expected) < 1e-12


def run_all() -> None:
    test_apply_decay_uses_default_config_rate()


if __name__ == "__main__":
    run_all()
