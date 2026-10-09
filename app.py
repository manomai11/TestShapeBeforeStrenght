import random
import streamlit as st

from engine import (
    opening_bid,
    response_1nt,
    response_1major,
    response_1d,
    response_1c,
)

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide"
)

# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================

if "page" not in st.session_state:
    st.session_state.page = "login"

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "score" not in st.session_state:
    st.session_state.score = 0

if "question" not in st.session_state:
    st.session_state.question = 1

if "answered" not in st.session_state:
    st.session_state.answered = False

if "result" not in st.session_state:
    st.session_state.result = ""

if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

if "seen_signatures" not in st.session_state:
    st.session_state.seen_signatures = set()

if "pass_count_in_set" not in st.session_state:
    st.session_state.pass_count_in_set = 0

if "current_hand_data" not in st.session_state:
    st.session_state.current_hand_data = None


# ==================================================
# CARD & ENGINE FUNCTIONS
# ==================================================

RANKS = "AKQJT98765432"

HCP_MAP = {
    "A": 4,
    "K": 3,
    "Q": 2,
    "J": 1
}

def generate_single_hand():
    deck = []
    for suit in ["S", "H", "D", "C"]:
        for rank in RANKS:
            deck.append((suit, rank))
    random.shuffle(deck)
    cards = deck[:13]
    hand = {"S": [], "H": [], "D": [], "C": []}
    for suit, rank in cards:
        hand[suit].append(rank)
    for suit in hand:
        hand[suit].sort(key=lambda x: RANKS.index(x))
    return hand

def calculate_hcp(hand):
    total = 0
    for cards in hand.values():
        for card in cards:
            total += HCP_MAP.get(card, 0)
    return total

def calculate_shape(hand):
    return (
        str(len(hand["S"])) +
        str(len(hand["H"])) +
        str(len(hand["D"])) +
        str(len(hand["C"]))
    )

def get_next_question_data(mode_type):
    while True:
        hand = generate_single_hand()
        hcp = calculate_hcp(hand)
        shape = calculate_shape(hand)
        
        signature = (hcp, shape, tuple(tuple(v) for v in hand.values()))
        if signature in st.session_state.seen_signatures:
            continue
            
        if mode_type == "opening":
            ans = opening_bid(hcp, shape)
        elif mode_type == "response_1nt":
            ans = response_1nt(hcp, shape)
        elif mode_type == "response_1c":
            ans = response_1c(hcp, shape)
        elif mode_type == "response_1d":
            ans = response_1d(hcp, shape)
        elif mode_type == "response_1h":
            ans = response_1major("1H", hcp, shape)
        else:
            ans = response_1major("1S", hcp, shape)
            
        if ans == "PASS":
            if st.session_state.pass_count_in_set >= 1:
                continue
            st.session_state.pass_count_in_set += 1
            
        st.session_state.seen_signatures.add(signature)
        
        return {
            "hand": hand,
            "hcp": hcp,
            "shape": shape,
            "correct_answer": ans
        }

def process_answer(chosen_bid, correct):
    st.session_state.user_answer = chosen_bid
    if chosen_bid == correct:
        st.session_state.result = "✅ Correct"
        st.session_state.score += 1
    else:
        st.session_state.result = "❌ Incorrect"
    st.session_state.answered = True
    st.rerun()

def start_new_practice(page_name):
    st.session_state.page = page_name
    st.session_state.question = 1
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.result = ""
    st.session_state.user_answer = ""
    st.session_state.seen_signatures = set()
    st.session_state.pass_count_in_set = 0
    st.session_state.current_hand_data = get_next_question_data(page_name)
    st.rerun()


# ==================================================
# 1. LOGIN SCREEN
# ==================================================

if st.session_state.page == "login":
    col1, col2, col3 = st.columns([1.5, 1.2, 0.8])

    with col1:
        st.markdown("## ♠ Bridge Master Engine")
        st.markdown("**ยกระดับการประมูลไพ่สากลด้วยระบบตรรกะมาตรฐาน**")
        st.markdown("""
        แอปพลิเคชันฝึกฝนการประมูลบริดจ์รูปแบบชุด 20 ข้อ:
        - **🎯 Fast Random:** สุ่มโจทย์สดทีละข้อ ลื่นไหล
        - **⚖️ Unique & Balanced:** มือไม่ซ้ำกัน คุม PASS ไม่เกิน 1 ข้อ
        - **💡 Detailed Explanation:** มีเฉลยพร้อมเหตุผลประกอบชัดเจน
        """)

    with col2:
        st.markdown("### เริ่มต้นใช้งาน")
        st.write("กรอกชื่อเพื่อเข้าสู่สนามฝึกซ้อม")
        
        with st.form("login_form"):
            name = st.text_input("ชื่อของคุณ:", placeholder="เช่น Player_01")
            submitted = st.form_submit_button("เข้าสู่หน้าเลือกแบบฝึกหัด", use_container_width=True)
            
            if submitted:
                if name.strip() != "":
                    st.session_state.player_name = name
                    st.session_state.page = "menu"
                    st.rerun()
                else:
                    st.warning("⚠️ กรุณากรอกชื่อก่อนครับ")

    with col3:
        st.write("")


# ==================================================
# 2. MENU SCREEN (4 Sections)
# ==================================================

elif st.session_state.page == "menu":

    st.title(f"Welcome, {st.session_state.player_name} 👋")
    st.write("หน้าเลือกเมนูแบบฝึกหัด (ชุดละ 20 ข้อ):")

    # แบ่งเป็น 4 ส่วนตามโครงร่าง
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.markdown("### ส่วนที่ 1")
        st.markdown("**ฝึกเปิด (Opening)**")
        if st.button("Start Opening", use_container_width=True):
            start_new_practice("opening")

    with col_m2:
        st.markdown("### ส่วนที่ 2")
        st.markdown("**ฝึก Response**")
        if st.button("Response 1C", use_container_width=True):
            start_new_practice("response_1c")
        if st.button("Response 1D", use_container_width=True):
            start_new_practice("response_1d")
        if st.button("Response 1H", use_container_width=True):
            start_new_practice("response_1h")
        if st.button("Response 1S", use_container_width=True):
            start_new_practice("response_1s")
        if st.button("Response 1NT", use_container_width=True):
            start_new_practice("response_1nt")

    with col_m3:
        st.markdown("### ส่วนที่ 3")
        st.markdown("*ว่าง*")
        st.info("รอเติมเนื้อหาในอนาคต")

    with col_m4:
        st.markdown("### ส่วนที่ 4")
        st.markdown("*ว่าง*")
        st.info("รอเติมเนื้อหาในอนาคต")


# ==================================================
# 3. QUIZ SCREEN (3 Sections)
# ==================================================

elif st.session_state.page in [
    "opening",
    "response_1nt",
    "response_1c",
    "response_1d",
    "response_1h",
    "response_1s",
]:

    if st.session_state.current_hand_data is None:
        st.session_state.current_hand_data = get_next_question_data(st.session_state.page)

    current_data = st.session_state.current_hand_data
    hand = current_data["hand"]
    hcp = current_data["hcp"]
    shape = current_data["shape"]
    correct_answer = current_data["correct_answer"]

    titles = {
        "opening": "Opening Practice",
        "response_1nt": "Response 1NT",
        "response_1c": "Response 1C",
        "response_1d": "Response 1D",
        "response_1h": "Response 1H",
        "response_1s": "Response 1S"
    }
    current_topic_name = titles.get(st.session_state.page, "Bridge Practice")

    # จัดเลย์เอาต์ 3 ส่วนตามตารางออกแบบ
    col_q1, col_q2, col_q3 = st.columns([1, 2.5, 1.2])

    # ----------------------------------
    # QUIZ SECTION 1: เมนูซ้าย (ปุ่มกลับ, คะแนน, ข้อปัจจุบัน)
    # ----------------------------------
    with col_q1:
        if st.button("⬅ กลับหน้าเมนู", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
        
        st.markdown("---")
        st.metric(label="คะแนนสะสม", value=f"{st.session_state.score} / 20")
        st.metric(label="ข้อปัจจุบัน", value=f"{st.session_state.question} / 20")

    # ----------------------------------
    # QUIZ SECTION 2: พื้นที่ตรงกลาง (หัวข้อ, ไพ่, Bidding Box / เฉลย)
    # ----------------------------------
    with col_q2:
        st.markdown(f"### 📚 หัวข้อ: {current_topic_name}")
        st.markdown(f"**ผู้เล่น:** {st.session_state.player_name}")
        st.markdown("---")

        # แสดงไพ่ 13 ใบชัดเจน พร้อม HCP และ Shape
        st.markdown(
f"""
### 🎴 มือไพ่ของคุณ
- ♠ **Spades:** `{"".join(hand["S"])}`
- ♥ **Hearts:** `{"".join(hand["H"])}`
- ♦ **Diamonds:** `{"".join(hand["D"])}`
- ♣ **Clubs:** `{"".join(hand["C"])}`
"""
        )
        st.info(f"✨ **แต้มรวม (HCP):** {hcp} | 📊 **ทรงไพ่ (Shape):** {shape}")
        st.markdown("---")

        # เงื่อนไข: ถ้ายังไม่ตอบ แสดง Bidding Box | ถ้าตอบแล้ว ซ่อน Bidding Box แล้วแสดงเฉลยแทน
        if not st.session_state.answered:
            st.markdown("#### 🎛️ Bidding Box (เลือกคำตอบของคุณ)")
            
            level_key = f"level_q_{st.session_state.question}"
            if level_key not in st.session_state:
                st.session_state[level_key] = None

            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                if st.button("PASS", use_container_width=True, key=f"pass_{st.session_state.question}"):
                    process_answer("PASS", correct_answer)
            with col_p2:
                if st.button("DBL", use_container_width=True, key=f"dbl_{st.session_state.question}"):
                    process_answer("DBL", correct_answer)
            with col_p3:
                if st.button("RDBL", use_container_width=True, key=f"rdbl_{st.session_state.question}"):
                    process_answer("RDBL", correct_answer)

            st.write("เลือกเลเวล (1 - 7):")
            cols_lvl = st.columns(7)
            levels = ["1", "2", "3", "4", "5", "6", "7"]
            
            for i, lvl in enumerate(levels):
                with cols_lvl[i]:
                    if st.button(lvl, use_container_width=True, key=f"lvl_{lvl}_{st.session_state.question}"):
                        st.session_state[level_key] = lvl
                        st.rerun()

            current_level = st.session_state.get(level_key, None)
            if current_level:
                st.markdown(f"**เลเวลที่เลือก: {current_level}** — เลือกชุดไพ่:")
                suit_cols = st.columns(5)
                suits = [
                    ("♣ C", "C"), 
                    ("♦ D", "D"), 
                    ("♥ H", "H"), 
                    ("♠ S", "S"), 
                    ("NT N", "N")
                ]
                
                for i, (label, s_code) in enumerate(suits):
                    with suit_cols[i]:
                        final_bid = f"{current_level}{s_code}"
                        if st.button(label, use_container_width=True, key=f"suit_{s_code}_{st.session_state.question}"):
                            process_answer(final_bid, correct_answer)
        else:
            # หลังกดตอบ: บิดดิ้งหายไป เอาเฉลยพร้อมคำอธิบายมาแทน และมีปุ่มข้อต่อไป
            st.markdown(f"## {st.session_state.result}")
            st.write(f"**คำตอบของคุณ:** {st.session_state.user_answer}")
            st.write(f"**คำตอบที่ถูกต้อง:** {correct_answer}")
            
            with st.expander("💡 เหตุผลและหลักการประมูล", expanded=True):
                st.markdown(f"""
                - **แต้มรวม (HCP):** {hcp} แต้ม
                - **ทรงไพ่ (Shape):** {shape}
                - **หลักการพิจารณา:** อิงตามกฎ Core Engine และลำดับความสำคัญ (Shape Before Strength / Find Fit Before Game) ทำให้คำตอบที่ถูกต้องคือ **{correct_answer}**
                """)

            st.markdown("---")

            if st.session_state.question < 20:
                if st.button("ข้อถัดไป ➡", use_container_width=True, type="primary"):
                    st.session_state.question += 1
                    st.session_state.answered = False
                    st.session_state.user_answer = ""
                    st.session_state.current_hand_data = get_next_question_data(st.session_state.page)
                    st.rerun()
            else:
                if st.button("🏁 ดูผลสรุปคะแนนประจำชุด", use_container_width=True, type="primary"):
                    st.session_state.page = "summary"
                    st.rerun()

    # ----------------------------------
    # QUIZ SECTION 3: ฝั่งขวา (Cheat Code / สรุปกฎประจำเรื่อง)
    # ----------------------------------
    with col_q3:
        st.markdown("### 📌 Cheat Code")
        st.markdown("*(สรุปกฎประจำเรื่อง)*")
        
        # แสดง Cheat Code ตามหัวข้อที่กำลังฝึกอยู่
        if st.session_state.page == "opening":
            st.success("""
            **Opening Rules:**
            - HCP 12+ เปิดประมูล
            - เปิด 5-card Major ก่อนถ้ามี
            - เปิด 4-card Minor (ชอร์ตสุด/ดีสุด)
            - 1NT เปิดที่ 15-17 สมดุล (Balanced)
            """)
        elif st.session_state.page == "response_1nt":
            st.success("""
            **Rule 1: Transfer First**
            - มีโอกาสใช้ Transfer ให้ใช้ก่อนเพื่อหา Major Fit, เก็บพื้นที่ และซ่อนมือเปิด
            """)
        elif st.session_state.page in ["response_1c", "response_1d", "response_1h", "response_1s"]:
            st.success("""
            **Response Rules:**
            - **Rule 2:** Shape Before Strength (หาทรงไพ่ก่อนถามแต้ม)
            - **Rule 5:** Find Fit Before Game (เกมตัดสินหลังรู้ Fit)
            """)
        else:
            st.info("รวบรวมเทคนิคและกฎสำคัญสำหรับใช้อ้างอิงระหว่างทำ Quiz")


# ==================================================
# 4. SUMMARY SCREEN
# ==================================================

elif st.session_state.page == "summary":
    st.title("🎉 สรุปผลการฝึกซ้อมครบ 20 ข้อ")
    
    st.markdown(f"### ผู้ฝึกซ้อม: {st.session_state.player_name}")
    st.metric(label="คะแนนรวมที่คุณทำได้", value=f"{st.session_state.score} / 20")
    
    percentage = (st.session_state.score / 20) * 100
    if percentage >= 80:
        st.success("🌟 ยอดเยี่ยมมาก! คุณมีความเข้าใจหลักการประมูลระดับเซียน")
    elif percentage >= 50:
        st.info("👍 ทำได้ดี! ลองทบทวนข้อที่พลาดแล้วฝึกใหม่อีกรอบเพื่อความแม่นยำ")
    else:
        st.warning("💪 สู้ๆ ครับ ลองกลับไปทบทวนกฎ 5 ข้อหลักแล้วมาลองใหม่อีกครั้ง!")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔄 กลับไปหน้าเมนูหลัก", use_container_width=True):
        st.session_state.page = "menu"
        st.rerun()
