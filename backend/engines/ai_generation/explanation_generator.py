import json
from engines.ai_generation.llm_client import generate_text
from engines.ai_generation.prompt_templates import build_explanation_prompt
EXPLANATION_TEMPERATURE = 0.3
EXPLANATION_MAX_TOKENS = 200
FALLBACK_EXPLANATION = "Explanation unavailable."
def generate_explanation(question, correct_answer):
    prompt = build_explanation_prompt(question, correct_answer)
    try:
        raw_output = generate_text(prompt, EXPLANATION_TEMPERATURE, EXPLANATION_MAX_TOKENS)
        parsed_output = json.loads(raw_output)
    except Exception:
        return {"explanation": FALLBACK_EXPLANATION}
    explanation = parsed_output.get("explanation") if isinstance(parsed_output, dict) else None
    if isinstance(explanation, str):
        return {"explanation": explanation}
    return {"explanation": FALLBACK_EXPLANATION}