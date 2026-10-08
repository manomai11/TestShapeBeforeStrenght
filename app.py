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
    "temp_bid": None
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

---

### หลังเข้าสู่ระบบ

✅ ฝึก Opening Bid

✅ ฝึก Response และ Rebid

✅ ดูสถิติความแม่นยำ

✅ ดูประวัติการฝึกย้อนหลัง

✅ เปรียบเทียบผลแต่ละ Session

✅ ทบทวนข้อผิดพลาดที่พบบ่อย
""")

    with right:

        st.subheader("เข้าสู่ระบบ")

        name = st.text_input(
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

            if name.strip():

                st.session_state.player_name = name
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

    # =====================================
    # DEMO HAND
    # =====================================

    hcp = 13
    shape = "5332"

    correct_answer = "1C"

    # =====================================
    # HAND
    # =====================================

    st.markdown("""
## Hand

♠ AQ852

♥ K73

♦ Q42

♣ J3
""")

    st.write(
        f"HCP : {hcp}"
    )

    st.write(
        f"Shape : {shape}"
    )

    st.divider()

    # =====================================
    # QUESTION MODE
    # =====================================

    if not st.session_state.answered:

        st.write(
            "What is your opening bid?"
        )

        bids = ["PASS"]

        for level in range(1, 8):

            bids.extend([
                f"{level}C",
                f"{level}D",
                f"{level}H",
                f"{level}S",
                f"{level}N",
            ])

        cols = st.columns(5)

        for index, bid in enumerate(bids):

            col = cols[index % 5]

            with col:

                if st.button(
                    bid,
                    key=f"bid_{bid}"
                ):
                    st.session_state.temp_bid = bid

        st.divider()

        st.write(
            f"Selected Bid : {st.session_state.temp_bid}"
        )

        if st.session_state.temp_bid:

            if st.button(
                "Submit Bid",
                use_container_width=True
            ):

                st.session_state.user_answer = (
                    st.session_state.temp_bid
                )

                if (
                    st.session_state.user_answer
                    ==
                    correct_answer
                ):

                    st.session_state.result = (
                        "✅ Correct"
                    )

                    st.session_state.score += 1

                else:

                    st.session_state.result = (
                        "❌ Incorrect"
                    )

                st.session_state.answered = True

                st.rerun()

    # =====================================
    # RESULT MODE
    # =====================================

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

Open 1C
"""
        )

        if st.button(
            "Next Question",
            use_container_width=True
        ):

            st.session_state.question += 1

            st.session_state.answered = False
            st.session_state.temp_bid = None

            if st.session_state.question > 20:

                st.session_state.page = "summary"

            st.rerun()

# ==================================================
# SUMMARY
# ==================================================

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

    accuracy = (
        st.session_state.score / 20
    ) * 100

    st.write(
        f"Accuracy : {accuracy:.0f}%"
    )

    if st.button(
        "Back To Menu"
    ):

        st.session_state.page = "menu"

        st.session_state.question = 1
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.temp_bid = None

        st.rerun()
