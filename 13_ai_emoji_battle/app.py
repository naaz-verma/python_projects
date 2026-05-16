import streamlit as st

from utils import get_gemini_model
from emoji_game import (
    EMOJI_SETS,
    get_random_emojis,
    score_story,
    generate_scenario,
    judge_emoji_match,
    get_all_emojis_flat,
    calculate_final_stats,
    get_star_rating,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Emoji Story Battle", page_icon="🎭", layout="centered")

# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------
st.title("🎭 AI Emoji Story Battle")
st.caption("Built with WorldWithWeb")

# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
model = get_gemini_model()
if model is None:
    st.error("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop()

# ---------------------------------------------------------------------------
# Sidebar -- game settings
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Game Settings")
    game_mode_label = st.radio(
        "Game Mode",
        options=["Emoji to Story", "Story to Emoji"],
        index=0,
        help="Choose your battle mode!",
    )
    game_mode = "emoji_to_story" if game_mode_label == "Emoji to Story" else "story_to_emoji"
    total_rounds = st.slider("Number of Rounds", min_value=3, max_value=5, value=3)

    st.divider()
    st.markdown("**How to Play**")
    st.markdown(
        "1. Choose a game mode\n"
        "2. Press **Start Game**\n"
        "3. Complete each round\n"
        "4. Get scored by AI!\n"
    )

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
DEFAULTS = {
    "game_started": False,
    "game_over": False,
    "game_mode": "emoji_to_story",
    "total_rounds": 3,
    "current_round": 1,
    "current_emojis": [],
    "current_scenario": "",
    "current_score": None,
    "rounds_history": [],
    "selected_emojis": [],
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ---------------------------------------------------------------------------
# Helper: initialise a new round
# ---------------------------------------------------------------------------
def init_round():
    """Prepare emojis or scenario for the current round."""
    st.session_state.current_score = None
    if st.session_state.game_mode == "emoji_to_story":
        st.session_state.current_emojis = get_random_emojis(5)
        st.session_state.current_scenario = ""
    else:
        st.session_state.current_scenario = generate_scenario(
            model, st.session_state.current_round
        )
        st.session_state.current_emojis = []
    st.session_state.selected_emojis = []


# ---------------------------------------------------------------------------
# SCREEN 1 -- Welcome (game not started)
# ---------------------------------------------------------------------------
if not st.session_state.game_started and not st.session_state.game_over:
    st.markdown("---")
    st.subheader("Welcome, Emoji Warrior!")
    st.markdown(
        "Test your creativity in an epic battle of emojis and stories. "
        "Choose a mode, write your heart out (or pick the perfect emojis), "
        "and let the AI judge your brilliance!"
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📝 Emoji to Story")
        st.markdown(
            "The AI gives you **5 random emojis**. Your mission: "
            "weave them into a short story (2-5 sentences). "
            "You are scored on **creativity**, **coherence**, and **emoji usage**."
        )
    with col2:
        st.markdown("#### 🎯 Story to Emoji")
        st.markdown(
            "The AI generates a vivid **scenario**. Your mission: "
            "pick **5 emojis** that best represent it. "
            "You are scored on **relevance**, **creativity**, and **coverage**."
        )

    st.markdown("---")
    if st.button("🚀 Start Game", use_container_width=True, type="primary"):
        st.session_state.game_started = True
        st.session_state.game_over = False
        st.session_state.game_mode = game_mode
        st.session_state.total_rounds = total_rounds
        st.session_state.current_round = 1
        st.session_state.rounds_history = []
        init_round()
        st.rerun()

# ---------------------------------------------------------------------------
# SCREEN 3 -- Game Over
# ---------------------------------------------------------------------------
elif st.session_state.game_over:
    st.markdown("---")
    st.subheader("🏆 Game Over -- Final Results")

    stats = calculate_final_stats(st.session_state.rounds_history)
    overall_stars = get_star_rating(stats["avg"], max_score=30)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Score", f"{stats['total']} / {stats['max_possible']}")
    c2.metric("Average Score", f"{stats['avg']} / 30")
    c3.metric("Best Round", f"Round {stats['best_round']} ({stats['best_score']}/30)")

    st.markdown(f"### Overall Rating: {overall_stars}")

    st.markdown("---")
    st.subheader("Round-by-Round Breakdown")

    for i, rnd in enumerate(st.session_state.rounds_history):
        round_stars = get_star_rating(rnd["score"]["total"])
        with st.expander(f"Round {i + 1}  --  {rnd['score']['total']}/30  {round_stars}"):
            if st.session_state.game_mode == "emoji_to_story":
                st.markdown(f"**Emojis:** {' '.join(rnd['emojis'])}")
                st.markdown(f"**Your Story:** {rnd['story']}")
                st.markdown(
                    f"- Creativity: **{rnd['score']['creativity']}**/10\n"
                    f"- Coherence: **{rnd['score']['coherence']}**/10\n"
                    f"- Emoji Usage: **{rnd['score']['emoji_usage']}**/10"
                )
            else:
                st.markdown(f"**Scenario:** {rnd['scenario']}")
                st.markdown(f"**Your Emojis:** {' '.join(rnd['emojis'])}")
                st.markdown(
                    f"- Relevance: **{rnd['score']['relevance']}**/10\n"
                    f"- Creativity: **{rnd['score']['creativity']}**/10\n"
                    f"- Coverage: **{rnd['score']['coverage']}**/10"
                )
            st.info(f"💬 {rnd['score']['feedback']}")

    st.markdown("---")
    if st.button("🔄 Play Again", use_container_width=True, type="primary"):
        for key, val in DEFAULTS.items():
            st.session_state[key] = val
        st.rerun()

# ---------------------------------------------------------------------------
# SCREEN 2 -- Playing
# ---------------------------------------------------------------------------
elif st.session_state.game_started and not st.session_state.game_over:
    progress = st.session_state.current_round / st.session_state.total_rounds
    st.progress(progress)
    st.subheader(f"Round {st.session_state.current_round} of {st.session_state.total_rounds}")

    # -------------------------------------------------------------------
    # MODE A -- Emoji to Story
    # -------------------------------------------------------------------
    if st.session_state.game_mode == "emoji_to_story":
        st.markdown("**Your emojis for this round:**")
        emoji_display = "  ".join(st.session_state.current_emojis)
        st.markdown(
            f"<div style='font-size:3rem; text-align:center; padding:1rem 0;'>{emoji_display}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("Write a **2-5 sentence story** that uses all five emojis above.")

        if st.session_state.current_score is None:
            story = st.text_area(
                "Your Story",
                height=180,
                placeholder="Once upon a time...",
                key=f"story_input_{st.session_state.current_round}",
            )

            if st.button("✅ Submit Story", use_container_width=True, type="primary"):
                if not story or len(story.strip()) < 10:
                    st.warning("Please write at least a couple of sentences!")
                else:
                    with st.spinner("The AI judge is reading your story..."):
                        result = score_story(
                            model,
                            st.session_state.current_emojis,
                            story.strip(),
                            st.session_state.current_round,
                        )
                    st.session_state.current_score = result
                    st.session_state.rounds_history.append(
                        {
                            "round": st.session_state.current_round,
                            "emojis": st.session_state.current_emojis,
                            "story": story.strip(),
                            "score": result,
                        }
                    )
                    st.rerun()

        else:
            result = st.session_state.current_score
            stars = get_star_rating(result["total"])

            st.markdown("---")
            st.markdown(f"### Score: {result['total']}/30  {stars}")

            m1, m2, m3 = st.columns(3)
            m1.metric("Creativity", f"{result['creativity']}/10")
            m2.metric("Coherence", f"{result['coherence']}/10")
            m3.metric("Emoji Usage", f"{result['emoji_usage']}/10")

            st.info(f"💬 {result['feedback']}")

            if st.session_state.current_round < st.session_state.total_rounds:
                if st.button("➡️ Next Round", use_container_width=True, type="primary"):
                    st.session_state.current_round += 1
                    init_round()
                    st.rerun()
            else:
                if st.button("🏆 See Results", use_container_width=True, type="primary"):
                    st.session_state.game_over = True
                    st.session_state.game_started = False
                    st.rerun()

    # -------------------------------------------------------------------
    # MODE B -- Story to Emoji
    # -------------------------------------------------------------------
    else:
        st.markdown("**Scenario:**")
        st.markdown(
            f"<div style='font-size:1.15rem; background:var(--secondary-background-color); color:var(--text-color); padding:1rem; "
            f"border-radius:0.5rem; margin-bottom:1rem;'>"
            f"📜 <em>{st.session_state.current_scenario}</em></div>",
            unsafe_allow_html=True,
        )
        st.markdown("Pick **exactly 5 emojis** that best represent the scenario above.")

        if st.session_state.current_score is None:
            for category, emojis in EMOJI_SETS.items():
                st.markdown(f"**{category.title()}**")
                cols = st.columns(len(emojis))
                for idx, emoji in enumerate(emojis):
                    with cols[idx]:
                        is_selected = emoji in st.session_state.selected_emojis
                        label = f"{emoji} {'[X]' if is_selected else ''}"
                        if st.button(
                            label,
                            key=f"emoji_{category}_{idx}_{st.session_state.current_round}",
                            use_container_width=True,
                        ):
                            if emoji in st.session_state.selected_emojis:
                                st.session_state.selected_emojis.remove(emoji)
                            elif len(st.session_state.selected_emojis) < 5:
                                st.session_state.selected_emojis.append(emoji)
                            st.rerun()

            if st.session_state.selected_emojis:
                sel_display = "  ".join(st.session_state.selected_emojis)
                st.markdown(
                    f"<div style='font-size:2.5rem; text-align:center; padding:0.75rem 0;'>"
                    f"{sel_display}</div>",
                    unsafe_allow_html=True,
                )
                st.caption(f"{len(st.session_state.selected_emojis)}/5 selected")
            else:
                st.caption("No emojis selected yet. Click emojis above to pick them.")

            if st.button("✅ Submit Emojis", use_container_width=True, type="primary"):
                if len(st.session_state.selected_emojis) != 5:
                    st.warning("Please select exactly 5 emojis!")
                else:
                    player_emojis_str = " ".join(st.session_state.selected_emojis)
                    with st.spinner("The AI judge is evaluating your picks..."):
                        result = judge_emoji_match(
                            model,
                            st.session_state.current_scenario,
                            player_emojis_str,
                        )
                    st.session_state.current_score = result
                    st.session_state.rounds_history.append(
                        {
                            "round": st.session_state.current_round,
                            "scenario": st.session_state.current_scenario,
                            "emojis": list(st.session_state.selected_emojis),
                            "score": result,
                        }
                    )
                    st.rerun()

        else:
            result = st.session_state.current_score
            stars = get_star_rating(result["total"])

            sel_display = "  ".join(st.session_state.selected_emojis)
            st.markdown(
                f"<div style='font-size:2.5rem; text-align:center; padding:0.5rem 0;'>"
                f"{sel_display}</div>",
                unsafe_allow_html=True,
            )

            st.markdown("---")
            st.markdown(f"### Score: {result['total']}/30  {stars}")

            m1, m2, m3 = st.columns(3)
            m1.metric("Relevance", f"{result['relevance']}/10")
            m2.metric("Creativity", f"{result['creativity']}/10")
            m3.metric("Coverage", f"{result['coverage']}/10")

            st.info(f"💬 {result['feedback']}")

            if st.session_state.current_round < st.session_state.total_rounds:
                if st.button("➡️ Next Round", use_container_width=True, type="primary"):
                    st.session_state.current_round += 1
                    init_round()
                    st.rerun()
            else:
                if st.button("🏆 See Results", use_container_width=True, type="primary"):
                    st.session_state.game_over = True
                    st.session_state.game_started = False
                    st.rerun()
