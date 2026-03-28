from engines.quiz_engine.utils import is_close


def test_is_close_true_case():
    expected = True
    output = is_close(0.30000001, 0.3)
    print("Expected:", expected)
    print("Got:", output)
    assert output is expected


def run_all():
    test_is_close_true_case()


if __name__ == "__main__":
    run_all()