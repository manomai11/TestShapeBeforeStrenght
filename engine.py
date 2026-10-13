# ==========================================
# SHAPE BEFORE STRENGTH
# ENGINE V1 (CENTRALIZED DECISION + SHOW RULES)
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
    "4045", "0445", "3145", "1345", "2245"
}

# ==========================================
# HELPERS
# ==========================================

def shape_lengths(shape):
    return (int(shape[0]), int(shape[1]), int(shape[2]), int(shape[3]))

def is_balanced(shape):
    return shape in BALANCED_SHAPES

def has_short(shape):
    s, h, d, c = shape_lengths(shape)
    return s <= 1 or h <= 1 or d <= 1 or c <= 1

# ==========================================
# CENTRALIZED DECISION ENGINE (ใช้ร่วมกันทุกการเปิด)
# ==========================================

def evaluate_central_decision(opener_hcp, opener_shape, response_range_dict, current_bid_str):
    s, h, d, c = shape_lengths(opener_shape)
    balanced = is_balanced(opener_shape)
    response_str = str(current_bid_str or "").upper().strip()

    min_resp = response_range_dict.get("min", response_range_dict.get("p_min", 6))
    max_resp = response_range_dict.get("max", response_range_dict.get("p_max", 10))
    
    resp_s = response_range_dict.get("s_min", 0)
    resp_h = response_range_dict.get("h_min", 0)
    resp_d = response_range_dict.get("d_min", 0)
    resp_c = response_range_dict.get("c_min", 0)

    total_s = s + resp_s
    total_h = h + resp_h
    total_d = d + resp_d
    total_c = c + resp_c

    suit_lengths = [s, h, d, c]
    min_len = min(suit_lengths)
    dist_points = 0
    if min_len == 0: dist_points += 5
    elif min_len == 1: dist_points += 3
    elif min_len == 2: dist_points += 1

    opener_total = opener_hcp + dist_points
    min_total = opener_total + min_resp
    max_total = opener_total + max_resp
    
    nt_min = opener_hcp + min_resp
    nt_max = opener_hcp + max_resp

    SLAM_ZONE = 32
    GAME_ZONE_MIN = 25
    GAME_ZONE_MAX = 31

    def suit_rank(suit_char):
        return {"C": 1, "D": 2, "H": 3, "S": 4, "N": 5}.get(suit_char, 0)

    current_level = int(response_str[0]) if response_str and response_str[0].isdigit() else 1
    current_suit = response_str[1:] if len(response_str) > 1 else "C"
    current_score_val = current_level * 5 + suit_rank(current_suit)

    def get_cheapest_bid(target_suit):
        for lvl in [2, 3, 4, 5]:
            candidate = f"{lvl}{target_suit}"
            cand_val = lvl * 5 + suit_rank(target_suit)
            if cand_val > current_score_val:
                return candidate
        return f"3{target_suit}"

    # ตรวจสอบ Trump Fit (Major สำคัญกว่า Minor)
    fit_suit = None
    opener_trump_len = 0
    if total_s >= 8: 
        fit_suit = "S"
        opener_trump_len = s
    elif total_h >= 8: 
        fit_suit = "H"
        opener_trump_len = h

    # ----------------------------------------------------
    # 1. กรณีมี MAJOR FIT (>= 8 ใบ)
    # ----------------------------------------------------
    if fit_suit:
        if min_total >= SLAM_ZONE:
            return f"6{fit_suit}", f"Decision: Major Slam"
        if GAME_ZONE_MIN <= min_total <= GAME_ZONE_MAX:
            return f"4{fit_suit}", f"Decision: Major Game"
        
        # --- GAME TRY / INVITATION ZONE (L < 25 แต่ M >= 25) [รู้แล้วว่ามี M Fit] ---
        if min_total < GAME_ZONE_MIN and max_total >= GAME_ZONE_MIN:
            if fit_suit == "H" and (s <= 1 or d <= 1 or c <= 1) and opener_trump_len >= 6:
                short_suit = "S" if s <= 1 else ("D" if d <= 1 else "C")
                return "2N", f"Decision: Game Try (Short {short_suit}, Trump 6+)"
            
            if d <= 1 and opener_trump_len >= 6 and fit_suit != "D":
                return "3D", "Decision: Game Try (Short D, Trump 6+)"
            if c <= 1 and opener_trump_len >= 6 and fit_suit != "C":
                return "3C", "Decision: Game Try (Short C, Trump 6+)"
            
            ask_bid = f"3{fit_suit}" if fit_suit == "H" else "3S"
            return ask_bid, "Decision: Game Try Ask Honor & Min/Max (Low Priority)"
            
        if max_total < GAME_ZONE_MIN:
            cheapest = get_cheapest_bid(fit_suit)
            return cheapest, f"Decision: Major Fit 8+ below game, cheapest safe stop"
        return f"4{fit_suit}", f"Decision: Major Game"

    # ----------------------------------------------------
    # 2. กรณีมี MINOR FIT
    # ----------------------------------------------------
    minor_fit_suit = None
    if total_d >= 8: minor_fit_suit = "D"
    elif total_c >= 8: minor_fit_suit = "C"

    if minor_fit_suit:
        if min_total >= SLAM_ZONE: 
            return f"6{minor_fit_suit}", f"Decision: Minor Slam"
        if min_total >= 28 and dist_points > 12:
            return f"5{minor_fit_suit}", f"Decision: 5{minor_fit_suit} chosen over 3N"
        if GAME_ZONE_MIN <= min_total <= GAME_ZONE_MAX:
            if nt_min >= GAME_ZONE_MIN:
                return "3N", f"Decision: NT Game preferred over 5{minor_fit_suit}"
            return f"5{minor_fit_suit}", f"Decision: Minor Game 5{minor_fit_suit}"
        if min_total < GAME_ZONE_MIN and max_total >= GAME_ZONE_MIN:
            cheapest = get_cheapest_bid(minor_fit_suit)
            return cheapest, f"Decision: Minor Game Invite / Try"
        if max_total < GAME_ZONE_MIN:
            cheapest = get_cheapest_bid(minor_fit_suit)
            return cheapest, f"Decision: Minor Fit below game, lowest safe stop"

    # ----------------------------------------------------
    # 3. กรณีไม่มี FIT อะไรเลย
    # ----------------------------------------------------
    if nt_min >= SLAM_ZONE: return "6N", "Decision: NT Slam"
    if GAME_ZONE_MIN <= nt_min <= GAME_ZONE_MAX: return "3N", "Decision: NT Game"
    
    if min_total < GAME_ZONE_MIN and max_total >= GAME_ZONE_MIN:
        if balanced:
            return "2N", "Decision: Game Invite (Balanced, Max goes to game)"
        else:
            unbid_suit = "S" if s >= 4 else ("H" if h >= 4 else ("D" if d >= 4 else "C"))
            return get_cheapest_bid(unbid_suit), "Decision: New Suit Forcing / 4th Suit Game Force"
            
    if nt_max < GAME_ZONE_MIN:
        return "2N", f"Decision: No fit, park at 2NT"
    
    return "3N", f"Decision: Max reaches game, bid 3NT"
    
# ==========================================
# OPENING
# ==========================================

def opening_bid(hcp, shape):

    s,h,d,c = shape_lengths(shape)

    balanced = is_balanced(shape)

    # ----------------------------
    # 4 LEVEL PREEMPT
    # ----------------------------

    if 5 <= hcp <= 10:

        if s >= 8 and h <= 4 and d <= 4 and c <= 4:
            return "4S","มีแต้ม 5-10 และมีไพ่ Spade 8 ใบขึ้นไป (4 Level Preempt)"

        if h >= 8 and s <= 4 and d <= 4 and c <= 4:
            return "4H","มีแต้ม 5-10 และมีไพ่ Heart 8 ใบขึ้นไป (4 Level Preempt)"

        if d >= 8 and s <= 4 and h <= 4 and c <= 4:
            return "4D","มีแต้ม 5-10 และมีไพ่ Diamond 8 ใบขึ้นไป (4 Level Preempt)"

        if c >= 8 and s <= 4 and h <= 4 and d <= 4:
            return "4C","มีแต้ม 5-10 และมีไพ่ Club 8 ใบขึ้นไป (4 Level Preempt)"

    # ----------------------------
    # 3 LEVEL PREEMPT
    # ----------------------------

    if 5 <= hcp <= 10:

        if s == 7 and h <= 4 and d <= 4 and c <= 4:
            return "3S","มีแต้ม 5-10 และมีไพ่ Spade 7 ใบ (3 Level Preempt)"

        if h == 7 and s <= 4 and d <= 4 and c <= 4:
            return "3H","มีแต้ม 5-10 และมีไพ่ Heart 7 ใบ (3 Level Preempt)"

        if d == 7 and s <= 4 and h <= 4 and c <= 4:
            return "3D","มีแต้ม 5-10 และมีไพ่ Diamond 7 ใบ (3 Level Preempt)"

        if c == 7 and s <= 4 and h <= 4 and d <= 4:
            return "3C","มีแต้ม 5-10 และมีไพ่ Club 7 ใบ (3 Level Preempt)"

    # ----------------------------
    # 2NT
    # ----------------------------

    if balanced and 20 <= hcp <= 22:
        return "2N","20-22 Balanced"

    # ----------------------------
    # 2C
    # ----------------------------

    if hcp >= 21:
        return "2C","21+ any or 18+ playing tricks"

    # ----------------------------
    # STRONG M55
    # ----------------------------

    if 17 <= hcp <= 20:

        if s >= 5 and h >= 5:
            return "2D","Multi 17-20 M55"
    # ----------------------------
    # WEAK MAJOR
    # ----------------------------

    if 6 <= hcp <= 10:

        if s == 6 and h <= 4 and d <= 4 and c <= 4:
            return "2D","Multi weak 1M"
        if h == 6 and s <= 4 and d <= 4 and c <= 4:
            return "2D","Multi weak 1M"

    # ----------------------------
    # 2S
    # ----------------------------

    if (
        11 <= hcp <= 13
        and s == 6
        and h <= 4
        and d <= 4
        and c <= 4
    ):
        return "2S","11-13 S6"

    # ----------------------------
    # 2H
    # ----------------------------

    if (
        11 <= hcp <= 13
        and h == 6
        and s <= 4
        and d <= 4
        and c <= 4
    ):
        return "2H","11-13 H6"

    # ----------------------------
    # BALANCED
    # ----------------------------

    if balanced:

        if 17 <= hcp <= 19:

            if s >= 5:
                return "1S","11+ S5"

            if h >= 5:
                return "1H","11+ H5"

            return "1C","big NT 17-19 no M5 open 1C"

        if 14 <= hcp <= 16:
            return "1N","strong NT 14-16 open 1N"

        if 11 <= hcp <= 13:
            return "1C","weak NT 11-13 open 1C"

    # ----------------------------
    # MAJORS
    # ----------------------------

    if 11 <= hcp <= 20:

        if s >= 5 and h >= 5:

            if s >= h:
                return "1S","11+ S5"

            return "1H","11+ H5"

        if s >= 5:
            return "1S","11+ S5"

        if h >= 5:
            return "1H","11+ H5"

    # ----------------------------
    # 4441 FAMILY
    # ----------------------------

    if 11 <= hcp <= 20 and shape in ["1444", "4144", "4441"]:
        return "1D","11+ D4+ unbalanced"

    if 11 <= hcp <= 20 and shape == "4414":
        return "1C","11+ C4+ unbalanced"
    # ----------------------------
    # SPECIAL D4C5
    # ----------------------------

    if shape in SPECIAL_D4C5:

        if 11 <= hcp <= 15:
            return "1D","11+ D4+ unbalanced"

        if hcp >= 16:
            return "1C","11-15 D4C5 เปิด 1D เตรียมรีบิด 2C"

    # ----------------------------
    # LONGER MINOR
    # ----------------------------

    if 11 <= hcp <= 20:

        if c > d:
            return "1C","11+ C4+ unbalanced"

        return "1D","11+ D4+ unbalanced"

    return "PASS","0-10 no good bid"


# ==========================================
# RESPONSE 1NT
# ==========================================

def response_1nt(hcp, shape):

    s, h, d, c = shape_lengths(shape)

    # 3D
    if hcp >= 9 and s >= 5 and h >= 5:
        return "3D"," GF 9+ M55"

    # 10+ M5 oM=4
    if hcp >= 10:

        if s >= 5 and h == 4:
            return "2C","GF 10+ M5+ and oM4"

        if h >= 5 and s == 4:
            return "2C","GF 10+ M5+ and oM4"

    # 8-9 M55 / M5m5

    if 8 <= hcp <= 9:

        if s >= 5 and h >= 5:
            return "2C","Constructive 8-9 55 atleast 1M"

        if (
            (s >= 5 or h >= 5)
            and
            (d >= 5 or c >= 5)
        ):
            return "2C","Constructive 8-9 55 atleast 1M"

    # 9 M5-6

    if hcp == 9:

        if s >= 5:
            return "2C","GI 9 Hcp S5-6 ใบ"

        if h >= 5:
            return "2C","GI 9 Hcp S5-6 ใบ"

    # Texas S

    if (
        (10 <= hcp <= 12 and s >= 6)
        or
        (6 <= hcp <= 9 and s >= 7)
        or
        (0 <= hcp <= 5 and s >= 8)
    ):
        return "4D","Transfer Spade"

    # Texas H

    if (
        (10 <= hcp <= 12 and h >= 6)
        or
        (6 <= hcp <= 9 and h >= 7)
        or
        (0 <= hcp <= 5 and h >= 8)
    ):
        return "4C","Transfer Heart"

    # 3S

    if hcp >= 11 and shape in ["1345", "1354"]:
        return "3S","GF m54 with singleton S"
    # 3H

    if hcp >= 11 and shape in ["3145", "3154"]:
        return "3H","GF m54 with singleton H"

    # m55

    if d >= 5 and c >= 5:
        return "2D","m55"

    # 3NT

    if (
        10 <= hcp <= 12
        and max(s, h) < 3
        and max(d, c) >= 6
    ):
        return "3N","To Play"

    if (
        11 <= hcp <= 15
        and shape in ["2254", "2245"]
    ):
        return "3N","To Play"

    # Transfer S

    if (
        (0 <= hcp <= 8 and s >= 5 and s >= h)
        or
        (hcp >= 10 and s >= 5 and h < 4)
    ):
        return "2H","Transfer S weak or GF"

    # Transfer H

    if (
        (0 <= hcp <= 8 and h >= 5 and h > s)
        or
        (hcp >= 10 and h >= 5 and s < 4)
    ):
        return "2D","Transfer H weak or GF"
    
    # 3C

    if 13 <= hcp <= 15 and (s >= 3 or h >= 3) and min(d, c) < 6:
        return "3C","ASk M with no M5 not interest slam"

    elif 11 <= hcp <= 12 and (s >= 3 or h >= 3) and min(d, c) < 7:
        return "3C","ASk M with no M5 not interest slam"

    elif hcp == 10 and (s >= 3 or h >= 3) and min(d, c) == 6:
        return "3C","ASk M with no M5 not interest slam"

    # D route

    if (
        (0 <= hcp <= 9 and d >= 6)
        or
        (13 <= hcp and d >= 6)
        or
        (10 <= hcp <= 12 and d >= 7)
    ):
        return "2N","Transfer D6+"

    # C route

    if (
        (0 <= hcp <= 9 and c >= 6)
        or
        (13 <= hcp and c >= 6)
        or
        (10 <= hcp <= 12 and c >= 7)
    ):
        return "2S","Transfer C"
    
    # 16+

    if (
        hcp >= 16
        and s < 5
        and h < 5
        and d < 6
        and c < 6
        and not (d >= 5 and c >= 5)
    ):
        return "2C","16+ M<5"

    # 10

    if (
        hcp == 10
        and s < 5
        and h < 5
        and d < 6
        and c < 6
        and not (d >= 5 and c >= 5)
    ):
        return "2C","Game invited"

    return "PASS","no good bid"

# ==========================================
# RESPONSE 1 MAJOR
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

    # =====================================
    # SUPPORT 4+
    # =====================================

    if trump >= 4:

        # Rule 1
        # 13+ M4+ with any void

        if hcp >= 13 and has_void:
            return "3D","GF 13+ M4+ with any void"

        # Rule 2
        # 13+ M4+ with other major singleton

        if hcp >= 13 and other_major == 1:

            if opening == "1H":
                return "3S","GF 13+ H4+ singletom S"
            else:
                return "3H","GF 13+ S4+ singletom H"

        # Rule 3
        # 13+ M4+ C=1

        if hcp >= 13 and c == 1:
            return "3N","GF 13+ singleton C"

        # Rule 4
        # 13+ M4+ D=1

        if hcp >= 13 and d == 1:
            return "4C","GF 13+ singleton D"

        # Rule 6
        # 13+ catch-all GF

        if hcp >= 13:
            return "2C","GF RELAY"

        # Rule 7
        # 10-12 M4+ any short

        if (
            10 <= hcp <= 12
            and has_short
        ):
            return "2N","Game Invite M4+ with any short"

        # Rule 8
        # 8-12 M4+ no short

        if (
            8 <= hcp <= 12
            and not has_short
        ):
            return "3C","Game Invite M4+ with no short"

        # Rule 9
        # 6-9 M5+

        if (
            6 <= hcp <= 9
            and trump >= 5
        ):
            return ("4H" if opening == "1H" else "4S"),"Non Force M4+"

        # Rule 10
        # 6-9 M4+ with short

        if (
            6 <= hcp <= 9
            and has_short
        ):
            return ("4H" if opening == "1H" else "4S"),"Non Force M4+ "

        # Rule 11
        # 4-7 M4 not 4333 and has Ace

        if (
            4 <= hcp <= 7
            and shape != "4333"
            and has_ace
        ):
            return ("3H" if opening == "1H" else "3S"),"Blocking M4+ 4-7 hcp  ถ้ามี4-5แต้มต้องมีเอ"

        # Rule 12
        # 0-5 M4 not 4333

        if (
            0 <= hcp <= 5
                and shape != "4333"
        ):
            return "3D","weak raise M4+"

        # special 4333 case

        if shape == "4333":

            if hcp >= 5:
                return ("2H" if opening == "1H" else "2S"),"constructive raised"

            return "PASS","no good bid"

    # =====================================
    # SUPPORT EXACTLY 3
    # =====================================

    if trump == 3:

        # Rule 5
        # 13+ M3 with any short

        if hcp >= 13:

            if has_short:

                if opening == "1H":
                    return "2D","GF 13+ M3 with any short"
                else:
                    return "2H","GF 13+ M3 with any short"

            return "2C","GF RELAY"

        # GI

        if 10 <= hcp <= 12:

            if opening == "1H":
                return "2D","Game invited H3"
            else:
                return "2H","Game invited S3"

        # constructive

        if 6 <= hcp <= 9:

            if opening == "1H":
                return "2H","constructive raised"
            else:
                return "2S","constructive raised"

        return "PASS","no good bid"

    # =====================================
    # OPEN 1S
    # =====================================

    if opening == "1S":

        # Rule 14

        if (
            6 <= hcp <= 10
            and h >= 6
            and s < 3
        ):
            return "2D","Transfer H"

        # Rule 15

        if (
            11 <= hcp <= 12
            and h >= 5
            and s < 4
        ):
            return "2D","Transfer H"

        if hcp >= 13:
            return "2C","GF RELAY"

        if 6 <= hcp <= 12:
            return "1N","1N Forcing"

        return "PASS","no good bid"

    # =====================================
    # OPEN 1H
    # =====================================

    else:

        # Rule 18

        if (
            6 <= hcp <= 9
            and s == 6
            and h < 2
        ):
            return "2S","6-9 S6"

        if hcp >= 13:
            return "2C","GF RELAY"

        # Rule 19

        if (
            0 <= hcp <= 9
            and s >= 5
            and h < 3
        ):
            return "1N","6-12 S5+"

        # Rule 20

        if (
            10 <= hcp <= 11
            and s >= 5
            and h < 4
        ):
            return "1N","6-12 S5+"

        # Rule 21

        if 6 <= hcp <= 12:
            return "1S","S<5 1RF"

        # Rule 22

        return "PASS","no good bid"

# ==========================================
# RESPONSE 1 DIAMOND
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

    if hcp >= 13 and s < 3 and h < 3:
        return "1N","GF RELAY"

    if (
        hcp >= 13
        and balanced
        and not bad_suit
        and (s == 4 or h == 4)
    ):
        return "1N","GF RELAY"

    if (
        10 <= hcp <= 12
        and s < 4
        and h < 4
        and c >= 5
        and c > d
    ):
        return "2S","Game invited C5+ C>D"

    if (
        10 <= hcp <= 12
        and s < 4
        and h < 4
        and d >= 4
        and d >= c
    ):
        return "3C","Game invited D4+ unbalanced"

    if (
        11 <= hcp <= 12
        and balanced
        and s < 4
        and h < 4
    ):
        return "2H","11-12 Balanced"

    if (
        6 <= hcp <= 10
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "3D","6-9 D5+ or D4 unbalanced"

    if (
        6 <= hcp <= 9
        and d == 4
        and s < 4
        and h < 4
        and (s <= 1 or h <= 1)
    ):
        return "3D","6-9 D5+ or D4 unbalanced"

    if (
        hcp == 10
        and shape == "3325"
    ):
        return "2C","NF C5+"

    if (
        6 <= hcp <= 9
        and c >= 6
        and d < 4
        and s < 4
        and h < 4
    ):
        return "2C","NF C5+"

    if (
        6 <= hcp <= 10
        and d == 3
        and s < 4
        and h < 4
    ):
        return "2D","constructive D3-4"

    if (
        0 <= hcp <= 5
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "2N","weak raised"

    if (
        hcp >= 6
        and s >= 4
        and s >= h
        and not (s == 4 and h == 4)
    ):
        return "1S","S4+"

    if (
        0 <= hcp <= 5
        and s >= 4
        and d >= 4
        and s >= h
        and not (s == 4 and h == 4)
    ):
        return "1S","S4+"

    if (
        hcp >= 6
        and h >= 4
        and h > s
    ):
        return "1H","H4+"

    if (
        0 <= hcp <= 5
        and h >= 4
        and d >= 4
        and h > s
    ):
        return "1H","H4+"

    return "PASS","no good bid"
    
# ==========================================
# RESPONSE 1 CLUB
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

    # Rule 1
    # 13+ M<4

    if (
        hcp >= 13
        and s < 4
        and h < 4
    ):
        return "1N","GF RELAY"

    # Rule 2
    # 13+ M=4 Balanced No Bad Suit

    if (
        hcp >= 13
        and balanced
        and not bad_suit
        and (s == 4 or h == 4)
    ):
        return "1N","GF RELAY"

    # Rule 3
    # H4+ 44 หรือ H>S

    if (
        h >= 4
        and (
            (h == 4 and s == 4)
            or
            h > s
        )
    ):
        return "1D","Transfer H4+"

    # Rule 4
    # S4+ S>=H ยกเว้น 44

    if (
        s >= 4
        and not (s == 4 and h == 4)
        and s >= h
    ):
        return "1H","Transfer S4+"

    # Rule 5
    # 11-12 C=5

    if (
        11 <= hcp <= 12
        and c == 5
    ):
        return "2D","11-12 C5+"

    # Rule 6
    # 11-12 Balanced M<4 m<5

    if (
        11 <= hcp <= 12
        and balanced
        and s < 4
        and h < 4
        and d < 5
        and c < 5
    ):
        return "2H","11-12 Balanced no m5"

    # Rule 7
    # Transfer Diamond

    if (
        6 <= hcp <= 10
        and d >= 6
        and s < 4
        and h < 4
    ):
        return "2C","Transfer D"

    if (
        11 <= hcp <= 12
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "2C","Transfer D"

    if (
        0 <= hcp <= 5
        and d >= 7
        and s < 4
        and h < 4
    ):
        return "2C","Transfer D"

    # Rule 8
    # 6-10 m55

    if (
        6 <= hcp <= 10
        and d >= 5
        and c >= 5
    ):
        return "2S","6-10 m55"

    # Rule 9
    # 0-5 C6+

    if (
        0 <= hcp <= 5
        and c >= 6
    ):
        return "2N","weak raised"

    # Rule 10
    # 6-10 C6+

    if (
        6 <= hcp <= 10
        and c >= 6
    ):
        return "3C","blocking raised"

    # Rule 11
    # 6-10 M<4 m<6

    if (
        6 <= hcp <= 10
        and s < 4
        and h < 4
        and d < 6
        and c < 6
    ):
        return "1S","6-10 M<4 m<5"

    # Rule 12

    return "PASS","no good bid"
    
# ==========================================
# BRIDGE EXACT TABLE DATABASE (Strict Matching)
# ==========================================

EXACT_BRIDGE_TABLE = [
    # --- กลุ่ม Decision ---
    {"bid": "1C-3C", "status": "decision", "p_min": 6, "p_max": 10, "s_min": 0, "s_max": 3, "h_min": 0, "h_max": 3, "d_min": 0, "d_max": 3, "c_min": 6, "c_max": 11},
    {"bid": "1C-2N", "status": "decision", "p_min": 0, "p_max": 5, "s_min": 0, "s_max": 3, "h_min": 0, "h_max": 3, "d_min": 0, "d_max": 3, "c_min": 6, "c_max": 11},
    {"bid": "1C-2S", "status": "decision", "p_min": 6, "p_max": 10, "s_min": 0, "s_max": 3, "h_min": 0, "h_max": 3, "d_min": 5, "d_max": 8, "c_min": 5, "c_max": 8},
    {"bid": "1C-2D", "status": "decision", "p_min": 11, "p_max": 12, "s_min": 0, "s_max": 3, "h_min": 0, "h_max": 3, "d_min": 0, "d_max": 4, "c_min": 5, "c_max": 11},
    {"bid": "1C-2C", "priority": 500, "status": "decision", "p_min": 6, "p_max": 10, "s_min": 0, "s_max": 3, "h_min": 0, "h_max": 3, "d_min": 6, "d_max": 13, "c_min": 0, "c_max": 4},
    {"bid": "1C-2C", "priority": 400, "status": "decision", "p_min": 11, "p_max": 12, "s_min": 0, "s_max": 3, "h_min": 0, "h_max": 3, "d_min": 5, "d_max": 13, "c_min": 0, "c_max": 5},
    {"bid": "1C-2H", "status": "decision", "p_min": 11, "p_max": 12, "s_min": 2, "s_max": 3, "h_min": 2, "h_max": 3, "d_min": 3, "d_max": 4, "c_min": 3, "c_max": 4},
]

# ฟังก์ชันดึงช่วงแต้มจากตาราง
def get_response_range(response_str):
    for row in EXACT_BRIDGE_TABLE:
        if row.get("bid") == f"1C-{response_str}" or row.get("bid") == response_str:
            if "p_min" in row and "p_max" in row:
                # ส่งค่าทั้งหมดใน row กลับไปเลย เพื่อให้ดึง s_min, c_min ได้ครบ
                return row 
    return {"p_min": 6, "p_max": 10, "s_min": 0, "h_min": 0, "d_min": 0, "c_min": 0}

# ==========================================
# OPENER REBID AFTER 1C (SHOW RULES + CENTRAL DECISION)
# ==========================================

def opener_rebid_1c(response, hcp, shape, extra_info=None):
    if extra_info is None:
        extra_info = {}
    
    s, h, d, c = shape_lengths(shape)
    balanced = is_balanced(shape)
    response_str = str(response or "").upper().strip()

    # ดึงข้อมูลจากตาราง EXACT_BRIDGE_TABLE (ถ้ามีตรงกับเคส Decision)
    row = get_response_range(response_str) # ฟังก์ชันนี้คืนค่า row ทั้งก้อนตามที่เราแก้ไปก่อนหน้านี้
    
    # เช็คว่าเป็นสถานะ Decision หรือไม่ (ถ้า row มี key status เป็น decision)
    if isinstance(row, dict) and row.get("status") == "decision":
        return evaluate_central_decision(hcp, shape, row, response_str)

    # ----------------------------------------------------
    # 1. GROUP SHOW: 1C - 1D
    # ----------------------------------------------------
    if response_str == "1D":
        if 17 <= hcp <= 19 and balanced and h == 4:
            return "2N", "2N FIT 16+ H4 Balanced"
        if 16 <= hcp <= 20 and not balanced and h >= 4:
            return "2S", "Power Fit 16+ H4 unbalanced"
        if 16 <= hcp <= 20 and not balanced and h == 3:
            return "2D", "Turbo Fit 16+ H3"
        if 16 <= hcp <= 20 and h < 4:
            return "1N", "1N no fit 16+ H<4"
        if 14 <= hcp <= 15 and h == 4:
            return "2H", "Medium Fit 14-15 H4"
        if 14 <= hcp <= 15 and h < 3 and c >= 6:
            return "3C", "Medium Fit 14-15 C6"
        if balanced or (11 <= hcp <= 13 and h == 4):
            return "1H", "weak NT or H4"
        if 11 <= hcp <= 15 and s == 4 and not balanced:
            return "1S", "minimum 11-15 S4 unbalanced"
        if 11 <= hcp <= 15 and c >= 6:
            return "2C", "minimum 11-15 C6"
        return "1H", "weak NT or H4"

    # ----------------------------------------------------
    # 2. GROUP SHOW: 1C - 1H
    # ----------------------------------------------------
    elif response_str == "1H":
        if 17 <= hcp <= 19 and balanced and s == 4:
            return "2N", "2N FIT 16+ S4 Balanced"
        if 16 <= hcp <= 20 and not balanced and s >= 4:
            return "2H", "Power Fit 16+ S4 unbalanced"
        if 16 <= hcp <= 20 and not balanced and s == 3:
            return "2D", "Turbo Fit 16+ S3"
        if 16 <= hcp <= 20 and s < 4:
            return "1N", "1N no fit 16+ S<4"
        if 14 <= hcp <= 15 and s == 4:
            return "2S", "Medium Fit 14-15 S4"
        if 14 <= hcp <= 15 and s < 3 and c >= 6:
            return "3C", "Medium Fit 14-15 good C6"
        if balanced or (11 <= hcp <= 13 and s == 4):
            return "1S", "weak NT or S4"
        if 11 <= hcp <= 15 and c >= 5:
            return "2C", "minimum 11-15 C5"
        return "1S", "weak NT or S4"
        
    # ----------------------------------------------------
    # CASE: 1C - 1S
    # ----------------------------------------------------

    elif response_str == "1S":
        if 11 <= hcp <= 13 and s >= 5:
            return "PASS", "Minimum S5"
        if (17 <= hcp <= 19 and balanced) or (hcp >= 16 and d >= 4):
            return "2D", "Big NT or 16+ D4"
        if hcp >= 16 and s >= 4:
            return "2S", "16+ SH4"
        if hcp >= 16 and h >= 4:
            return "2H", "16+ H4"
        if 14 <= hcp <= 15 and c >= 6 and s < 4 and h < 4 and c_honors >= 2:
            return "3C", "Medium 14-15 C6"
        if 11 <= hcp <= 15 and c >= 5:
            return "2C", "Minimum 11-15 C5+"
        if balanced or shape == "4414":
            return "1N", "weak NT or 4414"
    # ----------------------------------------------------
    # 3. GROUP SHOW: 1C - 1N
    # ----------------------------------------------------
    elif response_str == "1N":
        if 17 <= hcp <= 19 and balanced:
            return "2C", "Big NT"
        if 11 <= hcp <= 13 and balanced:
            return "2C", "weak NT"
        if 11 <= hcp <= 20 and shape == "4414":
            return "2C", "4-4-1-4"
        if h >= 4:
            return "2D", "Transfer H [C5H4]"
        if s >= 4:
            return "2H", "Transfer S [C5S4]"
        if c >= 6:
            return "2S", "Transfer C [C6]"
        if d >= 4 and s <= 1:
            return "2N", "Transfer D [1345]"
        if d >= 4 and h <= 1:
            return "3C", "Transfer D [3145]"
        if d >= 4:
            return "3D", "Transfer D [2245]"
        return "PASS", "no good bid for 1C-1N"

        
# ==========================================
# BRIDGE EXACT TABLE DATABASE (1D REBID)
# ==========================================

EXACT_BRIDGE_TABLE_1D = [
    # --- กลุ่ม Decision ---
    {"bid": "1D-3D", "status": "decision", "priority": 500, "type_hand": "not Balanced", "p_min": 6, "p_max": 9, "s_min": 0, "s_max": 3, "h_min": 0, "h_max": 3, "d_min": 4, "d_max": 9, "c_min": 0, "c_max": 5},
    {"bid": "1D-2S", "status": "decision", "type_hand": "not Balanced", "p_min": 10, "p_max": 12, "s_min": 0, "s_max": 2, "h_min": 0, "h_max": 3, "d_min": 0, "d_max": 3, "c_min": 5, "c_max": 6, "special": 13}, # C>D
    {"bid": "1D-3C", "status": "decision", "type_hand": "not Balanced", "p_min": 10, "p_max": 12, "s_min": 0, "s_max": 2, "h_min": 0, "h_max": 3, "d_min": 0, "d_max": 3, "c_min": 5, "c_max": 9},
    {"bid": "1D-2N", "status": "decision", "p_min": 0, "p_max": 5, "s_min": 0, "s_max": 5, "h_min": 0, "h_max": 3, "d_min": 0, "d_max": 3, "c_min": 5, "c_max": 9},
    {"bid": "1D-2H", "status": "decision", "p_min": 11, "p_max": 12, "s_min": 2, "s_max": 1, "h_min": 2, "h_max": 3, "d_min": 2, "d_max": 3, "c_min": 2, "c_max": 5},
    {"bid": "1D-2D", "status": "decision", "type_hand": "Balanced", "p_min": 6, "p_max": 10, "s_min": 2, "s_max": 4, "h_min": 2, "h_max": 3, "d_min": 3, "d_max": 3, "c_min": 2, "c_min_max": 5},
    {"bid": "1D-2C", "status": "decision", "priority": 600, "type_hand": "Balanced", "p_min": 6, "p_max": 10, "s_min": 3, "s_max": 4, "h_min": 3, "h_max": 3, "d_min": 2, "d_max": 3, "c_min": 2, "c_max": 5},
    {"bid": "1D-2C", "status": "decision", "priority": 500, "p_min": 6, "p_max": 10, "s_min": 0, "s_max": 4, "h_min": 0, "h_max": 3, "d_min": 3, "d_max": 3, "c_min": 6, "c_max": 6},

def get_table_row_1d(response_str, prefix="1D"):
    key = f"{prefix}-{response_str}".upper()
    matching_rows = [r for r in EXACT_BRIDGE_TABLE_1D if r.get("bid").upper() == key]
    if not matching_rows:
        return None
    # เรียงตาม priority สูงสุดก่อน
    matching_rows.sort(key=lambda x: x.get("priority", 0), reverse=True)
    return matching_rows[0]

# ==========================================
# OPENER REBID AFTER 1D (SHOW RULES + CENTRAL DECISION)
# ==========================================

def opener_rebid_1d(response, hcp, shape, extra_info=None):
    if extra_info is None:
        extra_info = {}
    
    s, h, d, c = shape_lengths(shape)
    balanced = is_balanced(shape)
    response_str = str(response or "").upper().strip()
    
    # ดึงข้อมูลจากตาราง 1D
    row = get_table_row_1d(response_str, "1D")
    if not row:
        return "PASS", "no matching rule for 1D rebid"

    status = row.get("status", "show")

    # ==========================================
    # 1. โซน DECISION -> ส่งให้ฟังก์ชันกลางคำนวณอัตโนมัติ
    # ==========================================
    if status == "decision":
        return evaluate_central_decision(hcp, shape, row, response_str)

    # ==========================================
    # 2. โซน SHOW -> ใช้ Rule ตามตารางที่คุณออกแบบ
    # ==========================================
    d_honors = extra_info.get("d_honors", 0) # จำนวนตัว A, K, Q ในชุด D
    
    if response_str == "1H":
        # Rule 1: 1D - 1H - 2N (16-20, 1444)
        if 16 <= hcp <= 20 and shape == "1444":
            return "2N", "2N FIT 16+ H4 1444"
        # Rule 2: 1D - 1H - 3C (16-20, 4441)
        if 16 <= hcp <= 20 and shape == "4441":
            return "3C", "2N FIT 16+ H4 4441"
        # Rule 3: 1D - 1H - 2S (16-20, H4 unbalanced)
        if hcp >= 16 and h >= 4 and not balanced:
            return "2S", "Power Fit 16+ H4 unbalanced"
        # Rule 4: 1D - 1H - 2D (16-20, H3)
        if hcp >= 16 and h == 3 and not balanced:
            return "2D", "Turbo Fit 16+ H3"
        # Rule 5: 1D - 1H - 1N (16-20, H<3) หรือ (11-15, S<4, H<4, D6+)ตามที่เพิ่มใหม่
        if hcp >= 16 and h < 3:
            return "1N", "1N no Fit 16+ H<3"
        if 11 <= hcp <= 15 and s < 4 and h < 4 and d >= 6 and c < 4:
            return "1N", "1N minimum 11-15 S<4 H<4 D6+"
        # Rule 6: 1D - 1H - 3H (14-15, H4)
        if 14 <= hcp <= 15 and h >= 4:
            return "3H", "Medium Fit 14-15 H4"
        # Rule 7: 1D - 1H - 3D (14-15, H<3, D6 good)
        if 14 <= hcp <= 15 and h < 3 and d >= 6 and d_honors >= 2:
            return "3D", "Medium 14-15 good D6"
        # Rule 8: 1D - 1H - 2H (11-13, H4)
        if 11 <= hcp <= 13 and h >= 4:
            return "2H", "minimum Fit 11-13 H4"
        # Rule 9: 1D - 1H - 1S (11-15, S4)
        if 11 <= hcp <= 15 and s >= 4:
            return "1S", "minimum 11-15 S4"
        # Rule 10: 1D - 1H - 2C (11-15, C4+)
        if 11 <= hcp <= 15 and c >= 4:
            return "2C", "minimum 11-15 2m"

    elif response_str == "1S":
        # Rule 1: 1D - 1S - 2N (16-20, 4144)
        if 16 <= hcp <= 20 and shape == "4144":
            return "2N", "2N FIT 16+ 4144"
        # Rule 2: 1D - 1S - 3C (16-20, 4441)
        if 16 <= hcp <= 20 and shape == "4441":
            return "3C", "2N FIT 16+ 4441"
        # Rule 3: 1D - 1S - 2H (16-20, S4 unbalanced)
        if hcp >= 16 and s >= 4 and not balanced:
            return "2H", "Power Fit 16+ S4 unbalanced"
        # Rule 4: 1D - 1S - 2D (16-20, S3)
        if hcp >= 16 and s == 3 and not balanced:
            return "2D", "Turbo Fit 16+ S3"
        # Rule 5: 1D - 1S - 1N (16-20, S<3, H<3) หรือเงื่อนไข 1N ช่วง 11-15 ตามที่เพิ่มใหม่
        if hcp >= 16 and s < 3 and h < 5 and c < 4:
            return "1N", "1N no Fit 16+ S<3"
        if 11 <= hcp <= 15 and s < 3 and h == 4 and d >= 5 and c < 4:
            return "1N", "1N minimum 11-15 S<3 H=4 D5+"
        if 11 <= hcp <= 15 and s < 3 and h < 4 and d >= 6:
            return "1N", "1N minimum 11-15 S<3 H<4 D6+"
        # Rule 6: 1D - 1S - 3S (14-15, S4)
        if 14 <= hcp <= 15 and s >= 4:
            return "3S", "Medium Fit 14-15 S4"
        # Rule 7: 1D - 1S - 3D (14-15, S<3, D6)
        if 14 <= hcp <= 15 and s < 3 and d >= 6 and d_honors >= 2:
            return "3D", "Medium 14-15 good D6"
        # Rule 8: 1D - 1S - 2S (11-13, S4)
        if 11 <= hcp <= 13 and s >= 4:
            return "2S", "minimum 11-13 S4"
        # Rule 9: 1D - 1S - 2C (11-15, C4)
        if 11 <= hcp <= 15 and c >= 4:
            return "2C", "minimum 11-15 C4"

    elif response_str == "1N":
        # Rule 1: 1D - 1N - 2C (any 4441 or balanced M>=4 or not balanced min 2m)
        if (shape in ["4441", "4144", "1444"]) or 11 <= hcp <= and d ==4 and c == 5:
            return "2C", "any 4441 or D4C5 "
        # Rule 2: 1D - 1N - 2D (D5 H4+)
        if d >= 5 and h >= 4:
            return "2D", "Transfer H [C5H4]"
        # Rule 3: 1D - 1N - 2H (D5 S4+)
        if d >= 5 and s >= 4:
            return "2H", "Transfer S [C5S4]"
        # Rule 4: 1D - 1N - 2S (C4+)
        if d >= 5 and c >= 4:
            return "2S", "Transfer C [C4]"
        # Rule 5: 1D - 1N - 2N (D6 with short)
        if d >= 6 and has_short(shape):
            return "2N", "Transfer D6 with short"
        # Rule 6: 1D - 1N - 3C (D6 no short)
        if d >= 6:
            return "3C", "Transfer D6 no short"

    return "PASS", f"No rule matched for show status: {response_str}"


    
# ==========================================
# OPENER REBID AFTER 1H 
# ==========================================

def opener_rebid_1h(response, hcp, shape, extra_info=None):
    """
    ฟังก์ชันคำนวณ Opener Rebid หลังจากเปิด 1H 
    ตามกฎที่คุณระบุเพิ่มเติมเข้ามา
    """
    if extra_info is None:
        extra_info = {}
    
    s, h, d, c = shape_lengths(shape)
    balanced = is_balanced(shape)
    has_short_suit = has_short(shape)
    
    # ----------------------------------------------------
    # CASE: 1H - 1S
    # ----------------------------------------------------
    if response == "1S":
        # Rule 1: 4H priority 1000 (13-15 H6+ m5 AKQ ของ 2 ชุดยาว ต้องมี 4+)
        if 13 <= hcp <= 15 and h >= 6 and (d >= 5 or c >= 5) and extra_info.get("akq_honors", 0) >= 1:
            return "4H", "H6m5 AKQ"
        # Rule 2: 4C priority 950 (13-15 C6+ AKQ ของ 2 ชุดยาว ต้องมี 4+)
        if 13 <= hcp <= 15 and c >= 6 and extra_info.get("akq_honors", 0) >= 1:
            return "4C", "C6H5 AKQ"
        # Rule 3: 4D priority 930 (13-15 D6+ AKQ ของ 2 ชุดยาว ต้องมี 4+)
        if 13 <= hcp <= 15 and d >= 6 and extra_info.get("akq_honors", 0) >= 1:
            return "4D", "D6H5 AKQ"
        # Rule 4: 3H priority 900 (11-15 H7)
        if 11 <= hcp <= 15 and h >= 7:
            return "3H", "minimum H7"
        # Rule 5: 3C priority 800 (15-17 C5+)
        if 15 <= hcp <= 17 and c >= 5:
            return "3C", "15-17 C5"
        # Rule 6: 3D priority 750 (15-17 D5+)
        if 15 <= hcp <= 17 and d >= 5:
            return "3D", "15-17 D5"
        # Rule 7: 2H priority 700 (14-16 H6+)
        if 14 <= hcp <= 16 and h >= 6:
            return "2H", "medium H6"
        # Rule 8: 2S priority 600 (11-15 S5) -> แก้ไขตามเงื่อนไข (min H6S5 หรือ S5)
        if 11 <= hcp <= 15 and s >= 5:
            return "2S", "minimum H6S5"
        # Rule 9: 2D priority 500 (11-15 S4+)
        if 11 <= hcp <= 15 and s >= 4:
            return "2D", "minimum S"
        # Rule 10: 2C priority 400 (11-15 C4+)
        if 11 <= hcp <= 15 and c >= 4:
            return "2C", "minimum C"
        # Rule 11: 1N priority 300 (11-15 D4+ or 16+ any)
        if (11 <= hcp <= 15 and d >= 4) or hcp >= 16:
            return "1N", "minimum D or Extra any"

    # ----------------------------------------------------
    # CASE: 1H - 1NT (1N)
    # ----------------------------------------------------
    elif response == "1N":
        # Rule 1: 4H priority 1000
        if 13 <= hcp <= 15 and h >= 6 and (d >= 5 or c >= 5):
            return "4H", "H6m5"
        # Rule 2: 4C priority 950
        if 13 <= hcp <= 15 and c >= 6:
            return "4C", "C6H5"
        # Rule 3: 4D priority 930
        if 13 <= hcp <= 15 and d >= 6:
            return "4D", "D6H5"
        # Rule 4: 3S priority 950 (14-15 S3+)
        if 14 <= hcp <= 15 and s >= 3:
            return "3S", "Medium S4"
        # Rule 4 (ซ้ำ): 3H priority 900 (11-15 H7 S<3)
        if 11 <= hcp <= 15 and h >= 7 and s < 3:
            return "3H", "minimum H7"
        # Rule 5: 3C priority 800 (15-17 C5+)
        if 15 <= hcp <= 17 and c >= 5:
            return "3C", "15-17 C5"
        # Rule 6: 3D priority 750 (15-17 D5+)
        if 15 <= hcp <= 17 and d >= 5:
            return "3D", "15-17 D5"
        # Rule 7: 2H priority 700 (14-16 H6+)
        if 14 <= hcp <= 16 and h >= 6:
            return "2H", "medium H6"
        # Rule 8: 2N priority 600 (16+ S3+)
        if hcp >= 16 and s >= 3:
            return "2N", "Extra S3+"
        # Rule 9: 2S priority 500 (11-13 S3+)
        if 11 <= hcp <= 13 and s >= 3:
            return "2S", "11-13 S3+"
        # Rule 10: 2D priority 400 (11-15 D4)
        if 11 <= hcp <= 15 and d == 4:
            return "2D", "minimum D4"
        # Rule 11: 2C priority 300 (ที่เหลือ)
        return "2C", "Minimum C4 or Extra"

    # ----------------------------------------------------
    # CASE: 1H - 2C
    # ----------------------------------------------------
    elif response == "2C":
        if h >= 6:
            return "2D", "Transfer H (H6+)"
        if s == 4:
            return "2H", "Transfer S"
        if c == 4:
            return "2S", "Transfer C"
        if d == 4 and s <= 1:
            return "2N", "Transfer Last suit with short Hi"
        if d == 4 and c <= 1:
            return "3C", "Transfer Last suit with short Lo"
        if d == 4:
            return "3D", "Transfer Last suit with no short"

    # ----------------------------------------------------
    # CASE: 1H - 2D
    # ----------------------------------------------------
    elif response == "2D":
        if hcp >= 11 and h >= 6 and s <= 1:
            return "2N", "Short suit game try (S)"
        if hcp >= 11 and h >= 6 and c <= 1:
            return "3C", "Short suit game try (C)"
        if hcp >= 11 and h >= 6 and d <= 1:
            return "3D", "Short suit game try (D)"
        if hcp >= 14:
            return "2S", "Ask min max + honor"
        return "2H", "minimum (no short)"

    # ----------------------------------------------------
    # CASE: 1H - 2H
    # ----------------------------------------------------
    elif response == "2H":
        if hcp >= 13 and h >= 6 and s <= 1:
            return "2N", "Short suit game try (S)"
        if hcp >= 13 and h >= 6 and c <= 1:
            return "3C", "Short suit game try (C)"
        if hcp >= 13 and h >= 6 and d <= 1:
            return "3D", "Short suit game try (D)"
        if hcp >= 16:
            return "2S", "Ask min max + honor"
        return "PASS", "minimum (no short)"

    # ----------------------------------------------------
    # CASE: 1H - 2S
    # ----------------------------------------------------
    elif response == "2S":
        if 11 <= hcp <= 15 and s == 4 and has_short_suit:
            return "4S", "minimum S4 good shape"
        if 14 <= hcp <= 15 and s == 3:
            return "3S", "Medium S3"
        if 13 <= hcp <= 15 and h >= 6 and (d >= 5 or c >= 5):
            return "4H", "H6m5"
        if 13 <= hcp <= 15 and c >= 6:
            return "4C", "C6H5"
        if 13 <= hcp <= 15 and d >= 6:
            return "4D", "D6H5"
        if 16 <= hcp <= 17 and h >= 6 and s < 2:
            return "3H", "16+"
        if 16 <= hcp <= 17 and d >= 4 and s < 2:
            return "3D", "16+ D4+ short"
        if 16 <= hcp <= 17 and c >= 4 and s < 2:
            return "3C", "16+ C4+ short S"
        if hcp >= 18 or (hcp >= 16 and s == 2):
            return "2N", "Asking"
        return "PASS", "minimum"

    # ----------------------------------------------------
    # CASE: 1H - 2N
    # ----------------------------------------------------
    elif response == "2N":
        if 13 <= hcp <= 15 and not has_short_suit:
            return "4H", "not interest slam 13-15 no short"
        if hcp >= 16 or (hcp >= 13 and has_short_suit):
            return "3C", "อาจไม่เกมถ้าสั้น C or good hand"
        if 11 <= hcp <= 12 and s <= 3 and extra_info.get("has_c_honor", False):
            return "3C", "อาจไม่เกมถ้าสั้น C"
        if 11 <= hcp <= 12 and s <= 3 and extra_info.get("has_s_honor", False):
            return "3H", "อาจไม่เกมถ้าสั้น S"
        if 11 <= hcp <= 12 and d <= 3 and extra_info.get("has_d_honor", False):
            return "3D", "อาจไม่เกมถ้าสั้น D"

    # ----------------------------------------------------
    # CASE: 1H - 3C
    # ----------------------------------------------------
    elif response == "3C":
        if has_short_suit:
            return "4H", "minimum with short"
        if hcp >= 16 and d <= 1:
            return "4C", "splinter Transfer"
        if hcp >= 16 and c <= 1:
            return "3N", "splinter Transfer"
        if hcp >= 16 and s <= 1:
            return "3S", "splinter S"
        if hcp >= 14 and not has_short_suit:
            return "3D", "สนใจเกมถ้า 10-12"
        if 11 <= hcp <= 13 and not has_short_suit:
            return "3H", "bad hand"

    # ----------------------------------------------------
    # CASE: 1H - 3D
    # ----------------------------------------------------
    elif response == "3D":
        # คำนวณสูตร Hand Evaluation ตามกฎ: Hcp + Singleton(3) + void(5) + (จำนวนH-5)*4 + second suit >= 22
        h_count = h
        computed_val = hcp + (3 if has_short_suit else 0) + ((h_count - 5) * 4 if h_count > 5 else 0)
        if computed_val >= 22:
            return "4H", "Formula >= 22"
        if hcp >= 17 and has_short_suit:
            return "3N", "17+ any short"
        return "3H", "waiting 0-5 ไม่เกม"

    # ----------------------------------------------------
    # CASE: 1H - 3H
    # ----------------------------------------------------
    elif response == "3H":
        if hcp >= 16 and not has_short_suit or hcp >= 14 and has_short_suit:
            return "4H", "ไพ่ที่คิดว่าเกมได้"
        if hcp >= 16 and d <= 1:
            return "4C", "splinter D"
        if hcp >= 16 and c <= 1:
            return "3N", "splinter C"
        if hcp >= 16 and s <= 1:
            return "3S", "splinter S"
        return "PASS", "ไพ่ที่คิดว่าไม่เกม ประมาณ 11-15 no short"

    # ----------------------------------------------------
    # CASE: 1H - 3S
    # ----------------------------------------------------
    elif response == "3S":
        if extra_info.get("has_black_honor", False):
            return "4H", "มี K/KJ/KQ/QJ ในชุดดำ"
        return "3N", "no K or Q ในชุดดำ or 15+"

    # ----------------------------------------------------
    # CASE: 1H - 3N
    # ----------------------------------------------------
    elif response == "3N":
        if extra_info.get("has_c_honor", False):
            return "4H", "มี K/KJ/KQ/QJ ในชุด C"
        return "3N", "no K or Q ในชุด C or 15+"

    # ----------------------------------------------------
    # CASE: 1H - 4C
    # ----------------------------------------------------
    elif response == "4C":
        if extra_info.get("has_d_honor", False):
            return "4H", "มี K/KJ/KQ/QJ ในชุด D"
        return "3N", "no K or Q ในชุด D or 15+"

    # ----------------------------------------------------
    # CASE: 1H - 4H
    # ----------------------------------------------------
    elif response == "4H":
        return "PASS", "ไม่น่าไปสแลมไหว"

    return "PASS", "no good bid for 1H rebid"
