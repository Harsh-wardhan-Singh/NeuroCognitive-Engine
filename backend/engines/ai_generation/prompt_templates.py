def build_question_prompt(concept, difficulty, recent_questions):
	recent_block = ""
	if recent_questions:
		joined_recent = "\n".join(f"- {item}" for item in recent_questions)
		recent_block = (
			"Avoid generating questions similar to these recent questions:\n"
			f"{joined_recent}\n\n"
		)

	return (
		"You are an expert educational assessment question generator.\n"
		+ f"Concept: {concept}\n"
		+ f"Difficulty: {difficulty}\n\n"
		+ "Difficulty behavior definitions:\n"
		+ "- EASY: direct recall, single-step, basic understanding only.\n"
		+ "- MEDIUM: multi-step reasoning and application-based understanding.\n"
		+ "- HARD: tricky edge cases, multi-concept reasoning, deep understanding required.\n\n"
		+ recent_block
		+ "Question quality requirements:\n"
		+ "1) Create a realistic exam-style question clearly tied to the concept and requested difficulty.\n"
		+ "2) The question must be specific, unambiguous, and solvable from the information given.\n"
		+ "3) Avoid vague wording and avoid hallucinated or unverifiable facts.\n"
		+ "4) Use precise language and ensure there is exactly one best correct answer.\n\n"
		+ "Option quality requirements:\n"
		+ "1) Provide exactly 4 plausible options.\n"
		+ "2) Options must be similar in length and grammatical structure.\n"
		+ "3) Do NOT include jokes, irrelevant text, absurd outliers, or obviously wrong distractors.\n"
		+ "4) Distractors must be credible and close enough to challenge the learner.\n\n"
		+ "Anti-repetition requirements:\n"
		+ "1) Do not repeat or paraphrase recent questions.\n"
		+ "2) Ensure high variation in numbers, context, and sentence structure compared with recent questions.\n"
		+ "3) Generate a completely new question intent, not a lightly edited version.\n\n"
		+ "Self-verification before final output:\n"
		+ "1) Think carefully before answering.\n"
		+ "2) Verify that correct_answer is factually and logically correct.\n"
		+ "3) Verify each distractor is plausible but incorrect.\n"
		+ "4) Verify the question is unambiguous and matches the requested difficulty level.\n\n"
		+ "Return ONLY valid JSON. No markdown. No comments. No explanation outside JSON.\n"
		+ "JSON schema:\n"
		+ "{\n"
		+ '  "question": "string",\n'
		+ '  "options": ["string", "string", "string", "string"],\n'
		+ '  "correct_answer": "string"\n'
		+ "}\n\n"
		+ "Final strict rules:\n"
		+ "1) options must contain exactly 4 choices\n"
		+ "2) correct_answer must exactly match one option\n"
		+ "3) Output ONLY valid JSON\n"
	)


def build_explanation_prompt(question, correct_answer):
	return (
		"You are generating a concise learning explanation.\n"
		f"Question: {question}\n"
		f"Correct Answer: {correct_answer}\n\n"
		"Return ONLY valid JSON. Do not include markdown. Do not include extra text.\n"
		"JSON schema:\n"
		"{\n"
		'  "explanation": "string"\n'
		"}\n\n"
		"Output ONLY valid JSON\n"
	)
