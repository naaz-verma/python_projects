import random
import math
import json
import re


# Terrain types and their emojis
TERRAIN = {
    "grass": "🟩",
    "tree": "🌲",
    "mountain": "⛰️",
    "water": "🌊",
    "fog": "⬜",
    "player": "🧭",
    "treasure": "💎",
    "visited": "👣",
    "start": "🏠",
}


def create_grid(size):
    """Create a grid with random terrain.

    Args:
        size: grid dimensions (size x size)

    Returns:
        2D list of terrain strings
    """
    grid = []
    for row in range(size):
        grid_row = []
        for col in range(size):
            # Random terrain distribution
            r = random.random()
            if r < 0.55:
                grid_row.append("grass")
            elif r < 0.75:
                grid_row.append("tree")
            elif r < 0.88:
                grid_row.append("mountain")
            else:
                grid_row.append("water")
        grid.append(grid_row)
    return grid


def place_player_and_treasure(size):
    """Place player and treasure at random positions (at least half the grid apart).

    Args:
        size: grid dimensions

    Returns:
        tuple of (player_pos, treasure_pos) as [row, col] lists
    """
    min_distance = size // 2

    player_pos = [random.randint(0, size - 1), random.randint(0, size - 1)]

    while True:
        treasure_pos = [random.randint(0, size - 1), random.randint(0, size - 1)]
        dist = calculate_distance(player_pos, treasure_pos)
        if dist >= min_distance:
            break

    return player_pos, treasure_pos


def calculate_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions.

    Args:
        pos1: [row, col]
        pos2: [row, col]

    Returns:
        int distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def get_direction_hint(player_pos, treasure_pos):
    """Get a general direction from player to treasure.

    Args:
        player_pos: [row, col]
        treasure_pos: [row, col]

    Returns:
        string describing direction
    """
    row_diff = treasure_pos[0] - player_pos[0]
    col_diff = treasure_pos[1] - player_pos[1]

    directions = []
    if row_diff < 0:
        directions.append("north")
    elif row_diff > 0:
        directions.append("south")

    if col_diff > 0:
        directions.append("east")
    elif col_diff < 0:
        directions.append("west")

    if not directions:
        return "right here"

    return "-".join(directions)


def get_warmth_level(distance, grid_size):
    """Get warmth level based on distance.

    Args:
        distance: Manhattan distance to treasure
        grid_size: size of the grid

    Returns:
        string warmth level
    """
    ratio = distance / grid_size

    if distance == 0:
        return "FOUND IT!"
    elif ratio <= 0.15:
        return "BURNING HOT"
    elif ratio <= 0.3:
        return "Very Hot"
    elif ratio <= 0.5:
        return "Warm"
    elif ratio <= 0.7:
        return "Cool"
    elif ratio <= 0.85:
        return "Cold"
    else:
        return "Freezing"


def move_player(player_pos, direction, grid_size):
    """Move the player in a direction.

    Args:
        player_pos: [row, col]
        direction: 'north', 'south', 'east', 'west'
        grid_size: size of the grid

    Returns:
        new [row, col] or None if invalid move
    """
    moves = {
        "north": [-1, 0],
        "south": [1, 0],
        "east": [0, 1],
        "west": [0, -1],
    }

    if direction not in moves:
        return None

    new_row = player_pos[0] + moves[direction][0]
    new_col = player_pos[1] + moves[direction][1]

    # Check boundaries
    if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
        return [new_row, new_col]
    return None


def render_grid(grid, player_pos, treasure_pos, visited, found_treasure, fog_of_war=True):
    """Render the grid as emoji strings for display.

    Args:
        grid: 2D list of terrain
        player_pos: [row, col]
        treasure_pos: [row, col]
        visited: set of (row, col) tuples
        found_treasure: bool
        fog_of_war: if True, hide unvisited cells

    Returns:
        list of strings (one per row)
    """
    rows = []
    for r in range(len(grid)):
        row_str = ""
        for c in range(len(grid[0])):
            if [r, c] == player_pos:
                row_str += TERRAIN["player"]
            elif [r, c] == treasure_pos and found_treasure:
                row_str += TERRAIN["treasure"]
            elif fog_of_war and (r, c) not in visited:
                row_str += TERRAIN["fog"]
            elif (r, c) in visited and [r, c] != player_pos:
                row_str += TERRAIN["visited"]
            else:
                row_str += TERRAIN.get(grid[r][c], "🟩")
        rows.append(row_str)
    return rows


def generate_ai_clue(model, distance, grid_size, direction, move_count, difficulty, terrain):
    """Generate an AI clue based on current game state.

    Args:
        model: Gemini model instance
        distance: Manhattan distance to treasure
        grid_size: grid size
        direction: direction string to treasure
        move_count: number of moves made
        difficulty: 'easy', 'medium', 'hard'
        terrain: terrain type at current position

    Returns:
        string clue text
    """
    warmth = get_warmth_level(distance, grid_size)

    if difficulty == "easy":
        prompt = f"""You are a treasure hunt guide. Give a DIRECT helpful clue.
The treasure is {distance} steps away, to the {direction}.
Warmth level: {warmth}.
Current terrain: {terrain}.
Move count: {move_count}.

Give a 1-sentence clue. Be specific about direction. Example: "Head 3 steps north and then east."
Keep it simple and helpful."""

    elif difficulty == "medium":
        prompt = f"""You are a mysterious treasure hunt guide. Give a VAGUE but helpful clue.
The treasure is {distance} steps away, to the {direction}.
Warmth level: {warmth}.
Current terrain: {terrain}.

Give a 1-sentence atmospheric clue. Hint at direction without being exact.
Example: "The wind carries whispers from the north..." or "You feel warmth growing from the east."
Be poetic but useful."""

    else:  # hard
        prompt = f"""You are a cryptic oracle in a treasure hunt. Give a RIDDLE-like clue.
The treasure is {distance} steps away, to the {direction}.
Warmth level: {warmth}.
Current terrain: {terrain}.

Give a 1-sentence riddle that hints at the direction or distance.
Be cryptic and mysterious. Make the player think.
Example: "Where the sun sets, fortune awaits three paces hence." (meaning west, 3 steps)"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip().strip('"')
    except Exception:
        # Fallback clue
        return f"The treasure feels {warmth.lower()}. Try heading {direction}."


def get_difficulty_settings(difficulty):
    """Get grid size and settings for difficulty level.

    Args:
        difficulty: 'easy', 'medium', or 'hard'

    Returns:
        dict with 'grid_size', 'fog_of_war', 'label'
    """
    settings = {
        "easy": {"grid_size": 6, "fog_of_war": False, "label": "Easy (6x6, no fog)"},
        "medium": {"grid_size": 8, "fog_of_war": True, "label": "Medium (8x8, fog of war)"},
        "hard": {"grid_size": 10, "fog_of_war": True, "label": "Hard (10x10, fog of war)"},
    }
    return settings.get(difficulty, settings["medium"])


def calculate_score(moves, grid_size, difficulty):
    """Calculate score based on moves taken.

    Args:
        moves: number of moves made
        grid_size: grid size
        difficulty: difficulty level

    Returns:
        dict with 'score', 'max_score', 'stars', 'message'
    """
    multipliers = {"easy": 1, "medium": 2, "hard": 3}
    mult = multipliers.get(difficulty, 1)

    # Optimal moves would be roughly the Manhattan distance (grid_size)
    optimal = grid_size
    max_score = 1000 * mult

    # Score decreases as moves increase beyond optimal
    if moves <= optimal:
        score = max_score
    else:
        penalty = (moves - optimal) * (max_score // (grid_size * 2))
        score = max(100 * mult, max_score - penalty)

    # Stars (1-5)
    ratio = score / max_score
    if ratio >= 0.9:
        stars = 5
        message = "Treasure Hunter Legend!"
    elif ratio >= 0.7:
        stars = 4
        message = "Expert Navigator!"
    elif ratio >= 0.5:
        stars = 3
        message = "Skilled Explorer!"
    elif ratio >= 0.3:
        stars = 2
        message = "Wandering Adventurer"
    else:
        stars = 1
        message = "Lost but Found It!"

    return {
        "score": score,
        "max_score": max_score,
        "stars": stars,
        "message": message,
        "optimal_moves": optimal,
    }
