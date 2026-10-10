from datetime import datetime
import random
import sqlite3
import streamlit as st

from engine import (
    opening_bid,
    response_1nt,
    response_1major,
    response_1d,
    response_1c,
    opener_rebid_1c,
)

# ==================================================
# CONFIG & DATABASE SETUP
# ==================================================

st.set_page_config(
    page_title="SHAPE BEFORE STRENGTH",
    page_icon="♠",
    layout="wide"
)

def init_db():
    conn = sqlite3.connect("bridge_stats.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            mode TEXT,
            score INTEGER,
            total_questions INTEGER,
            week_number INTEGER,
            year INTEGER,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

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
        elif mode_type == "opener_1c_rebid":
        # 1. เช็คก่อนว่ามือนี้เปิด 1C จริงไหม ถ้าไม่ใช่ให้สุ่มใหม่
            opening_check = opening_bid(hcp, shape)
        if not opening_check or opening_check[0] != "1C":
            continue
            
        # 2. สุ่ม Response ของ Partner
        responses = ["1D", "1H", "1S", "1N", "2C", "2D", "2H", "2S", "2N", "3C"]
        weights   = [ 24,   24,   8,   12,   8,   8,   8,   4,   2,   2 ]
            
        resp = random.choices(responses, weights=weights, k=1)[0]
            
        c_cards = hand["C"]
        c_honors = sum(1 for card in c_cards if card in ["A", "K", "Q"])
        extra_info = {"c_honors": c_honors}
            
        ans = opener_rebid_1c(resp, hcp, shape, extra_info)
        if not ans:
            continue
                
        # 3. บันทึก Sequence ไว้แสดงผล
        st.session_state.current_auction_context = f"1C ➔ {resp}"
        else:
            ans = opening_bid(hcp, shape)
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

def save_session_to_db(player_name, mode, score):
    conn = sqlite3.connect("bridge_stats.db")
    cursor = conn.cursor()
    now = datetime.now()
    year, week_number, _ = now.isocalendar()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO training_sessions (player_name, mode, score, total_questions, week_number, year, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (player_name, mode, score, 20, week_number, year, timestamp))
    
    conn.commit()
    conn.close()

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
             col_l1, col_l2 = st.columns(2)
             with col_l1:
                 submitted = st.form_submit_button("เข้าสู่หน้าเลือกแบบฝึกหัด", use_container_width=True)
             with col_l2:
                 trainer_btn = st.form_submit_button("🎓 Trainer Dashboard", use_container_width=True)
            
             if submitted:
                 if name.strip() != "":
                     st.session_state.player_name = name
                     st.session_state.page = "menu"
                     st.rerun()
                 else:
                     st.warning("⚠️ กรุณากรอกชื่อก่อนครับ")
             elif trainer_btn:
                 st.session_state.page = "trainer_dashboard"
                 st.rerun()


# ==================================================
# 1.5 TRAINER DASHBOARD SCREEN
# ==================================================

elif st.session_state.page == "trainer_dashboard":
    st.title("🎓 Trainer & Progress Dashboard")
    st.write("ตรวจสอบสถิติ ความคืบหน้า และผลงานรายสัปดาห์ของผู้เรียนทั้งหมด")
    
    if st.button("⬅ กลับหน้าแรก"):
        st.session_state.page = "login"
        st.rerun()
        
    st.markdown("---")
    
    conn = sqlite3.connect("bridge_stats.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT player_name, mode, score, total_questions, week_number, year, timestamp 
        FROM training_sessions ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        st.info("ยังไม่มีข้อมูลการฝึกซ้อมในระบบ")
    else:
        import pandas as pd
        df = pd.DataFrame(rows, columns=["Player", "Mode", "Score", "Total", "Week", "Year", "Timestamp"])
        
        selected_player = st.selectbox("กรองตามรายชื่อผู้เล่น:", ["ทั้งหมด"] + list(df["Player"].unique()))
        if selected_player != "ทั้งหมด":
            df_filtered = df[df["Player"] == selected_player]
        else:
            df_filtered = df
            
        st.subheader("📊 ประวัติการฝึกซ้อมทั้งหมด")
        st.dataframe(df_filtered, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📅 สรุปสถิติเฉลี่ยรายสัปดาห์ (Weekly Progress)")
        
        weekly_summary = df.groupby(["Year", "Week", "Player", "Mode"]).agg(
            Times_Practiced=("Score", "count"),
            Avg_Score=("Score", "mean"),
            Max_Score=("Score", "max")
        ).reset_index()
        weekly_summary["Avg_Score"] = weekly_summary["Avg_Score"].round(2)
        
        st.dataframe(weekly_summary, use_container_width=True)


# ==================================================
# 2. MENU SCREEN (4 Sections)
# ==================================================

elif st.session_state.page == "menu":

    st.title(f"Welcome, {st.session_state.player_name} 👋")
    st.markdown("### ♠ SHAPE BEFORE STRENGTH — หน้าเลือกเมนูแบบฝึกหัด")
    st.write("เลือกหัวข้อแบบฝึกหัดที่คุณต้องการฝึกซ้อม (ชุดละ 20 ข้อ):")

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.markdown("**ฝึกเปิด (Opening)**")
        if st.button("Start Opening", use_container_width=True):
            start_new_practice("opening")

    with col_m2:
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
        st.markdown("**ฝึก Rebid (Opener)**")
        if st.button("Opener 1C Rebid", use_container_width=True):
            start_new_practice("opener_1c_rebid")

    with col_m4:
        st.markdown("### ส่วนที่ 4")
        st.markdown("*ว่าง*")
        st.info("รอเติมเนื้อหาในอนาคต")

    st.markdown("---")
    if st.button("🚪 ออกจากระบบ / เปลี่ยนชื่อ"):
        st.session_state.player_name = ""
        st.session_state.page = "login"
        st.rerun()


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
    "opener_1c_rebid",
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
        "response_1s": "Response 1S",
        "opener_1c_rebid": "Opener 1C Rebid Practice",
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
        # เพิ่มบรรทัดนี้เพื่อให้โชว์สถานการณ์การประมูลครับ
        if st.session_state.page == "opener_1c_rebid" and "current_auction_context" in st.session_state:
            st.info(f"🔄 **สถานการณ์การประมูล:** {st.session_state.current_auction_context}")
            
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
                    save_session_to_db(
                        st.session_state.player_name,
                        st.session_state.page,
                        st.session_state.score
                    )
                    st.session_state.page = "summary"
                    st.rerun()

    # ----------------------------------
    # QUIZ SECTION 3: ฝั่งขวา (Cheat Sheet / Cheat Code)
    # ----------------------------------
    with col_q3:
        st.markdown("### 📌 Cheat Sheet")
        st.markdown("*(สรุปกติกาเร่งด่วน)*")
        
        def get_cheat_sheet_content(mode):
            sheets = {
                "opening": """
**Opening Rules:**
- Pass = 0-10 HCP
- 1C = 11-20 HCP, ♣ 2+ (ถ้า Balanced ไม่จำกัดว่าชุดต้องยาวกว่า เช่น 5332, 4432)
- 1D = 11-20 HCP, Unbalanced, ♦ 4+
- 1H = 11-20 HCP, M5 (ไม่มี 5332 ยกเว้นมี 17+ HCP)
- 1S = 11-20 HCP, M5 (ไม่มี 5332 ยกเว้นมี 17+ HCP)
- 1NT = 14-16 (Balanced)
- 2C = 21+ or 8.5 PT
- 2D = weak 1M or 17-20 M55
- 2M = 11-13 M6 no second suit >4
                """,
                "response_1c": """
**Response 1C Rules:**
- 1D = Transfer H (4+)
- 1H = Transfer S (4+)
- 1S = 0-10, No M4, No Void
- 1NT = GF, No M5
- 2C = Transfer D
- 2D = GI (C 5+)
- 2H = GI Balanced (M<4m<5)
- 3C = NF (C 6)
                """,
                "response_1nt": """
**Response 1NT Rules:**
- 2C = inverted stayman จะทะยอยเพิ่มรายละเอียดในเวป
- 2D = Transfer to H or mss
- 2H = Transfer to S
- 2S/2N = transfer C/D
- 3C = Ask M คนถามไม่มี M5 และแค่เกมไม่สนใจสแลม
- 3D = GF 9+ M55 (GF 10+ M54 ใช้ 2C)
- 3H = GF 3154 or 3145
- 3S = GF 1354 or 1345
- 3N = To play
                """,
                "response_1d": """
**Response 1D Rules:**
- Level 1 คล้าย เปิด 1C
- 2C = NF C6+ or 3325 (แทน 1N  ที่คุณเคยเล่น)
- 2D = NF D3-4
- 2H = 11-12 Balance 
- 2S = GI C5+ C>D
- 3C = GI D4+ D>C
- 3D = NF D5 or D4 with any short
                """,
                "response_1h": """
**Response 1H Rules:**
- 1S = S<5 แทน 1NFC
- 1N = S5+ less than GF
- 2C = GF RELAY
- 2D = GI H3 or GF H3 with any short
- 2H = constructive raised H3 or 3433
- 2S = <10 S6
- 2N = 10-12 H4+ with any short
- 3C = 8-12 H4+ no short
- 3D = 0-5 H4 or GF H4 with any void
- 3H = 4-7 H4 4-5 must have A
- 3S = GF H4+ singleton S
- 3N = GF H4+ singleton C
- 4C = GF H4+ singleton D
- 4H = <10 H5 or H4+short
                """,
                "response_1s": """
**Response 1S Rules:**
- 1N = Force 1 round
- 2C = GF RELAY
- 2D = Transfer H
- 2H = GI S3 or GF S3 with any short
- 2S = constructive raised S3 or 4333
- 2N up คล้าย open 1H
                """,
                "opener_1c_rebid": """
**Opener 1C Rebid Rules:**
- Extran hand 16+
- 2N 17-19 Balanced M4
- 2M-1 Turbo Fit 16+ M3
- 2D or 2oM ที่ไม่ใช้ Turbo Fit ==>Power Fit 16+ M4
- 1N 17-19 Bal no M4 or 16+ M<3
- Medium Hand 14-15
- 2M 14-15 M4 
- 3C 14-15 good C6+
- minimum 11-15
- 1M Accept transfer 11-13 Balanced or M4
- 1S 11-15 S4 unbalanced
- 2C 11-15 C5+ 
                """  # <--- ปิดด้วยเครื่องหมายคำพูด 3 ตัวและใส่คอมมาให้ถูกต้อง
            }
            return sheets.get(mode, "หลักการ Shape Before Strength: หา Fit & Shape ก่อนแต้ม")

        with st.expander("📖 เปิดดู Cheat Sheet", expanded=True):
            st.markdown(get_cheat_sheet_content(st.session_state.page))

        st.markdown("---")
        st.markdown("### 💡 คำคมประจำหมวด")
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
        st.success("🌟 ยอดเยี่ยมมาก! บันทึกสถิติลงระบบเรียบร้อยแล้ว")
    elif percentage >= 50:
        st.info("👍 ทำได้ดี! ระบบได้บันทึกสถิติการฝึกรอบนี้ไว้แล้ว")
    else:
        st.warning("💪 สู้ๆ ครับ บันทึกผลไว้แล้ว ลองกลับมาฝึกซ้อมซ้ำเพื่อพัฒนาการที่ดีขึ้น!")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("🔄 กลับไปหน้าเมนูหลัก", use_container_width=True):
            st.session_state.page = "menu"
            st.rerun()
    with col_s2:
        if st.button("🎓 ไปหน้า Trainer Dashboard", use_container_width=True):
            st.session_state.page = "trainer_dashboard"
            st.rerun()
