import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Study Tracker",
    page_icon="📚",
    layout="centered"
)

# Create a separate Supabase client for this Streamlit session.
if "supabase" not in st.session_state:
    st.session_state.supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

supabase = st.session_state.supabase

st.title("📚 Study Tracker")
st.write("Sign in or create an account to get started.")

# Remember whether this session has successfully signed in.
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    choice = st.radio(
        "Choose an option",
        ["Log in", "Create account"],
        horizontal=True
    )

    with st.form("auth_form"):
        email = st.text_input("Email address").strip()
        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            choice,
            type="primary"
        )

    if submitted:
        if not email or not password:
            st.error("Please enter both your email and password.")

        elif choice == "Create account" and len(password) < 8:
            st.error("Please use a password with at least 8 characters.")

        else:
            try:
                if choice == "Create account":
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    if response.session is not None:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success("Account created! You are signed in.")
                        st.rerun()
                    else:
                        st.success(
                            "Registration submitted. If email confirmation "
                            "is enabled, check your inbox before logging in."
                        )

                else:
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if response.session is not None:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(
                            "No active login session was returned. "
                            "Please try again."
                        )

            except Exception as e:
                st.error(f"Authentication failed: {e}")

else:
    st.success(
        f"Signed in as {st.session_state.user_email}"
    )

    st.info(
        "Authentication test successful! Task storage will be added "
        "after we verify this step."
    )

    if st.button("Log out"):
        try:
            supabase.auth.sign_out()
        finally:
            st.session_state.logged_in = False
            st.session_state.pop("user_email", None)
            st.rerun()
