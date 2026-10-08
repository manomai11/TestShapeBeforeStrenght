import streamlit as st

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide"
)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "page": "login",
    "player_name": "",
    "opening_score": 0,
    "opening_question": 1,
    "show_result": False,
    "user_answer": "",
    "correct_answer": "1S",
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================
# LOGIN
# ==========================================

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

ระบบนี้เน้น

✅ วิเคราะห์ Shape ก่อนแต้ม

✅ ใช้การบิดแบบ Transfer

✅ เปิดเผยข้อมูลให้น้อยที่สุด

✅ หา Fit อย่างมีประสิทธิภาพ

✅ ฝึกผ่านโจทย์จริง

---

### หลังเข้าสู่ระบบ คุณจะสามารถ

✅ ฝึก Opening Bid

✅ ฝึก Response และ Rebid

✅ ดูสถิติความแม่นยำ

✅ ดูประวัติการฝึกย้อนหลัง

✅ เปรียบเทียบผลแต่ละ Session

✅ ทบทวนข้อผิดพลาดที่พบบ่อย
        """)

    with right:

        st.subheader("เข้าสู่ระบบ")

        player_name = st.text_input(
            "ชื่อผู้เล่น"
        )

        st.checkbox(
            "จดจำการเข้าสู่ระบบ",
            value=True
        )

        if st.button(
            "🚀 เริ่มฝึก",
            use_container_width=True
        ):

            if player_name.strip():

                st.session_state.player_name = player_name
                st.session_state.page = "menu"

                st.rerun()

        st.markdown("---")

        st.markdown("""
### ตัวอย่างสถิติ

🏆 จำนวน Session : 127

✅ Opening Accuracy : 88%

✅ Response Accuracy : 79%

✅ Best Score : 20 / 20
        """)

# ==========================================
# MENU
# ==========================================

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

    st.divider()

    st.info("""
Opening

11-13 Balanced = 1C

14-16 Balanced = 1NT

17-19 Balanced No M5 = 1C

20-22 Balanced = 2NT
""")

# ==========================================
# OPENING QUIZ
# ==========================================

elif st.session_state.page == "opening":

    st.title("Opening Practice")

    if st.button("⬅ กลับเมนู"):
        st.session_state.page = "menu"
        st.rerun()

    st.divider()

    st.write(
        f"Question {st.session_state.opening_question} / 20"
    )

    st.write(
        f"Score : {st.session_state.opening_score}"
    )

    st.divider()

    if not st.session_state.show_result:

        st.markdown("""
## Hand

♠ AQ852

♥ K73

♦ Q42

♣ J3
""")

        st.write("What is your opening bid?")

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

            if choice == st.session_state.correct_answer:

                st.session_state.result = "✅ Correct"

                st.session_state.opening_score += 1

            else:

                st.session_state.result = "❌ Incorrect"

            st.session_state.show_result = True

            st.rerun()

    else:

        st.markdown(
            f"## {st.session_state.result}"
        )

        st.write(
            f"Your Answer : {st.session_state.user_answer}"
        )

        st.write(
            f"Correct Answer : {st.session_state.correct_answer}"
        )

        st.info("""
HCP = 13

Shape = 5332

Opening Bid = 1S
""")

        if st.button("Next Question"):

            st.session_state.opening_question += 1
            st.session_state.show_result = False

            if st.session_state.opening_question > 20:
                st.session_state.page = "summary"

            st.rerun()

# ==========================================
# SUMMARY
# ==========================================

elif st.session_state.page == "summary":

    st.title("Quiz Complete")

    st.write(
        f"Player : {st.session_state.player_name}"
    )

    st.write(
        f"Score : {st.session_state.opening_score} / 20"
    )

    percent = (
        st.session_state.opening_score / 20
    ) * 100

    st.write(
        f"Accuracy : {percent:.0f}%"
    )

    if st.button("Back To Menu"):

        st.session_state.page = "menu"

        st.session_state.opening_score = 0
        st.session_state.opening_question = 1
        st.session_state.show_result = False

        st.rerun()
