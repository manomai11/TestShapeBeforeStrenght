import streamlit as st
import engine

st.set_page_config(page_title="Shape Before Strength", layout="wide")

# ปรับสไตล์ CSS ให้ปุ่มใน Bidding Box ชิดติดกันกระชับ และกล่องไพ่สวยงาม
st.markdown("""
<style>
.bbo-card-box {
    background-color: #113822;
    padding: 12px;
    border-radius: 6px;
    border: 2px solid #2d6a4f;
    color: white;
    font-size: 20px;
    font-family: monospace;
}
.suit-s { color: #f8f9fa; }
.suit-h { color: #ff4d4d; }
.suit-d { color: #ff9933; }
.suit-c { color: #33cc33; }
</style>
""", unsafe_allow_html=True)

defaults = {
    "page": "login",
    "player_name": "",
    "practice_mode": "",
    "questions_list": [],
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

# ================= LOGIN PAGE =================
if st.session_state.page == "login":
    st.title("♠ Shape Before Strength")
    st.subheader("Bridge Bidding Practice App")
    with st.form("login_form"):
        name_input = st.text_input("Enter your name to start (Press Enter):")
        if st.form_submit_button("Start Practice") or name_input:
            if name_input.strip() != "":
                st.session_state.player_name = name_input
                st.session_state.page = "menu"
                st.rerun()

# ================= MENU PAGE =================
elif st.session_state.page == "menu":
    st.title(f"Welcome, {st.session_state.player_name}!")
    st.subheader("Select Practice Mode")
    
    modes = [
        ("Opening Practice", "opening"),
        ("Response to 1C", "resp_1c"),
        ("Response to 1D", "resp_1d"),
        ("Response to 1H", "resp_1h"),
        ("Response to 1S", "resp_1s"),
        ("Response to 1N", "resp_1n"),
    ]

    c1, c2 = st.columns(2)
    for idx, (label, mode_key) in enumerate(modes):
        col = c1 if idx % 2 == 0 else c2
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.practice_mode = mode_key
                st.session_state.page = "practice"
                st.session_state.questions_list = engine.generate_practice_questions(mode_key, 20)
                st.session_state.question = 1
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.user_answer = ""
                st.session_state.level_selected = None
                st.rerun()

# ================= PRACTICE SCREEN (3 ZONES LAYOUT) =================
elif st.session_state.page == "practice":

    mode_titles = {
        "opening": "Opening Practice: What is your opening bid?",
        "resp_1c": "Response to 1C: Partner opened 1C, what is your bid?",
        "resp_1d": "Response to 1D: Partner opened 1D, what is your bid?",
        "resp_1h": "Response to 1H: Partner opened 1H, what is your bid?",
        "resp_1s": "Response to 1S: Partner opened 1S, what is your bid?",
        "resp_1n": "Response to 1N: Partner opened 1N, what is your bid?",
    }

    # หัวข้อ A อยู่ด้านบนสุด
    st.markdown(f"### 🏆 {mode_titles.get(st.session_state.practice_mode)}")
    st.markdown("---")

    q_data = st.session_state.questions_list[st.session_state.question - 1]
    cards = q_data["cards"]
    hcp = q_data["hcp"]
    shape = q_data["shape"]
    correct_answer = q_data["correct_answer"]
    rule_desc = q_data["rule_description"]

    # แบ่งหน้าจอออกเป็น 3 โซน (Zone A, B, C)
    zone_a, zone_b, zone_c = st.columns([1, 2, 1])

    # -----------------------------------------
    # ZONE A: เมนูควบคุม, คะแนน, และข้อมูล Shape/HCP
    # -----------------------------------------
    with zone_a:
        if st.button("◀ Back to Menu", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
        
        st.markdown("")
        st.markdown(f"**Question:** {st.session_state.question} / 20")
        st.markdown(f"**Score:** {st.session_state.score}")
        st.markdown(f"👤 **Player:** {st.session_state.player_name}")
        st.markdown("---")
        st.markdown(f"**Shape:** `{shape}`")
        st.markdown(f"**HCP:** `{hcp}`")

    # -----------------------------------------
    # ZONE B: โต๊ะไพ่, Mission, และ Bidding Box แบบปุ่มชิดติดกัน
    # -----------------------------------------
    with zone_b:
        if not st.session_state.answered:
            st.info(f"💡 **Mission:** {mode_titles.get(st.session_state.practice_mode)}")
        else:
            if "✅" in st.session_state.result:
                st.success(f"**{st.session_state.result}** | Your: {st.session_state.user_answer} | Correct: **{correct_answer}**\n\n📖 *{rule_desc}*")
            else:
                st.error(f"**{st.session_state.result}** | Your: {st.session_state.user_answer} | Correct: **{correct_answer}**\n\n📖 *{rule_desc}*")

        # แสดงสำรับไพ่
        st.markdown("##### Your Hand (South)")
        s_text = " ".join([c[0] for c in cards["♠"]]) or "-"
        h_text = " ".join([c[0] for c in cards["♥"]]) or "-"
        d_text = " ".join([c[0] for c in cards["♦"]]) or "-"
        c_text = " ".join([c[0] for c in cards["♣"]]) or "-"

        st.markdown(f"""
        <div class="bbo-card-box">
        <span class="suit-s">♠</span> {s_text}<br>
        <span class="suit-h">♥</span> {h_text}<br>
        <span class="suit-d">♦</span> {d_text}<br>
        <span class="suit-c">♣</span> {c_text}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Bidding Box (ปรับปุ่มให้ชิดติดกัน ไม่เว้นช่องว่างยาว)
        if not st.session_state.answered:
            st.markdown("#### Bidding Box")
            if st.button("PASS", key="btn_pass", use_container_width=True):
                st.session_state.user_answer = "PASS"
                if st.session_state.user_answer == correct_answer:
                    st.session_state.result = "✅ Correct"
                    st.session_state.score += 1
                else:
                    st.session_state.result = "❌ Incorrect"
                st.session_state.answered = True
                st.rerun()

            st.write("Select Level:")
            # ใช้คอลัมน์แคบติดกัน 7 ช่องสำหรับเลข 1-7
            lvl_cols = st.columns(7)
            for i in range(1, 8):
                with lvl_cols[i - 1]:
                    if st.button(str(i), key=f"lvl_{i}", use_container_width=True):
                        st.session_state.level_selected = i

            if st.session_state.level_selected:
                level = st.session_state.level_selected
                st.markdown(f"**Level:** {level}")
                # คอลัมน์ 5 ช่องชิดติดกันสำหรับดอกและ NT
                suit_cols = st.columns(5)
                suit_map = {"C": "♣", "D": "♦", "H": "♥", "S": "♠", "N": "NT"}
                for idx, (key, symbol) in enumerate(suit_map.items()):
                    with suit_cols[idx]:
                        if st.button(symbol, key=f"suit_{level}_{key}", use_container_width=True):
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
            if st.session_state.question < 20:
                if st.button("▶ Next Question", type="primary", use_container_width=True):
                    st.session_state.answered = False
                    st.session_state.user_answer = ""
                    st.session_state.result = ""
                    st.session_state.level_selected = None
                    st.session_state.question += 1
                    st.rerun()
            else:
                st.success(f"🎉 Practice Completed! Final Score: {st.session_state.score} / 20")
                if st.button("Back to Menu", use_container_width=True):
                    st.session_state.page = "menu"
                    st.rerun()

    # -----------------------------------------
    # ZONE C: พื้นที่ว่างสำรอง (สำหรับใส่วิเคราะห์เพิ่มเติม, สถิติ, หรือบันทึกย่อในอนาคต)
    # -----------------------------------------
    with zone_c:
        st.markdown("##### 📌 Notes & Stats")
        st.info("โซนนี้เตรียมไว้สำหรับใส่ข้อมูลสถิติ หรือคำใบ้กฎเพิ่มเติมในอนาคตครับ")
        st.markdown(f"**Mode:** `{st.session_state.practice_mode}`")
        st.markdown(f"**Balanced:** `{q_data['balanced']}`")
