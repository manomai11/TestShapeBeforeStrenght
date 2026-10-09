import streamlit as st
from engine import opening_bid

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

            name = st.text_input(
                "ชื่อผู้เล่น"
            )

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

    c1, c2, c3 = st.columns([2, 2, 1])

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

    with c3:

        st.info(
            "Statistics\n\nComing Soon"
        )

# =====================================================
# OPENING PRACTICE
# =====================================================

elif st.session_state.page == "opening":

    hcp = 13
    shape = "5332"

    import random

    OPENING_QUESTIONS = [

        (13, "5332"),
        (17, "5530"),
        (22, "5332"),

        (14, "4432"),
        (11, "4432"),

        (17, "1345"),
        (14, "2245"),

        (8, "6322"),
        (12, "6322"),
        (15, "6322"),

        (8, "3622"),
        (12, "3622"),
        (15, "3622"),

        (13, "5512"),
        (15, "5161"),

        (17, "3523"),

        (16, "3343")
    ]

    if "current_question" not in st.session_state:
        import random

    OPENING_QUESTIONS = [

        (13, "5332"),
        (17, "5530"),
        (22, "5332"),

        (14, "4432"),
        (11, "4432"),

        (17, "1345"),
        (14, "2245"),

        (8, "6322"),
        (12, "6322"),
        (15, "6322"),

        (8, "3622"),
        (12, "3622"),
        (15, "3622"),

        (13, "5512"),
        (15, "5161"),

        (17, "3523"),

        (16, "3343")
    ]

    if (
        "current_question" not in st.session_state
        or
        st.session_state.current_question is None
    ):

        st.session_state.current_question = random.choice(
            OPENING_QUESTIONS
        )

    hcp, shape = st.session_state.current_question

    correct_answer = opening_bid(
        hcp,
        shape
    )

    left, middle, right = st.columns([1, 3, 1])

    # =================================================
    # LEFT
    # =================================================

    with left:

        if st.button("⬅ เมนู"):
            st.session_state.page = "menu"
            st.rerun()

        st.markdown("### Score")
        st.write(st.session_state.score)

        st.markdown("### Question")
        st.write(
            f"{st.session_state.question}/20"
        )

        st.markdown("### Player")
        st.write(
            st.session_state.player_name
        )

    # =================================================
    # CENTER
    # =================================================

    with middle:

        st.title("Opening Practice")

        st.write("You Open")

        st.markdown(
            """
<div style="font-size:24px; line-height:1.3">

♠ AQ852<br>
♥ K73<br>
♦ Q42<br>
♣ J3

</div>
""",
            unsafe_allow_html=True
        )

        st.divider()

        # =============================================
        # QUESTION MODE
        # =============================================

        if not st.session_state.answered:

            st.subheader("Bidding Box")

            bid_cols = st.columns(
                [2,1,1,1,1,1,1,1,2]
            )

            # PASS

            if bid_cols[1].button(
                "PASS",
                key="pass_btn"
            ):

                bid = "PASS"

                st.session_state.user_answer = bid

                if bid == correct_answer:

                    st.session_state.result = "✅ Correct"

                    st.session_state.score += 1

                else:

                    st.session_state.result = "❌ Incorrect"

                st.session_state.answered = True

                st.rerun()

            # LEVELS

            for level in range(1, 8):

                if bid_cols[level + 1].button(
                    str(level),
                    key=f"level_{level}"
                ):
                    st.session_state.level_selected = level

            # SUITS

            if st.session_state.level_selected:

                st.markdown("---")

                level = st.session_state.level_selected

                suit_cols = st.columns(
                    [2,1,1,1,1,1,2]
                )

                suit_map = {
                    "C": "♣",
                    "D": "♦",
                    "H": "♥",
                    "S": "♠",
                    "N": "NT"
                }

                positions = [1,2,3,4,5]

                for key, pos in zip(
                    suit_map.keys(),
                    positions
                ):

                    if suit_cols[pos].button(
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

        # =============================================
        # RESULT MODE
        # =============================================

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

Opening = {correct_answer}
"""
            
            if st.button("Next Question", use_container_width=True):
        
                st.session_state.question += 1
                st.session_state.answered = False
                st.session_state.level_selected = None
                st.session_state.current_question = None   
            
                if st.session_state.question > 20:
                   st.session_state.page = "summary"

                st.rerun()

    # =================================================
    # RIGHT
    # =================================================

    with right:

        st.subheader("Opening Notes")

        st.info(
"""
11-13 Balanced → 1C

14-16 Balanced → 1NT

17-19 Balanced
No M5 → 1C

20-22 Balanced → 2NT
"""
        )

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
