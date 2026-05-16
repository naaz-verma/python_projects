import streamlit as st
from utils import get_gemini_model
from case_generator import (
    CASE_TYPES,
    generate_case,
    get_suspect_prompt,
    get_guilty_suspect,
    check_accusation,
)

# -- Page config ---------------------------------------------------------------
st.set_page_config(page_title="AI Detective", page_icon="🔍", layout="centered")

# -- Session state defaults ----------------------------------------------------
defaults = {
    "case": None,
    "game_phase": "setup",
    "suspects_interviewed": set(),
    "clues_revealed": 0,
    "chat_histories": {},
    "chat_sessions": {},
    "current_suspect": None,
    "notebook": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


def reset_game():
    """Reset every piece of session state back to defaults."""
    for key, val in defaults.items():
        st.session_state[key] = val


# -- Sidebar -------------------------------------------------------------------
with st.sidebar:
    st.header("🔍 AI Detective")
    st.caption("Built with WorldWithWeb")
    st.divider()

    case_type = st.selectbox("Case Type", list(CASE_TYPES.keys()))

    if st.button("Generate New Case", use_container_width=True, type="primary"):
        with st.spinner("Generating mystery case..."):
            model = get_gemini_model()
            if model is None:
                st.error("Gemini API key not found. Add GEMINI_API_KEY to your .env file.")
            else:
                reset_game()
                case = generate_case(model, case_type)
                st.session_state.case = case
                st.session_state.game_phase = "investigate"
                for s in case["suspects"]:
                    st.session_state.chat_histories[s["name"]] = []
                st.rerun()

    if st.button("Reset Game", use_container_width=True):
        reset_game()
        st.rerun()

    st.divider()
    if st.session_state.case:
        st.subheader("Progress")
        total_suspects = len(st.session_state.case["suspects"])
        interviewed = len(st.session_state.suspects_interviewed)
        st.progress(
            interviewed / total_suspects,
            text=f"Suspects interviewed: {interviewed}/{total_suspects}",
        )
        st.progress(
            st.session_state.clues_revealed / 3,
            text=f"Clues found: {st.session_state.clues_revealed}/3",
        )

# -- Title ---------------------------------------------------------------------
st.title("🔍 AI Detective")
st.caption("Built with WorldWithWeb")

# ==============================================================================
# PHASE 1 - SETUP (no case generated yet)
# ==============================================================================
if st.session_state.game_phase == "setup":
    st.markdown("---")
    st.subheader("Welcome, Detective!")
    st.markdown(
        """
You have been called to investigate a mysterious crime.
Your job is to examine the crime scene, interrogate suspects, gather evidence,
and identify the culprit.

**How to play:**

1. **Choose a case type** from the sidebar and click *Generate New Case*.
2. **Examine the crime scene** to learn about the victim and circumstances.
3. **Interrogate suspects** -- ask them questions and look for inconsistencies.
4. **Examine evidence** -- reveal physical clues found at the scene.
5. **Take notes** in your notebook to keep track of your findings.
6. **Make your accusation** when you think you know who did it!

Good luck, Detective. The truth is out there.
"""
    )
    st.info("Select a case type in the sidebar and click **Generate New Case** to begin.")

# ==============================================================================
# PHASE 2 - INVESTIGATE
# ==============================================================================
elif st.session_state.game_phase == "investigate":
    case = st.session_state.case

    tabs = st.tabs([
        "🏠 Crime Scene",
        "🗣 Interrogation",
        "🧩 Evidence",
        "📓 Notebook",
        "⚖️ Make Accusation",
    ])

    # -- Crime Scene tab -------------------------------------------------------
    with tabs[0]:
        st.header(case["title"])
        st.markdown(f"*{case['setting']}*")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Victim")
            st.markdown(f"**Name:** {case['victim']['name']}")
            st.markdown(f"**Role:** {case['victim']['role']}")
            st.markdown(f"{case['victim']['details']}")
        with col2:
            st.subheader("Crime Details")
            st.markdown(f"**Weapon:** {case['crime']['weapon']}")
            st.markdown(f"**Location:** {case['crime']['location']}")
            st.markdown(f"**Time of Death:** {case['crime']['time']}")

        st.divider()
        st.subheader("Discovery")
        st.info(case["crime"]["discovery"])

        st.divider()
        st.subheader("Suspects")
        suspect_cols = st.columns(2)
        for idx, suspect in enumerate(case["suspects"]):
            with suspect_cols[idx % 2]:
                interviewed = suspect["name"] in st.session_state.suspects_interviewed
                badge = " ✅" if interviewed else ""
                st.markdown(f"**{suspect['name']}**{badge}")
                st.caption(f"{suspect['relationship']} -- _{suspect['personality']}_")

    # -- Interrogation tab -----------------------------------------------------
    with tabs[1]:
        st.subheader("Interrogation Room")
        st.markdown("Select a suspect to interrogate. Ask them questions to find inconsistencies.")

        suspect_cols = st.columns(4)
        for idx, suspect in enumerate(case["suspects"]):
            with suspect_cols[idx]:
                interviewed = suspect["name"] in st.session_state.suspects_interviewed
                label = f"{'✅ ' if interviewed else ''}{suspect['name']}"
                if st.button(label, key=f"suspect_btn_{idx}", use_container_width=True):
                    st.session_state.current_suspect = suspect["name"]
                    st.rerun()

        st.divider()

        current = st.session_state.current_suspect
        if current:
            suspect_data = None
            for s in case["suspects"]:
                if s["name"] == current:
                    suspect_data = s
                    break

            if suspect_data is None:
                st.error("Suspect not found.")
            else:
                st.markdown(f"### Interrogating: {current}")
                st.caption(f"{suspect_data['relationship']} -- _{suspect_data['personality']}_")
                st.divider()

                history = st.session_state.chat_histories.get(current, [])
                for msg in history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

                user_input = st.chat_input(
                    f"Ask {current} a question...", key="interrogation_input"
                )
                if user_input:
                    st.session_state.suspects_interviewed.add(current)

                    first_time_note = f"Interviewed {current} ({suspect_data['relationship']})"
                    if first_time_note not in st.session_state.notebook:
                        st.session_state.notebook.append(first_time_note)

                    st.session_state.chat_histories[current].append(
                        {"role": "user", "content": user_input}
                    )

                    if current not in st.session_state.chat_sessions:
                        model = get_gemini_model()
                        if model is None:
                            st.error("Gemini API key not configured.")
                            st.stop()
                        chat = model.start_chat()
                        system_prompt = get_suspect_prompt(suspect_data, case)
                        chat.send_message(system_prompt)
                        st.session_state.chat_sessions[current] = chat

                    chat = st.session_state.chat_sessions[current]

                    try:
                        response = chat.send_message(user_input)
                        reply = response.text
                    except Exception as e:
                        reply = f"*{current} stares silently...* (Error: {e})"

                    st.session_state.chat_histories[current].append(
                        {"role": "assistant", "content": reply}
                    )
                    st.rerun()
        else:
            st.info("Click on a suspect above to begin interrogation.")

    # -- Evidence tab ----------------------------------------------------------
    with tabs[2]:
        st.subheader("Evidence Locker")
        st.markdown("Examine the physical evidence collected from the crime scene.")

        revealed = st.session_state.clues_revealed

        for i in range(revealed):
            st.success(f"**Clue {i + 1}:** {case['clues'][i]}")

        if revealed < 3:
            if st.button(
                "Examine Evidence",
                key="examine_evidence",
                use_container_width=True,
                type="primary",
            ):
                st.session_state.clues_revealed += 1
                clue_idx = st.session_state.clues_revealed - 1
                note = f"Evidence found -- Clue {clue_idx + 1}: {case['clues'][clue_idx]}"
                if note not in st.session_state.notebook:
                    st.session_state.notebook.append(note)
                st.rerun()
            st.caption(f"{3 - revealed} piece(s) of evidence remaining.")
        else:
            st.info("All evidence has been examined.")

    # -- Notebook tab ----------------------------------------------------------
    with tabs[3]:
        st.subheader("Detective's Notebook")
        st.markdown("Your collected notes and observations.")
        st.divider()

        if st.session_state.notebook:
            for idx, note in enumerate(st.session_state.notebook, 1):
                st.markdown(f"{idx}. {note}")
        else:
            st.caption(
                "No notes yet. Interview suspects and examine evidence to "
                "start collecting notes."
            )

        st.divider()
        custom_note = st.text_input("Add a personal note:", key="custom_note_input")
        if st.button("Add Note", key="add_note_btn"):
            if custom_note.strip():
                st.session_state.notebook.append(custom_note.strip())
                st.rerun()

    # -- Accusation tab --------------------------------------------------------
    with tabs[4]:
        st.subheader("Make Your Accusation")
        st.markdown(
            "When you are confident you know who committed the crime, "
            "make your accusation below."
        )
        st.divider()

        suspect_names = [s["name"] for s in case["suspects"]]
        accused = st.selectbox(
            "Who do you accuse?", suspect_names, key="accusation_select"
        )

        reasoning = st.text_area(
            "Explain your reasoning:",
            placeholder=(
                "Describe why you believe this suspect is guilty, "
                "referencing evidence and testimony..."
            ),
            key="accusation_reasoning",
        )

        interviewed_count = len(st.session_state.suspects_interviewed)
        clues_count = st.session_state.clues_revealed

        if interviewed_count < 2:
            st.warning(
                "You should interview at least 2 suspects before making an accusation."
            )
        if clues_count < 1:
            st.warning(
                "You should examine at least 1 piece of evidence before making "
                "an accusation."
            )

        if st.button(
            "Submit Accusation",
            type="primary",
            use_container_width=True,
            key="submit_accusation",
        ):
            if not reasoning.strip():
                st.error("Please provide your reasoning before submitting.")
            else:
                result = check_accusation(case, accused)
                st.session_state.accusation_result = result
                st.session_state.accusation_reasoning = reasoning.strip()
                st.session_state.accusation_name = accused
                st.session_state.game_phase = "solved"
                st.rerun()

# ==============================================================================
# PHASE 3 - SOLVED
# ==============================================================================
elif st.session_state.game_phase == "solved":
    case = st.session_state.case
    result = st.session_state.accusation_result

    st.markdown("---")

    if result["correct"]:
        st.balloons()
        st.success("## Case Solved! Congratulations, Detective!")
        st.markdown(
            f"You correctly identified **{result['guilty_name']}** as the culprit!"
        )
    else:
        st.error("## Wrong Suspect!")
        st.markdown(
            f"You accused **{st.session_state.accusation_name}**, "
            f"but the real culprit was **{result['guilty_name']}**."
        )

    st.divider()

    st.subheader("The Solution")
    st.info(result["solution"])

    st.subheader("Your Reasoning")
    st.markdown(st.session_state.accusation_reasoning)

    st.divider()

    st.subheader("Full Case Breakdown")

    st.markdown(f"**Case:** {case['title']}")
    st.markdown(f"**Setting:** {case['setting']}")

    st.markdown("---")
    st.markdown("**Victim**")
    st.markdown(f"- **{case['victim']['name']}** -- {case['victim']['role']}")
    st.markdown(f"- {case['victim']['details']}")

    st.markdown("---")
    st.markdown("**Crime Details**")
    st.markdown(f"- **Weapon:** {case['crime']['weapon']}")
    st.markdown(f"- **Location:** {case['crime']['location']}")
    st.markdown(f"- **Time of Death:** {case['crime']['time']}")
    st.markdown(f"- **Discovery:** {case['crime']['discovery']}")

    st.markdown("---")
    st.markdown("**All Suspects**")
    for suspect in case["suspects"]:
        guilty_tag = " **(GUILTY)**" if suspect.get("is_guilty") else ""
        interviewed_tag = (
            " -- interviewed"
            if suspect["name"] in st.session_state.suspects_interviewed
            else ""
        )
        with st.expander(f"{suspect['name']}{guilty_tag}{interviewed_tag}"):
            st.markdown(f"**Relationship:** {suspect['relationship']}")
            st.markdown(f"**Personality:** {suspect['personality']}")
            st.markdown(f"**Alibi:** {suspect['alibi']}")
            st.markdown(f"**Motive:** {suspect['motive']}")

    st.markdown("---")
    st.markdown("**Evidence**")
    for i, clue in enumerate(case["clues"], 1):
        revealed = i <= st.session_state.clues_revealed
        tag = "" if revealed else " *(missed)*"
        st.markdown(f"{i}. {clue}{tag}")

    st.markdown("---")
    st.markdown("**Your Investigation Stats**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Suspects Interviewed",
            f"{len(st.session_state.suspects_interviewed)}/4",
        )
    with col2:
        st.metric("Clues Found", f"{st.session_state.clues_revealed}/3")
    with col3:
        st.metric("Notes Taken", len(st.session_state.notebook))

    st.divider()
    if st.button("Play Again", type="primary", use_container_width=True):
        reset_game()
        st.rerun()

# -- Footer -------------------------------------------------------------------
st.markdown("---")
st.caption("AI Detective -- Built with WorldWithWeb | Powered by Gemini")
