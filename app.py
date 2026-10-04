import streamlit as st
import random

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Bridge Bidding Trainer", page_icon="🃏", layout="centered")

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

# --- ฟังก์ชันสุ่มไพ่และสร้างโจทย์จำลองตามหัวข้อ ---
def generate_question(topic):
    # สุ่ม HCP 0 ถึง 16
    hcp = random.randint(0, 16)
    
    # สุ่มแจกแจงทรงไพ่ (Shape) ให้รวมกันได้ 13 ใบ
    suits = [random.randint(0, 6), random.randint(0, 6), random.randint(0, 6), random.randint(0, 6)]
    while sum(suits) != 13 or max(suits) > 7:
        suits = [random.randint(0, 5), random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)]
        suits[random.randint(0, 3)] += (13 - sum(suits))
        if sum(suits) != 13:
            suits = [3, 3, 3, 4]
            
    s, h, d, c = suits
    shape_str = f"{s}{h}{d}{c}"
    
    # จำลองการเลือกคำตอบและปุ่มที่อนุญาตตามหัวข้อ
    all_bids = ["Pass", "1♣", "1♦", "1♥", "1♠", "1NT", "2♣", "2♦", "2♥", "2♠", "2NT", "3♣", "3♦", "3♥", "3♠", "3NT"]
    
    # กำหนดโจทย์คร่าวๆ ตามหัวข้อและเงื่อนไข
    if hcp <= 5:
        correct = "Pass"
    elif hcp >= 13:
        correct = "1NT" if max([s, h, d, c]) < 4 else ("1♥" if h >= s else "1♠")
    else:
        correct = "2♣" if c >= 5 else "1NT"
        
    # สุ่มปุ่มที่อนุญาตให้แสดง (รวมตัวที่ถูกและตัวหลอก)
    allowed = [correct, "Pass", "1NT"]
    if "1" in topic or "Response" in topic:
        allowed.extend(["1♣", "1♦", "1♥", "1♠"])
    else:
        allowed.extend(["2♣", "2♦", "2♥", "2♠"])
        
    allowed = list(set(allowed))
    random.shuffle(allowed)

    # จำลองหน้าไพ่
    cards_display = f"♠ {''.join(random.choices('AKQJT98765432', k=s))}  ♥ {''.join(random.choices('AKQJT98765432', k=h))}  ♦ {''.join(random.choices('AKQJT98765432', k=d))}  ♣ {''.join(random.choices('AKQJT98765432', k=c))}"

    return {
        "cards": cards_display,
        "hcp": hcp,
        "shape": shape_str,
        "allowed_bids": allowed,
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
    # แถบแสดงสถานะด้านบนกันลืม
    st.markdown(f"### 📌 Topic: `{st.session_state.topic}`")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"👤 **Player:** {st.session_state.username}")
    with col2:
        st.write(f"📊 **Question:** {st.session_state.q_index + 1} / 20 | ⭐ **Score:** {st.session_state.score}")
    
    st.divider()

    q = st.session_state.current_question

    # แสดงโจทย์ไพ่
    st.info(f"**Your Hand:**\n\n### `{q['cards']}`")
    st.write(f"🔍 **HCP:** {q['hcp']}  |  📏 **Shape:** {q['shape']}")

    # ส่วนเลือกคำตอบ
    if not st.session_state.answered:
        st.write("👉 **Select your bid:**")
        
        # สร้างปุ่มเฉพาะบิดที่อนุญาต (ซ่อนตัวที่ผิดกติกา)
        cols = st.columns(4)
        for i, bid in enumerate(q["allowed_bids"]):
            with cols[i % 4]:
                if st.button(bid, key=f"bid_{bid}", use_container_width=True):
                    st.session_state.selected_bid = bid
                    st.session_state.answered = True
                    if bid == q["correct_bid"]:
                        st.session_state.score += 1
                    st.rerun()
    else:
        # แสดงผลลัพธ์และคำอธิบายเมื่อตอบแล้ว
        selected = st.session_state.selected_bid
        correct = q["correct_bid"]

        if selected == correct:
            st.success(f"✅ **Correct!** Your answer: {selected}")
        else:
            st.error(f"❌ **Incorrect!** Your answer: {selected} | Correct answer: {correct}")

        st.markdown(f"💡 **Explanation:** {q['explanation']}")
        
        st.divider()

        # ปุ่มไปข้อถัดไป
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
