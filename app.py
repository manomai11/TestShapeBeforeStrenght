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
    page_title="SHAPE BEFORE STRENGTH",
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

# ฟังก์ชันแจกจ่ายคำคม/เพลงที่แตกต่างกันตามโหมด
def get_cheat_code_quote(mode):
    quotes = {
        "opening": [
            "🎵 *'ก้าวแรกสำคัญที่สุด เปิดให้ถูกทรง ไพ่ในมือจะนำทาง'*",
            "💡 **Opening Wisdom:** เสียงแรกที่เปล่งออกไป คือเข็มทิศนำทางของคู่หู",
            "🔥 'อย่ากลัวที่จะเปิด เมื่อทรงไพ่ในมือคุณกระซิบว่าพร้อม'"
        ],
        "response_1nt": [
            "🎵 *'1NT คือความนิ่งสงบ สยบความเคลื่อนไหวทั้งหมดบนโต๊ะ'*",
            "💡 **1NT Rule:** สมดุลคือหัวใจ ไร้ความโลภคือชัยชนะ",
            "🔥 'เมื่อ partner เปิด 1NT โลกทั้งใบก็อยู่ในกำมือ'"
        ],
        "response_1c": [
            "🎵 *'Club เล็กๆ แต่พลังยิ่งใหญ่ จุดประกายความหวัง'*",
            "💡 **1C Mindset:** ก้าวเล็กที่มั่น and safe คือทางสู่เกมนิรันดร์",
            "🔥 'คลับที่เรียบง่าย ซ่อนเร้นพลังมหาศาลไว้เสมอ'"
        ],
        "response_1d": [
            "🎵 *'Diamond เพชรเม็ดงามที่รอการเจียระไน'*",
            "💡 **1D Focus:** อดทนรอจังหวะ ค้นหา Fit ให้เจอ",
            "🔥 'เพชรแท้ดูที่ทรง ไม่ใช่แค่แสงสะท้อนของแต้ม'"
        ],
        "response_1h": [
            "🎵 *'Hearts หัวใจแห่งเกมบริดจ์ รักใครให้บอก Spades หรือ Hearts'*",
            "💡 **Major First:** หัวใจสำคัญคือการปกป้องแต้มสูงสุด",
            "🔥 'เมื่อใจตรงกัน (Fit) เกมไหนก็ไม่หวั่น'"
        ],
        "response_1s": [
            "🎵 *'Spades เจ้าแห่งโพดำ สูงสุดย่อมเป็นราชา'*",
            "💡 **King of Suits:** โพดำคือเกียรติยศและอำนาจการตัดสินใจ",
            "🔥 'เหนือกว่าด้วยทรง เหนือชั้นด้วยโพดำ'"
        ]
    }
    mode_quotes = quotes.get(mode, ["🎵 *'Bridge is an art of logic'*"])
    return random.choice(mode_quotes)


# ==================================================
# 1. LOGIN SCREEN
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
""")

    with right:
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



# ==================================================
# 2. MENU SCREEN (4 Sections)
# ==================================================

elif st.session_state.page == "menu":

    st.title(f"Welcome, {st.session_state.player_name} 👋")
    st.markdown("### ♠ SHAPE BEFORE STRENGTH — หน้าเลือกเมนูแบบฝึกหัด")
    st.write("เลือกหัวข้อแบบฝึกหัดที่คุณต้องการฝึกซ้อม (ชุดละ 20 ข้อ):")

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

    col_q1, col_q2, col_q3 = st.columns([1, 2.8, 1.2])

    # ----------------------------------
    # QUIZ SECTION 1: เมนูซ้าย
    # ----------------------------------
    with col_q1:
        if st.button("⬅ กลับหน้าเมนู", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
        
        st.markdown("---")
        st.metric(label="คะแนนสะสม", value=f"{st.session_state.score} / 20")
        st.metric(label="ข้อปัจจุบัน", value=f"{st.session_state.question} / 20")

    # ----------------------------------
    # QUIZ SECTION 2: พื้นที่ตรงกลาง
    # ----------------------------------
    with col_q2:
        st.markdown(f"### 📚 {current_topic_name} (ผู้เล่น: {st.session_state.player_name})")
        st.markdown("---")

        s_str = " ".join(hand["S"]) if hand["S"] else "-"
        h_str = " ".join(hand["H"]) if hand["H"] else "-"
        d_str = " ".join(hand["D"]) if hand["D"] else "-"
        c_str = " ".join(hand["C"]) if hand["C"] else "-"

        st.markdown(
            f"""
            <div style="font-size: 1.25rem; line-height: 1.8; font-weight: bold; background-color: #f8f9fa; padding: 12px 16px; border-radius: 8px; border: 1px solid #e9ecef;">
                <div>♠ <span style="color: #111;">{s_str}</span></div>
                <div>♥ <span style="color: #d32f2f;">{h_str}</span></div>
                <div>♦ <span style="color: #d32f2f;">{d_str}</span></div>
                <div>♣ <span style="color: #111;">{c_str}</span></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.caption(f"✨ **แต้มรวม (HCP):** {hcp} &nbsp;&nbsp;|&nbsp;&nbsp; 📊 **ทรงไพ่ (Shape):** {shape}")
        st.markdown("---")

        if not st.session_state.answered:
            st.markdown("#### 🎛️ Bidding Box")
            
            level_key = f"level_q_{st.session_state.question}"
            if level_key not in st.session_state:
                st.session_state[level_key] = None

            allowed_levels = ["1", "2", "3", "4", "5", "6", "7"]
            
            cols_box = st.columns(8)
            
            with cols_box[0]:
                if st.button("PASS", use_container_width=True, key=f"pass_{st.session_state.question}"):
                    process_answer("PASS", correct_answer[0])
            
            for idx, lvl in enumerate(allowed_levels):
                with cols_box[idx + 1]:
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
                            process_answer(final_bid, correct_answer[0])
        else:
            st.markdown(f"### {st.session_state.result}")
            st.write(f"**ตอบ:** `{st.session_state.user_answer}` | **ที่ถูก:** `{correct_answer[0]}`")
            
            with st.expander("💡 เหตุผลและหลักการประมูล", expanded=True):
                st.markdown(f"""
                - **แต้มรวม (HCP):** {hcp} แต้ม | **Shape:** {shape}
                - เหตุผล **{correct_answer[1]}**
                """)

            if st.session_state.question < 20:
                if st.button("ข้อถัดไป ➡", use_container_width=True, type="primary"):
                    st.session_state.question += 1
                    st.session_state.answered = False
                    st.session_state.user_answer = ""
                    st.session_state.current_hand_data = get_next_question_data(st.session_state.page)
                    st.rerun()
            else:
                if st.button("🏁 ดูผลสรุปคะแนน", use_container_width=True, type="primary"):
                    st.session_state.page = "summary"
                    st.rerun()

    # ----------------------------------
    # QUIZ SECTION 3: ฝั่งขวา (Cheat Code / สุ่มคำคมประจำหมวด)
    # ----------------------------------
    with col_q3:
        st.markdown("### 📌 Cheat Code")
        st.markdown("*(มุมมองและแรงบันดาลใจ)*")
        
        # เรียกใช้ฟังก์ชันสุ่มคำคมตามหมวดหมู่ปัจจุบัน
        current_quote = get_cheat_code_quote(st.session_state.page)
        st.info(current_quote)


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
