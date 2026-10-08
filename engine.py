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
    suits = ['♠', '♥', '♦', '♣']
    deck = [r + s for s in suits for r in ranks]
    
    while True:
        random.shuffle(deck)
        # สุ่มแบ่งไพ่ 13 ใบให้ครบ 4 ชุดโดยไม่ให้ซ้ำกัน
        hand_cards = {"♠": [], "♥": [], "♦": [], "♣": []}
        
        # แจกไพ่แบบสุ่มความยาวแต่รวมกันได้ 13 ใบเป๊ะ
        s_len = random.randint(1, 9)
        h_len = random.randint(1, 9)
        d_len = random.randint(1, 9)
        c_len = 13 - (s_len + h_len + d_len)
        
        if 0 <= c_len <= 9:
            lengths = {"♠": s_len, "♥": h_len, "♦": d_len, "♣": c_len}
            deck_copy = deck.copy()
            valid = True
            for suit, slen in lengths.items():
                if slen > 0:
                    cards = [deck_copy.pop(0) for _ in range(slen)]
                    hand_cards[suit] = sorted(cards, key=lambda x: ranks.index(x[0]))
            
            # ตรวจสอบความถูกต้องว่าไพ่ครบ 13 ใบและไม่มีใบซ้ำ
            all_cards = [c for suit in hand_cards.values() for c in suit]
            if len(all_cards) == 13 and len(set(all_cards)) == 13:
                shape_str = f"{len(hand_cards['♠'])}{len(hand_cards['♥'])}{len(hand_cards['♦'])}{len(hand_cards['♣'])}"
                
                # แปลงรูปแบบให้ match กับระบบเช็คค่าไพ่ (ตัดสัญลักษณ์ชุดออกเหลือแค่ตัวอักษร rank สำหรับเช็คเงื่อนไข หรือใช้ตามโครงสร้างเดิม)
                cleaned_hand = {
                    "♠": [c[0] for c in hand_cards["♠"]],
                    "♥": [c[0] for c in hand_cards["♥"]],
                    "♦": [c[0] for c in hand_cards["♦"]],
                    "♣": [c[0] for c in hand_cards["♣"]]
                }
                
                # เก็บแบบแสดงผลเต็มใบไว้โชว์หน้าเว็บ (ถ้าตัวแปร cards หน้าเว็บต้องการแบบมีดอกด้วย)
                display_hand = {
                    "♠": hand_cards["♠"],
                    "♥": hand_cards["♥"],
                    "♦": hand_cards["♦"],
                    "♣": hand_cards["♣"]
                }
                
                hcp = calculate_hcp(cleaned_hand)
                return hcp, shape_str, display_hand

def has_honor(card_list, honors):
    return any(c[0] in honors for c in card_list)

def is_bad_suit(cards, length):
    if length == 2 and not has_honor(cards, ['A', 'K', 'Q']):
        return True
    if length == 3 and not has_honor(cards, ['A', 'K', 'Q', 'J']):
        return True
    return False

# ==========================================
# OPENING RULES
# ==========================================
def opening_bid(hcp, shape, hand, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    s_cards, h_cards, d_cards, c_cards = hand["♠"], hand["♥"], hand["♦"], hand["♣"]
    
    def max_other(exclude_suit):
        other_suits = [s, h, d, c]
        other_suits.pop(exclude_suit)
        return max(other_suits)

    s_top4 = len(s_cards) >= 7 and all(r in [card[0] for card in s_cards] for r in ['A', 'K', 'Q', 'J'])
    s_top3_8 = len(s_cards) >= 8 and all(r in [card[0] for card in s_cards] for r in ['A', 'K', 'Q'])
    h_top4 = len(h_cards) >= 7 and all(r in [card[0] for card in h_cards] for r in ['A', 'K', 'Q', 'J'])
    h_top3_8 = len(h_cards) >= 8 and all(r in [card[0] for card in h_cards] for r in ['A', 'K', 'Q'])
    
    if 9 <= hcp <= 11 and (s_top4 or s_top3_8 or h_top4 or h_top3_8):
        return "3N", "Rule 1: Solid Major 7+ or 8+"

    if 0 <= hcp <= 10 and s == 8 and max_other(0) <= 4:
        return "4S", "Rule 2: 8 Spades"
    if 0 <= hcp <= 10 and h == 8 and max_other(1) <= 4:
        return "4H", "Rule 3: 8 Hearts"
    if 0 <= hcp <= 10 and d == 8 and max_other(2) <= 4:
        return "4D", "Rule 4: 8 Diamonds"
    if 0 <= hcp <= 10 and c == 8 and max_other(3) <= 4:
        return "4C", "Rule 5: 8 Clubs"

    if 5 <= hcp <= 10 and s == 7 and max_other(0) <= 4:
        return "3S", "Rule 6: 7 Spades"
    if 5 <= hcp <= 10 and h == 7 and max_other(1) <= 4:
        return "3H", "Rule 3: 7 Hearts"
    if 5 <= hcp <= 10 and d == 7 and max_other(2) <= 4:
        return "3D", "Rule 4: 7 Diamonds"
    if 5 <= hcp <= 10 and c == 7 and max_other(3) <= 4:
        return "3C", "Rule 5: 7 Clubs"

    if hcp >= 21:
        return "2C", "Rule 7: 21+ HCP"
    if 17 <= hcp <= 20 and s >= 5 and h >= 5:
        return "2D", "Rule 8: 17-20 HCP, M55"
    if 6 <= hcp <= 10 and ((s == 6 and max_other(0) <= 4) or (h == 6 and max_other(1) <= 4)):
        return "2D", "Rule 9: 6-10 HCP, 6-card Major"
    if 11 <= hcp <= 13 and s == 6 and max_other(0) <= 4:
        return "2S", "Rule 10: 11-13 HCP, 6 Spades"
    if 11 <= hcp <= 13 and h == 6 and max_other(1) <= 4:
        return "2H", "Rule 11: 11-13 HCP, 6 Hearts"

    if 11 <= hcp <= 20 and s >= 5 and s >= h:
        return "1S", "Rule 15: 5+ Spades"
    if 11 <= hcp <= 20 and h >= 5 and h > s:
        return "1H", "Rule 16: 5+ Hearts"

    shapes_set = {s, h, d, c}
    if 11 <= hcp <= 20 and shapes_set == {1, 4} and list(shape).count('1') == 1:
        return "1D", "Rule: 4441 shape"
    if 11 <= hcp <= 20 and shape in ["4414", "4144", "1444"]:
        return "1C", "Rule: 4414 shape"
    if 11 <= hcp <= 15 and d == 4 and c == 5:
        return "1D", "Rule: D=4, C=5"
    if 11 <= hcp <= 20 and d >= 5 and d >= c:
        return "1D", "Rule: 5+ Diamonds"
    if 11 <= hcp <= 20 and c >= 5 and c > d:
        return "1C", "Rule: 5+ Clubs"

    return "PASS", "Rule 20: Pass"

# ==========================================
# RESPONSE TO 1N RULES
# ==========================================
def response_1n(hcp, shape, hand, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    
    def max_other(exclude_suit):
        other_suits = [s, h, d, c]
        other_suits.pop(exclude_suit)
        return max(other_suits)

    if hcp >= 9 and s >= 5 and h >= 5:
        return "3D", "Rule 1"
    if hcp == 8 and s >= 5 and h >= 5:
        return "2C", "Rule 2"
    if 0 <= hcp <= 26 and d >= 5 and c >= 5:
        return "2D", "Rule 3"
    if (10 <= hcp <= 12 and s == 6 and max_other(0) <= 4) or (6 <= hcp <= 12 and s == 7) or (0 <= hcp <= 12 and s >= 8):
        return "4D", "Rule 4"
    if (10 <= hcp <= 12 and h == 6 and max_other(1) <= 4) or (6 <= hcp <= 12 and h == 7) or (0 <= hcp <= 12 and h >= 8):
        return "4C", "Rule 5"
    if 11 <= hcp <= 26 and shape in ["1345", "1354"]:
        return "3S", "Rule 6"
    if 11 <= hcp <= 26 and shape in ["3145", "3154"]:
        return "3H", "Rule 7"
    if 11 <= hcp <= 15 and shape in ["2254", "2245"]:
        return "3N", "Rule 8"
    if 10 <= hcp <= 12 and s < 3 and h < 3 and (d == 6 or c == 6):
        return "3N", "Rule 9"
    if hcp == 10 and (3 <= s <= 4 or 3 <= h <= 4) and (d == 6 or c == 6):
        return "3C", "Rule 12"
    if (0 <= hcp <= 9 or hcp >= 13) and d >= 6 and s < 4 and h < 4:
        return "2N", "Rule 13"
    if 10 <= hcp <= 12 and d >= 7:
        return "2N", "Rule 14"
    if (0 <= hcp <= 9 or hcp >= 13) and c >= 6 and s < 4 and h < 4:
        return "2S", "Rule 15"
    if 10 <= hcp <= 12 and c >= 7:
        return "2S", "Rule 16"
    if s >= 5 and s >= h:
        return "2H", "Rule 17"
    if hcp >= 10 and s >= 5 and h < 4:
        return "2H", "Rule 18"
    if h >= 5 and h > s:
        return "2D", "Rule 19"
    if hcp >= 10 and h >= 5 and h > s:
        return "2D", "Rule 20"
    if hcp >= 16 and s < 5 and h < 5:
        return "2C", "Rule 21"
    if hcp >= 10 and ((s >= 5 and h == 4) or (h >= 5 and s == 4)):
        return "2C", "Rule 22"
    if hcp == 10 and s < 5 and h < 5:
        return "2C", "Rule 23"
    if hcp == 9 and (5 <= s <= 6 or 5 <= h <= 6 or (s >= 5 and d >= 5) or (h >= 5 and c >= 5)):
        return "2C", "Rule 24"

    return "PASS", "Rule 25"

# ==========================================
# RESPONSE TO 1C RULES
# ==========================================
def response_1c(hcp, shape, hand, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    bad_suit = is_bad_suit(hand["♠"], s) or is_bad_suit(hand["♥"], h) or is_bad_suit(hand["♦"], d) or is_bad_suit(hand["♣"], c)

    if hcp >= 13 and balanced and not bad_suit and (s == 4 or h == 4):
        return "1N"
    if h >= 4 and ((h == 4 and s == 4) or h > s):
        return "1D"
    if s >= 4 and not (s == 4 and h == 4) and s >= h:
        return "1H"
    if 11 <= hcp <= 12 and c == 5:
        return "2D"
    if 11 <= hcp <= 12 and balanced and s < 4 and h < 4 and d < 5 and c < 5:
        return "2H"
    if 6 <= hcp <= 10 and d >= 6 and s < 4 and h < 4:
        return "2C"
    if 11 <= hcp <= 12 and d >= 5 and s < 4 and h < 4:
        return "2C"
    if 0 <= hcp <= 5 and d >= 7 and s < 4 and h < 4:
        return "2C"
    if 6 <= hcp <= 10 and d >= 5 and c >= 5:
        return "2S"
    if 0 <= hcp <= 5 and c >= 6:
        return "2N"
    if 6 <= hcp <= 10 and c >= 6:
        return "3C"
    if 6 <= hcp <= 10 and s < 4 and h < 4 and d < 6 and c < 6:
        return "1S"

    return "PASS"

# ==========================================
# EVALUATE ROUTER
# ==========================================
def evaluate_answer(mode, hcp, shape, hand):
    balanced = shape in BALANCED_SHAPES
    if mode == "opening":
        return opening_bid(hcp, shape, hand, balanced)
def generate_practice_questions(mode, total=20):
    questions = []
    seen = set()
    while len(questions) < total:
        hcp, shape, cards = generate_unique_hand()
        
        # ป้องกันกรณีบางฟังก์ชัน return ค่าเดียวหรือสองค่า
        result = evaluate_answer(mode, hcp, shape, cards)
        if isinstance(result, tuple):
            ans, rule_desc = result
        else:
            ans, rule_desc = result, "Rule Match"
        
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
