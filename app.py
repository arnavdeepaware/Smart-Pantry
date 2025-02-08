import streamlit as st
import pandas as pd
from datetime import datetime
from pages.dashboard import show_dashboard
from pages.ingredients import show_ingredients
from pages.profile import show_profile

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
df["Purchase Date"] = pd.to_datetime(df["Purchase Date"])

def calculate_days_ago(purchase_date):
    return (datetime.today() - purchase_date).days


df["Days Ago Purchased"] = df["Purchase Date"].apply(calculate_days_ago)
df = df.drop(columns=["Purchase Date"])  # Remove old column

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

    # Initialize session state for quantities if not already done
    if 'quantities' not in st.session_state:
        st.session_state.quantities = df["Quantity"].tolist()

    # Display table with updated "Days Ago Purchased"
    st.write("<table>", unsafe_allow_html=True)
    st.write("<tr><th>Product</th><th>Days Ago Purchased</th><th>Quantity</th><th>Calories</th><th>Suggested Recipes</th><th>Nearby Locations</th></tr>", unsafe_allow_html=True)

    for index, row in df.iterrows():
        st.write(f"""
        <tr>
            <td>{row['Product']}</td>
            <td>{row['Days Ago Purchased']}</td>
            <td>
                <button onclick="document.getElementById('quantity_{index}').innerText = Math.max(0, parseInt(document.getElementById('quantity_{index}').innerText) - 1)">-</button>
                <span id="quantity_{index}">{st.session_state.quantities[index]}</span>
                <button onclick="document.getElementById('quantity_{index}').innerText = parseInt(document.getElementById('quantity_{index}').innerText) + 1">+</button>
            </td>
            <td>{row['Calories']} kcal</td>
            <td><a href="{row['Suggested Recipes']}">Suggested Recipes</a></td>
            <td><a href="{row['Nearby Locations']}">Nearby Locations</a></td>
        </tr>
        """, unsafe_allow_html=True)

    st.write("</table>", unsafe_allow_html=True)
    
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
        
    st.sidebar.title("Smart Pantry")
    options = ["Sign Up", "Sign In", "My Pantry Dashboard", "Profile Page", "Dashboard", "Ingredients"]
    choice = st.sidebar.radio("Select a Page", options, key="page")

    if choice == "Sign Up":
        signup()
    elif choice == "Sign In":
        signin()
    elif choice == "My Pantry Dashboard":
        pantry_dashboard()
    elif choice == "Profile Page":
        show_profile()
    elif choice == "Dashboard":
        show_dashboard()
    elif choice == "Ingredients":
        show_ingredients()

if __name__ == "__main__":
    main()