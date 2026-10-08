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

    if hcp >= 21:
        return "2C"

    return "PASS"


# ==========================================
# RESPONSE 1NT
# ==========================================

def response_1nt(hcp, shape):

    s,h,d,c = shape_lengths(shape)

    if hcp >= 9 and s >= 5 and h >= 5:
        return "3D"

    return "PASS"


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
