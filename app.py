import random
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Bridge Master Training", page_icon="🃏", layout="centered")

HCP_MAP = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}
RANK_ORDER = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

def evaluate_hand(hand):
    counts = {'S': 0, 'H': 0, 'D': 0, 'C': 0}
    hcp = 0
    suit_cards = {'S': [], 'H': [], 'D': [], 'C': []}
    for card in hand:
        rank = card[0]
        suit = card[1]
        counts[suit] += 1
        suit_cards[suit].append(rank)
        if rank in HCP_MAP:
            hcp += HCP_MAP[rank]
    for suit in suit_cards:
        suit_cards[suit].sort(key=lambda r: RANK_ORDER[r], reverse=True)
    shape = [counts['S'], counts['H'], counts['D'], counts['C']]
    return hcp, shape, counts, suit_cards

def is_balanced(shape):
    s = sorted(shape, reverse=True)
    return s in [[4, 3, 3, 3], [4, 4, 3, 2], [5, 3, 3, 2]]

def match_shape_new(shape, pattern_str):
    parts = pattern_str.strip().split()
    if parts[0] == "any":
        target_counts = sorted([int(x) for x in parts[1]])
        actual_counts = sorted(shape)
        return target_counts == actual_counts
    else:
        target_tuple = tuple(int(x) for x in pattern_str.strip())
        return tuple(shape) == target_tuple

def has_second_suit_greater_than_4(shape, primary_suit_idx):
    for idx, length in enumerate(shape):
        if idx != primary_suit_idx and length > 4:
            return True
    return False

def has_second_suit_5plus(shape, primary_suit_idx):
    for idx, length in enumerate(shape):
        if idx != primary_suit_idx and length >= 5:
            return True
    return False

def logic_opening(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    def is_solid(suit_name, suit_idx):
        cards = suit_cards[suit_name]
        if len(cards) >= 7:
            honors = [card for card in cards if card in ['A', 'K', 'Q', 'J', 'T']]
            if len(honors) >= min(len(cards)-1, 5):
                if not has_second_suit_5plus(shape, suit_idx):
                    return True
        return False

    if 5 <= hcp <= 10:
        if c >= 8 and not has_second_suit_5plus(shape, 3): return "4C", "5-10 HCP, C=8"
        if d >= 8 and not has_second_suit_5plus(shape, 2): return "4D", "5-10 HCP, D=8"
        if h >= 8 and not has_second_suit_5plus(shape, 1): return "4H", "5-10 HCP, H=8"
        if s >= 8 and not has_second_suit_5plus(shape, 0): return "4S", "5-10 HCP, S=8"

    if is_solid('H', 1): return "3N", "Solid H7+"
    if is_solid('S', 0): return "3N", "Solid S7+"

    if 5 <= hcp <= 10:
        if c == 7 and not has_second_suit_greater_than_4(shape, 3): return "3C", "C=7"
        if d == 7 and not has_second_suit_greater_than_4(shape, 2): return "3D", "D=7"
        if h == 7 and not has_second_suit_5plus(shape, 1): return "3H", "H=7"
        if s == 7 and not has_second_suit_5plus(shape, 0): return "3S", "S=7"

    if 11 <= hcp <= 13:
        if h == 6 and not has_second_suit_5plus(shape, 1): return "2H", "H=6"
        if s == 6 and not has_second_suit_5plus(shape, 0): return "2S", "S=6"

    if 11 <= hcp <= 20:
        if (s, h, d, c) == (4, 4, 1, 4): return "1C", "Shape 4414"
        elif (4 in shape) and shape.count(4) == 3 and shape.count(1) == 1:
            return "1D", "Shape 4-4-4-1"

    if 11 <= hcp <= 20 and (match_shape_new(shape, "4144") or match_shape_new(shape, "1444")):
        return "1D", "4144 or 1444"
    if 11 <= hcp <= 15 and d == 4 and c == 5:
        return "1D", "D=4, C=5"

    if hcp < 11: return "Pass", "<11 HCP"
    if hcp >= 21:
        if 20 <= hcp <= 22 and is_balanced(shape): return "2N", "20-22 Balanced"
        return "2C", "21+ HCP"
    if 20 <= hcp <= 22 and is_balanced(shape): return "2N", "20-22 Balanced"
    
    if 11 <= hcp <= 20:
        if s == 5 and h == 5: return "1S", "5-5 Major, S > H"
        if s == 5 and d == 5: return "1S", "5-5 S and D, S > D"
        if s == 5 and c == 5: return "1S", "5-5 S and C, S > C"
        if h == 5 and d == 5: return "1H", "5-5 H and D, H > D"
        if h == 5 and c == 5: return "1H", "5-5 H and C, H > C"
        if d == 5 and c == 5: return "1D", "5-5 Minor, D > C"
        
        suits_len = [('S', s), ('H', h), ('D', d), ('C', c)]
        long_suits = [item for item in suits_len if item[1] >= 5]
        if len(long_suits) >= 2:
            order = {'S': 4, 'H': 3, 'D': 2, 'C': 1}
            long_suits.sort(key=lambda x: (x[1], order[x[0]]), reverse=True)
            best_suit = long_suits[0][0]
            mapping = {'S': '1S', 'H': '1H', 'D': '1D', 'C': '1C'}
            return mapping[best_suit], f"Two suits, longer suit {best_suit}"

    if 17 <= hcp <= 20 and s >= 5 and h >= 5: return "2D", "M55+"
    if 11 <= hcp <= 13 and is_balanced(shape): return "1C", "Balanced"
    if 14 <= hcp <= 16 and is_balanced(shape): return "1N", "Balanced"
    if 17 <= hcp <= 19 and is_balanced(shape) and s < 5 and h < 5: return "1C", "Balanced"
    if 11 <= hcp <= 20 and c >= 5 and c >= s and c >= h: return "1C", "C5+"
    if 11 <= hcp <= 20 and d >= 5: return "1D", "D5+"
    if 11 <= hcp <= 16 and s >= 5: return "1S", "S5+"
    if 17 <= hcp <= 20 and s >= 5: return "1S", "S5+"
    if 11 <= hcp <= 16 and h >= 5: return "1H", "H5+"
    if 17 <= hcp <= 20 and h >= 5: return "1H", "H5+"
    return "Pass", "Pass"

def logic_resp_1n(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    has_M5 = (s >= 5 or h >= 5)
    has_m55 = (d >= 5 and c >= 5)
    has_M55 = (s >= 5 and h >= 5)
    if hcp >= 11 and (s == 3 and h == 1 and ((d == 5 and c == 4) or (d == 4 and c == 5))): return "3H", "3154/3145"
    if hcp >= 11 and (s == 1 and h == 3 and ((d == 5 and c == 4) or (d == 4 and c == 5))): return "3S", "1354/1345"
    if hcp <= 8 and s < 5 and h < 5 and d < 6 and c < 6 and not has_m55: return "Pass", "Pass"
    if 7 <= hcp <= 8 and (has_M55 or (has_M5 and (d >= 5 or c >= 5))): return "2C", "M55 or M5m5"
    if hcp == 9 and d < 6 and c < 6 and not has_m55: return "2C", "9 HCP"
    if hcp == 10 and s < 5 and h < 5 and d < 6 and c < 6 and not has_m55: return "2C", "10 HCP"
    if hcp >= 16 and s < 5 and h < 5 and d < 6 and c < 6 and not has_m55: return "2C", "16+ HCP"
    if 11 <= hcp <= 15 and ((2 < s < 5) or (2 < h < 5)): return "3C", "3-card Major support"
    return "Pass", "Default Pass"

def logic_resp_1c(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    has_M4 = (s >= 4 or h >= 4)
    has_m6 = (d >= 6 or c >= 6)
    has_m55 = (d >= 5 and c >= 5)
    def check_bal_dbl():
        if is_balanced(shape):
            for st, cards in suit_cards.items():
                if len(cards) == 2 and not has_honor(cards): return False
            return True
        return False
    if hcp <= 5 and c >= 4 and c > s and c > h and c > d: return "Pass", "Pass"
    if h >= 4 and s >= 4: return "1D", "H4S4"
    if h >= 4 and h > s: return "1D", "H4+ H>S"
    if s >= 4 and s >= h and not (s == 4 and h == 4): return "1H", "S4+, S>=H"
    if 5 <= hcp <= 10 and has_m55: return "2S", "m55"
    if 5 <= hcp <= 10 and c >= 6: return "3C", "C6+"
    if 0 <= hcp <= 10 and d >= 6 and not has_M4: return "2C", "D6 no M4"
    if 11 <= hcp <= 12 and d >= 5 and not has_M4: return "2C", "D5 no M4"
    if 11 <= hcp <= 12 and c >= 5 and s < 4 and h < 4: return "2D", "C5+ M<4"
    if 11 <= hcp <= 12 and is_balanced(shape) and s < 4 and h < 4 and d < 5 and c < 5: return "2H", "Balanced"
    if 5 <= hcp <= 10 and s < 4 and h < 4 and not has_m6 and not has_m55: return "1S", "M<4"
    if hcp >= 13 and s < 4 and h < 4: return "1N", "13+ M<4"
    if hcp >= 13 and (s == 4 or h == 4) and check_bal_dbl(): return "1N", "13+ 4M Balanced"
    return "Pass", "Pass"

def logic_resp_1d(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    def check_bal_dbl():
        if is_balanced(shape):
            for st, cards in suit_cards.items():
                if len(cards) == 2 and not has_honor(cards): return False
            return True
        return False
    if hcp <= 5: return "Pass", "Pass"
    if hcp >= 5 and h >= 4 and h > s and not (h == 4 and s == 4): return "1H", "H4+ H>S"
    if hcp >= 5 and s >= 4 and s >= h and not (h == 4 and s == 4): return "1S", "S4+ S>=H"
    if hcp >= 13 and s < 4 and h < 4: return "1N", "13+ M<4"
    if hcp >= 13 and (h == 4 or s == 4) and check_bal_dbl(): return "1N", "13+ 4M Balanced"
    if 5 <= hcp <= 10 and c == 5 and s < 4 and h < 4 and d < 3: return "2C", "C=5"
    if 5 <= hcp <= 10 and c >= 6 and s < 4 and h < 4 and d < 4: return "2C", "C6+"
    if 5 <= hcp <= 10 and 3 <= d <= 4 and s < 4 and h < 4: return "2D", "D 3-4"
    if 11 <= hcp <= 12 and is_balanced(shape) and s < 4 and h < 4: return "2H", "Balanced"
    if 11 <= hcp <= 12 and c >= 5 and not is_balanced(shape) and s < 4 and h < 4: return "2S", "C5+ Unbalanced"
    if 11 <= hcp <= 12 and d >= 4 and not is_balanced(shape) and s < 4 and h < 4: return "3C", "D4+ Unbalanced"
    if 5 <= hcp <= 10 and d == 5 and s < 4 and h < 4: return "3D", "D=5"
    return "Pass", "Pass"

def logic_resp_1h(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    def is_3433(shp): return sorted(shp, reverse=True) == [4, 3, 3, 3] and shp[1] == 4
    def has_shg(shp, mx=0): return any(l <= mx for l in shp)
    if hcp >= 13 and h >= 4 and s < 2: return "3S", "H4+ S<2"
    if hcp >= 13 and h >= 4 and c < 2: return "3N", "H4+ C<2"
    if hcp >= 13 and h >= 4 and d < 2: return "4C", "H4+ D<2"
    if hcp >= 13 and h >= 4 and has_shg(shape, 0): return "3D", "Void"
    if hcp >= 13 and h == 3 and has_shg(shape, 1): return "2D", "H=3 Shortage"
    if hcp >= 13: return "2C", "13+ Any"
    has_ace = any(r == 'A' for r in suit_cards['H'])
    if 4 <= hcp <= 5 and h == 4 and has_ace and not is_3433(shape): return "3H", "H=4 Ace"
    if hcp <= 5 and h == 4 and not is_3433(shape): return "3D", "H=4"
    if 11 <= hcp <= 12 and s >= 5 and h < 4: return "1N", "S5+"
    if 10 <= hcp <= 12 and h == 3: return "2D", "H=3"
    if hcp <= 5 and h < 4: return "Pass", "Pass"
    if 5 <= hcp <= 12 and s < 5 and h < 3: return "1S", "S<5 H<3"
    if 5 <= hcp <= 10 and s == 5 and h < 3: return "1N", "S=5"
    if 5 <= hcp <= 10 and s >= 6 and h < 2: return "2S", "S>=6"
    if 5 <= hcp <= 10 and s >= 7 and h < 3: return "1N", "S>=7"
    if 5 <= hcp <= 9 and (h == 3 or is_3433(shape)): return "2H", "H=3 or 3433"
    if 10 <= hcp <= 12 and h >= 4 and has_shg(shape, 1): return "2N", "H4+ Shortage"
    if 8 <= hcp <= 12 and h >= 4 and not has_shg(shape, 1): return "3C", "H4+"
    if 6 <= hcp <= 7 and h == 4 and not is_3433(shape): return "3H", "H=4"
    if 5 <= hcp <= 10 and h == 4 and has_shg(shape, 1): return "4H", "H=4 Shortage"
    if 5 <= hcp <= 10 and h >= 5: return "4H", "H5+"
    return "Pass", "Pass"

def logic_resp_1s(hcp, shape, counts, suit_cards):
    s, h, d, c = shape
    def is_4333(shp): return sorted(shp, reverse=True) == [4, 3, 3, 3] and shp[0] == 4
    def has_shg(shp, mx=0): return any(l <= mx for l in shp)
    if hcp >= 13 and s >= 4 and s == 1: return "3H", "S4+ S=1"
    if hcp >= 13 and s >= 4 and c == 1: return "3N", "S4+ C=1"
    if hcp >= 13 and s >= 4 and d == 1: return "4C", "S4+ D=1"
    if hcp >= 13 and s >= 4 and has_shg(shape, 0): return "3D", "Void"
    if hcp >= 13 and s == 3 and has_shg(shape, 1): return "2H", "S=3 Shortage"
    if hcp >= 13: return "2C", "13+ Any"
    has_ace = any(r == 'A' for r in suit_cards['S'])
    if 4 <= hcp <= 5 and s == 4 and has_ace and not is_4333(shape): return "3S", "S=4 Ace"
    if hcp <= 5 and s == 4 and not is_4333(shape): return "3D", "S=4"
    if 11 <= hcp <= 12 and s < 3 and h < 5: return "1N", "S<3 H<5"
    if 10 <= hcp <= 12 and s == 3: return "2H", "S=3"
    if hcp <= 5 and s < 4: return "Pass", "Pass"
    if 5 <= hcp <= 10 and s < 3 and h < 6: return "1N", "S<3 H<6"
    if 6 <= hcp <= 10 and h >= 6 and s < 3: return "2D", "H6+"
    if 11 <= hcp <= 12 and h >= 5 and s < 4: return "2D", "H5+"
    if 5 <= hcp <= 9 and (s == 3 or is_4333(shape)): return "2S", "S=3"
    if 10 <= hcp <= 12 and s >= 4 and has_shg(shape, 1): return "2N", "S4+ Shortage"
    if 8 <= hcp <= 12 and s >= 4 and not has_shg(shape, 1): return "3C", "S4+"
    if 6 <= hcp <= 7 and s == 4 and not is_4333(shape): return "3S", "S=4"
    if 5 <= hcp <= 9 and s == 4 and has_shg(shape, 1): return "4S", "S=4 Shortage"
    if hcp <= 9 and s >= 5: return "4S", "S5+"
    return "Pass", "Pass"

# จัดการ Session State ของ Streamlit
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'username' not in st.session_state: st.session_state.username = ""
if 'mode' not in st.session_state: st.session_state.mode = None
if 'mode_name' not in st.session_state: st.session_state.mode_name = ""
if 'question_no' not in st.session_state: st.session_state.question_no = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'current_hand_data' not in st.session_state: st.session_state.current_hand_data = None
if 'feedback' not in st.session_state: st.session_state.feedback = None

def generate_hand_data(mode):
    suits = ['S', 'H', 'D', 'C']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    deck = [r + s for s in suits for r in ranks]
    while True:
        hand = random.sample(deck, 13)
        hcp, shape, counts, suit_cards = evaluate_hand(hand)
        if mode == 'opening':
            bid, reason = logic_opening(hcp, shape, counts, suit_cards)
            if bid == 'Pass': continue
        elif mode == 'resp_1c':
            bid, reason = logic_resp_1c(hcp, shape, counts, suit_cards)
        elif mode == 'resp_1d':
            bid, reason = logic_resp_1d(hcp, shape, counts, suit_cards)
        elif mode == 'resp_1h':
            bid, reason = logic_resp_1h(hcp, shape, counts, suit_cards)
        elif mode == 'resp_1s':
            bid, reason = logic_resp_1s(hcp, shape, counts, suit_cards)
        elif mode == 'resp_1n':
            bid, reason = logic_resp_1n(hcp, shape, counts, suit_cards)
        break
    return {'suit_cards': suit_cards, 'hcp': hcp, 'shape': shape, 'bid': bid, 'reason': reason}

# 1. หน้า Login
if not st.session_state.logged_in:
    st.title("🃏 ระบบฝึกทักษะบริดจ์")
    username = st.text_input("กรอกชื่อผู้ใช้ของคุณ:")
    if st.button("เข้าสู่ระบบ", type="primary"):
        if username.strip():
            st.session_state.username = username.strip()
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("⚠️ กรุณากรอกชื่อก่อนครับ")

# 2. หน้า Menu เลือกหมวดหมู่
elif st.session_state.mode is None:
    st.title(f"ยินดีต้อนรับคุณ {st.session_state.username}")
    st.subheader("📂 กรุณาเลือกหัวข้อแบบฝึกหัด (เซ็ตละ 20 ข้อ)")
    
    modes = [
        ('ฝึกเปิด (Opening)', 'opening'),
        ('ฝึกตอบ 1C opening', 'resp_1c'),
        ('ฝึกตอบ 1D opening', 'resp_1d'),
        ('ฝึกตอบ 1H opening', 'resp_1h'),
        ('ฝึกตอบ 1S opening', 'resp_1s'),
        ('ฝึกตอบ 1N opening', 'resp_1n')
    ]
    
    for name, key in modes:
        if st.button(name, use_container_width=True):
            st.session_state.mode = key
            st.session_state.mode_name = name
            st.session_state.question_no = 1
            st.session_state.score = 0
            st.session_state.current_hand_data = generate_hand_data(key)
            st.session_state.feedback = None
            st.rerun()
            
    if st.button("ออกจากระบบ"):
        st.session_state.logged_in = False
        st.rerun()

# 3. หน้า Quiz ทำแบบฝึกหัด
else:
    col_top1, col_top2 = st.columns([3, 1])
    with col_top1:
        st.markdown(f"**ผู้เล่น:** {st.session_state.username} | **หมวด:** {st.session_state.mode_name}")
    with col_top2:
        if st.button("⬅️ กลับหน้าเมนู"):
            st.session_state.mode = None
            st.rerun()
            
    st.markdown("---")
    
    if st.session_state.question_no > 20:
        st.success(f"🎉 จบเซ็ตแบบฝึกหัด 20 ข้อแล้วครับ! คะแนนรวม: {st.session_state.score} / 20 คะแนน")
        if st.button("กลับไปหน้าเลือกหมวดหมู่"):
            st.session_state.mode = None
            st.rerun()
    else:
        hand_data = st.session_state.current_hand_data
        suit_cards = hand_data['suit_cards']
        
        col_left, col_right = st.columns([1.2, 1])
        
        with col_left:
            st.markdown(f"### ข้อที่ {st.session_state.question_no} จาก 20")
            st.markdown(f"♠ **S:** {'  '.join(suit_cards['S'])}")
            st.markdown(f"♥ **H:** {'  '.join(suit_cards['H'])}")
            st.markdown(f"♦ **D:** {'  '.join(suit_cards['D'])}")
            st.markdown(f"♣ **C:** {'  '.join(suit_cards['C'])}")
            st.markdown(f"📊 **HCP:** {hand_data['hcp']} &nbsp;&nbsp;|&nbsp;&nbsp; **Shape:** {hand_data['shape'][0]}{hand_data['shape'][1]}{hand_data['shape'][2]}{hand_data['shape'][3]}")
            
            st.markdown("#### เลือกคำตอบ Bidding:")
            levels = ['1', '2', '3', '4', '5', '6', '7']
            suits_list = ['C', 'D', 'H', 'S', 'N']
            
            # สร้างปุ่มกดเลือกคำตอบ
            for lvl in levels:
                cols = st.columns(5)
                for i, s in enumerate(suits_list):
                    bid_str = lvl + s
                    with cols[i]:
                        if st.button(bid_str, key=f"btn_{lvl}_{s}", use_container_width=True):
                            # ตรวจคำตอบ
                            correct = (bid_str == hand_data['bid'])
                            if correct:
                                st.session_state.score += 1
                                st.session_state.feedback = ("correct", bid_str, hand_data['reason'])
                            else:
                                st.session_state.feedback = ("wrong", bid_str, hand_data['bid'], hand_data['reason'])
                            st.rerun()
            
            if st.button("Pass", type="secondary", use_container_width=True):
                correct = ("Pass" == hand_data['bid'])
                if correct:
                    st.session_state.score += 1
                    st.session_state.feedback = ("correct", "Pass", hand_data['reason'])
                else:
                    st.session_state.feedback = ("wrong", "Pass", hand_data['bid'], hand_data['reason'])
                st.rerun()

        with col_right:
            st.markdown(f"### คะแนน: {st.session_state.score} / {st.session_state.question_no - 1}")
            st.markdown("---")
            
            if st.session_state.feedback:
                fb = st.session_state.feedback
                if fb[0] == "correct":
                    st.success(f"✅ ถูกต้อง! คุณตอบ {fb[1]}\n\n💡 **เหตุผล:** {fb[2]}")
                else:
                    st.error(f"❌ ผิด! คุณตอบ {fb[1]} แต่ที่ถูกคือ **{fb[2]}**\n\n💡 **เหตุผล:** {fb[3]}")
                
                if st.button("ข้อต่อไป (Next) ➡️", type="primary", use_container_width=True):
                    st.session_state.question_no += 1
                    st.session_state.feedback = None
                    if st.session_state.question_no <= 20:
                        st.session_state.current_hand_data = generate_hand_data(st.session_state.mode)
                    st.rerun()
