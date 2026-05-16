"""
AI Dungeon Escape - Streamlit App
A puzzle-based escape room game powered by AI-generated challenges.
Built with WorldWithWeb.
"""

import streamlit as st
from utils import get_gemini_model
from game_engine import (
    get_rooms_for_difficulty,
    generate_puzzle,
    check_answer,
    get_score,
)


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Dungeon Escape",
    page_icon="🏰",
    layout="centered",
)


# ---------------------------------------------------------------------------
# Session-state initialisation
# ---------------------------------------------------------------------------
def init_session_state():
    """Ensure every required key exists in session state."""
    defaults = {
        "game_started": False,
        "current_room": 0,
        "rooms": [],
        "puzzles": {},
        "hints_used": {},
        "rooms_solved": [],
        "inventory": [],
        "game_won": False,
        "difficulty": "easy",
        "model": None,
        "answer_correct": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ---------------------------------------------------------------------------
# Helper: load / cache the AI model
# ---------------------------------------------------------------------------
def ensure_model():
    """Load the Gemini model once and store it in session state."""
    if st.session_state.model is None:
        st.session_state.model = get_gemini_model()
    return st.session_state.model


# ---------------------------------------------------------------------------
# Helper: get or generate puzzle for the current room
# ---------------------------------------------------------------------------
def get_current_puzzle():
    """Return the puzzle for the current room, generating it lazily if needed."""
    idx = st.session_state.current_room
    if idx not in st.session_state.puzzles:
        model = ensure_model()
        if model is None:
            st.error(
                "Gemini API key not found. Please set GEMINI_API_KEY in your .env file."
            )
            st.stop()

        room = st.session_state.rooms[idx]
        total = len(st.session_state.rooms)
        with st.spinner("The dungeon master is crafting your puzzle..."):
            puzzle = generate_puzzle(
                model,
                room,
                st.session_state.difficulty,
                room_number=idx + 1,
                total_rooms=total,
            )
        st.session_state.puzzles[idx] = puzzle

        if idx not in st.session_state.hints_used:
            st.session_state.hints_used[idx] = 0

    return st.session_state.puzzles[idx]


# ---------------------------------------------------------------------------
# Helper: start a new game
# ---------------------------------------------------------------------------
def start_game(difficulty):
    """Reset state and begin a new game at the chosen difficulty."""
    st.session_state.difficulty = difficulty.lower()
    st.session_state.rooms = get_rooms_for_difficulty(difficulty)
    st.session_state.current_room = 0
    st.session_state.puzzles = {}
    st.session_state.hints_used = {}
    st.session_state.rooms_solved = []
    st.session_state.inventory = []
    st.session_state.game_won = False
    st.session_state.game_started = True
    st.session_state.answer_correct = False
    st.session_state.model = None


# ---------------------------------------------------------------------------
# Helper: reset everything
# ---------------------------------------------------------------------------
def reset_game():
    """Clear all session state and return to the welcome screen."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def render_sidebar():
    """Draw the sidebar with controls and game info."""
    with st.sidebar:
        st.header("🎮 Game Controls")

        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=["Easy", "Medium", "Hard"].index(
                st.session_state.difficulty.capitalize()
            ),
            disabled=st.session_state.game_started and not st.session_state.game_won,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Start Game", use_container_width=True):
                start_game(difficulty)
                st.rerun()
        with col2:
            if st.button("🔄 Reset", use_container_width=True):
                reset_game()
                st.rerun()

        if st.session_state.game_started and not st.session_state.game_won:
            st.divider()

            st.subheader("🎒 Inventory")
            if st.session_state.inventory:
                for item in st.session_state.inventory:
                    st.write(f"🔑 {item}")
            else:
                st.caption("No items yet.")

            st.subheader("🚪 Rooms Cleared")
            total = len(st.session_state.rooms)
            solved = len(st.session_state.rooms_solved)
            st.write(f"{solved} / {total}")
            for idx in st.session_state.rooms_solved:
                room = st.session_state.rooms[idx]
                st.write(f"✅ {room['name']}")

        st.divider()
        st.caption("Built with **WorldWithWeb**")


# ---------------------------------------------------------------------------
# Screen 1: Welcome / not started
# ---------------------------------------------------------------------------
def render_welcome():
    """Show the welcome screen with instructions."""
    st.title("🏰 AI Dungeon Escape")
    st.markdown("*Built with **WorldWithWeb***")

    st.markdown("---")

    st.markdown(
        """
        ### Welcome, brave adventurer!

        You have been trapped in a mysterious dungeon. To escape, you must
        navigate through a series of rooms, each guarded by a unique puzzle
        crafted by an AI dungeon master. Solve every puzzle to earn the keys
        that will set you free!
        """
    )

    st.markdown("### 📖 How to Play")
    st.markdown(
        """
        1. **Choose a difficulty** from the sidebar.
        2. **Click "Start Game"** to begin your escape.
        3. Each room presents a **puzzle** you must solve.
        4. Type your answer and click **Submit**.
        5. Stuck? Use the **Hint** button (up to 3 hints per room, but each
           hint costs points!).
        6. Solve the puzzle to earn a **key** and unlock the next room.
        7. Clear all rooms to **escape the dungeon** and see your final score!
        """
    )

    st.markdown("### 🎯 Difficulty Levels")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            **🟢 Easy**
            - 3 rooms
            - Simple riddles
            - Great for beginners
            """
        )
    with col2:
        st.markdown(
            """
            **🟡 Medium**
            - 4 rooms
            - Tricky puzzles
            - Requires some thought
            """
        )
    with col3:
        st.markdown(
            """
            **🔴 Hard**
            - 5 rooms
            - Lateral thinking
            - For puzzle masters
            """
        )

    st.info(
        "👉 Select a difficulty in the sidebar and click **Start Game** to begin!"
    )


# ---------------------------------------------------------------------------
# Screen 2: Active gameplay
# ---------------------------------------------------------------------------
def render_game():
    """Render the main gameplay screen."""
    rooms = st.session_state.rooms
    total = len(rooms)
    idx = st.session_state.current_room
    room = rooms[idx]
    solved_count = len(st.session_state.rooms_solved)

    st.title("🏰 AI Dungeon Escape")
    st.markdown("*Built with **WorldWithWeb***")

    progress_value = solved_count / total
    st.progress(progress_value, text=f"Rooms solved: {solved_count} / {total}")

    st.markdown("---")

    st.header(f"🚪 Room {idx + 1} of {total}: {room['name']}")

    puzzle = get_current_puzzle()

    st.markdown(f"*{puzzle['description']}*")
    st.markdown("---")

    st.subheader("🧩 Puzzle")
    st.markdown(f"> {puzzle['puzzle']}")

    already_solved = idx in st.session_state.rooms_solved

    if not already_solved:
        st.markdown("#### Your Answer")
        answer = st.text_input(
            "Type your answer below:",
            key=f"answer_input_{idx}",
            placeholder="Enter your answer here...",
        )

        col_submit, col_hint = st.columns([1, 1])

        with col_submit:
            if st.button("✅ Submit Answer", use_container_width=True):
                if not answer.strip():
                    st.warning("Please type an answer before submitting.")
                else:
                    if check_answer(answer, puzzle["answer"]):
                        st.session_state.rooms_solved.append(idx)
                        st.session_state.answer_correct = True
                        key_name = f"{room['name']} Key"
                        st.session_state.inventory.append(key_name)
                        st.rerun()
                    else:
                        st.error(
                            "❌ That's not right. Try again, or use a hint!"
                        )

        with col_hint:
            hints_used_here = st.session_state.hints_used.get(idx, 0)
            hint_label = (
                f"💡 Hint ({hints_used_here}/3)"
                if hints_used_here < 3
                else "💡 No more hints"
            )
            if st.button(
                hint_label,
                use_container_width=True,
                disabled=hints_used_here >= 3,
            ):
                st.session_state.hints_used[idx] = hints_used_here + 1
                st.rerun()

        hints_used_here = st.session_state.hints_used.get(idx, 0)
        if hints_used_here > 0:
            st.markdown("#### 💡 Hints")
            for h in range(1, hints_used_here + 1):
                st.info(f"**Hint {h}:** {puzzle[f'hint{h}']}")

    else:
        st.success(
            f"🎉 Correct! You solved the puzzle and found the "
            f"**{room['name']} Key**!"
        )

        if solved_count >= total:
            st.session_state.game_won = True
            st.rerun()
        else:
            if st.button(
                "➡️ Proceed to Next Room", use_container_width=True
            ):
                st.session_state.current_room = idx + 1
                st.session_state.answer_correct = False
                st.rerun()


# ---------------------------------------------------------------------------
# Screen 3: Victory / game won
# ---------------------------------------------------------------------------
def render_victory():
    """Show the victory screen with score breakdown."""
    st.balloons()

    st.title("🏰 AI Dungeon Escape")
    st.markdown("*Built with **WorldWithWeb***")

    st.markdown("---")
    st.header("🎉 Congratulations, You Escaped!")

    rooms = st.session_state.rooms
    total = len(rooms)
    solved = len(st.session_state.rooms_solved)
    total_hints = sum(
        st.session_state.hints_used.get(i, 0) for i in range(total)
    )

    result = get_score(
        rooms_solved=solved,
        total_rooms=total,
        total_hints_used=total_hints,
        difficulty=st.session_state.difficulty,
    )

    st.markdown("---")
    st.subheader("🏆 Final Score")

    col_score, col_grade = st.columns(2)
    with col_score:
        st.metric("Score", f"{result['score']} / {result['max_score']}")
        st.metric("Percentage", f"{result['percentage']}%")
    with col_grade:
        grade_colors = {
            "S": "🌟",
            "A": "🥇",
            "B": "🥈",
            "C": "🥉",
            "D": "💧",
        }
        grade_icon = grade_colors.get(result["grade"], "")
        st.metric("Grade", f"{grade_icon} {result['grade']}")
        st.metric("Difficulty", st.session_state.difficulty.capitalize())

    st.info(f"💬 {result['message']}")

    st.markdown("---")
    st.subheader("📊 Room Breakdown")

    for i, room in enumerate(rooms):
        hints = st.session_state.hints_used.get(i, 0)
        hint_stars = "⭐" * (3 - hints) + "☆" * hints
        st.markdown(
            f"**{room['name']}** -- Hints used: {hints}/3  {hint_stars}"
        )

    st.markdown(f"**Total hints used:** {total_hints}")

    st.markdown("---")
    if st.button("🔄 Play Again", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("---")
    st.caption("Built with **WorldWithWeb**")


# ---------------------------------------------------------------------------
# Main routing
# ---------------------------------------------------------------------------
def main():
    """Route to the correct screen based on game state."""
    render_sidebar()

    if st.session_state.game_won:
        render_victory()
    elif st.session_state.game_started:
        render_game()
    else:
        render_welcome()


if __name__ == "__main__":
    main()
