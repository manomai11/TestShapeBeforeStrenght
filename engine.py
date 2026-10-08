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

def generate_cards_from_shape(shape_str):
    ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    lengths = [int(x) for x in shape_str]
    suit_keys = ["♠", "♥", "♦", "♣"]
    deck = [r+s for s in ['s','h','d','c'] for r in ranks]
    random.shuffle(deck)
    
    hand = {"♠": [], "♥": [], "♦": [], "♣": []}
    available_cards = deck.copy()
    for idx, slen in enumerate(lengths):
        s_name = suit_keys[idx]
        chosen = available_cards[:slen]
        available_cards = available_cards[slen:]
        hand[s_name] = sorted(chosen, key=lambda x: ranks.index(x[0]))
    return hand

def generate_random_hand():
    while True:
        s = random.randint(0, 5)
        h = random.randint(0, 5 - s)
        d = random.randint(0, 13 - s - h)
        c = 13 - s - h - d
        if max(s, h, d, c) <= 7:
            shape_str = f"{s}{h}{d}{c}"
            break
            
    cards = generate_cards_from_shape(shape_str)
    hcp = calculate_hcp(cards)
    actual_shape = f"{len(cards['♠'])}{len(cards['♥'])}{len(cards['♦'])}{len(cards['♣']) }"
    return hcp, actual_shape.strip(), cards

def generate_practice_questions(mode, total=20):
    questions = []
    seen = set()
    while len(questions) < total:
        hcp, shape, cards = generate_random_hand()
        is_bal = shape in BALANCED_SHAPES
        
        # ตัวอย่างการประเมินคำตอบตาม Rule เบื้องต้น
        if mode == "resp_1c":
            ans = "1D" if hcp >= 6 else "PASS"
        elif mode == "resp_1d":
            ans = "1H" if hcp >= 6 else "PASS"
        elif mode == "resp_1h":
            ans = "1S" if hcp >= 6 else "1N"
        else:
            ans = "1N"
            
        key = f"{hcp}_{shape}"
        if key not in seen:
            seen.add(key)
            questions.append({
                "hcp": hcp,
                "shape": shape,
                "balanced": is_bal,
                "cards": cards,
                "correct_answer": ans
            })
    return questions
