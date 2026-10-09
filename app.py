import streamlit as st
import random

from engine import (
    opening_bid,
    response_1nt,
    response_1major,
    response_1d,
    response_1c,
)
import streamlit as st

# ตั้งค่าหน้าจอเล็กน้อย (ถ้ายังไม่มี)
# st.set_page_config(page_title="Bridge Master", page_icon="♠️", layout="centered")

# ใช้ Container ตกแต่งกรอบให้ดูสะอาดตา
with st.container():
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>♠️ Bridge Master Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; color: #4B5563;'>ยกระดับการประมูลไพ่สากลด้วยระบบตรรกะอัจฉริยะ ฝึกฝนตามกฎจริง แม่นยำทุกสถานการณ์</p>", unsafe_allow_html=True)
    
    st.divider()

    # ส่วนรับข้อมูลผู้ใช้ (Login / Enter Name)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("ยินดีต้อนรับผู้เล่น")
        username = st.text_input("กรอกชื่อของคุณเพื่อเริ่มต้น:", placeholder="เช่น Player_01", key="input_username")
        
        # เลือกระดับความยากหรือโหมดเริ่มต้น (ถ้ามี)
        mode = st.selectbox("เลือกโหมดการฝึกซ้อม:", ["Opening Bids", "Response 1NT", "Advanced Relay"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ปุ่มกดเข้าสู่ระบบ / เริ่มต้นใช้งาน
        if st.button("🚀 เข้าสู่สนามประมูล", use_container_width=True):
            if username.strip() != "":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = "opening"  # หรือหน้าแรกของเกม
                st.rerun()
            else:
                st.warning("⚠️ กรุณากรอกชื่อก่อนเข้าสู่ระบบครับ")

    # ฟีเจอร์ย่อยด้านล่างดึงดูดสายตา
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("🎯 **Core Engine**<br><span style='font-size: 0.9rem; color: #6B7280;'>ประมวลผลแม่นยำตามกฎ 5 ข้อหลัก</span>", unsafe_allow_html=True)
    with c2:
        st.markdown("📊 **Instant Feedback**<br><span style='font-size: 0.9ynth;'>ตรวจคำตอบทันที รู้ผลไว เข้าใจง่าย</span>", unsafe_allow_html=True)
    with c3:
        st.markdown("⚡ **Shape First**<br><span style='font-size: 0.9rem; color: #6B7280;'>ฝึกมองทรงไพ่ก่อนนับแต้มจริง</span>", unsafe_allow_html=True)
# ==================================================
# CARD ENGINE
# ==================================================

RANKS = "AKQJT98765432"

HCP_MAP = {
    "A": 4,
    "K": 3,
    "Q": 2,
    "J": 1
}


def generate_hand():

    deck = []

    for suit in ["S", "H", "D", "C"]:

        for rank in RANKS:

            deck.append((suit, rank))

    random.shuffle(deck)

    cards = deck[:13]

    hand = {
        "S": [],
        "H": [],
        "D": [],
        "C": []
    }

    for suit, rank in cards:
        hand[suit].append(rank)

    for suit in hand:
        hand[suit].sort(
            key=lambda x: RANKS.index(x)
        )

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


# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide"
)

# ==================================================
# SESSION
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

if "hand" not in st.session_state:
    st.session_state.hand = generate_hand()

# ==================================================
# LOGIN
# ==================================================

if st.session_state.page == "login":

    st.title("Shape Before Strength")

    with st.form("login"):

        name = st.text_input(
            "ชื่อผู้เล่น"
        )

        submitted = st.form_submit_button(
            "เริ่มฝึก"
        )

        if submitted and name.strip():

            st.session_state.player_name = name
            st.session_state.page = "menu"

            st.rerun()

# ==================================================
# MENU
# ==================================================

elif st.session_state.page == "menu":

    st.title(
        f"Welcome {st.session_state.player_name}"
    )

    if st.button(
        "Opening Practice",
        use_container_width=True
    ):

        st.session_state.page = "opening"

        st.session_state.answered = False
        st.session_state.result = ""
        st.session_state.user_answer = ""
        st.session_state.level_selected = None

        st.rerun()

    if st.button(
         "Response 1NT",
        use_container_width=True
    ):

        st.session_state.page = "response_1nt"

        st.session_state.answered = False
        st.session_state.result = ""
        st.session_state.user_answer = ""
        st.session_state.level_selected = None

        st.rerun()

    if st.button(
         "Response 1C",
        use_container_width=True
    ):

        st.session_state.page = "response_1c"

        st.session_state.answered = False
        st.session_state.result = ""
        st.session_state.user_answer = ""
        st.session_state.level_selected = None

        st.rerun()

    if st.button(
         "Response 1D",
        use_container_width=True
    ):

        st.session_state.page = "response_1d"

        st.session_state.answered = False
        st.session_state.result = ""
        st.session_state.user_answer = ""
        st.session_state.level_selected = None

        st.rerun()

    if st.button(
         "Response 1H",
        use_container_width=True
    ):

        st.session_state.page = "response_1h"

        st.session_state.answered = False
        st.session_state.result = ""
        st.session_state.user_answer = ""
        st.session_state.level_selected = None

        st.rerun()

    if st.button(
         "Response 1S",
        use_container_width=True
    ):

        st.session_state.page = "response_1s"

        st.session_state.answered = False
        st.session_state.result = ""
        st.session_state.user_answer = ""
        st.session_state.level_selected = None

        st.rerun()

# ==================================================
# COMMON SCREEN
# ==================================================

elif st.session_state.page in [
    "opening",
    "response_1nt",
    "response_1c",
    "response_1d",
    "response_1h",
    "r1s",
]:

    if st.button("⬅ Menu"):

        st.session_state.page = "menu"

        st.rerun()

    if st.session_state.hand is None:

        st.session_state.hand = generate_hand()

    hand = st.session_state.hand

    hcp = calculate_hcp(hand)

    shape = calculate_shape(hand)

    # ----------------------------------
    # ENGINE
    # ----------------------------------

    if st.session_state.page == "opening":

        title = "Opening"

        correct_answer = opening_bid(
            hcp,
            shape
        )

    elif st.session_state.page == "response_1nt":

        title = "Response 1NT"

        correct_answer = response_1nt(
            hcp,
            shape
        )

    elif st.session_state.page == "response_1c":

        title = "Response 1C"

        correct_answer = response_1c(
            hcp,
            shape
        )

    elif st.session_state.page == "response_1d":

        title = "Response 1D"

        correct_answer = response_1d(
            hcp,
            shape
        )

    elif st.session_state.page == "response_1h":

        title = "Response 1H"

        correct_answer = response_1major(
            "1H",
            hcp,
            shape
        )

    else:

        title = "Response 1S"

        correct_answer = response_1major(
            "1S",
            hcp,
            shape
        )

    st.title(title)

    st.write(
        f"Question : {st.session_state.question}"
    )

    st.write(
        f"Score : {st.session_state.score}"
    )

    st.markdown(
f"""
### Hand

♠ {"".join(hand["S"])}

♥ {"".join(hand["H"])}

♦ {"".join(hand["D"])}

♣ {"".join(hand["C"])}
"""
    )

    st.write(f"HCP : {hcp}")
    st.write(f"Shape : {shape}")

    bids = [
        "PASS",

        "1C","1D","1H","1S","1N",

        "2C","2D","2H","2S","2N",

        "3C","3D","3H","3S","3N",

        "4C","4D","4H","4S","4N",

        "5C","5D","5H","5S","5N",

        "6C","6D","6H","6S","6N",

        "7C","7D","7H","7S","7N"
    ]

    if not st.session_state.answered:

        choice = st.radio("Choose Bid", bids, key="r1nt_choice", index=None)

        if choice:

            st.session_state.user_answer = choice

            if choice == correct_answer:

                st.session_state.result = "✅ Correct"

                st.session_state.score += 1

            else:

                st.session_state.result = "❌ Incorrect"

            st.session_state.answered = True

            st.rerun()

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

        if st.button("Next Question"):

            st.session_state.question += 1

            st.session_state.answered = False
            
            st.session_state.user_answer = ""

            st.session_state.hand = generate_hand()

            st.rerun()
