# ==========================================
# SHAPE BEFORE STRENGTH
# ENGINE V1
# ==========================================

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
    "4045",
    "0445",
    "3145",
    "1345",
    "2245"
}


# ==========================================
# HELPERS
# ==========================================

def shape_lengths(shape):

    return (
        int(shape[0]),
        int(shape[1]),
        int(shape[2]),
        int(shape[3])
    )


def is_balanced(shape):

    return shape in BALANCED_SHAPES


def has_short(shape):

    s,h,d,c = shape_lengths(shape)

    return (
        s <= 1 or
        h <= 1 or
        d <= 1 or
        c <= 1
    )


# ==========================================
# OPENING
# ==========================================
def opening_bid(hcp, shape, hand, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    s_cards, h_cards, d_cards, c_cards = hand["♠"], hand["♥"], hand["♦"], hand["♣"]
    
    # เช็คความยาวชุดรอง (ไม่รวมชุดหลักที่กำลังพิจารณา)
    def max_other(exclude_suit):
        other_suits = [s, h, d, c]
        other_suits.pop(exclude_suit)
        return max(other_suits)

    # Rule 1: 3N | Priority 1100 | 9-11 HCP | solid major 7 cards (AKQJ...) or 8 cards+ (AKQ...)
    s_top4 = len(s_cards) >= 7 and all(r in [c[0] for c in s_cards] for r in ['A', 'K', 'Q', 'J'])
    s_top3_8 = len(s_cards) >= 8 and all(r in [c[0] for c in s_cards] for r in ['A', 'K', 'Q'])
    h_top4 = len(h_cards) >= 7 and all(r in [c[0] for c in h_cards] for r in ['A', 'K', 'Q', 'J'])
    h_top3_8 = len(h_cards) >= 8 and all(r in [c[0] for c in h_cards] for r in ['A', 'K', 'Q'])
    
    if 9 <= hcp <= 11 and (s_top4 or s_top3_8 or h_top4 or h_top3_8):
        return "3N", "Rule 1: 9-11 HCP, solid 7+ card major with AKQJ or 8+ with AKQ (Priority 1100)"

    # Rule 2: 4S | Priority 1000 | 0-10 HCP | S = 8 | no second suit > 4
    if 0 <= hcp <= 10 and s == 8 and max_other(0) <= 4:
        return "4S", "Rule 2: 0-10 HCP, 8 Spades, no second suit > 4 (Priority 1000)"

    # Rule 3: 4H | Priority 980 | 0-10 HCP | H = 8 | no second suit > 4
    if 0 <= hcp <= 10 and h == 8 and max_other(1) <= 4:
        return "4H", "Rule 3: 0-10 HCP, 8 Hearts, no second suit > 4 (Priority 980)"

    # Rule 4: 4D | Priority 960 | 0-10 HCP | D = 8 | no second suit > 4
    if 0 <= hcp <= 10 and d == 8 and max_other(2) <= 4:
        return "4D", "Rule 4: 0-10 HCP, 8 Diamonds, no second suit > 4 (Priority 960)"

    # Rule 5: 4C | Priority 940 | 0-10 HCP | C = 8 | no second suit > 4
    if 0 <= hcp <= 10 and c == 8 and max_other(3) <= 4:
        return "4C", "Rule 5: 0-10 HCP, 8 Clubs, no second suit > 4 (Priority 940)"

    # Rule 6 (แรก): 3S | Priority 800 | 5-10 HCP | S = 7 | no second suit > 4
    if 5 <= hcp <= 10 and s == 7 and max_other(0) <= 4:
        return "3S", "Rule 6: 5-10 HCP, 7 Spades, no second suit > 4 (Priority 800)"

    # Rule 3: 3H | Priority 780 | 5-10 HCP | H = 7 | no second suit > 4
    if 5 <= hcp <= 10 and h == 7 and max_other(1) <= 4:
        return "3H", "Rule 3: 5-10 HCP, 7 Hearts, no second suit > 4 (Priority 780)"

    # Rule 4: 3D | Priority 760 | 5-10 HCP | D = 7 | no second suit > 4
    if 5 <= hcp <= 10 and d == 7 and max_other(2) <= 4:
        return "3D", "Rule 4: 5-10 HCP, 7 Diamonds, no second suit > 4 (Priority 760)"

    # Rule 5: 3C | Priority 740 | 5-10 HCP | C = 7 | no second suit > 4
    if 5 <= hcp <= 10 and c == 7 and max_other(3) <= 4:
        return "3C", "Rule 5: 5-10 HCP, 7 Clubs, no second suit > 4 (Priority 740)"

    # Rule 7: 2C | Priority 500 | 21+ HCP
    if hcp >= 21:
        return "2C", "Rule 7: 21+ HCP (Priority 500)"

    # Rule 8: 2D | Priority 400 | 17-20 HCP | M55 (S>=5 and H>=5)
    if 17 <= hcp <= 20 and s >= 5 and h >= 5:
        return "2D", "Rule 8: 17-20 HCP, 5+ Spades and 5+ Hearts (Priority 400)"

    # Rule 9: 2D | Priority 380 | 6-10 HCP | M6 (S=6 or H=6) | no second suit > 4
    if 6 <= hcp <= 10 and ((s == 6 and max_other(0) <= 4) or (h == 6 and max_other(1) <= 4)):
        return "2D", "Rule 9: 6-10 HCP, 6-card Major, no second suit > 4 (Priority 380)"

    # Rule 10: 2S | Priority 350 | 11-13 HCP | S = 6 | no second suit > 4
    if 11 <= hcp <= 13 and s == 6 and max_other(0) <= 4:
        return "2S", "Rule 10: 11-13 HCP, 6 Spades, no second suit > 4 (Priority 350)"

    # Rule 11: 2H | Priority 330 | 11-13 HCP | H = 6 | no second suit > 4
    if 11 <= hcp <= 13 and h == 6 and max_other(1) <= 4:
        return "2H", "Rule 11: 11-13 HCP, 6 Hearts, no second suit > 4 (Priority 330)"

    # Rule 15: 1S | Priority 140 | 11-20 HCP | S >= 5 | S >= H
    if 11 <= hcp <= 20 and s >= 5 and s >= h:
        return "1S", "Rule 15: 11-20 HCP, 5+ Spades, Spades >= Hearts (Priority 140)"

    # Rule 16: 1H | Priority 120 | 11-20 HCP | H >= 5 | H > S
    if 11 <= hcp <= 20 and h >= 5 and h > s:
        return "1H", "Rule 16: 11-20 HCP, 5+ Hearts, Hearts > Spades (Priority 120)"

    # Rule 15: 1D | Priority 100 | 11-20 HCP | 4441 shape (มี 1 ใบหนึ่งชุด และอีก 3 ชุดมี 4 ใบ)
    shapes_set = {s, h, d, c}
    if 11 <= hcp <= 20 and shapes_set == {1, 4} and list(shape).count('1') == 1:
        return "1D", "Rule 15: 11-20 HCP, 4441 shape (Priority 100)"

    # Rule 16: 1C | Priority 80 | 11-20 HCP | 4414 shape (C เป็น 4, ตัวอื่นมี 4, 4, 1) -> ปรับเช็ค 4414 ตามความเหมาะสม
    if 11 <= hcp <= 20 and shape in ["4414", "4144", "1444"]: # หรือปรับตามโครงสร้าง 4414 จริง
        return "1C", "Rule 16: 11-20 HCP, 4414 distribution (Priority 80)"

    # Rule 17: 1D | Priority 60 | 11-15 HCP | D = 4 and C = 5
    if 11 <= hcp <= 15 and d == 4 and c == 5:
        return "1D", "Rule 17: 11-15 HCP, Diamonds=4 and Clubs=5 (Priority 60)"

    # Rule 18: 1D | Priority 40 | 11-20 HCP | D >= 5 | D >= C
    if 11 <= hcp <= 20 and d >= 5 and d >= c:
        return "1D", "Rule 18: 11-20 HCP, 5+ Diamonds, Diamonds >= Clubs (Priority 40)"

    # Rule 19: 1C | Priority 20 | 11-20 HCP | C >= 5 | C > D
    if 11 <= hcp <= 20 and c >= 5 and c > d:
        return "1C", "Rule 19: 11-20 HCP, 5+ Clubs, Clubs > Diamonds (Priority 20)"

    # Rule 20: Pass | Priority 10 | 0-10 HCP (หรือเคสอื่นๆ ที่เปิดไม่ได้)
    return "PASS", "Rule 20: Insufficient values to open / Pass (Priority 10)"


# ==========================================
# RESPONSE 1NT
# ==========================================

# ==========================================
# RESPONSE TO 1N RULES (ตามข้อตกลงของคุณ)
# ==========================================
def response_1n(hcp, shape, hand, balanced=False):
    s, h, d, c = int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3])
    
    def max_other(exclude_suit):
        other_suits = [s, h, d, c]
        other_suits.pop(exclude_suit)
        return max(other_suits)

    # Rule 1: 3D | Priority 1000 | 9+ HCP | M55 (S>=5 and H>=5)
    if hcp >= 9 and s >= 5 and h >= 5:
        return "3D", "Rule 1: 9+ HCP, 5+ Spades and 5+ Hearts (Priority 1000)"

    # Rule 2: 2C | Priority 980 | 8 HCP | M55 (S>=5 and H>=5)
    if hcp == 8 and s >= 5 and h >= 5:
        return "2C", "Rule 2: 8 HCP, 5+ Spades and 5+ Hearts (Priority 980)"

    # Rule 3: 2D | Priority 950 | 0-26 HCP | m55 (D>=5 and C>=5)
    if 0 <= hcp <= 26 and d >= 5 and c >= 5:
        return "2D", "Rule 3: 0-26 HCP, 5+ Diamonds and 5+ Clubs (Priority 950)"

    # Rule 4: 4D | Priority 800 | 10-12 HCP & S=6 (no second >4) OR 6-12 HCP & S=7 OR 0-12 HCP & S>=8
    if (10 <= hcp <= 12 and s == 6 and max_other(0) <= 4) or (6 <= hcp <= 12 and s == 7) or (0 <= hcp <= 12 and s >= 8):
        return "4D", "Rule 4: Spades length/HCP condition (Priority 800)"

    # Rule 5: 4C | Priority 780 | 10-12 HCP & H=6 (no second >4) OR 6-12 HCP & H=7 OR 0-12 HCP & H>=8
    if (10 <= hcp <= 12 and h == 6 and max_other(1) <= 4) or (6 <= hcp <= 12 and h == 7) or (0 <= hcp <= 12 and h >= 8):
        return "4C", "Rule 5: Hearts length/HCP condition (Priority 780)"

    # Rule 6: 3S | Priority 700 | 11-26 HCP | Shape 1345 or 1354
    if 11 <= hcp <= 26 and shape in ["1345", "1354"]:
        return "3S", "Rule 6: 11-26 HCP, shape 1345 or 1354 (Priority 700)"

    # Rule 7: 3H | Priority 680 | 11-26 HCP | Shape 3145 or 3154
    if 11 <= hcp <= 26 and shape in ["3145", "3154"]:
        return "3H", "Rule 7: 11-26 HCP, shape 3145 or 3154 (Priority 680)"

    # Rule 8: 3N | Priority 650 | 11-15 HCP | Shape 2254 or 2245
    if 11 <= hcp <= 15 and shape in ["2254", "2245"]:
        return "3N", "Rule 8: 11-15 HCP, shape 2254 or 2245 (Priority 650)"

    # Rule 9: 3N | Priority 630 | 10-12 HCP | M < 3 and minor = 6
    if 10 <= hcp <= 12 and s < 3 and h < 3 and (d == 6 or c == 6):
        return "3N", "Rule 9: 10-12 HCP, no major support, 6-card minor (Priority 630)"

    # Rule 12: 3C | Priority 450 | 10 HCP | Major 3-4 cards | minor = 6
    if hcp == 10 and (3 <= s <= 4 or 3 <= h <= 4) and (d == 6 or c == 6):
        return "3C", "Rule 12: 10 HCP, Major fit search, 6-card minor (Priority 450)"

    # Rule 13: 2N | Priority 450 | 0-9 or 13+ HCP | D >= 6 and M < 4
    if (0 <= hcp <= 9 or hcp >= 13) and d >= 6 and s < 4 and h < 4:
        return "2N", "Rule 13: Diamonds 6+, no 4-card major (Priority 450)"

    # Rule 14: 2N | Priority 430 | 10-12 HCP | D >= 7
    if 10 <= hcp <= 12 and d >= 7:
        return "2N", "Rule 14: 10-12 HCP, 7+ Diamonds (Priority 430)"

    # Rule 15: 2S | Priority 300 | 0-9 or 13+ HCP | C >= 6 and M < 4
    if (0 <= hcp <= 9 or hcp >= 13) and c >= 6 and s < 4 and h < 4:
        return "2S", "Rule 15: Clubs 6+, no 4-card major (Priority 300)"

    # Rule 16: 2S | Priority 380 | 10-12 HCP | C >= 7
    if 10 <= hcp <= 12 and c >= 7:
        return "2S", "Rule 16: 10-12 HCP, 7+ Clubs (Priority 380)"

    # Rule 17: 2H | Priority 200 | S >= 5 and S >= H
    if s >= 5 and s >= h:
        return "2H", "Rule 17: 5+ Spades, Spades >= Hearts (Priority 200)"

    # Rule 18: 2H | Priority 180 | 10+ HCP | S >= 5 and H < 4
    if hcp >= 10 and s >= 5 and h < 4:
        return "2H", "Rule 18: 10+ HCP, 5+ Spades, short hearts (Priority 180)"

    # Rule 19: 2D | Priority 150 | H >= 5 and H > S
    if h >= 5 and h > s:
        return "2D", "Rule 150: 5+ Hearts, Hearts > Spades (Priority 150)"

    # Rule 20: 2D | Priority 120 | 10+ HCP | H >= 5 and H > S
    if hcp >= 10 and h >= 5 and h > s:
        return "2D", "Rule 120: 10+ HCP, 5+ Hearts (Priority 120)"

    # Rule 21: 2C | Priority 100 | 16+ HCP | M < 5
    if hcp >= 16 and s < 5 and h < 5:
        return "2C", "Rule 21: 16+ HCP, invite/forcing without 5-card major (Priority 100)"

    # Rule 22: 2C | Priority 80 | 10+ HCP | M >= 5 and oM = 4 (Stayman variation)
    if hcp >= 10 and ((s >= 5 and h == 4) or (h >= 5 and s == 4)):
        return "2C", "Rule 22: 10+ HCP, 5-card major with 4-card other major (Priority 80)"

    # Rule 23: 2C | Priority 50 | 10 HCP | M < 5
    if hcp == 10 and s < 5 and h < 5:
        return "2C", "Rule 23: 10 HCP, minor/invitational check (Priority 50)"

    # Rule 24: 2C | Priority 30 | 9 HCP | M = 5-6 or M5m5
    if hcp == 9 and (5 <= s <= 6 or 5 <= h <= 6 or (s >= 5 and d >= 5) or (h >= 5 and c >= 5)):
        return "2C", "Rule 24: 9 HCP, Major/Two-suit shape check (Priority 30)"

    # Rule 25: Pass | 0-8 HCP (หรือเคสที่เหลือ)
    return "PASS", "Rule 25: 0-8 HCP / Pass (Priority 10)"


# ==========================================
# RESPONSE 1MAJOR
# ==========================================

def response_1major(
    opening,
    hcp,
    shape,
    has_ace=False
):

    s = int(shape[0])
    h = int(shape[1])
    d = int(shape[2])
    c = int(shape[3])

    trump = h if opening == "1H" else s
    other_major = s if opening == "1H" else h

    has_void = (
        s == 0 or
        h == 0 or
        d == 0 or
        c == 0
    )

    has_short = (
        s <= 1 or
        h <= 1 or
        d <= 1 or
        c <= 1
    )

    # -------------------------
    # SUPPORT 4+
    # -------------------------

    if trump >= 4:

        if hcp >= 13 and has_void:
            return "3D"

        if hcp >= 13 and other_major == 1:

            if opening == "1H":
                return "3S"
            else:
                return "3H"

        if hcp >= 13 and c == 1:
            return "3N"

        if hcp >= 13 and d == 1:
            return "4C"

        if hcp >= 13:
            return "2C"

        if (
            10 <= hcp <= 12
            and has_short
        ):
            return "2N"

        if (
            8 <= hcp <= 12
            and not has_short
        ):
            return "3C"

        if (
            6 <= hcp <= 9
            and trump >= 5
        ):
            return "4H" if opening == "1H" else "4S"

        if (
            6 <= hcp <= 9
            and has_short
        ):
            return "4H" if opening == "1H" else "4S"

        if (
            4 <= hcp <= 7
            and shape != "4333"
            and has_ace
        ):
            return "3H" if opening == "1H" else "3S"

        if (
            0 <= hcp <= 5
            and shape != "4333"
        ):
            return "3D"

        if shape == "4333":

            if hcp >= 5:
                return "2H" if opening == "1H" else "2S"

            return "PASS"

    # -------------------------
    # SUPPORT EXACTLY 3
    # -------------------------

    if trump == 3:

        if hcp >= 13:

            if has_short:

                if opening == "1H":
                    return "2D"
                else:
                    return "2H"

            return "2C"

        if 10 <= hcp <= 12:

            if opening == "1H":
                return "2D"
            else:
                return "2H"

        if 6 <= hcp <= 9:

            if opening == "1H":
                return "2H"
            else:
                return "2S"

        return "PASS"

    # -------------------------
    # OPEN 1S
    # -------------------------

    if opening == "1S":

        if (
            6 <= hcp <= 10
            and h >= 6
            and s < 3
        ):
            return "2D"

        if (
            11 <= hcp <= 12
            and h >= 5
            and s < 4
        ):
            return "2D"

        if hcp >= 13:
            return "2C"

        if 6 <= hcp <= 12:
            return "1N"

        return "PASS"

    # -------------------------
    # OPEN 1H
    # -------------------------

    else:

        if (
            6 <= hcp <= 9
            and s == 6
            and h < 2
        ):
            return "2S"

        if hcp >= 13:
            return "2C"

        if (
            0 <= hcp <= 9
            and s >= 5
            and h < 3
        ):
            return "1N"

        if (
            10 <= hcp <= 11
            and s >= 5
            and h < 4
        ):
            return "1N"

        if 6 <= hcp <= 12:
            return "1S"

        return "PASS"


# ==========================================
# RESPONSE 1D
# ==========================================

def response_1d(
    hcp,
    shape,
    balanced=False,
    bad_suit=False
):

    s = int(shape[0])
    h = int(shape[1])
    d = int(shape[2])
    c = int(shape[3])

    # Rule 1
    # 13+ M<3

    if hcp >= 13 and s < 3 and h < 3:
        return "1N"

    # Rule 2
    # 13+ M=4 Balanced no bad suit

    if (
        hcp >= 13
        and balanced
        and not bad_suit
        and (s == 4 or h == 4)
    ):
        return "1N"

    # Rule 3
    # 10-12 C5+ M<4 C>D

    if (
        10 <= hcp <= 12
        and s < 4
        and h < 4
        and c >= 5
        and c > d
    ):
        return "2S"

    # Rule 4
    # 10-12 D4+ M<4 D>=C

    if (
        10 <= hcp <= 12
        and s < 4
        and h < 4
        and d >= 4
        and d >= c
    ):
        return "3C"

    # Rule 5
    # 11-12 Balanced M<4

    if (
        11 <= hcp <= 12
        and balanced
        and s < 4
        and h < 4
    ):
        return "2H"

    # Rule 6
    # 6-10 D5+ M<4

    if (
        6 <= hcp <= 10
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "3D"

    # Rule 7
    # 6-9 D=4 M<4 short major

    if (
        6 <= hcp <= 9
        and d == 4
        and s < 4
        and h < 4
        and (s <= 1 or h <= 1)
    ):
        return "3D"

    # Rule 8
    # 10 HCP 3325

    if (
        hcp == 10
        and shape == "3325"
    ):
        return "2C"

    # Rule 9
    # 6-9 C6+ D<4

    if (
        6 <= hcp <= 9
        and c >= 6
        and d < 4
        and s < 4
        and h < 4
    ):
        return "2C"

    # Rule 10
    # 6-10 D=3 M<4

    if (
        6 <= hcp <= 10
        and d == 3
        and s < 4
        and h < 4
    ):
        return "2D"

    # Rule 11
    # 0-5 D5+ M<4

    if (
        0 <= hcp <= 5
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "2N"

    # Rule 12
    # 1S
    # 6+ S>=H except 44

    if (
        hcp >= 6
        and s >= 4
        and s >= h
        and not (s == 4 and h == 4)
    ):
        return "1S"

    # Rule 13
    # 0-5 S4+ D4+

    if (
        0 <= hcp <= 5
        and s >= 4
        and d >= 4
        and s >= h
        and not (s == 4 and h == 4)
    ):
        return "1S"

    # Rule 14
    # 1H
    # 6+ H>S

    if (
        hcp >= 6
        and h >= 4
        and h > s
    ):
        return "1H"

    # Rule 15
    # 0-5 H4+ D4+

    if (
        0 <= hcp <= 5
        and h >= 4
        and d >= 4
        and h > s
    ):
        return "1H"

    # Rule 16
    # PASS

    return "PASS"


# ==========================================
# RESPONSE 1C
# ==========================================

def response_1c(
    hcp,
    shape,
    balanced=False,
    bad_suit=False
):

    s = int(shape[0])
    h = int(shape[1])
    d = int(shape[2])
    c = int(shape[3])

    # =====================================
    # RULE 1
    # 13+ M<4
    # =====================================

    if (
        hcp >= 13
        and s < 4
        and h < 4
    ):
        return "1N"

    # =====================================
    # RULE 2
    # 13+ M=4
    # Balanced
    # No Bad Suit
    # =====================================

    if (
        hcp >= 13
        and balanced
        and not bad_suit
        and (s == 4 or h == 4)
    ):
        return "1N"

    # =====================================
    # RULE 3
    # Transfer Hearts
    # H4+
    # 44 or H>S
    # =====================================

    if (
        h >= 4
        and (
            (h == 4 and s == 4)
            or
            h > s
        )
    ):
        return "1D"

    # =====================================
    # RULE 4
    # Transfer Spades
    # S4+
    # S>=H
    # except 44
    # =====================================

    if (
        s >= 4
        and not (s == 4 and h == 4)
        and s >= h
    ):
        return "1H"

    # =====================================
    # RULE 5
    # 11-12 C=5
    # =====================================

    if (
        11 <= hcp <= 12
        and c == 5
    ):
        return "2D"

    # =====================================
    # RULE 6
    # 11-12 Balanced
    # M<4
    # m<5
    # =====================================

    if (
        11 <= hcp <= 12
        and balanced
        and s < 4
        and h < 4
        and d < 5
        and c < 5
    ):
        return "2H"

    # =====================================
    # RULE 7
    # Transfer Diamond
    #
    # 6-10 D6+
    # 11-12 D5+
    # 0-5 D7+
    # =====================================

    if (
        6 <= hcp <= 10
        and d >= 6
        and s < 4
        and h < 4
    ):
        return "2C"

    if (
        11 <= hcp <= 12
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "2C"

    if (
        0 <= hcp <= 5
        and d >= 7
        and s < 4
        and h < 4
    ):
        return "2C"

    # =====================================
    # RULE 8
    # 6-10 m55
    # =====================================

    if (
        6 <= hcp <= 10
        and d >= 5
        and c >= 5
    ):
        return "2S"

    # =====================================
    # RULE 9
    # 0-5 C6+
    # =====================================

    if (
        0 <= hcp <= 5
        and c >= 6
    ):
        return "2N"

    # =====================================
    # RULE 10
    # 6-10 C6+
    # =====================================

    if (
        6 <= hcp <= 10
        and c >= 6
    ):
        return "3C"

    # =====================================
    # RULE 11
    # 6-10
    # M<4
    # m<6
    # =====================================

    if (
        6 <= hcp <= 10
        and s < 4
        and h < 4
        and d < 6
        and c < 6
    ):
        return "1S"

    # =====================================
    # RULE 12
    # PASS
    # =====================================

    return "PASS"
