import random

BALANCED_SHAPES = {
    "4333","3433","3343","3334",
    "4432","4423","4342","4243",
    "4324","4234","3442","2443",
    "3424","2434","3244","2344",
    "5332","5323","5233",
    "3532","3523","2533",
    "3352","3253","2353",
    "3325","3235","2335"
}

def calculate_hcp(hand):
    hcp = 0
    values = {"A": 4, "K": 3, "Q": 2, "J": 1}
    for suit in hand:
        for card in hand[suit]:
            rank = card[0]
            if rank in values:
                hcp += values[rank]
    return hcp

def generate_unique_hand():
    ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    suits = ['s', 'h', 'd', 'c']
    deck = [r+s for s in suits for r in ranks]
    
    while True:
        random.shuffle(deck)
        s_len = random.randint(1, 6)
        h_len = random.randint(1, 6)
        d_len = random.randint(1, 6)
        c_len = 13 - (s_len + h_len + d_len)
        
        if 0 <= c_len <= 7:
            lengths = {"♠": s_len, "♥": h_len, "♦": d_len, "♣": c_len}
            hand = {"♠": [], "♥": [], "♦": [], "♣": []}
            deck_copy = deck.copy()
            
            for suit, slen in lengths.items():
                if slen > 0:
                    cards = [deck_copy.pop(0) for _ in range(slen)]
                    hand[suit] = sorted(cards, key=lambda x: ranks.index(x[0]))
            
            shape_str = f"{len(hand['♠'])}{len(hand['♥'])}{len(hand['♦'])}{len(hand['♣'])}"
            hcp = calculate_hcp(hand)
            return hcp, shape_str, hand

# ==========================================
# 1. RESPONSE TO 1C
# ==========================================
def response_1c(hcp, shape, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    if hcp >= 13 and balanced and (s == 4 or h == 4):
        return "1N", "Response 1C: 13+ HCP Balanced with 4-card Major"
    if h >= 4 and ((h == 4 and s == 4) or h > s):
        return "1D", "Response 1C: Showing Hearts / Transfer"
    if s >= 4 and not (s == 4 and h == 4) and s >= h:
        return "1H", "Response 1C: Showing Spades"
    if 6 <= hcp <= 10 and d >= 6:
        return "2C", "Response 1C: 6+ Diamonds"
    return "PASS", "Response 1C: Standard Pass"

# ==========================================
# 2. RESPONSE TO 1D
# ==========================================
def response_1d(hcp, shape, balanced=False, bad_suit=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    if hcp >= 13 and s < 3 and h < 3:
        return "1N", "Response 1D: 13+ HCP with no 3-card Major"
    if 6 <= hcp <= 10 and d >= 5:
        return "3D", "Response 1D: 6-10 HCP with 5+ Diamond support"
    if hcp >= 6 and s >= 4 and s >= h:
        return "1S", "Response 1D: Showing Spades (4+ cards)"
    if hcp >= 6 and h >= 4 and h > s:
        return "1H", "Response 1D: Showing Hearts (4+ cards)"
    return "PASS", "Response 1D: Standard Pass"

# ==========================================
# 3. RESPONSE TO 1H (เพิ่มโครงสร้างฟังก์ชันจริง)
# ==========================================
def response_1h(hcp, shape, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    # ตัวอย่างตรรกะ Response 1H (ปรับแก้ตามกฎของคุณได้เลยครับ)
    if hcp >= 13 and h >= 3:
        return "3H", "Response 1H: Limit raise or better with 3+ support"
    if hcp >= 6 and s >= 4 and s > h:
        return "1S", "Response 1H: 4+ Spades (New suit forcing/semi-forcing)"
    if 6 <= hcp <= 10 and h >= 3:
        return "2H", "Response 1H: Single raise (3+ support, 6-10 HCP)"
    if hcp >= 6 and h >= 3:
        return "2N", "Response 1H: Jacoby 2NT (13+ HCP with 4+ support)" # ปรับตามระบบของคุณ
    return "PASS", "Response 1H: Minimum hand, Pass"

# ==========================================
# 4. RESPONSE TO 1S (เพิ่มโครงสร้างฟังก์ชันจริง)
# ==========================================
def response_1s(hcp, shape, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    if hcp >= 6 and s >= 3:
        return "2S", "Response 1S: Single raise with 3+ support"
    if hcp >= 13 and s >= 3:
        return "3S", "Response 1S: Limit raise with 3+ support"
    return "PASS", "Response 1S: Weak hand, Pass"

# ==========================================
# 5. RESPONSE TO 1N (เพิ่มโครงสร้างฟังก์ชันจริง - Stayman / Transfer ฯลฯ)
# ==========================================
def response_1n(hcp, shape, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    # ตัวอย่าง: Stayman check
    if hcp >= 8 and (s >= 4 or h >= 4):
        return "2C", "Response 1N: Stayman (8+ HCP with 4+ Major)"
    # ตัวอย่าง: Transfer to Hearts (ถ้ามี Spades 5 ตัว หรือตามระบบของคุณ)
    if hcp >= 0 and h >= 5:
        return "2D", "Response 1N: Transfer to Hearts"
    if hcp >= 0 and s >= 5:
        return "2H", "Response 1N: Transfer to Spades"
    if 0 <= hcp <= 7:
        return "PASS", "Response 1N: Weak hand (0-7 HCP), Pass"
    return "2N", "Response 1N: Invitational (8-9 HCP)"

# ==========================================
# 6. OPENING PRACTICE (เพิ่มโครงสร้างฟังก์ชันจริง)
# ==========================================
def opening_bid(hcp, shape, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    if hcp < 12:
        return "PASS", "Opening: Less than 12 HCP, Pass"
    if balanced and 15 <= hcp <= 17:
        return "1N", "Opening: Balanced hand with 15-17 HCP"
    if h >= 5 and h >= s:
        return "1H", "Opening: 5+ Hearts"
    if s >= 5 and s > h:
        return "1S", "Opening: 5+ Spades"
    if d >= c:
        return "1D", "Opening: Better Minor (Diamonds)"
    return "1C", "Opening: Clubs"

# ==========================================
# EVALUATE ROUTER
# ==========================================
def evaluate_answer(mode, hcp, shape, hand):
    balanced = shape in BALANCED_SHAPES
    
    if mode == "opening":
        return opening_bid(hcp, shape, balanced)
    elif mode == "resp_1c":
        return response_1c(hcp, shape, balanced)
    elif mode == "resp_1d":
        return response_1d(hcp, shape, balanced)
    elif mode == "resp_1h":
        return response_1h(hcp, shape, balanced)
    elif mode == "resp_1s":
        return response_1s(hcp, shape, balanced)
    elif mode == "resp_1n":
        return response_1n(hcp, shape, balanced)
    else:
        return "PASS", "Default Rule"

def generate_practice_questions(mode, total=20):
    questions = []
    seen = set()
    while len(questions) < total:
        hcp, shape, cards = generate_unique_hand()
        ans, rule_desc = evaluate_answer(mode, hcp, shape, cards)
        
        key = f"{hcp}_{shape}"
        if key not in seen:
            seen.add(key)
            questions.append({
                "hcp": hcp,
                "shape": shape,
                "balanced": shape in BALANCED_SHAPES,
                "cards": cards,
                "correct_answer": ans,
                "rule_description": rule_desc
            })
    return questions
