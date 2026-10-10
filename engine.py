# ==========================================
# SHAPE BEFORE STRENGTH
# ENGINE V1
# OPENING ONLY + 1NT
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
# OPENER REBID AFTER 1C
# ==========================================

def opener_rebid_1c(response, hcp, shape, extra_info=None):
    """
    extra_info สามารถส่งค่าเพิ่มเติมเข้ามาได้ เช่น:
    - c_honors: จำนวนตัว A, K, Q ในชุด Club (เช่นนับได้กี่ตัว)
    - opening_suit_lengths: ความยาวของไพ่แต่ละชุด
    """
    if extra_info is None:
        extra_info = {}
    
    s, h, d, c = shape_lengths(shape)
    balanced = is_balanced(shape)
    has_short_suit = has_short(shape)
    c_honors = extra_info.get("c_honors", 0) # จำนวน AKQ ในชุด C

    # ----------------------------------------------------
    # CASE: 1C - 1D
    # ----------------------------------------------------
    if response == "1D":
        # Rule 1: 17-19 Balanced H4 -> 2N (priority 1000)
        if 17 <= hcp <= 19 and balanced and h == 4:
            return "2N", "2NT Fit 17-19 Balanced H4"
        
        # Rule 2: Balanced H<4 -> 1N (priority ต่ำสุด/default ของกลุ่ม)
        if balanced and h < 4 and 16 <= hcp <= 20: # ปรับช่วงตามบริบท
            return "1N", "1NT no Fit 16+ H<4"

        # Rule 3: 16+ H<3 unbalanced -> 1N (priority 860)
        if 16 <= hcp <= 20 and not balanced and h < 3:
            return "1N", "1NT no Fit 16+ H<4"

        # Rule 4: 16+ H<3 C6+ -> 1N (priority 840)
        if 16 <= hcp <= 20 and h < 3 and c >= 6:
            return "1N", "1NT no Fit 16+ H<4"

        # Rule 5: 16+ H4+ unbalanced -> 2S (priority 700)
        if 16 <= hcp <= 20 and not balanced and h >= 4:
            return "2S", "Power Fit 16+ H4"

        # Rule 6: 16+ H=3 unbalanced -> 2D (priority 600)
        if 16 <= hcp <= 20 and not balanced and h == 3:
            return "2D", "Turbo Fit (2M-1)16+ H3"

        # Rule 7: 14-15 H4 have short -> 2H (priority 500)
        if 14 <= hcp <= 15 and h == 4 and has_short_suit:
            return "2H", "Medium 14-15 H4"

        # Rule 8: 14-15 H<3 อย่างน้อย AK AQ or KQ in C -> 3C (priority 400)
        if 14 <= hcp <= 15 and h < 3 and c_honors >= 2: # สมมติเช็ค honors จากตัวแปรเสริม
            return "3C", "Medium 14-15 C6"

        # Rule 9: Balanced หรือ 11-13 H3+ -> 1H (priority ต่ำสุด)
        if balanced or (11 <= hcp <= 13 and h >= 3):
            return "1H", "accept Transfer weak NT"

        # Rule 10: 11-15 S4 unbalanced -> 1S (priority 200)
        if 11 <= hcp <= 15 and s == 4 and not balanced:
            return "1S", "Minimum 11-15 S4 unbalanced"

        # Rule 11: 11-15 C6 -> 2C (priority 10)
        if 11 <= hcp <= 15 and c >= 6:
            return "2C", "Minimum 11-15 C6"

    # ----------------------------------------------------
    # CASE: 1C - 1H
    # ----------------------------------------------------
    elif response == "1H":
        # Rule 1: 17-19 Balanced S4 -> 2N (priority 1000)
        if 17 <= hcp <= 19 and balanced and s == 4:
            return "2N", "2NT Fit 17-19 Balanced S4"

        # Rule 2 & 3 & 4 (1N ต่างๆ)
        if (16 <= hcp <= 20) and (balanced and s < 4 or not balanced and s < 3):
            return "1N", "1NT no Fit 16+ S<4"

        # Rule 5: 16+ S4+ unbalanced -> 2D (priority 700)
        if 16 <= hcp <= 20 and not balanced and s >= 4:
            return "2D", "Power Fit 16+ S4"

        # Rule 6: 16+ S=3 unbalanced -> 2H (priority 600)
        if 16 <= hcp <= 20 and not balanced and s == 3:
            return "2H", "Turbo Fit (2M-1) 16+ S3"

        # Rule 7: 14-15 S4 have short -> 2S (priority 500)
        if 14 <= hcp <= 15 and s == 4 and has_short_suit:
            return "2S", "Medium 14-15 S4"

        # Rule 8: 14-15 S<3 C6+ (AKQ >= 2) -> 3C (priority 400)
        if 14 <= hcp <= 15 and s < 3 and c >= 6 and c_honors >= 2:
            return "3C", "Medium 14-15 C6"

        # Rule 9: Balanced หรือ 11-13 S3+ -> 1S
        if balanced or (11 <= hcp <= 13 and s >= 3):
            return "1S", "accept Transfer weak NT"

        # Rule 11: 11-15 C5+ -> 2C (priority 10)
        if 11 <= hcp <= 15 and c >= 5:
            return "2C", "Minimum 11-15 C5+"

    # ----------------------------------------------------
    # CASE: 1C - 1S
    # ----------------------------------------------------
    elif response == "1S":
        # Rule 1: 11-13 S5 -> Pass (priority 1100)
        if 11 <= hcp <= 13 and s >= 5:
            return "PASS", "Minimum S5"

        # Rule 2: 17-19 balanced หรือ 16+ D4 -> 2D (priority 1000)
        if (17 <= hcp <= 19 and balanced) or (hcp >= 16 and d >= 4):
            return "2D", "Big NT or 16+ D4"

        # Rule 3: 16+ S4 or second suit <4 S not bad suit -> 2S (priority 900)
        if hcp >= 16 and s >= 4:
            return "2S", "16+ SH4 or stop"

        # Rule 4: 16+ H4 or second suit <4 H not bad suit -> 2H (priority 800)
        if hcp >= 16 and h >= 4:
            return "2H", "16+ H4 or stop"

        # Rule 5: 14-15 C6+ M<4 (AKQ >= 2) -> 3C (priority 700)
        if 14 <= hcp <= 15 and c >= 6 and s < 4 and h < 4 and c_honors >= 2:
            return "3C", "Medium 14-15 C6"

        # Rule 6: 11-15 C5+ -> 2C (priority 600)
        if 11 <= hcp <= 15 and c >= 5:
            return "2C", "Minimum 11-15 C5+"

        # Rule 7: Weak NT หรือ 4414 -> 1N
        if balanced or shape == "4414":
            return "1N", "weak NT or 4414"

    # ----------------------------------------------------
    # CASE: 1C - 1NT (1N)
    # ----------------------------------------------------
    elif response == "1N":
        # Rule 1: Balanced หรือ 4414 -> 2C (priority 1000)
        if balanced or shape == "4414":
            return "2C", "Balanced or 4414"
        # Rule 2: unbalanced H4 -> 2D (priority 900)
        if not balanced and h == 4:
            return "2D", "unbalanced Transfer H"
        # Rule 3: unbalanced S4 -> 2H (priority 800)
        if not balanced and s == 4:
            return "2H", "unbalanced Transfer S"
        # Rule 4: unbalanced C4 -> 2S (priority 700)
        if not balanced and c == 4:
            return "2S", "unbalanced Transfer C"
        # Rule 5: unbalanced D4 short S -> 2N (priority 600)
        if not balanced and d == 4 and s <= 1:
            return "2N", "unbalanced D4 short S(Hi)"
        # Rule 6 & 7: unbalanced D4 short H / no short
        if not balanced and d == 4:
            if h <= 1:
                return "2D", "unbalanced D4 short H(Lo)"
            else:
                return "2D", "unbalanced D4 no short 2245"

    # ----------------------------------------------------
    # CASE: 1C - 2C
    # ----------------------------------------------------
    elif response == "2C":
        if balanced:
            return "2N", "BiG NT"
        if hcp >= 16:
            return "2H", "16+ Forcing"
        if 14 <= hcp <= 15 and c >= 6 and c_honors >= 2:
            return "3C", "Medium 14-15 C6"
        if 11 <= hcp <= 13 and c >= 6 and d == 0:
            return "PASS", "Minimum Long C"
        if 14 <= hcp <= 15:
            return "PASS", "Medium 14-15 C6"
        return "2D", "waiting"

    # ----------------------------------------------------
    # CASE: 1C - 2D
    # ----------------------------------------------------
    elif response == "2D":
        if balanced:
            return "2N", "BiG NT"
        if hcp >= 14:
            return "2H", "14+ GF"
        if (11 <= hcp <= 13 and c <= 2) or (hcp == 13 and c == 3):
            return "2S", "waiting"
        if 11 <= hcp <= 12 and c >= 3:
            return "3C", "To play"

    # ----------------------------------------------------
    # CASE: 1C - 2H
    # ----------------------------------------------------
    elif response == "2H":
        if 11 <= hcp <= 12 and h >= 5:
            return "PASS", "Minimum H5"
        if balanced or hcp >= 14:
            return "2S", "F bid 2N"
        if hcp == 13 and balanced:
            return "2N", "GI"
        if 11 <= hcp <= 12 and c >= 5:
            return "3C", "To play"

    # ----------------------------------------------------
    # CASE: 1C - 2S
    # ----------------------------------------------------
    elif response == "2S":
        if hcp >= 14:
            return "2N", "Asking"
        if 11 <= hcp <= 13 and c >= 3:
            return "3C", "Minimum"
        if 11 <= hcp <= 13 and d >= 3:
            return "3D", "Minimum"

    # ----------------------------------------------------
    # CASE: 1C - 2N
    # ----------------------------------------------------
    elif response == "2N":
        if hcp >= 14:
            return "3C", "Hmmm เซงเป็ด"

    # ----------------------------------------------------
    # CASE: 1C - 3C
    # ----------------------------------------------------
    elif response == "3C":
        if balanced:
            return "3N", "To Play"
        if hcp >= 16 and h <= 1:
            return "3H", "Cue bid"
        if hcp >= 16 and s <= 1:
            return "3S", "Cue bid"
        if hcp >= 16:
            return "3D", "waiting"
        return "PASS", "กำขี้ดีกว่ากำตด"

    return "PASS", "no good rebid"
