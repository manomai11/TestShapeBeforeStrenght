import streamlit as st

st.set_page_config(
    page_title="Shape Before Strength",
    layout="wide"
)

if "page" not in st.session_state:
    st.session_state.page = "login"

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# -----------------------
# LOGIN
# -----------------------

if st.session_state.page == "login":

    st.title("Shape Before Strength")

    st.write(
        "Bridge Bidding Trainer"
    )

    name = st.text_input(
        "Player Name"
    )

    if st.button("Start"):

        if name.strip():

            st.session_state.player_name = name
            st.session_state.page = "menu"

            st.rerun()

# -----------------------
# MENU
# -----------------------

elif st.session_state.page == "menu":

    st.title(
        f"Welcome {st.session_state.player_name}"
    )

    st.subheader("Practice")

    col1, col2 = st.columns(2)

    with col1:

        st.button("Opening Practice")

        st.button("Response 1NT")

        st.button("Response 1H")

    with col2:

        st.button("Response 1S")

        st.button("Response 1D")

        st.button("Response 1C")

    st.divider()

    st.subheader("System Notes")

    st.write(
        """
        Shape Before Strength

        Opening

        11-13 Balanced = 1C

        14-16 Balanced = 1NT

        17-19 Balanced No M5 = 1C

        20-22 Balanced = 2NT
        """
    )
