from engine import (
    opening_bid,
    response_1nt,
    response_1major,
    response_1d,
    response_1c,
)

total = 0
passed = 0


def check(name, expected, actual):

    global total
    global passed

    total += 1

    if expected == actual:

        passed += 1
        print(f"PASS {name}")

    else:

        print(f"FAIL {name}")
        print(f"Expected = {expected}")
        print(f"Actual   = {actual}")
        print("-" * 40)


# =====================================
# OPENING
# =====================================

opening_tests = [

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

print("\nOPENING\n")

for i, test in enumerate(opening_tests):

    hcp, shape, expected = test

    actual = opening_bid(
        hcp,
        shape
    )

    check(
        f"O{i+1}",
        expected,
        actual
    )

# =====================================
# RESPONSE 1NT
# =====================================

nt_tests = [

    (8,"5521","2C"),
    (8,"5611","2C"),
    (8,"6511","2C"),

    (9,"5512","3D"),
    (9,"5611","3D"),
    (9,"6511","3D"),

    (10,"5422","2C"),

    (10,"3613","4C"),
    (10,"6313","4D"),

    (11,"4333","3C"),

    (11,"2245","3N"),
    (12,"2263","3N"),

    (11,"3145","3H"),
    (11,"1345","3S"),

    (16,"4333","2C"),
]

print("\nRESPONSE 1NT\n")

for i, test in enumerate(nt_tests):

    hcp, shape, expected = test

    actual = response_1nt(
        hcp,
        shape
    )

    check(
        f"N{i+1}",
        expected,
        actual
    )

# =====================================
# RESPONSE 1MAJOR
# =====================================

major_tests = [

    ("1H",8,"6511",False,"4H"),
    ("1H",12,"6511",False,"2N"),

    ("1H",13,"4513",False,"4C"),
    ("1H",13,"4531",False,"3N"),
    ("1H",13,"4504",False,"3D"),

    ("1S",8,"5521",False,"4S"),
    ("1S",12,"5521",False,"2N"),

    ("1S",13,"4513",False,"4C"),
    ("1S",13,"4531",False,"3N"),
    ("1S",13,"4504",False,"3D"),
]

print("\nRESPONSE 1MAJOR\n")

for i, test in enumerate(major_tests):

    opening, hcp, shape, ace, expected = test

    actual = response_1major(
        opening,
        hcp,
        shape,
        ace
    )

    check(
        f"M{i+1}",
        expected,
        actual
    )

# =====================================
# RESPONSE 1D
# =====================================

r1d_tests = [

    (13,"4432",True,False,"1N"),
    (13,"4432",True,True,"1H"),

    (11,"2254",False,False,"2S"),

    (11,"3334",True,False,"2H"),

    (8,"1156",False,False,"3D"),
    (10,"1156",False,False,"2S"),

    (8,"1265",False,False,"3D"),
    (12,"1265",False,False,"3C"),

    (5,"1265",False,False,"2N"),
]

print("\nRESPONSE 1D\n")

for i, test in enumerate(r1d_tests):

    hcp, shape, balanced, bad_suit, expected = test

    actual = response_1d(
        hcp,
        shape,
        balanced,
        bad_suit
    )

    check(
        f"D{i+1}",
        expected,
        actual
    )

# =====================================
# RESPONSE 1C
# =====================================

r1c_tests = [

    (13,"4423",True,False,"1N"),
    (13,"4432",True,True,"1D"),

    (6,"4432",False,False,"1D"),
    (10,"4342",False,False,"1H"),

    (11,"1264",False,False,"2C"),
    (12,"1264",False,False,"2C"),

    (0,"3337",False,False,"2N"),
    (6,"3337",False,False,"3C"),

    (7,"1255",False,False,"2S"),
    (12,"1255",False,False,"2C"),
]

print("\nRESPONSE 1C\n")

for i, test in enumerate(r1c_tests):

    hcp, shape, balanced, bad_suit, expected = test

    actual = response_1c(
        hcp,
        shape,
        balanced,
        bad_suit
    )

    check(
        f"C{i+1}",
        expected,
        actual
    )

# =====================================
# SUMMARY
# =====================================

print("\n========================")
print("SUMMARY")
print("========================")

print(f"Passed : {passed}")
print(f"Total  : {total}")

if total > 0:

    pct = passed / total * 100

    print(f"Accuracy : {pct:.2f}%")
