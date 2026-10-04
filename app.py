import streamlit as st
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Bridge Bidding Trainer", page_icon="🃏", layout="centered")

# --- CSS แต่งหน้าไพ่ให้สวยงามเหมือนไพ่จริง ---
st.markdown("""
<style>
.bridge-hand-container {
    background-color: #0f172a;
    color: #f8fafc;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    margin-bottom: 20px;
}
.suit-row {
    font-size: 20px;
    font-family: monospace;
    margin: 8px 0;
    font-weight: bold;
}
.red-suit {
    color: #ef4444;
}
.black-suit {
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# --- ฟังก์ชันจัดการสถานะ Session State ---
if "step" not in st.session_state:
    st.session_state.step = "login"
if "username" not in st.session_state:
    st.session_state.username = ""
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_bid" not in st.session_state:
    st.session_state.selected_bid = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None

# --- ฟังก์ชันสุ่มไพ่และสร้างโจทย์ ---
def generate_question(topic):
    hcp = random.randint(0, 16)
    
    # สุ่มแจกแจงทรงไพ่ (Shape) รวมให้ได้ 13 ใบ
    suits = [random.randint(0, 6), random.randint(0, 6), random.randint(0, 6), random.randint(0, 6)]
    while sum(suits) != 13 or max(suits) > 7:
        suits = [random.randint(0, 5), random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)]
        suits[random.randint(0, 3)] += (13 - sum(suits))
        if sum(suits) != 13:
            suits = [3, 3, 3, 4]
            
    s, h, d, c = suits
    shape_str = f"{s}{h}{d}{c}"
    
    # กำหนดคำตอบที่ถูกต้องตามเงื่อนไขจำลองเบื้องต้น
    if hcp <= 5:
        correct = "Pass"
    elif hcp >= 13:
        correct = "1NT" if max([s, h, d, c]) < 4 else ("1♥" if h >= s else "1♠")
    else:
        correct = "2♣" if c >= 5 else "1NT"

    # สุ่มหน้าไพ่จริง 13 ใบแยกตาม Suit
    ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    s_cards = " ".join(sorted(random.choices(ranks, k=s), key=lambda x: "AKQJT98765432".index(x)))
    h_cards = " ".join(sorted(random.choices(ranks, k=h), key=lambda x: "AKQJT98765432".index(x)))
    d_cards = " ".join(sorted(random.choices(ranks, k=d), key=lambda x: "AKQJT98765432".index(x)))
    c_cards = " ".join(sorted(random.choices(ranks, k=c), key=lambda x: "AKQJT98765432".index(x)))

    return {
        "s_cards": s_cards if s_cards else "-",
        "h_cards": h_cards if h_cards else "-",
        "d_cards": d_cards if d_cards else "-",
        "c_cards": c_cards if c_cards else "-",
        "hcp": hcp,
        "shape": shape_str,
        "correct_bid": correct,
        "explanation": f"Based on HCP ({hcp}) and Shape ({shape_str}), the correct system response is {correct}."
    }

# --- 1. หน้า Login ---
if st.session_state.step == "login":
    st.title("🃏 Bridge Bidding Trainer")
    st.write("Welcome! Please enter your name to start practicing.")
    
    with st.form("login_form"):
        name_input = st.text_input("Your Name / Username")
        submitted = st.form_submit_button("Log In")
        if submitted:
            if name_input.strip():
                st.session_state.username = name_input.strip()
                st.session_state.step = "menu"
                st.rerun()
            else:
                st.warning("Please enter a valid name.")

# --- 2. หน้าเลือกหมวดหมู่ฝึกซ้อม ---
elif st.session_state.step == "menu":
    st.sidebar.write(f"👤 **Player:** {st.session_state.username}")
    if st.sidebar.button("Log out"):
        st.session_state.step = "login"
        st.rerun()

    st.title("📋 Select Training Module")
    st.write("Choose the bidding practice category you want to test:")

    topics = [
        ("Opening Practice", "ฝึกเปิด (Opening)"),
        ("Response 1C Opening", "ฝึก response 1C opening"),
        ("Response 1D Opening", "ฝึก response 1D opening"),
        ("Response 1H Opening", "ฝึก response 1H opening"),
        ("Response 1S Opening", "ฝึก response 1S opening"),
        ("Response 1N Opening", "ฝึก response 1N opening"),
    ]

    for key, label in topics:
        if st.button(label, use_container_width=True):
            st.session_state.topic = key
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.current_question = generate_question(key)
            st.session_state.step = "quiz"
            st.rerun()

# --- 3. หน้า Quiz (20 ข้อ) ---
elif st.session_state.step == "quiz":
    st.markdown(f"### 📌 Topic: `{st.session_state.topic}`")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"👤 **Player:** {st.session_state.username}")
    with col2:
        st.write(f"📊 **Question:** {st.session_state.q_index + 1} / 20 | ⭐ **Score:** {st.session_state.score}")
    
    st.divider()

    q = st.session_state.current_question

    # แสดงไพ่สไตล์การ์ดจริงสวยงาม
    st.markdown(f"""
    <div class="bridge-hand-container">
        <div style="font-size: 14px; color: #94a3b8; margin-bottom: 10px;">YOUR HAND (HCP: {q['hcp']} | Shape: {q['shape']})</div>
        <div class="suit-row black-suit">♠ {q['s_cards']}</div>
        <div class="suit-row red-suit">♥ {q['h_cards']}</div>
        <div class="suit-row red-suit">♦ {q['d_cards']}</div>
        <div class="suit-row black-suit">♣ {q['c_cards']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ส่วนเลือกคำตอบ (แสดงปุ่มบิดทั้งหมดครบถ้วนถึง 7N)
    if not st.session_state.answered:
        st.write("👉 **Select your bid:**")
        
        # ปุ่มพิเศษ Pass
        if st.button("Pass", use_container_width=True):
            st.session_state.selected_bid = "Pass"
            st.session_state.answered = True
            if "Pass" == q["correct_bid"]:
                st.session_state.score += 1
            st.rerun()

        # สร้างตารางปุ่มบิด ระดับ 1 ถึง 7
        suits_symbol = ["♣", "♦", "♥", "♠", "NT"]
        for level in range(1, 8):
            cols = st.columns(5)
            for i, suit_char in enumerate(suits_symbol):
                bid_text = f"{level}{suit_char}"
                internal_bid = f"{level}{'C' if suit_char=='♣' else 'D' if suit_char=='♦' else 'H' if suit_char=='♥' else 'S' if suit_char=='♠' else 'NT'}"
                
                with cols[i]:
                    if st.button(bid_text, key=f"bid_{level}_{suit_char}", use_container_width=True):
                        st.session_state.selected_bid = internal_bid
                        st.session_state.answered = True
                        if internal_bid == q["correct_bid"]:
                            st.session_state.score += 1
                        st.rerun()
    else:
        # แสดงผลลัพธ์และเฉลย
        selected = st.session_state.selected_bid
        correct = q["correct_bid"]

        if selected == correct:
            st.success(f"✅ **Correct!** Your answer: {selected}")
        else:
            st.error(f"❌ **Incorrect!** Your answer: {selected} | Correct answer: {correct}")

        st.markdown(f"💡 **Explanation:** {q['explanation']}")
        
        st.divider()

        if st.button("Next Question ➔", use_container_width=True):
            if st.session_state.q_index + 1 < 20:
                st.session_state.q_index += 1
                st.session_state.answered = False
                st.session_state.selected_bid = None
                st.session_state.current_question = generate_question(st.session_state.topic)
                st.rerun()
            else:
                st.session_state.step = "result"
                st.rerun()

# --- 4. หน้าสรุปผลคะแนน ---
elif st.session_state.step == "result":
    st.title("🎉 Training Completed!")
    st.balloons()
    
    st.subheader(f"Great job, {st.session_state.username}!")
    st.write(f"Your final score in **{st.session_state.topic}** is:")
    
    st.metric(label="Total Score", value=f"{st.session_state.score} / 20")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.current_question = generate_question(st.session_state.topic)
            st.session_state.step = "quiz"
            st.rerun()
    with col_b:
        if st.button("🏠 Back to Menu", use_container_width=True):
            st.session_state.step = "menu"
            st.rerun()
