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

# ฟังก์ชันสุ่มแจกไพ่แบบสำรับจริง (ไม่มีไพ่ซ้ำในมือ)
def generate_unique_hand():
    ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    suits = ['s', 'h', 'd', 'c']
    deck = [r+s for s in suits for r in ranks]
    
    while True:
        random.shuffle(deck)
        # สุ่มความยาว Shape ให้ผลรวมเป็น 13
        s_len = random.randint(1, 6)
        h_len = random.randint(1, 6)
        d_len = random.randint(1, 6)
        c_len = 13 - (s_len + h_len + d_len)
        
        if 0 <= c_len <= 7:
            lengths = {"♠": s_len, "♥": h_len, "♦": d_len, "♣": c_len}
            hand = {"♠": [], "♥": [], "♦": [], "♣": []}
            
            deck_copy = deck.copy()
            valid = True
            for suit, slen in lengths.items():
                if slen > 0:
                    cards = [deck_copy.pop(0) for _ in range(slen)]
                    # เรียงลำดับแต้มจากใหญ่ไปเล็ก
                    hand[suit] = sorted(cards, key=lambda x: ranks.index(x[0]))
            
            if valid:
                shape_str = f"{len(hand['♠'])}{len(hand['♥'])}{len(hand['♦'])}{len(hand['♣'])}"
                hcp = calculate_hcp(hand)
                return hcp, shape_str, hand

# ฟังก์ชันประเมินคำตอบพร้อมเหตุผล Rule
def evaluate_answer(mode, hcp, shape, hand):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    balanced = shape in BALANCED_SHAPES
    
    # ตัวอย่างการตรวจสอบตาม Rule ของคุณ (สามารถนำฟังก์ชันสมบูรณ์ที่คุณเขียนมาใส่แทนตรงนี้ได้เลย)
    if mode == "resp_1n":
        # ตัวอย่าง: ตอบตามกฎ Response to 1N
        if hcp >= 8 and (s >= 4 or h >= 4):
            return "2C", "Rule: Stayman (8+ HCP with 4+ Major)"
        elif hcp <= 7:
            return "PASS", "Rule: Weak hand (0-7 HCP), pass 1NT"
        else:
            return "2N", "Rule: Invitational without 4-card major"
            
    elif mode == "resp_1c":
        if hcp >= 6 and s >= 4 and s >= h:
            return "1H", "Rule: Showing Spades with 6+ HCP"
        elif hcp >= 13:
            return "3C", "Rule: Limit raise or strong minor support"
        else:
            return "1D", "Rule: Standard response structure"
            
    # ค่าเริ่มต้นพื้นฐาน
    return "1N", "Rule: Standard Bidding Evaluation"

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
