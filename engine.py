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
            return "2D","Multi 17-20 2M ตัวนี้เอาไว้ช่วยลดความหมายตอนเปิด 1M ไม่ให้สับสน"
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
        return "2S","11-13 S6 ตัวนี้ช่วยตอบปัญหาตอน 1S rebid 2S = 14-16 ทำให้ช่วงแต้มเคลียร์แต่จะไม่ได้เล่น weak 2 suit"

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
        return "2H","11-13 H6 ตัวนี้ช่วยตอบปัญหาตอน 1S rebid 2S = 14-16 ทำให้ช่วงแต้มเคลียร์แต่จะไม่ได้เล่น weak 2 suit"

    # ----------------------------
    # BALANCED
    # ----------------------------

    if balanced:

        if 17 <= hcp <= 19:

            if s >= 5:
                return "1S","11+ S5 "

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
            return "1D","11-15 D4C5 เปิด 1D เตรียมรีบิด 2C"

        if hcp >= 16:
            return "1C","16+ D4C5 เปิด 1C เตรียมรีบิด 1N or 2D[Turbo Fit]"

    # ----------------------------
    # LONGER MINOR
    # ----------------------------

    if 11 <= hcp <= 20:

        if c > d:
            return "1C","11+ C5+ unbalanced"

        return "1D","11+ D5+ unbalanced"

    return "PASS","0-10 no good bid"


# ==========================================
# RESPONSE 1NT
# ==========================================

def response_1nt(hcp, shape):

    s, h, d, c = shape_lengths(shape)

    # 3D
    if hcp >= 9 and s >= 5 and h >= 5:
        return "3D"," GF 9+ M55  <== ตัดปัญหา GF 2M จบในมี่เดียว"

    # 10+ M5 oM=4
    if hcp >= 10:

        if s >= 5 and h == 4:
            return "2C","GF 10+ M5+ and oM4 <== 2C จะแยกไพ่เกม 2M54/64 ใบออกจาก Transfer เพื่อลดภาระ 1N-3C ที่เกิดบ่อยกว่า ทำให้ซ่อนไพ่ได้ดีกว่า"

        if h >= 5 and s == 4:
            return "2C","GF 10+ M5+ and oM4 <== 2C จะแยกไพ่เกม 2M54/64 ใบออกจาก Transfer เพื่อลดภาระ 1N-3C ที่เกิดบ่อยกว่า ทำให้ซ่อนไพ่ได้ดีกว่า"

    # 8-9 M55 / M5m5

    if 8 <= hcp <= 9:

        if s >= 5 and h >= 5:
            return "2C","Constructive 8 hcp 2M <== เปิด14-16[15-17] ไพ่แนวนี้ควรแยกมาให้ชัดกัน over bid"

        if (
            (s >= 5 or h >= 5)
            and
            (d >= 5 or c >= 5)
        ):
            return "2C","Constructive 8-9 55 atleast 1M <== เปิด14-16[15-17] ไพ่แนวนี้ควรแยกมาให้ชัดกัน over bid"
    
    # m55

    if d >= 5 and c >= 5:
        return "2D","m55 <==  ซ่อนไว้กับ transfer H  เตรียมบอก 2S ในรีบิดต่อไป"

    # 9 M5-6

    if hcp == 9:

        if s >= 5:
            return "2C","GI 9 Hcp S5-6 ใบ <== 2C จะแยกไพ่ชวนเกม M5-6 ใบออกจาก Transfer  เพื่อลดการชวนเกมออกให้ชวนเกมที่ระดีล 2 ได้"

        if h >= 5:
            return "2C","GI 9 Hcp S5-6 ใบ <== 2C จะแยกไพ่ชวนเกม M5-6 ใบออกจาก Transfer  เพื่อลดการชวนเกมออกให้ชวนเกมที่ระดีล 2 ได้"

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
        return "3C","ASk M with no M5 not interest slam <==  ไพ่ 63 1.หา M5-3 2.อาจสร้างความไขว้เขวให้คนลีดได้"

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
        return "2C","16+ M<5 <= 2C Slam interest คัดไพ่ 1M or m6 or m55 มราไปจามทางของตัวเอง"

    # 10

    if (
        hcp == 10
        and s < 5
        and h < 5
        and d < 6
        and c < 6
        and not (d >= 5 and c >= 5)
    ):
        return "2C","Game invited <==  เล่นจริงใครอยากชวน 9 แต้มก็ตามใจแต่แนะนำว่าควรมี ชุด 5ใบ เพราะเราเริ่ม overvid แล้ว"

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
    if extra_info is None:
        extra_info = {}
    
    s, h, d, c = shape_lengths(shape)
    balanced = is_balanced(shape)
    has_short_suit = has_short(shape)
    c_honors = extra_info.get("c_honors", 0)

    if response == "1D":
        if 17 <= hcp <= 19 and balanced and h == 4:
            return "2N", "2NT Fit 17-19 Balanced H4"
        if balanced and h < 4 and 16 <= hcp <= 20:
            return "1N", "1NT no Fit 16+ H<4"
        if 16 <= hcp <= 20 and not balanced and h < 3:
            return "1N", "1NT no Fit 16+ H<4"
        if 16 <= hcp <= 20 and h < 3 and c >= 6:
            return "1N", "1NT no Fit 16+ H<4"
        if 16 <= hcp <= 20 and not balanced and h >= 4:
            return "2S", "Power Fit 16+ H4"
        if 16 <= hcp <= 20 and not balanced and h == 3:
            return "2D", "Turbo Fit 16+ H3"
        if 14 <= hcp <= 15 and h == 4:
            return "2H", "Medium 14-15 H4"
        if 14 <= hcp <= 15 and h < 3 and c_honors >= 2:
            return "3C", "Medium 14-15 good C6"
        if balanced or (11 <= hcp <= 13 and h == 4):
            return "1H", "accept Transfer weak NT or H4"
        if 11 <= hcp <= 15 and s == 4:
            return "1S", "Minimum 11-15 S4 unbalanced"
        if 11 <= hcp <= 15 and c >= 6:
            return "2C", "Minimum 11-15 C6"

    elif response == "1H":
        if 17 <= hcp <= 19 and balanced and s == 4:
            return "2N", "2NT Fit 17-19 Balanced S4"
        if (16 <= hcp <= 20) and (balanced and s < 4 or not balanced and s < 3):
            return "1N", "1NT no Fit 16+ S<4"
        if 16 <= hcp <= 20 and not balanced and s >= 4:
            return "2H", "Power Fit 16+ S4"
        if 16 <= hcp <= 20 and not balanced and s == 3:
            return "2D", "Turbo Fit 16+ S3"
        if 14 <= hcp <= 15 and s == 4:
            return "2S", "Medium 14-15 S4"
        if 14 <= hcp <= 15 and s < 3 and c >= 6 and c_honors >= 2:
            return "3C", "Medium 14-15 C6"
        if balanced or (11 <= hcp <= 13 and s == 3):
            return "1S", "accept Transfer weak NT or S4"
        if 11 <= hcp <= 15 and c >= 5:
            return "2C", "Minimum 11-15 C5+"

    elif response == "1S":
        if 11 <= hcp <= 13 and s >= 5:
            return "PASS", "Minimum S5"
        if (17 <= hcp <= 19 and balanced) or (hcp >= 16 and d >= 4):
            return "2D", "Big NT or 16+ D4"
        if hcp >= 16 and s >= 4:
            return "2S", "16+ SH4 or stop"
        if hcp >= 16 and h >= 4:
            return "2H", "16+ H4 or stop"
        if 14 <= hcp <= 15 and c >= 6 and s < 4 and h < 4 and c_honors >= 2:
            return "3C", "Medium 14-15 C6"
        if 11 <= hcp <= 15 and c >= 5:
            return "2C", "Minimum 11-15 C5+"
        if balanced or shape == "4414":
            return "1N", "weak NT or 4414"

    elif response == "1N":
        if balanced or shape == "4414":
            return "2C", "Balanced or 4414"
        if not balanced and h == 4:
            return "2D", "unbalanced Transfer H"
        if not balanced and s == 4:
            return "2H", "unbalanced Transfer S"
        if not balanced and c >= 6:
            return "2S", "unbalanced Transfer C"
        if not balanced and d == 4 and s <= 1:
            return "2N", "unbalanced D4 short S(Hi)"
        if not balanced and d == 4:
            if h <= 1:
                return "3C", "unbalanced D4 short H(Lo)"
            else:
                return "3D", "unbalanced D4 no short 2245"

    elif response == "2C":
        if 17 <= hcp <= 19 and balanced:
            return "2N", "BiG NT"
        if 14 <= hcp <= 15 and c >= 6 and c_honors >= 2:
            return "3C", "Medium 14-15 C6"
        if hcp >= 16:
            return "2H", "16+ Forcing"
        if 11 <= hcp <= 13 and c >= 6 and d == 0:
            return "PASS", "Minimum Long C"
        if 14 <= hcp <= 15:
            return "PASS", "Medium 14-15 C6"
        return "2D", "11-15 อดทนไว้"

    elif response == "2D":
        if 17 <= hcp <= 19 and balanced:
            return "2N", "BiG NT"
        if hcp >= 14:
            return "2H", "14+ GF"
        if (11 <= hcp <= 12 and c <= 2) or (hcp == 13 and c == 3):
            return "2S", "waiting"
        if 11 <= hcp <= 12 and c >= 3:
            return "3C", "To play"

    elif response == "2H":
        if 11 <= hcp <= 12 and h >= 5:
            return "PASS", "Minimum H5"
        if 11 <= hcp <= 12 and c >= 5:
            return "3C", "To play"
        if hcp == 13 and balanced:
            return "2N", "GI"            
        return "2S", "F bid 2N"

    elif response == "2S":
        if 11 <= hcp <= 13 and c >= 3:
            return "3C", "Minimum"
        if 11 <= hcp <= 13 and d >= 3:
            return "3D", "Minimum"
        return "2N", "Asking"

    elif response == "2N":
        if hcp >= 11:
            return "3C", "Hmmm เซงเป็ด"

    elif response == "3C":
        if 17 <= hcp <= 19 and balanced:
            return "3N", "Big NT To Play"
        if hcp >= 16 and h <= 1:
            return "3H", "Cue short"
        if hcp >= 16 and s <= 1:
            return "3S", "Cue short"
        if hcp >= 16:
            return "3D", "waiting"
        return ("PASS", "กำขี้ดีกว่ากำตด")
        
    return "PASS", "no good bid for 1c rebid"


# ==========================================
# OPENER REBID AFTER 1D
# ==========================================

def opener_rebid_1d(response, hcp, shape, extra_info=None):
    if extra_info is None:
        extra_info = {}
    
    s, h, d, c = shape_lengths(shape)
    balanced = is_balanced(shape)
    d_honors = extra_info.get("d_honors", 0)

    if response == "1H":
        if 16 <= hcp <= 20 and shape in ["4441", "1444"]:
            return "2N", "2N Fit 16+ 4441"
        if hcp >= 16 and h >= 4:
            return "2S", "Power Fit 16+ H4"
        if hcp >= 16 and h == 3:
            return "2D", "Turbo Fit 16+ H3"
        if hcp >= 16 and h < 3:
            return "1N", "1N no Fit 16+ H<3"
        if 14 <= hcp <= 15 and h >= 4:
            return "3H", "Medium raise 14-15 H4"
        if 11 <= hcp <= 13 and h >= 4:
            return "2H", "Minimum raise 11-13 H4"
        if 14 <= hcp <= 15 and h < 3 and d >= 6 and d_honors >= 2:
            return "3D", "Medium 14-15 good D"
        if 11 <= hcp <= 15 and s >= 4:
            return "1S", "minimum S4"
        if 11 <= hcp <= 15 and d >= 6:
            return "1N", "Minimum D6"
        if 11 <= hcp <= 15 and c >= 4:
            return "2C", "Minimum 2m"

    elif response == "1S":
        if 16 <= hcp <= 20 and shape in ["4441", "4144"]:
            return "2N", "2N Fit 16+ 4441"
        if hcp >= 16 and s >= 4:
            return "2H", "Power Fit 16+ S4"
        if hcp >= 16 and s == 3:
            return "2D", "Turbo Fit 16+ S3"
        if hcp >= 16 and s < 3 and h < 3:
            return "1N", "1N no Fit 16+ S<3"
        if 14 <= hcp <= 15 and s >= 4:
            return "3S", "Medium raise 14-15 S4"
        if 11 <= hcp <= 13 and s >= 4:
            return "2S", "Minimum raise 11-13 S4"
        if 14 <= hcp <= 15 and s < 3 and d >= 6 and d_honors >= 2:
            return "3D", "Medium 14-15 good D"
        if 11 <= hcp <= 15 and c >= 4:
            return "1S", "minimum 2m"
        if 11 <= hcp <= 15 and (d >= 6 or (h >= 4 and d >= 5)):
            return "1N", "Minimum D6 or H4D5"

    elif response == "1N":
        if shape in ["4441", "4144", "1444"] or (11 <= hcp <= 15 and d >= 4 and c >= 4):
            return "2C", "any 4441 or minimum 2m"
        if d >= 5 and h >= 4:
            return "2D", "D5H4"
        if d >= 5 and s >= 4:
            return "2H", "D5S4"
        if c >= 4:
            return "2S", "extra 2m"
        if d >= 6 and has_short(shape):
            return "2N", "D6 have short"
        if d >= 6:
            return "3C", "D6 no short"

    elif response == "2C":
        if hcp >= 16:
            return "2H", "Extra asking"
        if 11 <= hcp <= 15 and d >= 6 and c <= 1:
            return "2D", "Minimum D6+"
        if 14 <= hcp <= 15 and c >= 3:
            return "3C", "Medium raised"
        return "PASS", "good luck partner"

    elif response == "2D":
        if hcp >= 16:
            return "2H", "Asking"
        if 14 <= hcp <= 15 and d >= 5:
            return "3D", "Medium raised"
        return "PASS", "ทนไว้อย่าซน"

    elif response == "2H":
        if hcp >= 13:
            return "2S", "13+ Asking"
        if 11 <= hcp <= 12 and c >= 4:
            return "3C", "P/C"
        if 11 <= hcp <= 12 and d >= 6:
            return "3D", "11-12 D6"
        if 11 <= hcp <= 12 and c < 4:
            return "2N", "P/C"

    elif response == "2S":
        if hcp >= 14:
            return "3S", "show Stop"
        if hcp >= 14:
            return "3H", "slam interest or stop H"
        if 11 <= hcp <= 13 and shape == "4441":
            return "2N", "11-13 4441"
        if 11 <= hcp <= 12 and c >= 3:
            return "3C", "11-13 C3+"
        if 11 <= hcp <= 13 and d >= 6:
            return "3D", "11-13 D6"

    elif response == "2N":
        if hcp >= 11:
            return "3D", "อดทนไว้"

    elif response == "3C":
        if hcp >= 14:
            return "3H", "interest slam or stop"
        if hcp >= 14:
            return "3S", "show stop"
        return "3D", "minimum"

    elif response == "3D":
        if hcp >= 17:
            return "3N", "stop M"
        if hcp >= 16:
            return "3S", "show stop"
        if hcp >= 16:
            return "3H", "16+ กำลังหาเกม"
        return "PASS", "อดทนไว้"

    return "PASS", "no good bid for 1D rebid"


# ==========================================
# OPENER REBID AFTER 1H 
# ==========================================

def opener_rebid_1h(response, hcp, shape, extra_info=None):
    if extra_info is None:
        extra_info = {}
    s = extra_info.get("S", int(shape[0]))
    h = extra_info.get("H", int(shape[1]))
    d = extra_info.get("D", int(shape[2]))
    c = extra_info.get("C", int(shape[3]))
    balanced = extra_info.get("balanced", False)
    short_suit = extra_info.get("short_suit", None)
    
    total_point = hcp + extra_info.get("distribution_point", 0)
    a_min = total_point
    b_max = total_point + 3 
    
    if response == "1S":
        sec_suit_len = extra_info.get("sec_suit_len", max(s, d, c))
        if 11 <= hcp <= 15:
            if h >= 8: return "4H", "11-15 H8+"
            if h == 7: return "3H", "11-15 H7"
            if s >= 5: return "2S", "11-15 S5+"
            if h >= 6 and sec_suit_len >= 5: return "3N", "11-15 H6+ m5+"
            if d >= 6: return "4D", "11-15 D6+"
            if c >= 6: return "4C", "11-15 C6+"
        if 15 <= hcp <= 16 and s >= 5: return "3S", "15-16 S5+"
        if 15 <= hcp <= 17 and d >= 5: return "3D", "15-17 D5+"
        if 15 <= hcp <= 17 and c >= 5: return "3C", "15-17 C5+"
        if 17 <= hcp <= 19 and balanced: return "2N", "Big NT"
        if 14 <= hcp <= 15 and h >= 6: return "2H", "14-15 H6+"
        if 11 <= hcp <= 15:
            if s == 4: return "2D", "11-15 S4"
            if c >= 4: return "2C", "11-15 C4+"
            if d >= 4 or hcp >= 16: return "1N", "11-15 D4+ or 16+ any"

    elif response == "1N":
        sec_suit_len = extra_info.get("sec_suit_len", max(s, d, c))
        if 14 <= hcp <= 15 and s >= 4: return "3S", "14-15 S4+"
        if 11 <= hcp <= 15 and s >= 3: return "2S", "11-13 S3+"    
        if 11 <= hcp <= 15:
            if h >= 8 and s <= 3: return "4H", "11-15 H8+"
            if h == 7 and s <= 3: return "3H", "11-15 H7"
            if h >= 6 and sec_suit_len >= 5: return "3N", "11-15 H6+ second suit 5+"
            if d >= 6: return "4D", "11-15 D6+"
            if c >= 6: return "4C", "11-15 C6+"
        if 15 <= hcp <= 17 and d >= 5: return "3D", "15-17 D5+"
        if 15 <= hcp <= 17 and c >= 5: return "3C", "15-17 C5+"
        if 17 <= hcp <= 19 and shape == "2533": return "2N", "Big NT"
        if 14 <= hcp <= 15 and h >= 6: return "2H", "14-15 S6+"
        if 11 <= hcp <= 15:
            if d >= 4: return "2D", "11-15 D4+"
            if c >= 4 or hcp >= 16: return "2C", "11-15 C4+ or 16+ any"

    elif response == "2C":
        if h >= 6: return "2D", "Transfer H"
        if s >= 4: return "2H", "Transfer S"
        if c >= 4: return "2S", "Transfer C"
        if d >= 4 and short_suit == 'S': return "2N", "Transfer D short Hi"
        if d >= 4 and short_suit == 'C': return "3C", "Transfer D short Lo"
        if d >= 4 and shape == "2542": return "3D", "Transfer D no short"
        if d >= 5: return "3H", "S5D5"
        if 17 <= hcp <= 19 and balanced and s == 3: return "3S", "Big NT S3"
        if 17 <= hcp <= 19 and balanced and h == 2: return "3N", "Big NT S2"

    elif response in ["2D", "2H"]:
        if a_min > 25 and b_max < 30 and not short_suit: return "4H", "not interest slam"
        if a_min > 22 and b_max < 25 and s >= 6 and short_suit == 'S': return "2N", "Game try short S"
        if a_min > 22 and b_max < 25 and s >= 6 and short_suit == 'D': return "3D", "Game try short D"
        if a_min > 22 and b_max < 25 and s >= 6 and short_suit == 'C': return "3C", "Game try short C"
        if b_max < 25 and s == 5 and not short_suit: return "2H", "not interest game"
        return "2S", "Asking"

    elif response == "2S":
        if 11 <= hcp <= 15 and s == 4 and short_suit:
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

    elif response == "2N":
        # black_point = spade point, c_point = club point
        e = a_min - extra_info.get("black_point", 0)
        f = a_min - extra_info.get("diamond_point", 0)
        g = a_min - extra_info.get("c_point", 0)
        min_efg = min(e, f, g)
        if min_efg == e and e < 20: return "3H", "สั้น S อาจไม่เกม"
        elif min_efg == f and f < 20: return "3D", "สั้น D อาจไม่เกม"
        elif min_efg == g and g < 20: return "3C", "สั้น C อาจไม่เกม"
        return "3C", "ถามชุดสั้น สนใจสแลม"

    elif response == "3C":
        if a_min > 24 and b_max < 30: return "4H", "To play"
        if b_max < 25: return "3H", "minimum hand"
        return "3D", "สนใจเกม ถ้าถือ 10-12"

    elif response == "3D":
        return "3H", "waiting"

    elif response == "3H":
        if a_min > 20: return "4H", "ยิง"
        return "PASS", "ไม่น่าเกม"

    elif response == "3S":
        # black_point = spade point
        k = hcp - extra_info.get("unused_black_point", 0) + 13
        if k < 25: return "4H", "bad hand"
        return "3N", "สนใจสแลม"

    elif response == "3N":
        # c_point = club point
        k = hcp - extra_info.get("unused_c_point", 0) + 13
        if k < 25: return "4S", "K < 25"
        return "4C", "สนใจสแลม"

    elif response == "4C":
        k = hcp - extra_info.get("unused_diamond_point", 0) + 13
        if k < 25: return "4S", "K < 25"
        return "4D", "สนใจสแลม"

    elif response == "4H":
        return "PASS", "ไม่น่าไปสแลมไหว"

    return "PASS", "no good bid for 1H rebid"


# ==========================================
# OPENER REBID AFTER 1S
# ==========================================

def opener_rebid_1s(response, hcp, shape, extra_info=None):
    if extra_info is None:
        extra_info = {}
    
    s = extra_info.get("S", int(shape[0]))
    h = extra_info.get("H", int(shape[1]))
    d = extra_info.get("D", int(shape[2]))
    c = extra_info.get("C", int(shape[3]))
    balanced = extra_info.get("balanced", False)
    short_suit = extra_info.get("short_suit", None)
    
    total_point = hcp + extra_info.get("distribution_point", 0)
    a_min = total_point
    b_max = total_point + 3

    if response == "1N":
        sec_suit_len = extra_info.get("sec_suit_len", max(h, d, c))
        if 11 <= hcp <= 15:
            if s >= 8: return "4S", "11-15 S8+"
            if s == 7: return "3S", "11-15 S7"
            if s >= 6 and sec_suit_len >= 5: return "3N", "11-15 S6+ second suit 5+"
            if h >= 6: return "4H", "11-15 H6+"
            if d >= 6: return "4D", "11-15 D6+"
            if c >= 6: return "4C", "11-15 C6+"
        if 15 <= hcp <= 16 and h >= 5: return "3H", "15-16 H5+"
        if 15 <= hcp <= 17 and d >= 5: return "3D", "15-17 D5+"
        if 15 <= hcp <= 17 and c >= 5: return "3C", "15-17 C5+"
        if 17 <= hcp <= 19 and balanced: return "2N", "Big NT"
        if 14 <= hcp <= 15 and s >= 6: return "2S", "14-15 S6+"
        if 11 <= hcp <= 15:
            if h >= 4: return "2H", "11-15 H4+"
            if d >= 4: return "2D", "11-15 D4+"
            if c >= 4 or hcp >= 16: return "2C", "11-15 C4+ or 16+ any"

    elif response == "2C":
        if h >= 4: return "2D", "Transfer H"
        if s >= 6: return "2H", "Transfer S"
        if c >= 4: return "2S", "Transfer C"
        if d >= 4 and short_suit == 'H': return "2N", "Transfer D short Hi"
        if d >= 4 and short_suit == 'C': return "3C", "Transfer D short Lo"
        if d >= 4 and shape == "5242": return "3D", "Transfer D no short"
        if d >= 5: return "3H", "S5D5"
        if 17 <= hcp <= 19 and balanced and h == 3: return "3S", "Big NT oM3"
        if 17 <= hcp <= 19 and balanced and h == 2: return "3N", "Big NT oM2"
        return "2H", "Default 2H"

    elif response == "2D":
        if hcp >= 17 and s >= 6: return "3S", "17+ S6+"
        if 14 <= hcp <= 15 and h == 4: return "3H", "14-15 H4"
        if hcp >= 17 and d >= 4: return "3D", "17+ D4+"
        if hcp >= 17 and c >= 4: return "3C", "17+ C4+"
        if hcp >= 16 and h >= 2: return "2N", "asking"
        if 14 <= hcp <= 16 and s >= 6 and h < 2: return "2S", "S6+ ทนเดิน 2H ไม่ไหว"
        if 11 <= hcp <= 15: return "2H", "waiting"
        return "2H", "Default 2H"

    elif response in ["2H", "2S"]:
        if a_min > 25 and b_max < 30 and not short_suit: return "4S", "not interest slam"
        if a_min > 22 and b_max < 25 and s >= 6 and short_suit == 'H': return "3H", "Game try short H"
        if a_min > 22 and b_max < 25 and s >= 6 and short_suit == 'D': return "3D", "Game try short D"
        if a_min > 22 and b_max < 25 and s >= 6 and short_suit == 'C': return "3C", "Game try short C"
        if b_max < 25 and s == 5 and not short_suit: return "2S", "not interest game"
        return "2N", "Asking"

    elif response == "2N":
        # red_point = heart point, c_point = club point
        e = a_min - extra_info.get("red_point", 0)
        f = a_min - extra_info.get("diamond_point", 0)
        g = a_min - extra_info.get("c_point", 0)
        min_efg = min(e, f, g)
        if min_efg == e and e < 20: return "3H", "สั้น H อาจไม่เกม"
        elif min_efg == f and f < 20: return "3D", "สั้น D อาจไม่เกม"
        elif min_efg == g and g < 20: return "3C", "สั้น C อาจไม่เกม"
        return "3C", "ถามชุดสั้น สนใจสแลม"

    elif response == "3C":
        if a_min > 24 and b_max < 30: return "4S", "To play"
        if b_max < 25: return "3S", "minimum hand"
        return "3D", "สนใจเกม ถ้าถือ 10-12"

    elif response == "3D":
        return "3S", "waiting"

    elif response == "3H":
        # red_point = heart point
        k = hcp - extra_info.get("unused_red_point", 0) + 13
        if k < 25: return "4S", "K < 25"
        return "3S", "สนใจสแลม"

    elif response == "3N":
        # c_point = club point
        k = hcp - extra_info.get("unused_c_point", 0) + 13
        if k < 25: return "4S", "K < 25"
        return "4C", "สนใจสแลม"

    elif response == "4C":
        k = hcp - extra_info.get("unused_diamond_point", 0) + 13
        if k < 25: return "4S", "K < 25"
        return "4D", "สนใจสแลม"

    elif response == "3S":
        if a_min > 20: return "4S", "ยิง"
        return "PASS", "ไม่น่าเกม"

    return "PASS", "no good bid for 1S rebid"
