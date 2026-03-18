import streamlit as st
from utils import get_gemini_model
from story_engine import StoryEngine

# --- Page Config ---
st.set_page_config(page_title="AI Story Forge", page_icon="📖", layout="centered")

# --- Session State ---
if "story_engine" not in st.session_state:
    st.session_state.story_engine = None
if "story_log" not in st.session_state:
    st.session_state.story_log = []
if "current_scene" not in st.session_state:
    st.session_state.current_scene = None
if "game_started" not in st.session_state:
    st.session_state.game_started = False

# --- Sidebar ---
st.sidebar.title("AI Story Forge")
st.sidebar.markdown("*Built with WorldWithWeb*")
st.sidebar.markdown("---")

genre = st.sidebar.selectbox("Choose a genre:", list(StoryEngine.GENRES.keys()))
character_name = st.sidebar.text_input("Your character's name:", value="Alex")

start_btn = st.sidebar.button("Start New Story", type="primary", use_container_width=True)

if st.sidebar.button("Reset", use_container_width=True):
    st.session_state.story_engine = None
    st.session_state.story_log = []
    st.session_state.current_scene = None
    st.session_state.game_started = False
    st.rerun()

# --- Main Area ---
st.title("AI Story Forge")

# --- Start Story ---
if start_btn:
    model = get_gemini_model()
    if not model:
        st.error("Gemini API key not found! Please add your GEMINI_API_KEY to the .env file.")
    else:
        with st.spinner(f"Forging a {genre} story for {character_name}..."):
            try:
                engine = StoryEngine(model)
                result = engine.start_story(genre, character_name)
                st.session_state.story_engine = engine
                st.session_state.current_scene = result
                st.session_state.story_log = [result]
                st.session_state.game_started = True
                st.rerun()
            except Exception as e:
                st.error(f"Error starting story: {e}")

# --- No Story ---
if not st.session_state.game_started:
    st.markdown("### Welcome, storyteller!")
    st.markdown("""
    AI Story Forge creates **unique, AI-generated stories** where YOU make the decisions.

    **How it works:**
    1. Pick a genre and name your character
    2. The AI writes an immersive opening scene
    3. Choose your path at every turn
    4. Your story is one-of-a-kind -- no two playthroughs are alike!

    **Available genres:** Fantasy, Sci-Fi, Horror, Mystery, Adventure
    """)
    st.info("Choose a genre and click **Start New Story** to begin!")

# --- Story In Progress ---
elif st.session_state.current_scene:
    scene = st.session_state.current_scene
    engine = st.session_state.story_engine

    # Turn counter
    st.caption(f"Chapter {engine.turn_count} | Genre: {engine.genre}")

    # Story text
    st.markdown(scene["story"])

    # Choices
    st.markdown("---")
    if scene["choices"]:
        st.markdown("### What do you do?")
        for i, choice in enumerate(scene["choices"]):
            if st.button(f"{i+1}. {choice}", key=f"choice_{engine.turn_count}_{i}", use_container_width=True):
                with st.spinner("The story continues..."):
                    try:
                        result = engine.make_choice(choice)
                        st.session_state.current_scene = result
                        st.session_state.story_log.append(result)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error continuing story: {e}")
    else:
        st.markdown("**The End.**")
        st.balloons()

    # Story log in expander
    if len(st.session_state.story_log) > 1:
        with st.expander("Story so far..."):
            for i, entry in enumerate(st.session_state.story_log[:-1]):
                st.markdown(f"**Chapter {i + 1}**")
                st.markdown(entry["story"][:300] + "...")
                st.markdown("---")

# --- Sidebar stats ---
if st.session_state.game_started and st.session_state.story_engine:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Chapters:** {st.session_state.story_engine.turn_count}")
    st.sidebar.markdown(f"**Genre:** {st.session_state.story_engine.genre}")
