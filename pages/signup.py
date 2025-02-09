import streamlit as st
from backend.views import supabase

st.title("Sign Up")
firstName = st.text_input("First Name")
lastName = st.text_input("Last Name")
email = st.text_input("Email")
username = st.text_input("Username")
password = st.text_input("Password", type="password")


if st.button("Sign Up"):
    if firstName and lastName and email and username and password:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

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
            supabase.table("users").insert(data).execute()
            
            st.success("Sign Up Successful! Please check your email for confirmation.")
        else:
            st.error(f"Error: {response.error.message if response.error else 'Unknown error'}")
    else:
        st.error("All fields are required!")