"""
AI Word Duel - Streamlit Web App
A creative word challenge game where players compete against AI judgment.
Play solo or duel a friend across multiple rounds of word challenges.
"""

import streamlit as st
from utils import get_gemini_model
from word_game import (
    generate_category,
    judge_answer,
    calculate_round_score,
    calculate_final_score,
    get_max_possible_score,
    get_rank_title,
)

# --- Page Config ---
st.set_page_config(page_title="AI Word Duel", page_icon="⚔️", layout="centered")

# --- Sidebar ---
st.sidebar.title("⚔️ AI Word Duel")
st.sidebar.markdown("*Built with WorldWithWeb*")
st.sidebar.markdown("---")

difficulty = st.sidebar.radio("Difficulty:", ["Easy", "Medium", "Hard"])
total_rounds = st.sidebar.slider("Number of Rounds:", min_value=3, max_value=7, value=5)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
**Scoring:**
- Easy: 1x multiplier
- Medium: 1.5x multiplier
- Hard: 2x multiplier

Creativity scored 1-10 by AI.
"""
)

# --- Session State ---
defaults = {
    "game_started": False,
    "game_over": False,
    "game_mode": None,
    "difficulty": "Easy",
    "total_rounds": 5,
    "current_round": 1,
    "current_category": None,
    "current_judgment": None,
    "player_rounds": [],
    "player1_rounds": [],
    "player2_rounds": [],
    "duel_phase": "player1",
    "player1_name": "Player 1",
    "player2_name": "Player 2",
    "error": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --- Helper Functions ---


def reset_game():
    """Reset all session state to defaults."""
    for key, value in defaults.items():
        st.session_state[key] = value


def start_game(mode):
    """Initialize a new game."""
    model = get_gemini_model()
    if not model:
        st.session_state.error = (
            "Gemini API key not found! Add your GEMINI_API_KEY to the .env file."
        )
        return

    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.game_mode = mode
    st.session_state.difficulty = difficulty
    st.session_state.total_rounds = total_rounds
    st.session_state.current_round = 1
    st.session_state.current_category = None
    st.session_state.current_judgment = None
    st.session_state.player_rounds = []
    st.session_state.player1_rounds = []
    st.session_state.player2_rounds = []
    st.session_state.duel_phase = "player1"
    st.session_state.error = None

    category = generate_category(model, difficulty, 1, total_rounds)
    st.session_state.current_category = category


def generate_next_category():
    """Generate category for the next round."""
    model = get_gemini_model()
    if not model:
        st.session_state.error = "Lost connection to AI model."
        return
    round_num = st.session_state.current_round
    category = generate_category(
        model,
        st.session_state.difficulty,
        round_num,
        st.session_state.total_rounds,
    )
    st.session_state.current_category = category
    st.session_state.current_judgment = None


def submit_answer_solo(answer):
    """Submit and judge an answer for solo mode."""
    if not answer or not answer.strip():
        st.session_state.error = "Please enter an answer!"
        return

    model = get_gemini_model()
    if not model:
        st.session_state.error = "Lost connection to AI model."
        return

    st.session_state.error = None
    category = st.session_state.current_category["category"]
    judgment = judge_answer(model, category, answer.strip(), st.session_state.difficulty)
    score = calculate_round_score(judgment, st.session_state.difficulty)

    st.session_state.current_judgment = judgment
    st.session_state.player_rounds.append(
        {
            "round": st.session_state.current_round,
            "category": category,
            "hint": st.session_state.current_category.get("hint", ""),
            "answer": answer.strip(),
            "judgment": judgment,
            "score": score,
        }
    )


def submit_answer_duel(answer, player):
    """Submit and judge an answer for duel mode."""
    if not answer or not answer.strip():
        st.session_state.error = "Please enter an answer!"
        return

    model = get_gemini_model()
    if not model:
        st.session_state.error = "Lost connection to AI model."
        return

    st.session_state.error = None
    category = st.session_state.current_category["category"]
    judgment = judge_answer(model, category, answer.strip(), st.session_state.difficulty)
    score = calculate_round_score(judgment, st.session_state.difficulty)

    round_data = {
        "round": st.session_state.current_round,
        "category": category,
        "hint": st.session_state.current_category.get("hint", ""),
        "answer": answer.strip(),
        "judgment": judgment,
        "score": score,
    }

    if player == "player1":
        st.session_state.player1_rounds.append(round_data)
        st.session_state.duel_phase = "player2"
    else:
        st.session_state.player2_rounds.append(round_data)
        st.session_state.duel_phase = "results"


def advance_round():
    """Move to the next round or end the game."""
    next_round = st.session_state.current_round + 1
    if next_round > st.session_state.total_rounds:
        st.session_state.game_over = True
    else:
        st.session_state.current_round = next_round
        st.session_state.current_judgment = None
        st.session_state.duel_phase = "player1"
        generate_next_category()


# --- Title ---
st.title("⚔️ AI Word Duel")
st.caption("Built with WorldWithWeb")

# --- Error Display ---
if st.session_state.error:
    st.error(st.session_state.error)

# =====================================================================
# SCREEN 1: Mode Selection (not started)
# =====================================================================
if not st.session_state.game_started:
    st.markdown("---")
    st.markdown(
        """
### Welcome to AI Word Duel!

Test your vocabulary and creativity against an AI judge. Each round, you will
receive a unique word challenge category. Your goal is to come up with the most
creative valid answer possible.

**How to play:**
1. Choose your difficulty and number of rounds in the sidebar.
2. Pick Solo Challenge or 2-Player Duel below.
3. Read the category and hint, then type your best answer.
4. The AI judges your answer for validity and creativity (1-10).
5. Score points based on creativity multiplied by difficulty bonus.
"""
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Solo Challenge")
        st.markdown(
            "Play by yourself and try to beat your own high score. "
            "Perfect for practice and improving your word skills."
        )
        if st.button("Start Solo Game", type="primary", use_container_width=True):
            start_game("solo")
            st.rerun()

    with col2:
        st.subheader("2-Player Duel")
        st.markdown(
            "Challenge a friend! Both players answer the same category, "
            "then compare scores. Who has the sharper word skills?"
        )
        if st.button("Start Duel", type="primary", use_container_width=True):
            start_game("duel")
            st.rerun()

# =====================================================================
# SCREEN 4: Game Over
# =====================================================================
elif st.session_state.game_over:
    st.markdown("---")

    if st.session_state.game_mode == "solo":
        final = calculate_final_score(st.session_state.player_rounds)
        max_score = get_max_possible_score(
            st.session_state.total_rounds, st.session_state.difficulty
        )
        rank = get_rank_title(final["total_score"], max_score)

        st.header("Game Over!")
        st.subheader(f"Your Rank: {rank}")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Score", f"{final['total_score']}/{max_score}")
        col2.metric("Valid Answers", f"{final['valid_answers']}/{final['rounds_played']}")
        col3.metric("Avg Creativity", f"{final['avg_creativity']}/10")
        col4.metric("Difficulty", st.session_state.difficulty)

        score_pct = final["total_score"] / max_score if max_score > 0 else 0
        st.progress(score_pct)

        st.markdown("---")
        st.subheader("Round-by-Round Breakdown")

        for r in st.session_state.player_rounds:
            valid_icon = "✅" if r["judgment"]["valid"] else "❌"
            with st.expander(
                f"Round {r['round']}: {r['category']} -- {valid_icon} {r['score']} pts"
            ):
                st.markdown(f"**Category:** {r['category']}")
                st.markdown(f"**Hint:** {r['hint']}")
                st.markdown(f"**Your Answer:** {r['answer']}")
                st.markdown(f"**Valid:** {'Yes' if r['judgment']['valid'] else 'No'}")
                st.markdown(f"**Creativity Score:** {r['judgment']['score']}/10")
                st.markdown(f"**AI Feedback:** {r['judgment']['reason']}")
                st.markdown(f"**Points Earned:** {r['score']}")

    else:
        final_p1 = calculate_final_score(st.session_state.player1_rounds)
        final_p2 = calculate_final_score(st.session_state.player2_rounds)
        max_score = get_max_possible_score(
            st.session_state.total_rounds, st.session_state.difficulty
        )
        rank_p1 = get_rank_title(final_p1["total_score"], max_score)
        rank_p2 = get_rank_title(final_p2["total_score"], max_score)

        p1_name = st.session_state.player1_name
        p2_name = st.session_state.player2_name

        st.header("Duel Complete!")

        if final_p1["total_score"] > final_p2["total_score"]:
            st.success(f"**{p1_name} wins the duel!**")
        elif final_p2["total_score"] > final_p1["total_score"]:
            st.success(f"**{p2_name} wins the duel!**")
        else:
            st.info("**It's a tie!** Both players matched wits equally.")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{p1_name}")
            st.markdown(f"**Rank:** {rank_p1}")
            st.metric("Total Score", f"{final_p1['total_score']}/{max_score}")
            st.metric(
                "Valid Answers",
                f"{final_p1['valid_answers']}/{final_p1['rounds_played']}",
            )
            st.metric("Avg Creativity", f"{final_p1['avg_creativity']}/10")

        with col2:
            st.subheader(f"{p2_name}")
            st.markdown(f"**Rank:** {rank_p2}")
            st.metric("Total Score", f"{final_p2['total_score']}/{max_score}")
            st.metric(
                "Valid Answers",
                f"{final_p2['valid_answers']}/{final_p2['rounds_played']}",
            )
            st.metric("Avg Creativity", f"{final_p2['avg_creativity']}/10")

        st.markdown("---")
        st.subheader("Round-by-Round Breakdown")

        for i in range(len(st.session_state.player1_rounds)):
            r1 = st.session_state.player1_rounds[i]
            r2 = st.session_state.player2_rounds[i]
            round_winner = ""
            if r1["score"] > r2["score"]:
                round_winner = f" -- {p1_name} wins!"
            elif r2["score"] > r1["score"]:
                round_winner = f" -- {p2_name} wins!"
            else:
                round_winner = " -- Tie!"

            with st.expander(f"Round {r1['round']}: {r1['category']}{round_winner}"):
                st.markdown(f"**Category:** {r1['category']}")
                st.markdown(f"**Hint:** {r1['hint']}")
                st.markdown("---")

                rc1, rc2 = st.columns(2)
                with rc1:
                    st.markdown(f"**{p1_name}**")
                    st.markdown(f"Answer: {r1['answer']}")
                    valid1 = "Yes" if r1["judgment"]["valid"] else "No"
                    st.markdown(f"Valid: {valid1}")
                    st.markdown(f"Creativity: {r1['judgment']['score']}/10")
                    st.markdown(f"Points: {r1['score']}")
                    st.markdown(f"*{r1['judgment']['reason']}*")

                with rc2:
                    st.markdown(f"**{p2_name}**")
                    st.markdown(f"Answer: {r2['answer']}")
                    valid2 = "Yes" if r2["judgment"]["valid"] else "No"
                    st.markdown(f"Valid: {valid2}")
                    st.markdown(f"Creativity: {r2['judgment']['score']}/10")
                    st.markdown(f"Points: {r2['score']}")
                    st.markdown(f"*{r2['judgment']['reason']}*")

    st.markdown("---")
    if st.button("Play Again", type="primary", use_container_width=True):
        reset_game()
        st.rerun()

# =====================================================================
# SCREEN 2: Solo Play
# =====================================================================
elif st.session_state.game_started and st.session_state.game_mode == "solo":
    current = st.session_state.current_round
    total = st.session_state.total_rounds

    st.progress(current / total)
    st.markdown(
        f"**Round {current} of {total}** | Difficulty: **{st.session_state.difficulty}**"
    )
    st.markdown("---")

    if st.session_state.current_category:
        st.subheader("Category:")
        st.info(f"**{st.session_state.current_category['category']}**")
        st.markdown(f"*Hint: {st.session_state.current_category.get('hint', '')}*")
    else:
        st.warning("Generating category...")
        generate_next_category()
        st.rerun()

    already_judged = len(st.session_state.player_rounds) >= current

    if not already_judged:
        answer = st.text_input(
            "Your answer:",
            key=f"solo_answer_{current}",
            placeholder="Type your most creative answer...",
        )

        if st.button("Submit Answer", type="primary", use_container_width=True):
            with st.spinner("AI is judging your answer..."):
                submit_answer_solo(answer)
            st.rerun()

    else:
        round_data = st.session_state.player_rounds[-1]
        judgment = round_data["judgment"]

        st.markdown(f"**Your answer:** {round_data['answer']}")
        st.markdown("---")

        if judgment["valid"]:
            st.success(f"**Valid answer!** +{round_data['score']} points")
        else:
            st.error("**Invalid answer.** 0 points")

        col1, col2 = st.columns(2)
        col1.metric("Creativity Score", f"{judgment['score']}/10")
        col2.metric("Points Earned", round_data["score"])

        st.markdown(f"**AI Feedback:** {judgment['reason']}")

        running_total = sum(r["score"] for r in st.session_state.player_rounds)
        st.markdown(f"**Running Total: {running_total} points**")

        st.markdown("---")

        if current < total:
            if st.button("Next Round", type="primary", use_container_width=True):
                advance_round()
                st.rerun()
        else:
            if st.button("See Results", type="primary", use_container_width=True):
                st.session_state.game_over = True
                st.rerun()

# =====================================================================
# SCREEN 3: Duel Play
# =====================================================================
elif st.session_state.game_started and st.session_state.game_mode == "duel":
    current = st.session_state.current_round
    total = st.session_state.total_rounds
    phase = st.session_state.duel_phase

    if current == 1 and phase == "player1" and len(st.session_state.player1_rounds) == 0:
        st.subheader("Enter Player Names")
        name1 = st.text_input("Player 1 name:", value="Player 1", key="input_p1_name")
        name2 = st.text_input("Player 2 name:", value="Player 2", key="input_p2_name")

        if st.button("Start Duel!", type="primary", use_container_width=True):
            st.session_state.player1_name = name1.strip() if name1.strip() else "Player 1"
            st.session_state.player2_name = name2.strip() if name2.strip() else "Player 2"
            st.rerun()
        st.stop()

    p1_name = st.session_state.player1_name
    p2_name = st.session_state.player2_name

    st.progress(current / total)
    st.markdown(
        f"**Round {current} of {total}** | Difficulty: **{st.session_state.difficulty}**"
    )
    st.markdown("---")

    if not st.session_state.current_category:
        st.warning("Generating category...")
        generate_next_category()
        st.rerun()

    if phase == "player1":
        st.subheader(f"{p1_name}'s Turn")
        st.warning(f"**{p2_name}, please look away!**")
        st.markdown("---")

        st.markdown("**Category:**")
        st.info(f"**{st.session_state.current_category['category']}**")
        st.markdown(f"*Hint: {st.session_state.current_category.get('hint', '')}*")

        answer = st.text_input(
            f"{p1_name}'s answer:",
            key=f"duel_p1_answer_{current}",
            placeholder="Type your most creative answer...",
        )

        if st.button("Submit Answer", type="primary", use_container_width=True):
            with st.spinner("AI is judging..."):
                submit_answer_duel(answer, "player1")
            st.rerun()

    elif phase == "player2":
        st.subheader(f"{p2_name}'s Turn")
        st.warning(f"**{p1_name}, please look away!**")
        st.markdown("---")

        st.markdown("**Category:**")
        st.info(f"**{st.session_state.current_category['category']}**")
        st.markdown(f"*Hint: {st.session_state.current_category.get('hint', '')}*")

        answer = st.text_input(
            f"{p2_name}'s answer:",
            key=f"duel_p2_answer_{current}",
            placeholder="Type your most creative answer...",
        )

        if st.button("Submit Answer", type="primary", use_container_width=True):
            with st.spinner("AI is judging..."):
                submit_answer_duel(answer, "player2")
            st.rerun()

    elif phase == "results":
        st.subheader(f"Round {current} Results")
        st.markdown("---")

        r1 = st.session_state.player1_rounds[-1]
        r2 = st.session_state.player2_rounds[-1]

        st.markdown(f"**Category:** {st.session_state.current_category['category']}")
        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### {p1_name}")
            st.markdown(f"**Answer:** {r1['answer']}")
            if r1["judgment"]["valid"]:
                st.success(f"Valid! +{r1['score']} pts")
            else:
                st.error("Invalid. 0 pts")
            st.metric("Creativity", f"{r1['judgment']['score']}/10")
            st.markdown(f"*{r1['judgment']['reason']}*")

        with col2:
            st.markdown(f"### {p2_name}")
            st.markdown(f"**Answer:** {r2['answer']}")
            if r2["judgment"]["valid"]:
                st.success(f"Valid! +{r2['score']} pts")
            else:
                st.error("Invalid. 0 pts")
            st.metric("Creativity", f"{r2['judgment']['score']}/10")
            st.markdown(f"*{r2['judgment']['reason']}*")

        st.markdown("---")
        if r1["score"] > r2["score"]:
            st.success(f"**{p1_name} wins this round!**")
        elif r2["score"] > r1["score"]:
            st.success(f"**{p2_name} wins this round!**")
        else:
            st.info("**This round is a tie!**")

        p1_total = sum(r["score"] for r in st.session_state.player1_rounds)
        p2_total = sum(r["score"] for r in st.session_state.player2_rounds)

        score_col1, score_col2 = st.columns(2)
        score_col1.metric(f"{p1_name} Total", f"{p1_total} pts")
        score_col2.metric(f"{p2_name} Total", f"{p2_total} pts")

        st.markdown("---")

        if current < total:
            if st.button("Next Round", type="primary", use_container_width=True):
                advance_round()
                st.rerun()
        else:
            if st.button("See Final Results", type="primary", use_container_width=True):
                st.session_state.game_over = True
                st.rerun()

# --- Footer ---
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "⚔️ AI Word Duel | Built with WorldWithWeb"
    "</div>",
    unsafe_allow_html=True,
)
