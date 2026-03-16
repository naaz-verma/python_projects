import streamlit as st
from utils import get_openai_client
from chatbot import Chatbot
from personalities import get_personality_names, get_personality, create_custom_personality

# --- Page Config ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# --- Session State ---
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "current_personality" not in st.session_state:
    st.session_state.current_personality = None

# --- Sidebar ---
st.sidebar.title("AI Chatbot")
st.sidebar.markdown("*Built with WorldWithWeb*")
st.sidebar.markdown("---")

# Personality selection
mode = st.sidebar.radio("Personality:", ["Pre-built", "Custom"])

if mode == "Pre-built":
    personality_name = st.sidebar.selectbox("Choose a character:", get_personality_names())
    personality = get_personality(personality_name)
else:
    st.sidebar.markdown("#### Create Your Character")
    custom_name = st.sidebar.text_input("Character name:", value="Professor Quirky")
    custom_desc = st.sidebar.text_area("Description:", value="A quirky professor who loves trivia")
    custom_style = st.sidebar.text_input("Speaking style:", value="Academic but fun, uses big words then explains them")
    custom_greeting = st.sidebar.text_input("Greeting:", value="Ah, a new student! Splendid!")
    personality = create_custom_personality(custom_name, custom_desc, custom_style, custom_greeting)
    personality_name = custom_name

# Start chat button
if st.sidebar.button("Start Chat", type="primary", use_container_width=True):
    client = get_openai_client()
    if not client:
        st.sidebar.error("API key not found! Add your key to the .env file.")
    else:
        bot = Chatbot(client, personality)
        st.session_state.chatbot = bot
        st.session_state.current_personality = personality
        greeting = bot.get_greeting()
        st.session_state.chat_messages = [
            {"role": "assistant", "content": greeting}
        ]
        st.rerun()

if st.sidebar.button("Reset Chat", use_container_width=True):
    st.session_state.chatbot = None
    st.session_state.chat_messages = []
    st.session_state.current_personality = None
    st.rerun()

# Export chat
if st.session_state.chatbot and len(st.session_state.chat_messages) > 1:
    st.sidebar.markdown("---")
    export = st.session_state.chatbot.export_chat()
    st.sidebar.download_button(
        "Download Chat",
        export,
        file_name="chat_export.txt",
        mime="text/plain",
        use_container_width=True,
    )

# --- Main Area ---
st.title("AI Chatbot")

if not st.session_state.chatbot:
    st.markdown("### Pick a personality and start chatting!")
    st.markdown("""
    Choose from fun pre-built characters or create your own:

    | Character | Personality |
    |-----------|------------|
    | **Captain Redbeard** | Swashbuckling pirate captain |
    | **The Bard** | Shakespeare himself |
    | **Chuckles** | Sarcastic stand-up comedian |
    | **Dr. Eureka** | Eccentric mad scientist |
    | **Coach Blaze** | Motivational life coach |
    | **Custom** | Design your own! |
    """)
    st.info("Select a personality in the sidebar and click **Start Chat**.")
else:
    # Display personality info
    p = st.session_state.current_personality
    st.caption(f"Chatting with **{p.get('emoji', '')} {p.get('name', 'Bot')}**")

    # Chat display
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Show user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.chat(user_input)
                st.markdown(response)
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
