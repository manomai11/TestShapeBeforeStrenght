import streamlit as st

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
    "score": 0,
    "question": 1,
    "answered": False,
    "result": "",
    "user_answer": "",
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

        name = st.text_input("ชื่อผู้เล่น")

        if st.button("🚀 เริ่มฝึก", use_container_width=True):

            if name.strip():

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

    col1, col2 = st.columns(2)

    with col1:

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

    with col2:

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

# =====================================================
# OPENING QUIZ
# =====================================================

elif st.session_state.page == "opening":

    st.title("Opening Practice")

    if st.button("⬅ กลับเมนู"):
        st.session_state.page = "menu"
        st.rerun()

    st.divider()

    c1, c2 = st.columns([1,1])

    with c1:

        st.write(
            f"Question : {st.session_state.question} / 20"
        )

    with c2:

        st.write(
            f"Score : {st.session_state.score}"
        )

    st.divider()

    # -----------------------------------
    # DEMO HAND
    # -----------------------------------

    hcp = 13
    shape = "5332"
    correct_answer = "1C"

    # -----------------------------------
    # QUESTION SCREEN
    # -----------------------------------

    if not st.session_state.answered:

        st.markdown("""
## Hand

♠ AQ852

♥ K73

♦ Q42

♣ J3
""")

        st.write(
            "What is your opening bid?"
        )

        bids = [
            "PASS",

            "1C","1D","1H","1S","1N",

            "2C","2D","2H","2S","2N",

            "3C","3D","3H","3S","3N",

            "4C","4D","4H","4S"
        ]

        choice = st.selectbox(
            "Choose Bid",
            bids
        )

        if st.button("Submit Bid"):

            st.session_state.user_answer = choice

            if choice == correct_answer:

                st.session_state.result = "✅ Correct"

                st.session_state.score += 1

            else:

                st.session_state.result = "❌ Incorrect"

            st.session_state.answered = True

            st.rerun()

    # -----------------------------------
    # RESULT SCREEN
    # -----------------------------------

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

Opening Bid = {correct_answer}
"""
        )

        if st.button("Next Question"):

            st.session_state.question += 1
            st.session_state.answered = False

            if st.session_state.question > 20:

                st.session_state.page = "summary"

            st.rerun()

# =====================================================
# SUMMARY
# =====================================================

elif st.session_state.page == "summary":

    st.title("Quiz Complete")

    st.write(
        f"Player : {st.session_state.player_name}"
    )

    st.write(
        f"Score : {st.session_state.score} / 20"
    )

    accuracy = (
        st.session_state.score / 20
    ) * 100

    st.write(
        f"Accuracy : {accuracy:.0f}%"
    )

    if st.button("Back To Menu"):

        st.session_state.page = "menu"
        st.session_state.question = 1
        st.session_state.score = 0
        st.session_state.answered = False

        st.rerun()
