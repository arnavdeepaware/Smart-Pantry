import streamlit as st
import sqlite3
from datetime import datetime
from comps.dashboard import show_dashboard
from comps.profile import show_profile
from comps.ingredients import show_ingredients

# Page configuration
st.set_page_config(
    page_title="Smart Pantry",
    page_icon="🏠",
    layout="centered"
)

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
    st.session_state.active_page = 'Home'

def show_landing():
    # Create a container for centered content
    with st.container():
        st.markdown("<div style='margin-top: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='title' style='text-align: center;'>Welcome to Smart Pantry!!</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle' style='text-align: center;'>Your digital solution for smart kitchen management</p>", unsafe_allow_html=True)
        
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
            st.markdown("### 🔍 Smart Inventory")
            st.write("""
                Track your pantry items automatically.
                Never run out of essentials again!
                - Real-time tracking
                - Low stock alerts
                - Shopping suggestions
            """)
        
        with promo2:
            st.markdown("### 📊 Usage Analytics")
            st.write("""
                Understand your kitchen better.
                Make data-driven decisions!
                - Consumption patterns
                - Cost analysis
                - Waste reduction tips
            """)
            
        with promo3:
            st.markdown("### 🌟 Smart Features")
            st.write("""
                Make cooking easier than ever.
                Let AI help you in the kitchen!
                - Recipe suggestions
                - Meal planning
                - Expiry date tracking
            """)

def show_login():
    with st.container():
        st.markdown("<div style='margin-top: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='title' style='text-align: center;'>Login to Smart Pantry</h1>", unsafe_allow_html=True)
                
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
                
            if st.button("Login", use_container_width=True, key="login_button"):
                if username and password:  # Basic validation
                    # Add your login validation logic here
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.active_page = 'Home'
                    st.success("Successfully logged in!")
                    st.rerun()  # Changed from st.experimental_rerun()
                else:
                    st.error("Please enter both username and password")
            
            if st.button("Back to Home", use_container_width=True, key="login_back"):
                st.session_state.login_submitted = False
                st.session_state.page = 'landing'

def show_signup():
    with st.container():
        st.markdown("<div style='margin-top: 15vh;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 class='title' style='text-align: center;'>Create Smart Pantry Account</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            first_name = st.text_input("First Name", key="signup_firstname")
            last_name = st.text_input("Last Name", key="signup_lastname")
            email = st.text_input("Email Address", key="signup_email")
            new_username = st.text_input("Choose Username", key="signup_username")
            new_password = st.text_input("Choose Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
            
            if st.button("Sign Up", use_container_width=True, key="signup_button"):
                st.session_state.signup_submitted = True
                # Basic validation for all fields
                if all([first_name, last_name, email, new_username, new_password, confirm_password]):
                    if new_password == confirm_password:
                        # Basic email validation
                        if "@" in email and "." in email:
                            # Add your signup logic here
                            st.session_state.logged_in = True
                            st.session_state.current_user = new_username
                            st.session_state.active_page = 'Home'
                            st.success("Account created successfully!")
                            st.rerun()  # Changed from st.experimental_rerun()
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
            ["Home", "My Profile", "Pantry", "Recipe Suggestions", "Analytics", "Settings"],  # "My Profile" matches the condition
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
        
    elif st.session_state.active_page == "My Profile":  # Match the radio button text
        show_profile()
        
    elif st.session_state.active_page == "Pantry":
        show_ingredients()
        
    elif st.session_state.active_page == "Recipe Suggestions":
        st.title("Recipe Suggestions")
        # Add your recipe content
        
    elif st.session_state.active_page == "Analytics":
        st.title("Analytics")
        # Add your analytics content
        
    elif st.session_state.active_page == "Settings":
        st.title("Settings")
        # Add your settings content

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