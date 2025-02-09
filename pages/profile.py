import streamlit as st
from datetime import datetime

def show_profile():
    st.title("👤 Profile")
    st.markdown("""
    <style>
        .stForm {
            border: 1px solid #ddd;
            padding: 20px;
            border-radius: 10px;
        }
        .stMarkdown {
            padding: 0 !important;
        }
        hr {
            margin: 20px 0;
            border: none;
            border-top: 1px solid #ddd;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state with default values
    default_values = {
        'first_name': "John",
        'last_name': "Doe",
        'username': "JohnDoe123",
        'email': "john.doe@example.com",  # Add this
        'current_weight': 70,
        'target_weight': 65.00,
        'current_height': 170.00,
        'time_to_target': "3 months",
        'daily_calories': 2000  # Add this
    }

    # Initialize session state if values don't exist
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Create a form with custom styling
    with st.form("profile_form"):
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "First Name 👤",
                value=st.session_state.first_name,
                help="Enter your first name"
            )
            
            username = st.text_input(
                "Username 📝",
                value=st.session_state.username,
                max_chars=50,
                help="Choose a unique username (max 50 characters)"
            )

        with col2:
            last_name = st.text_input(
                "Last Name 👤",
                value=st.session_state.last_name,
                help="Enter your last name"
            )
            
            # Move email to second column for better balance
            email = st.text_input(
                "Email 📧",
                value=st.session_state.email,
                disabled=True,
                help="Contact support to change your email"
            )

        # Add separator between sections
        st.markdown("<hr>", unsafe_allow_html=True)

        st.subheader("Health Goals")
        col3, col4 = st.columns(2)
        
        with col3:
            current_height = st.number_input(
                "Current Height 📏",
                min_value=0.0,
                max_value=300.0,
                value=float(st.session_state.current_height),
                step=0.01,
                help="Your current height in centimeters"
            )
            
            current_weight = st.number_input(
                "Current Weight ⚖️",
                min_value=0,
                max_value=500,
                value=int(st.session_state.current_weight),
                help="Your current weight in kilograms"
            )

            # Move daily calories to first column
            daily_calories = st.number_input(
                "Daily Calories Budget 🔥",
                value=int(st.session_state.daily_calories),
                disabled=True,
                help="Calculated based on your goals and current metrics"
            )

        with col4:
            target_weight = st.number_input(
                "Target Weight 🎯",
                min_value=0.0,
                max_value=500.0,
                value=float(st.session_state.target_weight),
                step=0.1,
                help="Your goal weight in kilograms"
            )
            
            time_to_target = st.selectbox(
                "Time to Target ⏱️",
                options=['1 month', '3 months', '6 months', '12 months'],
                index=['1 month', '3 months', '6 months', '12 months'].index(st.session_state.time_to_target),
                help="Select your target timeframe"
            )
        
        # Center the submit button
        _, col_submit, _ = st.columns([1, 2, 1])
        with col_submit:
            submit_button = st.form_submit_button("💾 Save Changes")
        
        if submit_button:
            # Update session state with new values
            st.session_state.first_name = first_name
            st.session_state.last_name = last_name
            st.session_state.username = username
            st.session_state.current_height = current_height
            st.session_state.current_weight = current_weight
            st.session_state.target_weight = target_weight
            st.session_state.time_to_target = time_to_target
            
            st.success("✅ Profile updated successfully!")

if __name__ == "__main__":  # Changed from "__profile__" to "__main__"
    show_profile()