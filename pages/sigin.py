import streamlit as st

st.title("Sign In")
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Sign In"):
    if username and password:
        st.success("Sign In Successful!")
    else:
        st.error("Please fill in both fields.")