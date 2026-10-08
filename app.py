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
    
    name_input = st.text_input("Enter your name to start:")
    if st.button("Start Practice"):
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
    
    if st.button("Opening Practice (1D Response)"):
        st.session_state.page = "opening"
        st.rerun()

# ==================================================
# OPENING PRACTICE
# ==================================================

elif st.session_state.page == "opening":

    # ใช้หัวข้อกระชับ เพื่อไม่ให้กินพื้นที่แนวตั้ง
    st.markdown("### Opening & Response Practice")

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
    # DEMO DATA
    # --------------------------------------------------
    hcp = 13
    shape = "5332"
    is_bal = shape in engine.BALANCED_SHAPES
    correct_answer = engine.response_1d(hcp=hcp, shape=shape, balanced=is_bal)

    # --------------------------------------------------
    # LAYOUT แบ่งซ้าย (ไพ่และข้อมูล) - ขวา (Bidding Box)
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
            # ปุ่ม PASS ขนาดกะทัดรัด
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
            
            # บีบพื้นที่ปุ่ม 1-7 ให้ยาวไม่เกินช่วงสั้นๆ (ใช้สัดส่วนคอลัมน์แคบลง)
            lvl_cols = st.columns([1, 1, 1, 1, 1, 1, 1, 5])
            for i in range(1, 8):
                with lvl_cols[i - 1]:
                    if st.button(str(i), key=f"lvl_{i}"):
                        st.session_state.level_selected = i

            # --------------------------------------------------
            # SHOW SUITS (เมื่อเลือก Level แล้วจะแสดงขึ้นมาทันทีในกรอบเดิม)
            # --------------------------------------------------
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
            # แสดงผลลัพธ์
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
