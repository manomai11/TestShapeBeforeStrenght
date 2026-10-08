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

def opening_bid(hcp, shape):

    s,h,d,c = shape_lengths(shape)

    balanced = is_balanced(shape)

    # ----------------------------
    # 4 level
    # ----------------------------

    if 5 <= hcp <= 10:

        if s >= 8 and h <= 4 and d <= 4 and c <= 4:
            return "4S"

        if h >= 8 and s <= 4 and d <= 4 and c <= 4:
            return "4H"

        if d >= 8 and s <= 4 and h <= 4 and c <= 4:
            return "4D"

        if c >= 8 and s <= 4 and h <= 4 and d <= 4:
            return "4C"

    # ----------------------------
    # 3 level
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
    # Strong M55
    # ----------------------------

    if 17 <= hcp <= 20:

        if s >= 5 and h >= 5:
            return "2D"

    # ----------------------------
    # Weak Major
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
    # Balanced
    # ----------------------------

    if balanced:

        if 17 <= hcp <= 19:

            if s >= 5:
                return "1S"

            if h >= 5:
                return "1H"

            return "1C"

        if 14 <= hcp <= 16:
            return "1N"

        if 11 <= hcp <= 13:
            return "1C"

    # ----------------------------
    # Majors
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
    # 4441 Family
    # ----------------------------

    if shape in ["1444","4144","4441"]:
        return "1D"

    if shape == "4414":
        return "1C"

    # ----------------------------
    # D4C5
    # ----------------------------

    if shape in SPECIAL_D4C5:

        if 11 <= hcp <= 15:
            return "1D"

        return "1C"

    # ----------------------------
    # Longer Minor
    # ----------------------------

    if 11 <= hcp <= 20:

        if c > d:
            return "1C"

        return "1D"

    return "PASS"


# ==========================================
# RESPONSE 1NT
# ==========================================

def response_1nt(hcp, shape):

    s,h,d,c = shape_lengths(shape)

    # rule 1
    if hcp >= 9 and s >= 5 and h >= 5:
        return "3D"

    # rule 2
    if hcp >= 10:

        if s >= 5 and h == 4:
            return "2C"

        if h >= 5 and s == 4:
            return "2C"

    # rule 3
    if 8 <= hcp <= 9:

        if s >= 5 and h >= 5:
            return "2C"

        if (
            (s >= 5 or h >= 5)
            and
            (d >= 5 or c >= 5)
        ):
            return "2C"

    # rule 4

    if hcp == 9:

        if s >= 5:
            return "2C"

        if h >= 5:
            return "2C"

    # rule 5

    if (
        (10 <= hcp <= 12 and s >= 6)
        or
        (6 <= hcp <= 9 and s >= 7)
        or
        (0 <= hcp <= 5 and s >= 8)
    ):
        return "4D"

    # rule 6

    if (
        (10 <= hcp <= 12 and h >= 6)
        or
        (6 <= hcp <= 9 and h >= 7)
        or
        (0 <= hcp <= 5 and h >= 8)
    ):
        return "4C"

    # rule 7

    if hcp >= 11 and shape in ["1345","1354"]:
        return "3S"

    # rule 8

    if hcp >= 11 and shape in ["3145","3154"]:
        return "3H"

    # rule 9

    if d >= 5 and c >= 5:
        return "2D"

    # rule 10

    if (
        (0 <= hcp <= 8 and d >= 6)
        or
        (13 <= hcp and d >= 6)
        or
        (9 <= hcp <= 12 and d >= 7)
    ):
        return "2N"

    # rule 11

    if (
        (0 <= hcp <= 8 and c >= 6)
        or
        (13 <= hcp and c >= 6)
        or
        (9 <= hcp <= 12 and c >= 7)
    ):
        return "2S"

    # rule 12

    if (
        9 <= hcp <= 12
        and max(s,h) < 3
        and max(d,c) >= 6
    ):
        return "3N"

    if (
        11 <= hcp <= 15
        and shape in ["2254","2245"]
    ):
        return "3N"

    # rule 13

    if (
        11 <= hcp <= 15
        and (s >= 3 or h >= 3)
    ):
        return "3C"

    # rule 14

    if (
        (0 <= hcp <= 8 and s >= 5 and s >= h)
        or
        (hcp >= 10 and s >= 5 and h < 4)
    ):
        return "2H"

    # rule 15

    if (
        (0 <= hcp <= 8 and h >= 5 and h > s)
        or
        (hcp >= 10 and h >= 5 and s < 4)
    ):
        return "2D"

    # rule 16

    if (
        hcp >= 16
        and s < 5
        and h < 5
        and d < 6
        and c < 6
        and not (d >= 5 and c >= 5)
    ):
        return "2C"

    # rule 17

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
# RESPONSE 1MAJOR
# ==========================================

def response_1major(*args, **kwargs):
    return "TBD"


# ==========================================
# RESPONSE 1D
# ==========================================

def response_1d(*args, **kwargs):
    return "TBD"


# ==========================================
# RESPONSE 1C
# ==========================================

def response_1c(*args, **kwargs):
    return "TBD"

# ==========================================
# PLACEHOLDERS
# ==========================================

def response_1major(*args, **kwargs):
    return "TBD"

def response_1d(*args, **kwargs):
    return "TBD"

def response_1c(*args, **kwargs):
    return "TBD"
