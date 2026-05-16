import json
import re


# Room themes and descriptions
ROOMS = {
    "easy": [
        {"name": "The Cellar", "theme": "a dark underground wine cellar with wooden barrels"},
        {"name": "The Kitchen", "theme": "an old abandoned kitchen with rusty pots and pans"},
        {"name": "The Garden", "theme": "a walled garden with overgrown plants and a locked gate"},
    ],
    "medium": [
        {"name": "The Dungeon Cell", "theme": "a cold stone dungeon cell with chains on the walls"},
        {"name": "The Library", "theme": "a dusty library with thousands of old books"},
        {"name": "The Armory", "theme": "a medieval armory filled with weapons and shields"},
        {"name": "The Tower", "theme": "a tall tower room with a window overlooking the kingdom"},
    ],
    "hard": [
        {"name": "The Crypt", "theme": "an ancient crypt beneath a cathedral with stone coffins"},
        {"name": "The Laboratory", "theme": "an alchemist's laboratory with bubbling potions"},
        {"name": "The Throne Room", "theme": "a grand throne room with hidden passages"},
        {"name": "The Observatory", "theme": "a rooftop observatory with star maps and telescopes"},
        {"name": "The Vault", "theme": "a heavily guarded treasure vault with combination locks"},
    ],
}


def get_rooms_for_difficulty(difficulty):
    """Return the list of rooms for the selected difficulty."""
    return ROOMS.get(difficulty.lower(), ROOMS["medium"])


def generate_puzzle(model, room, difficulty, room_number, total_rooms):
    """Generate a puzzle for a room using AI.

    Args:
        model: Gemini model instance
        room: dict with 'name' and 'theme'
        difficulty: 'easy', 'medium', or 'hard'
        room_number: current room number (1-based)
        total_rooms: total number of rooms

    Returns:
        dict with 'description', 'puzzle', 'answer', 'hint1', 'hint2', 'hint3'
    """
    prompt = f"""You are a game master for a dungeon escape game. Generate a puzzle for Room {room_number} of {total_rooms}.

Room: {room['name']}
Setting: {room['theme']}
Difficulty: {difficulty}

Generate a puzzle that fits this room's theme. The answer should be a single word or short phrase (max 3 words).

For easy: simple riddles with obvious answers
For medium: tricky riddles that require thinking
For hard: lateral thinking puzzles or logic puzzles

Respond ONLY with valid JSON in this exact format (no markdown, no extra text):
{{
    "description": "A 2-3 sentence vivid description of the room and what the player sees",
    "puzzle": "The puzzle or riddle text that the player must solve",
    "answer": "the answer in lowercase",
    "hint1": "A vague hint that nudges in the right direction",
    "hint2": "A more specific hint that narrows it down",
    "hint3": "A very obvious hint that almost gives it away"
}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Clean up markdown code blocks if present
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)
        text = text.strip()

        result = json.loads(text)

        # Validate all fields exist
        required = ["description", "puzzle", "answer", "hint1", "hint2", "hint3"]
        for field in required:
            if field not in result:
                result[field] = "Error generating this field"

        # Normalize the answer
        result["answer"] = result["answer"].strip().lower()
        return result

    except (json.JSONDecodeError, KeyError, IndexError) as e:
        # Fallback puzzle if AI fails
        return {
            "description": f"You enter {room['name']}. {room['theme']}.",
            "puzzle": "What has keys but no locks, space but no room, and you can enter but can't go inside?",
            "answer": "keyboard",
            "hint1": "You might be using one right now",
            "hint2": "It has letters and numbers on it",
            "hint3": "You type on it every day",
        }


def check_answer(player_answer, correct_answer):
    """Check if the player's answer matches the correct answer.

    Args:
        player_answer: what the player typed
        correct_answer: the correct answer

    Returns:
        True if correct, False otherwise
    """
    # Normalize both answers: lowercase, strip whitespace
    player = player_answer.strip().lower()
    correct = correct_answer.strip().lower()

    # Exact match
    if player == correct:
        return True

    # Check if one contains the other (for close answers)
    if player in correct or correct in player:
        return True

    return False


def get_score(rooms_solved, total_rooms, total_hints_used, difficulty):
    """Calculate the final score.

    Args:
        rooms_solved: number of rooms completed
        total_rooms: total rooms in the game
        total_hints_used: total hints used across all rooms
        difficulty: game difficulty level

    Returns:
        dict with 'score', 'max_score', 'grade', 'message'
    """
    # Base points per room
    difficulty_multiplier = {"easy": 1, "medium": 2, "hard": 3}
    multiplier = difficulty_multiplier.get(difficulty.lower(), 1)

    # Points calculation
    room_points = rooms_solved * 100 * multiplier
    hint_penalty = total_hints_used * 15 * multiplier
    completion_bonus = 200 * multiplier if rooms_solved == total_rooms else 0

    score = max(0, room_points - hint_penalty + completion_bonus)
    max_score = (total_rooms * 100 + 200) * multiplier

    # Grade
    percentage = (score / max_score * 100) if max_score > 0 else 0
    if percentage >= 90:
        grade = "S"
        message = "Master Escapist! Perfect run!"
    elif percentage >= 75:
        grade = "A"
        message = "Expert! You barely needed any help."
    elif percentage >= 60:
        grade = "B"
        message = "Great job! You escaped with skill."
    elif percentage >= 40:
        grade = "C"
        message = "Not bad! Room for improvement."
    else:
        grade = "D"
        message = "You escaped, but used a lot of hints!"

    return {
        "score": score,
        "max_score": max_score,
        "grade": grade,
        "message": message,
        "percentage": round(percentage, 1),
    }
