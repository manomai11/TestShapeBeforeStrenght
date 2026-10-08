from engine import (
    opening_bid,
    response_1nt,
)

# =====================================
# COUNTERS
# =====================================

total = 0
passed = 0

# =====================================
# TEST HELPER
# =====================================

def check(
    name,
    expected,
    actual
):

    global total
    global passed

    total += 1

    if expected == actual:

        passed += 1

        print(f"PASS {name}")

    else:

        print(f"FAIL {name}")

        print(
            f"Expected={expected}"
        )

        print(
            f"Actual={actual}"
        )

        print("-" * 40)

# =====================================
# OPENING TESTS
# =====================================

OPENING = [

    (13,"5512","1S"),
    (17,"5530","2D"),
    (22,"5332","2N"),
    (14,"4432","1N"),
    (11,"4432","1C"),

    (17,"1345","1C"),
    (14,"2245","1D"),

    (8,"6322","2D"),
    (12,"6322","2S"),
    (15,"6322","1S"),

    (8,"3622","2D"),
    (12,"3622","2H"),
    (15,"3622","1H"),
]

print("\nOPENING TESTS\n")

for idx, row in enumerate(OPENING):

    hcp, shape, expected = row

    actual = opening_bid(
        hcp,
        shape
    )

    check(
        f"O{idx+1}",
        expected,
        actual
    )

# =====================================
# 1NT TESTS
# =====================================

NT = [

    (8,"5521","2C"),
    (8,"5611","2C"),
    (8,"6511","2C"),

    (9,"5512","3D"),
    (9,"5611","3D"),
    (9,"6511","3D"),

    (9,"1255","2D"),

    (10,"5422","2C"),

    (10,"3613","4C"),
    (10,"6313","4D"),

    (11,"4333","3C"),

    (11,"2245","3N"),
    (12,"2263","3N"),

    (11,"3145","3H"),
    (11,"1345","3S"),

    (16,"4333","2C"),
    (16,"2236","2S"),
    (16,"1255","2D"),
]

print("\nRESPONSE 1NT TESTS\n")

for idx, row in enumerate(NT):

    hcp, shape, expected = row

    actual = response_1nt(
        hcp,
        shape
    )

    check(
        f"N{idx+1}",
        expected,
        actual
    )

print("\nSUMMARY\n")

print(
    f"Passed = {passed}"
)

print(
    f"Total  = {total}"
)

if total:

    print(
        f"Accuracy = {passed/total*100:.2f}%"
    )
