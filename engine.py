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

SPECIAL_D4C5 = {
    "4045", "0445", "3145", "1345", "2245"
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

# สุ่มไพ่จากสำรับมาตรฐาน 52 ใบจริง (ไม่มีทางซ้ำกัน)
def generate_unique_hand():
    ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    suits = ['s', 'h', 'd', 'c']
    deck = [r+s for s in suits for r in ranks]
    
    while True:
        random.shuffle(deck)
        # สุ่มความยาวให้รวมกันได้ 13 ใบ
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
# รวมกฎการประมูลทั้งหมดของคุณ (Opening & Responses)
# ==========================================

def response_1c(hcp, shape, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    if hcp >= 13 and balanced and (s == 4 or h == 4):
        return "1N", "13+ HCP, Balanced with 4-card Major -> Bid 1N"
    if h >= 4 and ((h == 4 and s == 4) or h > s):
        return "1D", "Showing Hearts (Transfer style)"
    if s >= 4 and not (s == 4 and h == 4) and s >= h:
        return "1H", "Showing Spades"
    if 6 <= hcp <= 10 and d >= 6:
        return "2C", "6+ Diamonds with invitational values"
    if hcp >= 6 and s < 4 and h < 4 and d < 6 and c < 6:
        return "1S", "Standard minor response"
    return "PASS", "Standard Pass rule"

def response_1d(hcp, shape, balanced=False, bad_suit=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    if hcp >= 13 and s < 3 and h < 3:
        return "1N", "13+ HCP with no 3-card Major -> 1N"
    if hcp >= 13 and balanced and not bad_suit and (s == 4 or h == 4):
        return "1N", "13+ HCP Balanced with 4-card Major"
    if 6 <= hcp <= 10 and d >= 5:
        return "3D", "6-10 HCP with 5+ Diamonds Support"
    if hcp >= 6 and s >= 4 and s >= h:
        return "1S", "Showing Spades (4+ cards)"
    if hcp >= 6 and h >= 4 and h > s:
        return "1H", "Showing Hearts (4+ cards)"
    return "PASS", "Pass based on point range"

def evaluate_answer(mode, hcp, shape, hand):
    balanced = shape in BALANCED_SHAPES
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])

    if mode == "resp_1c":
        ans, rule = response_1c(hcp, shape, balanced)
    elif mode == "resp_1d":
        ans, rule = response_1d(hcp, shape, balanced)
    elif mode == "opening":
        if hcp >= 12 and (s >= 5 or h >= 5 or d >= 3 or c >= 3):
            ans = "1H" if h >= s and h >= 5 else ("1S" if s >= 5 else ("1D" if d >= c else "1C"))
            rule = "Standard Opening Bid based on HCP & Longest Suit"
        else:
            ans = "PASS"
            rule = "Insufficient HCP to open (< 12 HCP)"
    else:
        # สำหรับโหมด 1H, 1S, 1N อื่นๆ
        if hcp >= 6:
            ans = "2C"
            rule = f"Standard response to {mode.upper()} with {hcp} HCP"
        else:
            ans = "PASS"
            rule = "Weak hand, Pass"
            
    return ans, rule

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
