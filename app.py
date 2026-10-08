import streamlit as st

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide"
)

# ==================================================
# SESSION
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
# LOGIN
# ==================================================

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

            player_name = st.text_input(
                "ชื่อผู้เล่น"
            )

            submitted = st.form_submit_button(
                "🚀 เริ่มฝึก"
            )

            if submitted:

                if player_name.strip():

                    st.session_state.player_name = player_name
                    st.session_state.page = "menu"

                    st.rerun()

# ==================================================
# MENU
# ==================================================

elif st.session_state.page == "menu":

    st.title(
        f"ยินดีต้อนรับ {st.session_state.player_name}"
    )

    st.subheader("เลือกหัวข้อฝึก")

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "Opening Practice",
            use_container_width=True
        ):
            st.session_state.page = "opening"
            st.rerun()

        st.button(
            "Response 1C",
            use_container_width=True
        )

        st.button(
            "Response 1D",
            use_container_width=True
        )

    with c2:

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

# ==================================================
# OPENING PRACTICE
# ==================================================

elif st.session_state.page == "opening":

    st.title("Opening Practice")

    if st.button("⬅ กลับเมนู"):

        st.session_state.page = "menu"
        st.rerun()

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.write(
            f"Question : {st.session_state.question} / 20"
        )

    with c2:

        st.write(
            f"Score : {st.session_state.score}"
        )

    st.divider()

    # ----------------------------------
    # DEMO HAND
    # ----------------------------------

    hcp = 13
    shape = "5332"

    correct_answer = "1C"

    # ----------------------------------
    # HAND
    # ----------------------------------

    st.markdown(
        """
<div style="font-size:36px; line-height:1.8">

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

    # ----------------------------------
    # QUESTION
    # ----------------------------------

    if not st.session_state.answered:

        st.subheader("Bidding Box")

        if st.button("PASS"):

            st.session_state.user_answer = "PASS"

            if (
                st.session_state.user_answer
                ==
                correct_answer
            ):
                st.session_state.result = "✅ Correct"
                st.session_state.score += 1
            else:
                st.session_state.result = "❌ Incorrect"

            st.session_state.answered = True
            st.rerun()

        st.markdown("---")

        cols = st.columns(7)

        for i in range(1, 8):

            with cols[i - 1]:

                if st.button(
                    str(i)
                ):
                    st.session_state.level_selected = i

        # -----------------------------
        # SHOW SUITS
        # -----------------------------

        if st.session_state.level_selected:

            level = st.session_state.level_selected

            st.write(
                f"Level Selected : {level}"
            )

            c1, c2, c3, c4, c5 = st.columns(5)

            suit_map = {
                "C": "♣",
                "D": "♦",
                "H": "♥",
                "S": "♠",
                "N": "NT",
            }

            for key, col in zip(
                suit_map.keys(),
                [c1, c2, c3, c4, c5]
            ):

                with col:

                    if st.button(
                        suit_map[key],
                        key=f"{level}{key}"
                    ):

                        bid = f"{level}{key}"

                        st.session_state.user_answer = bid

                        if bid == correct_answer:

                            st.session_state.result = (
                                "✅ Correct"
                            )

                            st.session_state.score += 1

                        else:

                            st.session_state.result = (
                                "❌ Incorrect"
