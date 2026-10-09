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

    # ----------------------------------
    # DEMO QUESTION
    # ----------------------------------

    hcp = 13
    shape = "5332"

    correct_answer = opening_bid(
        hcp,
        shape
    )

    left, middle, right = st.columns([1, 3, 1])

    # ----------------------------------
    # LEFT
    # ----------------------------------

    with left:

        if st.button("⬅ เมนู"):
            st.session_state.page = "menu"
            st.rerun()

        st.markdown("### Score")

        st.write(st.session_state.score)

        st.markdown("### Question")

        st.write(
            f"{st.session_state.question} / 20"
        )

        st.markdown("### Player")

        st.write(
            st.session_state.player_name
        )

    # ----------------------------------
    # CENTER
    # ----------------------------------

    with middle:

        st.title("Opening Practice")

        st.write("You Open")

        # ไพ่
        st.markdown(
            """
<div style="font-size:24px;line-height:1.4">

♠ AQ852<br>
♥ K73<br>
♦ Q42<br>
♣ J3

</div>
""",
            unsafe_allow_html=True
        )

        st.divider()

        # ------------------------------
        # QUESTION MODE
        # ------------------------------

        if not st.session_state.answered:

            st.subheader("Bidding Box")

            top = st.columns(
                [2,1,1,1,1,1,1,1,2]
            )

            if top[1].button("PASS"):

                bid = "PASS"

                st.session_state.user_answer = bid

                if bid == correct_answer:

                    st.session_state.result = "✅ Correct"
                    st.session_state.score += 1

                else:

                    st.session_state.result = "❌ Incorrect"

                st.session_state.answered = True
                st.rerun()

            lv_cols = st.columns(
                [2,1,1,1,1,1,1,1,2]
            )

            for level in range(1, 8):

                if lv_cols[level].button(
                    str(level),
                    key=f"lvl_{level}"
                ):
                    st.session_state.level_selected = level

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
                    
