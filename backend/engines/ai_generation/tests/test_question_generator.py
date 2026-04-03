import engines.ai_generation.question_generator as question_generator


def test_generate_question_probability_easy():
    original_generate_text = question_generator.generate_text
    original_queue = list(question_generator.RECENT_QUESTIONS_QUEUE)
    question_generator.RECENT_QUESTIONS_QUEUE.clear()

    def mock_generate_text(prompt, temperature, max_tokens):
        return (
            '{"question":"What is the probability of getting heads on a fair coin toss?",'
            '"options":["0","0.25","0.5","1"],'
            '"correct_answer":"0.5"}'
        )

    question_generator.generate_text = mock_generate_text

    output = question_generator.generate_question("Probability", "EASY")
    expected = {
        "question": "What is the probability of getting heads on a fair coin toss?",
        "options": ["0", "0.25", "0.5", "1"],
        "correct_answer": "0.5",
    }

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    expected_queue = ["What is the probability of getting heads on a fair coin toss?"]
    actual_queue = list(question_generator.RECENT_QUESTIONS_QUEUE)
    print("Expected:", expected_queue)
    print("Got:", actual_queue)
    assert actual_queue == expected_queue

    question_generator.RECENT_QUESTIONS_QUEUE.clear()
    question_generator.RECENT_QUESTIONS_QUEUE.extend(original_queue)
    question_generator.generate_text = original_generate_text


def test_generate_question_algebra_hard():
    original_generate_text = question_generator.generate_text
    original_queue = list(question_generator.RECENT_QUESTIONS_QUEUE)
    question_generator.RECENT_QUESTIONS_QUEUE.clear()

    def mock_generate_text(prompt, temperature, max_tokens):
        return (
            '{"question":"If x^2 - 5x + 6 = 0, what is the larger root?",'
            '"options":["1","2","3","6"],'
            '"correct_answer":"3"}'
        )

    question_generator.generate_text = mock_generate_text

    output = question_generator.generate_question("Algebra", "HARD")
    expected = {
        "question": "If x^2 - 5x + 6 = 0, what is the larger root?",
        "options": ["1", "2", "3", "6"],
        "correct_answer": "3",
    }

    print("Expected:", expected)
    print("Got:", output)
    assert output == expected

    question_generator.RECENT_QUESTIONS_QUEUE.clear()
    question_generator.RECENT_QUESTIONS_QUEUE.extend(original_queue)
    question_generator.generate_text = original_generate_text


def test_generate_question_retries_once_then_succeeds():
    original_generate_text = question_generator.generate_text
    original_queue = list(question_generator.RECENT_QUESTIONS_QUEUE)
    question_generator.RECENT_QUESTIONS_QUEUE.clear()

    state = {"count": 0}

    def mock_generate_text(prompt, temperature, max_tokens):
        state["count"] += 1
        if state["count"] == 1:
            return "not-json"
        return (
            '{"question":"What is 2+2?",'
            '"options":["1","2","3","4"],'
            '"correct_answer":"4"}'
        )

    question_generator.generate_text = mock_generate_text

    output = question_generator.generate_question("Arithmetic", "EASY")
    expected_question = "What is 2+2?"
    expected_attempts = 2

    print("Expected:", expected_question)
    print("Got:", output["question"])
    assert output["question"] == expected_question

    print("Expected:", expected_attempts)
    print("Got:", state["count"])
    assert state["count"] == expected_attempts

    question_generator.RECENT_QUESTIONS_QUEUE.clear()
    question_generator.RECENT_QUESTIONS_QUEUE.extend(original_queue)
    question_generator.generate_text = original_generate_text


def test_recent_questions_queue_keeps_only_last_ten():
    original_generate_text = question_generator.generate_text
    original_queue = list(question_generator.RECENT_QUESTIONS_QUEUE)
    question_generator.RECENT_QUESTIONS_QUEUE.clear()

    state = {"index": 0}

    def mock_generate_text(prompt, temperature, max_tokens):
        question_text = f"Question #{state['index']}"
        state["index"] += 1
        return (
            '{"question":"' + question_text + '",'
            '"options":["A","B","C","D"],'
            '"correct_answer":"A"}'
        )

    question_generator.generate_text = mock_generate_text

    for _ in range(11):
        question_generator.generate_question("Probability", "MEDIUM")

    expected_len = 10
    actual_len = len(question_generator.RECENT_QUESTIONS_QUEUE)
    print("Expected:", expected_len)
    print("Got:", actual_len)
    assert actual_len == expected_len

    expected_first = "Question #1"
    actual_first = list(question_generator.RECENT_QUESTIONS_QUEUE)[0]
    print("Expected:", expected_first)
    print("Got:", actual_first)
    assert actual_first == expected_first

    question_generator.RECENT_QUESTIONS_QUEUE.clear()
    question_generator.RECENT_QUESTIONS_QUEUE.extend(original_queue)
    question_generator.generate_text = original_generate_text


def run_all():
    test_generate_question_probability_easy()
    test_generate_question_algebra_hard()
    test_generate_question_retries_once_then_succeeds()
    test_recent_questions_queue_keeps_only_last_ten()


if __name__ == "__main__":
    run_all()
