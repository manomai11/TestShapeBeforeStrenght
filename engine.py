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

# ฟังก์ชันจำลองสุ่มแจกหน้าไพ่ตาม Shape และ HCP
def generate_cards_from_shape(shape_str):
    ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    # สุ่มแจกไพ่ตามความยาวแต่ละชุด (♠, ♥, ♦, ♣)
    lengths = [int(x) for x in shape_str]
    suits = ["♠", "♥", "♦", "♣"]
    deck = [r+s for s in ['s','h','d','c'] for r in ranks]
    random.shuffle(deck)
    
    hand = {"♠": [], "♥": [], "♦": [], "♣": []}
    suit_keys = ["♠", "♥", "♦", "♣"]
    
    # จัดกลุ่มไพ่จำลองตามความยาว Shape
    available_cards = deck.copy()
    for idx, slen in enumerate(lengths):
        s_name = suit_keys[idx]
        chosen = available_cards[:slen]
        available_cards = available_cards[slen:]
        # เรียงลำดับแต้มคร่าวๆ
        hand[s_name] = sorted(chosen, key=lambda x: ranks.index(x[0]))
    return hand

def generate_random_hand():
    while True:
        s = random.randint(0, 6)
        h = random.randint(0, 6 - s)
        d = random.randint(0, 13 - s - h)
        c = 13 - s - h - d
        if max(s, h, d, c) <= 7:
            shape = f"{s}{h}{d}{c}"
            break
    hcp = random.randint(0, 22)
    return hcp, shape

def generate_practice_questions(mode, total=20):
    questions = []
    seen = set()
    while len(questions) < total:
        hcp, shape = generate_random_hand()
        is_bal = shape in BALANCED_SHAPES
        
        # กำหนดคำตอบตาม Mode
        if mode == "resp_1c":
            ans = "1D" if hcp >= 6 else "PASS"
        elif mode == "resp_1d":
            ans = "1H" if hcp >= 6 else "PASS"
        else:
            ans = "1N"
            
        key = f"{hcp}_{shape}"
        if key not in seen:
            seen.add(key)
            cards = generate_cards_from_shape(shape)
            questions.append({
                "hcp": hcp,
                "shape": shape,
                "balanced": is_bal,
                "cards": cards,
                "correct_answer": ans
            })
    return questions
