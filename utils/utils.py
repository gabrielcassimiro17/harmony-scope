import random
import streamlit as st


def sample_playlist(song_list, sample_size):
    return random.sample(song_list, sample_size)


def check_password():
    """Check the password entered by the user."""
    if st.session_state.login_attempts >= 3:
        st.error("Too many login attempts. Please try again later.")
        return False

    # Check if the password matches
    if (
        st.sidebar.text_input("Enter the password:", type="password")
        == st.secrets["password"]
    ):
        st.sidebar.success("Password is correct. You are logged in.")
        return True
    else:
        # Increment the attempt count
        st.session_state.login_attempts += 1
        if st.session_state.login_attempts < 3:
            st.error("Password is incorrect. Try again.")
        else:
            st.error("Too many login attempts. Please try again later.")
        return False
