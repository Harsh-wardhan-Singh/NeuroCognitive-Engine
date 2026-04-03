from datetime import datetime, timezone

from config.settings import (
    AVG_TIME_CONFIG,
    DEFAULT_AVG_RESPONSE_TIME,
    DEFAULT_TOPIC_CONCEPTS,
    NUM_QUESTIONS_MAX,
    NUM_QUESTIONS_MIN,
    STRONG_MASTERY_THRESHOLD,
    WEAK_MASTERY_THRESHOLD,
)


def build_concept_id(subject: str, topic: str, concept: str) -> str:
    return f"{subject}.{topic}.{concept}"


def validate_num_questions(num_questions: int) -> None:
    if num_questions < NUM_QUESTIONS_MIN or num_questions > NUM_QUESTIONS_MAX:
        raise ValueError("num_questions must be between 5 and 20")


def validate_submit_input(selected_option: str, reported_confidence: float, response_time: float) -> None:
    if not isinstance(selected_option, str) or selected_option.strip() == "":
        raise ValueError("selected_option is required")
    if reported_confidence < 0.0 or reported_confidence > 1.0:
        raise ValueError("reported_confidence must be between 0 and 1")
    if response_time <= 0.0:
        raise ValueError("response_time must be greater than 0")


def datetime_to_unix_timestamp(value: datetime) -> float:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.timestamp()


def get_avg_time_for_concept(concept_id: str) -> float:
    return AVG_TIME_CONFIG.get(concept_id, DEFAULT_AVG_RESPONSE_TIME)


def get_default_concepts(subject: str, topic: str) -> list[str]:
    key = f"{subject}.{topic}"
    return DEFAULT_TOPIC_CONCEPTS.get(key, ["linear_equations"])


def is_weak_concept(mastery: float) -> bool:
    return mastery < WEAK_MASTERY_THRESHOLD


def is_strong_concept(mastery: float) -> bool:
    return mastery >= STRONG_MASTERY_THRESHOLD
