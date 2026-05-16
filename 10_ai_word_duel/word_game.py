import json
import re


def generate_category(model, difficulty, round_num, total_rounds):
    """Generate a word challenge category using AI.

    Args:
        model: Gemini model instance
        difficulty: 'Easy', 'Medium', or 'Hard'
        round_num: current round (1-based)
        total_rounds: total rounds in the game

    Returns:
        dict with 'category' and 'hint'
    """
    prompt = f"""You are a word game host. Generate ONE creative word challenge for round {round_num} of {total_rounds}.

Difficulty: {difficulty}
- Easy: Simple, common categories (e.g., "Name a fruit that is yellow")
- Medium: More specific categories (e.g., "Name something you'd find in a doctor's office that starts with S")
- Hard: Obscure or creative categories (e.g., "Name something that exists in both a kitchen and outer space")

The challenge should have MANY possible valid answers. Make it fun and interesting.
Make each round's category different from typical ones.

Respond ONLY with valid JSON (no markdown, no extra text):
{{"category": "The challenge text", "hint": "A short helpful hint"}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)
        text = text.strip()
        result = json.loads(text)
        if "category" not in result:
            result["category"] = "Name something blue"
        if "hint" not in result:
            result["hint"] = "Think creatively!"
        return result
    except (json.JSONDecodeError, KeyError, IndexError):
        return {
            "category": "Name an animal that could survive in a city",
            "hint": "Think about what animals you see in urban areas",
        }


def judge_answer(model, category, answer, difficulty):
    """Ask AI to judge if an answer is valid and score creativity.

    Args:
        model: Gemini model instance
        category: the challenge category text
        answer: the player's answer
        difficulty: game difficulty

    Returns:
        dict with 'valid', 'score', 'reason'
    """
    prompt = f"""You are a fair word game judge. Judge this answer:

Category: "{category}"
Player's answer: "{answer}"
Difficulty: {difficulty}

Rules:
- "valid": true if the answer reasonably fits the category, false if not
- "score": rate creativity from 1-10 (1=obvious, 5=decent, 8=clever, 10=brilliant)
- "reason": one sentence explaining your judgment

Be fair but not too strict. If the answer is a reasonable stretch, accept it.
Give higher creativity scores for unexpected but valid answers.

Respond ONLY with valid JSON (no markdown, no extra text):
{{"valid": true, "score": 7, "reason": "Good answer because..."}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)
        text = text.strip()
        result = json.loads(text)

        # Ensure valid fields
        result["valid"] = bool(result.get("valid", False))
        result["score"] = max(0, min(10, int(result.get("score", 5))))
        result["reason"] = str(result.get("reason", "No comment"))
        return result
    except (json.JSONDecodeError, KeyError, IndexError, ValueError):
        return {"valid": True, "score": 5, "reason": "Acceptable answer!"}


def calculate_round_score(judgment, difficulty):
    """Calculate points for a round based on judgment and difficulty.

    Args:
        judgment: dict from judge_answer()
        difficulty: 'Easy', 'Medium', or 'Hard'

    Returns:
        int score for this round
    """
    if not judgment["valid"]:
        return 0

    multipliers = {"Easy": 1.0, "Medium": 1.5, "Hard": 2.0}
    multiplier = multipliers.get(difficulty, 1.0)
    return int(judgment["score"] * multiplier)


def calculate_final_score(rounds):
    """Calculate final score from all rounds.

    Args:
        rounds: list of round result dicts

    Returns:
        dict with 'total_score', 'valid_answers', 'avg_creativity', 'rounds_played'
    """
    total = sum(r["score"] for r in rounds)
    valid = sum(1 for r in rounds if r["judgment"]["valid"])
    creativity_scores = [r["judgment"]["score"] for r in rounds if r["judgment"]["valid"]]
    avg = round(sum(creativity_scores) / len(creativity_scores), 1) if creativity_scores else 0

    return {
        "total_score": total,
        "valid_answers": valid,
        "avg_creativity": avg,
        "rounds_played": len(rounds),
    }


def get_max_possible_score(total_rounds, difficulty):
    """Calculate maximum possible score."""
    multipliers = {"Easy": 1.0, "Medium": 1.5, "Hard": 2.0}
    multiplier = multipliers.get(difficulty, 1.0)
    return int(10 * multiplier * total_rounds)


def get_rank_title(score, max_score):
    """Get a fun rank title based on score percentage."""
    if max_score == 0:
        return "Beginner"
    pct = score / max_score * 100
    if pct >= 90:
        return "Word Wizard"
    elif pct >= 75:
        return "Vocabulary Master"
    elif pct >= 60:
        return "Word Smith"
    elif pct >= 40:
        return "Word Explorer"
    elif pct >= 20:
        return "Word Apprentice"
    else:
        return "Word Beginner"
