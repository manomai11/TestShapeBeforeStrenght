import streamlit as st
import engine

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

defaults = {
    "page": "login",
    "player_name": "",
    "practice_mode": "",
    "questions_list": [],
    "question": 1,
    "score": 0,
    "answered": False,
    "result": "",
    "user_answer": "",
    "level_selected": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==================================================
# LOGIN PAGE
# ==================================================

if st.session_state.page == "login":
    st.title("♠ Shape Before Strength")
    st.subheader("Bridge Bidding Practice App")
    
    with st.form("login_form"):
        name_input = st.text_input("Enter your name to start:")
        submit_button = st.form_submit_button("Start Practice")
        
        if submit_button:
            if name_input.strip() != "":
                st.session_state.player_name = name_input
                st.session_state.page = "menu"
                st.rerun()
            else:
                st.warning("Please enter your name first.")

# ==================================================
# MENU PAGE
# ==================================================

elif st.session_state.page == "menu":
    st.title(f"Welcome, {st.session_state.player_name}!")
    st.subheader("Select Practice Mode")
    
    modes = [
        ("Opening Practice (Practicing Opening Bids)", "opening"),
        ("Response to 1C (Responding to Partner's 1C)", "resp_1c"),
        ("Response to 1D (Responding to Partner's 1D)", "resp_1d"),
        ("Response to 1H (Responding to Partner's 1H)", "resp_1h"),
        ("Response to 1S (Responding to Partner's 1S)", "resp_1s"),
        ("Response to 1N (Responding to Partner's 1N)", "resp_1n"),
    ]

    col1, col2 = st.columns(2)
    for idx, (label, mode_key) in enumerate(modes):
        target_col = col1 if idx % 2 == 0 else col2
        with target_col:
            if st.button(label, use_container_width=True):
                st.session_state.practice_mode = mode_key
                st.session_state.page = "practice"
                # สุ่มโจทย์ใหม่ 20 ข้อทันทีที่กดเลือกโหมด
                st.session_state.questions_list = engine.generate_practice_questions(mode_key, 20)
                st.session_state.question = 1
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.user_answer = ""
                st.session_state.level_selected = None
                st.rerun()

# ==================================================
# PRACTICE SCREEN
# ==================================================

elif st.session_state.page == "practice":

    mode_titles = {
        "opening": "Opening Practice: What is your opening bid?",
        "resp_1c": "Response to 1C: Partner opened 1C, what is your bid?",
        "resp_1d": "Response to 1D: Partner opened 1D, what is your bid?",
        "resp_1h": "Response to 1H: Partner opened 1H, what is your bid?",
        "resp_1s": "Response to 1S: Partner opened 1S, what is your bid?",
        "resp_1n": "Response to 1N: Partner opened 1N, what is your bid?",
    }

    current_title = mode_titles.get(st.session_state.practice_mode, "Bridge Practice")
    st.markdown(f"### {current_title}")

    col_top1, col_top2, col_top3 = st.columns([2, 6, 2])
    with col_top1:
        if st.button("◀ Back to Menu"):
            st.session_state.page = "menu"
            st.rerun()
    with col_top2:
        st.write(f"**Question:** {st.session_state.question} / 20")
    with col_top3:
        st.write(f"**Score:** {st.session_state.score}")

    st.markdown("---")

    # ดึงโจทย์ข้อปัจจุบันจากรายการที่สุ่มไว้ (Index = question - 1)
    q_data = st.session_state.questions_list[st.session_state.question - 1]
    hcp = q_data["hcp"]
    shape = q_data["shape"]
    correct_answer = q_data["correct_answer"]

    # --------------------------------------------------
    # LAYOUT
    # --------------------------------------------------
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### Your Hand")
        # แสดงรูปทรงจำลองจาก Shape (เช่น 5332 แปลงเป็นการแสดงผลคร่าวๆ)
        st.markdown(
            f"""
            <div style="font-size:26px; line-height:1.6">
            Shape Code: {shape}<br>
            HCP: <b>{hcp}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        st.subheader("Bidding Box")

        if not st.session_state.answered:
            if st.button("PASS", key="btn_pass"):
                st.session_state.user_answer = "PASS"
                if st.session_state.user_answer == correct_answer:
                    st.session_state.result = "✅ Correct"
                    st.session_state.score += 1
                else:
                    st.session_state.result = f"❌ Incorrect (Correct: {correct_answer})"
                st.session_state.answered = True
                st.rerun()

            st.write("Select Level:")
            
            lvl_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 5])
            for i in range(1, 8):
                with lvl_cols[i - 1]:
                    if st.button(str(i), key=f"lvl_{i}"):
                        st.session_state.level_selected = i

            if st.session_state.level_selected:
                level = st.session_state.level_selected
                st.markdown(f"**Level:** {level}")

                suit_cols = st.columns(5)
                suit_map = {
                    "C": "♣",
                    "D": "♦",
                    "H": "♥",
                    "S": "♠",
                    "N": "NT",
                }

                for idx, (key, symbol) in enumerate(suit_map.items()):
                    with suit_cols[idx]:
                        if st.button(symbol, key=f"suit_{level}_{key}"):
                            bid = f"{level}{key}"
                            st.session_state.user_answer = bid

                            if bid == correct_answer:
                                st.session_state.result = "✅ Correct"
                                st.session_state.score += 1
                            else:
                                st.session_state.result = f"❌ Incorrect (Correct: {correct_answer})"

                            st.session_state.answered = True
                            st.rerun()
        else:
            st.markdown(f"### {st.session_state.result}")
            st.write(f"**Your Answer:** {st.session_state.user_answer}")
            st.write(f"**Correct Answer:** {correct_answer}")

            # เช็คว่าครบ 20 ข้อหรือยัง
            if st.session_state.question < 20:
                if st.button("Next Question"):
                    st.session_state.answered = False
                    st.session_state.user_answer = ""
                    st.session_state.result = ""
                    st.session_state.level_selected = None
                    st.session_state.question += 1
                    st.rerun()
            else:
                st.success(f"🎉 Practice Completed! Your final score is {st.session_state.score} / 20")
                if st.button("Back to Menu"):
                    st.session_state.page = "menu"
                    st.rerun()
