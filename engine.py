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
            return "3S"

        if h == 7 and s <= 4 and d <= 4 and c <= 4:
            return "3H"

        if d == 7 and s <= 4 and h <= 4 and c <= 4:
            return "3D"

        if c == 7 and s <= 4 and h <= 4 and d <= 4:
            return "3C"

    # ----------------------------
    # 2NT
    # ----------------------------

    if balanced and 20 <= hcp <= 22:
        return "2N"

    # ----------------------------
    # 2C
    # ----------------------------

    if hcp >= 21:
        return "2C"

    # ----------------------------
    # STRONG M55
    # ----------------------------

    if 17 <= hcp <= 20:

        if s >= 5 and h >= 5:
            return "2D"
    # ----------------------------
    # WEAK MAJOR
    # ----------------------------

    if 6 <= hcp <= 10:

        if s == 6 and h <= 4 and d <= 4 and c <= 4:
            return "2D"
        if h == 6 and s <= 4 and d <= 4 and c <= 4:
            return "2D"

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
        return "2S"

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
        return "2H"

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
                return "1S"

            return "1H"

        if s >= 5:
            return "1S"

        if h >= 5:
            return "1H"

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
        return "3D"

    # 10+ M5 oM=4
    if hcp >= 10:

        if s >= 5 and h == 4:
            return "2C"

        if h >= 5 and s == 4:
            return "2C"

    # 8-9 M55 / M5m5,"Transfer H weak or GF or m55"

    if 8 <= hcp <= 9:

        if s >= 5 and h >= 5:
            return "2C"

        if (
            (s >= 5 or h >= 5)
            and
            (d >= 5 or c >= 5)
        ):
            return "2C"

    # 9 M5-6

    if hcp == 9:

        if s >= 5:
            return "2C"

        if h >= 5:
            return "2C"

    # Texas S

    if (
        (10 <= hcp <= 12 and s >= 6)
        or
        (6 <= hcp <= 9 and s >= 7)
        or
        (0 <= hcp <= 5 and s >= 8)
    ):
        return "4D"

    # Texas H

    if (
        (10 <= hcp <= 12 and h >= 6)
        or
        (6 <= hcp <= 9 and h >= 7)
        or
        (0 <= hcp <= 5 and h >= 8)
    ):
        return "4C"

    # 3S

    if hcp >= 11 and shape in ["1345", "1354"]:
        return "3S"
    # 3H

    if hcp >= 11 and shape in ["3145", "3154"]:
        return "3H"

    # m55

    if d >= 5 and c >= 5:
        return "2D"

    # D route

    if (
        (0 <= hcp <= 8 and d >= 6)
        or
        (13 <= hcp and d >= 6)
        or
        (9 <= hcp <= 12 and d >= 7)
    ):
        return "2N"

    # C route

    if (
        (0 <= hcp <= 8 and c >= 6)
        or
        (13 <= hcp and c >= 6)
        or
        (9 <= hcp <= 12 and c >= 7)
    ):
        return "2S"

    # 3NT

    if (
        9 <= hcp <= 12
        and max(s, h) < 3
        and max(d, c) >= 6
    ):
        return "3N"

    if (
        11 <= hcp <= 15
        and shape in ["2254", "2245"]
    ):
        return "3N"

    # 3C

    if (
        11 <= hcp <= 15
        and (s >= 3 or h >= 3)
    ):
        return "3C","GF Stayman not interest Slam"

    # Transfer S

    if (
        (0 <= hcp <= 8 and s >= 5 and s >= h)
        or
        (hcp >= 10 and s >= 5 and h < 4)
    ):
        return "2H"

    # Transfer H

    if (
        (0 <= hcp <= 8 and h >= 5 and h > s)
        or
        (hcp >= 10 and h >= 5 and s < 4)
    ):
        return "2D"
    # 16+

    if (
        hcp >= 16
        and s < 5
        and h < 5
        and d < 6
        and c < 6
        and not (d >= 5 and c >= 5)
    ):
        return "2C"

    # 10

    if (
        hcp == 10
        and s < 5
        and h < 5
        and d < 6
        and c < 6
        and not (d >= 5 and c >= 5)
    ):
        return "2C"

    return "PASS"

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
            return "3D"

        # Rule 2
        # 13+ M4+ with other major singleton

        if hcp >= 13 and other_major == 1:

            if opening == "1H":
                return "3S"
            else:
                return "3H"

        # Rule 3
        # 13+ M4+ C=1

        if hcp >= 13 and c == 1:
            return "3N"

        # Rule 4
        # 13+ M4+ D=1

        if hcp >= 13 and d == 1:
            return "4C"

        # Rule 6
        # 13+ catch-all GF

        if hcp >= 13:
            return "2C"

        # Rule 7
        # 10-12 M4+ any short

        if (
            10 <= hcp <= 12
            and has_short
        ):
            return "2N"

        # Rule 8
        # 8-12 M4+ no short

        if (
            8 <= hcp <= 12
            and not has_short
        ):
            return "3C"

        # Rule 9
        # 6-9 M5+

        if (
            6 <= hcp <= 9
            and trump >= 5
        ):
            return "4H" if opening == "1H" else "4S"

        # Rule 10
        # 6-9 M4+ with short

        if (
            6 <= hcp <= 9
            and has_short
        ):
            return "4H" if opening == "1H" else "4S"

        # Rule 11
        # 4-7 M4 not 4333 and has Ace

        if (
            4 <= hcp <= 7
            and shape != "4333"
            and has_ace
        ):
            return "3H" if opening == "1H" else "3S"

        # Rule 12
        # 0-5 M4 not 4333

        if (
            0 <= hcp <= 5
            and shape != "4333"
        ):
            return "3D"

        # special 4333 case

        if shape == "4333":

            if hcp >= 5:
                return "2H" if opening == "1H" else "2S"

            return "PASS"

    # =====================================
    # SUPPORT EXACTLY 3
    # =====================================

    if trump == 3:

        # Rule 5
        # 13+ M3 with any short

        if hcp >= 13:

            if has_short:

                if opening == "1H":
                    return "2D"
                else:
                    return "2H"

            return "2C"

        # GI

        if 10 <= hcp <= 12:

            if opening == "1H":
                return "2D"
            else:
                return "2H"

        # constructive

        if 6 <= hcp <= 9:

            if opening == "1H":
                return "2H"
            else:
                return "2S"

        return "PASS"

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
            return "2D"

        # Rule 15

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
            return "2S"

        if hcp >= 13:
            return "2C"

        # Rule 19

        if (
            0 <= hcp <= 9
            and s >= 5
            and h < 3
        ):
            return "1N"

        # Rule 20

        if (
            10 <= hcp <= 11
            and s >= 5
            and h < 4
        ):
            return "1N"

        # Rule 21

        if 6 <= hcp <= 12:
            return "1S"

        # Rule 22

        return "PASS"

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
        return "1N"

    if (
        hcp >= 13
        and balanced
        and not bad_suit
        and (s == 4 or h == 4)
    ):
        return "1N"

    if (
        10 <= hcp <= 12
        and s < 4
        and h < 4
        and c >= 5
        and c > d
    ):
        return "2S"

    if (
        10 <= hcp <= 12
        and s < 4
        and h < 4
        and d >= 4
        and d >= c
    ):
        return "3C"

    if (
        11 <= hcp <= 12
        and balanced
        and s < 4
        and h < 4
    ):
        return "2H"

    if (
        6 <= hcp <= 10
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "3D"

    if (
        6 <= hcp <= 9
        and d == 4
        and s < 4
        and h < 4
        and (s <= 1 or h <= 1)
    ):
        return "3D"

    if (
        hcp == 10
        and shape == "3325"
    ):
        return "2C"

    if (
        6 <= hcp <= 9
        and c >= 6
        and d < 4
        and s < 4
        and h < 4
    ):
        return "2C"

    if (
        6 <= hcp <= 10
        and d == 3
        and s < 4
        and h < 4
    ):
        return "2D"

    if (
        0 <= hcp <= 5
        and d >= 5
        and s < 4
        and h < 4
    ):
        return "2N"

    if (
        hcp >= 6
        and s >= 4
        and s >= h
        and not (s == 4 and h == 4)
    ):
        return "1S"

    if (
        0 <= hcp <= 5
        and s >= 4
        and d >= 4
        and s >= h
        and not (s == 4 and h == 4)
    ):
        return "1S"

    if (
        hcp >= 6
        and h >= 4
        and h > s
    ):
        return "1H"

    if (
        0 <= hcp <= 5
        and h >= 4
        and d >= 4
        and h > s
    ):
        return "1H"

    return "PASS"
    
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
        return "1N"

    # Rule 2
    # 13+ M=4 Balanced No Bad Suit

    if (
        hcp >= 13
        and balanced
        and not bad_suit
        and (s == 4 or h == 4)
    ):
        return "1N"

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
        return "1D"

    # Rule 4
    # S4+ S>=H ยกเว้น 44

    if (
        s >= 4
        and not (s == 4 and h == 4)
        and s >= h
    ):
        return "1H"

    # Rule 5
    # 11-12 C=5

    if (
        11 <= hcp <= 12
        and c == 5
    ):
        return "2D"

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
        return "2H"

    # Rule 7
    # Transfer Diamond

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

    # Rule 8
    # 6-10 m55

    if (
        6 <= hcp <= 10
        and d >= 5
        and c >= 5
    ):
        return "2S"

    # Rule 9
    # 0-5 C6+

    if (
        0 <= hcp <= 5
        and c >= 6
    ):
        return "2N"

    # Rule 10
    # 6-10 C6+

    if (
        6 <= hcp <= 10
        and c >= 6
    ):
        return "3C"

    # Rule 11
    # 6-10 M<4 m<6

    if (
        6 <= hcp <= 10
        and s < 4
        and h < 4
        and d < 6
        and c < 6
    ):
        return "1S"

    # Rule 12

    return "PASS"
