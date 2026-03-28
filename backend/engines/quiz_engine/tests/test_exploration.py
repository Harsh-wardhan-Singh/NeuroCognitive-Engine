import random

from engines.quiz_engine.exploration import should_explore
from engines.quiz_engine.utils import is_close


def test_exploration_rate_approximate():
    random.seed(42)
    runs = 10000
    explore_count = 0
    for _ in range(runs):
        if should_explore(0.15):
            explore_count += 1

    output_rate = explore_count / runs
    expected_rate = 0.15
    print("Expected:", expected_rate)
    print("Got:", output_rate)
    assert is_close(output_rate, expected_rate, tol=0.02)


def test_explore_always_when_epsilon_one():
    random.seed(1)
    expected = True
    output = should_explore(1.0)
    print("Expected:", expected)
    print("Got:", output)
    assert output is expected


def run_all():
    test_exploration_rate_approximate()
    test_explore_always_when_epsilon_one()


if __name__ == "__main__":
    run_all()