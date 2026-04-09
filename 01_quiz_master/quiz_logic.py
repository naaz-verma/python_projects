import json


def generate_quiz(model, topic, difficulty, num_questions):
    """Generate a quiz using Gemini on any topic."""
    prompt = f"""Generate a quiz with exactly {num_questions} multiple-choice questions about "{topic}".
Difficulty level: {difficulty}

Rules:
- Each question must have exactly 4 options labeled A, B, C, D
- Only one option should be correct
- For "Easy": straightforward factual questions
- For "Medium": questions requiring some reasoning
- For "Hard": tricky questions that test deep understanding
- Make questions fun and engaging for teenagers

You are a quiz master who creates fun, educational quizzes for teenagers. Always respond with valid JSON only.

Respond ONLY with valid JSON in this exact format (no extra text):
{{
  "questions": [
    {{
      "question": "What is ...?",
      "options": {{
        "A": "Option 1",
        "B": "Option 2",
        "C": "Option 3",
        "D": "Option 4"
      }},
      "correct": "B",
      "explanation": "Brief explanation of why B is correct"
    }}
  ]
}}"""

    response = model.generate_content(prompt)

    content = response.text.strip()

    # Find the JSON portion (skip any markdown fences or extra text)
    start = content.find('{')
    if start == -1:
        start = content.find('[')
    if start == -1:
        raise ValueError("No JSON found in model response")
    end = max(content.rfind('}'), content.rfind(']'))
    content = content[start:end + 1]

    quiz_data = json.loads(content)

    # Handle both {"questions": [...]} and bare [...] formats
    if isinstance(quiz_data, list):
        questions = quiz_data
    else:
        questions = quiz_data["questions"]

    # Validate that each question is a proper dict
    for q in questions:
        if not isinstance(q, dict) or "question" not in q or "options" not in q:
            raise ValueError("Model returned invalid question format. Please try again.")

    return questions


def check_answer(user_answer, correct_answer):
    """Check if the user's answer is correct."""
    return user_answer == correct_answer


def calculate_score(user_answers, questions):
    """Calculate quiz score and breakdown."""
    correct = 0
    results = []

    for i, question in enumerate(questions):
        is_correct = user_answers[i] == question["correct"]
        if is_correct:
            correct += 1
        results.append({
            "question": question["question"],
            "user_answer": user_answers[i],
            "correct_answer": question["correct"],
            "is_correct": is_correct,
            "explanation": question["explanation"]
        })

    return {
        "correct": correct,
        "total": len(questions),
        "percentage": round((correct / len(questions)) * 100),
        "results": results
    }
