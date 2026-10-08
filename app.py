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
# LOGIN PAGE (รองรับการกด Enter)
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
# MENU PAGE (แสดงโหมดฝึกซ้อมทั้งหมด)
# ==================================================

elif st.session_state.page == "menu":
    st.title(f"Welcome, {st.session_state.player_name}!")
    st.subheader("Select Practice Mode")
    
    modes = [
        ("Opening Practice", "opening"),
        ("Response 1C", "resp_1c"),
        ("Response 1D", "resp_1d"),
        ("Response 1H", "resp_1h"),
        ("Response 1S", "resp_1s"),
        ("Response 1N", "resp_1n"),
    ]

    col1, col2, col3 = st.columns(3)
    for idx, (label, mode_key) in enumerate(modes):
        target_col = [col1, col2, col3][idx % 3]
        with target_col:
            if st.button(label, use_container_width=True):
                st.session_state.practice_mode = mode_key
                st.session_state.page = "practice"
                st.session_state.question = 1
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.user_answer = ""
                st.session_state.level_selected = None
                st.rerun()

# ==================================================
# PRACTICE SCREEN (เชื่อมโยง Engine และ Bidding Box กระชับ)
# ==================================================

elif st.session_state.page == "practice":

    mode_titles = {
        "opening": "Opening Practice",
        "resp_1c": "Response to 1C",
        "resp_1d": "Response to 1D",
        "resp_1h": "Response to 1H",
        "resp_1s": "Response to 1S",
        "resp_1n": "Response to 1N",
    }

    current_title = mode_titles.get(st.session_state.practice_mode, "Practice")
    st.markdown(f"### {current_title}")

    col_top1, col_top2, col_top3 = st.columns([2, 6, 2])
    with col_top1:
        if st.button("◀ กลับเมนู"):
            st.session_state.page = "menu"
            st.rerun()
    with col_top2:
        st.write(f"**Question:** {st.session_state.question} / 20")
    with col_top3:
        st.write(f"**Score:** {st.session_state.score}")

    st.markdown("---")

    # --------------------------------------------------
    # DEMO DATA (สามารถปรับเปลี่ยนเป็นการสุ่มมือไพ่จริงจาก Engine ได้ในอนาคต)
    # --------------------------------------------------
    hcp = 13
    shape = "5332"
    is_bal = shape in engine.BALANCED_SHAPES

    # เรียกใช้ฟังก์ชันตรวจสอบคำตอบจาก engine.py ตามโหมดที่เลือก
    mode = st.session_state.practice_mode
    if mode == "resp_1c":
        correct_answer = engine.response_1c(hcp=hcp, shape=shape, balanced=is_bal)
    elif mode == "resp_1d":
        correct_answer = engine.response_1d(hcp=hcp, shape=shape, balanced=is_bal)
    else:
        # โหมดอื่นๆ สามารถเพิ่มฟังก์ชันใน engine.py แล้วมาผูกเพิ่มตรงนี้ได้ครับ
        correct_answer = "1N" 

    # --------------------------------------------------
    # LAYOUT แสดงมือไพ่ (ซ้าย) และ Bidding Box (ขวา)
    # --------------------------------------------------
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### Your Hand")
        st.markdown(
            """
            <div style="font-size:28px; line-height:1.6">
            ♠ AQ852<br>
            ♥ K73<br>
            ♦ Q42<br>
            ♣ J3
            </div>
            """,
            unsafe_allow_html=True
        )
        st.text(f"HCP : {hcp}  |  Shape : {shape}")

    with col_right:
        st.subheader("Bidding Box")

        if not st.session_state.answered:
            if st.button("PASS", key="btn_pass"):
                st.session_state.user_answer = "PASS"
                if st.session_state.user_answer == correct_answer:
                    st.session_state.result = "✅ Correct"
                    st.session_state.score += 1
                else:
                    st.session_state.result = "❌ Incorrect"
                st.session_state.answered = True
                st.rerun()

            st.write("Select Level:")
            
            # ควบคุมความกว้างปุ่ม 1-7 ให้กระชับ
            lvl_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 5])
            for i in range(1, 8):
                with lvl_cols[i - 1]:
                    if st.button(str(i), key=f"lvl_{i}"):
                        st.session_state.level_selected = i

            # แสดงชุดไพ่ (Suit) เมื่อเลือก Level แล้ว
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
                                st.session_state.result = "❌ Incorrect"

                            st.session_state.answered = True
                            st.rerun()
        else:
            st.markdown(f"### {st.session_state.result}")
            st.write(f"**Your Answer:** {st.session_state.user_answer}")
            st.write(f"**Correct Answer:** {correct_answer}")

            if st.button("Next Question"):
                st.session_state.answered = False
                st.session_state.user_answer = ""
                st.session_state.result = ""
                st.session_state.level_selected = None
                st.session_state.question += 1
                st.rerun()
