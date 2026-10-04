import streamlit as st
import random

# ตั้งค่าหน้าเว็บให้ชิดขอบและกว้างขึ้น
st.set_page_config(page_title="Bridge Bidding Trainer", page_icon="🃏", layout="centered")

# --- CSS แต่งหน้าจอและขยายขนาดไพ่ให้ใหญ่ชัดเจนสไตล์ BBO ---
st.markdown("""
<style>
.bbo-table {
    background-color: #0f5132;
    padding: 12px;
    border-radius: 12px;
    border: 3px solid #198754;
    color: white;
    margin-bottom: 15px;
}
.bbo-header-box {
    background-color: #212529;
    color: #ffc107;
    padding: 6px 10px;
    border-radius: 6px;
    text-align: center;
    font-weight: bold;
    font-size: 13px;
    border: 1px solid #495057;
}
.bbo-score-box {
    background-color: #000000;
    color: #ffffff;
    padding: 4px;
    border-radius: 6px;
    text-align: center;
    font-family: monospace;
    font-size: 12px;
    border: 1px solid #6c757d;
}
.bbo-bidding-panel {
    background-color: #e9ecef;
    padding: 8px;
    border-radius: 8px;
    border: 2px solid #ced4da;
    margin-bottom: 8px;
}
.bridge-hand-box {
    background-color: #ffffff;
    border: 3px solid #000000;
    border-radius: 10px;
    padding: 15px;
    color: #000000;
    font-family: monospace;
    font-size: 26px;
    font-weight: 900;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    margin-top: 10px;
}
.player-tag {
    background-color: #ffc107;
    color: #000;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: bold;
    display: inline-block;
    margin-top: 6px;
}
.suit-red { color: #dc3545; }
.suit-black { color: #111111; }
.suit-symbol { font-size: 28px; margin-right: 6px; }
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
if "used_hands" not in st.session_state:
    st.session_state.used_hands = set()

# --- ฟังก์ชันคำนวณ HCP และตรวจสอบความถูกต้องตามหลักบริดจ์ ---
def calculate_hcp_and_cards(cards_list):
    hcp = 0
    rank_values = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
    for card in cards_list:
        hcp += rank_values.get(card, 0)
    return hcp

def determine_opening_bid(hcp, s, h, d, c):
    # กตุกาเบื้องต้นมาตรฐานการเปิด (Opening Bidding Rules)
    if hcp < 12:
        return "Pass"
    
    # คำนวณความยาวแต่ละ Suit
    suits_len = {'S': s, 'H': h, 'D': d, 'C': c}
    max_suit = max(suits_len, key=suits_len.get)
    max_len = suits_len[max_suit]
    
    # 1NT Opening (15-17 HCP, Balanced hand 4333, 4432, 5332)
    if 15 <= hcp <= 17 and max_len <= 5 and sorted(list(suits_len.values()), reverse=True)[0] <= 5 and sorted(list(suits_len.values()), reverse=True)[1] >= 3:
        return "1NT"
        
    # เปิด 5+ Major หรือ Minor ที่ยาวที่สุด
    if max_len >= 5:
        if max_suit == 'S': return "1♠"
        if max_suit == 'H': return "1♥"
        if max_suit == 'D': return "1♦"
        if max_suit == 'C': return "1♣"
    
    # ถ้าไม่มีสีใดยาวถึง 5 เปิดสีที่ยาวรองลงมา (Minor ดีกว่าถ้าแต้มไม่พอ Major)
    if h >= 4 and s >= 4:
        return "1♥" if h >= s else "1♠"
    if h >= 4: return "1♥"
    if s >= 4: return "1♠"
    
    if d >= c: return "1♦"
    return "1♣"

# --- ฟังก์ชันสร้างโจทย์แบบไม่ซ้ำกัน ---
def generate_unique_question(topic):
    ranks_pool = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    
    while True:
        # สุ่มแจกไพ่ 13 ใบให้ครบ 4 ชุด
        all_cards = random.choices(ranks_pool, k=13) + random.choices(ranks_pool, k=13) + random.choices(ranks_pool, k=13) + random.choices(ranks_pool, k=13)
        # จัดสรรแบ่งเป็น 4 กอง (Spade, Heart, Diamond, Club) โดยรวมกันได้ 13 ใบ
        s_count = random.randint(1, 6)
        h_count = random.randint(1, 6)
        d_count = random.randint(1, 6)
        c_count = 13 - (s_count + h_count + d_count)
        
        if c_count < 1 or c_count > 7:
            continue
            
        s_cards = sorted(random.choices(ranks_pool, k=s_count), key=lambda x: "AKQJT98765432".index(x))
        h_cards = sorted(random.choices(ranks_pool, k=h_count), key=lambda x: "AKQJT98765432".index(x))
        d_cards = sorted(random.choices(ranks_pool, k=d_count), key=lambda x: "AKQJT98765432".index(x))
        c_cards = sorted(random.choices(ranks_pool, k=c_count), key=lambda x: "AKQJT98765432".index(x))
        
        hand_signature = f"{s_count}{h_count}{d_count}{c_count}:{''.join(s_cards)}{''.join(h_cards)}{''.join(d_cards)}{''.join(c_cards)}"
        
        if hand_signature not in st.session_state.used_hands:
            st.session_state.used_hands.add(hand_signature)
            
            flat_cards = s_cards + h_cards + d_cards + c_cards
            hcp = calculate_hcp_and_cards(flat_cards)
            shape_str = f"{s_count}{h_count}{d_count}{c_count}"
            
            # ตรรกะคำตอบตาม Topic
            if "Opening" in topic:
                correct = determine_opening_bid(hcp, s_count, h_count, d_count, c_count)
            else:
                # ตัวอย่างสำหรับ Response หัวข้ออื่นๆ
                correct = "1NT" if hcp < 10 else "2NT"
                
            return {
                "s_cards": " ".join(s_cards) if s_cards else "-",
                "h_cards": " ".join(h_cards) if h_cards else "-",
                "d_cards": " ".join(d_cards) if d_cards else "-",
                "c_cards": " ".join(c_cards) if c_cards else "-",
                "hcp": hcp,
                "shape": shape_str,
                "correct_bid": correct,
                "explanation": f"HCP calculated accurately is {hcp} (A=4, K=3, Q=2, J=1) with shape {shape_str}. Correct bid is {correct}."
            }

# --- 1. หน้า Login ---
if st.session_state.step == "login":
    st.title("🃏 Bridge Bidding Trainer")
    st.write("Welcome! Please enter your name to start practicing.")
    
    with st.form("login_form"):
        name_input = st.text_input("Your Name / Username")
        submitted = st.form_submit_button("Log In", use_container_width=True)
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
    if st.sidebar.button("Log out", use_container_width=True):
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
            st.session_state.used_hands = set()
            st.session_state.current_question = generate_unique_question(key)
            st.session_state.step = "quiz"
            st.rerun()

# --- 3. หน้า Quiz จำลองหน้าจอ BBO แท้ๆ (ไพ่ใหญ่ชัดเจน & ไม่ซ้ำกัน) ---
elif st.session_state.step == "quiz":
    q = st.session_state.current_question

    col_a, col_b, col_c, col_d = st.columns([1, 1.2, 1, 2.5])
    
    with col_a:
        if st.button("≡ Menu", use_container_width=True):
            st.session_state.step = "menu"
            st.rerun()
            
    with col_b:
        st.markdown(f"""
        <div class="bbo-score-box">
            Score<br><b>{st.session_state.score} pts</b>
        </div>
        """, unsafe_allow_html=True)
        
    with col_c:
        st.markdown(f"""
        <div class="bbo-score-box">
            Question<br><b>{st.session_state.q_index + 1} / 20</b>
        </div>
        """, unsafe_allow_html=True)
        
    with col_d:
        st.markdown(f"""
        <div class="bbo-header-box">
            {st.session_state.topic}
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown('<div class="bbo-table">', unsafe_allow_html=True)

    if not st.session_state.answered:
        st.markdown('<div class="bbo-bidding-panel">', unsafe_allow_html=True)
        st.markdown("<span style='color:black; font-weight:bold; font-size:12px;'>Bidding Box:</span>", unsafe_allow_html=True)
        
        if st.button("Pass", use_container_width=True, type="primary"):
            st.session_state.selected_bid = "Pass"
            st.session_state.answered = True
            if "Pass" == q["correct_bid"]:
                st.session_state.score += 1
            st.rerun()

        st.markdown("<span style='color:black; font-size:11px;'>Select Level:</span>", unsafe_allow_html=True)
        lvl_cols = st.columns(7)
        for lvl in range(1, 8):
            with lvl_cols[lvl-1]:
                if st.button(str(lvl), key=f"bbo_lvl_{lvl}", use_container_width=True):
                    st.session_state.temp_level = lvl

        active_level = st.session_state.get("temp_level", 1)
        st.markdown(f"<span style='color:black; font-size:11px;'>Level: <b>{active_level}</b> | Choose suit:</span>", unsafe_allow_html=True)
        
        suit_cols = st.columns(5)
        suits_data = [("♣", "C"), ("♦", "D"), ("♥", "H"), ("♠", "S"), ("NT", "NT")]
        for i, (symbol, code) in enumerate(suits_data):
            with suit_cols[i]:
                bid_code = f"{active_level}{code}"
                if st.button(f"{active_level}{symbol}", key=f"bbo_suit_{code}", use_container_width=True):
                    st.session_state.selected_bid = bid_code
                    st.session_state.answered = True
                    if bid_code == q["correct_bid"]:
                        st.session_state.score += 1
                    st.rerun()
                    
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        selected = st.session_state.selected_bid
        correct = q["correct_bid"]
        if selected == correct:
            st.success(f"✅ Correct! Your bid: {selected}")
        else:
            st.error(f"❌ Incorrect! Your bid: {selected} | Correct: {correct}")
        st.markdown(f"<span style='color:white;'>💡 Explanation: {q['explanation']}</span>", unsafe_allow_html=True)
        
        if st.button("Next Question ➔", use_container_width=True, type="primary"):
            if st.session_state.q_index + 1 < 20:
                st.session_state.q_index += 1
                st.session_state.answered = False
                st.session_state.selected_bid = None
                st.session_state.current_question = generate_unique_question(st.session_state.topic)
                st.rerun()
            else:
                st.session_state.step = "result"
                st.rerun()

    st.markdown(f"""
    <div class="bridge-hand-box">
        <div style="font-size: 13px; color: #475569; margin-bottom: 6px; font-weight: bold;">HCP: {q['hcp']} &nbsp;|&nbsp; Shape: {q['shape']}</div>
        <div class="suit-black"><span class="suit-symbol">♠</span>{q['s_cards']}</div>
        <div class="suit-red"><span class="suit-symbol">♥</span>{q['h_cards']}</div>
        <div class="suit-red"><span class="suit-symbol">♦</span>{q['d_cards']}</div>
        <div class="suit-black"><span class="suit-symbol">♣</span>{q['c_cards']}</div>
    </div>
    <div class="player-tag">S: {st.session_state.username}</div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. หน้าสรุปผลคะแนน ---
elif st.session_state.step == "result":
    st.title("🎉 Training Completed!")
    st.balloons()
    
    st.subheader(f"Great job, {st.session_state.username}!")
    st.metric(label="Final Score", value=f"{st.session_state.score} / 20")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.q_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.used_hands = set()
            st.session_state.current_question = generate_unique_question(st.session_state.topic)
            st.session_state.step = "quiz"
            st.rerun()
    with col_b:
        if st.button("🏠 Back to Menu", use_container_width=True, type="primary"):
            st.session_state.step = "menu"
            st.rerun()
