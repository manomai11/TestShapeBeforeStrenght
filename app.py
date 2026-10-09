import streamlit as st

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide"
)

# =====================================================
# SESSION
# =====================================================

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


# =====================================================
# LOGIN
# =====================================================

if st.session_state.page == "login":

    left, right = st.columns([3, 2])

    with left:

        st.title("♠ Shape Before Strength")

        st.markdown("""
### A Modern Low-Information Transfer Club System

### Learn • Practice • Improve
""")

        st.markdown("""
เรียนรู้และฝึกประมูลไพ่บริดจ์ตามระบบ

**Shape Before Strength**

✅ วิเคราะห์ Shape ก่อนแต้ม

✅ ใช้การบิดแบบ Transfer

✅ เปิดเผยข้อมูลให้น้อยที่สุด

✅ หา Fit อย่างมีประสิทธิภาพ

✅ ฝึกผ่านโจทย์จริง
""")

    with right:

        st.subheader("เข้าสู่ระบบ")

        with st.form("login_form"):

            name = st.text_input("ชื่อผู้เล่น")

            submitted = st.form_submit_button(
                "🚀 เริ่มฝึก"
            )

            if submitted and name.strip():

                st.session_state.player_name = name
                st.session_state.page = "menu"

                st.rerun()

# =====================================================
# MENU
# =====================================================

elif st.session_state.page == "menu":

    st.title(
        f"ยินดีต้อนรับ {st.session_state.player_name}"
    )

    st.subheader("เลือกหัวข้อฝึก")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if st.button(
            "Opening Practice",
            use_container_width=True
        ):
            st.session_state.page = "opening"
            st.rerun()

    with c2:

        st.button(
            "Response 1C",
            use_container_width=True
        )

        st.button(
            "Response 1D",
            use_container_width=True
        )

        st.button(
            "Response 1H",
            use_container_width=True
        )

        st.button(
            "Response 1S",
            use_container_width=True
        )

        st.button(
            "Response 1NT",
            use_container_width=True
        )

    with c3:

        st.info(
            "พื้นที่สำหรับสถิติ\n\nComing Soon"
        )

    with c4:

        st.info(
            "System Notes\n\nComing Soon"
        )

# =====================================================
# OPENING PRACTICE
# =====================================================

elif st.session_state.page == "opening":

    # ------------------------------------
    # DEMO HAND
    # ------------------------------------

    hcp = 13
    shape = "5332"

    correct_answer = "1C"

    left, middle, right = st.columns([1, 3, 1])

    # ------------------------------------
    # LEFT
    # ------------------------------------

    with left:

        if st.button("⬅ เมนู"):
            st.session_state.page = "menu"
            st.rerun()

        st.write(
            f"Score : {st.session_state.score}"
        )

        st.write(
            f"Question : {st.session_state.question}/20"
        )

        st.write(
            f"Player : {st.session_state.player_name}"
        )

    # ------------------------------------
    # CENTER
    # ------------------------------------

    with middle:

        st.subheader("Opening Practice")

        st.write("You Open")

        st.markdown(
            """
<div style="font-size:36px;line-height:1.8">

♠ AQ852<br>

♥ K73<br>

♦ Q42<br>

♣ J3

</div>
""",
            unsafe_allow_html=True
        )

        st.write(
            f"HCP : {hcp}"
        )

        st.write(
            f"Shape : {shape}"
        )

        st.divider()

        # --------------------------------
        # QUESTION MODE
        # --------------------------------

        if not st.session_state.answered:

            st.write("เลือกคำตอบ")

            if st.button("PASS"):

                st.session_state.user_answer = "PASS"

                if "PASS" == correct_answer:

                    st.session_state.result = "✅ Correct"
                    st.session_state.score += 1

                else:

                    st.session_state.result = "❌ Incorrect"

                st.session_state.answered = True
                st.rerun()

            st.divider()

            cols = st.columns([1,1,1,1,1,1,1])

            for level in range(1, 8):

                with cols[level - 1]:

                    if st.button(
                        str(level),
                        key=f"level_{level}"
                    ):
                        st.session_state.level_selected = level

            if st.session_state.level_selected:

                st.markdown("---")

                level = st.session_state.level_selected

                st.write(
                    f"Level : {level}"
                )

                c1, c2, c3, c4, c5 = st.columns(5)

                suit_map = {
                    "C": "♣",
                    "D": "♦",
                    "H": "♥",
                    "S": "♠",
                    "N": "NT"
                }

                for key, col in zip(
                    suit_map.keys(),
                    [c1, c2, c3, c4, c5]
                ):

                    with col:

                        if st.button(
                            suit_map[key],
                            key=f"{level}_{key}"
                        ):

                            bid = f"{level}{key}"

                            st.session_state.user_answer = bid

                            if bid == correct_answer:

                                st.session_state.result = "✅ Correct"

                                st.session_state.score += 1

                            else:

                                st.session_state.result = "❌ Incorrect"

                            st.session_state.answered = True

                            st.rerun()

        # --------------------------------
        # RESULT MODE
        # --------------------------------

        else:

            st.markdown(
                f"## {st.session_state.result}"
            )

            st.write(
                f"Your Answer : {st.session_state.user_answer}"
            )

            st.write(
                f"Correct Answer : {correct_answer}"
            )

            st.info(
f"""
HCP = {hcp}

Shape = {shape}

11-13 Balanced

Opening = {correct_answer}
"""
            )

            if st.button(
                "Next Question",
                use_container_width=True
            ):

                st.session_state.question += 1

                st.session_state.answered = False

                st.session_state.level_selected = None

                if st.session_state.question > 20:

                    st.session_state.page = "summary"

                st.rerun()

    # ------------------------------------
    # RIGHT
    # ------------------------------------

    with right:

        st.subheader("Cheat Sheet")

        st.info("""
11-13 Balanced → 1C

14-16 Balanced → 1NT

17-19 Balanced
(no M5) → 1C

20-22 Balanced → 2NT
""")

# =====================================================
# SUMMARY
# =====================================================

elif st.session_state.page == "summary":

    st.title("Quiz Complete")

    st.write(
        f"Player : {st.session_state.player_name}"
    )

    st.write(
        f"Correct : {st.session_state.score}"
    )

    st.write(
        f"Wrong : {20 - st.session_state.score}"
    )

    pct = (
        st.session_state.score / 20
    ) * 100

    st.write(
        f"Accuracy : {pct:.0f}%"
    )

    if st.button("Back To Menu"):

        st.session_state.page = "menu"
        st.session_state.question = 1
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.level_selected = None

        st.rerun()
