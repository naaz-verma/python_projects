import streamlit as st

from utils import get_gemini_model
from game_map import (
    create_grid,
    place_player_and_treasure,
    calculate_distance,
    get_direction_hint,
    get_warmth_level,
    move_player,
    render_grid,
    generate_ai_clue,
    get_difficulty_settings,
    calculate_score,
    TERRAIN,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Treasure Hunt", page_icon="🗺️", layout="wide")

# ---------------------------------------------------------------------------
# Custom CSS for grid rendering and warmth colours
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .grid-row {
        font-size: 1.6rem;
        line-height: 1.7;
        letter-spacing: 2px;
        font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;
    }
    .warmth-hot    { color: #ff4b4b; font-weight: 700; }
    .warmth-warm   { color: #ff8c00; font-weight: 600; }
    .warmth-cool   { color: #1e90ff; font-weight: 600; }
    .warmth-cold   { color: #4169e1; font-weight: 700; }
    .warmth-found  { color: #2ecc71; font-weight: 700; }
    .clue-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 4px solid #e94560;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        color: #eee;
        font-style: italic;
    }
    .score-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        color: #f5f5f5;
    }
    .branding {
        text-align: center;
        margin-top: 2rem;
        color: #888;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
def init_session_state():
    """Ensure every required key exists in session state."""
    defaults = {
        "game_started": False,
        "game_over": False,
        "difficulty": "medium",
        "grid": None,
        "grid_size": 8,
        "player_pos": None,
        "treasure_pos": None,
        "visited": set(),
        "move_count": 0,
        "clue_history": [],
        "found_treasure": False,
        "fog_of_war": True,
        "model": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ---------------------------------------------------------------------------
# Helper: load the AI model (cached so it only runs once)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    """Load the Gemini model once and cache it."""
    return get_gemini_model()


# ---------------------------------------------------------------------------
# Start / reset game
# ---------------------------------------------------------------------------
def start_new_game(difficulty: str):
    """Initialise a fresh game with the chosen difficulty."""
    settings = get_difficulty_settings(difficulty)
    grid_size = settings["grid_size"]
    fog_of_war = settings["fog_of_war"]

    grid = create_grid(grid_size)
    player_pos, treasure_pos = place_player_and_treasure(grid_size)

    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.difficulty = difficulty
    st.session_state.grid = grid
    st.session_state.grid_size = grid_size
    st.session_state.player_pos = player_pos
    st.session_state.treasure_pos = treasure_pos
    st.session_state.visited = {tuple(player_pos)}
    st.session_state.move_count = 0
    st.session_state.clue_history = []
    st.session_state.found_treasure = False
    st.session_state.fog_of_war = fog_of_war
    st.session_state.model = load_model()


def reset_game():
    """Return to the welcome screen."""
    st.session_state.game_started = False
    st.session_state.game_over = False
    st.session_state.grid = None
    st.session_state.clue_history = []
    st.session_state.found_treasure = False
    st.session_state.move_count = 0


# ---------------------------------------------------------------------------
# Warmth styling helper
# ---------------------------------------------------------------------------
def warmth_class(level: str) -> str:
    """Return a CSS class name for the given warmth level."""
    level_lower = level.lower()
    if "found" in level_lower:
        return "warmth-found"
    if "hot" in level_lower or "burning" in level_lower:
        return "warmth-hot"
    if "warm" in level_lower:
        return "warmth-warm"
    if "cool" in level_lower:
        return "warmth-cool"
    return "warmth-cold"


# ---------------------------------------------------------------------------
# Process a movement
# ---------------------------------------------------------------------------
def handle_move(direction: str):
    """Move the player, generate a clue, and check for treasure."""
    s = st.session_state
    new_pos = move_player(s.player_pos, direction, s.grid_size)

    if new_pos is None:
        st.toast("You can't move outside the map!", icon="🚧")
        return

    s.player_pos = new_pos
    s.visited.add(tuple(new_pos))
    s.move_count += 1

    distance = calculate_distance(s.player_pos, s.treasure_pos)

    if distance == 0:
        s.found_treasure = True
        s.game_over = True
        return

    # Generate AI clue
    direction_hint = get_direction_hint(s.player_pos, s.treasure_pos)
    terrain = s.grid[s.player_pos[0]][s.player_pos[1]]

    if s.model is not None:
        clue = generate_ai_clue(
            s.model,
            distance,
            s.grid_size,
            direction_hint,
            s.move_count,
            s.difficulty,
            terrain,
        )
    else:
        warmth = get_warmth_level(distance, s.grid_size)
        clue = f"The treasure feels {warmth.lower()}. Try heading {direction_hint}."

    s.clue_history.append(clue)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🗺️ AI Treasure Hunt")

    difficulty = st.selectbox(
        "Difficulty",
        options=["easy", "medium", "hard"],
        format_func=lambda d: get_difficulty_settings(d)["label"],
        index=1,
        disabled=st.session_state.game_started and not st.session_state.game_over,
    )

    col_start, col_reset = st.columns(2)
    with col_start:
        if st.button("🏁 Start New Hunt", use_container_width=True):
            start_new_game(difficulty)
            st.rerun()
    with col_reset:
        if st.button("🔄 Reset", use_container_width=True):
            reset_game()
            st.rerun()

    # In-game sidebar widgets
    if st.session_state.game_started and not st.session_state.game_over:
        st.divider()
        st.metric("Moves", st.session_state.move_count)

        distance = calculate_distance(
            st.session_state.player_pos, st.session_state.treasure_pos
        )
        warmth = get_warmth_level(distance, st.session_state.grid_size)
        css = warmth_class(warmth)
        st.markdown(
            f"**Warmth:** <span class='{css}'>{warmth}</span>",
            unsafe_allow_html=True,
        )

    # Terrain legend (always visible)
    st.divider()
    st.subheader("Terrain Legend")
    legend_items = [
        ("🧭", "Player (you)"),
        ("💎", "Treasure"),
        ("👣", "Visited"),
        ("🟩", "Grass"),
        ("🌲", "Tree"),
        ("⛰️", "Mountain"),
        ("🌊", "Water"),
        ("⬜", "Fog (hidden)"),
        ("🏠", "Start"),
    ]
    for emoji, label in legend_items:
        st.markdown(f"{emoji} {label}")

    st.markdown(
        '<div class="branding">Built with WorldWithWeb</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("🗺️ AI Treasure Hunt")
st.caption("Built with WorldWithWeb")

# ---------------------------------------------------------------------------
# Screen 1 -- Welcome (game not started)
# ---------------------------------------------------------------------------
if not st.session_state.game_started:
    st.markdown("---")
    st.subheader("Welcome, Explorer!")
    st.markdown(
        """
        An ancient treasure has been hidden on a mysterious island.
        Use your wits and the AI guide's cryptic clues to find the **hidden gem**
        before your moves run out!
        """
    )

    st.markdown("### How to Play")
    st.markdown(
        """
        1. **Choose a difficulty** from the sidebar and click **Start New Hunt**.
        2. **Move** using the directional buttons (North / South / East / West).
        3. After each move you receive a **warmth indicator** (hot = close, cold = far)
           and an **AI-generated clue**.
        4. Find the treasure in as few moves as possible for the highest score!
        """
    )

    st.markdown("### Difficulty Levels")
    diff_cols = st.columns(3)
    difficulties = [
        ("Easy", "6x6 grid, no fog of war. Direct clues that guide you clearly."),
        ("Medium", "8x8 grid with fog of war. Vague, atmospheric clues."),
        ("Hard", "10x10 grid with fog of war. Cryptic riddles as clues. Good luck!"),
    ]
    for col, (name, desc) in zip(diff_cols, difficulties):
        with col:
            st.markdown(f"**{name}**")
            st.write(desc)

    st.markdown("### Terrain Legend")
    legend_cols = st.columns(4)
    terrains = [
        ("🟩 Grass", "Open land, easy to cross."),
        ("🌲 Tree", "Dense forest areas."),
        ("⛰️ Mountain", "Rocky highlands."),
        ("🌊 Water", "Rivers and lakes."),
    ]
    for col, (name, desc) in zip(legend_cols, terrains):
        with col:
            st.markdown(f"**{name}**")
            st.caption(desc)

    st.info("Select a difficulty in the sidebar and press **Start New Hunt** to begin!")

# ---------------------------------------------------------------------------
# Screen 3 -- Treasure found (game over)
# ---------------------------------------------------------------------------
elif st.session_state.game_over and st.session_state.found_treasure:
    st.balloons()

    st.markdown("---")
    st.subheader("🎉 You Found the Treasure!")

    score_data = calculate_score(
        st.session_state.move_count,
        st.session_state.grid_size,
        st.session_state.difficulty,
    )

    stars_display = "⭐" * score_data["stars"] + "☆" * (5 - score_data["stars"])

    st.markdown(
        f"""
        <div class="score-card">
            <h2>{stars_display}</h2>
            <h3>{score_data['message']}</h3>
            <p style="font-size:1.3rem;">Score: <strong>{score_data['score']}</strong> / {score_data['max_score']}</p>
            <p>Moves taken: <strong>{st.session_state.move_count}</strong> &nbsp;|&nbsp;
               Optimal moves: <strong>{score_data['optimal_moves']}</strong></p>
            <p>Difficulty: <strong>{st.session_state.difficulty.title()}</strong> &nbsp;|&nbsp;
               Grid: <strong>{st.session_state.grid_size}x{st.session_state.grid_size}</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Show the final grid (fully revealed)
    st.markdown("### Final Map")
    final_rows = render_grid(
        st.session_state.grid,
        st.session_state.player_pos,
        st.session_state.treasure_pos,
        st.session_state.visited,
        found_treasure=True,
        fog_of_war=False,
    )
    for row in final_rows:
        st.markdown(f'<div class="grid-row">{row}</div>', unsafe_allow_html=True)

    # Clue history
    if st.session_state.clue_history:
        with st.expander("Clue History", expanded=False):
            for i, clue in enumerate(st.session_state.clue_history, 1):
                st.markdown(f"**Move {i}:** {clue}")

    st.markdown("")
    if st.button("🏁 Play Again", use_container_width=True):
        reset_game()
        st.rerun()

# ---------------------------------------------------------------------------
# Screen 2 -- Active gameplay
# ---------------------------------------------------------------------------
else:
    left_col, right_col = st.columns([3, 2])

    # --- Grid display ---
    with left_col:
        st.markdown("### Map")
        grid_rows = render_grid(
            st.session_state.grid,
            st.session_state.player_pos,
            st.session_state.treasure_pos,
            st.session_state.visited,
            st.session_state.found_treasure,
            st.session_state.fog_of_war,
        )
        for row in grid_rows:
            st.markdown(f'<div class="grid-row">{row}</div>', unsafe_allow_html=True)

        # --- Movement buttons ---
        st.markdown("#### Move")
        btn_cols = st.columns(4)
        directions = [
            ("⬆️ North", "north"),
            ("⬇️ South", "south"),
            ("➡️ East", "east"),
            ("⬅️ West", "west"),
        ]
        for col, (label, direction) in zip(btn_cols, directions):
            with col:
                if st.button(label, use_container_width=True, key=f"move_{direction}"):
                    handle_move(direction)
                    st.rerun()

    # --- Right panel: warmth, clues ---
    with right_col:
        distance = calculate_distance(
            st.session_state.player_pos, st.session_state.treasure_pos
        )
        warmth = get_warmth_level(distance, st.session_state.grid_size)
        css = warmth_class(warmth)

        st.markdown("### Warmth Indicator")
        st.markdown(
            f"<h2 class='{css}'>{warmth}</h2>",
            unsafe_allow_html=True,
        )

        # Current terrain
        r, c = st.session_state.player_pos
        terrain = st.session_state.grid[r][c]
        terrain_emoji = TERRAIN.get(terrain, "🟩")
        st.markdown(f"**Current terrain:** {terrain_emoji} {terrain.title()}")

        st.markdown("---")

        # Latest clue
        st.markdown("### AI Clue")
        if st.session_state.clue_history:
            latest_clue = st.session_state.clue_history[-1]
            st.markdown(
                f'<div class="clue-box">{latest_clue}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="clue-box">Make your first move to receive a clue from the AI guide...</div>',
                unsafe_allow_html=True,
            )

        # Clue history
        if len(st.session_state.clue_history) > 1:
            with st.expander("Clue History", expanded=False):
                for i, clue in enumerate(st.session_state.clue_history, 1):
                    st.markdown(f"**Move {i}:** {clue}")

    # If treasure was just found
    if st.session_state.found_treasure:
        st.session_state.game_over = True
        st.rerun()

# ---------------------------------------------------------------------------
# Footer branding
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    '<div class="branding">Built with WorldWithWeb &bull; Powered by Gemini AI</div>',
    unsafe_allow_html=True,
)
