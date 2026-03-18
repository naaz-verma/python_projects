import streamlit as st
import plotly.graph_objects as go
from analyzer import analyze_password, is_common_password
from cracker_sim import brute_force_sim, dictionary_attack_sim, hash_password
from generator import generate_password, generate_passphrase

# --- Page Config ---
st.set_page_config(page_title="Password Fortress", page_icon="🔒", layout="centered")

st.title("Password Fortress")
st.markdown("*Built with WorldWithWeb*")

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Analyze Password",
    "Crack Simulator",
    "Generate Password",
    "Learn"
])

# ==================== TAB 1: ANALYZE ====================
with tab1:
    st.header("Password Strength Analyzer")
    password = st.text_input("Enter a password to analyze:", type="password", key="analyze_input")

    if st.button("Analyze", key="analyze_btn") and password:
        result = analyze_password(password)

        # Strength gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result["score"],
            title={"text": f"Strength: {result['strength']}"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": result["color"]},
                "steps": [
                    {"range": [0, 20], "color": "#ffcccc"},
                    {"range": [20, 40], "color": "#ffe0b2"},
                    {"range": [40, 60], "color": "#fff9c4"},
                    {"range": [60, 80], "color": "#c8e6c9"},
                    {"range": [80, 100], "color": "#a5d6a7"},
                ],
            },
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

        # Common password check
        if is_common_password(password):
            st.error("This password is in the list of commonly leaked passwords! Change it immediately.")

        # Details
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Character Analysis")
            st.markdown(f"- Length: **{result['length']}** characters")
            st.markdown(f"- Uppercase: {'Yes' if result['has_upper'] else 'No'}")
            st.markdown(f"- Lowercase: {'Yes' if result['has_lower'] else 'No'}")
            st.markdown(f"- Numbers: {'Yes' if result['has_digit'] else 'No'}")
            st.markdown(f"- Special chars: {'Yes' if result['has_special'] else 'No'}")
            st.markdown(f"- Entropy: **{result['entropy']} bits**")

        with col2:
            st.markdown("#### Estimated Crack Times")
            for method, time_str in result["crack_times"].items():
                st.markdown(f"- {method}: **{time_str}**")

        # Patterns
        if result["patterns"]:
            st.warning("**Weak patterns detected:**")
            for pattern in result["patterns"]:
                st.markdown(f"- {pattern}")
        else:
            st.success("No weak patterns detected!")

# ==================== TAB 2: CRACK SIMULATOR ====================
with tab2:
    st.header("Crack Simulator")
    st.info("This is a safe, educational simulation. It only cracks passwords you type here -- nothing else.")

    sim_password = st.text_input("Enter a password to crack (up to 6 chars for brute force):", key="crack_input")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Brute Force Attack")
        st.markdown("Tries every possible combination of characters.")
        if st.button("Run Brute Force", key="brute_btn") and sim_password:
            if len(sim_password) > 6:
                st.warning("Brute force demo limited to 6 characters. Try a shorter password!")
            else:
                progress_bar = st.progress(0, text="Starting brute force attack...")
                status_text = st.empty()

                def update_progress(attempts, current_guess):
                    status_text.markdown(f"Trying: `{current_guess}` | Attempts: **{attempts:,}**")

                result = brute_force_sim(sim_password, max_length=6, callback=update_progress)
                progress_bar.empty()
                status_text.empty()

                if result["cracked"]:
                    st.success(f"Cracked: **{result['password']}**")
                    st.markdown(f"- Attempts: **{result['attempts']:,}**")
                    st.markdown(f"- Time: **{result['time']}s**")
                    st.markdown(f"- Speed: **{result['speed']:,} guesses/sec**")
                else:
                    st.info(f"Not cracked in {result['attempts']:,} attempts.")

    with col2:
        st.subheader("Dictionary Attack")
        st.markdown("Tries common passwords and their variations.")
        if st.button("Run Dictionary Attack", key="dict_btn") and sim_password:
            with st.spinner("Trying dictionary words..."):
                result = dictionary_attack_sim(sim_password)
            if result["cracked"]:
                st.error(f"Cracked: **{result['password']}**")
                st.markdown(f"- Attempts: **{result['attempts']:,}**")
                st.markdown(f"- Time: **{result['time']}s**")
                st.markdown("Your password is a common word or variation!")
            else:
                st.success(f"Not found in {result['attempts']:,} dictionary entries!")

    # Hash display
    st.markdown("---")
    st.subheader("Password Hashes")
    hash_input = st.text_input("See how your password is stored:", key="hash_input")
    if hash_input:
        st.code(f"SHA-256: {hash_password(hash_input, 'sha256')}")
        st.code(f"MD5:     {hash_password(hash_input, 'md5')}")
        st.markdown("*Websites store hashes, not your actual password. Attackers try to reverse these hashes.*")

# ==================== TAB 3: GENERATE ====================
with tab3:
    st.header("Password Generator")

    gen_type = st.radio("Type:", ["Random Password", "Passphrase"], horizontal=True)

    if gen_type == "Random Password":
        length = st.slider("Length:", 8, 32, 16)
        col1, col2 = st.columns(2)
        with col1:
            use_upper = st.checkbox("Uppercase (A-Z)", value=True)
            use_lower = st.checkbox("Lowercase (a-z)", value=True)
        with col2:
            use_digits = st.checkbox("Numbers (0-9)", value=True)
            use_special = st.checkbox("Special (!@#$%)", value=True)
        exclude_ambiguous = st.checkbox("Exclude ambiguous characters (0/O, 1/l)")

        if st.button("Generate Password", key="gen_pwd_btn"):
            pwd = generate_password(length, use_upper, use_lower, use_digits, use_special, exclude_ambiguous)
            st.code(pwd, language=None)
            # Show strength of generated password
            result = analyze_password(pwd)
            st.markdown(f"Strength: **{result['strength']}** ({result['score']}/100) | Entropy: **{result['entropy']} bits**")

    else:
        num_words = st.slider("Number of words:", 3, 6, 4)
        separator = st.selectbox("Separator:", ["-", ".", "_", " "], index=0)
        capitalize = st.checkbox("Capitalize words", value=True)

        if st.button("Generate Passphrase", key="gen_phrase_btn"):
            phrase = generate_passphrase(num_words, separator, capitalize)
            st.code(phrase, language=None)
            result = analyze_password(phrase)
            st.markdown(f"Strength: **{result['strength']}** ({result['score']}/100) | Entropy: **{result['entropy']} bits**")
            st.markdown("*Passphrases are easier to remember and often stronger than random passwords!*")

# ==================== TAB 4: LEARN ====================
with tab4:
    st.header("Password Security 101")

    st.markdown("""
    ### Why Password Security Matters
    - **81%** of data breaches involve weak or stolen passwords
    - The average person has **100+** online accounts
    - Attackers use automated tools that try **billions** of guesses per second

    ### How Passwords Get Cracked

    | Method | How It Works | Speed |
    |--------|-------------|-------|
    | **Brute Force** | Tries every combination (aaa, aab, aac...) | Slow but thorough |
    | **Dictionary** | Tries common words and variations | Fast for common passwords |
    | **Rainbow Table** | Pre-computed hash lookups | Nearly instant |
    | **Credential Stuffing** | Uses leaked password databases | Depends on leaks |

    ### Rules for Strong Passwords
    1. **Length > Complexity** -- a 20-char passphrase beats a short complex password
    2. **Never reuse** passwords across sites
    3. **Use a password manager** (Bitwarden, 1Password, KeePass)
    4. **Enable 2FA** wherever possible
    5. **Avoid personal info** (birthdays, pet names, etc.)

    ### What is Entropy?
    Entropy measures the randomness of your password in **bits**.
    - **< 28 bits**: Very weak (cracked instantly)
    - **28-35 bits**: Weak (cracked in minutes)
    - **36-59 bits**: Reasonable (cracked in days-years)
    - **60-127 bits**: Strong (cracked in millions of years)
    - **128+ bits**: Very strong (practically uncrackable)

    > Formula: `entropy = log2(pool_size ^ length)`
    >
    > A 12-character password using uppercase + lowercase + digits + symbols:
    > `log2(94^12) = 78.7 bits`
    """)
