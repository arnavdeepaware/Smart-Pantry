import streamlit as st
import sqlite3
from datetime import datetime
from comps.dashboard import show_dashboard
from comps.profile import show_profile
from comps.ingredients import show_ingredients
from comps.recipes import show_recipes_board
from supabase import create_client
import os
from dotenv import load_dotenv

# Page configuration
st.set_page_config(
    page_title="Smart Pantry",
    page_icon="🏠",
    layout="centered"
)


load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)



# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stButton > button {
        width: 100%;
        margin: 15px 0;
        font-size: 1.2rem !important;
        padding: 0.5rem 1rem;
    }
    div.row-widget.stButton {
        text-align: center;
    }
    /* Increase text input font sizes */
    .stTextInput input {
        font-size: 1.1rem;
    }
    /* Custom class for larger text */
    .title {
        font-size: 2.5rem !important;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.3rem !important;
        margin-bottom: 2rem;
    }
    .stMarkdown {
        text-align: center;
    }
    /* Updated promotional columns styling */
    [data-testid="column"] {
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        margin: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }

    [data-testid="column"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }

    /* Add styles for the promotional content */
    [data-testid="column"] h3 {
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }

    [data-testid="column"] p {
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Initialize additional session states
if 'login_submitted' not in st.session_state:
    st.session_state.login_submitted = False
if 'signup_submitted' not in st.session_state:
    st.session_state.signup_submitted = False
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'My Profile'
if 'sub_page' not in st.session_state:
    st.session_state.sub_page = None

def show_landing():
    # Create a container for centered content
    with st.container():
        st.markdown("<div style='margin-top: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='title' style='text-align: center;'>Welcome to Smart Pantry!!</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle' style='text-align: center;'>Snack Smarter, Waste Lesser!</p>", unsafe_allow_html=True)
        # Create three columns to center the buttons
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Login", use_container_width=True):
                st.session_state.page = 'login'
            if st.button("Sign Up", use_container_width=True):
                st.session_state.page = 'signup'
        # Add spacing between buttons and promotional content
        st.markdown("<div style='margin-top: 5vh;'></div>", unsafe_allow_html=True)
        # Create three promotional columns
        promo1, promo2, promo3 = st.columns(3)

    with promo1:
        st.markdown("### 🔍 Smart Pantry Tracking")
        st.write("""
            Keep track of your pantry ingredients effortlessly.
            Never let food go to waste again!
            - Automatic pantry logging from receipts
            - Expiry date reminders
            - Real-time inventory updates
        """)

    with promo2:
        st.markdown("### 📊 Personalized Meal Insights")
        st.write("""
            Understand your food consumption and health goals.
            Make every meal count!
            - Custom recipe suggestions based on pantry items
            - Nutritional analysis for balanced meals
            - Waste-reduction tips to maximize your ingredients
        """)

    with promo3:
        st.markdown("### 🌟 Sustainable Meal Planning")
        st.write("""
            Make cooking easy, sustainable, and nutritious.
            Let SnackGPT help you eat better while reducing waste!
            - Recipe ideas with available ingredients
            - Health and fitness goal alignment
            - Smart shopping suggestions for missing ingredients
        """)


def show_login():
    with st.container():
        st.markdown("<div style='margin-top: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='title' style='text-align: center;'>Login to Smart Pantry</h1>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            email = st.text_input("Email Address", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True, key="login_button"):
                if email and password:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })

                        if response.user:
                            st.session_state.logged_in = True
                            st.session_state.current_user = email
                            st.session_state.user_id = response.user.id  # Save user_id
                            st.session_state.active_page = "My Profile"
                            st.success("Successfully logged in!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials, please try again.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
                else:
                    st.error("Please enter both email and password")

            if st.button("Back to Home", use_container_width=True, key="login_back"):
                st.session_state.page = 'landing'


def show_signup():
    with st.container():
        st.markdown("<div style='margin-top: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='title' style='text-align: center;'>Create Smart Pantry Account</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])

        with col2:
            email = st.text_input("Email Address", key="signup_email")
            new_username = st.text_input("Choose Username", key="signup_username")
            new_password = st.text_input("Choose Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

            if st.button("Sign Up", use_container_width=True, key="signup_button"):
                st.session_state.signup_submitted = True
                if all([email, new_username, new_password, confirm_password]):
                    if new_password == confirm_password:
                        if "@" in email and "." in email:
                            response = supabase.auth.sign_up({
                                "email": email,
                                "password": new_password
                            })

                            if response.user:
                                user_id = response.user.id
                                user_data = {
                                    "auth_id": user_id,
                                    "username": new_username,
                                    "email": email
                                }

                                insert_result = supabase.table("users").insert(user_data).execute()

                                if insert_result.data:
                                    st.session_state.logged_in = True
                                    st.session_state.current_user = new_username
                                    st.session_state.user_id = user_id  # Save user_id
                                    st.session_state.page = "My Profile"
                                    st.rerun()
                                else:
                                    st.error("Failed to create account. Please try again.")
                            else:
                                st.error("Sign-up failed. Please try again later.")
                        else:
                            st.error("Please enter a valid email address")
                    else:
                        st.error("Passwords don't match!")
                else:
                    st.error("Please fill in all fields")
            if st.button("Back to Home", use_container_width=True, key="signup_back"):
                st.session_state.signup_submitted = False
                st.session_state.page = 'landing'


# Add this new function for the sidebar navigation
def show_sidebar():
    with st.sidebar:
        st.title(f"Welcome, {st.session_state.current_user}")
        st.markdown("---")
        # Navigation options
        st.session_state.active_page = st.radio(
            "Navigation",
            ["Home", "My Profile", "Pantry", "Recipes"],  # "My Profile" matches the condition
            key="nav"
        )
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = 'landing'
            st.rerun()  # Changed from st.experimental_rerun()

# Add this new function to handle the logged-in state pages
def show_logged_in_page():
    show_sidebar()
    # Handle different pages based on navigation selection
    if st.session_state.active_page == "Home":
        show_dashboard()
    elif st.session_state.active_page == "My Profile":
        show_profile()
    elif st.session_state.active_page == "Pantry":
        show_ingredients()
    elif st.session_state.active_page == "Recipes":
        show_recipes_board()


# Main app logic
def main():
    if st.session_state.logged_in:
        show_logged_in_page()
    else:
        if st.session_state.page == 'landing':
            show_landing()
        elif st.session_state.page == 'signup':
            show_signup()
        elif st.session_state.page == 'login':
            show_login()

if __name__ == "__main__":
    main()