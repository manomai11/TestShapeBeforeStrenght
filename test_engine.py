from engine import (
    opening_bid,
    response_1nt,
    response_1major,
    response_1d,
    response_1c,
)

# =====================================
# COUNTER
# =====================================

total_tests = 0
passed_tests = 0


# =====================================
# TEST HELPER
# =====================================

def run_test(
    name,
    expected,
    actual
):

    global total_tests
    global passed_tests

    total_tests += 1

    if expected == actual:

        passed_tests += 1
        print(f"PASS  {name}")

    else:

        print(f"FAIL  {name}")
        print(f"Expected : {expected}")
        print(f"Actual   : {actual}")
        print("-" * 40)


# =====================================
# OPENING
# =====================================

OPENING_TESTS = [

    (13, "5512", "1S"),
    (17, "5530", "2D"),
    (22, "5332", "2N"),
    (14, "4432", "1N"),
    (11, "4432", "1C"),

    (17, "1345", "1C"),
    (14, "2245", "1D"),

    (8, "6322", "2D"),
    (12, "6322", "2S"),
    (15, "6322", "1S"),

    (8, "3622", "2D"),
    (12, "3622", "2H"),
    (15, "3622", "1H"),
]

print("\nOPENING TESTS\n")

for idx, row in enumerate(OPENING_TESTS):

    hcp, shape, expected = row

    actual = opening_bid(
        hcp,
        shape
    )

    run_test(
        f"O{idx+1}",
        expected,
        actual
    )


# =====================================
# RESPONSE 1NT
# =====================================

NT_TESTS = [

    (8, "5521", "2C"),
    (8, "5611", "2C"),
    (8, "6511", "2C"),

    (9, "5512", "3D"),
    (9, "5611", "3D"),
    (9, "6511", "3D"),

    (9, "1255", "2D"),

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

print("\nRESPONSE 1NT TESTS\n")

for idx, row in enumerate(NT_TESTS):

    hcp, shape, expected = row

    actual = response_1nt(
        hcp,
        shape
    )

    run_test(
        f"N{idx+1}",
        expected,
        actual
    )


# =====================================
# RESPONSE 1MAJOR
# =====================================

MAJOR_TESTS = [

    ("1H", 0, "4432", False, "3D"),
    ("1H", 5, "4432", True, "3H"),
    ("1H", 8, "4432", False, "3C"),
    ("1H", 9, "5521", False, "4H"),
    ("1H", 12, "5521", False, "2N"),

    ("1H", 13, "4513", False, "4C"),
    ("1H", 13, "4531", False, "3N"),
    ("1H", 13, "4504", False, "3D"),

    ("1S", 0, "4432", False, "3D"),
    ("1S", 5, "4432", True, "3S"),
    ("1S", 8, "4432", False, "3C"),

    ("1S", 9, "5521", False, "4S"),
    ("1S", 12, "5521", False, "2N"),

    ("1S", 13, "4513", False, "4C"),
    ("1S", 13, "4531", False, "3N"),
    ("1S", 13, "4504", False, "3D"),
]

print("\nRESPONSE 1MAJOR TESTS\n")

for idx, row in enumerate(MAJOR_TESTS):

    opening, hcp, shape, ace, expected = row

    actual = response_1major(
        opening,
        hcp,
        shape,
        ace
    )

    run_test(
        f"M{idx+1}",
        expected,
        actual
    )


# =====================================
# RESPONSE 1D
# =====================================

RESP1D_TESTS = [

    (13, "4432", True, False, "1N"),
    (13, "4432", True, True, "1H"),

    (13, "5530", False, False, "1S"),
    (13, "4513", False, False, "1H"),

    (11, "2254", False, False, "2S"),

    (11, "3334", True, False, "2H"),

    (8, "1156", False, False, "3D"),
    (10, "1156", False, False, "2S"),

    (8, "1265", False, False, "3D"),
    (12, "1265", False, False, "3C"),

    (5, "1265", False, False, "2N"),
]

print("\nRESPONSE 1D TESTS\n")

for idx, row in enumerate(RESP1D_TESTS):

    hcp, shape, balanced, bad_suit, expected = row

    actual = response_1d(
        hcp,
        shape,
        balanced,
        bad_suit
    )

    run_test(
        f"D{idx+1}",
        expected,
        actual
    )


# =====================================
# RESPONSE 1C
# =====================================

RESP1C_TESTS = [

    (13, "4423", True, False, "1N"),
    (13, "4432", True, True, "1D"),

    (6, "4432", False, False, "1D"),
    (10, "4342", False, False, "1H"),

    (11, "1264", False, False, "2C"),
    (12, "1264", False, False, "2C"),

    (0, "3337", False, False, "2N"),
    (6, "3337", False, False, "3C"),

    (7, "1255", False, False, "2S"),
    (12, "1255", False, False, "2C"),
]

print("\nRESPONSE 1C TESTS\n")

for idx, row in enumerate(RESP1C_TESTS):

    hcp, shape, balanced, bad_suit, expected = row

    actual = response_1c(
        hcp,
        shape,
        balanced,
        bad_suit
    )

    run_test(
        f"C{idx+1}",
        expected,
        actual
    )


# =====================================
# SUMMARY
# =====================================

print("\n")
print("=" * 40)
print("SUMMARY")
print("=" * 40)

print(f"Passed : {passed_tests}")
print(f"Total  : {total_tests}")

if total_tests > 0:

    score = (
        passed_tests / total_tests
    ) * 100

    print(
        f"Accuracy : {score:.2f}%"
    )
