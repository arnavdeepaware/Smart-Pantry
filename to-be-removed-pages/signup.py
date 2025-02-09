import streamlit as st
from supabase import create_client, Client
import os

# Initialize supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

#st.set_page_config(page_title="Smart Pantry", page_icon="🍲", layout="wide")

# Create a Sign Up page
st.title("Sign Up")
firstName = st.text_input("First Name")
lastName = st.text_input("Last Name")
email = st.text_input("Email")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if firstName and lastName and email and username and password:
        try:
            # Step 1: Create a new user with email and password (password_hash handled by Supabase)
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            # Check if the user is successfully created
            if response.user:
                user_id = response.user.id  # Get the authenticated user ID

                # Step 2: Insert additional user data into 'users' table with 'auth_id'
                data = {
                    "auth_id": user_id,  # Store UUID here
                    "first_name": firstName,
                    "last_name": lastName,
                    "username": username,
                    "email": email
                }
                # Insert data into users table (exclude the password hash column)
                result = supabase.table("users").insert(data).execute()
                
                if result.status_code == 201:  # Successfully inserted
                    st.success("Sign Up Successful! Please check your email for confirmation.")
                else:
                    st.error(f"Error inserting user data: {result.error_message}")
            else:
                st.error(f"Error: {response.error.message if response.error else 'Unknown error'}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("All fields are required!")
