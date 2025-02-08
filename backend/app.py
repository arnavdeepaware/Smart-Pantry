import streamlit as st
import pandas as pd
from datetime import datetime
#Comment


products_data = {
    "Product": ["Milk", "Eggs", "Spinach", "Chicken Breast"],
    "Purchase Date": ["2024-01-10", "2024-02-01", "2024-02-05", "2024-01-20"],
    "Quantity": [1, 12, 3, 2], 
    "Calories": [150, 72, 23, 165],  
    "Suggested Recipes": [
        "https://www.example.com/milk-recipes",
        "https://www.example.com/eggs-recipes",
        "https://www.example.com/spinach-recipes",
        "https://www.example.com/chicken-recipes",
    ],
    "Nearby Locations": [
        "https://www.example.com/nearby-milk-store",
        "https://www.example.com/nearby-eggs-store",
        "https://www.example.com/nearby-spinach-store",
        "https://www.example.com/nearby-chicken-store",
    ]
}


df = pd.DataFrame(products_data)
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])

def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if username and password:
            st.success("Sign Up Successful!")
        else:
            st.error("Please fill in both fields.")

def signin():
    st.title("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign In"):
        if username and password:
            st.success("Sign In Successful!")
        else:
            st.error("Please fill in both fields.")

def pantry_dashboard():
    st.title("My Pantry Dashboard")
    st.write("Welcome to your pantry! Here's a list of the products currently in your fridge:")

    st.table(df)

    for index, row in df.iterrows():
        st.subheader(row["Product"])
        st.write(f"**Purchase Date:** {row['Purchase Date'].strftime('%B %d, %Y')}")
        st.write(f"**Quantity:** {row['Quantity']}")
        st.write(f"**Calories (per serving):** {row['Calories']} kcal")
        st.markdown(f"**[Suggested Recipes]({row['Suggested Recipes']})**")
        st.markdown(f"**[Nearby Locations]({row['Nearby Locations']})**")
        st.write("---")

def profile_page():
    st.title("Profile Page")
    st.write("Edit your profile information.")

def main():
    st.sidebar.title("Smart Pantry")
    options = ["Sign Up", "Sign In", "My Pantry Dashboard", "Profile Page"]
    choice = st.sidebar.radio("Select a Page", options)

    if choice == "Sign Up":
        signup()
    elif choice == "Sign In":
        signin()
    elif choice == "My Pantry Dashboard":
        pantry_dashboard()
    elif choice == "Profile Page":
        profile_page()

if __name__ == "__main__":
    main()