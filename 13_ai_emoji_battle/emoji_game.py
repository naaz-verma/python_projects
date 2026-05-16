import random
import json
import re


# Emoji categories
EMOJI_SETS = {
    "animals": ["🐶", "🐱", "🐼", "🦁", "🐸", "🦊", "🐧", "🦋", "🐙", "🦄", "🐝", "🐬"],
    "food": ["🍕", "🍩", "🌮", "🍦", "🎂", "🍣", "🥑", "🍔", "🍪", "🧁", "🍉", "🥐"],
    "weather": ["☀️", "🌧️", "⛈️", "🌈", "❄️", "🌪️", "🌙", "⭐", "🔥", "💨", "🌊", "☁️"],
    "emotions": ["😊", "😢", "😡", "😱", "🥳", "😴", "🤔", "😎", "🥺", "😂", "💀", "🤯"],
    "objects": ["🔑", "💡", "🎸", "📱", "⏰", "🎯", "🧲", "🔮", "🗡️", "🛡️", "💎", "🏆"],
    "places": ["🏠", "🏔️", "🏖️", "🌋", "🏰", "🚀", "🎪", "🏥", "🏫", "⛩️", "🗽", "🎡"],
}


def get_random_emojis(count=5):
    """Pick random emojis from different categories.

    Args:
        count: number of emojis to pick

    Returns:
        list of emoji strings
    """
    all_emojis = []
    categories = list(EMOJI_SETS.keys())

    # Pick from different categories for variety
    random.shuffle(categories)
    for i in range(count):
        cat = categories[i % len(categories)]
        emoji = random.choice(EMOJI_SETS[cat])
        all_emojis.append(emoji)

    return all_emojis


def score_story(model, emojis, story, round_num):
    """Ask AI to score a player's story based on emoji usage.

    Args:
        model: Gemini model instance
        emojis: list of emojis that should be used
        story: the player's story text
        round_num: current round number

    Returns:
        dict with 'creativity', 'coherence', 'emoji_usage', 'total', 'feedback'
    """
    emoji_str = " ".join(emojis)

    prompt = f"""You are a creative writing judge for an emoji story game.

The player was given these 5 emojis: {emoji_str}
They wrote this story: "{story}"

Score the story on 3 criteria (each 1-10):
1. creativity: How creative and imaginative is the story? (1=boring, 5=decent, 10=brilliant)
2. coherence: Does the story make sense as a narrative? (1=random words, 5=okay, 10=perfect flow)
3. emoji_usage: How well did they incorporate ALL 5 emojis? (1=ignored emojis, 5=mentioned some, 10=all emojis naturally woven in)

Also give a short, encouraging feedback comment (1-2 sentences).

Respond ONLY with valid JSON (no markdown, no extra text):
{{"creativity": 7, "coherence": 8, "emoji_usage": 6, "total": 21, "feedback": "Great imagination! Try to weave all emojis more naturally."}}

The "total" should be creativity + coherence + emoji_usage."""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)
        text = text.strip()
        result = json.loads(text)

        # Validate and clamp scores
        for key in ["creativity", "coherence", "emoji_usage"]:
            result[key] = max(1, min(10, int(result.get(key, 5))))
        result["total"] = result["creativity"] + result["coherence"] + result["emoji_usage"]
        result["feedback"] = str(result.get("feedback", "Good effort!"))
        return result

    except (json.JSONDecodeError, KeyError, ValueError):
        return {
            "creativity": 5,
            "coherence": 5,
            "emoji_usage": 5,
            "total": 15,
            "feedback": "Nice story! Keep being creative.",
        }


def generate_scenario(model, round_num):
    """Generate a short scenario for Story-to-Emoji mode.

    Args:
        model: Gemini model instance
        round_num: current round number

    Returns:
        string scenario text
    """
    prompt = f"""Create a short, vivid scenario in 2-3 sentences for round {round_num} of an emoji game.
The scenario should be descriptive and visual -- something a player could represent using 5 emojis.

Examples:
- "A brave knight rides through a thunderstorm to rescue a princess trapped in a burning castle."
- "A scientist discovers a glowing crystal in an underwater cave that gives anyone who touches it the ability to fly."

Write only the scenario, nothing else. Make it fun and imaginative."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip().strip('"')
    except Exception:
        scenarios = [
            "A lonely astronaut discovers a garden growing on Mars, filled with glowing flowers and singing birds.",
            "A chef accidentally creates a pizza that makes anyone who eats it invisible for one hour.",
            "A cat burglar is chased through a thunderstorm by a pack of robot dogs across the rooftops.",
            "A wizard opens a portal in the school library that leads to an underwater kingdom.",
            "A delivery driver's truck breaks down in front of a haunted castle during a snowstorm.",
        ]
        return scenarios[(round_num - 1) % len(scenarios)]


def judge_emoji_match(model, scenario, player_emojis):
    """Judge how well player's emoji selection matches a scenario.

    Args:
        model: Gemini model instance
        scenario: the original scenario text
        player_emojis: string of emojis the player selected

    Returns:
        dict with 'relevance', 'creativity', 'coverage', 'total', 'feedback'
    """
    prompt = f"""You are judging an emoji matching game.

Original scenario: "{scenario}"
Player's emoji selection: {player_emojis}

Score the emoji selection on 3 criteria (each 1-10):
1. relevance: How relevant are the emojis to the scenario? (1=unrelated, 10=perfect match)
2. creativity: How creative/clever is the emoji choice? (1=obvious, 10=brilliantly creative)
3. coverage: How well do the emojis cover all aspects of the scenario? (1=misses most, 10=covers everything)

Also give a short feedback comment.

Respond ONLY with valid JSON (no markdown, no extra text):
{{"relevance": 7, "creativity": 8, "coverage": 6, "total": 21, "feedback": "Great picks!"}}"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r"```json\s*", "", text)
        text = re.sub(r"```\s*", "", text)
        text = text.strip()
        result = json.loads(text)

        for key in ["relevance", "creativity", "coverage"]:
            result[key] = max(1, min(10, int(result.get(key, 5))))
        result["total"] = result["relevance"] + result["creativity"] + result["coverage"]
        result["feedback"] = str(result.get("feedback", "Interesting choices!"))
        return result

    except (json.JSONDecodeError, KeyError, ValueError):
        return {
            "relevance": 5,
            "creativity": 5,
            "coverage": 5,
            "total": 15,
            "feedback": "Interesting emoji choices!",
        }


def get_all_emojis_flat():
    """Return all available emojis as a flat list for the picker."""
    all_emojis = []
    for cat_emojis in EMOJI_SETS.values():
        all_emojis.extend(cat_emojis)
    return all_emojis


def calculate_final_stats(rounds):
    """Calculate final game statistics.

    Args:
        rounds: list of round result dicts

    Returns:
        dict with stats
    """
    if not rounds:
        return {"total": 0, "avg": 0, "best_round": 0, "best_score": 0, "rounds_played": 0}

    totals = [r["score"]["total"] for r in rounds]
    best_idx = totals.index(max(totals))

    return {
        "total": sum(totals),
        "avg": round(sum(totals) / len(totals), 1),
        "best_round": best_idx + 1,
        "best_score": max(totals),
        "rounds_played": len(rounds),
        "max_possible": len(rounds) * 30,
    }


def get_star_rating(score, max_score=30):
    """Convert a score to star rating string.

    Args:
        score: round total (out of 30)
        max_score: maximum possible per round

    Returns:
        string of star emojis
    """
    ratio = score / max_score if max_score > 0 else 0
    if ratio >= 0.9:
        return "⭐⭐⭐⭐⭐"
    elif ratio >= 0.7:
        return "⭐⭐⭐⭐"
    elif ratio >= 0.5:
        return "⭐⭐⭐"
    elif ratio >= 0.3:
        return "⭐⭐"
    else:
        return "⭐"
