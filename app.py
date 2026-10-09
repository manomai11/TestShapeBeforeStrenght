import streamlit as st
import random

from engine import opening_bid

# ==========================================
# CARD HELPERS
# ==========================================

RANKS = "AKQJT98765432"

HCP_MAP = {
    "A": 4,
    "K": 3,
    "Q": 2,
    "J": 1
}


def generate_hand():

    deck = []

    for suit in ["S", "H", "D", "C"]:
        for rank in RANKS:
            deck.append((suit, rank))

    random.shuffle(deck)

    hand = deck[:13]

    suits = {
        "S": [],
        "H": [],
        "D": [],
        "C": [],
    }

    for suit, rank in hand:
        suits[suit].append(rank)

    for suit in suits:
        suits[suit].sort(
            key=lambda x: RANKS.index(x)
        )

    return suits


def calculate_hcp(hand):

    total = 0

    for suit_cards in hand.values():

        for card in suit_cards:

            total += HCP_MAP.get(card, 0)

    return total


def calculate_shape(hand):

    return (
        str(len(hand["S"])) +
        str(len(hand["H"])) +
        str(len(hand["D"])) +
        str(len(hand["C"]))
    )


# ==========================================
# STREAMLIT
# ==========================================

st.set_page_config(
    page_title="Shape Before Strength",
    page_icon="♠",
    layout="wide",
)

if "hand" not in st.session_state:
    st.session_state.hand = generate_hand()

if "score" not in st.session_state:
    st.session_state.score = 0

if "question" not in st.session_state:
    st.session_state.question = 1

if "answered" not in st.session_state:
    st.session_state.answered = False

if "result" not in st.session_state:
    st.session_state.result = ""

if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""


hand = st.session_state.hand

hcp = calculate_hcp(hand)
shape = calculate_shape(hand)

correct_answer = opening_bid(
    hcp,
    shape
)

st.title("Opening Practice")

st.write(f"Question : {st.session_state.question}/20")
st.write(f"Score : {st.session_state.score}")

st.divider()

st.markdown(
    f"""
### Hand

♠ {"".join(hand["S"])}

♥ {"".join(hand["H"])}

♦ {"".join(hand["D"])}

♣ {"".join(hand["C"])}
"""
)

st.write(f"HCP : {hcp}")
st.write(f"Shape : {shape}")

st.divider()

if not st.session_state.answered:

    bids = [
        "PASS",

        "1C","1D","1H","1S","1N",

        "2C","2D","2H","2S","2N",

        "3C","3D","3H","3S","3N",

        "4C","4D","4H","4S",

        "5C","5D","5H","5S","5N",

        "6C","6D","6H","6S","6N",

        "7C","7D","7H","7S","7N"
    ]

    choice = st.selectbox(
        "Choose Bid",
        bids
    )

    if st.button("Submit"):

        st.session_state.user_answer = choice

        if choice == correct_answer:

            st.session_state.result = "✅ Correct"

            st.session_state.score += 1

        else:

            st.session_state.result = "❌ Incorrect"

        st.session_state.answered = True

        st.rerun()

else:

    st.markdown(
        f"## {st.session_state.result}"
    )

    st.write(
        f"Your Answer : {st.session_state.user_answer}"
    )

    st.write(
        f"Correct Answer : {correct_answer}"
    )

    if st.button("Next Question"):

        st.session_state.question += 1

        st.session_state.answered = False

        st.session_state.hand = generate_hand()

        st.rerun()
