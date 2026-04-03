from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from config.settings import (
    DECAY_RATE,
    DEFAULT_AVG_RESPONSE_TIME,
    GUESS_PROB,
    LEARNING_RATE,
    MAX_QUESTION_HISTORY,
    PASSWORD_MIN_LENGTH,
    SLIP_PROB,
)


def test_core_settings_values() -> None:
    expected = {
        "DECAY_RATE": 0.1,
        "LEARNING_RATE": 0.2,
        "SLIP_PROB": 0.1,
        "GUESS_PROB": 0.2,
        "DEFAULT_AVG_RESPONSE_TIME": 30.0,
        "MAX_QUESTION_HISTORY": 15,
        "PASSWORD_MIN_LENGTH": 8,
    }
    actual = {
        "DECAY_RATE": DECAY_RATE,
        "LEARNING_RATE": LEARNING_RATE,
        "SLIP_PROB": SLIP_PROB,
        "GUESS_PROB": GUESS_PROB,
        "DEFAULT_AVG_RESPONSE_TIME": DEFAULT_AVG_RESPONSE_TIME,
        "MAX_QUESTION_HISTORY": MAX_QUESTION_HISTORY,
        "PASSWORD_MIN_LENGTH": PASSWORD_MIN_LENGTH,
    }

    print("Expected:", expected)
    print("Got:", actual)
    assert actual == expected


def run_all() -> None:
    test_core_settings_values()


if __name__ == "__main__":
    run_all()
