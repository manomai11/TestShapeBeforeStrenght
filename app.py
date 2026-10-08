import streamlit as st

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide"
)

# ==========================================
# SESSION
# ==========================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# ==========================================
# LOGIN PAGE
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

✅ วิเคราะห์ Shape ของมือก่อนแต้ม

✅ ใช้การบิดแบบ Transfer

✅ เปิดเผยข้อมูลให้น้อยที่สุด

✅ หา Fit อย่างมีประสิทธิภาพ

✅ ฝึกผ่านโจทย์จริงและสถานการณ์จริง

---

### หลังเข้าสู่ระบบ คุณจะสามารถ

✅ ฝึก Opening Bid

✅ ฝึก Response และ Rebid

✅ ดูสถิติความแม่นยำ

✅ ดูประวัติการฝึกย้อนหลัง

✅ เปรียบเทียบผลของแต่ละ Session

✅ ทบทวนข้อผิดพลาดที่พบบ่อย

---

เป้าหมายของระบบนี้ไม่ใช่การท่องจำคำตอบ

แต่เพื่อช่วยให้ผู้เล่นเข้าใจ

• Shape

• Fit

• Distribution

• Judgement

• Philosophy ของระบบ Shape Before Strength
        """)

    with right:

        st.subheader("เข้าสู่ระบบ")

        player_name = st.text_input(
            "ชื่อผู้เล่น"
        )

        remember_me = st.checkbox(
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

    st.subheader("System Notes")

    st.info("""
Opening

• 11-13 Balanced = 1C

• 14-16 Balanced = 1NT

• 17-19 Balanced (No M5) = 1C

• 20-22 Balanced = 2NT
""")

# ==========================================
# OPENING PAGE
# ==========================================

elif st.session_state.page == "opening":

    st.title("Opening Practice")

    if st.button("⬅ กลับเมนู"):
        st.session_state.page = "menu"
        st.rerun()

    st.write(
        "Opening Quiz จะถูกเพิ่มในขั้นตอนถัดไป"
    )

    st.success(
        "ระบบพร้อมแล้ว ✅"
    )
