import streamlit as st
from quiz_logic import generate_quiz, check_answer, calculate_score
from utils import get_openai_client

# --- Page Config ---
st.set_page_config(page_title="AI Quiz Master", page_icon="🧠", layout="centered")

# --- Session State Init ---
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []
if "quiz_complete" not in st.session_state:
    st.session_state.quiz_complete = False
if "score" not in st.session_state:
    st.session_state.score = None

# --- Sidebar ---
st.sidebar.title("AI Quiz Master")
st.sidebar.markdown("*Built with WorldWithWeb*")
st.sidebar.markdown("---")

topic = st.sidebar.text_input("Enter any topic:", placeholder="e.g. Space, Cricket, Marvel, Python...")
difficulty = st.sidebar.radio("Difficulty:", ["Easy", "Medium", "Hard"])
num_questions = st.sidebar.slider("Number of questions:", 3, 10, 5)

generate_btn = st.sidebar.button("Generate Quiz!", type="primary", use_container_width=True)

if st.sidebar.button("Reset", use_container_width=True):
    st.session_state.quiz_data = None
    st.session_state.current_q = 0
    st.session_state.user_answers = []
    st.session_state.quiz_complete = False
    st.session_state.score = None
    st.rerun()

# --- Main Area ---
st.title("AI Quiz Master")

# --- Generate Quiz ---
if generate_btn and topic:
    client = get_openai_client()
    if not client:
        st.error("OpenAI API key not found! Please add your key to the .env file.")
    else:
        with st.spinner(f"Generating a {difficulty.lower()} quiz about **{topic}**..."):
            try:
                questions = generate_quiz(client, topic, difficulty, num_questions)
                st.session_state.quiz_data = questions
                st.session_state.current_q = 0
                st.session_state.user_answers = []
                st.session_state.quiz_complete = False
                st.session_state.score = None
                st.rerun()
            except Exception as e:
                st.error(f"Error generating quiz: {e}")

# --- No Quiz Yet ---
if st.session_state.quiz_data is None:
    st.markdown("### How it works")
    st.markdown("""
    1. **Pick any topic** -- literally anything! History, gaming, science, Bollywood...
    2. **Choose difficulty** -- Easy, Medium, or Hard
    3. **Take the quiz** -- Answer each question and see how you score
    4. **Learn** -- Read the explanations for every answer
    """)
    st.info("Enter a topic in the sidebar and click **Generate Quiz!** to start.")

# --- Quiz In Progress ---
elif not st.session_state.quiz_complete:
    questions = st.session_state.quiz_data
    idx = st.session_state.current_q
    total = len(questions)
    q = questions[idx]

    # Progress bar
    st.progress((idx) / total, text=f"Question {idx + 1} of {total}")

    # Question
    st.markdown(f"### Q{idx + 1}. {q['question']}")

    # Options as buttons
    cols = st.columns(2)
    for i, (key, value) in enumerate(q["options"].items()):
        col = cols[i % 2]
        if col.button(f"{key}. {value}", key=f"opt_{idx}_{key}", use_container_width=True):
            st.session_state.user_answers.append(key)

            if idx + 1 < total:
                st.session_state.current_q += 1
            else:
                st.session_state.quiz_complete = True
                st.session_state.score = calculate_score(
                    st.session_state.user_answers, questions
                )
            st.rerun()

# --- Quiz Complete ---
else:
    score = st.session_state.score
    questions = st.session_state.quiz_data

    # Score header
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Score", f"{score['correct']}/{score['total']}")
    col2.metric("Percentage", f"{score['percentage']}%")

    if score["percentage"] >= 80:
        col3.metric("Grade", "Excellent!")
    elif score["percentage"] >= 60:
        col3.metric("Grade", "Good Job!")
    elif score["percentage"] >= 40:
        col3.metric("Grade", "Keep Learning!")
    else:
        col3.metric("Grade", "Try Again!")

    # Progress bar colored by score
    st.progress(score["percentage"] / 100)

    # Detailed Results
    st.markdown("### Review Your Answers")
    for i, result in enumerate(score["results"]):
        q = questions[i]
        if result["is_correct"]:
            st.success(f"**Q{i+1}. {result['question']}**")
            st.markdown(f"Your answer: **{result['user_answer']}** -- Correct!")
        else:
            st.error(f"**Q{i+1}. {result['question']}**")
            st.markdown(f"Your answer: **{result['user_answer']}** | Correct: **{result['correct_answer']}. {q['options'][result['correct_answer']]}**")

        st.markdown(f"*{result['explanation']}*")
        st.markdown("---")
