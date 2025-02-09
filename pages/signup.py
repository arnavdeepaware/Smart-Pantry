import streamlit as st

st.title("Sign Up")
firstName = st.text_input("First Name")
lastName = st.text_input("Last Name")
email = st.text_input("Email")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if username and password:
        st.success("Sign Up Successful!")
    else:
        st.error("Please fill in both fields.")