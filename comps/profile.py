import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client
from backend.test import get_user_info, update_user_info

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def show_profile():

    # Initialize session state with default values
    default_values = {
        'first_name': "",
        'last_name': "",
        'username': "",
        'email': "",
        'current_weight': 0.0,
        'target_weight': 0.0,
        'current_height': 0.0,
        'time_to_target': "3 months",
        'daily_calories': 2200,
        'age': 25,
        'dietary_preference': 'Vegetarian',
        'sex': 'Male'
    }

    # Initialize session state if values don't exist
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    user_id = st.session_state.user_id
    user_data = get_user_info(user_id)

    if user_data:
        profile_keys = ['first_name', 'last_name', 'username', 'email', 'current_weight', 'target_weight', 'current_height', 'time_to_target', 'age', 'dietary_preference', 'sex']
        for key in profile_keys:
            if key in user_data and user_data[key] is not None:
                st.session_state[key] = user_data[key]

    st.title("👤 Profile")
    st.write("<div style='text-align: left;'>Update your personal information and health goals below.</div>", unsafe_allow_html=True)
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
        /* Center the submit button container */
        div.stButton {
            text-align: center;
            width: 100%;
        }
        /* Style the submit button itself */
        div.stButton > button {
            width: auto;
            padding-left: 2rem;
            padding-right: 2rem;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)

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
                value=float(st.session_state.current_height) if st.session_state.current_height is not None else 0.0,
                help="Your current height in centimeters"
            )
            current_weight = st.number_input(
                "Current Weight ⚖️",
                min_value=0.0,
                max_value=500.0,
                value=float(st.session_state.current_weight) if st.session_state.current_weight is not None else 0.0,
                help="Your current weight in kilograms"
            )

            # Move daily calories to first column
            daily_calories = st.number_input(
                "Daily Calories Budget 🔥",
                value=int(st.session_state.daily_calories) if st.session_state.daily_calories is not None else 2200,
                disabled=True,
                help="Calculated based on your goals and current metrics"
            )

            age = st.number_input(
                "Age 🎂",
                min_value=0,
                max_value=120,
                value=st.session_state.age,
                step=1,
                help="Enter your age"
            )

            # Dietary preference dropdown
            dietary_preference = st.selectbox(
                "Dietary Preference 🥗",
                options=['vegetarian', 'vegan', 'halal', 'kosher', 'gluten-free', 'dairy-free'],
                index=['vegetarian', 'vegan', 'halal', 'kosher', 'gluten-free', 'dairy-free'].index(
                    st.session_state.dietary_preference.lower() if st.session_state.dietary_preference else 'vegetarian'
                ),
                help="Select your dietary preference"
            )

        with col4:
            target_weight = st.number_input(
                "Target Weight 🎯",
                min_value=0.0,
                max_value=500.0,
                value=float(st.session_state.target_weight) if st.session_state.target_weight is not None else 0.0,
                help="Your goal weight in kilograms"
            )

            time_to_target = st.selectbox(
                "Time to Target ⏱️",
                options=['1 month', '3 months', '6 months', '12 months'],
                index=['1 month', '3 months', '6 months', '12 months'].index(st.session_state.time_to_target),
                help="Select your target timeframe"
            )

            # Sex dropdown (male, female, other)
            sex = st.selectbox(
                "Sex",
                options=['Male', 'Female', 'Other'],
                index=['Male', 'Female', 'Other'].index(st.session_state.sex),
                help="Select your sex"
            )

        # Center the submit button
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
            st.session_state.age = age
            st.session_state.dietary_preference = dietary_preference
            st.session_state.sex = sex

            # Prepare data for update
            update_data = {
                'first_name': first_name[:100] if first_name else None,  # VARCHAR(100)
                'last_name': last_name[:100] if last_name else None,     # VARCHAR(100)
                'username': username[:50] if username else None,          # VARCHAR(50)
                'current_height': float(current_height) if current_height else None,  # DECIMAL(5,2)
                'current_weight': int(current_weight) if current_weight else None,    # INTEGER NOT NULL
                'target_weight': float(target_weight) if target_weight else None,     # DECIMAL(5,2)
                'time_to_target': time_to_target,  # VARCHAR(20) with CHECK constraint
                'age': int(age) if age else None,  # INTEGER with CHECK constraint
                'dietary_preference': dietary_preference.lower(),  # VARCHAR(50) with CHECK constraint
                'sex': sex  # TEXT with CHECK constraint
            }

            # Validate constraints before sending
            if update_data['current_weight'] is None:
                st.error("❌ Current weight is required")
                return

            if update_data['time_to_target'] not in ['1 month', '3 months', '6 months', '12 months']:
                st.error("❌ Invalid time to target value")
                return

            if update_data['dietary_preference'] not in ['vegetarian', 'vegan', 'halal', 'kosher', 'gluten-free', 'dairy-free']:
                st.error("❌ Invalid dietary preference")
                return

            if update_data['sex'] not in ['Male', 'Female', 'Other']:
                st.error("❌ Invalid sex value")
                return

            if update_data['age'] and (update_data['age'] < 1 or update_data['age'] > 120):
                st.error("❌ Age must be between 1 and 120")
                return

            # Update user information
            update_response = update_user_info(user_id, update_data)
            with st.spinner("Updating profile..."):
                if update_response:
                    if isinstance(update_response, dict) and 'error' in update_response:
                        st.error(f"❌ Failed to update profile: {update_response['error']}")
                    else:
                        st.success("✅ Profile updated successfully!")
                else:
                    st.error("❌ Failed to update profile: No response from server")

