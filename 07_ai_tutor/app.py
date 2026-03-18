import streamlit as st
from utils import get_gemini_model
from tutor_engine import TutorEngine
from subjects import get_subject_names, get_subject, LEVELS, LEARNING_MODES

# --- Page Config ---
st.set_page_config(page_title="AI Tutor", page_icon="🎓", layout="centered")

# --- Session State ---
if "tutor" not in st.session_state:
    st.session_state.tutor = None
if "tutor_messages" not in st.session_state:
    st.session_state.tutor_messages = []
if "session_active" not in st.session_state:
    st.session_state.session_active = False
if "learning_mode" not in st.session_state:
    st.session_state.learning_mode = "Explain"

# --- Sidebar ---
st.sidebar.title("AI Tutor")
st.sidebar.markdown("*Built with WorldWithWeb*")
st.sidebar.markdown("---")

subject = st.sidebar.selectbox("Subject:", get_subject_names())
subject_info = get_subject(subject)

if subject_info:
    topic = st.sidebar.selectbox(f"{subject_info['emoji']} Topic:", subject_info["topics"])
else:
    topic = st.sidebar.text_input("Topic:", value="General")

level = st.sidebar.radio("Your level:", LEVELS)

# Learning mode selector
st.sidebar.markdown("---")
st.sidebar.markdown("**Learning Mode:**")
mode = st.sidebar.radio(
    "How should the tutor help?",
    list(LEARNING_MODES.keys()),
    format_func=lambda x: f"{x} -- {LEARNING_MODES[x]}",
    label_visibility="collapsed",
)
st.session_state.learning_mode = mode

# Start session
if st.sidebar.button("Start Session", type="primary", use_container_width=True):
    model = get_gemini_model()
    if not model:
        st.sidebar.error("Gemini API key not found! Add your GEMINI_API_KEY to the .env file.")
    else:
        tutor = TutorEngine(model, subject, topic, level)
        with st.spinner(f"Starting {topic} session..."):
            greeting = tutor.start_session()
        st.session_state.tutor = tutor
        st.session_state.tutor_messages = [
            {"role": "assistant", "content": greeting}
        ]
        st.session_state.session_active = True
        st.rerun()

# Session summary
if st.session_state.session_active and st.session_state.tutor:
    if st.sidebar.button("Get Session Summary", use_container_width=True):
        with st.spinner("Generating summary..."):
            summary = st.session_state.tutor.get_session_summary()
        st.session_state.tutor_messages.append(
            {"role": "assistant", "content": f"**Session Summary:**\n\n{summary}"}
        )
        st.rerun()

if st.sidebar.button("End Session", use_container_width=True):
    st.session_state.tutor = None
    st.session_state.tutor_messages = []
    st.session_state.session_active = False
    st.rerun()

# Session stats
if st.session_state.session_active and st.session_state.tutor:
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Subject:** {subject}")
    st.sidebar.markdown(f"**Topic:** {topic}")
    st.sidebar.markdown(f"**Level:** {level}")
    st.sidebar.markdown(f"**Questions:** {st.session_state.tutor.questions_asked}")

# --- Main Area ---
st.title("AI Tutor")

if not st.session_state.session_active:
    st.markdown("### Your personal AI learning assistant")
    st.markdown("""
    AI Tutor uses the **Socratic method** -- instead of just giving you answers,
    it guides you to discover them yourself through questions and hints.

    **How to use:**
    1. Pick your subject and topic
    2. Choose your level
    3. Select a learning mode:
       - **Explain** -- Get clear explanations with examples
       - **Practice** -- Get problems to solve with hints
       - **Quiz Me** -- Test your understanding
       - **Simplify** -- Break down complex ideas
       - **Real World** -- See practical applications
    4. Ask anything -- the AI adapts to how you learn!
    """)

    # Subject cards
    st.markdown("### Available Subjects")
    cols = st.columns(3)
    for i, (name, info) in enumerate(zip(get_subject_names(), [get_subject(s) for s in get_subject_names()])):
        with cols[i % 3]:
            st.markdown(f"**{info['emoji']} {name}**")
            st.caption(info["description"])

    st.info("Choose a subject in the sidebar and click **Start Session**.")

else:
    # Active tutoring session
    tutor = st.session_state.tutor

    # Chat display
    for msg in st.session_state.tutor_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a question or respond to the tutor...")

    if user_input:
        st.session_state.tutor_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = tutor.ask(user_input, mode=st.session_state.learning_mode)
                st.markdown(response)
                st.session_state.tutor_messages.append({"role": "assistant", "content": response})
