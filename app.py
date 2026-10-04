import random

# ลำดับความสูงของการบิดทั้งหมดในบริดจ์ (ใช้อ้างอิงการกรองปุ่ม)
BID_RANKING = {
    "Pass": 0,
    "1C": 1, "1D": 2, "1H": 3, "1S": 4, "1N": 5,
    "2C": 6, "2D": 7, "2H": 8, "2S": 9, "2N": 10,
    "3C": 11, "3D": 12, "3H": 13, "3S": 14, "3N": 15,
    "4C": 16, "4D": 17, "4H": 18, "4S": 19, "4N": 20,
    "5C": 21, "5D": 22, "5H": 23, "5S": 24, "5N": 25,
    "6C": 26, "6D": 27, "6H": 28, "6S": 29, "6N": 30,
    "7C": 31, "7D": 32, "7H": 33, "7S": 34, "7N": 35
}

# ฟังก์ชันเช็คทรงไพ่ Balanced (เช่น 4333, 4432, 5332)
def is_balanced(shape):
    s, h, d, c = shape
    if 0 in shape or 1 in shape:
        return False
    if any(x >= 6 for x in shape):
        return False
    five_count = sum(1 for x in shape if x == 5)
    return five_count <= 1

# ฟังก์ชันเช็คว่ามีชุดสั้น 2 หรือ 3 ใบที่แย่ๆ (ไม่มี A, K, Q ค้ำ) หรือไม่
def has_bad_short_suit(suit_cards, shape):
    honors = ['A', 'K', 'Q']
    for suit_name, length in zip(['S', 'H', 'D', 'C'], shape):
        if length == 2 or length == 3:
            cards = suit_cards.get(suit_name, [])
            has_honor = any(c in honors for c in cards)
            if not has_honor:
                return True
    return False

# ฟังก์ชัน Response ต่อ 1C
def logic_resp_1c(hcp, shape, counts, suit_cards):
    s, h, d, c = shape

    # Priority สูงสุด: 13+ HCP, Balanced, มี M = 4 และไม่มีชุดสั้นแย่ๆ
    if hcp >= 13 and is_balanced(shape) and (s == 4 or h == 4) and not has_bad_short_suit(suit_cards, shape):
        return "1N", "13+ Balanced with M=4 and Good Holding"

    # ระบบเปิด 1C ของคุณ: ตอบ 1D โชว์ H4+, ตอบ 1H โชว์ S4+
    if h >= 4 and s >= 4:
        if s > h:
            return "1H", "Both M4+, S longer (Show S via 1H)"
        elif h > s:
            return "1D", "Both M4+, H longer (Show H via 1D)"
        elif s >= 5:
            return "1H", "Equal 5-5+ Majors, show S via 1H"
        else:
            return "1D", "Equal 4-4 Majors, show H via 1D"

    if h >= 4:
        return "1D", "H4+ (Show H)"
    if s >= 4:
        return "1H", "S4+ (Show S)"

    # เงื่อนไขพิเศษ: เปิด 1C ถ้ามี M5 หรือ M4C4+ แม้แต้ม 0-5 ก็ต้องโชว์ M
    if hcp <= 5:
        if h >= 5 or s >= 5:
            if s >= h:
                return "1H", "Low HCP (0-5) but has S5+ (Open 1C)"
            else:
                return "1D", "Low HCP (0-5) but has H5+ (Open 1C)"
        if (h >= 4 or s >= 4) and c >= 4:
            if s >= h:
                return "1H", "Low HCP (0-5) but has S4+ C4+ (Open 1C)"
            else:
                return "1D", "Low HCP (0-5) but has H4+ C4+ (Open 1C)"

    has_m55 = (d >= 5 and c >= 5)
    if 0 <= hcp <= 5 and c >= 6:
        return "2N", "0-5 HCP, C6+"
    if 5 <= hcp <= 10 and has_m55:
        return "2S", "m55"
    if 5 <= hcp <= 10 and c >= 6:
        return "3C", "C6+"
    if 0 <= hcp <= 10 and d >= 6:
        return "2C", "D6 no M4"
    if 11 <= hcp <= 12 and d >= 5:
        return "2C", "D5 no M4"
    if 11 <= hcp <= 12 and c >= 5:
        return "2D", "C5+ M<4"
    if 11 <= hcp <= 12 and is_balanced(shape):
        return "2H", "Balanced"
    if 5 <= hcp <= 10:
        return "1S", "M<4"
    if hcp >= 13:
        return "1N", "13+ M<4"

    # Priority สุดท้าย: ถ้าไม่เข้าเงื่อนไขไหนเลย ค่อย Pass
    return "Pass", "Default Pass (No other bids matched)"


# ฟังก์ชัน Response ต่อ 1D
def logic_resp_1d(hcp, shape, counts, suit_cards):
    s, h, d, c = shape

    # Priority สูงสุด: 13+ HCP, Balanced, มี M = 4 และไม่มีชุดสั้นแย่ๆ
    if hcp >= 13 and is_balanced(shape) and (s == 4 or h == 4) and not has_bad_short_suit(suit_cards, shape):
        return "1N", "13+ Balanced with M=4 and Good Holding"

    # ระบบเปิด 1D ของคุณ: ตอบ 1H โชว์ H4+, ตอบ 1S โชว์ S4+
    if h >= 4 and s >= 4:
        if s > h:
            return "1S", "Both M4+, S longer than H"
        elif h > s:
            return "1H", "Both M4+, H longer than S"
        elif s >= 5:
            return "1S", "Equal 5-5+ Majors, show S first"
        else:
            return "1H", "Equal 4-4 Majors, show H first"

    if h >= 4:
        return "1H", "H4+ (Show H)"
    if s >= 4:
        return "1S", "S4+ (Show S)"

    # เงื่อนไขพิเศษ: เปิด 1D แต้ม 0-5 ต้องมีครบทั้ง M4+ และ D4+ ถึงจะตอบโชว์ได้
    if hcp <= 5:
        if (h >= 4 or s >= 4) and d >= 4:
            if s >= h:
                return "1S", "Low HCP (0-5) but has S4+ D4+ (Support D)"
            else:
                return "1H", "Low HCP (0-5) but has H4+ D4+ (Support D)"

    if 0 <= hcp <= 5 and d >= 5:
        return "2N", "0-5 HCP, D5+"
    if hcp >= 13:
        return "1N", "13+ M<4"
    if 5 <= hcp <= 10 and c == 5 and d < 3:
        return "2C", "C=5"
    if 5 <= hcp <= 10 and c >= 6 and d < 4:
        return "2C", "C6+"
    if 5 <= hcp <= 10 and 3 <= d <= 4:
        return "2D", "D 3-4"
    if 11 <= hcp <= 12 and is_balanced(shape):
        return "2H", "Balanced"
    if 11 <= hcp <= 12 and c >= 5:
        return "2S", "C5+ Unbalanced"
    if 11 <= hcp <= 12 and d >= 4:
        return "3C", "D4+ Unbalanced"
    if 5 <= hcp <= 10 and d == 5:
        return "3D", "D=5"

    # Priority สุดท้าย: ถ้าไม่เข้าเงื่อนไขไหนเลย ค่อย Pass
    return "Pass", "Default Pass (No other bids matched)"


# ฟังก์ชันกรองปุ่มกดคำตอบ (ซ่อนบิดที่ต่ำกว่าหรือเท่ากับการบิดล่าสุด เช่น เปิด 1N ซ่อน 1C-1N)
def get_allowed_bids(last_bid):
    all_bids = list(BID_RANKING.keys())
    last_rank = BID_RANKING.get(last_bid, 0)
    
    allowed = ["Pass"] # อนุญาตให้ Pass ได้เสมอ
    for bid in all_bids:
        if bid != "Pass" and BID_RANKING[bid] > last_rank:
            allowed.append(bid)
            
    return allowed
