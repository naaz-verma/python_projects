import json


def generate_quiz(client, topic, difficulty, num_questions):
    """Generate a quiz using OpenAI on any topic."""
    prompt = f"""Generate a quiz with exactly {num_questions} multiple-choice questions about "{topic}".
Difficulty level: {difficulty}

Rules:
- Each question must have exactly 4 options labeled A, B, C, D
- Only one option should be correct
- For "Easy": straightforward factual questions
- For "Medium": questions requiring some reasoning
- For "Hard": tricky questions that test deep understanding
- Make questions fun and engaging for teenagers

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a quiz master who creates fun, educational quizzes for teenagers. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0]

    quiz_data = json.loads(content)
    return quiz_data["questions"]


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
