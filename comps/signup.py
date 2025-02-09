import streamlit as st

st.title("Sign Up")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if username and password:
        st.success("Sign Up Successful!")
    else:
        st.error("Please fill in both fields.")