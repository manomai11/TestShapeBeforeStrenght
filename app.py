from engine import (
    opening_bid,
    response_1nt,
    response_1major,
    response_1d,
    response_1c,
)

# ============================================
# OPENING TESTS
# ============================================

OPENING_TESTS = [

    (13, "5512", False, "1S"),
    (17, "5530", False, "2D"),
    (22, "5332", True,  "2N"),
    (14, "4432", True,  "1N"),
    (11, "4432", True,  "1C"),

    (17, "1345", False, "1C"),
    (14, "2245", False, "1D"),

    (8,  "6322", False, "2D"),
    (12, "6322", False, "2S"),
    (15, "6322", False, "1S"),

    (8,  "3622", False, "2D"),
    (12, "3622", False, "2H"),
    (15, "3622", False, "1H"),
]

# ============================================
# RESPONSE 1NT
# ============================================

NT_TESTS = [

    (8,  "5521", "2C"),
    (8,  "6511", "2C"),

    (9,  "5512", "3D"),
    (9,  "5611", "3D"),

    (9,  "1255", "2D"),

    (10, "5422", "2C"),

    (10, "3613", "4C"),
    (10, "6313", "4D"),

    (11, "4333", "3C"),

    (11, "2245", "3N"),
    (12, "2263", "3N"),

    (11, "3145", "3H"),
    (11, "1345", "3S"),

    (16, "4333", "2C"),
    (16, "2236", "2S"),
    (16, "1255", "2D"),
]

# ============================================
# RESPONSE 1MAJOR
# ============================================

MAJOR_TESTS = [

    ("1H", 0,  "4432", "3D"),
    ("1H", 5,  "4432", "3H"),
    ("1H", 8,  "4432", "3C"),
    ("1H", 9,  "5521", "4H"),
    ("1H", 12, "5521", "2N"),

    ("1H", 13, "4513", "4C"),
    ("1H", 13, "4531", "3N"),
    ("1H", 13, "4504", "3D"),

    ("1S", 0,  "4432", "3D"),
    ("1S", 5,  "4432", "3S"),
    ("1S", 8,  "4432", "3C"),

    ("1S", 9,  "5521", "4S"),
    ("1S", 12, "5521", "2N"),

    ("1S", 13, "4513", "4C"),
    ("1S", 13, "4531", "3N"),
    ("1S", 13, "4504", "3D"),
]

# ============================================
# RESPONSE 1D
# ============================================

RESP1D_TESTS = [

    (13, "4432", True,  False, "1N"),
    (13, "4423", True,  True,  "1H"),

    (13, "5530", False, False, "1S"),
    (13, "4513", False, False, "1H"),

    (11, "2254", False, False, "2S"),

    (11, "3334", True,  False, "2H"),

    (6,  "1156", False, False, "3D"),
    (8,  "1156", False, False, "3D"),

    (10, "1156", False, False, "2S"),
    (12, "1156", False, False, "2S"),

    (6,  "1265", False, False, "3D"),
    (8,  "1265", False, False, "3D"),

    (10, "1265", False, False, "3C"),
    (12, "1265", False, False, "3C"),

    (5,  "1255", False, False, "2N"),
]

# ============================================
# RESPONSE 1C
# ============================================

RESP1C_TESTS = [

    (0,  "4432", False, False, "1D"),
    (0,  "5530", False, False, "1H"),

    (13, "3334", False, False, "1N"),

    (6,  "3334", False, False, "1S"),

    (7,  "1265", False, False, "2S"),

    (11, "2254", False, False, "2D"),

    (0,  "3337", False, False, "2N"),

    (6,  "3337", False, False, "3C"),
]

# ============================================
# HELPERS
# ============================================

def report(name, expected, actual):

    if expected == actual:
        print(f"PASS {name}: {actual}")
    else:
        print(
            f"FAIL {name}: "
            f"expected={expected} "
            f"actual={actual}"
        )

# ============================================
# RUN
# ============================================

print("\nOPENING TESTS")

for i, test in enumerate(OPENING_TESTS):

    hcp, shape, balanced, expected = test

    actual = opening_bid(
        hcp,
        shape
    )

    report(f"O{i+1}", expected, actual)


print("\n1NT TESTS")

for i, test in enumerate(NT_TESTS):

    hcp, shape, expected = test

    actual = response_1nt(
        hcp,
        shape
    )

    report(f"N{i+1}", expected, actual)
